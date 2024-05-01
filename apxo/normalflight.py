"""
Normal flight for aircraft.
"""

import math
import re
from apxo.math import *

import apxo.airtoair       as apairtoair
import apxo.altitude       as apaltitude
import apxo.aircraft       as apaircraft
import apxo.capabilities   as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.configuration  as apconfiguration
import apxo.flight         as apflight
import apxo.hex            as aphex
import apxo.speed          as apspeed
import apxo.stores         as apstores
import apxo.turnrate       as apturnrate
import apxo.variants       as apvariants

from apxo.log import plural

def checkflight(A):

  if apcapabilities.hasproperty(A, "SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform normal flight.")

  flighttype         = A._flighttype
  previousflighttype = A._previousflighttype

  # See rule 13.3.5. A HRD is signalled by appending "/HRD" to the flight type.
  if flighttype[-4:] == "/HRD":

    if apcapabilities.hasproperty(A, "NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")

    hrd = True
    flighttype = flighttype[:-4]
    A._flighttype = flighttype

    # See rule 7.7.
    if A.altitude() > apcapabilities.ceiling(A):
      A._logevent("check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
    elif A.altitudeband() == "EH" or A.altitudeband() == "UH":
      A._logevent("check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % A.altitudeband())  
      
  else:

    hrd = False

  A._hrd = hrd

  if flighttype not in ["LVL", "SC", "ZC", "VC", "SD", "UD", "VD"]:
    raise RuntimeError("invalid flight type %r." % flighttype)

  # See rule 13.3.5 for restrictions on HRDs.

  if hrd:
    if previousflighttype == "LVL" and flighttype == "VD":
      pass
    elif (previousflighttype == "ZC" or previousflighttype == "SC") and flighttype == "VD":
      pass
    elif previousflighttype == "VC" and flighttype == "SD":
      pass
    else:
      raise RuntimeError("flight type immediately after %s cannot be %s with a HRD." % (
        previousflighttype, flighttype
      ))

  if previousflighttype == "DP":

    # See rule 6.4 on recovering from departed flight.

    if _isclimbingflight(flighttype):
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))
    elif flighttype == "LVL" and not apcapabilities.hasproperty(A, "HPR"):
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))
    
  if previousflighttype == "ST":

    # See rule 6.4 on recovering from stalled flight.

    if _isclimbingflight(flighttype):
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))

  if flighttype == "LVL":

    # See rule 8.2.3 on VD recovery.

    if previousflighttype == "VD":
      if apvariants.withvariant("use version 2.4 rules") and A.speed() <= 2.0:
        pass
      elif not apcapabilities.hasproperty(A, "HPR"):
        raise RuntimeError("flight type immediately after %s cannot be %s." % (
          previousflighttype, flighttype
        ))
      elif A.speed() >= 3.5:
        raise RuntimeError("flight type immediately after %s cannot be %s (for HPR aircraft at high speed)." % (
          previousflighttype, flighttype
        ))

  elif flighttype == "ZC":

    # See rule 8.2.3 on VD recovery.

    if previousflighttype == "VD":
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))
      
  elif flighttype == "SC":

    # See rule 8.1.2 on SC prerequsistes.

    if A.speed() < apcapabilities.minspeed(A) + 1:
      raise RuntimeError("insufficient speed for SC.")

    # See rule 8.2.3 on VD recovery.

    if previousflighttype == "VD":
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))

  elif flighttype == "VC":

    # See rule 8.1.3 on VC prerequisites.

    if _isdivingflight(previousflighttype):
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))      
    if previousflighttype == "LVL":
      if not apcapabilities.hasproperty(A, "HPR"):
        raise RuntimeError("flight type immediately after %s cannot be %s." % (
          previousflighttype, flighttype
        ))
      elif A.speed() >= 4.0:
        raise RuntimeError("flight type immediately after %s cannot be %s (for HPR aircraft at high speed)." % (
          previousflighttype, flighttype
        ))

    # See rule 8.2.3 on VD recovery.

    if previousflighttype == "VD":
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))
        
  elif flighttype == "SD":

    # See rule 8.1.3 on VC restrictions.
    # See rule 13.3.5 on HRD restrictions.

    if previousflighttype == "VC" and not (apcapabilities.hasproperty(A, "HPR") or hrd):
      raise RuntimeError("flight type immediately after %s cannot be %s (without a HRD)." % (
        previousflighttype, flighttype
      ))

  elif flighttype == "UD":

    # See rule 8.2.2 on VC restrictions.

    if apvariants.withvariant("use version 2.4 rules"):

      # I interpret the text "start from level flight" to mean that the aircraft
      # must have been in level flight on the previous turn.

      if previousflighttype != "LVL":
        raise RuntimeError("flight type immediately after %s cannot be %s." % (
          previousflighttype, flighttype
        ))

    else:

      # See rule 8.1.3 on VC restrictions.

      if previousflighttype == "VC" and not apcapabilities.hasproperty(A, "HPR"):
        raise RuntimeError("flight type immediately after %s cannot be %s." % (
          previousflighttype, flighttype
        ))

  elif flighttype == "VD":

    # See rule 8.2.3 (with errata) on VD restrictions.
    # See rule 13.3.5 on HRD restrictions.

    if previousflighttype == "LVL":
      if not hrd:
        raise RuntimeError("flight type immediately after %s cannot be %s (without a HRD)." % (
          previousflighttype, flighttype
        ))
    elif (previousflighttype == "ZC" or previousflighttype == "SC"):
      if hrd and A.speed() > 4.0:
        raise RuntimeError("flight type immediately after %s cannot be %s (without a low-speed HRD)." % (
          previousflighttype, flighttype
        ))
    elif previousflighttype == "VC":
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))

    # See rule 8.1.3 on VC restrictions. This duplicates the restriction above.

    if previousflighttype == "VC":
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))  

################################################################################

def continueflight(A, actions, note=False):

  """
  Continue to carry out out normal flight.
  """

  ########################################

  def invalidelement(element):
    raise RuntimeError("%r is not a valid element." % element)

  ########################################

  def dohorizontal(element):

    """
    Move horizontally.
    """

    if A._maneuvertype == "VR":
      raise RuntimeError("attempt to declare a vertical roll during an HFP.")
      
    altitudechange = 0

    A._horizontal = True
    A._fp += 1
    A._hfp += 1

    if element == "HD":

      if flighttype == "LVL":
        altitudechange = 1
      else:
        raise RuntimeError("%r is not a valid element when the flight type is %s." % (element, A._flighttype))

    elif element == "HU":

      if flighttype != "UD":
        raise RuntimeError("%r is not a valid element when the flight type is %s." % (element, A._flighttype))

      A._hasunloaded = True
      A._unloadedhfp += 1
      if A._firstunloadedfp == None:
        A._firstunloadedfp = A._hfp
      A._lastunloadedfp = A._hfp

      if apvariants.withvariant("use version 2.4 rules"):
        if math.floor(A._maxfp) == 1:
          # Both half FPs and all FPs.
          altitudechange = 2
        elif A._unloadedhfp == math.floor(A._maxfp / 2):
          altitudechange = 1
        elif A._unloadedhfp == math.floor(A._maxfp):
          altitudechange = 1
      else:
        altitudechange = 1

    A._dodive(altitudechange)
    A._doforward()

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    def determinealtitudechange(altitudechange):

      assert altitudechange == 1 or altitudechange == 2 or altitudechange == 3
    
      climbcapability = A._effectiveclimbcapability

      if flighttype == "ZC":

        # See rule 8.1.1.
        if altitudechange == 2:
          if climbcapability <= 2.0:
            raise RuntimeError("invalid altitude change in climb.")
        elif altitudechange == 3:
          if not apvariants.withvariant("use version 2.4 rules"):
            raise RuntimeError("invalid altitude change in climb.")
          if climbcapability < 6.0:
            raise RuntimeError("invalid altitude change in climb.")
          if A._usedsuperclimb:
            raise RuntimeError("invalid altitude change in climb.")
          A._usedsuperclimb = True

      elif flighttype == "SC":

        # See rule 8.1.2.
        if A.speed() < apcapabilities.climbspeed(A):
          climbcapability /= 2
        if climbcapability < 2.0 and altitudechange == 2:
          raise RuntimeError("invalid altitude change in climb.")
        if A._vfp == 0 and climbcapability % 1 != 0:
          # First VFP with fractional climb capability.
          altitudechange = climbcapability % 1

      elif flighttype == "VC":

        # See rule 8.1.3.
        if altitudechange != 1 and altitudechange != 2:
          raise RuntimeError("invalid altitude change in climb.")

      else:

        # See rule 8.0.
        raise RuntimeError("attempt to climb while flight type is %s." % A._flighttype)

      return altitudechange

    if A._hfp < A._mininitialhfp:
      raise RuntimeError("insufficient initial HFPs.")
      
    altitudechange = determinealtitudechange(altitudechange)
    
    A._vertical = True
    A._fp += 1  
    A._vfp += 1

    A._doclimb(altitudechange)

    # See rule 8.5.
    if flighttype == "SC" and A.altitude() > apcapabilities.ceiling(A):
      raise RuntimeError("attempt to climb above ceiling in SC.")

  ########################################

  def dodive(altitudechange):

    """
    Dive.
    """

    def checkaltitudechange():

      assert altitudechange == 1 or altitudechange == 2 or altitudechange == 3

      if flighttype == "SD":

        # See rule 8.2.1.
        if altitudechange != 1 and altitudechange != 2:
          raise RuntimeError("attempt to dive %d levels per VFP while the flight type is SC." % altitudechange)
  
      elif flighttype == "UD":

        # See rule 8.2.2.
        if altitudechange != 1:
          raise RuntimeError("attempt to dive %d levels per unloaded HFP while the flight type is UL." % altitudechange)

      elif flighttype == "VD":

        # See rule 8.2.3.
        if altitudechange != 2 and altitudechange != 3: 
          raise RuntimeError("attempt to dive %s per VFP while the flight type is VD." % 
            plural(altitudechange, "1 level", "%d levels" % altitudechange))

      elif flighttype == "LVL":

        # See rule 8.2.4.
        if altitudechange != 1:
          raise RuntimeError("attempt to descend %d levels while flight type is LVL." % altitudechange)

      else:

        # See rule 8.0.
        raise RuntimeError("attempt to dive while flight type is %s." % A._flighttype)
    
    checkaltitudechange()

    if A._hfp < A._mininitialhfp:
      raise RuntimeError("insufficient initial HFPs.")
      
    A._vertical = True
    A._fp += 1  
    A._vfp += 1
  
    A._dodive(altitudechange)

  ########################################

  def dobank(sense):

    if A._hasbanked:
      raise RuntimeError("attempt to bank twice.")

    # See rule 7.4.
    if apcapabilities.hasproperty(A, "LRR"):
      if (A._bank == "L" and sense == "R") or (A._bank == "R" and sense == "L"):
        raise RuntimeError("attempt to bank to %s while banked to %s in a LRR aircraft." % (sense, A._bank))

    A._bank = sense
    if _isturn(A._maneuvertype):
      A._maneuvertype         = None
      A._maneuversense        = None
      A._maneuverfacingchange = None
      A._maneuverfp           = 0

    A._hasbanked = True

  ########################################

  def dodeclareturn(turnrate, sense):

    """
    Declare the start of turn in the specified direction and rate.
    """

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare turn while flight type is %s." % flighttype)
      
    # See rule 7.1.

    # Check the bank. See rule 7.4.
    if apcapabilities.hasproperty(A, "LRR"):
      if A._bank != sense:
        raise RuntimeError("attempt to declare a turn to %s while not banked to %s in a LRR aircraft." % (sense, sense))
    elif not apcapabilities.hasproperty(A, "HRR"):
      if (A._bank == "L" and sense == "R") or (A._bank == "R" and sense == "L"):
        raise RuntimeError("attempt to declare a turn to %s while banked to %s." % (sense, A._bank))

    if A._allowedturnrates == []:
      raise RuntimeError("turns are forbidded.")

    if turnrate not in A._allowedturnrates:
      raise RuntimeError("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")

    turnrateap = apcapabilities.turndrag(A, turnrate)
    if turnrateap == None:
      raise RuntimeError("attempt to declare a turn rate tighter than allowed by the aircraft.")

    # Determine the maximum turn rate.
    if A._maxturnrate == None:
      A._maxturnrate = turnrate
    else:
      turnrates = ["EZ", "TT", "HT", "BT", "ET"]
      A._maxturnrate = turnrates[max(turnrates.index(turnrate), turnrates.index(A._maxturnrate))]

    A._bank                 = sense
    A._maneuvertype         = turnrate
    A._maneuversense        = sense
    A._maneuverfp           = 0
    A._maneuversupersonic   = (A.speed() >= apspeed.m1speed(A.altitudeband()))
    turnrequirement = apturnrate.turnrequirement(A.altitudeband(), A.speed(), A._maneuvertype)
    if turnrequirement == None:
      raise RuntimeError("attempt to declare a turn rate tighter than allowed by the speed and altitude.")
    if turnrequirement >= 60:
      A._maneuverrequiredfp   = 1
      A._maneuverfacingchange = turnrequirement
    else:
      A._maneuverrequiredfp   = turnrequirement
      A._maneuverfacingchange = 30

  ########################################

  def doturn(sense, facingchange, continuous):

    """
    Turn in the specified sense and amount.
    """

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to turn while flight type is %s." % flighttype)
      
    # See rule 7.1.
    if A._maneuverfp < A._maneuverrequiredfp or facingchange > A._maneuverfacingchange:
      raise RuntimeError("attempt to turn faster than the declared turn rate.")

    # See Hack's article in APJ 36
    if A._turnmaneuvers == 0:
      sustainedfacingchanges = facingchange // 30 - 1
    else:
      sustainedfacingchanges = facingchange // 30

    if apvariants.withvariant("use version 2.4 rules"):
      if apcapabilities.hasproperty(A, "LBR"):
        A._sustainedturnap -= sustainedfacingchanges * 0.5
      elif apcapabilities.hasproperty(A, "HBR"):
        A._sustainedturnap -= sustainedfacingchanges * 1.5
      else:
        A._sustainedturnap -= sustainedfacingchanges * 1.0
    else:
      if apcapabilities.hasproperty(A, "HBR"):
        A._sustainedturnap -= sustainedfacingchanges * 2.0
      else:
        A._sustainedturnap -= sustainedfacingchanges * 1.0

    A._turnmaneuvers += 1

    A._doturn(sense, facingchange)

  ########################################

  def dodeclareslide(sense):

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare slide while flight type is %s." % flighttype)

    # See rules 13.1 and 13.2.

    if A._slides == 1 and A.speed() <= 9.0:
      raise RuntimeError("only one slide allowed per turn at low speed.")
    if A._slides == 1 and A._fp - A._slidefp <  4:
      raise RuntimeError("attempt to start a second slide without sufficient intermediate FPs.")
    elif A._slides == 2:
      raise RuntimeError("at most two slides allowed per turn.")

    A._bank                 = None
    A._maneuvertype         = "SL"
    A._maneuversense        = sense
    A._maneuverfacingchange = None
    A._maneuverfp           = 0
    A._maneuversupersonic   = (A.speed() >= apspeed.m1speed(A.altitudeband()))
    # The requirement has +1 FP to account for the final H.
    A._maneuverrequiredfp   = 2 + extrapreparatoryhfp() + 1

  ########################################

  def extrapreparatoryhfp():

    # See rule 13.1.

    extrapreparatoryfp = { "LO": 0, "ML": 0, "MH": 0, "HI": 1, "VH": 2, "EH": 3, "UH": 4 }[A.altitudeband()]

    if A.speed() >= apspeed.m1speed(A.altitudeband()):
      extrapreparatoryfp += 1.0

    # See "Aircraft Damage Effects" in the Play Aids.

    if A.damageatleast("2L"):
      extrapreparatoryfp += 1.0

    return extrapreparatoryfp

  ########################################

  def doslide(sense):

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to slide while flight type is %s." % flighttype)

    # See rules 13.1 and 13.2.

    if A._maneuverfp < A._maneuverrequiredfp:
      raise RuntimeError("attempt to slide without sufficient preparatory HFPs.")

    # Move.
    A._doslide(sense)

    # See rule 13.2.
    if A._slides >= 1:
      A._othermaneuversap -= 1.0

    # Keep track of the number of slides and the FP of the last slide.
    A._slides += 1
    A._slidefp = A._fp

    # Implicitly finish with wings level.
    A._bank = None

  ########################################

  def dodeclaredisplacementroll(sense):

    # See rules 13.1 and 13.3.1.

    if apcapabilities.hasproperty(A, "NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if apcapabilities.rolldrag(A, "DR") == None:
      raise RuntimeError("aircraft cannot perform displacement rolls.")
      
    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if flighttype == "SC" or flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare a displacement roll while flight type is %s." % flighttype)

    A._bank                 = None
    A._maneuvertype         = "DR"
    A._maneuversense        = sense
    A._maneuverfacingchange = None
    A._maneuverfp           = 0
    A._maneuversupersonic   = (A.speed() >= apspeed.m1speed(A.altitudeband()))
    # The requirement includes the FPs used to execute the roll.
    if apvariants.withvariant("use version 2.4 rules"):
      A._maneuverrequiredfp   = apcapabilities.rollhfp(A) + extrapreparatoryhfp() + rounddown(A.speed() / 3)
    else:
      A._maneuverrequiredfp   = apcapabilities.rollhfp(A) + extrapreparatoryhfp() + 1

  ########################################

  def dodisplacementroll(sense):

    # See rules 13.1 and 13.3.1.

    if A._maneuverfp < A._maneuverrequiredfp:
      raise RuntimeError("attempt to roll without sufficient preparatory FPs.")

    if not A._horizontal:
      raise RuntimeError("attempt to roll on a VFP.")
      
    # Move.
    A._dodisplacementroll(sense)

    # See rule 13.3.1.
    A._othermaneuversap -= apcapabilities.rolldrag(A, "DR")

    # See rule 6.6.
    if A._maneuversupersonic:
      if apcapabilities.hasproperty(A, "PSSM"):
        A._othermaneuversap -= 2.0
      elif not apcapabilities.hasproperty(A, "GSSM"):
        A._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if A._rollmaneuvers > 0:
      A._othermaneuversap -= 1.0
    A._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    A._bank = None
    
  ########################################

  def dodeclarelagroll(sense):

    # See rule 13.3.2.

    if apcapabilities.hasproperty(A, "NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if apcapabilities.rolldrag(A, "LR") == None:
      raise RuntimeError("aircraft cannot perform lag rolls.")
      
    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if flighttype == "SC" or flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare a lag roll while flight type is %s." % flighttype)

    A._bank                 = None
    A._maneuvertype         = "LR"
    A._maneuversense        = sense
    A._maneuverfacingchange = None
    A._maneuverfp           = 0
    A._maneuversupersonic   = (A.speed() >= apspeed.m1speed(A.altitudeband()))
    # The requirement includes the FPs used to execute the roll.
    if apvariants.withvariant("use version 2.4 rules"):
      A._maneuverrequiredfp   = apcapabilities.rollhfp(A) + extrapreparatoryhfp() + rounddown(A.speed() / 3)
    else:
      A._maneuverrequiredfp   = apcapabilities.rollhfp(A) + extrapreparatoryhfp() + 1

  ########################################

  def dolagroll(sense):

    # See rules 13.1 and 13.3.2.

    if A._maneuverfp < A._maneuverrequiredfp:
      raise RuntimeError("attempt to roll without sufficient preparatory FPs.")

    if not A._horizontal:
      raise RuntimeError("attempt to roll on a VFP.")

    # Move.
    A._dolagroll(sense)

    # See rule 13.3.1.
    A._othermaneuversap -= apcapabilities.rolldrag(A, "LR")

    # See rule 6.6.
    if A._maneuversupersonic:
      if apcapabilities.hasproperty(A, "PSSM"):
        A._othermaneuversap -= 2.0
      elif not apcapabilities.hasproperty(A, "GSSM"):
        A._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if A._rollmaneuvers > 0:
      A._othermaneuversap -= 1.0
    A._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    A._bank = None
    
  ########################################  

  def dodeclareverticalroll(sense):

    if apcapabilities.hasproperty(A, "NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if A._verticalrolls == 1 and apcapabilities.hasproperty(A, "OVR"):
      raise RuntimeError("aircraft can only perform one vertical roll per turn.")
      
    # See rule 13.3.4.  
    if A._flighttype != "VC" and A._flighttype != "VD":
      raise RuntimeError("attempt to declare a vertical roll while flight type is %s." % A._flighttype)
    if previousflighttype == "LVL" and flighttype == "VC" and not A._lastfp:
      raise RuntimeError("attempt to declare a vertical roll in VC following LVL flight other than on the last FP.")

    # See rule 13.3.5.
    if A._hrd and not A._lastfp:
      raise RuntimeError("attempt to declare a vertical roll after HRD other than on the last FP.")
      
    A._bank                 = None
    A._maneuvertype         = "VR"
    A._maneuversense        = sense
    A._maneuverfacingchange = None
    A._maneuverfp           = 0
    A._maneuversupersonic   = (A.speed() >= apspeed.m1speed(A.altitudeband()))
    A._maneuverrequiredfp   = 1
  
  ########################################

  def doverticalroll(sense, facingchange, shift):

    if A._maneuverfp < A._maneuverrequiredfp:
      raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")
  
    # See rule 13.3.4.
    if apcapabilities.hasproperty(A, "LRR") and facingchange > 90:
      raise RuntimeError("attempt to roll vertically by more than 90 degrees in LRR aircraft.")

    A._othermaneuversap -= apcapabilities.rolldrag(A, "VR")

    # See rule 13.3.6
    if A._rollmaneuvers > 0:
      A._othermaneuversap -= 1
    A._rollmaneuvers += 1
    A._verticalrolls += 1

    # See rule 6.6.
    if A._maneuversupersonic:
      if apcapabilities.hasproperty(A, "PSSM"):
        A._othermaneuversap -= 2.0
      elif not apcapabilities.hasproperty(A, "GSSM"):
        A._othermaneuversap -= 1.0

    # Move.
    A._doverticalroll(sense, facingchange, shift)
      
  ########################################

  def dodeclaremaneuver(maneuvertype, sense):

    if A._hasdeclaredamaneuver:
      raise RuntimeError("attempt to declare a second maneuver.")
      
    if maneuvertype == "SL":
      dodeclareslide(sense)
    elif maneuvertype == "DR":
      dodeclaredisplacementroll(sense)
    elif maneuvertype == "LR":
      dodeclarelagroll(sense)
    elif maneuvertype == "VR":
      dodeclareverticalroll(sense)
    else:
      dodeclareturn(maneuvertype, sense)
      
    A._logevent("declared %s." % A.maneuver())
    A._hasdeclaredamaneuver = True

  ########################################

  def domaneuver(sense, facingchange, shift, continuous):

    if A._maneuvertype == None:
      raise RuntimeError("attempt to maneuver without a declaration.")
      
    if A._maneuversense != sense:
      raise RuntimeError("attempt to maneuver against the sense of the declaration.")

    if A._maneuvertype == "SL":
      if facingchange != None:
        raise RuntimeError("invalid element for a slide.")
      doslide(sense)
    elif A._maneuvertype == "DR":
      if facingchange != None:
        raise RuntimeError("invalid element for a displacement roll.")
      dodisplacementroll(sense)
    elif A._maneuvertype == "LR":
      if facingchange != None:
        raise RuntimeError("invalid element for a lag roll.")
      dolagroll(sense)
    elif A._maneuvertype == "VR":
      if facingchange == None:
        facingchange = 30
      doverticalroll(sense, facingchange, shift)
    else:
      if facingchange == None:
        facingchange = 30
      doturn(sense, facingchange, continuous)

    A._hasmaneuvered = True
    A._maneuverfp = 0

    if not continuous:
      A._maneuvertype         = None
      A._maneuversense        = None
      A._maneuverfacingchange = None
      A._maneuverrequiredfp   = 0
      A._maneuversupersonic   = False
    else:
      A._hasdeclaredamaneuver = False
      dodeclaremaneuver(A._maneuvertype, A._maneuversense)

  ########################################

  def dospeedbrakes(spbr):

    """
    Use the speedbrakes.
    """

    # See rules 6.5 and 6.6.

    if A._spbrap != 0:
      raise RuntimeError("speedbrakes can only be used once per turn.")
        
    maxspbr = apcapabilities.spbr(A)
    if maxspbr == None:
      raise RuntimeError("aircraft does not have speedbrakes.")
        
    if apvariants.withvariant("use version 2.4 rules"):

      maxspbr = apcapabilities.spbr(A)

      if A.speed() >= apspeed.m1speed(A.altitudeband()):
        maxspbr += 2.0      

      if spbr > maxspbr:
        raise RuntimeError(plural(maxspbr,
          "speedbrake capability is only 1 DP.",
          "speedbrake capability is only %.1f DPs." % maxspbr))
          
      A._spbrap = -spbr
          
    else:

      if A.speed() > apspeed.m1speed(A.altitudeband()):
        maxspbr += 0.5
        
      if spbr > maxspbr:
        raise RuntimeError(plural(maxspbr,
          "speedbrake capability is only 1 FP.",
          "speedbrake capability is only %.1f FPs." % maxspbr))
          
      maxspbr = A._maxfp - A._hfp - A._vfp
      if spbr >= maxspbr:
        raise RuntimeError(plural(maxspbr,
          "invalid use of speedbrakes when only 1 FP remains.",
          "invalid use of speedbrakes when only %s FPs remain." % maxspbr))

      A._spbrfp = spbr
      A._maxfp -= spbr

      A._spbrap = -spbr / 0.5
  
  ########################################

  def dojettison(m):

    # See rule 4.4.   
    # We implement the delay of 1 FP by making this an other element.
    
    previousconfiguration = A._configuration

    for released in m[1].split("+"):
      A._stores = apstores._release(A._stores, released,
        printer=lambda s: A._logevent(s)
      )

    apconfiguration.update(A)

    if A._configuration != previousconfiguration:
      A._logevent("configuration changed from %s to %s." % (
        previousconfiguration, A._configuration
      ))

  ########################################

  def doataattack(m):

    """
    Declare an air-to-air attack.
    """

    if useofweaponsforbidden():
      raise RuntimeError("attempt to use weapons %s." % useofweaponsforbidden())

    attacktype   = m[1]
    targetname   = m[2]
    result       = m[3]

    if targetname == "":
      target = None
    else:
      target = apaircraft.fromname(targetname)
      if target is None:
        raise RuntimeError("unknown target aircraft %s." % targetname)
      
    apairtoair.attack(A, attacktype, target, result)

  ########################################

  def dossgt(m):

    """
    Start SSGT.
    """

    # See rule 9.4.

    # The rules only explicitly prohibit SSGT during recovery from an
    # ET. However, we assume that SSGT has the same restrictions as
    # attacks.

    if useofweaponsforbidden():
      raise RuntimeError("attempt to start SSGT while %s" % useofweaponsforbidden())

    # TODO: Check we can start SSGT on a specific target.

    targetname = m[1]

    target = apaircraft.fromname(targetname)
    if target is None:
      raise RuntimeError("unknown target aircraft %s." % targetname)

    if apairtoair.trackingforbidden(A, target):
      raise RuntimeError("attempt to start SSGT while %s" %  apairtoair.trackingforbidden(A, target))

    A._logevent("started SSGT on %s." % targetname)
    A._tracking = target

  ########################################

  def domaneuveringdeparture(sense, facingchange):

    # Do the first facing change.
    A._doturn(sense, 30)
    A._flightpath.next(A.x(), A.y(), A.facing(), A.altitude())
    facingchange -= 30

    # Shift.

    shift = int((A._maxfp - A._fp) / 2)
    for i in range(0, shift):
      A._doforward()
      A.checkforterraincollision()
      A.checkforleavingmap()
      if A._destroyed or A._leftmap:
        return

    # Do any remaining facing changes.
    A._doturn(sense, facingchange)
    A._flightpath.next(A.x(), A.y(), A.facing(), A.altitude())

  ########################################

  def argsregex(n):
    """
    Return a regex to match n arguments.
    """
    return r"\(([^)]*)\)" * n

  elementdispatchlist = [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

    # [0] is the element code.
    # [1] is the element type.
    # [2] is a possible regex to apply
    # [3] is the element procedure.
  
    ["SLL"   , "prolog"             , None, lambda: dodeclaremaneuver("SL", "L") ],
    ["SLR"   , "prolog"             , None, lambda: dodeclaremaneuver("SL", "R") ],

    ["DRL"   , "prolog"             , None, lambda: dodeclaremaneuver("DR", "L") ],
    ["DRR"   , "prolog"             , None, lambda: dodeclaremaneuver("DR", "R") ],

    ["LRL"   , "prolog"             , None, lambda: dodeclaremaneuver("LR", "L") ],
    ["LRR"   , "prolog"             , None, lambda: dodeclaremaneuver("LR", "R") ],
        
    ["VRL"   , "prolog"             , None, lambda: dodeclaremaneuver("VR", "L") ],
    ["VRR"   , "prolog"             , None, lambda: dodeclaremaneuver("VR", "R") ],
    
    ["EZL"   , "prolog"             , None, lambda: dodeclaremaneuver("EZ", "L") ],
    ["TTL"   , "prolog"             , None, lambda: dodeclaremaneuver("TT", "L") ],
    ["HTL"   , "prolog"             , None, lambda: dodeclaremaneuver("HT", "L") ],
    ["BTL"   , "prolog"             , None, lambda: dodeclaremaneuver("BT", "L") ],
    ["ETL"   , "prolog"             , None, lambda: dodeclaremaneuver("ET", "L") ],
    
    ["EZR"   , "prolog"             , None, lambda: dodeclaremaneuver("EZ", "R") ],
    ["TTR"   , "prolog"             , None, lambda: dodeclaremaneuver("TT", "R") ],
    ["HTR"   , "prolog"             , None, lambda: dodeclaremaneuver("HT", "R") ],
    ["BTR"   , "prolog"             , None, lambda: dodeclaremaneuver("BT", "R") ],
    ["ETR"   , "prolog"             , None, lambda: dodeclaremaneuver("ET", "R") ],
    
    ["SSGT"  , "prolog"             , argsregex(1), lambda m: dossgt(m) ],

    ["S1/2"  , "prolog"             , None, lambda: dospeedbrakes(1/2) ],
    ["S1"    , "prolog"             , None, lambda: dospeedbrakes(1)   ],
    ["S3/2"  , "prolog"             , None, lambda: dospeedbrakes(3/2) ],
    ["S2"    , "prolog"             , None, lambda: dospeedbrakes(2)   ],
    ["S5/2"  , "prolog"             , None, lambda: dospeedbrakes(5/2) ],
    ["S3"    , "prolog"             , None, lambda: dospeedbrakes(3)   ],
    ["S7/2"  , "prolog"             , None, lambda: dospeedbrakes(7/2) ],
    ["S4"    , "prolog"             , None, lambda: dospeedbrakes(4)   ],
    ["SSSS"  , "prolog"             , None, lambda: dospeedbrakes(4)   ],
    ["SSS"   , "prolog"             , None, lambda: dospeedbrakes(3)   ],
    ["SS"    , "prolog"             , None, lambda: dospeedbrakes(2)   ],
    ["S"     , "prolog"             , None, lambda: dospeedbrakes(1)   ],
    
    ["BL"    , "epilog"             , None, lambda: dobank("L")  ],
    ["BR"    , "epilog"             , None, lambda: dobank("R")  ],
    ["WL"    , "epilog"             , None, lambda: dobank(None) ],

    ["L90+"  , "epilog"             , None, lambda: domaneuver("L",   90, True , True ) ],
    ["L60+"  , "epilog"             , None, lambda: domaneuver("L",   60, True , True ) ],
    ["L30+"  , "epilog"             , None, lambda: domaneuver("L",   30, True , True ) ],
    ["LLL+"  , "epilog"             , None, lambda: domaneuver("L",   90, True , True ) ],
    ["LL+"   , "epilog"             , None, lambda: domaneuver("L",   60, True , True ) ],
    ["L+"    , "epilog"             , None, lambda: domaneuver("L", None, True , True ) ],
    
    ["R90+"  , "epilog"             , None, lambda: domaneuver("R",   90, True , True ) ],
    ["R60+"  , "epilog"             , None, lambda: domaneuver("R",   60, True , True ) ],
    ["R30+"  , "epilog"             , None, lambda: domaneuver("R",   30, True , True ) ],
    ["RRR+"  , "epilog"             , None, lambda: domaneuver("R",   90, True , True ) ],
    ["RR+"   , "epilog"             , None, lambda: domaneuver("R",   60, True , True ) ],
    ["R+"    , "epilog"             , None, lambda: domaneuver("R", None, True , True ) ],    

    ["LS180" , "epilog"             , None, lambda: domaneuver("L",  180, True , False) ],
    ["L180"  , "epilog"             , None, lambda: domaneuver("L",  180, False, False) ],
    ["L150"  , "epilog"             , None, lambda: domaneuver("L",  150, True , False) ],
    ["L120"  , "epilog"             , None, lambda: domaneuver("L",  120, True , False) ],
    ["L90"   , "epilog"             , None, lambda: domaneuver("L",   90, True , False) ],
    ["L60"   , "epilog"             , None, lambda: domaneuver("L",   60, True , False) ],
    ["L30"   , "epilog"             , None, lambda: domaneuver("L",   30, True , False) ],
    ["LLL"   , "epilog"             , None, lambda: domaneuver("L",   90, True , False) ],
    ["LL"    , "epilog"             , None, lambda: domaneuver("L",   60, True , False) ],
    ["L"     , "epilog"             , None, lambda: domaneuver("L", None, True , False) ],

    ["RS180" , "epilog"             , None, lambda: domaneuver("R",  180, True , False) ],
    ["R180"  , "epilog"             , None, lambda: domaneuver("R",  180, False, False) ],
    ["R150"  , "epilog"             , None, lambda: domaneuver("R",  150, True , False) ],
    ["R120"  , "epilog"             , None, lambda: domaneuver("R",  120, True , False) ],
    ["R90"   , "epilog"             , None, lambda: domaneuver("R",   90, True , False) ],
    ["R60"   , "epilog"             , None, lambda: domaneuver("R",   60, True , False) ],
    ["R30"   , "epilog"             , None, lambda: domaneuver("R",   30, True , False) ],
    ["RRR"   , "epilog"             , None, lambda: domaneuver("R",   90, True , False) ],
    ["RR"    , "epilog"             , None, lambda: domaneuver("R",   60, True , False) ],
    ["R"     , "epilog"             , None, lambda: domaneuver("R", None, True , False) ],
    
    ["AA"    , "epilog"             , argsregex(3), lambda m: doataattack(m) ],

    ["J"     , "epilog"             , argsregex(1), lambda m: dojettison(m) ],

    ["HC1"   , "FP"                 , None, lambda: invalidelement("HC1")  ],
    ["HC2"   , "FP"                 , None, lambda: invalidelement("HC2")  ],
    ["HCC"   , "FP"                 , None, lambda: invalidelement("HCC")  ],
    ["HC"    , "FP"                 , None, lambda: invalidelement("HC")   ],
    
    ["HD1"   , "FP"                 , None, lambda: dohorizontal("HD")     ],
    ["HD2"   , "FP"                 , None, lambda: invalidelement("HD2")  ],
    ["HD3"   , "FP"                 , None, lambda: invalidelement("HD3")  ],
    ["HDDD"  , "FP"                 , None, lambda: invalidelement("HDDD") ],
    ["HDD"   , "FP"                 , None, lambda: invalidelement("HDD")  ],
    ["HD"    , "FP"                 , None, lambda: dohorizontal("HD")     ],

    ["HU"   , "FP"                  , None, lambda: dohorizontal("HU")     ],

    ["H"    , "FP"                  , None, lambda: dohorizontal("H")      ],

    ["C1"   , "FP"                  , None, lambda: doclimb(1) ],
    ["C2"   , "FP"                  , None, lambda: doclimb(2) ],
    ["C3"   , "FP"                  , None, lambda: doclimb(3) ],
    ["CCC"  , "FP"                  , None, lambda: doclimb(3) ],
    ["CC"   , "FP"                  , None, lambda: doclimb(2) ],
    ["C"    , "FP"                  , None, lambda: doclimb(1) ],

    ["D1"   , "FP"                  , None, lambda: dodive(1) ],
    ["D2"   , "FP"                  , None, lambda: dodive(2) ],
    ["D3"   , "FP"                  , None, lambda: dodive(3) ],
    ["DDD"  , "FP"                  , None, lambda: dodive(3) ],
    ["DD"   , "FP"                  , None, lambda: dodive(2) ],
    ["D"    , "FP"                  , None, lambda: dodive(1) ],

    ["MDL300", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 300)],
    ["MDL270", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 270)],
    ["MDL240", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 240)],
    ["MDL210", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 210)],
    ["MDL180", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 180)],
    ["MDL150", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 150)],
    ["MDL120", "maneuvering departure", None, lambda: domaneuveringdeparture("L", 120)],
    ["MDL90" , "maneuvering departure", None, lambda: domaneuveringdeparture("L",  90)],
    ["MDL60" , "maneuvering departure", None, lambda: domaneuveringdeparture("L",  60)],
    ["MDL30" , "maneuvering departure", None, lambda: domaneuveringdeparture("L",  30)],
    
    ["MDR300", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 300)],
    ["MDR270", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 270)],
    ["MDR240", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 240)],
    ["MDR210", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 210)],
    ["MDR180", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 180)],
    ["MDR150", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 150)],
    ["MDR120", "maneuvering departure", None, lambda: domaneuveringdeparture("R", 120)],
    ["MDR90" , "maneuvering departure", None, lambda: domaneuveringdeparture("R",  90)],
    ["MDR60" , "maneuvering departure", None, lambda: domaneuveringdeparture("R",  60)],
    ["MDR30" , "maneuvering departure", None, lambda: domaneuveringdeparture("R",  30)],

    [""      , ""                     , None, None                                    ],

  ]

  ########################################

  def doelements(action, selectedelementtype):

    """
    Carry out the elements in an action that match the element type.
    """

    while action != "":

      if action[0] == "/" or action[0] == " ":
        action = action[1:]
        continue

      for element in elementdispatchlist:

        elementcode      = element[0]
        elementtype      = element[1]
        elementregex     = element[2]
        elementprocedure = element[3]

        if elementcode == action[:len(elementcode)]:
          break
          
      if selectedelementtype == "prolog" and elementtype == "epilog":
        raise RuntimeError("unexpected %s element in action prolog." % elementcode)
      if selectedelementtype == "epilog" and elementtype == "prolog":
        raise RuntimeError("unexpected %s element in action epilog." % elementcode)

      if selectedelementtype != elementtype:
        break

      if elementprocedure is None:
        break

      action = action[len(elementcode):]

      if elementregex == None:
        elementprocedure()
      else:
        m = re.compile(elementregex).match(action)
        if not m:
          raise RuntimeError("invalid arguments to %s element." % elementcode)
        action = action[len(m.group()):]   
        elementprocedure(m)

    return action
  
  ################################################################################

  def checkrecovery():

    # See rules 9.1 and 13.3.6. The +1 is because the recovery period is
    # this turn plus half of the speed, rounding down.

    if A._hasunloaded:
      A._unloadedrecoveryfp = int(A.speed() / 2) + 1
      A._ETrecoveryfp       -= 1
      A._BTrecoveryfp       = -1
      A._rollrecoveryfp     = -1
      A._HTrecoveryfp       = -1
      A._TTrecoveryfp       = -1
    elif A._maneuvertype == "ET":
      A._unloadedrecoveryfp = -1
      A._ETrecoveryfp       = int(A.speed() / 2) + 1
      A._BTrecoveryfp       = -1
      A._rollrecoveryfp     = -1
      A._HTrecoveryfp       = -1
      A._TTrecoveryfp       = -1
    elif A._maneuvertype == "BT":
      A._unloadedrecoveryfp -= 1
      A._ETrecoveryfp       -= 1
      A._BTrecoveryfp       = int(A.speed() / 2) + 1
      A._rollrecoveryfp     = -1
      A._HTrecoveryfp       = -1
      A._TTrecoveryfp       = -1
    elif A._maneuvertype in ["VR", "LR", "DR"] or (A._hrd and A._fp == 1):
      A._unloadedrecoveryfp -= 1
      A._ETrecoveryfp       -= 1
      A._BTrecoveryfp       = -1
      A._rollrecoveryfp     = int(A.speed() / 2) + 1
      A._HTrecoveryfp       = -1
      A._TTrecoveryfp       = -1
    elif A._maneuvertype == "HT":
      A._unloadedrecoveryfp -= 1
      A._ETrecoveryfp       -= 1
      A._BTrecoveryfp       -= 1
      A._rollrecoveryfp     -= 1
      A._HTrecoveryfp       = int(A.speed() / 2) + 1
      A._TTrecoveryfp       = -1
    elif A._maneuvertype == "TT":
      A._unloadedrecoveryfp -= 1
      A._ETrecoveryfp       -= 1
      A._BTrecoveryfp       -= 1
      A._rollrecoveryfp     -= 1
      A._HTrecoveryfp       -= 1
      A._TTrecoveryfp       = int(A.speed() / 2) + 1
      A._unloadedrecoveryfp -= 1
    else:
      A._unloadedrecoveryfp -= 1
      A._ETrecoveryfp       -= 1
      A._BTrecoveryfp       -= 1
      A._rollrecoveryfp     -= 1
      A._HTrecoveryfp       -= 1
      A._TTrecoveryfp       -= 1

    if A._ETrecoveryfp == 0:
      A._logevent("recovered from ET.")
    if A._BTrecoveryfp == 0:
      A._logevent("recovered from BT.")
    if A._rollrecoveryfp == 0:
      A._logevent("recovered from roll.")
    if A._HTrecoveryfp == 0:
      A._logevent("recovered from HT.")
    if A._TTrecoveryfp == 0:
      A._logevent("recovered from TT.")

  ################################################################################

  def useofweaponsforbidden():

    # See rule 8.2.2.
    if A._unloadedhfp:
      return "while unloaded"
    if A._unloadedrecoveryfp > 0:
      return "while recovering from being unloaded"

    # See rule 10.1.
    if A._maneuvertype == "ET":
      return "while in an ET"

    if A._ETrecoveryfp > 0:
      return "while recovering from an ET"

    # See rule 13.3.5.
    if A._hrd:
      return "after HRD"

    # See rule 13.3.6.
    if A._hasrolled and A._hasmaneuvered:
      return "immediately after rolling"
      
    # See rule 13.3.6.
    if A._hasrolled:
      return "while rolling"

    return False

  ################################################################################

  def checktracking():

    # See rule 9.4.
    if A._tracking:
      if useofweaponsforbidden():
        A._logevent("stopped SSGT.")
        A._tracking   = None
        A._trackingfp = 0
      elif apairtoair.trackingforbidden(A, A._tracking):
        A._logevent("stopped SSGT as %s" % apairtoair.trackingforbidden(A, A._tracking))
        A._tracking   = None
        A._trackingfp = 0
      else:        
        A._trackingfp += 1

  ########################################

  def doaction(action):

    """
    Carry out an action for normal flight.
    """

    A._log1("FP %d" % (A._fp + 1), action)

    # Check we have at least one FP remaining.
    if A._fp + 1 > A._maxfp:
      raise RuntimeError(plural(A._maxfp,
        "only 1 FP is available",
        "only %.1f FPs are available." % A._maxfp))

    # Determine if this FP is the last FP of the move.
    A._lastfp = (A._fp + 2 > A._maxfp) 
    
    initialaltitude     = A.altitude()
    initialaltitudeband = A.altitudeband()

    try:

      remainingaction = action

      remainingaction = doelements(remainingaction, "maneuvering departure")
      if remainingaction != action:
    
        A._maneuveringdeparture = True

        assert aphex.isvalid(A.x(), A.y(), facing=A.facing())
        assert apaltitude.isvalidaltitude(A.altitude())
  
        A._logposition("end")
        A._flightpath.next(A.x(), A.y(), A.facing(), A.altitude())
    
        return

      A._horizontal           = False
      A._vertical             = False
      
      A._hasunloaded          = False
      A._hasdeclaredamaneuver = False
      A._hasmaneuvered        = False
      A._hasrolled            = False
      A._hasbanked            = False

      remainingaction = doelements(remainingaction, "prolog")
      
      fp = A._fp
      remainingaction = doelements(remainingaction, "FP")
      if A._fp == fp:
        raise RuntimeError("%r is not a valid action as it does not expend an FP." % action)
      elif A._fp > fp + 1:
        raise RuntimeError("%r is not a valid action as it attempts to expend more than one FP." % action)

      # The climb slope is defined in APJ 39.
      if A._hfp != 0:
        A._climbslope = (A.altitude() - A._startaltitude) / float(A._hfp)
      elif A.altitude() > A._startaltitude:
        A._climbslope = +math.inf
      else:
        A._climbslope = -math.inf

      # We save maneuvertype, as A._maneuvertype may be set to None of the
      # maneuver is completed below.

      maneuvertype = A._maneuvertype
      A._hasturned = _isturn(A._maneuvertype)
      A._hasrolled = _isroll(A._maneuvertype)
      A._hasslid   = _isslide(A._maneuvertype)
      
      # See rule 8.2.2 and 13.1.
      if not A._hasunloaded:
        if A._hasturned:
          A._maneuverfp += 1
        elif A._maneuvertype == "VR" and A._vertical:
          A._maneuverfp += 1
        elif apvariants.withvariant("use version 2.4 rules") and (A._maneuvertype == "DR" or A._maneuvertype == "LR"):
          A._maneuverfp += 1
        elif A._horizontal:
          A._maneuverfp += 1
          
      if A._hasturned and A._maneuversupersonic:
        A._turningsupersonic = True

      checkrecovery()
      checktracking()
              
      remainingaction = doelements(remainingaction, "epilog")

      if A._hasbanked and A._hasmaneuvered and not A._hasrolled:
        raise RuntimeError("attempt to bank immediately after a maneuver that is not a roll.")

      if remainingaction != "":
        raise RuntimeError("%r is not a valid action." % action)

      assert aphex.isvalid(A.x(), A.y(), facing=A.facing())
      assert apaltitude.isvalidaltitude(A.altitude())

    except RuntimeError as e:

      raise e
  
    finally:
      if A._lastfp:
        A._logpositionandmaneuver("end")
      else:
        A._logpositionandmaneuver("")
      A._flightpath.next(A.x(), A.y(), A.facing(), A.altitude())
        
    # See rules 7.7 and 8.5.
    if A._hasmaneuvered and A._hasrolled:
      if initialaltitude > apcapabilities.ceiling(A):
        A._logevent("check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
      elif initialaltitudeband == "EH" or initialaltitudeband == "UH":
        A._logevent("check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % initialaltitudeband)
    
    # See rules 7.7 and 8.5.
    if A._hasmaneuvered and A._hasturned:
      if initialaltitude > apcapabilities.ceiling(A) and maneuvertype != "EZ":
        A._logevent("check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ.")
      if maneuvertype == "ET" and initialaltitude <= 25:
        A._gloccheck += 1
        A._logevent("check for GLOC as turn rate is ET and altitude band is %s (check %d in cycle)." % (initialaltitudeband, A._gloccheck))

    # See rule 7.8.
    if A._hasturned and apcloseformation.size(A) != 0:
      if (apcloseformation.size(A) > 2 and maneuvertype == "HT") or maneuvertype == "BT" or maneuvertype == "ET":
        A._logevent("close formation breaks down as the turn rate is %s." % maneuvertype)
        apcloseformation.breakdown(A)

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if A._hasrolled and apcloseformation.size(A) != 0:
      A._logevent("close formation breaks down aircraft is rolling.")
      apcloseformation.breakdown(A)
    
    if initialaltitudeband != A.altitudeband():
      A._logevent("altitude band changed from %s to %s." % (initialaltitudeband, A.altitudeband()))
      
    A.checkforterraincollision()
    A.checkforleavingmap()
    if A._destroyed or A._leftmap:
      return

    A._actions += (" %s," % action)

  ########################################
  
  flighttype         = A._flighttype
  previousflighttype = A._previousflighttype  
  
  if actions != "":
    for action in actions.split(","):
      if not A._destroyed and not A._leftmap:
        doaction(action)

  A._lognote(note)

  assert A._maneuveringdeparture or (A._fp == A._hfp + A._vfp)
  assert A._maneuveringdeparture or (A._fp <= A._maxfp)

  if A._destroyed or A._leftmap or A._maneuveringdeparture:
  
    # Remove initial space and final comma.
    A._actions = A._actions[1:-1]
  
    apflight.endmove(A)

  elif A._fp + 1 > A._maxfp:

    # See rule 5.4.
    A._fpcarry = A._maxfp - A._fp

    # Remove initial space and final comma.
    A._actions = A._actions[1:-1]
    
    endflight(A)
  
################################################################################

def startflight(A, actions, note=False):
      
  """
  Start to carry out normal flight.
  """

  ########################################

  def reportapcarry():
     A._logevent("is carrying %+.2f APs." % A._apcarry)
 
  ########################################

  def reportaltitudecarry():
    if A._altitudecarry != 0:
     A._logevent("is carrying %.2f altitude levels." % A._altitudecarry)
  
  ########################################

  def determineallowedturnrates():

    """
    Determine the allowed turn rates according to the flight type and
    speed. The aircraft type and configuration may impose additional
    restrictions.
    """

    turnrates = ["EZ", "TT", "HT", "BT", "ET"]

    # See "Aircraft Damage Effects" in Play Aids.

    if A.damageatleast("C"):
      A._logevent("damage limits the turn rate to TT.")
      turnrates = turnrates[:2]
    elif A.damageatleast("2L"):
      A._logevent("damage limits the turn rate to HT.")
      turnrates = turnrates[:3]
    elif A.damageatleast("L"):
      A._logevent("damage limits the turn rate to BT.")
      turnrates = turnrates[:4]

    # See rule 7.5.

    minspeed = apcapabilities.minspeed(A)
    if A.speed() == minspeed:
      A._logevent("speed limits the turn rate to EZ.")
      turnrates = turnrates[:1]
    elif A.speed() == minspeed + 0.5:
      A._logevent("speed limits the turn rate to TT.")
      turnrates = turnrates[:2]
    elif A.speed() == minspeed + 1.0:
      A._logevent("speed limits the turn rate to HT.")
      turnrates = turnrates[:3]
    elif A.speed() == minspeed + 1.5:
      A._logevent("speed limits the turn rate to BT.")
      turnrates = turnrates[:4]
    else:
      A._logevent("speed does not limit the turn rate.")

    # See rule 8.1.1.

    if A._flighttype == "ZC":
      A._logevent("ZC limits the turn rate to BT.")
      turnrates = turnrates[:4]

    # See rule 8.1.1.

    if A._flighttype == "SC":
      A._logevent("SC limits the turn rate to EZ.")
      turnrates = turnrates[:1]

    # See rule 8.1.3.

    if A._flighttype == "VC":
      A._logevent("VC disallows all turns.")
      turnrates = []

    A._allowedturnrates = turnrates

  ########################################

  def checkcloseformationlimits():

    if A.closeformationsize() == 0:
      return

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if A._hrd:
      A._logevent("close formation breaks down upon a HRD.")
      apcloseformation.breakdown(A)    

    # See rule 8.6.
    if flighttype == "ZC" or \
      (flighttype == "SC" and A._powersetting == "AB") or \
      flighttype == "VC" or \
      flighttype == "UD" or \
      flighttype == "VD":
      A._logevent("close formation breaks down as the flight type is %s." % flighttype)
      apcloseformation.breakdown(A)

    return

  ########################################

  def determinemaxfp():

    """
    Determine the number of FPs available, according to the speed and any 
    carried FPs.
    """

    # See rule 5.4.

    A._maxfp = A.speed() + A._fpcarry
    A._logevent("has %.1f FPs (including %.1f carry)." % (A._maxfp, A._fpcarry))
    A._fpcarry = 0

  ########################################

  def determinefprequirements():

    """
    Determine the requirements on the use of FPs.
    """

    # See rule 5.5.
    # See rule 13.3.5 (with errata) on HRD restrictions.

    if (previousflighttype == "ZC" or previousflighttype == "SC") and flighttype == "VD":
      assert A._hrd
      mininitialhfp = A.speed() // 3
    elif previousflighttype == "LVL" and (_isclimbingflight(flighttype) or _isdivingflight(flighttype)):
      mininitialhfp = 1
    elif (_isclimbingflight(previousflighttype) and _isdivingflight(flighttype)) or (_isdivingflight(previousflighttype) and _isclimbingflight(flighttype)):
      if apcapabilities.hasproperty(A, "HPR"):
        mininitialhfp = A.speed() // 3
      else:
        mininitialhfp = A.speed() // 2
    else:
      mininitialhfp = 0

    maxfp = int(A._maxfp)

    minhfp = 0
    maxhfp = maxfp
    minvfp = 0
    maxvfp = maxfp
    minunloadedhfp = 0
    maxunloadedhfp = 0

    # The comments below about "see the blue sheet" refer to the VFP
    # requirements for SD, SC, and ZC, which do not appear in the rules
    # but which do appear on the blue "Flight Rules Summary" sheet.
    # Actually, there is no requirement for SCs even here, but we assume
    # that at least one VFP must be used in this case too.

    if flighttype == "LVL":

      # See rule 5.3.
      maxvfp = 0
    
    elif flighttype == "ZC":

      # See blue sheet.
      minvfp = 1      

      # See rules 8.1.1.
      minhfp = rounddown(onethirdfromtable(maxfp))

    elif flighttype == "SC":

      # See blue sheet.
      minvfp = 1
      
      # See rule 8.1.2.
      if A.speed() < apcapabilities.minspeed(A) + 1.0:
        raise RuntimeError("insufficient speed for SC.")
      climbcapability = apcapabilities.climbcapability(A)
      if A.speed() < apcapabilities.climbspeed(A):
        climbcapability /= 2
      if climbcapability < 1:
        maxvfp = 1
      else:
        maxvfp = rounddown(twothirdsfromtable(maxfp))

    elif flighttype == "VC" or flighttype == "VD":

      # See blue sheet.
      minvfp = 1
      
      # See rules 8.1.3 and 8.2.3.
      if previousflighttype != flighttype:
        minhfp = rounddown(onethirdfromtable(maxfp))
        maxhfp = minhfp
      else:
        maxhfp = rounddown(onethirdfromtable(maxfp))

    elif flighttype == "SD":

      # See blue sheet.
      minvfp = 1
      
      # See rules 8.2.1 and 8.2.3.
      if previousflighttype == "VD":
        minvfp = rounddown(maxfp / 2)
      minhfp = rounddown(onethirdfromtable(maxfp))    

    elif flighttype == "UD":

      if apvariants.withvariant("use version 2.4 rules"):

        # See rules 8.2.2.
        maxvfp = 0
        minunloadedhfp = 1
        maxunloadedhfp = maxfp
          
      else:

        # See rules 8.2.2 and 8.2.3.
        maxvfp = 0
        maxunloadedhfp = maxfp
        if previousflighttype == "VD":
          minunloadedhfp = rounddown(maxfp / 2)
        else:
          minunloadedhfp = 1

    minhfp = max(minhfp, mininitialhfp)

    if maxvfp == 0:

      A._logevent("all FPs must be HFPs.")

    else:

      if mininitialhfp == 1:
        A._logevent("the first FP must be an HFP.")
      elif mininitialhfp > 1:
        A._logevent("the first %d FPs must be HFPs." % mininitialhfp)
      
      if minhfp == maxhfp:
        A._logevent(plural(minhfp,
          "exactly 1 FP must be an HFP.",
          "exactly %d FPs must be HFPs." % minhfp
        ))
      elif minhfp > 0 and maxhfp < maxfp:
        A._logevent("between %d and %d FP must be HFPs." % (minhfp, maxhfp))
      elif minhfp > 0:
        A._logevent(plural(minhfp,
          "at least 1 FP must be an HFP.",
          "at least %d FPs must be HFPs." % minhfp
        ))
      else:
        A._logevent(plural(maxhfp,
          "at most 1 FP may be an HFP.",
          "at most %d FPs may be HFPs." % maxhfp
        ))

      if minvfp == maxvfp:
        A._logevent(plural(minvfp,
          "exactly 1 FP must be a VFP.",
          "exactly %d FPs must be VFPs." % minvfp
        ))
      elif minvfp > 0 and maxvfp < maxfp:
        A._logevent("between %d and %d FP must be VFPs." % (minvfp, maxvfp))
      elif minvfp > 0:
        A._logevent(plural(minvfp,
          "at least 1 FP must be a VFP.",
          "at least %d FPs must be VFPs." % minvfp
        ))
      else:
        A._logevent(plural(maxvfp,
          "at most 1 FP may be a VFP.",
          "at most %d FPs may be VFPs." % maxvfp
        ))

    if minhfp > maxhfp:
      raise RuntimeError("flight type not permitted by HFP requirements.")
    if minvfp > maxvfp:
      raise RuntimeError("flight type not permitted by VFP requirements.")
  
    if minunloadedhfp > 0:
      A._logevent(plural(minunloadedhfp,
        "at least 1 FP must be an unloaded HFP.",
        "at least %d FPs must be unloaded HFPs." % minunloadedhfp
      ))

    A._mininitialhfp  = mininitialhfp
    A._minhfp         = minhfp
    A._maxhfp         = maxhfp
    A._minvfp         = minvfp
    A._maxvfp         = maxvfp
    A._minunloadedhfp = minunloadedhfp
    A._maxunloadedhfp = maxunloadedhfp      

  ########################################

  def handlecarriedturn():

    """
    Handle any carried turn.
    """

    if _isturn(A._maneuvertype):

      # See rule 7.7.

      # Issue: The consequences of carried turn violating the turn
      # requirements of ZC, SC, and VC flight are not clear, but for the
      # moment we assume they result in a maneuvering departure.

      turnrequirement = apturnrate.turnrequirement(A.altitudeband(), A.speed(), A._maneuvertype)
      if not A._maneuvertype in A._allowedturnrates or turnrequirement == None:
        A._logevent("carried turn rate is tighter than the maximum allowed turn rate.")
        raise RuntimeError("aircraft has entered departed flight while maneuvering.")

      # See rule 7.1.

      previousmaneuverrequiredfp    = A._maneuverrequiredfp
      previous_maneuverfacingchange = A._maneuverfacingchange

      A._maneuversupersonic   = A.speed() >= apspeed.m1speed(A.altitudeband())
      turnrequirement = apturnrate.turnrequirement(A.altitudeband(), A.speed(), A._maneuvertype)
      if turnrequirement >= 60:
        A._maneuverrequiredfp   = 1
        A._maneuverfacingchange = turnrequirement
      else:
        A._maneuverrequiredfp   = turnrequirement
        A._maneuverfacingchange = 30

      if A._maneuverrequiredfp != previousmaneuverrequiredfp or A._maneuverfacingchange != previous_maneuverfacingchange:
        if A._maneuverfacingchange > 30:
          A._logevent("turn requirement changed to %d in 1 FP." % A._maneuverfacingchange)
        else:
          A._logevent("turn requirement changed to %s." % plural(A._maneuverrequiredfp, "1 FP", "%d FPs" % A._maneuverrequiredfp))

      A._maxturnrate       = A._maneuvertype
      A._turningsupersonic = A._maneuversupersonic

    else:

      A._maxturnrate       = None
      A._turningsupersonic = False

  ########################################

  def determineeffectiveclimbcapability():

    if _isclimbingflight(flighttype):

      A._effectiveclimbcapability = apcapabilities.climbcapability(A)

      # See rule 4.3 and 8.1.2.
      if flighttype == "SC" and A.speed() < apcapabilities.climbspeed(A):
        A._logevent("climb capability reduced in SC below climb speed.")
        A._effectiveclimbcapability *= 0.5

      # See the Aircraft Damage Effects Table in the charts.
      if A.damageatleast("H"):
        A._logevent("climb capability reduced by damage.")
        A._effectiveclimbcapability *= 0.5

      # See rule 6.6 and rule 8.1.4.
      if A.speed() >= apspeed.m1speed(A.altitudeband()):
        A._logevent("climb capability reduced at supersonic speed.")
        A._effectiveclimbcapability *= 2/3
    
      A._logevent("effective climb capability is %.2f." % A._effectiveclimbcapability)

    else:

      A._effectiveclimbcapability = None

  ########################################

  flighttype         = A._flighttype
  previousflighttype = A._previousflighttype  
  
  # The number of FPs, HFPs, and VFPs used and the number of FPs lost to
  # speedbrakes. They are used to ensure that the right mix of HFPs and
  # VFPs are used and to determine when the turn ends.

  A._fp         = 0
  A._hfp        = 0
  A._vfp        = 0
  A._spbrfp     = 0

  # The number of unloaded HFPs and the indices of the first and last
  # unloaded HFPs in an UD. They are then used to ensure that the
  # unloaded HFPs are continuous.

  A._unloadedhfp     = 0
  A._firstunloadedfp = None
  A._lastunloadedfp  = None

  # Whether the aircraft has used a superclimb (C3).
  A._usedsuperclimb = False

  # The aircraft being tracked and the number of FPs expended
  # while tracking.

  A._tracking   = None
  A._trackingfp = 0

  # This keeps track of the number of turns, rolls, and vertical rolls.

  A._turnmaneuvers = 0
  A._rollmaneuvers = 0
  A._verticalrolls = 0

  # The number of slides performed and the FP of the last last performed.

  A._slides = 0
  A._slidefp = 0

  # The string that we create to describe the actions.

  A._actions = ""

  reportapcarry()
  reportaltitudecarry()
  determineallowedturnrates()
  handlecarriedturn()
  checkcloseformationlimits()
  determinemaxfp()
  determinefprequirements()
  determineeffectiveclimbcapability()
    
  A._logpositionandmaneuver("start")

  continueflight(A, actions, note=note)

################################################################################

def endflight(A):

  ########################################

  def reportfp():
    A._logevent("used %s and %s." % (
      plural(A._hfp, "1 HFP", "%d HFPs" % A._hfp),
      plural(A._vfp, "1 VFP", "%d VFPs" % A._vfp)
    ))    
    if A._spbrfp > 0:
      A._logevent("lost %.1f FPs to speedbrakes." % A._spbrfp)
    A._logevent("will carry %.1f FPs." % A._fpcarry)

  ########################################

  def checkfp():

    if A._hfp < A._minhfp:
      raise RuntimeError("too few HFPs.")

    if A._hfp > A._maxhfp:
      raise RuntimeError("too many HFPs.")  
      
    if A._vfp < A._minvfp:
      raise RuntimeError("too few VFPs.")

    if A._vfp > A._maxvfp:
      raise RuntimeError("too many VFPs.")

    if A._flighttype == "UD":
      # See rule 8.2.2.
      if A._firstunloadedfp == None:
        n = 0
      else:
        n = A._lastunloadedfp - A._firstunloadedfp + 1
      if A._unloadedhfp != n:
        raise RuntimeError("unloaded HFPs must be continuous.")
      if A._unloadedhfp < A._minunloadedhfp:
        raise RuntimeError("too few unloaded HFPs.")
      if A._unloadedhfp > A._maxunloadedhfp:
        raise RuntimeError("too many unloaded HFPs.")

  ########################################

  def checkfreedescent():

    # See rule 8.2.4.
    
    if A._flighttype == "LVL":
      altitudechange = A.altitude() - A._previousaltitude
      if altitudechange < -1:
        raise RuntimeError("free descent cannot only be taken once per move.")      

  ########################################

  def reportgloccycle():

    # See rule 7.6.
    if A._gloccheck > 0 and A._maxturnrate != "ET" and A._maxturnrate != "BT":
      A._logevent("GLOC cycle ended.")
      A._gloccheck = 0 

  ########################################

  def reportcarry():

    if A._altitudecarry != 0:
      A._logevent("is carrying %.2f altitude levels." % A._altitudecarry)
          
  ########################################

  def determinemaxturnrateap():

    """
    Determine the APs from the maximum turn rate used.
    """

    if A._maxturnrate != None:
      A._turnrateap = -apcapabilities.turndrag(A, A._maxturnrate)
    else:
      A._turnrateap = 0

    if A._turningsupersonic:
      if apcapabilities.hasproperty(A, "PSSM"):
        A._turnrateap -= 2.0
      elif not apcapabilities.hasproperty(A, "GSSM"):
        A._turnrateap -= 1.0

  ########################################

  def determinealtitudeap():

    altitudechange = A.altitude() - A._previousaltitude

    if flighttype == "ZC":

      # See rule 8.1.1.
      if apvariants.withvariant("use version 2.4 rules"):
        altitudeap = -1.0 * altitudechange
      else:
        if _isclimbingflight(previousflighttype):
          altitudeap = -1.5 * altitudechange
        else:
          altitudeap = -1.0 * altitudechange

    elif flighttype == "SC":

      if altitudechange == 0:

        altitudeap = 0.0
        A._scwithzccomponent = False

      else:

        # See rule 8.1.2 and 8.1.4.

        climbcapability = A._effectiveclimbcapability

        # We need to figure out how much was climbed at the SC rate and
        # how much was climbed at the ZC rate. This is complicated since
        # altitudechange can be more than the climbcapability because of
        # altitudecarry. Therefore, we calculate how much was at the ZC
        # rate from the true altitude change, including carry, and then
        # assume that any difference was at the SC rate.
        # 
        # We also use that the altitude change at the ZC rate must be an
        # integral number of levels.

        truealtitude     = A.altitude()         + A._altitudecarry
        lasttruealtitude = A._previousaltitude + A._previousaltitudecarry

        truealtitudechange = truealtitude - lasttruealtitude

        scaltitudechange = min(truealtitudechange, climbcapability)
        zcaltitudechange = int(truealtitudechange - scaltitudechange + 0.5)
        scaltitudechange = altitudechange - zcaltitudechange

        if apvariants.withvariant("use version 2.4 rules"):
          altitudeap = -0.5 * scaltitudechange + -1.0 * zcaltitudechange
        else:
          if _isclimbingflight(previousflighttype):
            altitudeap = -0.5 * scaltitudechange + -1.5 * zcaltitudechange
          else:
            altitudeap = -0.5 * scaltitudechange + -1.0 * zcaltitudechange
        A._scwithzccomponent = (zcaltitudechange != 0)

    elif flighttype == "VC":

      # See rule 8.1.3.
      if apvariants.withvariant("use version 2.4 rules"):
        altitudeap = -1.5 * altitudechange
      else:
        altitudeap = -2.0 * altitudechange

    elif flighttype == "SD":

      # See rule 8.2.1.
      if apvariants.withvariant("use version 2.4 rules"):
        altitudeap = -1.0 * altitudechange
      else:
        if _isdivingflight(previousflighttype):
          altitudeap = -1.0 * altitudechange
        else:
          altitudeap = -0.5 * altitudechange

    elif flighttype == "UD":

      # See rule 8.2.2.
      if apvariants.withvariant("use version 2.4 rules"):
        altitudeap = -1.0 * altitudechange
      else:
        if _isdivingflight(previousflighttype):
          altitudeap = -1.0 * altitudechange
        else:
          altitudeap = -0.5 * altitudechange

    elif flighttype == "VD":

      # See rule 8.2.3
      altitudeap = -1.0 * altitudechange

    elif flighttype == "LVL":

      # See rule 8.2.4.
      altitudeap = 0

    # Round to nearest quarter. See rule 6.2.
    altitudeap = roundtoquarter(altitudeap)

    A._altitudeap = altitudeap

  ########################################

  def checkcloseformationlimits():

    if A.closeformationsize() == 0:
      return

    # See rule 8.6. The other climbing and diving cases are handled at
    # the start of the move.

    altitudeloss = A._previousaltitude - A.altitude()
    if flighttype == "SD" and altitudeloss > 2:
      A._logevent("close formation breaks down as the aircraft lost %d levels in an SD." % altitudeloss)
      apcloseformation.breakdown(A)
    elif flighttype == "SC" and A._scwithzccomponent:
      A._logevent("close formation breaks down as the aircraft climbed faster than the sustained climb rate.")
      apcloseformation.breakdown(A)
      
  ########################################

  def handleunloadeddiveflighttype():

    if flighttype == "UD" and apvariants.withvariant("use version 2.4 rules"):
      # See rule 8.2.2.
      altitudechange = A.altitude() - A._previousaltitude
      if altitudechange == -2:
        A._logevent("UD ends as flight type SD.")
        A._flighttype = "SD"
      else:
        A._logevent("UD ends as flight type LVL.")
        A._flighttype = "LVL"
        
  ########################################

  flighttype         = A._flighttype
  previousflighttype = A._previousflighttype  
  
  if not A._maneuveringdeparture:
    reportfp()
    checkfp()
    checkfreedescent()
    reportcarry()
    reportgloccycle()
    determinemaxturnrateap()
    determinealtitudeap()
    checkcloseformationlimits()
    handleunloadeddiveflighttype()

  apflight.endmove(A)

################################################################################

def _isturn(maneuvertype):

  """
  Return True if the maneuver type is a turn. Otherwise False.
  """

  return maneuvertype in ["EZ", "TT", "HT", "BT", "ET"]

################################################################################

def _isroll(maneuvertype):

  """
  Return True if the maneuver type is a roll. Otherwise False.
  """

  return maneuvertype in ["VR", "DR", "LR", "BR"]

################################################################################

def _isslide(maneuvertype):

  """
  Return True if the maneuver type is a slide. Otherwise False.
  """

  return maneuvertype == "SL"
  
################################################################################

def _isdivingflight(flighttype, vertical=False):

  """
  Return True if the flight type is SD, UD, or VD. Otherwise return False.
  """

  if vertical:
    return flighttype == "VD"
  else:
    return flighttype == "SD" or flighttype == "UD" or flighttype == "VD"

################################################################################

def _isclimbingflight(flighttype, vertical=False):

  """
  Return True if the flight type is ZC, SC, or VC. Otherwise return False.
  """
  
  if vertical:
    return flighttype == "VC"
  else:
    return flighttype == "ZC" or flighttype == "SC" or flighttype == "VC"

################################################################################

def _islevelflight(flighttype):

  """
  Return True if the flight type is LVL. Otherwise return False.
  """
  
  return flighttype == "LVL"
  
################################################################################
