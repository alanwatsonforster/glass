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

  def __init__(self, name, aircrafttype, hexcode, azimuth, altitude, speed):

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
    self._flighttype    = "LV"
    self._fpcarry       = 0
    self._apcarry       = 0
    self._aircrafttype  = apaircrafttype.aircrafttype(aircrafttype)
    self._destroyed     = False
    self._leftmap       = False

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

  def _formatifp(self):
    return "FP %d" % (self._hfp + self._vfp)

  def _log(self, s):
    aplog.log("%s: turn %-2d : %s" % (self._name, apturn.turn(), s))

  def _logbreak(self):
    aplog.logbreak()

  def _logposition(self):
    self._log("%-5s : %-16s : %s" % ("", "", self._formatposition()))

  def _logactionsandposition(self, action):
    self._log("%-5s : %-16s : %s" % (self._formatifp(), action, self._formatposition()))
  
  def _logevent(self, s):
    self._log("%-5s : %s" % (self._formatifp(), s))

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

      ["K"   , lambda : None               , lambda: self._K()],

    ]

  def _doaction(self, action):

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
    
      self._logactionsandposition(action)
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
    self._flighttype, \
    self._fpcarry, \
    self._apcarry, \
    self._destroyed, \
    self._leftmap \
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
      self._flighttype, \
      self._fpcarry, \
      self._apcarry, \
      self._destroyed, \
      self._leftmap, \
    )

  def startmove(self, flighttype, powerap, actions):

    if flighttype not in ["LV", "SC", "ZC", "VC", "SD", "UD", "VD"]:
      raise ValueError("invalid flight type %s." % flighttype)

    # TODO: Don't assume CL.
    powerchart = self._aircrafttype.powerchart("CL")
    if powerap == "IDLE":
      powersetting = "IDLE"
      powerap = 0
    elif powerap == "NOR" or powerap == 0:
      powersetting = "NOR"
      powerap = 0
    elif powerap == "MIL" or (powerap == "AB" and "AB" in powerchart):
      powersetting = powerap
      powerap = powerchart[powersetting]
    elif not isinstance(powerap, (int, float)) or powerap < 0 or powerap % 0.5 != 0:
      raise ValueError("invalid power AP %s" % powerap)
    elif powerap <= powerchart["MIL"]:
      powersetting = "MIL"
    elif "AB" in powerchart and powerap <= powerchart["AB"]:
      powersetting = "AB"
    else:
      raise ValueError("requested power %s APs exceeds aircraft capability.")

    self._restore(apturn.turn() - 1)

    self._lastflighttype  = self._flighttype
    self._flighttype      = flighttype
    self._fp              = self._speed + self._fpcarry
    self._hfp             = 0
    self._vfp             = 0
    self._spbrfp          = 0
    self._fpcarry         = 0
    self._altitudeband    = apaltitude.altitudeband(self._altitude)
    self._turns           = 0
    self._turnrate        = None
    self._maxturnrate     = None
    self._powerap         = powerap
    self._spbrap          = 0
    self._sustainedturnap = 0
    self._altitudeap      = 0

    self._log("--- start of move --")

    if self._destroyed:
      self._endmove()
      return

    if self._leftmap:
      self._endmove()
      return

    self._log("flight type is %s and power setting is %s (%+.1f APs)." % (self._flighttype, powersetting, powerap))

    self._log("carrying %.1f FPs, %+.1f APs, and %s altitude levels." % (
      self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
    ))

    self._log("min speed is %.1f, cruise speed is %.1f, and max speed is %.1f." % ( 
      self._aircrafttype.minspeed("CL", self._altitudeband),
      self._aircrafttype.cruisespeed(),
      self._aircrafttype.maxspeed("CL", self._altitudeband),
    ))
    self._log("climb speed is %.1f, dive speed is %.1f, and M1 is %.1f." % ( 
      self._aircrafttype.climbspeed(),
      self._aircrafttype.divespeed(self._altitudeband),
      self._m1(),
    ))

    # See rule 6.1.
    if (powersetting == "IDLE" or powersetting == "NOR") and self._speed > self._aircrafttype.cruisespeed():
      self._log("insufficient power above cruise speed.")
      self._powerap -= 1.0
    if powersetting == "IDLE" and self._speed > 0.5:
      self._log("reducing speed by 0.5 as the power setting is idle.")
      self._speed -= 0.5

    m1 = self._m1()
    if self._speed >= m1:
      speed = "%.1f (SSS)" % self._speed
    elif self._speed == m1 - 0.5:
      speed = "%.1f (HTS)" % self._speed
    elif self._speed == m1 - 1.0:
      speed = "%.1f (LTS)" % self._speed
    else:
      speed = "%.1f" % self._speed
    self._log("speed is %s and %.1f FPs are available." % (speed, self._fp))

    self._log("---")
    self._logactionsandposition("")
        
    self.continuemove(actions)

  def continuemove(self, actions):

    if self._destroyed or self._leftmap:
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

      self._log("used %d HFPs, %d VFPs, and %.1f SPBRFPs." % (self._hfp, self._vfp, self._spbrfp))

      if self._maxturnrate == None:
        self._log("no turns.")
        turnap = 0.0
      else:
        self._log("maximum turn rate is %s." % self._maxturnrate)
        if self._maxturnrate == "EZ":
          turnap = 0.0
        else:
          # TODO: Don't assume CL.
          # TODO: Calculate this at the moment of the maximum turn, since it depends on the configuration.
          turnap = -self._aircrafttype.turndragchart("CL")[self._maxturnrate]

      self._log("power    APs = %+.1f." % self._powerap)
      self._log("turn     APs = %+.1f and %+.1f." % (turnap, self._sustainedturnap))
      self._log("altitude APs = %+.1f" % self._altitudeap)
      self._log("SPBR     APs = %+.1f." % (self._spbrap))
      ap = self._powerap + self._sustainedturnap + turnap + self._altitudeap + self._spbrap
      self._log("total    APs = %+.1f with %+.1f carry = %+.1f." % (ap, self._apcarry, ap + self._apcarry))
      ap += self._apcarry

      # See rule 6.2.
      # TODO: rates for RA aircraft.
      initialspeed = self._speed
      if ap < 0:
        aprate = -2.0
      elif initialspeed >= self._m1():
        aprate = +3.0
      else:
        aprate = +2.0
      if ap >= 0:
        self._speed += 0.5 * (ap // aprate)
      else:
        self._speed -= 0.5 * (ap // aprate)
      self._apcarry = ap % aprate

      # See rule 6.2.
      if self._speed <= 0:
        self._speed = 0
        if self._apcarry < 0:
          self._apcarry = 0

      if self._speed != initialspeed:
        self._log("speed changed from %.1f to %.1f." % (initialspeed, self._speed))
      else:
        self._log("speed is unchanged at %.1f." % self._speed)

      initialaltitudeband = self._altitudeband
      self._altitudeband = apaltitude.altitudeband(self._altitude)
      if self._altitudeband != initialaltitudeband:
        self._log("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      else:
        self._log("altitude band is unchanged at %s." % self._altitudeband)

      fp = self._hfp + self._vfp + self._spbrfp
      self._fpcarry = self._fp - fp

      self._log("carrying %.1f FPs, %+.1f APs, and %s altitude levels." % (
        self._fpcarry, self._apcarry, apaltitude.formataltitudecarry(self._altitudecarry)
      ))

    self._save(apturn.turn())

    self._log("--- end of move -- ")
    self._logbreak()
