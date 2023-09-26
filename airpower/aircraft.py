import airpower.aircrafttype as apaircrafttype
import airpower.altitude     as apaltitude
import airpower.azimuth      as apazimuth
import airpower.draw         as apdraw
import airpower.hex          as aphex
import airpower.hexcode      as aphexcode
import airpower.log          as aplog
import airpower.map          as apmap
import airpower.turn         as apturn

import math
    
class aircraft:

  def __init__(self, name, aircrafttype, hexcode, azimuth, altitude, speed, configuration="CL"):

    x, y = aphexcode.toxy(hexcode)
    facing = apazimuth.tofacing(azimuth)

    apaltitude.checkisvalidaltitude(altitude)
    aphex.checkisvalidfacing(x, y, facing)

    self._name          = name
    self._x             = x
    self._y             = y
    self._facing        = facing
    self._altitude      = altitude
    self._altitudecarry = 0
    self._speed         = speed
    self._configuration = configuration
    self._flighttype    = "LV"
    self._powersetting  = "N"
    self._fpcarry       = 0
    self._apcarry       = 0
    self._aircrafttype  = apaircrafttype.aircrafttype(aircrafttype)
    self._destroyed     = False
    self._leftmap       = False
    self._turnsstalled  = None

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
      ["fpcarry"      , self._fpcarry],
      ["apcarry"      , self._apcarry],
      ["altitude"     , self._altitude],
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
        
  ##############################################################################

  def _m1(self):
    altitudeband = self._altitudeband
    if altitudeband == "LO" or altitudeband == "ML":
      return 7.5
    elif altitudeband == "MH" or altitudeband == "HI":
      return 7.0
    else:
      return 6.5

  ##############################################################################

  # Reporting

  def _formatposition(self):
    if apmap.isonmap(self._x, self._y):
      sheet = apmap.tosheet(self._x, self._y)
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      sheet = "--"
      hexcode = "----"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%2s %-9s  %-3s  %2d" % (sheet, hexcode, azimuth, altitude)

  def _log(self, s):
    aplog.log("%s: turn %-2d : %s" % (self._name, apturn.turn(), s))

  def _logbreak(self):
    aplog.logbreak()

  def _logposition(self, s, t):
    self._log("%-5s : %-16s : %s" % (s, t, self._formatposition()))

  def _logevent(self, s):
    self._log("%-5s : %s" % ("", s))

  #############################################################################

  # Elements

  def _A(self, what):
    self._logevent("attack with %s." % what)

  def _C(self, altitudechange):

    if not self._flighttype in ["ZC", "SC", "VC"]:
      raise ValueError("attempt to climb while flight type is %s." % self._flighttype)

    initialaltitude = self._altitude    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)
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

    if not self._flighttype in ["LV", "SD", "UD", "VD"]:
      raise ValueError("attempt to dive while flight type is %s." % self._flighttype)

    initialaltitude = self._altitude    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
    altitudechange = initialaltitude - self._altitude

    if self._flighttype == "LV":
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
    self._x, self._y = aphex.nextposition(self._x, self._y, self._facing)

  def _J(self, configuration):
    # See rule 4.4. We implement the delay of 1 FP by making this a non-movement element.
    if self._configuration == configuration:
      raise ValueError("configuration is already %s." % configuration)
    if self._configuration == "CL" or configuration == "DT":
      raise ValueError("attempt to change from configuration %s to %s." % (self._configuration, configuration))
    self._logevent("jettisoned stores.")
    self._logevent("changed configuration from %s to %s." % (self._configuration, configuration))
    self._configuration = configuration

  def _K(self):
    self._logevent("aircraft has been killed.")
    self._destroyed = True

  def _S(self, spbrfp):
    # TODO: check against aircraft SPBR capability.
    if self._spbrfp != 0:
      raise ValueError("speedbrakes can only be used once per turn.")
    maxspbrfp = self._fp - self._hfp - self._vfp
    if spbrfp > maxspbrfp:
      raise ValueError("attempt to use speedbrakes to eliminate %s FPs but only %s are remaining." % (spbrfp, maxspbrfp))
    self._spbrfp = spbrfp
    self._spbrap = -spbrfp / 0.5

  def _TD(self, turndirection, turnrate):
    """
    Declare a turn in the specified direction and rate.
    """
    turnrates = ["EZ", "TT", "HT", "BT", "ET"]
    assert turnrate in turnrates
    self._turndirection = turndirection
    self._turnrate = turnrate
    if self._maxturnrate == None:
      self._maxturnrate = turnrate
    else:
      self._maxturnrate = turnrates[max(turnrates.index(turnrate), turnrates.index(self._maxturnrate))]

  def _TL(self, facingchange):
    """
    Turn left.
    """

    if self._turnrate == None:
      # Implicitly declare a turn rate of EZ.
      self._TD("L", "EZ")

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

    if self._turnrate == None:
      # Implicitly declare a turn rate of EZ.
      self._TD("R", "EZ")

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

      ["H"   , lambda : self._H()          , lambda: None],

      ["C1/8", lambda : self._C(1/8)       , lambda: None],
      ["C1/4", lambda : self._C(1/4)       , lambda: None],
      ["C3/8", lambda : self._C(3/8)       , lambda: None],
      ["C1/2", lambda : self._C(1/2)       , lambda: None],
      ["C5/8", lambda : self._C(5/8)       , lambda: None],
      ["C3/4", lambda : self._C(3/4)       , lambda: None],
      ["C7/8", lambda : self._C(7/8)       , lambda: None],
      ["C⅛"  , lambda : self._C(1/8)       , lambda: None],
      ["C¼"  , lambda : self._C(1/4)       , lambda: None],
      ["C⅜"  , lambda : self._C(3/8)       , lambda: None],
      ["C½"  , lambda : self._C(1/2)       , lambda: None],
      ["C⅝"  , lambda : self._C(5/8)       , lambda: None],
      ["C¾"  , lambda : self._C(3/4)       , lambda: None],
      ["C⅞"  , lambda : self._C(7/8)       , lambda: None],
      ["C1"  , lambda : self._C(1)         , lambda: None],
      ["C2"  , lambda : self._C(2)         , lambda: None],
      ["CC"  , lambda : self._C(2)         , lambda: None],
      ["C"   , lambda : self._C(1)         , lambda: None],

      ["D1/8", lambda : self._D(1/8)       , lambda: None],
      ["D1/4", lambda : self._D(1/4)       , lambda: None],
      ["D3/8", lambda : self._D(3/8)       , lambda: None],
      ["D1/2", lambda : self._D(1/2)       , lambda: None],
      ["D5/8", lambda : self._D(5/8)       , lambda: None],
      ["D3/4", lambda : self._D(3/4)       , lambda: None],
      ["D7/8", lambda : self._D(7/8)       , lambda: None],
      ["D⅛"  , lambda : self._D(1/8)       , lambda: None],
      ["D¼"  , lambda : self._D(1/4)       , lambda: None],
      ["D⅜"  , lambda : self._D(3/8)       , lambda: None],
      ["D½"  , lambda : self._D(1/2)       , lambda: None],
      ["D⅝"  , lambda : self._D(5/8)       , lambda: None],
      ["D¾"  , lambda : self._D(3/4)       , lambda: None],
      ["D⅞"  , lambda : self._D(7/8)       , lambda: None],
      ["D1"  , lambda : self._D(1)         , lambda: None],
      ["D2"  , lambda : self._D(2)         , lambda: None],
      ["D3"  , lambda : self._D(3)         , lambda: None],
      ["DDD" , lambda : self._D(3)         , lambda: None],
      ["DD"  , lambda : self._D(2)         , lambda: None],
      ["D"   , lambda : self._D(1)         , lambda: None],

      ["LEZ" , lambda : self._TD("L", "EZ"), lambda: None],
      ["LTT" , lambda : self._TD("L", "TT"), lambda: None],
      ["LHT" , lambda : self._TD("L", "HT"), lambda: None],
      ["LBT" , lambda : self._TD("L", "BT"), lambda: None],
      ["LET" , lambda : self._TD("L", "ET"), lambda: None],
      
      ["REZ" , lambda : self._TD("R", "EZ"), lambda: None],
      ["RTT" , lambda : self._TD("R", "TT"), lambda: None],
      ["RHT" , lambda : self._TD("R", "HT"), lambda: None],
      ["RBT" , lambda : self._TD("R", "BT"), lambda: None],
      ["RET" , lambda : self._TD("R", "ET"), lambda: None],

      ["L90" , lambda : self._TL(90)       , lambda: None],
      ["L60" , lambda : self._TL(60)       , lambda: None],
      ["L30" , lambda : self._TL(30)       , lambda: None],
      ["LLL" , lambda : self._TL(90)       , lambda: None],
      ["LL"  , lambda : self._TL(60)       , lambda: None],
      ["L"   , lambda : self._TL(30)       , lambda: None],

      ["R90" , lambda : self._TR(90)       , lambda: None],
      ["R60" , lambda : self._TR(60)       , lambda: None],
      ["R30" , lambda : self._TR(30)       , lambda: None],
      ["RRR" , lambda : self._TR(90)       , lambda: None],
      ["RR"  , lambda : self._TR(60)       , lambda: None],
      ["R"   , lambda : self._TR(30)       , lambda: None],

      ["ST"  , lambda : self._ST()         , lambda: None],

      ["S1/2", lambda: self._S(1/2)        , lambda: None],
      ["S3/2", lambda: self._S(3/2)        , lambda: None],
      ["S½"  , lambda: self._S(1/2)        , lambda: None],
      ["S1½" , lambda: self._S(3/2)        , lambda: None],
      ["S1"  , lambda: self._S(1)          , lambda: None],
      ["S2"  , lambda: self._S(2)          , lambda: None],
      ["SSSS", lambda: self._S(2)          , lambda: None],
      ["SSS" , lambda: self._S(3/2)        , lambda: None],
      ["SS"  , lambda: self._S(1)          , lambda: None],
      ["S"   , lambda: self._S(1/2)        , lambda: None],

      ["/"   , lambda : None               , lambda: None],

      ["AGN" , lambda : None               , lambda: self._A("guns")],
      ["AGP" , lambda : None               , lambda: self._A("gun pod")],
      ["ARK" , lambda : None               , lambda: self._A("rockets")],
      ["ARP" , lambda : None               , lambda: self._A("rocket pods")],

      ["J1/2", lambda : None               , lambda: self._J("1/2")],
      ["JCL" , lambda : None               , lambda: self._J("CL") ],

      ["K"   , lambda : None               , lambda: self._K()],

    ]

  def _doaction(self, action):

      if self._flighttype == "ST":

        self._vfp += 1

      else:

        if self._hfp + self._vfp + self._spbrfp + 1 > self._fp:
          raise ValueError("only %d FPs are available." % self._fp)
        
        if action[0] == 'H':
          self._hfp += 1
        elif action[0] == 'D' or action[0] == 'C':
          self._vfp += 1
        else:
          raise ValueError("action %s does not begin with H, D, or C." % action)

      lastx = self._x
      lasty = self._y

      elementdispatchlist = self._getelementdispatchlist()

      # Movement elements.
      a = action
      while a != "":
        for element in elementdispatchlist:
          if element[0] == a[:len(element[0])]:
            element[1]()
            a = a[len(element[0]):]
            break
        else:
          raise ValueError("unknown element %s in action %s." % (a, action))

      assert aphex.isvalidposition(self._x, self._y)
      assert aphex.isvalidfacing(self._x, self._y, self._facing)
      assert apaltitude.isvalidaltitude(self._altitude)
    
      self._logposition("FP %d" % (self._hfp + self._vfp), action)
      self._drawflightpath(lastx, lasty)

      self.checkforterraincollision()
      self.checkforleavingmap()
      if self._destroyed or self._leftmap:
        return

      # Other elements.
      a = action
      while a != "":
        for element in elementdispatchlist:
          if element[0] == a[:len(element[0])]:
            element[2]()
            a = a[len(element[0]):]
            break
        else:
          raise ValueError("unknown element %s in action %s." % (a, action))

  ##############################################################################

  def _dostalledflight(self, actions):

    altitudechange = math.ceil(self._speed + self._turnsstalled)
    initialaltitude = self._altitude    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
    altitudechange = initialaltitude - self._altitude

    self.checkforterraincollision()

    if self._turnsstalled == 0:
      self._altitudeap = 0.5 * altitudechange
    else:
      self._altitudeap = 1.0 * altitudechange

    if actions == "J1/2":
      self._J("1/2")
    elif actions == "JCL":
      self._J("CL")
      
  ##############################################################################

  def checkforterraincollision(self):
    altitudeofterrain = apaltitude.terrainaltitude()
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._logevent("aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True

  def checkforleavingmap(self):
    if not apmap.iswithinmap(self._x, self._y):
      self._logevent("aircraft has left the map.")
      self._leftmap = True
  
  ##############################################################################

  # Turn management
  
  def _restore(self, i):
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
    self._turnsstalled \
    = self._saved[i]

  def _save(self, i):
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
      self._turnsstalled \
    )

  ##############################################################################

  def _startmovepower(self, power):

    lastpowersetting = self._lastpowersetting

    powerapM  = self._aircrafttype.power(self._configuration, "M")
    powerapAB = self._aircrafttype.power(self._configuration, "AB")

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
    elif not isinstance(power, (int, float)) or power < 0 or power % 0.5 != 0:
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

    # See rule 6.1.
    if powersetting == "I":
      speedchange = self._aircrafttype.power(self._configuration, "I")
      # This keeps the speed non-negative. See rule 6.2.
      speedchange = min(speedchange, self._speed)
      self._log("reducing speed by %.1f as the power setting is IDLE." % speedchange)
      self._speed -= speedchange

    # See rule 6.1.
    if lastpowersetting == "I" and powersetting == "AB" and not self._aircrafttype.hasproperty("RPR"):
      self._log("risk of flame-out as power setting has increased from IDLE to AB.")

    # See rule 6.1.
    if (powersetting == "I" or powersetting == "N") and self._speed > self._aircrafttype.cruisespeed():
      self._log("insufficient power above cruise speed.")
      powerap -= 1.0

    self._log("power is %+.1f AP." % powerap)

    return powersetting, powerap

  ##############################################################################

  def _startmoveflighttype(self, flighttype):

    if flighttype not in ["LV", "SC", "ZC", "VC", "SD", "UD", "VD", "ST"]:
      raise ValueError("invalid flight type %r." % flighttype)

    lastflighttype = self._lastflighttype

    requiredhfp = 0

    # See rule 6.3.
    if self._speed < self._aircrafttype.minspeed(self._configuration, self._altitudeband):

      # TODO: Implement departed flight.
      # See rule 6.4.
      # TODO: Implement a means to jetison stores while stalled.

      self._log("aircraft is stalled.")
      if flighttype != "ST":
        raise ValueError("flight type must be ST.")

      if self._turnsstalled == None:
        self._turnsstalled = 0
      else:
        self._turnsstalled += 1

    elif flighttype == "ST":

      raise ValueError("flight type cannot be ST as the aircraft is not stalled.")

    elif lastflighttype == "ST":

      # See rule 6.4.
      if _isclimbing(flighttype):
        raise ValueError("flight type immediately after ST cannot be climbing.")

      self._turnsstalled = None
   
    else:

      self._turnsstalled = None

      # See rule 5.5.
      if lastflighttype == "LV" and (_isclimbing(flighttype) or _isdiving(flighttype)):
        requiredhfp = 1
      elif (_isclimbing(lastflighttype) and _isdiving(flighttype)) or (_isdiving(lastflighttype) and _isclimbing(flighttype)):
        if self._aircrafttype.hasproperty("HPR"):
          requiredhfp = self._speed // 3
        else:
          requiredhfp = self._speed // 2

    self._log("flight type is %s." % (flighttype))
    if requiredhfp != 0:
      self._log("changing from %s to %s flight so the first %d FPs must be HFPs." % (lastflighttype, flighttype, requiredhfp))

    return flighttype

  ##############################################################################

  def startmove(self, flighttype, power, actions):

    self._log("--- start of move --")

    self._restore(apturn.turn() - 1)

    if self._destroyed or self._leftmap:
      self._endmove()
      return

    self._lastconfiguration = self._configuration
    self._lastpowersetting  = self._powersetting
    self._lastflighttype    = self._flighttype

    self._hfp              = 0
    self._vfp              = 0
    self._spbrfp           = 0

    self._turns            = 0
    self._turnrate         = None
    self._maxturnrate      = None

    self._spbrap           = 0
    self._sustainedturnap  = 0
    self._altitudeap       = 0

    self._altitudeband     = apaltitude.altitudeband(self._altitude)

    self._powersetting, \
    self._powerap          = self._startmovepower(power)
    self._flighttype       = self._startmoveflighttype(flighttype)

    if self._flighttype == "ST":

      self._log("carrying %+.1f APs, and %s altitude levels." % (
        self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))
      
      self._fp      = 0
      self._fpcarry = 0
      
      self._log("speed is %s." % (self._speed))

      if actions != "" and actions != "J1/2" and actions != "JCL":
        raise ValueError("invalid actions %r for flight type ST." % actions)

      self._log("---")
      self._logposition("start", "")
      self._dostalledflight(actions)
      self._logposition("end", "")
      self._log("---")
      self._endmove()

    else:

      self._log("carrying %.1f FPs, %+.1f APs, and %s altitude levels." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))
      
      # See rule 5.4.
      self._fp      = self._speed + self._fpcarry
      self._fpcarry = 0
  
      # See rule 6.6.
      m1 = self._m1()
      if self._speed >= m1:
        speed = "%.1f (SS)" % self._speed
      elif self._speed == m1 - 0.5:
        speed = "%.1f (HT)" % self._speed
      elif self._speed == m1 - 1.0:
        speed = "%.1f (LT)" % self._speed
      else:
        speed = "%.1f" % self._speed
      self._log("speed is %s and %.1f FPs are available." % (speed, self._fp))

      self._log("---")
      self._logposition("start", "")
      self.continuemove(actions)

  def continuemove(self, actions):

    if self._destroyed or self._leftmap or self._flighttype == "ST":
      return
  
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

  def _endmove(self):

    if self._destroyed:
    
      self._log("aircraft has been destroyed.")

    elif self._leftmap:

      self._log("aircraft has left the map.")

    else:

      if self._flighttype != "ST":
        self._log("used %d HFPs, %d VFPs, and %.1f SPBRFPs." % (self._hfp, self._vfp, self._spbrfp))

      if self._lastconfiguration != self._configuration:
        self._log("configuration changed from %s to %s." % (self._lastconfiguration, self._configuration))
      else:
        self._log("configuration is unchanged at %s." % self._configuration)
              
      initialaltitudeband = self._altitudeband
      self._altitudeband = apaltitude.altitudeband(self._altitude)
      if self._altitudeband != initialaltitudeband:
        self._log("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      else:
        self._log("altitude band is unchanged at %s." % self._altitudeband)

      if self._maxturnrate == None:
        self._log("no turns.")
        turnap = 0.0
      else:
        self._log("maximum turn rate is %s." % self._maxturnrate)
        if self._maxturnrate == "EZ":
          turnap = 0.0
        else:
          # TODO: Calculate this at the moment of the maximum turn, since it depends on the configuration.
          turnap = -self._aircrafttype.turndrag(self._configuration, self._maxturnrate)

      self._log("power    APs = %+.1f." % self._powerap)
      self._log("turn     APs = %+.1f and %+.1f." % (turnap, self._sustainedturnap))
      self._log("altitude APs = %+.1f." % self._altitudeap)
      self._log("SPBR     APs = %+.1f." % (self._spbrap))
      ap = self._powerap + self._sustainedturnap + turnap + self._altitudeap + self._spbrap
      self._log("total    APs = %+.1f with %+.1f carry = %+.1f." % (ap, self._apcarry, ap + self._apcarry))
      ap += self._apcarry

      # See rules 6.2 and 6.6.
      initialspeed = self._speed
      if ap < 0:
        aprate = -2.0
      elif self._aircrafttype.hasproperty("RA"):
        if initialspeed >= self._m1():
          aprate = +2.0
        else:
          aprate = +1.5
      else:
        if initialspeed >= self._m1():
          aprate = +3.0
        else:
          aprate = +2.0

      # See rule 6.2 and 6.3
      if ap < 0:
        self._speed -= 0.5 * (ap // aprate)
        self._apcarry = ap % aprate
      else:
        if self._flighttype == "LV" or _isclimbing(self._flighttype):
          maxspeed = self._aircrafttype.maxspeed(self._configuration, self._altitudeband)
        elif _isdiving(self._flighttype) or self._flighttype == "ST":
          maxspeed = self._aircrafttype.maxdivespeed(self._altitudeband)
        if self._speed + 0.5 * (ap // aprate) > maxspeed:
          self._log("speed is limited to %.1f." % maxspeed)
          self._speed = maxspeed
          self._apcarry = aprate - 0.5
        else:
          self._speed += 0.5 * (ap // aprate)
          self._apcarry = ap % aprate

      # See rule 6.3.
      if self._flighttype == "LV" or _isclimbing(self._flighttype):
        maxspeed = self._aircrafttype.maxspeed(self._configuration, self._altitudeband)
        if self._speed > maxspeed:
          self._log("speed is faded back from %.1f." % self._speed)
          self._speed = max(self._speed - 1, maxspeed)
      elif _isdiving(self._flighttype) or self._flighttype == "ST":
        maxspeed = self._aircrafttype.maxdivespeed(self._altitudeband)
        if self._speed > maxspeed:
          self._log("speed is reduced from %.1f to maximum dive speed." % self._speed)
          self._speed = maxspeed

      # See rule 6.2.
      if self._speed <= 0:
        self._speed = 0
        if self._apcarry < 0:
          self._apcarry = 0

      if self._speed != initialspeed:
        self._log("speed changed from %.1f to %.1f." % (initialspeed, self._speed))
      else:
        self._log("speed is unchanged at %.1f." % self._speed)

      if self._flighttype == "ST":
        if self._speed >= self._aircrafttype.minspeed(self._configuration, self._altitudeband):
          self._log("aircraft has exited from stall.")
        else:
          self._log("aircraft is still stalled.")

      # See rule 5.4.
      fp = self._hfp + self._vfp + self._spbrfp
      self._fpcarry = self._fp - fp

      self._log("carrying %.1f FPs, %+.1f APs, and %s altitude levels." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))

    self._save(apturn.turn())

    self._log("--- end of move -- ")
    self._logbreak()

################################################################################

def _isdiving(flighttype):
  return flighttype == "SD" or flighttype == "UD" or flighttype == "VD"

def _isclimbing(flighttype):
  return flighttype == "ZC" or flighttype == "SC" or flighttype == "VC"
