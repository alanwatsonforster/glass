"""
Normal flight for the aircraft class.
"""

import math
import re
from apxo.math import onethird, twothirds, roundtoquarter

import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.aircraft as apaircraft
import apxo.hex      as aphex
import apxo.speed    as apspeed
import apxo.stores   as apstores
import apxo.turnrate as apturnrate
import apxo.variants as apvariants

from apxo.log import plural

def _checknormalflight(self):

  if self.hasproperty("SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform normal flight.")

  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype

  # See rule 13.3.5. A HRD is signalled by appending "/HRD" to the flight type.
  if flighttype[-4:] == "/HRD":

    if self.hasproperty("NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")

    hrd = True
    flighttype = flighttype[:-4]
    self._flighttype = flighttype

    # See rule 7.7.
    if self._altitude > self.ceiling():
      self._logevent("check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
    elif self._altitudeband == "EH" or self._altitudeband == "UH":
      self._logevent("check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % self._altitudeband)  
      
  else:

    hrd = False

  self._hrd = hrd

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
    elif flighttype == "LVL" and not self.hasproperty("HPR"):
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
      if not self.hasproperty("HPR"):
        raise RuntimeError("flight type immediately after %s cannot be %s." % (
          previousflighttype, flighttype
        ))
      elif self._speed >= 3.5:
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

    if self._speed < self.minspeed() + 1:
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
      if not self.hasproperty("HPR"):
        raise RuntimeError("flight type immediately after %s cannot be %s." % (
          previousflighttype, flighttype
        ))
      elif self._speed >= 4.0:
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

    if previousflighttype == "VC" and not (self.hasproperty("HPR") or hrd):
      raise RuntimeError("flight type immediately after %s cannot be %s (without a HRD)." % (
        previousflighttype, flighttype
      ))

  elif flighttype == "UD":

    # See rule 8.1.3 on VC restrictions.

    if previousflighttype == "VC" and not self.hasproperty("HPR"):
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
      if hrd and self._speed > 4.0:
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

def _continuenormalflight(self, actions, note=False):

  """
  Continue to carry out out normal flight.
  """

  ########################################

  def dohorizontal():

    """
    Move horizontally.
    """

    self._x, self._y = aphex.forward(self._x, self._y, self._facing)

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    def determinealtitudechange(altitudechange):

      assert altitudechange == 1 or altitudechange == 2
    
      climbcapability = self._effectiveclimbcapability

      if flighttype == "ZC":

        # See rule 8.1.1.
        if climbcapability <= 2 and altitudechange != 1:
          raise RuntimeError("invalid altitude change in climb.")
        elif altitudechange != 1 and altitudechange != 2:
          raise RuntimeError("invalid altitude change in climb.")

      elif flighttype == "SC":

        # See rule 8.1.2.
        if self._speed < self.climbspeed():
          climbcapability /= 2
        if climbcapability < 2.0 and altitudechange == 2:
          raise RuntimeError("invalid altitude change in climb.")
        if self._vfp == 0 and climbcapability % 1 != 0:
          # First VFP with fractional climb capability.
          altitudechange = climbcapability % 1

      elif flighttype == "VC":

        # See rule 8.1.3.
        if altitudechange != 1 and altitudechange != 2:
          raise RuntimeError("invalid altitude change in climb.")

      else:

        # See rule 8.0.
        raise RuntimeError("attempt to climb while flight type is %s." % self._flighttype)

      return altitudechange

    # See rule 4.3 and 8.1.2.
    if self._effectiveclimbcapability == None:
      self._effectiveclimbcapability = self.climbcapability()
      if flighttype == "SC" and self._speed < self.climbspeed():
        self._effectiveclimbcapability /= 2

    altitudechange = determinealtitudechange(altitudechange)
    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)
    self._altitudeband = apaltitude.altitudeband(self._altitude)

    # See rule 8.5.
    if flighttype == "SC" and self._altitude > self.ceiling():
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
        raise RuntimeError("attempt to dive while flight type is %s." % self._flighttype)
    
    checkaltitudechange()

    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  ########################################

  def dobank(sense):

    # See rule 7.4.
    if self.hasproperty("LRR"):
      if (self._bank == "L" and sense == "R") or (self._bank == "R" and sense == "L"):
        raise RuntimeError("attempt to bank to %s while banked to %s in a LRR aircraft." % (sense, self._bank))

    self._bank = sense
    if _isturn(self._maneuvertype):
      self._maneuvertype         = None
      self._maneuversense        = None
      self._maneuverfacingchange = None
      self._maneuverfp           = 0

  ########################################

  def dodeclareturn(sense, turnrate):

    """
    Declare the start of turn in the specified direction and rate.
    """

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare turn while flight type is %s." % flighttype)
      
    # See rule 7.1.

    # Check the bank. See rule 7.4.
    if self.hasproperty("LRR"):
      if self._bank != sense:
        raise RuntimeError("attempt to declare a turn to %s while not banked to %s in a LRR aircraft." % (sense, sense))
    elif not self.hasproperty("HRR"):
      if (self._bank == "L" and sense == "R") or (self._bank == "R" and sense == "L"):
        raise RuntimeError("attempt to declare a turn to %s while banked to %s." % (sense, self._bank))

    if self._allowedturnrates == []:
      raise RuntimeError("turns are forbidded.")

    if turnrate not in self._allowedturnrates:
      raise RuntimeError("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")

    turnrateap = self.turndrag(turnrate)
    if turnrateap == None:
      raise RuntimeError("attempt to declare a turn rate tighter than allowed by the aircraft.")

    # Determine the maximum turn rate.
    if self._maxturnrate == None:
      self._maxturnrate = turnrate
    else:
      turnrates = ["EZ", "TT", "HT", "BT", "ET"]
      self._maxturnrate = turnrates[max(turnrates.index(turnrate), turnrates.index(self._maxturnrate))]

    self._bank                 = sense
    self._maneuvertype         = turnrate
    self._maneuversense        = sense
    self._maneuverfp           = 0
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))
    turnrequirement = apturnrate.turnrequirement(self._altitudeband, self._speed, self._maneuvertype)
    if turnrequirement == None:
      raise RuntimeError("attempt to declare a turn rate tigher than allowed by the speed and altitude.")
    if turnrequirement >= 60:
      self._maneuverrequiredfp   = 1
      self._maneuverfacingchange = turnrequirement
    else:
      self._maneuverrequiredfp   = turnrequirement
      self._maneuverfacingchange = 30

  ########################################

  def doturn(sense, facingchange, continuous):

    """
    Turn in the specified sense and amount.
    """

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to turn while flight type is %s." % flighttype)
      
    # See rule 7.1.
    if self._maneuverfp < self._maneuverrequiredfp or facingchange > self._maneuverfacingchange:
      raise RuntimeError("attempt to turn faster than the declared turn rate.")

    # See Hack's article in APJ 36
    if self._turnmaneuvers == 0:
      sustainedfacingchanges = facingchange // 30 - 1
    else:
      sustainedfacingchanges = facingchange // 30

    if apvariants.withvariant("use version 2.4 rules"):
      if self.hasproperty("LBR"):
        self._sustainedturnap -= sustainedfacingchanges * 0.5
      elif self.hasproperty("HBR"):
        self._sustainedturnap -= sustainedfacingchanges * 1.5
      else:
        self._sustainedturnap -= sustainedfacingchanges * 1.0
    else:
      if self.hasproperty("HBR"):
        self._sustainedturnap -= sustainedfacingchanges * 2.0
      else:
        self._sustainedturnap -= sustainedfacingchanges * 1.0

    self._turnmaneuvers += 1

    # Change facing.
    if aphex.isside(self._x, self._y):
      self._x, self._y = aphex.sidetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

  ########################################

  def dodeclareslide(sense):

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare slide while flight type is %s." % flighttype)

    # See rules 13.1 and 13.2.

    if self._slides == 1 and self._speed <= 9.0:
      raise RuntimeError("only one slide allowed per turn at low speed.")
    if self._slides == 1 and self._fp - self._slidefp - 1 <  4:
      raise RuntimeError("attempt to start a second slide without sufficient intermediate FPs.")
    elif self._slides == 2:
      raise RuntimeError("at most two slides allowed per turn.")

    self._bank                 = None
    self._maneuvertype         = "SL"
    self._maneuversense        = sense
    self._maneuverfacingchange = None
    self._maneuverfp           = 0
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))
    # The requirement has +1 FP to account for the final H.
    self._maneuverrequiredfp   = 2 + extrapreparatoryhfp() + 1
    
  ########################################

  def extrapreparatoryhfp():

    # See rule 13.1.

    extrapreparatoryfp = { "LO": 0, "ML": 0, "MH": 0, "HI": 1, "VH": 2, "EH": 3, "UH": 4 }[self._altitudeband]

    if self._speed >= apspeed.m1speed(self._altitudeband):
      extrapreparatoryfp += 1.0

    # See "Aircraft Damage Effects" in the Play Aids.

    if self.damageatleast("2L"):
      extrapreparatoryfp += 1.0

    return extrapreparatoryfp

  ########################################

  def doslide(sense):

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to slide while flight type is %s." % flighttype)

    # See rules 13.1 and 13.2.

    if self._maneuverfp < self._maneuverrequiredfp:
      raise RuntimeError("attempt to slide without sufficient preparatory HFPs.")

    # Slide. Remember that we have already moved forward one hex for the final H element.
    self._x, self._y = aphex.slide(self._x, self._y, self._facing, sense)

    # See rule 13.2.
    if self._slides >= 1:
      self._othermaneuversap -= 1.0

    # Keep track of the number of slides and the FP of the last slide.
    self._slides += 1
    self._slidefp = self._fp

    # Implicitly finish with wings level.
    self._bank = None

  ########################################

  def dodeclaredisplacementroll(sense):

    # See rules 13.1 and 13.3.1.

    if self.hasproperty("NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if self.rolldrag("DR") == None:
      raise RuntimeError("aircraft cannot perform displacement rolls.")
      
    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if flighttype == "SC" or flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare a displacement roll while flight type is %s." % flighttype)

    self._bank                 = None
    self._maneuvertype         = "DR"
    self._maneuversense        = sense
    self._maneuverfacingchange = None
    self._maneuverfp           = 0
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))
    # The requirement includes the FPs used to execute the roll.
    if apvariants.withvariant("use version 2.4 rules"):
      self._maneuverrequiredfp   = self.rollhfp() + extrapreparatoryhfp() + onethird(self._speed)
    else:
      self._maneuverrequiredfp   = self.rollhfp() + extrapreparatoryhfp() + 1

  ########################################

  def dodisplacementroll(sense):

    # See rules 13.1 and 13.3.1.

    if self._maneuverfp < self._maneuverrequiredfp:
      raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")

    if not self._horizontal:
      raise RuntimeError("attempt to roll on a VFP.")
      
    # Move.
    self._x, self._y = aphex.displacementroll(self._x, self._y, self._facing, sense)

    # See rule 13.3.1.
    self._othermaneuversap -= self.rolldrag("DR")

    # See rule 6.6.
    if self._maneuversupersonic:
      if self.hasproperty("PSSM"):
        self._othermaneuversap -= 2.0
      elif not self.hasproperty("GSSM"):
        self._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if self._rollmaneuvers > 0:
      self._othermaneuversap -= 1.0
    self._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    self._bank = None

  ########################################

  def dodeclarelagroll(sense):

    # See rule 13.3.2.

    if self.hasproperty("NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if self.rolldrag("LR") == None:
      raise RuntimeError("aircraft cannot perform lag rolls.")
      
    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if flighttype == "SC" or flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare a lag roll while flight type is %s." % flighttype)

    self._bank                 = None
    self._maneuvertype         = "LR"
    self._maneuversense        = sense
    self._maneuverfacingchange = None
    self._maneuverfp           = 0
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))
    # The requirement includes the FPs used to execute the roll.
    if apvariants.withvariant("use version 2.4 rules"):
      self._maneuverrequiredfp   = self.rollhfp() + extrapreparatoryhfp() + onethird(self._speed)
    else:
      self._maneuverrequiredfp   = self.rollhfp() + extrapreparatoryhfp() + 1

  ########################################

  def dolagroll(sense):

    # See rules 13.1 and 13.3.2.

    if self._maneuverfp < self._maneuverrequiredfp:
      raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")

    if not self._horizontal:
      raise RuntimeError("attempt to roll on a VFP.")

    # Move.
    self._x, self._y = aphex.lagroll(self._x, self._y, self._facing, sense)
    if sense == "R":
      self._facing += 30
    else:
      self._facing -= 30
    self._facing %= 360

    # See rule 13.3.1.
    self._othermaneuversap -= self.rolldrag("LR")

    # See rule 6.6.
    if self._maneuversupersonic:
      if self.hasproperty("PSSM"):
        self._othermaneuversap -= 2.0
      elif not self.hasproperty("GSSM"):
        self._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if self._rollmaneuvers > 0:
      self._othermaneuversap -= 1.0
    self._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    self._bank = None

  ########################################  

  def dodeclareverticalroll(sense):

    if self.hasproperty("NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if self._verticalrolls == 1 and self.hasproperty("OVR"):
      raise RuntimeError("aircraft can only perform one vertical roll per turn.")
      
    # See rule 13.3.4.  
    if self._flighttype != "VC" and self._flighttype != "VD":
      raise RuntimeError("attempt to declare a vertical roll while flight type is %s." % self._flighttype)
    if not self._vertical:
      raise RuntimeError("attempt to declare a vertical roll during an HFP.")
    if previousflighttype == "LVL" and flighttype == "VC" and not self._lastfp:
      raise RuntimeError("attempt to declare a vertical roll in VC following LVL flight other than on the last FP.")

    # See rule 13.3.5.
    if self._hrd and not self._lastfp:
      raise RuntimeError("attempt to declare a vertical roll after HRD other than on the last FP.")
      
    self._bank                 = None
    self._maneuvertype         = "VR"
    self._maneuversense        = sense
    self._maneuverfacingchange = None
    self._maneuverfp           = 0
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))
    self._maneuverrequiredfp   = 1

  ########################################

  def doverticalroll(sense, facingchange, shift):

    if self._maneuverfp < self._maneuverrequiredfp:
      raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")
  
    # See rule 13.3.4.
    if self.hasproperty("LRR") and facingchange > 90:
      raise RuntimeError("attempt to roll vertically by more than 90 degrees in LRR aircraft.")

    self._othermaneuversap -= self.rolldrag("VR")

    # See rule 13.3.6
    if self._rollmaneuvers > 0:
      self._othermaneuversap -= 1
    self._rollmaneuvers += 1
    self._verticalrolls += 1

    # See rule 6.6.
    if self._maneuversupersonic:
      if self.hasproperty("PSSM"):
        self._othermaneuversap -= 2.0
      elif not self.hasproperty("GSSM"):
        self._othermaneuversap -= 1.0

    # Change facing.
    if aphex.isside(self._x, self._y) and shift:
      self._x, self._y = aphex.sidetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360
    
  ########################################

  def domaneuver(sense, facingchange, shift, continuous):

    if self._maneuvertype == None:
      raise RuntimeError("attempt to maneuver without a declaration.")
      
    if self._maneuversense != sense:
      raise RuntimeError("attempt to maneuver against the sense of the declaration.")

    if self._maneuvertype == "SL":
      if facingchange != None:
        raise RuntimeError("invalid element for a slide.")
      doslide(sense)
    elif self._maneuvertype == "DR":
      if facingchange != None:
        raise RuntimeError("invalid element for a displacement roll.")
      dodisplacementroll(sense)
    elif self._maneuvertype == "LR":
      if facingchange != None:
        raise RuntimeError("invalid element for a lag roll.")
      dolagroll(sense)
    elif self._maneuvertype == "VR":
      if facingchange == None:
        facingchange = 30
      doverticalroll(sense, facingchange, shift)
    else:
      if facingchange == None:
        facingchange = 30
      doturn(sense, facingchange, continuous)

    self._maneuverfp = 0

    if not continuous:
      self._maneuvertype         = None
      self._maneuversense        = None
      self._maneuverfacingchange = None
      self._maneuverrequiredfp   = 0
      self._maneuversupersonic   = False
    elif self._maneuvertype == "SL":
      dodeclareslide(self._maneuversense)
    elif self._maneuvertype == "DR":
      dodeclaredisplacementroll(self._maneuversense)
    elif self._maneuvertype == "LR":
      dodeclarelagroll(self._maneuversense)
    elif self._maneuvertype == "VR":
      dodeclareverticalroll(self._maneuversense)
    else:
      dodeclareturn(self._maneuversense, self._maneuvertype)

  ########################################

  def dospeedbrakes(spbr):

    """
    Use the speedbrakes.
    """

    # See rules 6.5 and 6.6.

    if self._spbrap != 0:
      raise RuntimeError("speedbrakes can only be used once per turn.")
        
    maxspbr = self.spbr()
    if maxspbr == None:
      raise RuntimeError("aircraft does not have speedbrakes.")
        
    if apvariants.withvariant("use version 2.4 rules"):

      maxspbr = self.spbr()

      if self._speed >= apspeed.m1speed(self._altitudeband):
        maxspbr += 2.0      

      if spbr > maxspbr:
        raise RuntimeError(plural(maxspbr,
          "speedbrake capability is only 1 DP.",
          "speedbrake capability is only %.1f DPs." % maxspbr))
          
      self._spbrap = -spbr
          
    else:

      if self._speed > apspeed.m1speed(self._altitudeband):
        maxspbr += 0.5
        
      if spbr > maxspbr:
        raise RuntimeError(plural(maxspbr,
          "speedbrake capability is only 1 FP.",
          "speedbrake capability is only %.1f FPs." % maxspbr))
          
      maxspbr = self._maxfp - self._hfp - self._vfp
      if spbr >= maxspbr:
        raise RuntimeError(plural(maxspbr,
          "invalid use of speedbrakes when only 1 FP remains.",
          "invalid use of speedbrakes when only %s FPs remain." % maxspbr))

      self._spbrfp = spbr
      self._maxfp -= spbr

      self._spbrap = -spbr / 0.5
  
  ########################################

  def dojettison(m):

    # See rule 4.4.   
    # We implement the delay of 1 FP by making this an other element.
    
    previousconfiguration = self._configuration

    for released in m[1].split("+"):
      self._stores = apstores._release(self._stores, released,
        printer=lambda s: self._logevent(s)
      )

    self._updateconfiguration()

    if self._configuration != previousconfiguration:
      self._logevent("configuration changed from %s to %s." % (
        previousconfiguration, self._configuration
      ))

  ########################################

  def doataattack(m):

    """
    Declare an air-to-air attack.
    """

    # See rule 8.2.2.
    if self._unloaded:
      raise RuntimeError("attempt to use weapons while unloaded.")

    # See rule 13.3.5.
    if self._hrd:
      raise RuntimeError("attempt to use weapons during the turn after an HRD.")

    # See rule 13.3.6.
    if self._wasrollingonlastfp:
      raise RuntimeError("attempt to use weapons on the FP immediately after rolling.")

    # See rule 10.1.
    if self._ETrecoveryfp > 0:
      raise RuntimeError("attempt to use weapons in or while recovering from an ET.")

    weapon     = m[1]
    targetname = m[2]
    result     = m[3]

    if targetname == "":
      target = None
    else:
      target = apaircraft.fromname(targetname)
      if target is None:
        raise RuntimeError("unknown target aircraft %s." % targetname)
      
    apairtoair.attack(self, weapon, target, result)

  ########################################

  def domaneuveringdeparture(sense, facingchange):

    # Do the first facing change.

    if aphex.isside(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing, sense)
    if action[0] == "L":
      self._facing = (self._facing + 30) % 360
    else:
      self._facing = (self._facing - 30) % 360
    self._continueflightpath()
    facingchange -= 30

    # Shift.

    shift = int((self._maxfp - self._fp) / 2)
    for i in range(0, shift):
      self._x, self._y = aphex.forward(self._x, self._y, self._facing)
      self.checkforterraincollision()
      self.checkforleavingmap()
      if self._destroyed or self._leftmap:
        return

    # Do any remaining facing changes.
    if aphex.isside(self._x, self._y):
      self._x, self._y = aphex.sidetocenter(self._x, self._y, self._facing, sense)
    if action[0] == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

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
  
    ["SLL"  , "maneuver declaration", None, lambda: dodeclareslide("L") ],
    ["SLR"  , "maneuver declaration", None, lambda: dodeclareslide("R") ],

    ["DRL"  , "maneuver declaration", None, lambda: dodeclaredisplacementroll("L") ],
    ["DRR"  , "maneuver declaration", None, lambda: dodeclaredisplacementroll("R") ],

    ["LRL"  , "maneuver declaration", None, lambda: dodeclarelagroll("L") ],
    ["LRR"  , "maneuver declaration", None, lambda: dodeclarelagroll("R") ],
        
    ["VRL"  , "maneuver declaration", None, lambda: dodeclareverticalroll("L") ],
    ["VRR"  , "maneuver declaration", None, lambda: dodeclareverticalroll("R") ],
    
    ["EZL"  , "maneuver declaration", None, lambda: dodeclareturn("L", "EZ") ],
    ["TTL"  , "maneuver declaration", None, lambda: dodeclareturn("L", "TT") ],
    ["HTL"  , "maneuver declaration", None, lambda: dodeclareturn("L", "HT") ],
    ["BTL"  , "maneuver declaration", None, lambda: dodeclareturn("L", "BT") ],
    ["ETL"  , "maneuver declaration", None, lambda: dodeclareturn("L", "ET") ],
    
    ["EZR"  , "maneuver declaration", None, lambda: dodeclareturn("R", "EZ") ],
    ["TTR"  , "maneuver declaration", None, lambda: dodeclareturn("R", "TT") ],
    ["HTR"  , "maneuver declaration", None, lambda: dodeclareturn("R", "HT") ],
    ["BTR"  , "maneuver declaration", None, lambda: dodeclareturn("R", "BT") ],
    ["ETR"  , "maneuver declaration", None, lambda: dodeclareturn("R", "ET") ],
    
    ["BL"    , "bank"               , None, lambda: dobank("L")  ],
    ["BR"    , "bank"               , None, lambda: dobank("R")  ],
    ["WL"    , "bank"               , None, lambda: dobank(None) ],

    ["L90+"  , "maneuver"           , None, lambda: domaneuver("L",   90, True , True ) ],
    ["L60+"  , "maneuver"           , None, lambda: domaneuver("L",   60, True , True ) ],
    ["L30+"  , "maneuver"           , None, lambda: domaneuver("L",   30, True , True ) ],
    ["LLL+"  , "maneuver"           , None, lambda: domaneuver("L",   90, True , True ) ],
    ["LL+"   , "maneuver"           , None, lambda: domaneuver("L",   60, True , True ) ],
    ["L+"    , "maneuver"           , None, lambda: domaneuver("L", None, True , True ) ],
    
    ["R90+"  , "maneuver"           , None, lambda: domaneuver("R",   90, True , True ) ],
    ["R60+"  , "maneuver"           , None, lambda: domaneuver("R",   60, True , True ) ],
    ["R30+"  , "maneuver"           , None, lambda: domaneuver("R",   30, True , True ) ],
    ["RRR+"  , "maneuver"           , None, lambda: domaneuver("R",   90, True , True ) ],
    ["RR+"   , "maneuver"           , None, lambda: domaneuver("R",   60, True , True ) ],
    ["R+"    , "maneuver"           , None, lambda: domaneuver("R", None, True , True ) ],    

    ["LS180" , "maneuver"           , None, lambda: domaneuver("L",  180, True , False) ],
    ["L180"  , "maneuver"           , None, lambda: domaneuver("L",  180, False, False) ],
    ["L150"  , "maneuver"           , None, lambda: domaneuver("L",  150, True , False) ],
    ["L120"  , "maneuver"           , None, lambda: domaneuver("L",  120, True , False) ],
    ["L90"   , "maneuver"           , None, lambda: domaneuver("L",   90, True , False) ],
    ["L60"   , "maneuver"           , None, lambda: domaneuver("L",   60, True , False) ],
    ["L30"   , "maneuver"           , None, lambda: domaneuver("L",   30, True , False) ],
    ["LLL"   , "maneuver"           , None, lambda: domaneuver("L",   90, True , False) ],
    ["LL"    , "maneuver"           , None, lambda: domaneuver("L",   60, True , False) ],
    ["L"     , "maneuver"           , None, lambda: domaneuver("L", None, True , False) ],

    ["RS180" , "maneuver"           , None, lambda: domaneuver("R",  180, True , False) ],
    ["R180"  , "maneuver"           , None, lambda: domaneuver("R",  180, False, False) ],
    ["R150"  , "maneuver"           , None, lambda: domaneuver("R",  150, True , False) ],
    ["R120"  , "maneuver"           , None, lambda: domaneuver("R",  120, True , False) ],
    ["R90"   , "maneuver"           , None, lambda: domaneuver("R",   90, True , False) ],
    ["R60"   , "maneuver"           , None, lambda: domaneuver("R",   60, True , False) ],
    ["R30"   , "maneuver"           , None, lambda: domaneuver("R",   30, True , False) ],
    ["RRR"   , "maneuver"           , None, lambda: domaneuver("R",   90, True , False) ],
    ["RR"    , "maneuver"           , None, lambda: domaneuver("R",   60, True , False) ],
    ["R"     , "maneuver"           , None, lambda: domaneuver("R", None, True , False) ],

    ["S1/2"  , "other"              , None, lambda: dospeedbrakes(1/2) ],
    ["S1"    , "other"              , None, lambda: dospeedbrakes(1)   ],
    ["S3/2"  , "other"              , None, lambda: dospeedbrakes(3/2) ],
    ["S2"    , "other"              , None, lambda: dospeedbrakes(2)   ],
    ["S5/2"  , "other"              , None, lambda: dospeedbrakes(5/2) ],
    ["S3"    , "other"              , None, lambda: dospeedbrakes(3)   ],
    ["S7/2"  , "other"              , None, lambda: dospeedbrakes(7/2) ],
    ["S4"    , "other"              , None, lambda: dospeedbrakes(4)   ],
    ["SSSS"  , "other"              , None, lambda: dospeedbrakes(4)   ],
    ["SSS"   , "other"              , None, lambda: dospeedbrakes(3)   ],
    ["SS"    , "other"              , None, lambda: dospeedbrakes(2)   ],
    ["S"     , "other"              , None, lambda: dospeedbrakes(1)   ],
     
    ["J"     , "other"              , argsregex(1), lambda m: dojettison(m) ],
    
    ["AA"    , "other"              , argsregex(3), lambda m: doataattack(m) ],

    ["/"     , "other"              , None, lambda: None ],

    ["H"    , "H"                   , None, lambda: dohorizontal() ],

    ["C1"   , "C or D"              , None, lambda: doclimb(1) ],
    ["C2"   , "C or D"              , None, lambda: doclimb(2) ],
    ["CC"   , "C or D"              , None, lambda: doclimb(2) ],
    ["C"    , "C or D"              , None, lambda: doclimb(1) ],

    ["D1"   , "C or D"              , None, lambda: dodive(1) ],
    ["D2"   , "C or D"              , None, lambda: dodive(2) ],
    ["D3"   , "C or D"              , None, lambda: dodive(3) ],
    ["DDD"  , "C or D"              , None, lambda: dodive(3) ],
    ["DD"   , "C or D"              , None, lambda: dodive(2) ],
    ["D"    , "C or D"              , None, lambda: dodive(1) ],

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

  ]

  ########################################

  def doelements(action, selectedelementtype, allowrepeated):

    """
    Carry out the elements in an action that match the element type.
    """

    fullaction = action

    ielement = 0

    while action != "":

      for element in elementdispatchlist:

        elementcode      = element[0]
        elementtype      = element[1]
        elementregex     = element[2]
        elementprocedure = element[3]

        if elementcode == action[:len(elementcode)]:
          action = action[len(elementcode):]
          if elementregex == None:
            m = None
          else:
            m = re.compile(elementregex).match(action)
            if not m:
              raise RuntimeError("invalid arguments to %s element." % elementcode)
            if m:
              action = action[len(m.group()):]   
          if selectedelementtype == elementtype:
            ielement += 1
            if elementregex == None:
              elementprocedure()
            else:
              elementprocedure(m)
          break

      else:

        raise RuntimeError("invalid action %r." % action)

    if ielement > 1 and not allowrepeated:
      raise RuntimeError("invalid action %r: repeated %s element." % (fullaction, selectedelementtype))

    return ielement != 0
  
  ########################################

  def doaction(action):

    """
    Carry out an action for normal flight.
    """

    self._log1("FP %d" % (self._fp + 1), action)

    # Check we have at least one FP remaining.
    if self._fp + 1 > self._maxfp:
      raise RuntimeError(plural(self._maxfp,
        "only 1 FP is available",
        "only %.1f FPs are available." % self._maxfp))

    # Determine if this FP is the last FP of the move.
    self._lastfp = (self._fp + 2 > self._maxfp) 
    
    initialaltitude     = self._altitude
    initialaltitudeband = self._altitudeband
  
    try:
      
      declaredmaneuver    = None

      if doelements(action, "maneuvering departure", False):
    
        self._maneuveringdeparture = True

        assert aphex.isvalid(self._x, self._y, facing=self._facing)
        assert apaltitude.isvalidaltitude(self._altitude)
  
        self._logposition("end")
        self._continueflightpath()
    
        return

      self._horizontal = doelements(action, "H", False)
      self._vertical   = doelements(action, "C or D", False)

      if not self._horizontal and not self._vertical:
        raise RuntimeError("%r is not a valid action." % action)
      elif self._horizontal and self._vertical:
        if not flighttype == "UD" and not flighttype == "LVL":
          raise RuntimeError("%r is not a valid action when the flight type is %s." % (action, flighttype))

      self._fp += 1  
      if self._horizontal:
        self._hfp += 1
      elif self._hfp < self._mininitialhfp:
        raise RuntimeError("insufficient initial HFPs.")
      else:
       self._vfp += 1

      self._unloaded = (self._flighttype == "UD" and self._vertical)
      if self._unloaded:
        if self._firstunloadedfp == None:
          self._firstunloadedfp = self._hfp
        self._lastunloadedfp = self._hfp

      if doelements(action, "maneuver declaration", False):
        self._logevent("declared %s." % self.maneuver())

      # We save maneuvertype, as self._maneuvertype may be set to None of the
      # maneuver is completed below.

      maneuvertype = self._maneuvertype
      turning = _isturn(maneuvertype)
      rolling = _isroll(maneuvertype)
      sliding = _isslide(maneuvertype)
      
      # See rule 8.2.2 and 13.1.
      if not self._unloaded:
        if turning:
          self._maneuverfp += 1
        elif maneuvertype == "VR" and self._vertical:
          self._maneuverfp += 1
        elif apvariants.withvariant("use version 2.4 rules") and (maneuvertype == "DR" or maneuvertype == "LR"):
          self._maneuverfp += 1
        elif self._horizontal:
          self._maneuverfp += 1
    
      maneuver = doelements(action, "maneuver" , False)
      
      bank = doelements(action, "bank" , False)
      if bank and maneuver and not rolling:
        raise RuntimeError("attempt to bank immediately after a maneuver that is not a roll.")

      assert aphex.isvalid(self._x, self._y, facing=self._facing)
      assert apaltitude.isvalidaltitude(self._altitude)

    except RuntimeError as e:

      raise e
  
    finally:
      if self._lastfp:
        self._logpositionandmaneuver("end")
      else:
        self._logpositionandmaneuver("")
      self._continueflightpath()
        
    if turning and self._maneuversupersonic:
      self._turningsupersonic = True
    
      # See rules 9.1 and 13.3.6. We do this calculation here because any turn rate used in 
      # this turn is still reflected in self._maneuvertype; the turn may be stopped after the
      # facing change. The +1 is because the recovery period is this turn plus half of the
      # speed, rounding down.

    if maneuvertype == "ET":
      self._ETrecoveryfp   = int(self._speed / 2) + 1
      self._BTrecoveryfp   = -1
      self._rollrecoveryfp = -1
      self._HTrecoveryfp   = -1
      self._TTrecoveryfp   = -1
    elif maneuvertype == "BT":
      self._ETrecoveryfp   -= 1
      self._BTrecoveryfp   = int(self._speed / 2) + 1
      self._rollrecoveryfp = -1
      self._HTrecoveryfp   = -1
      self._TTrecoveryfp   = -1
    elif maneuvertype in ["VR", "LR", "DR"] or (self._hrd and self._fp == 1):
      self._ETrecoveryfp   -= 1
      self._BTrecoveryfp   = -1
      self._rollrecoveryfp = int(self._speed / 2) + 1
      self._HTrecoveryfp   = -1
      self._TTrecoveryfp   = -1
    elif maneuvertype == "HT":
      self._ETrecoveryfp   -= 1
      self._BTrecoveryfp   -= 1
      self._rollrecoveryfp -= 1
      self._HTrecoveryfp   = int(self._speed / 2) + 1
      self._TTrecoveryfp   = -1
    elif maneuvertype == "TT":
      self._ETrecoveryfp   -= 1
      self._BTrecoveryfp   -= 1
      self._rollrecoveryfp -= 1
      self._HTrecoveryfp   -= 1
      self._TTrecoveryfp   = int(self._speed / 2) + 1
    else:
      self._ETrecoveryfp   -= 1
      self._BTrecoveryfp   -= 1
      self._rollrecoveryfp -= 1
      self._HTrecoveryfp   -= 1
      self._TTrecoveryfp   -= 1

    if self._ETrecoveryfp == 0:
      self._logevent("recovered from ET.")
    if self._BTrecoveryfp == 0:
      self._logevent("recovered from BT.")
    if self._rollrecoveryfp == 0:
      self._logevent("recovered from roll.")
    if self._HTrecoveryfp == 0:
      self._logevent("recovered from HT.")
    if self._TTrecoveryfp == 0:
      self._logevent("recovered from TT.")
          
    # See rules 7.7 and 8.5.
    if maneuver and rolling:
      if initialaltitude > self.ceiling():
        self._logevent("check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
      elif initialaltitudeband == "EH" or initialaltitudeband == "UH":
        self._logevent("check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % initialaltitudeband)
    
    # See rules 7.7 and 8.5.
    if maneuver and turning:
      if initialaltitude > self.ceiling() and maneuvertype != "EZ":
        self._logevent("check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ.")
      if maneuvertype == "ET" and initialaltitude <= 25:
        self._gloccheck += 1
        self._logevent("check for GLOC as turn rate is ET and altitude band is %s (check %d in cycle)." % (initialaltitudeband, self._gloccheck))

    # See rule 7.8.
    if turning and self.closeformationsize() != 0:
      if (self.closeformationsize() > 2 and maneuvertype == "HT") or maneuvertype == "BT" or maneuvertype == "ET":
        self._logevent("close formation breaks down as the turn rate is %s." % maneuvertype)
        self._breakdowncloseformation()

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if rolling and self.closeformationsize() != 0:
      self._logevent("close formation breaks down aircraft is rolling.")
      self._breakdowncloseformation()      
    
    if initialaltitudeband != self._altitudeband:
      self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      
    self.checkforterraincollision()
    self.checkforleavingmap()
    if self._destroyed or self._leftmap:
      return

    doelements(action, "other", True)

    self._wasrollingonlastfp = rolling

  ########################################
  
  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype  
  
  if actions != "":
    for action in actions.split(","):
      if not self._destroyed and not self._leftmap:
        doaction(action)

  self._lognote(note)

  assert self._maneuveringdeparture or (self._fp == self._hfp + self._vfp)
  assert self._maneuveringdeparture or (self._fp <= self._maxfp)

  if self._destroyed or self._leftmap or self._maneuveringdeparture:
  
    self._endmove()

  elif self._fp + 1 > self._maxfp:

    # See rule 5.4.
    self._fpcarry = self._maxfp - self._fp

    self._endnormalflight()

################################################################################

def _startnormalflight(self, actions, note=False):
      
  """
  Start to carry out normal flight.
  """
  
  ########################################

  def reportapcarry():
     self._logevent("is carrying %+.2f APs." % self._apcarry)
 
  ########################################

  def reportaltitudecarry():
    if self._altitudecarry != 0:
     self._logevent("is carrying %.2f altitude levels." % self._altitudecarry)

  ########################################

  def determineallowedturnrates():

    """
    Determine the allowed turn rates according to the flight type and
    speed. The aircraft type and configuration may impose additional
    restrictions.
    """

    turnrates = ["EZ", "TT", "HT", "BT", "ET"]

    # See "Aircraft Damage Effects" in Play Aids.

    if self.damageatleast("C"):
      self._logevent("damage limits the turn rate to TT.")
      turnrates = turnrates[:2]
    elif self.damageatleast("2L"):
      self._logevent("damage limits the turn rate to HT.")
      turnrates = turnrates[:3]
    elif self.damageatleast("L"):
      self._logevent("damage limits the turn rate to BT.")
      turnrates = turnrates[:4]

    # See rule 7.5.

    minspeed = self.minspeed()
    if self._speed == minspeed:
      self._logevent("speed limits the turn rate to EZ.")
      turnrates = turnrates[:1]
    elif self._speed == minspeed + 0.5:
      self._logevent("speed limits the turn rate to TT.")
      turnrates = turnrates[:2]
    elif self._speed == minspeed + 1.0:
      self._logevent("speed limits the turn rate to HT.")
      turnrates = turnrates[:3]
    elif self._speed == minspeed + 1.5:
      self._logevent("speed limits the turn rate to BT.")
      turnrates = turnrates[:4]
    else:
      self._logevent("speed does not limit the turn rate.")

    # See rule 8.1.1.

    if self._flighttype == "ZC":
      self._logevent("ZC limits the turn rate to BT.")
      turnrates = turnrates[:4]

    # See rule 8.1.1.

    if self._flighttype == "SC":
      self._logevent("SC limits the turn rate to EZ.")
      turnrates = turnrates[:1]

    # See rule 8.1.3.

    if self._flighttype == "VC":
      self._logevent("VC disallows all turns.")
      turnrates = []

    self._allowedturnrates = turnrates

  ########################################

  def checkcloseformationlimits():

    if self.closeformationsize() == 0:
      return

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if self._hrd:
      self._logevent("close formation breaks down upon a HRD.")
      self._breakdowncloseformation()    

    # See rule 8.6.
    if flighttype == "ZC" or \
      (flighttype == "SC" and self._powersetting == "AB") or \
      flighttype == "VC" or \
      flighttype == "UD" or \
      flighttype == "VD":
      self._logevent("close formation breaks down as the flight type is %s." % flighttype)
      self._breakdowncloseformation()

    return

  ########################################

  def determinemaxfp():

    """
    Determine the number of FPs available, according to the speed and any 
    carried FPs.
    """

    # See rule 5.4.

    self._maxfp = self._speed + self._fpcarry
    self._logevent("has %.1f FPs (including %.1f carry)." % (self._maxfp, self._fpcarry))
    self._fpcarry = 0

  ########################################

  def determinefprequirements():

    """
    Determine the requirements on the use of FPs.
    """

    # See rule 5.5.
    # See rule 13.3.5 (with errata) on HRD restrictions.

    if (previousflighttype == "ZC" or previousflighttype == "SC") and flighttype == "VD":
      assert self._hrd
      mininitialhfp = self._speed // 3
    elif previousflighttype == "LVL" and (_isclimbingflight(flighttype) or _isdivingflight(flighttype)):
      mininitialhfp = 1
    elif (_isclimbingflight(previousflighttype) and _isdivingflight(flighttype)) or (_isdivingflight(previousflighttype) and _isclimbingflight(flighttype)):
      if self.hasproperty("HPR"):
        mininitialhfp = self._speed // 3
      else:
        mininitialhfp = self._speed // 2
    else:
      mininitialhfp = 0

    maxfp = int(self._maxfp)

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
      minhfp = math.ceil(onethird(maxfp))

    elif flighttype == "SC":

      # See blue sheet.
      minvfp = 1
      
      # See rule 8.1.2.
      if self._speed < self.minspeed() + 1.0:
        raise RuntimeError("insufficient speed for SC.")
      climbcapability = self.climbcapability()
      if self._speed < self.climbspeed():
        climbcapability /= 2
      if climbcapability < 1:
        maxvfp = 1
      else:
        maxvfp = math.floor(twothirds(maxfp))

    elif flighttype == "VC" or flighttype == "VD":

      # See blue sheet.
      minvfp = 1
      
      # See rules 8.1.3 and 8.2.3.
      if previousflighttype != flighttype:
        minhfp = math.floor(onethird(maxfp))
        maxhfp = minhfp
      else:
        maxhfp = math.floor(onethird(maxfp))

    elif flighttype == "SD":

      # See blue sheet.
      minvfp = 1
      
      # See rules 8.2.1 and 8.2.3.
      if previousflighttype == "VD":
        minvfp = math.floor(self._speed / 2)
      minhfp = math.ceil(onethird(maxfp))    

    elif flighttype == "UD":

      # See rules 8.2.2 and 8.2.3.
      maxvfp = 0
      maxunloadedhfp = maxfp
      if previousflighttype == "VD":
        minunloadedhfp = math.floor(self._speed / 2)
      else:
        minunloadedhfp = 1

    minhfp = max(minhfp, mininitialhfp)

    if maxvfp == 0:

      self._logevent("all FPs must be HFPs.")

    else:

      if mininitialhfp == 1:
        self._logevent("the first FP must be an HFP.")
      elif mininitialhfp > 1:
        self._logevent("the first %d FPs must be HFPs." % mininitialhfp)
      
      if minhfp == maxhfp:
        self._logevent(plural(minhfp,
          "exactly 1 FP must be an HFP.",
          "exactly %d FPs must be HFPs." % minhfp
        ))
      elif minhfp > 0 and maxhfp < maxfp:
        self._logevent("between %d and %d FP must be HFPs." % (minhfp, maxhfp))
      elif minhfp > 0:
        self._logevent(plural(minhfp,
          "at least 1 FP must be an HFP.",
          "at least %d FPs must be HFPs." % minhfp
        ))
      else:
        self._logevent(plural(maxhfp,
          "at most 1 FP may be an HFP.",
          "at most %d FPs may be HFPs." % maxhfp
        ))

      if minvfp == maxvfp:
        self._logevent(plural(minvfp,
          "exactly 1 FP must be a VFP.",
          "exactly %d FPs must be VFPs." % minvfp
        ))
      elif minvfp > 0 and maxvfp < maxfp:
        self._logevent("between %d and %d FP must be VFPs." % (minvfp, maxvfp))
      elif minvfp > 0:
        self._logevent(plural(minvfp,
          "at least 1 FP must be a VFP.",
          "at least %d FPs must be VFPs." % minvfp
        ))
      else:
        self._logevent(plural(maxvfp,
          "at most 1 FP may be a VFP.",
          "at most %d FPs may be VFPs." % maxvfp
        ))

    if minhfp > maxhfp:
      raise RuntimeError("flight type not permitted by HFP requirements.")
    if minvfp > maxvfp:
      raise RuntimeError("flight type not permitted by VFP requirements.")
  
    if minunloadedhfp > 0:
      self._logevent(plural(minunloadedhfp,
        "at least 1 FP must be an unloaded HFP.",
        "at least %d FPs must be unloaded HFPs." % minunloadedhfp
      ))

    self._mininitialhfp  = mininitialhfp
    self._minhfp         = minhfp
    self._maxhfp         = maxhfp
    self._minvfp         = minvfp
    self._maxvfp         = maxvfp
    self._minunloadedhfp = minunloadedhfp
    self._maxunloadedhfp = maxunloadedhfp      

  ########################################

  def handlecarriedturn():

    """
    Handle any carried turn.
    """

    if _isturn(self._maneuvertype):

      # See rule 7.7.

      # Issue: The consequences of carried turn violating the turn
      # requirements of ZC, SC, and VC flight are not clear, but for the
      # moment we assume they result in a maneuvering departure.

      turnrequirement = apturnrate.turnrequirement(self._altitudeband, self._speed, self._maneuvertype)
      if not self._maneuvertype in self._allowedturnrates or turnrequirement == None:
        self._logevent("carried turn rate is tighter than the maximum allowed turn rate.")
        raise RuntimeError("aircraft has entered departed flight while maneuvering.")

      # See rule 7.1.

      previousmaneuverrequiredfp    = self._maneuverrequiredfp
      previous_maneuverfacingchange = self._maneuverfacingchange

      self._maneuversupersonic   = self._speed >= apspeed.m1speed(self._altitudeband)
      turnrequirement = apturnrate.turnrequirement(self._altitudeband, self._speed, self._maneuvertype)
      if turnrequirement >= 60:
        self._maneuverrequiredfp   = 1
        self._maneuverfacingchange = turnrequirement
      else:
        self._maneuverrequiredfp   = turnrequirement
        self._maneuverfacingchange = 30

      if self._maneuverrequiredfp != previousmaneuverrequiredfp or self._maneuverfacingchange != previous_maneuverfacingchange:
        if self._maneuverfacingchange > 30:
          self._logevent("turn requirement changed to %d in 1 FP." % self._maneuverfacingchange)
        else:
          self._logevent("turn requirement changed to %s." % plural(self._maneuverrequiredfp, "1 FP", "%d FPs" % self._maneuverrequiredfp))

      self._maxturnrate       = self._maneuvertype
      self._turningsupersonic = self._maneuversupersonic

    else:

      self._maxturnrate       = None
      self._turningsupersonic = False
      
  ########################################

  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype  
  
  # These keep track of the number of FPs, HFPs, and VFPs used and the
  # number of FPs lost to speedbrakes. They are used to ensure that the
  # right mix of HFPs and VFPs are used and to determine when the turn
  # ends.

  self._fp     = 0
  self._hfp    = 0
  self._vfp    = 0
  self._spbrfp = 0

  # These keep track of the index of the first and last unloaded HFPs
  # in an UD. They are then used to ensure that the unloaded HFPs are
  # continuous.

  self._firstunloadedfp = None
  self._lastunloadedfp  = None

  # This keeps track of the number of turns, rolls, and vertical rolls.

  self._turnmaneuvers = 0
  self._rollmaneuvers = 0
  self._verticalrolls = 0

  # The number of slides performed and the FP of the last last performed.
  self._slides = 0
  self._slidefp = 0

  reportapcarry()
  reportaltitudecarry()
  determineallowedturnrates()
  handlecarriedturn()
  checkcloseformationlimits()
  determinemaxfp()
  determinefprequirements()
    
  self._logpositionandmaneuver("start")

  self._continuenormalflight(actions, note=note)

################################################################################

def _endnormalflight(self):

  ########################################

  def reportfp():
    self._logevent("used %s and %s." % (
      plural(self._hfp, "1 HFP", "%d HFPs" % self._hfp),
      plural(self._vfp, "1 VFP", "%d VFPs" % self._vfp)
    ))    
    if self._spbrfp > 0:
      self._logevent("lost %.1f FPs to speedbrakes." % self._spbrfp)
    self._logevent("will carry %.1f FPs." % self._fpcarry)

  ########################################

  def checkfp():

    if self._hfp < self._minhfp:
      raise RuntimeError("too few HFPs.")

    if self._hfp > self._maxhfp:
      raise RuntimeError("too many HFPs.")  
      
    if self._vfp < self._minvfp:
      raise RuntimeError("too few VFPs.")

    if self._vfp > self._maxvfp:
      raise RuntimeError("too many VFPs.")

    if self._flighttype == "UD":
      # See rule 8.2.2.
      unloadedhfp = self._previousaltitude - self._altitude
      if self._firstunloadedfp == None:
        n = 0
      elif self._lastunloadedfp == None:
        n = self._hfp - self._firstunloadedfp + 1
      else:
        n = self._lastunloadedfp - self._firstunloadedfp + 1
      if n != unloadedhfp:
        raise RuntimeError("unloaded HFPs must be continuous.")
      if unloadedhfp < self._minunloadedhfp:
        raise RuntimeError("too few unloaded HFPs.")
      if unloadedhfp > self._maxunloadedhfp:
        raise RuntimeError("too many unloaded HFPs.")

  ########################################

  def checkfreedescent():

    # See rule 8.2.4.
    
    if self._flighttype == "LVL":
      altitudechange = self._altitude - self._previousaltitude
      if altitudechange < -1:
        raise RuntimeError("free descent cannot only be taken once per move.")      

  ########################################

  def reportgloccycle():

    # See rule 7.6.
    if self._gloccheck > 0 and self._maxturnrate != "ET" and self._maxturnrate != "BT":
      self._logevent("GLOC cycle ended.")
      self._gloccheck = 0 

  ########################################

  def reportcarry():

    if self._altitudecarry != 0:
      self._logevent("is carrying %.2f altitude levels." % self._altitudecarry)
          
  ########################################

  def determinemaxturnrateap():

    """
    Determine the APs from the maximum turn rate used.
    """

    if self._maxturnrate != None:
      self.turnrateap = -self.turndrag(self._maxturnrate)
    else:
      self.turnrateap = 0

    if self._turningsupersonic:
      if self.hasproperty("PSSM"):
        self.turnrateap -= 2.0
      elif not self.hasproperty("GSSM"):
        self.turnrateap -= 1.0

  ########################################

  def determinealtitudeap():

    altitudechange = self._altitude - self._previousaltitude

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
        self._scwithzccomponent = False

      else:

        # See rule 8.1.2 and 8.1.4.

        climbcapability = self._effectiveclimbcapability

        # We need to figure out how much was climbed at the SC rate and
        # how much was climbed at the ZC rate. This is complicated since
        # altitudechange can be more than the climbcapability because of
        # altitudecarry. Therefore, we calculate how much was at the ZC
        # rate from the true altitude change, including carry, and then
        # assume that any difference was at the SC rate.
        # 
        # We also use that the altitude change at the ZC rate must be an
        # integral number of levels.

        truealtitude     = self._altitude         + self._altitudecarry
        lasttruealtitude = self._previousaltitude + self._previousaltitudecarry

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
        self._scwithzccomponent = (zcaltitudechange != 0)

    elif flighttype == "VC":

      # See rule 8.1.3.
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

    self._altitudeap = altitudeap

  ########################################

  def checkcloseformationlimits():

    if self.closeformationsize() == 0:
      return

    # See rule 8.6. The other climbing and diving cases are handled at
    # the start of the move.

    altitudeloss = self._previousaltitude - self._altitude
    if flighttype == "SD" and altitudeloss > 2:
      self._logevent("close formation breaks down as the aircraft lost %d levels in an SD." % altitudeloss)
      self._breakdowncloseformation()
    elif flighttype == "SC" and self._scwithzccomponent:
      self._logevent("close formation breaks down as the aircraft climbed faster than the sustained climb rate.")
      self._breakdowncloseformation()
      
  ########################################

  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype  
  
  if not self._maneuveringdeparture:
    reportfp()
    checkfp()
    checkfreedescent()
    reportcarry()
    reportgloccycle()
    determinemaxturnrateap()
    determinealtitudeap()
    checkcloseformationlimits()

  self._endmove()

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
