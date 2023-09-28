"""
Normal flight for the aircraft class.
"""

import math

import airpower.altitude as apaltitude
import airpower.data     as apdata
import airpower.hex      as aphex
import airpower.speed    as apspeed

def _doattack(self, weapon):

  """
  Declare an attack with the specified weapon.
  """

  self._logevent("attack with %s." % weapon)

def _doclimb(self, altitudechange):

  """
  Climb.
  """

  if not self._flighttype in ["ZC", "SC", "VC"]:
    raise ValueError("attempt to climb while flight type is %s." % self._flighttype)

  self._climb += 1

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

  if not self._flighttype in ["LVL", "SD", "UD", "VD"]:
    raise ValueError("attempt to dive while flight type is %s." % self._flighttype)

  self._dive += 1

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

  self._horizontal += 1

  self._x, self._y = aphex.nextposition(self._x, self._y, self._facing)

def _dojettison(self, configuration):

  """
  Jetison stores to achieve the specified configuration.
  """

  # See rule 4.4. 
  
  # We implement the delay of 1 FP by making this an epilog element.

  if self._configuration == configuration:
    raise ValueError("configuration is already %s." % configuration)
  if self._configuration == "CL" or configuration == "DT":
    raise ValueError("attempt to change from configuration %s to %s." % (self._configuration, configuration))
  self._logevent("jettisoned stores.")
  self._logevent("configuration changed from %s to %s." % (self._configuration, configuration))
  self._configuration = configuration

def _dokill(self):

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
    raise ValueError("speedbrakes can only be used once per turn.")

  maxspbrfp = self._fp - self._hfp - self._vfp
  if spbrfp > maxspbrfp:
    raise ValueError("only %s FPs are remaining." % maxspbrfp)
    
  maxspbrfp = self._aircrafttype.SPBR(self._configuration)
  if self._speed > apspeed.m1speed(self._altitudeband):
    maxspbrfp += 0.5
  if spbrfp > maxspbrfp:
    raise ValueError("speedbrake capability is only %.1f FPs." % maxspbrfp)

  self._spbrfp = spbrfp

  self._speedbrakesap = -spbrfp / 0.5

def _dodeclareturn(self, bank, turnrate):

  """
  Start a turn in the specified direction and rate.
  """
  
  turnrates = ["EZ", "TT", "HT", "BT", "ET"]
  assert turnrate in turnrates
  self._bank = bank
  self._turnrate = turnrate

def _doturn(self, sense, facingchange):

  """
  Turn left.
  """

  self._turn += 1

  # TODO: correct the bak adjustment for LBR and HBR aircraft.
  if self._bank != sense:
    self._turnfp -= 1

  minturnrate = apdata.determineturnrate(self._altitudeband, self._speed, self._turnfp, facingchange)
  if minturnrate == None:
    raise ValueError("attempt to turn faster than the maximum turn rate.")

  self._turnfp = 0
  self._bank = sense

  # Implicitly declare turn rates.
  self._turnrate = minturnrate

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
    
def _getelementdispatchlist(self):

  return [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

    # [0] is the element code.
    # [1] is the procedure for prolog elements.
    # [2] is the procedure for movement elements.
    # [3] is the procedure for the epilog elements.

    ["/"   , None                                   , None                            , None],

    ["H"   , None                                   , lambda : self._dohorizontal()   , None],

    ["C1/8", None                                   , lambda : self._doclimb(1/8)     , None],
    ["C1/4", None                                   , lambda : self._doclimb(1/4)     , None],
    ["C3/8", None                                   , lambda : self._doclimb(3/8)     , None],
    ["C1/2", None                                   , lambda : self._doclimb(1/2)     , None],
    ["C5/8", None                                   , lambda : self._doclimb(5/8)     , None],
    ["C3/4", None                                   , lambda : self._doclimb(3/4)     , None],
    ["C7/8", None                                   , lambda : self._doclimb(7/8)     , None],
    ["C1"  , None                                   , lambda : self._doclimb(1)       , None],
    ["C2"  , None                                   , lambda : self._doclimb(2)       , None],
    ["CC"  , None                                   , lambda : self._doclimb(2)       , None],
    ["C"   , None                                   , lambda : self._doclimb(1)       , None],

    ["D1/8", None                                   , lambda : self._dodive(1/8)      , None],
    ["D1/4", None                                   , lambda : self._dodive(1/4)      , None],
    ["D3/8", None                                   , lambda : self._dodive(3/8)      , None],
    ["D1/2", None                                   , lambda : self._dodive(1/2)      , None],
    ["D5/8", None                                   , lambda : self._dodive(5/8)      , None],
    ["D3/4", None                                   , lambda : self._dodive(3/4)      , None],
    ["D7/8", None                                   , lambda : self._dodive(7/8)      , None],
    ["D1"  , None                                   , lambda : self._dodive(1)        , None],
    ["D2"  , None                                   , lambda : self._dodive(2)        , None],
    ["D3"  , None                                   , lambda : self._dodive(3)        , None],
    ["DDD" , None                                   , lambda : self._dodive(3)        , None],
    ["DD"  , None                                   , lambda : self._dodive(2)        , None],
    ["D"   , None                                   , lambda : self._dodive(1)        , None],

    ["LEZ" , lambda : self._dodeclareturn("L", "EZ"), None                            , None],
    ["LTT" , lambda : self._dodeclareturn("L", "TT"), None                            , None],
    ["LHT" , lambda : self._dodeclareturn("L", "HT"), None                            , None],
    ["LBT" , lambda : self._dodeclareturn("L", "BT"), None                            , None],
    ["LET" , lambda : self._dodeclareturn("L", "ET"), None                            , None],
    
    ["REZ" , lambda : self._dodeclareturn("R", "EZ"), None                            , None],
    ["RTT" , lambda : self._dodeclareturn("R", "TT"), None                            , None],
    ["RHT" , lambda : self._dodeclareturn("R", "HT"), None                            , None],
    ["RBT" , lambda : self._dodeclareturn("R", "BT"), None                            , None],
    ["RET" , lambda : self._dodeclareturn("R", "ET"), None                            , None],

    ["L90" , None                                   , lambda : self._doturn("L", 90)  , None],
    ["L60" , None                                   , lambda : self._doturn("L", 60)  , None],
    ["L30" , None                                   , lambda : self._doturn("L", 30)  , None],
    ["LLL" , None                                   , lambda : self._doturn("L", 90)  , None],
    ["LL"  , None                                   , lambda : self._doturn("L", 60)  , None],
    ["L"   , None                                   , lambda : self._doturn("L", 30)  , None],

    ["R90" , None                                   , lambda : self._doturn("R", 90)  , None],
    ["R60" , None                                   , lambda : self._doturn("R", 60)  , None],
    ["R30" , None                                   , lambda : self._doturn("R", 30)  , None],
    ["RRR" , None                                   , lambda : self._doturn("R", 90)  , None],
    ["RR"  , None                                   , lambda : self._doturn("R", 60)  , None],
    ["R"   , None                                   , lambda : self._doturn("R", 30)  , None],

    ["S1/2", None                                   , lambda: self._dospeedbrakes(1/2), None],
    ["S1"  , None                                   , lambda: self._dospeedbrakes(1)  , None],
    ["S3/2", None                                   , lambda: self._dospeedbrakes(3/2), None],
    ["S2"  , None                                   , lambda: self._dospeedbrakes(2)  , None],
    ["SSSS", None                                   , lambda: self._dospeedbrakes(2)  , None],
    ["SSS" , None                                   , lambda: self._dospeedbrakes(3/2), None],
    ["SS"  , None                                   , lambda: self._dospeedbrakes(1)  , None],
    ["S"   , None                                   , lambda: self._dospeedbrakes(1/2), None],
    
    ["AGN" , None                                   , None                            , lambda: self._doattack("guns")],
    ["AGP" , None                                   , None                            , lambda: self._doattack("gun pod")],
    ["ARK" , None                                   , None                            , lambda: self._doattack("rockets")],
    ["ARP" , None                                   , None                            , lambda: self._doattack("rocket pods")],

    ["J1/2", None                                   , None                            , lambda: self._dojettison("1/2")],
    ["JCL" , None                                   , None                            , lambda: self._dojettison("CL") ],

    ["K"   , None                                   , None                            , lambda: self._dokill()],

  ]

def _doaction(self, action):

  """
  Carry out an action for normal flight.
  """

  if self._hfp + self._vfp + self._spbrfp + 1 > self._fp:
    raise ValueError("only %.1f FPs are available." % self._fp)
    
  self._turnfp += 1

  lastx = self._x
  lasty = self._y

  elementdispatchlist = self._getelementdispatchlist()

  initialaltitudeband = self._altitudeband

  # Prolog elements.
  a = action
  while a != "":
    for element in elementdispatchlist:
      if element[0] == a[:len(element[0])]:
        if element[1] != None:
            element[1]()
        a = a[len(element[0]):]
        break
    else:
      raise ValueError("invalid element %r in action %r." % (a, action))

  # Movement elements.

  self._horizontal = 0
  self._climb      = 0
  self._dive       = 0
  self._turn       = 0

  a = action
  while a != "":
    for element in elementdispatchlist:
      if element[0] == a[:len(element[0])]:
        if element[2] != None:
            element[2]()
        a = a[len(element[0]):]
        break
    else:
      raise ValueError("invalid element %r in action %r." % (a, action))

  if self._horizontal > 1 or self._climb > 1 or self._dive > 1 or self._turn > 1:
    raise ValueError("invalid action %r." % action)
  
  if self._horizontal == 1:
    self._hfp += 1
  elif self._climb == 0 and self._dive == 0:
    raise ValueError("invalid action %r." % action)
  elif self._hfp < self._requiredhfp:
    raise ValueError("insufficient initial HFPs")
  else:
    self._vfp += 1

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

  # Epilog elements.
  a = action
  while a != "":
    for element in elementdispatchlist:
      if element[0] == a[:len(element[0])]:
        if element[3] != None:
            element[3]()
        a = a[len(element[0]):]
        break
    else:
      raise ValueError("invalid element %r in action %r." % (a, action))

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

  if fp + 1 > self._fp or self._destroyed or self._leftmap:

    # See rule 5.4.
    self._fpcarry = self._fp - fp

    self._endmove()
    
  else:
    
    self._drawaircraft("next")

################################################################################

def _startnormalflight(self, actions):
      
  """
  Start to carry out normal flight.
  """

  # See rule 5.4.

  self._fp      = self._speed + self._fpcarry
  self._fpcarry = 0
  self._log("%.1f FPs (including %.1f carry)." % (self._fp, self._fpcarry))
  
  self._log("---")
  self._logposition("start", "")   
  
  # See rule 5.5.

  flighttype     = self._flighttype
  lastflighttype = self._lastflighttype
  
  if lastflighttype == "LVL" and (_isclimbing(flighttype) or _isdiving(flighttype)):
    requiredhfp = 1
  elif (_isclimbing(lastflighttype) and _isdiving(flighttype)) or (_isdiving(lastflighttype) and _isclimbing(flighttype)):
    if self._aircrafttype.hasproperty("HPR"):
      requiredhfp = self._speed // 3
    else:
      requiredhfp = self._speed // 2
  else:
    requiredhfp = 0
  if requiredhfp == 1:
    self._log("- last flight type was %s so the first FP must be an HFP." % lastflighttype)
  elif requiredhfp > 1:
    self._log("- last flight type was %s so the first %d FPs must be HFPs." % (lastflighttype, requiredhfp))
  self._requiredhfp = requiredhfp

  self._hfp     = 0
  self._vfp     = 0
  self._spbrfp  = 0 
      
  self._continuenormalflight(actions)

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

