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

def _doattack(self, weapon):

  """
  Declare an attack with the specified weapon.
  """

  if self._unloaded:
    raise RuntimeError("attempt to attack while unloaded.")

  self._logevent("attack with %s." % weapon)

def _doclimb(self, altitudechange):

  """
  Climb.
  """

  def determinealtitudechange(altitudechange):

    assert altitudechange == 1 or altitudechange == 2

    flighttype     = self._flighttype
    lastflighttype = self._lastflighttype  
    
    climbcapability = self.climbcapability()

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

  altitudechange = determinealtitudechange(altitudechange)
    
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)

def _dodive(self, altitudechange):

  """
  Dive.
  """

  def checkaltitudechange():

    assert altitudechange == 1 or altitudechange == 2 or altitudechange == 3

    flighttype     = self._flighttype
    lastflighttype = self._lastflighttype    

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

def _dohorizontal(self):

  """
  Move horizontally.
  """

  self._x, self._y = aphex.next(self._x, self._y, self._facing)

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
    
  maxspbrfp = self.spbr()
  if self._speed > apspeed.m1speed(self._altitudeband):
    maxspbrfp += 0.5
  if spbrfp > maxspbrfp:
    raise RuntimeError("speedbrake capability is only %.1f FPs." % maxspbrfp)

  self._spbrfp = spbrfp

  self._spbrap = -spbrfp / 0.5

def _dobank(self, sense):

  # TODO: LRR

  self._bank = sense
  self._turnrate = None

def _dodeclareturn(self, sense, turnrate):

  """
  Start a turn in the specified direction and rate.
  """

  # TODO: HRR and LRR

  if self._bank != None and self._bank != sense:
    raise RuntimeError("attempt to declare a turn while not banked correctly.")

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

    ["C1"  , "C or D"          , lambda: self._doclimb(1) ],
    ["C2"  , "C or D"          , lambda: self._doclimb(2) ],
    ["CC"  , "C or D"          , lambda: self._doclimb(2) ],
    ["C"   , "C or D"          , lambda: self._doclimb(1) ],

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

  elementdispatchlist = self._getelementdispatchlist()

  initialaltitudeband = self._altitudeband

  self._doelements(action, "turn declaration", False)

  actionhorizontal = (self._doelements(action, "H", False) == 1)
  actionvertical   = (self._doelements(action, "C or D", False) == 1)

  if not actionhorizontal and not actionvertical:
    raise RuntimeError("%r is not a valid action." % action)
  elif actionhorizontal and actionvertical:
    if not self._flighttype == "UD" and not self._flighttype == "LVL":
      raise RuntimeError("%r is not a valid action when the flight type is %s." % (action, self._flighttype))
  
  if actionhorizontal:
    self._hfp += 1
  elif self._hfp < self._mininitialhfp:
    raise RuntimeError("insufficient initial HFPs.")
  else:
   self._vfp += 1

  self._turnfp += 1

  self._unloaded = self._flighttype == "UD" and actionvertical
  if self._unloaded:
    if self._firstunloadedfp == None:
      self._firstunloadedfp = self._hfp
    self._lastunloadedfp = self._hfp

  self._doelements(action, "turn or bank", False)
  
  assert aphex.isvalid(self._x, self._y, facing=self._facing)
  assert apaltitude.isvalidaltitude(self._altitude)
  
  self._logposition("FP %d" % (self._hfp + self._vfp), action)
  self._continueflightpath()

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

################################################################################

def _startnormalflight(self, actions):
      
  """
  Start to carry out normal flight.
  """

  def reportapcarry():
     self._log("- carrying %+.2f APs." % self._apcarry)
 
  def reportaltitudecarry():
    if self._altitudecarry != 0:
     self._log("- carrying %.2f altitude levels." % self._altitudecarry)

  def reportturn():

    if self._turnfp > 0 and self._turnrate != None:
      self._log("- is turning %s at %s rate with %d FPs carried." % (self._bank, self._turnrate, self._turnfp))
    elif self._bank == None:
      self._log("- has wings level.")
    else:
      self._log("- is banked %s." % self._bank)

  def determineallowedturnrates():

    """
    Determine the allowed turn rates according to the flight type. The
    aircraft type and configuration may impose additional restrictions.
    """

    turnrates = ["EZ", "TT", "HT", "BT", "ET"]

    # See rule 7.5 "Turning and Minimum Speeds"

    minspeed = self.minspeed()
    if self._speed == minspeed + 1.5:
      self._log("- speed is limiting the turn rate to BT.")
      turnrates = turnrates[:4]
    elif self._speed == minspeed + 1.0:
      self._log("- speed is limiting the turn rate to HT.")
      turnrates = turnrates[:3]
    elif self._speed == minspeed + 0.5:
      self._log("- speed is limiting the turn rate to TT.")
      turnrates = turnrates[:2]
    elif self._speed == minspeed:
      self._log("- speed is limiting the turn rate to EZ.")
      turnrates = turnrates[:1]

    # See the "ZC Restrictions" section of rule 8.1.1.

    if self._flighttype == "ZC":
      self._log("- ZC is limiting the turn rate to BT.")
      turnrates = turnrates[:4]

    # See the "SC Restrictions" section of rule 8.1.1.

    if self._flighttype == "SC":
      self._log("- SC is limiting the turn rate to EZ.")
      turnrates = turnrates[:1]

    # See the "VC Restrictions" section of rule 8.1.3.

    if self._flighttype == "VC":
      self._log("- VC disallows all turns.")
      turnrates = []

    self._allowedturnrates = turnrates

  def checkformaneuveringdeparture():

    # See rule 7.7 "Maneuvering Departures"

    # Issue: The consequences of carried turn violating the turn requirements of 
    # ZC, SC, and VC flight are not clear, but for the moment we assume they 
    # result in a maneuvering departure.

    if self._turnrate != None and not self._turnrate in self._allowedturnrates:
      self._log("- carried turn rate is tighter than the maximum allowed turn rate.")
      raise RuntimeError("aircraft has entered departured flight while maneuvering.")

  def determinefp():

    # See rule 5.4.

    self._fp      = self._speed + self._fpcarry
    self._log("- has %.1f FPs (including %.1f carry)." % (self._fp, self._fpcarry))
    self._fpcarry = 0

    self._hfp     = 0
    self._vfp     = 0
    self._spbrfp  = 0 

    self._firstunloadedfp = None
    self._lastunloadedfp  = None

  def determinemininitialhfp():

    # See rule 5.5.

    flighttype     = self._flighttype
    lastflighttype = self._lastflighttype

    if lastflighttype == "LVL" and (_isclimbing(flighttype) or _isdiving(flighttype)):
      mininitialhfp = 1
    elif (_isclimbing(lastflighttype) and _isdiving(flighttype)) or (_isdiving(lastflighttype) and _isclimbing(flighttype)):
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

  def determinerequiredhfpvfpmix():

    flighttype     = self._flighttype
    lastflighttype = self._lastflighttype
    fp             = int(self._fp)

    minhfp = 0
    maxhfp = fp
    minvfp = 0
    maxvfp = fp
    minunloadedhfp = 0
    maxunloadedhfp = 0

    if flighttype == "LVL":

      # See rule 5.3.
      maxvfp = 0
    
    elif flighttype == "ZC":

      # See rules 8.1.1.
      minhfp = math.ceil(onethird(fp))

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
        maxvfp = math.floor(twothirds(fp))

    elif flighttype == "VC" or flighttype == "VD":

      # See rules 8.1.3 and 8.2.3.
      if lastflighttype != flighttype:
        minhfp = math.floor(onethird(fp))
        maxhfp = minhfp
      else:
        maxhfp = math.floor(onethird(fp))

    elif flighttype == "SD":

      # See rules 8.2.1 and 8.2.3.
      if lastflighttype == "VD":
        minvfp = math.floor(self._speed / 2)
      minhfp = math.ceil(onethird(fp))    

    elif flighttype == "UD":

      # See rules 8.2.2 and 8.2.3.
      maxunloadedhfp = fp
      if lastflighttype == "VD":
        minunloadedhfp = math.floor(self._speed / 2)
      else:
        minunloadedhfp = 0

    if maxvfp == 0:
      self._log("- all FPs must be HFPs.")
    elif minhfp == maxhfp:
      self._log("- exactly %d FPs must be HFPs." % minhfp)
    elif minhfp > 0:
      self._log("- at least %d FPs must be HFPs." % minhfp)
    elif maxhfp < fp:
      self._log("- at most %d FPs can be HFPs." % maxhfp)

    if minvfp > 0:
      self._log("- at least %d FPs must be VFPs." % maxvfp)
    elif maxvfp != 0 and maxvfp < fp:
      self._log("- at most %d FPs can be VFPs." % maxvfp)

    assert minunloadedhfp == 0 or maxunloadedhfp == fp
    if minunloadedhfp > 0:
      self._log("- at least %d FPs must be unloaded HFPs." % minunloadedhfp)
    elif maxunloadedhfp == fp:
      self._log("- all FPs may be unloaded HFPs.")    
    
    self._minhfp = minhfp
    self._maxhfp = maxhfp
    self._minvfp = minvfp
    self._maxvfp = maxvfp
    self._minunloadedhfp = minunloadedhfp
    self._maxunloadedhfp = maxunloadedhfp

  reportapcarry()
  reportaltitudecarry()
  reportturn()
  determineallowedturnrates()
  checkformaneuveringdeparture()

  determinefp()
  determinemininitialhfp()
  determinerequiredhfpvfpmix()
      
  self._log("---")
  self._logposition("start", "")   

  self._continuenormalflight(actions)

################################################################################

def _endnormalflight(self):

  def reportfp():
    self._log("- used %d HFPs and %d VFPs (lost %.1f FPs to speedbrakes)." % (
      self._hfp, self._vfp, self._spbrfp
    ))    

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
      unloadedhfp = self._lastaltitude - self._altitude
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

  def checkfreedescent():

    # See rule 8.2.4.
    
    if self._flighttype == "LVL":
      altitudechange = self._altitude - self._lastaltitude
      if altitudechange < -1:
        raise RuntimeError("free descent cannot only be taken once per move.")
  
  def reportturn():

    if self._maxturnrate != None:
      self._log("- turned at %s rate." % self._maxturnrate)

    if self._turnfp > 0 and self._turnrate != None:
      self._log("- finished turning %s at %s rate with %d FPs carried." % (self._bank, self._turnrate, self._turnfp))
    elif self._bank == None:
      self._log("- finished with wings level.")
    else:
      self._log("- finished banked %s." % self._bank)    

  self._log("---")

  def determinealtitudeap():

    altitudechange = self._altitude - self._lastaltitude

    if flighttype == "ZC":

      # See rule 8.1.1.
      if lastflighttype == "ZC":
        altitudeap = -1.5 * altitudechange
      else:
        altitudeap = -1.0 * altitudechange

    elif flighttype == "SC":

      if altitudechange == 0:

        altitudeap = 0.0

      else:

        # See rule 8.1.2 and 8.1.4.

        climbcapability = self.climbcapability()
        if self._speed < self.climbspeed():
          climbcapability /= 2

        # We need to figure out how much was climbed at the SC rate and
        # how much was climbed at the ZC rate. This is complicated since
        # altitudechange can be more than the climbcapability because of
        # altitudecarry. Therefore, we calculate how much was at the ZC
        # rate from the true altitude change, including carry, and then
        # assume that any difference was at the SC rate.
        # 
        # We also use that the altitude change at the ZC rate must be an
        # integral number of levels.

        truealtitude     = self._altitude     + self._altitudecarry
        lasttruealtitude = self._lastaltitude + self._lastaltitudecarry

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
      if lastflighttype == "SD":
        altitudeap = -1.0 * altitudechange
      else:
        altitudeap = -0.5 * altitudechange

    elif flighttype == "UD":

      # See rule 8.2.2.
      if lastflighttype == "UD":
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

  flighttype     = self._flighttype
  lastflighttype = self._lastflighttype

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

def _isclimbing(flighttype):

  """
  Return True if the flight type is ZC, SC, or VC. Otherwise return False.
  """
  
  return flighttype == "ZC" or flighttype == "SC" or flighttype == "VC"

################################################################################
