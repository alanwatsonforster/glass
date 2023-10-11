"""
Normal flight for the aircraft class.
"""

import math
from typing_extensions import LiteralString
from airpower.math import onethird, twothirds, roundtoquarter

import airpower.altitude as apaltitude
import airpower.hex      as aphex
import airpower.speed    as apspeed
import airpower.turnrate as apturnrate
import airpower.variants as apvariants

def _checknormalflight(self):

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

    self._x, self._y = aphex.next(self._x, self._y, self._facing)

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
          raise RuntimeError("attempt to dive levels per VFP while the flight type is SC." % altitudechange)
  
      elif flighttype == "UD":

        # See rule 8.2.2.
        if altitudechange != 1:
          raise RuntimeError("attempt to dive %d levels per unloaded HFP while the flight type is UL." % altitudechange)

      elif flighttype == "VD":

        # See rule 8.2.3.
        if altitudechange != 2 and altitudechange != 3: 
          raise RuntimeError("attempt to dive %d levels per VFP while the flight type is VD." % altitudechange)

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
    self._turnrate = None

  ########################################

  def dodeclareturn(sense, turnrate):

    """
    Declare the start of turn in the specified direction and rate.
    """

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

    self._turnrate = turnrate
    self._bank = sense
    self._turnfp = 0
  
  ########################################

  def doturn(sense, facingchange):

    """
    Turn in the specified sense and amount.
    """

    # See rule 7.1.

    if apvariants.withvariant("implicit turn and bank declarations"): 

      # TODO: correct the bank adjustment for LRR and HRR aircraft.
      # TODO: minimum speed requirements.
      if self.bank != None and self._bank != sense:
        self._turnfp -= 1
        self._bank = sense

      minturnrate = apturnrate.determineturnrate(self._altitudeband, self._speed, self._turnfp, facingchange)
      if minturnrate == None:
        raise RuntimeError("attempt to turn faster than the maximum turn rate.")

      self._turnrate = minturnrate

    else:

      if self._turnrate == None:
        raise RuntimeError("attempt to turn without a declared turn.")
      
      if self._bank != sense:
        raise RuntimeError("attempt to turn against the sense of the declared turn.")

      minturnrate = apturnrate.determineturnrate(self._altitudeband, self._speed, self._turnfp, facingchange)
      if minturnrate == None:
        raise RuntimeError("attempt to turn faster than the maximum turn rate.")

      turnrates = ["EZ", "TT", "HT", "BT", "ET"]
      if turnrates.index(minturnrate) > turnrates.index(self._turnrate):
        raise RuntimeError("attempt to turn faster than the declared turn rate.")

    if self._maxturnrate == None:
      self._maxturnrate = self._turnrate
    else:
      turnrates = ["EZ", "TT", "HT", "BT", "ET"]
      self._maxturnrate = turnrates[max(turnrates.index(self._turnrate), turnrates.index(self._maxturnrate))]
      if apvariants.withvariant("prefer v1 bleed rates"):
        if self.hasproperty("HBR"):
          self._sustainedturnap -= facingchange // 30 * 2.0
        else:
          self._sustainedturnap -= facingchange // 30 * 1.0
      else:
        # Use the proposed bleed rates for 2nd edition from p. 4 of AP 32.
        if self.hasproperty("LBR"):
          self._sustainedturnap -= facingchange // 30 * 0.5
        elif self.hasproperty("HBR"):
          self._sustainedturnap -= facingchange // 30 * 1.5
        else:
          self._sustainedturnap -= facingchange // 30 * 1.0

    self._turnrateap = -self.turndrag(self._maxturnrate)

    # See the "Supersonic Speeds" section of rule 6.6.
    if self._speed >= apspeed.m1speed(self._altitudeband):
      self._turnrateap -= 1

    # Change facing.
    if aphex.isedge(self._x, self._y):
      self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360
  
  ########################################

  def doverticalroll(sense, facingchange, shift):

    if self.hasproperty("NRM"):
      raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if self._verticalrolls == 1 and self.hasproperty("OVR"):
      raise RuntimeError("aircraft can only perform one vertical roll per turn.")
      
    # See rule 13.3.4.  
    if self._flighttype != "VC" and self._flighttype != "VD":
      raise RuntimeError("attempt to roll vertically while flight type is %s." % self._flighttype)
    if not self._vertical:
      raise RuntimeError("attempt to roll vertically during an HFP.")
    if previousflighttype == "LVL" and flighttype == "VC" and not self._lastfp:
      raise RuntimeError("attempt to roll vertically in VC following LVL flight other than on the last FP.")

    # See rule 13.3.5.
    if self._hrd and not self._lastfp:
      raise RuntimeError("attempt to roll vertically after HRD other than on the last FP.")

    # See rule 13.3.4.
    if self.hasproperty("LRR") and facingchange > 90:
      raise RuntimeError("attempt to roll vertically by more than 90 degrees in LRR aircraft.")

    self._maneuverap -= self.rolldrag("VR")

    # See rule 13.3.6
    if self._rollmaneuvers > 0:
      self._maneuverap -= 1
    self._rollmaneuvers += 1
    self._verticalrolls += 1

    # See rule 6.6.
    if self._speed >= apspeed.m1speed(self._altitudeband):
      self._maneuverap -= 1

    # Change facing.
    if aphex.isedge(self._x, self._y) and shift:
      self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

  ########################################

  def doslide(sense):

    # TODO: additional prepfps for altitude and speed.
    if self._prepfp < 2:
      raise RuntimeError("insufficient preparatory HFPs for a slide.")

    # TODO: check number of slides
    # TODO: check HFPs between first and second slides.

    self._x, self._y = aphex.slide(self._x, self._y, self._facing, sense)

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
      raise RuntimeError("only %s FPs are remaining." % maxspbrfp)
    
    maxspbrfp = self.spbr()
    if maxspbrfp == None:
      raise RuntimeError("aircraft does not have speedbrakes.")

    if self._speed > apspeed.m1speed(self._altitudeband):
      maxspbrfp += 0.5
    if spbrfp > maxspbrfp:
      raise RuntimeError("speedbrake capability is only %.1f FPs." % maxspbrfp)

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

    if self._unloaded:
      raise RuntimeError("attempt to attack while unloaded.")
    if self._hrd:
      raise RuntimeError("attempt to attack after HRD.")

    self._logevent("- attack with %s." % weapon)

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
      self._x, self._y = aphex.next(self._x, self._y, self._facing)
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
  
    ["H"   , "H"               , lambda: dohorizontal() ],

    ["C1"  , "C or D"          , lambda: doclimb(1) ],
    ["C2"  , "C or D"          , lambda: doclimb(2) ],
    ["CC"  , "C or D"          , lambda: doclimb(2) ],
    ["C"   , "C or D"          , lambda: doclimb(1) ],

    ["D1"  , "C or D"          , lambda: dodive(1) ],
    ["D2"  , "C or D"          , lambda: dodive(2) ],
    ["D3"  , "C or D"          , lambda: dodive(3) ],
    ["DDD" , "C or D"          , lambda: dodive(3) ],
    ["DD"  , "C or D"          , lambda: dodive(2) ],
    ["D"   , "C or D"          , lambda: dodive(1) ],

    ["LSL"     , "slide", lambda: doslide("L")],
    ["RSL"     , "slide", lambda: doslide("R")],

    ["LVR180S" , "roll", lambda: doverticalroll("L", 180, True )],
    ["LVR180"  , "roll", lambda: doverticalroll("L", 180, False)],
    ["LVR150"  , "roll", lambda: doverticalroll("L", 150, True )],
    ["LVR120"  , "roll", lambda: doverticalroll("L", 120, True )],
    ["LVR90"   , "roll", lambda: doverticalroll("L",  90, True )],
    ["LVR60"   , "roll", lambda: doverticalroll("L",  60, True )],
    ["LVR30"   , "roll", lambda: doverticalroll("L",  30, True )],
    ["LVR"     , "roll", lambda: doverticalroll("L",  30, True )],

    ["RVR180S" , "roll", lambda: doverticalroll("R", 180, True )],
    ["RVR180"  , "roll", lambda: doverticalroll("R", 180, False)],
    ["RVR150"  , "roll", lambda: doverticalroll("R", 150, True )],
    ["RVR120"  , "roll", lambda: doverticalroll("R", 120, True )],
    ["RVR90"   , "roll", lambda: doverticalroll("R",  90, True )],
    ["RVR60"   , "roll", lambda: doverticalroll("R",  60, True )],
    ["RVR30"   , "roll", lambda: doverticalroll("R",  30, True )],
    ["RVR"     , "roll", lambda: doverticalroll("R",  30, True )],
  
    ["LEZ" , "turn declaration or bank", lambda: dodeclareturn("L", "EZ") ],
    ["LTT" , "turn declaration or bank", lambda: dodeclareturn("L", "TT") ],
    ["LHT" , "turn declaration or bank", lambda: dodeclareturn("L", "HT") ],
    ["LBT" , "turn declaration or bank", lambda: dodeclareturn("L", "BT") ],
    ["LET" , "turn declaration or bank", lambda: dodeclareturn("L", "ET") ],
    
    ["REZ" , "turn declaration or bank", lambda: dodeclareturn("R", "EZ") ],
    ["RTT" , "turn declaration or bank", lambda: dodeclareturn("R", "TT") ],
    ["RHT" , "turn declaration or bank", lambda: dodeclareturn("R", "HT") ],
    ["RBT" , "turn declaration or bank", lambda: dodeclareturn("R", "BT") ],
    ["RET" , "turn declaration or bank", lambda: dodeclareturn("R", "ET") ],
    
    ["LB"  , "turn declaration or bank", lambda: dobank("L")  ],
    ["RB"  , "turn declaration or bank", lambda: dobank("R")  ],
    ["WL"  , "turn declaration or bank", lambda: dobank(None) ],

    ["L90" , "turn"    , lambda: doturn("L", 90) ],
    ["L60" , "turn"    , lambda: doturn("L", 60) ],
    ["L30" , "turn"    , lambda: doturn("L", 30) ],
    ["LLL" , "turn"    , lambda: doturn("L", 90) ],
    ["LL"  , "turn"    , lambda: doturn("L", 60) ],
    ["L"   , "turn"    , lambda: doturn("L", 30) ],

    ["R90" , "turn"    , lambda: doturn("R", 90) ],
    ["R60" , "turn"    , lambda: doturn("R", 60) ],
    ["R30" , "turn"    , lambda: doturn("R", 30) ],
    ["RRR" , "turn"    , lambda: doturn("R", 90) ],
    ["RR"  , "turn"    , lambda: doturn("R", 60) ],
    ["R"   , "turn"    , lambda: doturn("R", 30) ],

    ["P"   , "prep"    , lambda: None ],


    ["S1/2", "other"           , lambda: dospeedbrakes(1/2) ],
    ["S1"  , "other"           , lambda: dospeedbrakes(1) ],
    ["S3/2", "other"           , lambda: dospeedbrakes(3/2) ],
    ["S2"  , "other"           , lambda: dospeedbrakes(2) ],
    ["S5/2", "other"           , lambda: dospeedbrakes(5/2) ],
    ["S3"  , "other"           , lambda: dospeedbrakes(3) ],
    ["SSS" , "other"           , lambda: dospeedbrakes(3/2) ],
    ["SS"  , "other"           , lambda: dospeedbrakes(1) ],
    ["S"   , "other"           , lambda: dospeedbrakes(1/2) ],
    
    ["J1/2", "other"           , lambda: dojettison("1/2") ],
    ["JCL" , "other"           , lambda: dojettison("CL") ],
    
    ["AGN" , "other"           , lambda: doattack("guns") ],
    ["AGP" , "other"           , lambda: doattack("gun pod") ],
    ["ARK" , "other"           , lambda: doattack("rockets") ],
    ["ARP" , "other"           , lambda: doattack("rocket pods") ],

    ["K"   , "other"           , lambda: dokilled()],

    ["/"   , "other"           , lambda: None ],

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
      raise RuntimeError("only %.1f FPs are available." % self._maxfp)

    # Determine if this FP is the last FP of the move.
    self._lastfp = (self._fp + 2 > self._maxfp) 
    
    initialaltitude     = self._altitude
    initialaltitudeband = self._altitudeband

    if doelements(action, "maneuvering departure", False):
    
      self._maneuveringdeparture = True

      assert aphex.isvalid(self._x, self._y, facing=self._facing)
      assert apaltitude.isvalidaltitude(self._altitude)
  
      self._logposition("FP %d" % (self._hfp + self._vfp), action)
      self._continueflightpath()
    
      return

    doelements(action, "turn declaration or bank", False)

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

    # See rule 8.2.2.
    if not self._unloaded:
      self._turnfp += 1

    turn  = doelements(action, "turn" , False)
    roll  = doelements(action, "roll" , False)
    slide = doelements(action, "slide", False)
    prep  = doelements(action, "prep" , False)
    if roll and slide:
      raise RuntimeError("an aircraft cannot roll and slide on the same FP.")
    if turn and (roll or slide):
      raise RuntimeError("an aircraft cannot turn and maneuver on the same FP.")
    if prep and (roll or slide):
      raise RuntimeError("an aircraft cannot maneuver and prepare for a maneuver on the same FP.")
    if turn and prep:
      raise RuntimeError("an aircraft cannot turn and prepare for a maneuver on the same FP.")

    # See rule 13.1.
    if prep and not self._horizontal:
      raise RuntimeError("an aircraft can only prepare for a maneuver during an HFP.")
    # See rule 8.2.2.
    if prep and self._unloaded:
      raise RuntimeError("an aircraft may not prepare for a maneuver during an unloaded HFP.")

    if slide and not self._horizontal:
      raise RuntimeError("an aircraft can only slide on a HFP.")

    # See rule 13.1.
    if prep:
      self._prepfp += 1
      self._turnrate = None
      self._turnfp = 0
    elif turn or slide or roll:
      self._prepfp = 0
      self._turnfp = 0
  
    assert aphex.isvalid(self._x, self._y, facing=self._facing)
    assert apaltitude.isvalidaltitude(self._altitude)
  
    self._logposition("FP %d" % (self._hfp + self._vfp), action)
    self._continueflightpath()
    
    # See rules 7.7 and 8.5.
    if roll:
      if initialaltitude > self.ceiling():
        self._logevent("- check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll.")
      elif initialaltitudeband == "EH" or initialaltitudeband == "UH":
        self._logevent("- check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll." % initialaltitudeband)
    
    # See rules 7.7 and 8.5.
    if turn:
      if initialaltitude > self.ceiling() and self._turnrate != "EZ":
        self._logevent("- check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ.")
      if self._turnrate == "ET" and initialaltitude <= 25:
        self._gloccheck += 1
        self._log("- check for GLOC as turn rate is ET and altitude band is %s (check %d in cycle)." % (initialaltitudeband, self._gloccheck))
    
    if initialaltitudeband != self._altitudeband:
      self._logevent("- altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      
    self.checkforterraincollision()
    self.checkforleavingmap()
    if self._destroyed or self._leftmap:
      return

    doelements(action, "other", True)

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
     self._log("- carrying %+.2f APs." % self._apcarry)
 
  ########################################

  def reportaltitudecarry():
    if self._altitudecarry != 0:
     self._log("- carrying %.2f altitude levels." % self._altitudecarry)

  ########################################

  def reportturn():

    if self._turnfp > 0 and self._turnrate != None:
      self._log("- is turning %s at %s rate with %d FPs carried." % (self._bank, self._turnrate, self._turnfp))
    elif self._bank == None:
      self._log("- has wings level.")
    else:
      self._log("- is banked %s." % self._bank)

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

  def checkformaneuveringdeparture():

    """
    Check for a maneuvering departure caused by a carried turn exceeding the 
    maximum allowed turn rate.
    """

    # See rule 7.7.

    # Issue: The consequences of carried turn violating the turn
    # requirements of ZC, SC, and VC flight are not clear, but for the
    # moment we assume they result in a maneuvering departure.

    if self._turnrate != None and not self._turnrate in self._allowedturnrates:
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

  def determinemininitialhfp():

    """
    Determine the requirement, if any, on initial HFPs (e.g., when changing
    from climbing to diving).
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

    if mininitialhfp == 1:
      self._log("- the first FP must be an HFP.")
    elif mininitialhfp > 1:
      self._log("- the first %d FPs must be HFPs." % mininitialhfp)

    self._mininitialhfp = mininitialhfp

  ########################################

  def determinerequiredhfpvfpmix():


    """
    Determine the minimum and maximum number of HFPs, VFPs, and unloaded HFPs.
    """

    maxfp = int(self._maxfp)

    minhfp = 0
    maxhfp = maxfp
    minvfp = 0
    maxvfp = maxfp
    minunloadedhfp = 0
    maxunloadedhfp = 0

    if flighttype == "LVL":

      # See rule 5.3.
      maxvfp = 0
    
    elif flighttype == "ZC":

      # See rules 8.1.1.
      minhfp = math.ceil(onethird(maxfp))

    elif flighttype == "SC":

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

      # See rules 8.1.3 and 8.2.3.
      if previousflighttype != flighttype:
        minhfp = math.floor(onethird(maxfp))
        maxhfp = minhfp
      else:
        maxhfp = math.floor(onethird(maxfp))

    elif flighttype == "SD":

      # See rules 8.2.1 and 8.2.3.
      if previousflighttype == "VD":
        minvfp = math.floor(self._speed / 2)
      minhfp = math.ceil(onethird(maxfp))    

    elif flighttype == "UD":

      # See rules 8.2.2 and 8.2.3.
      maxunloadedhfp = maxfp
      if previousflighttype == "VD":
        minunloadedhfp = math.floor(self._speed / 2)
      else:
        minunloadedhfp = 1

    minhfp = max(minhfp, self._mininitialhfp)

    if minvfp > 0:
      self._log("- at least %d FPs must be VFPs." % minvfp)
    elif maxvfp != 0 and maxvfp < maxfp:
      self._log("- at most %d FPs can be VFPs." % maxvfp)
      
    if maxvfp == 0:
      self._log("- all FPs must be HFPs.")
    elif minhfp == maxhfp:
      self._log("- exactly %d FPs must be HFPs." % minhfp)
    elif minhfp > 0:
      self._log("- at least %d FPs must be HFPs." % minhfp)
    elif maxhfp < maxfp:
      self._log("- at most %d FPs can be HFPs." % maxhfp)

    if minhfp > maxhfp:
      raise RuntimeError("flight type not permitted by HFP requirements.")
    if minvfp > maxvfp:
      raise RuntimeError("flight type not permitted by VFP requirements.")
  
    assert minunloadedhfp == 0 or maxunloadedhfp == maxfp
    if minunloadedhfp > 0:
      self._log("- at least %d FPs must be unloaded HFPs." % minunloadedhfp)
    elif maxunloadedhfp == maxfp:
      self._log("- all FPs may be unloaded HFPs.")    
    
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

  # This keeps track of the number of roll maneuvers and vertical rolls.

  self._rollmaneuvers = 0
  self._verticalrolls = 0
  
  reportapcarry()
  reportaltitudecarry()
  reportturn()
  determineallowedturnrates()
  checkformaneuveringdeparture()

  determinemaxfp()
  determinemininitialhfp()
  determinerequiredhfpvfpmix()
    
  self._log("---")
  self._logposition("start", "")   

  self._continuenormalflight(actions)

################################################################################

def _endnormalflight(self):

  ########################################

  def reportfp():
    self._log("- used %d HFPs and %d VFPs (lost %.1f FPs to speedbrakes)." % (
      self._hfp, self._vfp, self._spbrfp
    ))    

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

  def reportturn():

    if self._maxturnrate != None:
      self._log("- turned at %s rate." % self._maxturnrate)

    # See rule 7.6.
    if self._gloccheck > 0 and self._maxturnrate != "ET" and self._maxturnrate != "BT":
      self._log("- GLOC cycle ended.")
      self._gloccheck = 0
      
    if self._turnfp > 0 and self._turnrate != None:
      self._log("- finished turning %s at %s rate with %d FPs carried." % (self._bank, self._turnrate, self._turnfp))
    elif self._bank == None:
      self._log("- finished with wings level.")
    else:
      self._log("- finished banked %s." % self._bank)    

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

  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype  
  
  self._log("---")
  if not self._maneuveringdeparture:
    reportfp()
    checkfp()
    checkfreedescent()
    reportturn()
    determinealtitudeap()

  self._endmove()

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
