"""
Normal flight for the aircraft class.
"""

import math
from typing_extensions import LiteralString
from apengine.math import onethird, twothirds, roundtoquarter

import apengine.altitude as apaltitude
import apengine.hex      as aphex
import apengine.speed    as apspeed
import apengine.turnrate as apturnrate
import apengine.variants as apvariants

from apengine.log import plural

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
      self._log("- check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
    elif self._altitudeband == "EH" or self._altitudeband == "UH":
      self._log("- check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % self._altitudeband)  
      
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

    if _isclimbing(flighttype):
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))
    elif flighttype == "LVL" and not self.hasproperty("HPR"):
      raise RuntimeError("flight type immediately after %s cannot be %s." % (
        previousflighttype, flighttype
      ))
    
  if previousflighttype == "ST":

    # See rule 6.4 on recovering from stalled flight.

    if _isclimbing(flighttype):
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

    if _isdiving(previousflighttype):
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

def _continuenormalflight(self, actions):

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
      self._maneuvertype  = None
      self._maneuversense = None
      self._maneuverfp    = 0

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

    turnrates = ["EZ", "TT", "HT", "BT", "ET"]
    assert turnrate in turnrates

    if turnrate not in self._allowedturnrates:
      raise RuntimeError("attempt to declare a turn rate tighter than allowed by the flight type.")

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
    self._maneuveraltitudeband = self._altitudeband
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))

  ########################################

  def doturn(sense, facingchange):

    """
    Turn in the specified sense and amount.
    """

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to turn while flight type is %s." % flighttype)
      
    # See rule 7.1.

    minturnrate = apturnrate.determineturnrate(self._maneuveraltitudeband, self._speed, self._maneuverfp, facingchange)
    if minturnrate == None:
      raise RuntimeError("attempt to turn faster than the maximum turn rate.")

    turnrates = ["EZ", "TT", "HT", "BT", "ET"]
    if turnrates.index(minturnrate) > turnrates.index(self._maneuvertype):
      raise RuntimeError("attempt to turn faster than the declared turn rate.")

    if self._turnmaneuvers > 0:
      if apvariants.withvariant("prefer v1 bleed rates"):
        # Use the bleed rates from the 1st edition rules in TSOH.
        if self.hasproperty("HBR"):
          self._sustainedturnap -= facingchange // 30 * 2.0
        else:
          self._sustainedturnap -= facingchange // 30 * 1.0
      else:
        # Use the proposed bleed rates for 2nd edition from p. 4 of APJ 32.
        if self.hasproperty("LBR"):
          self._sustainedturnap -= facingchange // 30 * 0.5
        elif self.hasproperty("HBR"):
          self._sustainedturnap -= facingchange // 30 * 1.5
        else:
          self._sustainedturnap -= facingchange // 30 * 1.0

    self._turnmaneuvers += 1
    
    # Change facing.
    if aphex.isedge(self._x, self._y):
      self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

    # Implicitly continue the turn.
    self._maneuverfp           = 0
    self._maneuveraltitudeband = self._altitudeband
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))

  ########################################

  def dodeclareslide(sense):

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to declare slide while flight type is %s." % flighttype)

    # See 13.2.
    if self._slides == 1 and self._speed <= 9.0:
      raise RuntimeError("only one slide allowed per turn at low speed.")
    if self._slides == 1 and self._fp - self._slidefp - 1 <  4:
      raise RuntimeError("attempt to start a second slide without sufficient intermediate FPs.")
    elif self._slides == 2:
      raise RuntimeError("at most two slides allowed per turn.")

    self._bank                 = None
    self._maneuvertype         = "SL"
    self._maneuversense        = sense
    self._maneuverfp           = 0
    self._maneuveraltitudeband = self._altitudeband
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))
    
  ########################################

  def doslide(sense):

    # See rule 8.1.3 and 8.2.3
    if flighttype == "VC" or flighttype == "VD":
      raise RuntimeError("attempt to slide while flight type is %s." % flighttype)

    # See rules 13.1 and 13.2.
    requiredfp = 2 + _extrapreparatoryhfp(self._altitudeband, self._speed)

    # The +1 in the next test because we are performing this calculation after
    # the final H in the slide has been included in self._maneuverfp.
    if self._maneuverfp < requiredfp + 1:
      raise RuntimeError("attempt to slide without sufficient preparatory HFPs.")

    # Slide. Remember that we have already moved forward one hex for the final H element.
    self._x, self._y = aphex.slide(self._x, self._y, self._facing, sense)

    # See rule 13.2.
    if self._slides >= 1:
      self._othermaneuversap -= 1.0

    # Keep track of the number of slides and the FP of the last slide.
    self._slides += 1
    self._slidefp = self._fp

    # Do not implicitly continue the maneuver.
    self._maneuvertype         = None
    self._maneuversense        = None
    self._maneuverfp           = 0
    self._maneuveraltitudeband = None
    self._maneuversupersonic   = False

    # Implicitly finish with wings level.
    self._bank = None

  ########################################

  def dodeclaredisplacementroll(sense):

    # See rule 13.3.1

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
    self._maneuverfp           = 0
    self._maneuveraltitudeband = self._altitudeband
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))

  ########################################

  def dodisplacementroll(sense):

    # See rules 13.1 and 13.3.1.

    requiredfp = self.rollhfp() + _extrapreparatoryhfp(self._altitudeband, self._speed)

    # The +1 in the next test because we are performing this calculation after
    # the final H in the slide has been included in self._maneuverfp.
    if self._maneuverfp < requiredfp + 1:
      raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")

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
    
    # Do not implicitly continue the maneuver.
    self._maneuvertype         = None
    self._maneuversense        = None
    self._maneuverfp           = 0
    self._maneuveraltitudeband = None
    self._maneuversupersonic   = False

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
    self._maneuverfp           = 0
    self._maneuveraltitudeband = self._altitudeband
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))

  ########################################

  def dolagroll(sense):

    # See rules 13.1 and 13.3.2.

    requiredfp = self.rollhfp() + _extrapreparatoryhfp(self._altitudeband, self._speed)

    # The +1 in the next test because we are performing this calculation after
    # the final H in the slide has been included in self._maneuverfp.
    if self._maneuverfp < requiredfp + 1:
      raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")

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
    
    # Do not implicitly continue the maneuver.
    self._maneuvertype         = None
    self._maneuversense        = None
    self._maneuverfp           = 0
    self._maneuveraltitudeband = None
    self._maneuversupersonic   = False

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
    self._maneuverfp           = 0
    self._maneuveraltitudeband = self._altitudeband
    self._maneuversupersonic   = (self._speed >= apspeed.m1speed(self._altitudeband))

    ########################################

  def doverticalroll(sense, facingchange, shift):

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
    if aphex.isedge(self._x, self._y) and shift:
      self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

    # Do not implicitly continue the maneuver.
    self._maneuvertype         = None
    self._maneuversense        = None
    self._maneuverfp           = 0
    self._maneuveraltitudeband = None
    self._maneuversupersonic   = False
    
    ########################################

  def domaneuver(sense, facingchange, shift):

    if self._maneuvertype == None:
      raise RuntimeError("attempt to maneuver without a declaration.")
      
    if self._maneuversense != sense:
      raise RuntimeError("attempt to maneuver against the sense of the declaration.")

    if self._maneuvertype == "SL":
      if facingchange != None:
        raise RuntimeError("invalid facing change for slide.")
      doslide(sense)
    elif self._maneuvertype == "DR":
      if facingchange != None:
        raise RuntimeError("invalid facing change for a displacement roll.")
      dodisplacementroll(sense)
    elif self._maneuvertype == "LR":
      if facingchange != None:
        raise RuntimeError("invalid facing change for a lag roll.")
      dolagroll(sense)
    elif self._maneuvertype == "VR":
      if facingchange == None:
        facingchange = 30
      doverticalroll(sense, facingchange, shift)
    else:
      if facingchange == None:
        facingchange = 30
      doturn(sense, facingchange)

  ########################################

  def dospeedbrakes(spbrfp):

    """
    Use the speedbrakes.
    """

    # See rules 6.5 and 6.6.

    maxspbrfp = self.spbr()

    if self._spbrfp != 0:
      raise RuntimeError("speedbrakes can only be used once per turn.")

    maxspbrfp = self._maxfp - self._hfp - self._vfp
    if spbrfp > maxspbrfp:
      raise RuntimeError(plural(maxspbrfp,
        "only 1 FP remains.",
        "only %s remain." % maxspbrfp))
    
    maxspbrfp = self.spbr()
    if maxspbrfp == None:
      raise RuntimeError("aircraft does not have speedbrakes.")

    if self._speed > apspeed.m1speed(self._altitudeband):
      maxspbrfp += 0.5
    if spbrfp > maxspbrfp:
      raise RuntimeError(plural(maxspbrfp,
        "speedbrake capability is only 1 FP.",
        "speedbrake capability is only %.1f FPs." % maxspbrfp))

    self._spbrfp = spbrfp
    self._maxfp -= spbrfp

    self._spbrap = -spbrfp / 0.5

  ########################################

  def dojettison(configuration):

    """
    Jetison stores to achieve the specified configuration.
    """

    # See rule 4.4. 
  
    # We implement the delay of 1 FP by making this an other element.

    if self._configuration == configuration:
      raise RuntimeError("configuration is already %s." % configuration)
    if self._configuration == "CL" or configuration == "DT":
      raise RuntimeError("attempt to change from configuration %s to %s." % (self._configuration, configuration))
    self._logevent("jettisoned stores.")
    self._logevent("configuration changed from %s to %s." % (self._configuration, configuration))
    self._configuration = configuration
  
  ########################################

  def doattack(weapon):

    """
    Declare an attack with the specified weapon.
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

    self._logevent("- attack using %s." % weapon)
    if self._maxturnrate != None:
      self._logevent("- maximum turn rate so far is %s." % self._maxturnrate)
    else:
      self._logevent("- no turns used so far.")

  ########################################

  def dokilled():

    """
    Declare that the aircraft has been killed.
    """

    self._logevent("- aircraft has been killed.")
    self._destroyed = True

  ########################################

  def domaneuveringdeparture(sense, facingchange):

    shift = int((self._maxfp - self._fp) / 2)

    # Do the first facing change.

    if aphex.isedge(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing, sense)
    if action[0] == "L":
      self._facing = (self._facing + 30) % 360
    else:
      self._facing = (self._facing - 30) % 360
    self._continueflightpath()
    facingchange -= 30

    # Shift.

    for i in range(0, shift):
      self._x, self._y = aphex.forward(self._x, self._y, self._facing)
      self.checkforterraincollision()
      self.checkforleavingmap()
      if self._destroyed or self._leftmap:
        return

    # Do any remaining facing changes.
    if aphex.isedge(self._x, self._y):
      self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
    if action[0] == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

  ########################################

  elementdispatchlist = [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

    # [0] is the element code.
    # [1] is the element type.
    # [2] is the element procedure.
  
    ["SLL"  , "maneuver declaration", lambda: dodeclareslide("L") ],
    ["SLR"  , "maneuver declaration", lambda: dodeclareslide("R") ],

    ["DRL"  , "maneuver declaration", lambda: dodeclaredisplacementroll("L") ],
    ["DRR"  , "maneuver declaration", lambda: dodeclaredisplacementroll("R") ],

    ["LRL"  , "maneuver declaration", lambda: dodeclarelagroll("L") ],
    ["LRR"  , "maneuver declaration", lambda: dodeclarelagroll("R") ],
        
    ["VRL"  , "maneuver declaration", lambda: dodeclareverticalroll("L") ],
    ["VRR"  , "maneuver declaration", lambda: dodeclareverticalroll("R") ],
    
    ["EZL"  , "maneuver declaration", lambda: dodeclareturn("L", "EZ") ],
    ["TTL"  , "maneuver declaration", lambda: dodeclareturn("L", "TT") ],
    ["HTL"  , "maneuver declaration", lambda: dodeclareturn("L", "HT") ],
    ["BTL"  , "maneuver declaration", lambda: dodeclareturn("L", "BT") ],
    ["ETL"  , "maneuver declaration", lambda: dodeclareturn("L", "ET") ],
    
    ["EZR"  , "maneuver declaration", lambda: dodeclareturn("R", "EZ") ],
    ["TTR"  , "maneuver declaration", lambda: dodeclareturn("R", "TT") ],
    ["HTR"  , "maneuver declaration", lambda: dodeclareturn("R", "HT") ],
    ["BTR"  , "maneuver declaration", lambda: dodeclareturn("R", "BT") ],
    ["ETR"  , "maneuver declaration", lambda: dodeclareturn("R", "ET") ],
    
    ["BKL"   , "bank"               , lambda: dobank("L")  ],
    ["BKR"   , "bank"               , lambda: dobank("R")  ],
    ["WL"    , "bank"               , lambda: dobank(None) ],

    ["LS180" , "maneuver"           , lambda: domaneuver("L",  180, True )],
    ["L180"  , "maneuver"           , lambda: domaneuver("L",  180, False)],
    ["L150"  , "maneuver"           , lambda: domaneuver("L",  150, True )],
    ["L120"  , "maneuver"           , lambda: domaneuver("L",  120, True )],
    ["L90"   , "maneuver"           , lambda: domaneuver("L",   90, True ) ],
    ["L60"   , "maneuver"           , lambda: domaneuver("L",   60, True ) ],
    ["L30"   , "maneuver"           , lambda: domaneuver("L",   30, True ) ],
    ["LLL"   , "maneuver"           , lambda: domaneuver("L",   90, True ) ],
    ["LL"    , "maneuver"           , lambda: domaneuver("L",   60, True ) ],
    ["L"     , "maneuver"           , lambda: domaneuver("L", None, True ) ],

    ["RS180" , "maneuver"           , lambda: domaneuver("R",  180, True )],
    ["R180"  , "maneuver"           , lambda: domaneuver("R",  180, False)],
    ["R150"  , "maneuver"           , lambda: domaneuver("R",  150, True )],
    ["R120"  , "maneuver"           , lambda: domaneuver("R",  120, True )],
    ["R90"   , "maneuver"           , lambda: domaneuver("R",   90, True ) ],
    ["R60"   , "maneuver"           , lambda: domaneuver("R",   60, True ) ],
    ["R30"   , "maneuver"           , lambda: domaneuver("R",   30, True ) ],
    ["RRR"   , "maneuver"           , lambda: domaneuver("R",   90, True ) ],
    ["RR"    , "maneuver"           , lambda: domaneuver("R",   60, True ) ],
    ["R"     , "maneuver"           , lambda: domaneuver("R", None, True ) ],

    ["S1/2"  , "other"              , lambda: dospeedbrakes(1/2) ],
    ["S1"    , "other"              , lambda: dospeedbrakes(1) ],
    ["S3/2"  , "other"              , lambda: dospeedbrakes(3/2) ],
    ["S2"    , "other"              , lambda: dospeedbrakes(2) ],
    ["S5/2"  , "other"              , lambda: dospeedbrakes(5/2) ],
    ["S3"    , "other"              , lambda: dospeedbrakes(3) ],
    ["SSS"   , "other"              , lambda: dospeedbrakes(3/2) ],
    ["SS"    , "other"              , lambda: dospeedbrakes(1) ],
    ["S"     , "other"              , lambda: dospeedbrakes(1/2) ],
    
    ["J1/2"  , "other"              , lambda: dojettison("1/2") ],
    ["JCL"   , "other"              , lambda: dojettison("CL") ],
    
    ["AGN"   , "other"              , lambda: doattack("guns") ],
    ["AGP"   , "other"              , lambda: doattack("gun pod") ],
    ["ARK"   , "other"              , lambda: doattack("rockets") ],
    ["ARP"   , "other"              , lambda: doattack("rocket pods") ],

    ["K"     , "other"              , lambda: dokilled()],

    ["/"     , "other"              , lambda: None ],

    ["H"    , "H"                   , lambda: dohorizontal() ],

    ["C1"   , "C or D"              , lambda: doclimb(1) ],
    ["C2"   , "C or D"              , lambda: doclimb(2) ],
    ["CC"   , "C or D"              , lambda: doclimb(2) ],
    ["C"    , "C or D"              , lambda: doclimb(1) ],

    ["D1"   , "C or D"              , lambda: dodive(1) ],
    ["D2"   , "C or D"              , lambda: dodive(2) ],
    ["D3"   , "C or D"              , lambda: dodive(3) ],
    ["DDD"  , "C or D"              , lambda: dodive(3) ],
    ["DD"   , "C or D"              , lambda: dodive(2) ],
    ["D"    , "C or D"              , lambda: dodive(1) ],

    ["MDL300", "maneuvering departure", lambda: domaneuveringdeparture("L", 300)],
    ["MDL270", "maneuvering departure", lambda: domaneuveringdeparture("L", 270)],
    ["MDL240", "maneuvering departure", lambda: domaneuveringdeparture("L", 240)],
    ["MDL210", "maneuvering departure", lambda: domaneuveringdeparture("L", 210)],
    ["MDL180", "maneuvering departure", lambda: domaneuveringdeparture("L", 180)],
    ["MDL150", "maneuvering departure", lambda: domaneuveringdeparture("L", 150)],
    ["MDL120", "maneuvering departure", lambda: domaneuveringdeparture("L", 120)],
    ["MDL90" , "maneuvering departure", lambda: domaneuveringdeparture("L",  90)],
    ["MDL60" , "maneuvering departure", lambda: domaneuveringdeparture("L",  60)],
    ["MDL30" , "maneuvering departure", lambda: domaneuveringdeparture("L",  30)],
    
    ["MDR300", "maneuvering departure", lambda: domaneuveringdeparture("R", 300)],
    ["MDR270", "maneuvering departure", lambda: domaneuveringdeparture("R", 270)],
    ["MDR240", "maneuvering departure", lambda: domaneuveringdeparture("R", 240)],
    ["MDR210", "maneuvering departure", lambda: domaneuveringdeparture("R", 210)],
    ["MDR180", "maneuvering departure", lambda: domaneuveringdeparture("R", 180)],
    ["MDR150", "maneuvering departure", lambda: domaneuveringdeparture("R", 150)],
    ["MDR120", "maneuvering departure", lambda: domaneuveringdeparture("R", 120)],
    ["MDR90" , "maneuvering departure", lambda: domaneuveringdeparture("R",  90)],
    ["MDR60" , "maneuvering departure", lambda: domaneuveringdeparture("R",  60)],
    ["MDR30" , "maneuvering departure", lambda: domaneuveringdeparture("R",  30)],

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

        elementcode = element[0]
        elementtype = element[1]
        elementprocedure = element[2]

        if len(elementcode) <= len(action) and elementcode == action[:len(elementcode)]:
          if selectedelementtype == elementtype:
            ielement += 1
            elementprocedure()
          action = action[len(elementcode):]
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
      
      if doelements(action, "maneuvering departure", False):
    
        self._maneuveringdeparture = True

        assert aphex.isvalid(self._x, self._y, facing=self._facing)
        assert apaltitude.isvalidaltitude(self._altitude)
  
        self._logaction("end", action, self.position())
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

      doelements(action, "maneuver declaration", False)

      # See rule 8.2.2 and 13.1.
      if not self._unloaded:
        if _isturn(self._maneuvertype):
          self._maneuverfp += 1
        elif self._maneuvertype == "VR" and self._vertical:
          self._maneuverfp += 1
        elif self._horizontal:
          self._maneuverfp += 1

      turning = _isturn(self._maneuvertype)
      rolling = _isroll(self._maneuvertype)
      maneuver = doelements(action, "maneuver" , False)

      bank = doelements(action, "bank" , False)
      if bank and maneuver and not rolling:
        raise RuntimeError("attempt to bank immediately after a maneuver that is not a roll.")

      assert aphex.isvalid(self._x, self._y, facing=self._facing)
      assert apaltitude.isvalidaltitude(self._altitude)

    except RuntimeError as e:
      self._logaction("FP %d" % self._fp, action, "")
      raise e
  
    self._logaction("FP %d" % self._fp, action, self.position())
    self._continueflightpath()

    if turning and self._maneuversupersonic:
      self._turningsupersonic = True
    
    # See rules 7.7 and 8.5.
    if maneuver and rolling:
      if initialaltitude > self.ceiling():
        self._logevent("- check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
      elif initialaltitudeband == "EH" or initialaltitudeband == "UH":
        self._logevent("- check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % initialaltitudeband)
    
    # See rules 7.7 and 8.5.
    if maneuver and turning:
      if initialaltitude > self.ceiling() and self._maneuvertype != "EZ":
        self._logevent("- check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ.")
      if self._maneuvertype == "ET" and initialaltitude <= 25:
        self._gloccheck += 1
        self._log("- check for GLOC as turn rate is ET and altitude band is %s (check %d in cycle)." % (initialaltitudeband, self._gloccheck))

    # See rule 7.8.
    if turning and self.closeformationsize() != 0:
      if (self.closeformationsize() > 2 and self._maneuvertype == "HT") or self._maneuvertype == "BT" or self._maneuvertype == "ET":
        self._log("- close formation breaks down as the turn rate is %s." % self._maneuvertype)
        self._breakdowncloseformation()

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if rolling and self.closeformationsize() != 0:
      self._log("- close formation breaks down aircraft is rolling.")
      self._breakdowncloseformation()      
    
    if initialaltitudeband != self._altitudeband:
      self._logevent("- altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      
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

  assert self._maneuveringdeparture or (self._fp == self._hfp + self._vfp)
  assert self._maneuveringdeparture or (self._fp <= self._maxfp)

  if self._destroyed or self._leftmap or self._maneuveringdeparture:
  
    self._log("---")
    self._endmove()

  elif self._fp + 1 > self._maxfp:

    # See rule 5.4.
    self._fpcarry = self._maxfp - self._fp

    self._endnormalflight()

################################################################################

def _startnormalflight(self, actions):
      
  """
  Start to carry out normal flight.
  """
  
  ########################################

  def reportapcarry():
     self._log("- is carrying %+.2f APs." % self._apcarry)
 
  ########################################

  def reportaltitudecarry():
    if self._altitudecarry != 0:
     self._log("- is carrying %.2f altitude levels." % self._altitudecarry)

  ########################################

  def reportcarriedmaneuver():

    if self._maneuvertype != None:
      self._log("- is carrying %s for %s%s." % (
        plural(self._maneuverfp, "1 FP", "%d FPs" % self._maneuverfp), 
        self._maneuvertype, self._maneuversense))
    elif self._bank == None:
      self._log("- has wings level.")
    else:
      self._log("- is banked %s." % self._bank)

  ########################################

  def determineinitialmaxturnrate():

    """
    Determine the initial maximum turn rate, according to any carried turn.
    """

    if _isturn(self._maneuvertype):
      self._maxturnrate       = self._maneuvertype
      self._turningsupersonic = self._maneuversupersonic
    else:
      self._maxturnrate       = None
      self._turningsupersonic = False

  ########################################

  def determineallowedturnrates():

    """
    Determine the allowed turn rates according to the flight type and
    speed. The aircraft type and configuration may impose additional
    restrictions.
    """

    turnrates = ["EZ", "TT", "HT", "BT", "ET"]

    # See rule 7.5.

    minspeed = self.minspeed()
    if self._speed == minspeed + 1.5:
      self._log("- speed limits the turn rate to BT.")
      turnrates = turnrates[:4]
    elif self._speed == minspeed + 1.0:
      self._log("- speed limits the turn rate to HT.")
      turnrates = turnrates[:3]
    elif self._speed == minspeed + 0.5:
      self._log("- speed limits the turn rate to TT.")
      turnrates = turnrates[:2]
    elif self._speed == minspeed:
      self._log("- speed limits the turn rate to EZ.")
      turnrates = turnrates[:1]

    # See rule 8.1.1.

    if self._flighttype == "ZC":
      self._log("- ZC limits the turn rate to BT.")
      turnrates = turnrates[:4]

    # See rule 8.1.1.

    if self._flighttype == "SC":
      self._log("- SC limits the turn rate to EZ.")
      turnrates = turnrates[:1]

    # See rule 8.1.3.

    if self._flighttype == "VC":
      self._log("- VC disallows all turns.")
      turnrates = []

    self._allowedturnrates = turnrates

  ########################################

  def checkcloseformationlimits():

    if self.closeformationsize() == 0:
      return

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if self._hrd:
      self._log("- close formation breaks down upon a HRD.")
      self._breakdowncloseformation()    

    # See rule 8.6.
    if flighttype == "ZC" or \
      (flighttype == "SC" and self._powersetting == "AB") or \
      flighttype == "VC" or \
      flighttype == "UD" or \
      flighttype == "VD":
      self._log("- close formation breaks down as the flight type is %s." % flighttype)
      self._breakdowncloseformation()

    return

  ########################################

  def checkformaneuveringdeparture():

    """
    Check for a maneuvering departure caused by a carried turn exceeding the 
    maximum allowed turn rate.
    """

    # See rule 7.7.

    # Issue: The consequences of carried turn violating the turn
    # requirements of ZC, SC, and VC flight are not clear, but for the
    # moment we assume they result in a maneuvering departure.

    if _isturn(self._maneuvertype) and not self._maneuvertype in self._allowedturnrates:
      self._log("- carried turn rate is tighter than the maximum allowed turn rate.")
      raise RuntimeError("aircraft has entered departured flight while maneuvering.")

  ########################################

  def determinemaxfp():

    """
    Determine the number of FPs available, according to the speed and any 
    carried FPs.
    """

    # See rule 5.4.

    self._maxfp = self._speed + self._fpcarry
    self._log("- has %.1f FPs (including %.1f carry)." % (self._maxfp, self._fpcarry))
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
    elif previousflighttype == "LVL" and (_isclimbing(flighttype) or _isdiving(flighttype)):
      mininitialhfp = 1
    elif (_isclimbing(previousflighttype) and _isdiving(flighttype)) or (_isdiving(previousflighttype) and _isclimbing(flighttype)):
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

      self._log("- all FPs must be HFPs.")

    else:

      if mininitialhfp == 1:
        self._log("- the first FP must be an HFP.")
      elif mininitialhfp > 1:
        self._log("- the first %d FPs must be HFPs." % mininitialhfp)
      
      if minhfp == maxhfp:
        self._log(plural(minhfp,
          "- exactly 1 FP must be an HFP.",
          "- exactly %d FPs must be HFPs." % minhfp
        ))
      elif minhfp > 0 and maxhfp < maxfp:
        self._log("- between %d and %d FP must be HFPs." % (minhfp, maxhfp))
      elif minhfp > 0:
        self._log(plural(minhfp,
          "- at least 1 FP must be an HFP.",
          "- at least %d FPs must be HFPs." % minhfp
        ))
      else:
        self._log(plural(maxhfp,
          "- at most 1 FP may be an HFP.",
          "- at most %d FPs may be HFPs." % maxhfp
        ))

      if minvfp == maxvfp:
        self._log(plural(minvfp,
          "- exactly 1 FP must be a VFP.",
          "- exactly %d FPs must be VFPs." % minvfp
        ))
      elif minvfp > 0 and maxvfp < maxfp:
        self._log("- between %d and %d FP must be VFPs." % (minvfp, maxvfp))
      elif minvfp > 0:
        self._log(plural(minvfp,
          "- at least 1 FP must be a VFP.",
          "- at least %d FPs must be VFPs." % minvfp
        ))
      else:
        self._log(plural(maxvfp,
          "- at most 1 FP may be a VFP.",
          "- at most %d FPs may be VFPs." % maxvfp
        ))

    if minhfp > maxhfp:
      raise RuntimeError("flight type not permitted by HFP requirements.")
    if minvfp > maxvfp:
      raise RuntimeError("flight type not permitted by VFP requirements.")
  
    if minunloadedhfp > 0:
      self._log(plural(minunloadedhfp,
        "- at least 1 FP must be an unloaded HFP.",
        "- at least %d FPs must be unloaded HFPs." % minunloadedhfp
      ))

    self._mininitialhfp  = mininitialhfp
    self._minhfp         = minhfp
    self._maxhfp         = maxhfp
    self._minvfp         = minvfp
    self._maxvfp         = maxvfp
    self._minunloadedhfp = minunloadedhfp
    self._maxunloadedhfp = maxunloadedhfp      

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
  reportcarriedmaneuver()
  determineinitialmaxturnrate()
  determineallowedturnrates()
  checkformaneuveringdeparture()
  checkcloseformationlimits()

  determinemaxfp()
  determinefprequirements()
    
  self._log("---")
  self._logaction("start", "", self.position())   

  self._continuenormalflight(actions)

################################################################################

def _endnormalflight(self):

  ########################################

  def reportfp():
    self._log("- used %s and %s." % (
      plural(self._hfp, "1 HFP", "%d HFPs" % self._hfp),
      plural(self._vfp, "1 VFP", "%d VFPs" % self._vfp)
    ))    
    if self._spbrfp > 0:
      self._log("- lost %.1f FPs to speedbrakes." % self._spbrfp)
    self._log("- is carrying %.1f FPs." % self._fpcarry)

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

  def reportmaneuver():

    if self._maxturnrate != None:
      self._log("- turned at %s rate." % self._maxturnrate)

    # See rule 7.6.
    if self._gloccheck > 0 and self._maxturnrate != "ET" and self._maxturnrate != "BT":
      self._log("- GLOC cycle ended.")
      self._gloccheck = 0
      
    if self._maneuvertype != None:
      self._log("- is carrying %s of %s%s." % (
        plural(self._maneuverfp, "1 FP", "%d FPs" % self._maneuverfp),
        self._maneuvertype, self._maneuversense))
    elif self._bank == None:
      self._log("- has wings level.")
    else:
      self._log("- is banked %s." % self._bank)    

  ########################################

  def reportcarry():

    if self._altitudecarry != 0:
      self._log("- is carrying %.2f altitude levels." % self._altitudecarry)
          
  ########################################

  def determinemaxturnrateap():

    """
    Determine the APs from the maximum turn rate used.
    """

    if self._maxturnrate != None:
      self._turnrateap = -self.turndrag(self._maxturnrate)
    else:
      self._turnrateap = 0

    if self._turningsupersonic:
      if self.hasproperty("PSSM"):
        self._turnrateap -= 2.0
      elif not self.hasproperty("GSSM"):
        self._turnrateap -= 1.0

  ########################################

  def determinealtitudeap():

    altitudechange = self._altitude - self._previousaltitude

    if flighttype == "ZC":

      # See rule 8.1.1.
      if previousflighttype == "ZC":
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

        altitudeap = -0.5 * scaltitudechange + -1.0 * zcaltitudechange
        self._scwithzccomponent = (zcaltitudechange != 0)

    elif flighttype == "VC":

      # See rule 8.1.3.
      altitudeap = -2.0 * altitudechange

    elif flighttype == "SD":

      # See rule 8.2.1.
      if previousflighttype == "SD":
        altitudeap = -1.0 * altitudechange
      else:
        altitudeap = -0.5 * altitudechange

    elif flighttype == "UD":

      # See rule 8.2.2.
      if previousflighttype == "UD":
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
      self._log("- close formation breaks down as the aircraft lost %d levels in an SD." % altitudeloss)
      self._breakdowncloseformation()
    elif flighttype == "SC" and self._scwithzccomponent:
      self._log("- close formation breaks down as the aircraft climbed faster than the sustained climb rate.")
      self._breakdowncloseformation()
      
  ########################################

  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype  
  
  self._log("---")
  if not self._maneuveringdeparture:
    reportfp()
    checkfp()
    checkfreedescent()
    reportcarry()
    reportmaneuver()
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

def _isdiving(flighttype):

  """
  Return True if the flight type is SD, UD, or VD. Otherwise return False.
  """

  return flighttype == "SD" or flighttype == "UD" or flighttype == "VD"

################################################################################

def _isclimbing(flighttype):

  """
  Return True if the flight type is ZC, SC, or VC. Otherwise return False.
  """
  
  return flighttype == "ZC" or flighttype == "SC" or flighttype == "VC"

################################################################################

def _extrapreparatoryhfp(altitudeband, speed):

    # See rule 13.1.

    extrapreparatoryfp = { "LO": 0, "ML": 0, "MH": 0, "HI": 1, "VH": 2, "EH": 3, "UH": 4 }[altitudeband]

    if speed >= apspeed.m1speed(altitudeband):
      extrapreparatoryfp += 1.0

    return extrapreparatoryfp
