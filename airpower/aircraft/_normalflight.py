"""
Normal flight for the aircraft class.
"""

import math
from airpower.math import onethird, twothirds

import airpower.altitude as apaltitude
import airpower.hex      as aphex
import airpower.speed    as apspeed
import airpower.turnrate as apturnrate
import airpower.variants as apvariants

def _doattack(self, weapon):

  """
  Declare an attack with the specified weapon.
  """

  self._logevent("attack with %s." % weapon)

def _doclimb(self, altitudechange):

  """
  Climb.
  """

  # See the "Climbs or Dives Only" section of chapter 8 "Changing Aircraft 
  # Altitude".

  if not self._flighttype in ["ZC", "SC", "VC"]:
    raise RuntimeError("attempt to climb while flight type is %s." % self._flighttype)

  initialaltitude = self._altitude    
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)
  self._altitudeband  = apaltitude.altitudeband(self._altitude)
  altitudechange = self._altitude - initialaltitude

  if self._flighttype == "ZC":
    if self._lastflighttype == "ZC":
      self._altitudeap -= 1.5 * altitudechange
    else:
      self._altitudeap -= 1.0 * altitudechange
  elif self._flighttype == "SC":
    # TODO: deceleration for climb in excess of CC
    self._altitudeap -= 0.5 * altitudechange
  elif self._flighttype == "VC":
    self._altitudeap -= 2.0 * altitudechange

def _dodive(self, altitudechange):

  """
  Dive.
  """

  # See the "Climbs or Dives Only" section of chapter 8 "Changing Aircraft 
  # Altitude" and rule 8.2.4 "Free Descent".
  
  if not self._flighttype in ["LVL", "SD", "UD", "VD"]:
    raise RuntimeError("attempt to dive while flight type is %s." % self._flighttype)

  initialaltitude = self._altitude    
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)
  altitudechange = initialaltitude - self._altitude

  if self._flighttype == "LVL":
    pass
  elif self._flighttype == "SD":
    if self._lastflighttype == "SD":
      self._altitudeap += 1.0 * altitudechange
    else:
      self._altitudeap += 0.5 * altitudechange
  elif self._flighttype == "UD":
    if self._lastflighttype == "UD":
      self._altitudeap += 1.0 * altitudechange
    else:
      self._altitudeap += 0.5 * altitudechange
  elif self._flighttype == "VD":
    self._altitudeap += 1.0 * altitudechange

def _dohorizontal(self):

  """
  Move horizontally.
  """

  self._x, self._y = aphex.nextposition(self._x, self._y, self._facing)

def _dojettison(self, configuration):

  """
  Jetison stores to achieve the specified configuration.
  """

  # See rule 4.4. 
  
  # We implement the delay of 1 FP by making this an epilog element.

  if self._configuration == configuration:
    raise RuntimeError("configuration is already %s." % configuration)
  if self._configuration == "CL" or configuration == "DT":
    raise RuntimeError("attempt to change from configuration %s to %s." % (self._configuration, configuration))
  self._logevent("jettisoned stores.")
  self._logevent("configuration changed from %s to %s." % (self._configuration, configuration))
  self._configuration = configuration

def _dokilled(self):

  """
  Declare that the aircraft has been killed.
  """

  self._logevent("aircraft has been killed.")
  self._destroyed = True

def _dospeedbrakes(self, spbrfp):

  """
  Use the speedbrakes.
  """

  # See rule 6.5 and the "Supersonic Speeds" section of rule 6.6.

  if self._spbrfp != 0:
    raise RuntimeError("speedbrakes can only be used once per turn.")

  maxspbrfp = self._fp - self._hfp - self._vfp
  if spbrfp > maxspbrfp:
    raise RuntimeError("only %s FPs are remaining." % maxspbrfp)
    
  maxspbrfp = self._aircrafttype.SPBR(self._configuration)
  if self._speed > apspeed.m1speed(self._altitudeband):
    maxspbrfp += 0.5
  if spbrfp > maxspbrfp:
    raise RuntimeError("speedbrake capability is only %.1f FPs." % maxspbrfp)

  self._spbrfp = spbrfp

  self._spbrap = -spbrfp / 0.5

def _dobank(self, sense):

  # TODO: make sure we can't change bank on the same FP as we turn.
  # TODO: LRR

  self._bank = sense
  self._turnrate = None

def _dodeclareturn(self, sense, turnrate):

  """
  Start a turn in the specified direction and rate.
  """

  # TODO: Minimum speed requirements.
  # TODO: HRR and LRR

  if self._bank != None and self._bank != sense:
    raise RuntimeError("attempt to declare a turn while not banked correctly.")

  turnrates = ["EZ", "TT", "HT", "BT", "ET"]
  assert turnrate in turnrates

  if turnrate not in self._allowedturnrates:
    raise RuntimeError("attempt to declare a turn rate tighter than the maximum allowed.")

  self._turnrate = turnrate
  self._bank = sense
  self._turnfp = 0

def _doturn(self, sense, facingchange):

  """
  Turn.
  """

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
    # TODO: drag for HBR and LBR aircraft.
    self._sustainedturnap -= facingchange // 30

  if self._maxturnrate == "EZ":
    self._turnrateap = 0.0
  else:
    self._turnrateap = -self._aircrafttype.turndrag(self._configuration, self._maxturnrate)

  # See the "Supersonic Speeds" section of rule 6.6.
  if self._speed >= apspeed.m1speed(self._altitudeband):
    self._turnrateap += 1

  # Change facing.
  if sense == "L":
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
    self._facing = (self._facing + facingchange) % 360
  else:
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
    self._facing = (self._facing - facingchange) % 360

  self._turnfp = 0
    
def _getelementdispatchlist(self):

  return [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

    # [0] is the element code.
    # [1] is the element type.
    # [2] is the element procedure.
    
    ["LEZ" , "turn declaration", lambda: self._dodeclareturn("L", "EZ") ],
    ["LTT" , "turn declaration", lambda: self._dodeclareturn("L", "TT") ],
    ["LHT" , "turn declaration", lambda: self._dodeclareturn("L", "HT") ],
    ["LBT" , "turn declaration", lambda: self._dodeclareturn("L", "BT") ],
    ["LET" , "turn declaration", lambda: self._dodeclareturn("L", "ET") ],
    
    ["REZ" , "turn declaration", lambda: self._dodeclareturn("R", "EZ") ],
    ["RTT" , "turn declaration", lambda: self._dodeclareturn("R", "TT") ],
    ["RHT" , "turn declaration", lambda: self._dodeclareturn("R", "HT") ],
    ["RBT" , "turn declaration", lambda: self._dodeclareturn("R", "BT") ],
    ["RET" , "turn declaration", lambda: self._dodeclareturn("R", "ET") ],
    
    ["H"   , "H"               , lambda: self._dohorizontal() ],

    ["C1/8", "C or D"          , lambda: self._doclimb(1/8) ],
    ["C1/4", "C or D"          , lambda: self._doclimb(1/4) ],
    ["C3/8", "C or D"          , lambda: self._doclimb(3/8) ],
    ["C1/2", "C or D"          , lambda: self._doclimb(1/2) ],
    ["C5/8", "C or D"          , lambda: self._doclimb(5/8) ],
    ["C3/4", "C or D"          , lambda: self._doclimb(3/4) ],
    ["C7/8", "C or D"          , lambda: self._doclimb(7/8) ],
    ["C1"  , "C or D"          , lambda: self._doclimb(1) ],
    ["C2"  , "C or D"          , lambda: self._doclimb(2) ],
    ["CC"  , "C or D"          , lambda: self._doclimb(2) ],
    ["C"   , "C or D"          , lambda: self._doclimb(1) ],

    ["D1/8", "C or D"          , lambda: self._dodive(1/8) ],
    ["D1/4", "C or D"          , lambda: self._dodive(1/4) ],
    ["D3/8", "C or D"          , lambda: self._dodive(3/8) ],
    ["D1/2", "C or D"          , lambda: self._dodive(1/2) ],
    ["D5/8", "C or D"          , lambda: self._dodive(5/8) ],
    ["D3/4", "C or D"          , lambda: self._dodive(3/4) ],
    ["D7/8", "C or D"          , lambda: self._dodive(7/8) ],
    ["D1"  , "C or D"          , lambda: self._dodive(1) ],
    ["D2"  , "C or D"          , lambda: self._dodive(2) ],
    ["D3"  , "C or D"          , lambda: self._dodive(3) ],
    ["DDD" , "C or D"          , lambda: self._dodive(3) ],
    ["DD"  , "C or D"          , lambda: self._dodive(2) ],
    ["D"   , "C or D"          , lambda: self._dodive(1) ],

    ["LB"  , "turn or bank"    , lambda: self._dobank("L") ],
    ["RB"  , "turn or bank"    , lambda: self._dobank("R") ],
    ["WL"  , "turn or bank"    , lambda: self._dobank(None) ],

    ["L90" , "turn or bank"    , lambda: self._doturn("L", 90) ],
    ["L60" , "turn or bank"    , lambda: self._doturn("L", 60) ],
    ["L30" , "turn or bank"    , lambda: self._doturn("L", 30) ],
    ["LLL" , "turn or bank"    , lambda: self._doturn("L", 90) ],
    ["LL"  , "turn or bank"    , lambda: self._doturn("L", 60) ],
    ["L"   , "turn or bank"    , lambda: self._doturn("L", 30) ],

    ["R90" , "turn or bank"    , lambda: self._doturn("R", 90) ],
    ["R60" , "turn or bank"    , lambda: self._doturn("R", 60) ],
    ["R30" , "turn or bank"    , lambda: self._doturn("R", 30) ],
    ["RRR" , "turn or bank"    , lambda: self._doturn("R", 90) ],
    ["RR"  , "turn or bank"    , lambda: self._doturn("R", 60) ],
    ["R"   , "turn or bank"    , lambda: self._doturn("R", 30) ],

    ["S1/2", "other"           , lambda: self._dospeedbrakes(1/2) ],
    ["S1"  , "other"           , lambda: self._dospeedbrakes(1) ],
    ["S3/2", "other"           , lambda: self._dospeedbrakes(3/2) ],
    ["S2"  , "other"           , lambda: self._dospeedbrakes(2) ],
    ["S5/2", "other"           , lambda: self._dospeedbrakes(5/2) ],
    ["S3"  , "other"           , lambda: self._dospeedbrakes(3) ],
    ["SSS" , "other"           , lambda: self._dospeedbrakes(3/2) ],
    ["SS"  , "other"           , lambda: self._dospeedbrakes(1) ],
    ["S"   , "other"           , lambda: self._dospeedbrakes(1/2) ],
    
    ["J1/2", "other"           , lambda: self._dojettison("1/2") ],
    ["JCL" , "other"           , lambda: self._dojettison("CL") ],
    
    ["AGN" , "other"           , lambda: self._doattack("guns") ],
    ["AGP" , "other"           , lambda: self._doattack("gun pod") ],
    ["ARK" , "other"           , lambda: self._doattack("rockets") ],
    ["ARP" , "other"           , lambda: self._doattack("rocket pods") ],
    ["K"   , "other"           , lambda: self._dokilled()],

    ["/"   , "other"           , lambda: None ],
  ]

def _doelements(self, action, selectedelementtype, allowrepeated):

  ielement = 0

  while action != "":
    for element in self._getelementdispatchlist():

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
    raise RuntimeError("invalid action %r: repeated %s element." % (action, selectedelementtype))

  return ielement

def _doaction(self, action):

  """
  Carry out an action for normal flight.
  """

  if self._hfp + self._vfp + self._spbrfp + 1 > self._fp:
    raise RuntimeError("only %.1f FPs are available." % self._fp)

  lastx = self._x
  lasty = self._y

  elementdispatchlist = self._getelementdispatchlist()

  initialaltitudeband = self._altitudeband

  self._doelements(action, "turn declaration", False)

  actionhorizontal = (self._doelements(action, "H", False) == 1)
  actionvertical   = (self._doelements(action, "C or D", False) == 1)

  if actionhorizontal:
    self._hfp += 1
  elif not actionvertical:
    raise RuntimeError("invalid action %r." % action)
  elif self._hfp < self._requiredinitialhfp:
    raise RuntimeError("insufficient initial HFPs.")
  else:
   self._vfp += 1

  self._turnfp += 1

  self._doelements(action, "turn or bank", False)
  
  assert aphex.isvalidposition(self._x, self._y)
  assert aphex.isvalidfacing(self._x, self._y, self._facing)
  assert apaltitude.isvalidaltitude(self._altitude)
  
  self._logposition("FP %d" % (self._hfp + self._vfp), action)
  self._drawflightpath(lastx, lasty)

  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      
  self.checkforterraincollision()
  self.checkforleavingmap()
  if self._destroyed or self._leftmap:
    return

  self._doelements(action, "other", True)

################################################################################

def _continuenormalflight(self, actions):

  """
  Continue to carry out out normal flight.
  """

  if actions != "":
    for action in actions.split(","):
      if not self._destroyed and not self._leftmap:
        self._doaction(action)

  fp = self._hfp + self._vfp + self._spbrfp
  assert fp <= self._fp

  if self._destroyed or self._leftmap:
  
    self._log("---")
    self._endmove()

  elif fp + 1 > self._fp:

    # See rule 5.4.
    self._fpcarry = self._fp - fp

    self._endnormalflight()
    
  else:
    
    self._drawaircraft("next")

################################################################################

def _startnormalflight(self, actions):
      
  """
  Start to carry out normal flight.
  """
  
  if self._turnfp > 0 and self._turnrate != None:
    self._log("- is turning %s at %s rate with %d FPs carried." % (self._bank, self._turnrate, self._turnfp))
  elif self._bank == None:
    self._log("- has wings level.")
  else:
    self._log("- is banked %s." % self._bank)

  # See rule 7.5 "Turning and Minimum Speeds"

  turnrates = self._aircrafttype.turnrates(self._configuration)
  minspeed = self._aircrafttype.minspeed(self._configuration, self._altitudeband)
  if self._speed == minspeed + 1.5 and "ET" in turnrates:
    turnrates = turnrates[:4]
  elif self._speed == minspeed + 1.0 and "BT" in turnrates:
    turnrates = turnrates[:3]
  elif self._speed == minspeed + 0.5 and "HT" in turnrates:
    turnrates = turnrates[:2]
  elif self._speed == minspeed and "TT" in turnrates:
     turnrates = turnrates[:1]
  self._log("- maximum allowed turn rate is %s." % turnrates[-1])
  self._allowedturnrates = turnrates

  if self._turnrate != None and not self._turnrate in self._allowedturnrates:
    self._log("- carried turn rate is tighter than the maximum allowed turn rate.")
    raise RuntimeError("aircraft has entered departured flight while maneuvering.")
         
  # See rule 5.5.

  flighttype     = self._flighttype
  lastflighttype = self._lastflighttype
  
  if lastflighttype == "LVL" and (_isclimbing(flighttype) or _isdiving(flighttype)):
    requiredinitialhfp = 1
  elif (_isclimbing(lastflighttype) and _isdiving(flighttype)) or (_isdiving(lastflighttype) and _isclimbing(flighttype)):
    if self._aircrafttype.hasproperty("HPR"):
      requiredinitialhfp = self._speed // 3
    else:
      requiredinitialhfp = self._speed // 2
  else:
    requiredinitialhfp = 0
  if requiredinitialhfp == 1:
    self._log("- last flight type was %s so the first FP must be an HFP." % lastflighttype)
  elif requiredinitialhfp > 1:
    self._log("- last flight type was %s so the first %d FPs must be HFPs." % (lastflighttype, requiredinitialhfp))
  self._requiredinitialhfp = requiredinitialhfp

  # See rule 5.4.

  self._fp      = self._speed + self._fpcarry
  self._fpcarry = 0
  self._log("- has %.1f FPs (including %.1f carry)." % (self._fp, self._fpcarry))

  # See rules 8.1 and 8.2.

  if self._flighttype == "ZC":
    # See rule 8.1.1
    self._log("- must use at least %d HFPs." % math.ceil(onethird(self._fp)))
  elif self._flighttype == "SC":
    # See rule 8.1.2
    climbcapability = self._aircrafttype.climbcapability(self._configuration, self._altitudeband, self._powersetting)
    if climbcapability < 1:
      self._log("- must use no more than 1 VFP.")
    else:
      self._log("- must use no more than %d VFPs." % math.floor(twothirds(self._fp)))

  self._hfp     = 0
  self._vfp     = 0
  self._spbrfp  = 0 
      
  self._log("---")
  self._logposition("start", "")   

  self._continuenormalflight(actions)

################################################################################

def _endnormalflight(self):

  self._log("---")

  self._log("- used %d HFPs and %d VFPs, lost %.1f FPs to speedbrakes, and is carrying %.1f FPs." % (
    self._hfp, self._vfp, self._spbrfp, self._fpcarry
  ))

  # See rules 8.1 and 8.2.

  if self._flighttype == "ZC":
    # See rule 8.1.1
    if self._hfp < onethird(self._fp):
      raise RuntimeError("must use at least 1/3 of FPs as HFPs.")
  elif self._flighttype == "SC":
    # See rule 8.1.2
    climbcapability = self._aircrafttype.climbcapability(self._configuration, self._altitudeband, self._powersetting)
    if climbcapability < 1:
      if self._vfp > 1:
        raise RuntimeError("must use no more than 1 VFP.")
    else:
      if self._vfp > twothirds(self._fp):
        self._log("must use no more than 2/3 of FPs as VFPs")

  if self._maxturnrate != None:
      self._log("- turned at %s rate." % self._maxturnrate)

  if self._turnfp > 0 and self._turnrate != None:
    self._log("- finished turning %s at %s rate with %d FPs carried." % (self._bank, self._turnrate, self._turnfp))
  elif self._bank == None:
    self._log("- finished with wings level.")
  else:
    self._log("- finished banked %s." % self._bank)

  self._endmove()

################################################################################

def _isdiving(flighttype):

  """
  Return True if the flight type is SD, UD, or VD. Otherwise return False.
  """

  return flighttype == "SD" or flighttype == "UD" or flighttype == "VD"

def _isclimbing(flighttype):

  """
  Return True if the flight type is ZC, SC, or VC. Otherwise return False.
  """
  
  return flighttype == "ZC" or flighttype == "SC" or flighttype == "VC"

################################################################################
