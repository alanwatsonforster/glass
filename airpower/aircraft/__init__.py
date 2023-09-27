import airpower.aircrafttype as apaircrafttype
import airpower.altitude     as apaltitude
import airpower.azimuth      as apazimuth
import airpower.data         as apdata
import airpower.draw         as apdraw
import airpower.hex          as aphex
import airpower.hexcode      as aphexcode
import airpower.log          as aplog
import airpower.map          as apmap
import airpower.turn         as apturn

import math
    
class aircraft:

  from ._log import _log, _logposition, _logevent, _logbreak

  def __init__(self, name, aircrafttype, hexcode, azimuth, altitude, speed, configuration="CL"):

    x, y = aphexcode.toxy(hexcode)
    facing = apazimuth.tofacing(azimuth)

    apaltitude.checkisvalidaltitude(altitude)
    aphex.checkisvalidfacing(x, y, facing)

    # In addition to the specified position, azimuth, altitude, speed, and 
    # configuration, aircraft initially have level flight, normal power, and
    #no carries.

    self._name          = name
    self._x             = x
    self._y             = y
    self._facing        = facing
    self._altitude      = altitude
    self._altitudeband  = apaltitude.altitudeband(self._altitude)
    self._altitudecarry = 0
    self._speed         = speed
    self._configuration = configuration
    self._flighttype    = "LVL"
    self._powersetting  = "N"
    self._turnfp        = 0
    self._bank          = None
    self._fpcarry       = 0
    self._apcarry       = 0
    self._aircrafttype  = apaircrafttype.aircrafttype(aircrafttype)
    self._destroyed     = False
    self._leftmap       = False
    self._turnsstalled  = None
    self._turnsdeparted = None

    self._saved = []
    self._save(0)

    self._drawaircraft("end")

  def __str__(self):
    s = ""
    for x in [
      ["name"         , self._name],
      ["sheet"        , apmap.tosheet(self._x, self._y) if not self._leftmap else "-- "],
      ["hexcode"      , aphexcode.fromxy(self._x, self._y) if not self._leftmap else "----"],
      ["facing"       , apazimuth.fromfacing(self._facing)],
      ["speed"        , self._speed],
      ["altitude"     , self._altitude],
      ["altitudeband" , self._altitudeband],
      ["flighttype"   , self._flighttype],
      ["powersetting" , self._powersetting],
      ["configuration", self._configuration],
      ["fpcarry"      , self._fpcarry],
      ["apcarry"      , self._apcarry],
      ["altitudecarry", self._altitudecarry],
      ["destroyed"    , self._destroyed],
      ["leftmap"      , self._leftmap],
    ]:
      s += "%-16s: %s\n" % (x[0], x[1])
    return s

  ##############################################################################

  # Drawing

  def _drawflightpath(self, lastx, lasty):
    apdraw.drawflightpath(lastx, lasty, self._x, self._y)

  def _drawaircraft(self, when):
    apdraw.drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, when)
        


  #############################################################################

  # Elements

  def _A(self, weapon):

    """
    Declare an attack with the specified weapon.
    """

    self._logevent("attack with %s." % weapon)

  def _C(self, altitudechange):

    """
    Climb.
    """

    if not self._flighttype in ["ZC", "SC", "VC"]:
      raise ValueError("attempt to climb while flight type is %s." % self._flighttype)

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

  def _D(self, altitudechange):

    """
    Dive.
    """

    if not self._flighttype in ["LVL", "SD", "UD", "VD"]:
      raise ValueError("attempt to dive while flight type is %s." % self._flighttype)

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

  def _H(self):

    """
    Move horizontally.
    """

    self._x, self._y = aphex.nextposition(self._x, self._y, self._facing)

  def _J(self, configuration):

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

  def _K(self):

    """
    Declare that the aircraft has been killed.
    """

    self._logevent("aircraft has been killed.")
    self._destroyed = True

  def _S(self, spbrfp):

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
    if self._speed > _m1speed(self._altitudeband):
      maxspbrfp += 0.5
    if spbrfp > maxspbrfp:
      raise ValueError("speedbrake capability is only %.1f FPs." % maxspbrfp)

    self._spbrfp = spbrfp

    self._spbrap = -spbrfp / 0.5

  def _TD(self, bank, turnrate):

    """
    Start a turn in the specified direction and rate.
    """
    
    turnrates = ["EZ", "TT", "HT", "BT", "ET"]
    assert turnrate in turnrates
    self._bank = bank
    self._turnrate = turnrate

  def _TL(self, facingchange):

    """
    Turn left.
    """

    if self._bank == "R":
      self._turnfp -= 1
    minturnrate = apdata.determineturnrate(self._altitudeband, self._speed, self._turnfp, facingchange)
    if minturnrate == None:
      raise ValueError("attempt to turn faster than the maximum turn rate.")

    self._turnfp = 0
    self._bank = "L"

    # Implicitly declare turn rates.
    self._turnrate = minturnrate

    if self._maxturnrate == None:
      self._maxturnrate = self._turnrate
    else:
      turnrates = ["EZ", "TT", "HT", "BT", "ET"]
      self._maxturnrate = turnrates[max(turnrates.index(self._turnrate), turnrates.index(self._maxturnrate))]

    if self._maxturnrate == "EZ":
      self._turnrateap = 0.0
    else:
      self._turnrateap = -self._aircrafttype.turndrag(self._configuration, self._maxturnrate)

    # See the "Supersonic Speeds" section of rule 6.6.
    if self._speed > _m1speed(self._altitudeband):
      self._turnrateap += 1

    # Change facing.
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
    self._facing = (self._facing + facingchange) % 360

    self._turns += 1
    if self._turns > 1:
      # Apply the sustained turn drag penalty.
      # TODO: drag for HBR and LBR aircraft.
      self._sustainedturnap -= facingchange // 30
      
  def _TR(self, facingchange):

    """
    Turn right.
    """

    if self._bank == "L":
      self._turnfp -= 1
    minturnrate = apdata.determineturnrate(self._altitudeband, self._speed, self._turnfp, facingchange)
    if minturnrate == None:
      raise ValueError("attempt to turn faster than the maximum turn rate.")

    self._turnfp = 0
    self._bank = "R"

    # Implicitly declare turn rates.
    self._turnrate = minturnrate

    if self._maxturnrate == None:
      self._maxturnrate = self._turnrate
    else:
      turnrates = ["EZ", "TT", "HT", "BT", "ET"]
      self._maxturnrate = turnrates[max(turnrates.index(self._turnrate), turnrates.index(self._maxturnrate))]

    if self._maxturnrate == "EZ":
      self._turnrateap = 0.0
    else:
      self._turnrateap = -self._aircrafttype.turndrag(self._configuration, self._maxturnrate)

    # See the "Supersonic Speeds" section of rule 6.6.
    if self._speed > _m1speed(self._altitudeband):
      self._turnrateap += 1

    # Change facing.
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
    self._facing = (self._facing - facingchange) % 360
    
    self._turns += 1
    if self._turns > 1:
      # Apply the sustained turn drag penalty.
      # TODO: drag for HBR and LBR aircraft.
      self._sustainedturnap -= facingchange // 30
      
  def _getelementdispatchlist(self):
  
    return [

      # This table is searched in order, so put longer elements before shorter 
      # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

      # [0] is the element code.
      # [1] is the procedure for movement elements.
      # [2] is the procedure for other (non-movement) elements.

      ["H"   , lambda : None               , lambda : self._H()          , lambda: None],

      ["C1/8", lambda : None               , lambda : self._C(1/8)       , lambda: None],
      ["C1/4", lambda : None               , lambda : self._C(1/4)       , lambda: None],
      ["C3/8", lambda : None               , lambda : self._C(3/8)       , lambda: None],
      ["C1/2", lambda : None               , lambda : self._C(1/2)       , lambda: None],
      ["C5/8", lambda : None               , lambda : self._C(5/8)       , lambda: None],
      ["C3/4", lambda : None               , lambda : self._C(3/4)       , lambda: None],
      ["C7/8", lambda : None               , lambda : self._C(7/8)       , lambda: None],
      ["C1"  , lambda : None               , lambda : self._C(1)         , lambda: None],
      ["C2"  , lambda : None               , lambda : self._C(2)         , lambda: None],
      ["CC"  , lambda : None               , lambda : self._C(2)         , lambda: None],
      ["C"   , lambda : None               , lambda : self._C(1)         , lambda: None],

      ["D1/8", lambda : None               , lambda : self._D(1/8)       , lambda: None],
      ["D1/4", lambda : None               , lambda : self._D(1/4)       , lambda: None],
      ["D3/8", lambda : None               , lambda : self._D(3/8)       , lambda: None],
      ["D1/2", lambda : None               , lambda : self._D(1/2)       , lambda: None],
      ["D5/8", lambda : None               , lambda : self._D(5/8)       , lambda: None],
      ["D3/4", lambda : None               , lambda : self._D(3/4)       , lambda: None],
      ["D7/8", lambda : None               , lambda : self._D(7/8)       , lambda: None],
      ["D1"  , lambda : None               , lambda : self._D(1)         , lambda: None],
      ["D2"  , lambda : None               , lambda : self._D(2)         , lambda: None],
      ["D3"  , lambda : None               , lambda : self._D(3)         , lambda: None],
      ["DDD" , lambda : None               , lambda : self._D(3)         , lambda: None],
      ["DD"  , lambda : None               , lambda : self._D(2)         , lambda: None],
      ["D"   , lambda : None               , lambda : self._D(1)         , lambda: None],

      ["LEZ" , lambda : self._TD("L", "EZ"), lambda : None               , lambda: None],
      ["LTT" , lambda : self._TD("L", "TT"), lambda : None               , lambda: None],
      ["LHT" , lambda : self._TD("L", "HT"), lambda : None               , lambda: None],
      ["LBT" , lambda : self._TD("L", "BT"), lambda : None               , lambda: None],
      ["LET" , lambda : self._TD("L", "ET"), lambda : None               , lambda: None],
      
      ["REZ" , lambda : self._TD("R", "EZ"), lambda : None               , lambda: None],
      ["RTT" , lambda : self._TD("R", "TT"), lambda : None               , lambda: None],
      ["RHT" , lambda : self._TD("R", "HT"), lambda : None               , lambda: None],
      ["RBT" , lambda : self._TD("R", "BT"), lambda : None               , lambda: None],
      ["RET" , lambda : self._TD("R", "ET"), lambda : None               , lambda: None],

      ["L90" , lambda : None               , lambda : self._TL(90)       , lambda: None],
      ["L60" , lambda : None               , lambda : self._TL(60)       , lambda: None],
      ["L30" , lambda : None               , lambda : self._TL(30)       , lambda: None],
      ["LLL" , lambda : None               , lambda : self._TL(90)       , lambda: None],
      ["LL"  , lambda : None               , lambda : self._TL(60)       , lambda: None],
      ["L"   , lambda : None               , lambda : self._TL(30)       , lambda: None],

      ["R90" , lambda : None               , lambda : self._TR(90)       , lambda: None],
      ["R60" , lambda : None               , lambda : self._TR(60)       , lambda: None],
      ["R30" , lambda : None               , lambda : self._TR(30)       , lambda: None],
      ["RRR" , lambda : None               , lambda : self._TR(90)       , lambda: None],
      ["RR"  , lambda : None               , lambda : self._TR(60)       , lambda: None],
      ["R"   , lambda : None               , lambda : self._TR(30)       , lambda: None],

      ["S1/2", lambda : None               , lambda: self._S(1/2)        , lambda: None],
      ["S1"  , lambda : None               , lambda: self._S(1)          , lambda: None],
      ["S3/2", lambda : None               , lambda: self._S(3/2)        , lambda: None],
      ["S2"  , lambda : None               , lambda: self._S(2)          , lambda: None],
      ["SSSS", lambda : None               , lambda: self._S(2)          , lambda: None],
      ["SSS" , lambda : None               , lambda: self._S(3/2)        , lambda: None],
      ["SS"  , lambda : None               , lambda: self._S(1)          , lambda: None],
      ["S"   , lambda : None               , lambda: self._S(1/2)        , lambda: None],

      ["/"   , lambda : None               , lambda : None               , lambda: None],

      ["AGN" , lambda : None               , lambda : None               , lambda: self._A("guns")],
      ["AGP" , lambda : None               , lambda : None               , lambda: self._A("gun pod")],
      ["ARK" , lambda : None               , lambda : None               , lambda: self._A("rockets")],
      ["ARP" , lambda : None               , lambda : None               , lambda: self._A("rocket pods")],

      ["J1/2", lambda : None               , lambda : None               , lambda: self._J("1/2")],
      ["JCL" , lambda : None               , lambda : None               , lambda: self._J("CL") ],

      ["K"   , lambda : None               , lambda : None               , lambda: self._K()],

    ]

  def _doaction(self, action):

    """
    Carry out an action for normal flight.
    """

    if self._hfp + self._vfp + self._spbrfp + 1 > self._fp:
      raise ValueError("only %.1f FPs are available." % self._fp)
        
    if action[0] == 'H':
      self._hfp += 1
    elif action[0] == 'D' or action[0] == 'C':
      self._vfp += 1
    else:
      raise ValueError("action %s does not begin with H, D, or C." % action)
      
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
          element[1]()
          a = a[len(element[0]):]
          break
      else:
        raise ValueError("invalid element %r in action %r." % (a, action))

    # Movement elements.
    a = action
    while a != "":
      for element in elementdispatchlist:
        if element[0] == a[:len(element[0])]:
          element[2]()
          a = a[len(element[0]):]
          break
      else:
        raise ValueError("invalid element %r in action %r." % (a, action))

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

    # Other elements.
    a = action
    while a != "":
      for element in elementdispatchlist:
        if element[0] == a[:len(element[0])]:
          element[3]()
          a = a[len(element[0]):]
          break
      else:
        raise ValueError("invalid element %r in action %r." % (a, action))

  def _donormalflight(self, actions):

    """
    Carry out normal flight.
    """

    if actions != "":
      for action in actions.split(","):
        if not self._destroyed and not self._leftmap:
          self._doaction(action)

    fp = self._hfp + self._vfp + self._spbrfp
    assert fp <= self._fp

    if fp + 1 > self._fp or self._destroyed or self._leftmap:

      self._drawaircraft("end")
      self._log("---")
      self._endmove()
      
    else:
      
      self._drawaircraft("next")

  ##############################################################################

  def _dostalledflightaction(self, action):

    """
    Validate and carry out an action for stalled flight.
    """

    if action == "J1/2":
      self._J("1/2")
    elif action == "JCL":
      self._J("CL")
    elif action != "":
      raise ValueError("invalid action %r for stalled flight." % action)

  def _dostalledflight(self, action):

    """
    Carry out stalled flight.
    """

    # See rule 6.4.

    initialaltitudeband = self._altitudeband

    altitudechange = math.ceil(self._speed + self._turnsstalled)

    initialaltitude = self._altitude    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
    self._altitudeband = apaltitude.altitudeband(self._altitude)
    altitudechange = initialaltitude - self._altitude
    
    if self._turnsstalled == 0:
      self._altitudeap = 0.5 * altitudechange
    else:
      self._altitudeap = 1.0 * altitudechange

    self._logposition("end", action)

    if initialaltitudeband != self._altitudeband:
      self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
    self.checkforterraincollision()

    self._dostalledflightaction(action)

  ##############################################################################

  def _dodepartedaction(self, action):

    """
    Validate and carry out an action for departed flight.
    """

    # See rule 6.4.

    if action == "R":
      action = "R30"
    elif action == "RR":
      action = "R60"
    elif action == "RRR":
      action = "R90"
    elif action == "L":
      action = "L30"
    elif action == "LL":
      action = "L60"
    elif action == "LLL":
      action = "L90"
  
    if len(action) < 3 or (action[0] != "R" and action[0] != "L") or not action[1:].isdecimal():
      raise ValueError("invalid action %r for departed flight." % action)

    facingchange = int(action[1:])
    if facingchange % 30 != 0 or facingchange <= 0 or facingchange > 300:
      raise ValueError("invalid action %r for departed flight." % action)

    if action[0] == "R":
      if aphex.isedgeposition(self._x, self._y):
        self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
      self._facing = (self._facing - facingchange) % 360
    else:
      if aphex.isedgeposition(self._x, self._y):
        self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
      self._facing = (self._facing + facingchange) % 360
 
  def _dodepartedflight(self, action):

    """
    Carry out departed flight.
    """

    # See rule 6.4.

    initialaltitudeband = self._altitudeband

    altitudechange = math.ceil(self._speed + 2 * self._turnsdeparted)
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
    self._altitudeband = apaltitude.altitudeband(self._altitude)

    self._logposition("end", action)

    if initialaltitudeband != self._altitudeband:
      self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
    self.checkforterraincollision()
      
    self._dodepartedaction(action)
    
      
  ##############################################################################

  def checkforterraincollision(self):

    """
    Check if the aircraft has collided with terrain.
    """

    altitudeofterrain = apaltitude.terrainaltitude()
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._logevent("aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True

  def checkforleavingmap(self):

    """
    Check if the aircraft has left the map.
    """

    if not apmap.iswithinmap(self._x, self._y):
      self._logevent("aircraft has left the map.")
      self._leftmap = True
  
  ##############################################################################

  # Turn management
  
  def _restore(self, i):

    """
    Restore the aircraft properties at the start of the specified turn.
    """

    self._x, \
    self._y, \
    self._facing, \
    self._altitude, \
    self._altitudecarry, \
    self._speed, \
    self._configuration, \
    self._powersetting, \
    self._flighttype, \
    self._fpcarry, \
    self._apcarry, \
    self._destroyed, \
    self._leftmap, \
    self._turnsstalled, \
    self._turnsdeparted \
    = self._saved[i]
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  def _save(self, i):

    """
    Save the aircraft properties at the end of the specified turn.
    """

    if len(self._saved) == i:
      self._saved.append(None)
    self._saved[i] = ( \
      self._x, \
      self._y, \
      self._facing, \
      self._altitude, \
      self._altitudecarry, \
      self._speed, \
      self._configuration, \
      self._powersetting, \
      self._flighttype, \
      self._fpcarry, \
      self._apcarry, \
      self._destroyed, \
      self._leftmap, \
      self._turnsstalled, \
      self._turnsdeparted \
    )

  ##############################################################################

  def _startmovepower(self, power, flamedoutfraction):

    """
    Carry out the rules to do with power and drag at the start of a move.
    """

    lastpowersetting = self._lastpowersetting

    powerapM  = self._aircrafttype.power(self._configuration, "M")
    powerapAB = self._aircrafttype.power(self._configuration, "AB")

    # See rule 6.1.

    if power == "I":
      powersetting = "I"
      powerap      = 0
    elif power == "N" or power == 0:
      powersetting = "N"
      powerap      = 0
    elif power == "M":
      powersetting = "M"
      powerap      = powerapM
    elif power == "AB" and powerapAB == None:
      raise ValueError("aircraft does not have AB.")
    elif power == "AB":
      powersetting = "AB"
      powerap      = powerapAB
    elif not isinstance(power, (int, float)) or power < 0 or power % 0.25 != 0:
      raise ValueError("invalid power %r" % power)
    elif power <= powerapM:
      powersetting = "M"
      powerap      = power
    elif powerapAB != None and power <= powerapAB:
      powersetting = "AB"
      powerap      = power
    else:
      raise ValueError("requested power of %s APs exceeds aircraft capability." % power)

    self._log("power setting is %s." % powersetting)

    # See the "Effects of Flame-Out" section of rule 6.7

    if flamedoutfraction == 1:

      self._log("- power setting is treated as idle as all engines are flamed-out.")
      power = "I"
      powerap = 0

    elif flamedoutfraction > 0.5:

      self._log("- power is reduced by one third as more than half of engines are flamed-out.")
      # 1/3 of APs, quantized in 1/4 units, rounding down.
      powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

      self._log("- power is reduced by one half as less than half of engines are flamed-out.")
      # 1/2 of APs, quantized in 1/4 units, rounding up.
      powerap = math.ceil(powerap / 2 * 4) / 4

    # See the "Rapid Power Response" section of rule 6.1.

    if lastpowersetting == "I" and powersetting == "AB" and not self._aircrafttype.hasproperty("RPR"):
      self._log("- risk of flame-out as power setting has increased from I to AB.")

    # See the "When Does a Jet Flame-Out?" section of rule 6.7.

    if powersetting != "I" and self._altitude > self._aircrafttype.ceiling(self._configuration):
      self._log("- risk of flame-out as aircraft is above its ceiling and power setting is %s." % powersetting)
      
    # See the "Speed of Sound" and "Transonic Speeds" section of rule 6.6.

    m1speed = _m1speed(self._altitudeband)
    htspeed = m1speed - 0.5
    ltspeed = m1speed - 1.0

    if self._speed >= m1speed:
      speed = "%.1f (SS)" % self._speed
    elif self._speed == htspeed:
      speed = "%.1f (HT)" % self._speed
    elif self._speed == ltspeed:
      speed = "%.1f (LT)" % self._speed
    else:
      speed = "%.1f" % self._speed
    self._log("speed is %s." % speed)

    # See the "Idle" section of rule 6.1 and the "Supersonic Speeds" section of rule 6.6

    if powersetting == "I":
      speedchange = self._aircrafttype.power(self._configuration, "I")
      if self._speed >= m1speed:
        speedchange += 0.5
      # This keeps the speed non-negative. See rule 6.2.
      speedchange = min(speedchange, self._speed)
      self._speed -= speedchange
      self._log("- reducing speed to %.1f as the power setting is I." % self._speed)

    # There is some ambiguity as to whether the other effects that depend on 
    # the start speed refer to it before or after the reduction for idle power.
    # Here we use it after the reduction.

    startspeed = self._speed

    # We use a explicit dragap rather than reducing powerap for drag effects.
    dragap = 0.0

    # See the "Decel Point Penalty for Insufficient Power" section of rule 6.1.

    if startspeed > self._aircrafttype.cruisespeed():
      if powersetting == "I" or powersetting == "N":
        self._log("- insufficient power above cruise speed.")
        dragap -= 1.0

    # See the "Supersonic Speeds" section of rule 6.6
    
    if startspeed >= m1speed:
      if powersetting == "I" or powersetting == "N":
        dragap -= 2.0 * (startspeed - htspeed) / 0.5
        self._log("- insufficient power at supersonic speed.")
      elif powersetting == "M":
        dragap -= 1.5 * (startspeed - htspeed) / 0.5
        self._log("- insufficient power at supersonic speed.")

    # See the "Transonic Speeds" section of rule 6.6

    if ltspeed <= startspeed and startspeed <= m1speed:
      self._log("- transonic drag.")
      if startspeed == ltspeed:
        dragap -= 0.5
      elif startspeed == htspeed:
        dragap -= 1.0
      elif startspeed == m1speed:
        dragap -= 1.5
      if self._aircrafttype.hasproperty("LTD"):
        dragap += 0.5
      elif self._aircrafttype.hasproperty("HTD"):
        dragap -= 0.5

    return powersetting, powerap, dragap

  ##############################################################################

  def _startmoveflighttype(self, flighttype):

    """
    Carry out the rules to do with the flight type at the start of a move.
    """

    if flighttype not in ["LVL", "SC", "ZC", "VC", "SD", "UD", "VD", "ST", "DP"]:
      raise ValueError("invalid flight type %r." % flighttype)

    self._log("flight type is %s." % (flighttype))

    lastflighttype = self._lastflighttype

    requiredhfp = 0

    if flighttype == "DP":

      # See rule 6.4.

      self._powerap = 0
      self._apcarry = 0

      if self._powersetting == "M" or self._powersetting == "AB":
        self._log("- risk of flame-out as power setting is %s in departed flight." % self._powersetting)

      if lastflighttype != "DP":
        self._turnsdeparted = 0
      else:
        self._turnsdeparted += 1
      self._turnsstalled  = None
  
    elif lastflighttype == "DP":

      # See rule 6.4.

      if _isclimbing(flighttype):
        raise ValueError("flight type immediately after DP must not be climbing.")
      elif flighttype == "LVL" and not self._aircrafttype.hasproperty("HPR"):
        raise ValueError("flight type immediately after DP must not be level.")

      self._speed = max(self._speed, self._aircrafttype.minspeed(self._configuration, self._altitudeband))

      self._turnsstalled  = None
      self._turnsdeparted = None
 
    elif self._speed < self._aircrafttype.minspeed(self._configuration, self._altitudeband):

      # See rules 6.3 and 6.4.

      self._log("- aircraft is stalled.")
      if flighttype != "ST":
        raise ValueError("flight type must be ST.")

      if lastflighttype != "ST":
        self._turnsstalled = 0
      else:
        self._turnsstalled += 1
      self._turnsdeparted = None

    elif flighttype == "ST":

      raise ValueError("flight type cannot be ST as aircraft is not stalled.")

    elif lastflighttype == "ST":

      # See rule 6.4.

      if _isclimbing(flighttype):
        raise ValueError("flight type immediately after ST must not be climbing.")

      self._turnsstalled  = None
      self._turnsdeparted = None

    else:

      # See rule 5.5.

      if lastflighttype == "LVL" and (_isclimbing(flighttype) or _isdiving(flighttype)):
        requiredhfp = 1
      elif (_isclimbing(lastflighttype) and _isdiving(flighttype)) or (_isdiving(lastflighttype) and _isclimbing(flighttype)):
        if self._aircrafttype.hasproperty("HPR"):
          requiredhfp = self._speed // 3
        else:
          requiredhfp = self._speed // 2
      if requiredhfp > 0:
        self._log("- changing from %s to %s flight so the first %d FPs must be HFPs." % (lastflighttype, flighttype, requiredhfp))

      self._turnsstalled  = None
      self._turnsdeparted = None
  
    return flighttype

  ##############################################################################

  def startmove(self, flighttype, power, actions, flamedoutfraction=0):

    """
    Start a move, declaring the flight type and power, and possible carrying 
    out some actions.
    """

    self._log("--- start of move --")

    self._restore(apturn.turn() - 1)

    if self._destroyed or self._leftmap:
      self._endmove()
      return

    self._lastconfiguration = self._configuration
    self._lastpowersetting  = self._powersetting
    self._lastflighttype    = self._flighttype
    self._lastaltitudeband  = self._altitudeband
    self._lastspeed         = self._speed

    self._hfp              = 0
    self._vfp              = 0
    self._spbrfp           = 0

    self._turns            = 0
    self._turnrate         = None
    self._maxturnrate      = None

    self._spbrap           = 0
    self._turnrateap       = 0
    self._sustainedturnap  = 0
    self._altitudeap       = 0

    self._powersetting,    \
    self._powerap,         \
    self._dragap           = self._startmovepower(power, flamedoutfraction)
    self._flighttype       = self._startmoveflighttype(flighttype)

    if self._flighttype == "ST":

      # See rule 6.4.

      self._log("carrying %+.2f APs, and %s altitude levels." % (
        self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))
      
      self._fp      = 0
      self._fpcarry = 0
      
      self._log("---")
      self._logposition("start", "")
      self._dostalledflight(actions)
      self._drawaircraft("end")
      self._log("---")
      self._endmove()

    elif self._flighttype == "DP":

      # See rule 6.4.

      self._log("carrying %s altitude levels." % (
        apaltitude.formataltitudecarry(self._altitudecarry)
      ))
      
      self._fp      = 0
      self._fpcarry = 0
      self._apcarry = 0
      
      self._log("---")
      self._logposition("start", "")
      self._dodepartedflight(actions)
      self._drawaircraft("end")
      self._log("---")
      self._endmove()
        
    else:

      self._log("carrying %.1f FPs, %+.2f APs, and %s altitude levels." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))
      
      # See rule 5.4.
      self._fp      = self._speed + self._fpcarry
      self._fpcarry = 0
      self._log("%.1f FPs are available." % self._fp)

      self._log("---")
      self._logposition("start", "")
      self.continuemove(actions)

  ################################################################################

  def continuemove(self, actions):

    """
    Continue a move that has been started, possible carrying out some actions.
    """

    if self._destroyed or self._leftmap or self._flighttype == "ST" or self._flighttype == "DP":
      return

    self._donormalflight(actions)

  ################################################################################

  def _endmove(self):

    """
    Process the end of a move.
    """

    if self._destroyed:
    
      self._log("aircraft has been destroyed.")

    elif self._leftmap:

      self._log("aircraft has left the map.")

    else:

      if self._flighttype != "ST" and self._flighttype != "DP":
        self._log("used %d HFPs, %d VFPs, and %.1f SPBRFPs." % (self._hfp, self._vfp, self._spbrfp))

      if self._lastconfiguration != self._configuration:
        self._log("configuration changed from %s to %s." % (self._lastconfiguration, self._configuration))
      else:
        self._log("configuration is unchanged at %s." % self._configuration)
              
      if self._lastaltitudeband != self._altitudeband:
        self._log("altitude band changed from %s to %s." % (self._lastaltitudeband, self._altitudeband))
      else:
        self._log("altitude band is unchanged at %s." % self._altitudeband)

      if self._maxturnrate == None:
        self._log("- no turns.")
      else:
        self._log("- maximum turn rate is %s." % self._maxturnrate)

      # See rule 6.2.

      self._log("- power     APs = %+.2f." % self._powerap)
      self._log("- altitude  APs = %+.2f." % self._altitudeap)
      self._log("- drag      APs = %+.2f." % self._dragap)
      self._log("- turn      APs = %+.2f and %+.2f." % (self._turnrateap, self._sustainedturnap))
      self._log("- SPBR      APs = %+.2f." % self._spbrap)
      ap = self._turnrateap + self._sustainedturnap + self._altitudeap + self._spbrap + self._powerap + self._dragap
      self._log("- total     APs = %+.2f with %+.2f carry = %+.2f." % (ap, self._apcarry, ap + self._apcarry))
      ap += self._apcarry

      # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
      # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

      if ap < 0:
        aprate = -2.0
      elif self._aircrafttype.hasproperty("RA"):
        if self._speed >= _m1speed(self._altitudeband):
          aprate = +2.0
        else:
          aprate = +1.5
      else:
        if self._speed >= _m1speed(self._altitudeband):
          aprate = +3.0
        else:
          aprate = +2.0

      # See rule 6.2 and 6.3

      if ap < 0:

        assert self._flighttype != "DP"

        self._speed -= 0.5 * (ap // aprate)
        self._apcarry = ap % aprate

        # See the "Maximum Deceleration" section of rule 6.2.

        if self._speed <= 0:
          self._speed = 0
          if self._apcarry < 0:
            self._apcarry = 0        

      elif ap > 0:

        assert self._flighttype != "DP"

        # See rule 6.2 and the "Acceleration limits" section of rule 6.3.

        if self._flighttype == "LVL" or _isclimbing(self._flighttype):
          maxspeed = self._aircrafttype.maxspeed(self._configuration, self._altitudeband)
          maxspeedname = "maximum speed"
        elif _isdiving(self._flighttype) or self._flighttype == "ST":
          maxspeed = self._aircrafttype.maxdivespeed(self._altitudeband)
          maxspeedname = "maximum dive speed"

        if self._speed >= maxspeed and ap >= aprate:
          self._log("- acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
          self._apcarry = aprate - 0.5
        elif self._speed >= maxspeed:
          self._apcarry = ap
        elif self._speed + 0.5 * (ap // aprate) > maxspeed:
          self._log("- acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
          self._speed = maxspeed
          self._apcarry = aprate - 0.5
        else:
          self._speed += 0.5 * (ap // aprate)
          self._apcarry = ap % aprate

      # See rule 6.3.

      if self._flighttype == "LVL" or _isclimbing(self._flighttype):

        # See the "Speed Fadeback" section of rule 6.3.

        maxspeed = self._aircrafttype.maxspeed(self._configuration, self._altitudeband)
        if self._speed > maxspeed:
          self._log("- speed is faded back from %.1f." % self._speed)
          self._speed = max(self._speed - 1, maxspeed)

      elif _isdiving(self._flighttype) or self._flighttype == "ST" or self._flighttype == "DP":

        # See the "Diving Speed Limits" section of rule 6.3.

        maxspeed = self._aircrafttype.maxdivespeed(self._altitudeband)
        if self._speed > maxspeed:
          self._log("- speed is reduced to maximum dive speed of %.1f." % maxspeed)
          self._speed = maxspeed

      if self._lastspeed != self._speed:
        self._log("speed changed from %.1f to %.1f." % (self._lastspeed, self._speed))
      else:
        self._log("speed is unchanged at %.1f." % self._speed)

      if self._flighttype == "ST":
        if self._speed >= self._aircrafttype.minspeed(self._configuration, self._altitudeband):
          self._log("- aircraft has exited from stall.")
        else:
          self._log("- aircraft is still stalled.")

      # See rule 5.4.

      fp = self._hfp + self._vfp + self._spbrfp
      self._fpcarry = self._fp - fp

      self._log("carrying %.1f FPs, %+.2f APs, and %s altitude levels." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))

    self._save(apturn.turn())

    self._log("--- end of move -- ")
    self._logbreak()

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

def _m1speed(altitudeband):
  if altitudeband == "LO" or altitudeband == "ML":
    return 7.5
  elif altitudeband == "MH" or altitudeband == "HI":
    return 7.0
  else:
    return 6.5
