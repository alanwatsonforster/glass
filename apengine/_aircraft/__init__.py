import apengine                as ap
import apengine._aircraftdata  as apaircraftdata
import apengine._altitude      as apaltitude
import apengine._azimuth       as apazimuth
import apengine._configuration as apconfiguration
import apengine._draw          as apdraw
import apengine._hex           as aphex
import apengine._hexcode       as aphexcode
import apengine._log           as aplog
import apengine._map           as apmap
import apengine._speed         as apspeed
import apengine._turnrate      as apturnrate

import math

################################################################################

_aircraftlist = []

def _startsetup():
  global _aircraftlist
  global _zorder
  _aircraftlist = []
  _zorder = 0

def _endsetup():
  for a in _aircraftlist:
    a._save(ap.turn())

def _startturn():
  global _zorder
  _zorder = 0
  for a in _aircraftlist:
    a._restore(ap.turn() - 1)
    a._finishedmove = False
    a._startflightpath()
  for a in _aircraftlist:
    a._checkcloseformation()

def _endturn():
  for a in _aircraftlist:
    if not a._destroyed and not a._leftmap and not a._finishedmove:
      raise RuntimeError("aircraft %s has not finished its move." % a._name)
  for a in _aircraftlist:
    a._speed = a._newspeed
    a._newspeed = None
  for a in _aircraftlist:
    a._checkcloseformation()
  for a in _aircraftlist:
    a._save(ap.turn())

def _drawmap():
  for a in _aircraftlist:
    a._drawflightpath()
    a._drawaircraft()

def _fromname(name):
  for a in _aircraftlist:
    if a._name == name:
      return a
  return None

#############################################################################

from ._draw import \
  _zorder

from ._geometry import \
  _showgeometry, _angleofftail, _gunattackrange, _rocketattackrange, _inlimitedradararc

from ._normalflight import \
  _isclimbingflight, _isdivingflight, _islevelflight
    
class aircraft:

  from ._closeformation import \
    joincloseformation, leavecloseformation, \
    _checkcloseformation, _leaveanycloseformation, _breakdowncloseformation, \
    closeformationsize, closeformationnames

  from ._flight import \
    move, continuemove, _endmove

  from ._stalledflight import \
    _checkstalledflight, _dostalledflight

  from ._departedflight import \
    _checkdepartedflight, _dodepartedflight

  from ._normalflight import \
    _checknormalflight, \
    _startnormalflight, _continuenormalflight, _endnormalflight

  from ._specialflight import \
    _checkspecialflight, _dospecialflight

  from ._speed import \
    _startmovespeed, _endmovespeed

  from ._damage import \
    damage, takedamage

  from ._flightcapabilities import \
    power, spbr, fuelrate, powerfade, engines, turndrag, \
    minspeed, maxspeed, cruisespeed, climbspeed, maxdivespeed, ceiling, \
    rollhfp, rolldrag, climbcapability, hasproperty, \
    specialclimbcapability

  from ._draw import \
    _drawaircraft, \
    _startflightpath, _continueflightpath, _drawflightpath

  from ._log import \
    _log, _logaction, _logevent, _logbreak

  #############################################################################

  def __init__(self, name, aircrafttype, hexcode, azimuth, altitude, speed, configuration,
    color="unpainted", counter=False
  ):

    global _aircraftlist

    aplog.clearerror()
    try:

      if not isinstance(name, str):
        raise RuntimeError("the name argument must be a string.")
      for a in _aircraftlist:
        if name == a._name:
          raise RuntimeError("the name argument must be unique.")

      if not isinstance(aircrafttype, str):
        raise RuntimeError("the aircrafttype argument must be a string.")
      # Require the hexcode to be a string to avoid surprised with things like 2020/2120 rather than "2020/2120".
      if not isinstance(hexcode, str):
        raise RuntimeError("the hexcode argument must be a string.")
      if not aphexcode.isvalidhexcode(hexcode):
        raise RuntimeError("the hexcode argument is not valid.")
      if not apazimuth.isvalidazimuth(azimuth):
        raise RuntimeError("the azimuth argument is not valid.")
      if not apaltitude.isvalidaltitude(altitude):
        raise RuntimeError("the altitude argument is not valid.")
      if not apspeed.isvalidspeed(speed):
        raise RuntimeError("the speed argument is not valid.")
      if not apconfiguration.isvalidconfiguration(configuration):
        raise RuntimeError("the configuration argument is not valid.")

      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)
      if not aphex.isvalid(x, y, facing):
        raise RuntimeError("the combination of hexcode and facing are not valid.")

      # In addition to the specified position, azimuth, altitude, speed, and 
      # configuration, aircraft initially have level flight, normal power, and
      # no carries.

      self._name                  = name
      self._x                     = x
      self._y                     = y
      self._facing                = facing
      self._altitude              = altitude
      self._altitudeband          = apaltitude.altitudeband(self._altitude)
      self._altitudecarry         = 0
      self._speed                 = speed
      self._newspeed              = None
      self._configuration         = configuration
      self._damageL               = 0
      self._damageH               = 0
      self._damageC               = 0
      self._damageK               = 0
      self._flighttype            = "LVL"
      self._powersetting          = "N"
      self._bank                  = None
      self._maneuvertype          = None
      self._maneuversense         = None
      self._maneuverfp            = 0
      self._maneuverrequiredfp    = 0
      self._maneuverfacingchange  = None
      self._manueversupersonic    = False
      self._wasrollingonlastfp    = False
      self._fpcarry               = 0
      self._apcarry               = 0
      self._gloccheck             = 0
      self._closeformation        = []
      self._aircraftdata          = apaircraftdata.aircraftdata(aircrafttype)
      self._destroyed             = False
      self._leftmap               = False
      self._turnsstalled          = 0
      self._turnsdeparted         = 0
      self._finishedmove          = True
      self._flightpathx           = []
      self._flightpathy           = []
      self._color                 = color
      self._counter               = counter

      global _zorder
      _zorder += 1
      self._zorder = _zorder
    
      self._saved = []

      _aircraftlist.append(self)

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

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
      ["gloccheck"    , self._gloccheck],
      ["altitudecarry", self._altitudecarry],
      ["destroyed"    , self._destroyed],
      ["leftmap"      , self._leftmap],
    ]:
      s += "%-16s: %s\n" % (x[0], x[1])
    return s

  #############################################################################

  def position(self):

    if apmap.isonmap(self._x, self._y):
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      hexcode = "----"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%-9s  %-3s  %2d" % (hexcode, azimuth, altitude)

  #############################################################################

  def maneuver(self):
    if self._maneuverfacingchange == 60 or self._maneuverfacingchange == 90:
      return "%s%s %d/%d %d" % (self._maneuvertype, self._maneuversense, self._maneuverfp, self._maneuverrequiredfp, self._maneuverfacingchange)
    elif self._maneuvertype != None:
      return "%s%s %d/%d" % (self._maneuvertype, self._maneuversense, self._maneuverfp, self._maneuverrequiredfp)
    elif self._bank != None:
      return "BK%s" % self._bank
    else:
      return "WL"

  #############################################################################

  def returnfire(self, target, arc=False):

    """
    Return fire, either with fixed guns or articulated guns.
    """

    aplog.clearerror()
    try:

      if arc:

        self._logevent("- %s returning fire: air-to-air attack on %s using articulated guns covering %s arc." % (self._name, target._name, arc))
  
        r = self.gunattackrange(target, arc=arc)
        if isinstance(r, str):
          raise RuntimeError(r)

        self._logevent("- %s returning fire: range is %d." % (self._name, r)      )
        self._logevent("- %s returning fire: angle-off-tail of %s is %s." % (self._name, self._name, target.angleofftail(self)))  
        
      else:
        
        self._log("- returning fire: air-to-air attack on %s using fixed guns." % target._name)

        r = self.gunattackrange(target)
        if isinstance(r, str):
          raise RuntimeError(r)
        angleofftail = self.angleofftail(target)
        if angleofftail != "180 line":
          raise RuntimeError("fixed guns can only return fire to head-on attacks.")

        self._log("- returning fire: range is %d." % r)      
        self._log("- returning fire: angle-off-tail is %s." % angleofftail)   

    except RuntimeError as e:
      aplog.logexception(e)
    
  #############################################################################

  def angleofftail(self, other):

    """
    Return the angle of the aircraft off the tail of the other aircraft.
    """

    return _angleofftail(self, other)

  #############################################################################

  def gunattackrange(self, other, arc=False):

    """
    Return the gun attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return _gunattackrange(self, other, arc=arc)

  #############################################################################

  def rocketattackrange(self, other):

    """
    Return the rocket attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return _rocketattackrange(self, other)

  #############################################################################

  def inlimitedradararc(self, other):

    """
    Return True if the other aircraft is in the limited radar arc of the aircraft.
    """

    return _inlimitedradararc(self, other)
    
  #############################################################################
  
  def showgeometry(self, other):

    """
    Show the geometry of the other aircraft with respect to the aircraft.
    """

    _showgeometry(self, other)
  
  #############################################################################

  def climbingflight(self):

    """
    Return true if the aircraft is climbing.
    """

    return _isclimbingflight(self._flighttype)

  #############################################################################

  def divingflight(self):

    """
    Return true if the aircraft is diving.
    """

    return _isdivingflight(self._flighttype)
   
  #############################################################################

  def levelflight(self):

    """
    Return true if the aircraft is in level flight.
    """

    return _islevelflight(self._flighttype)
    
  #############################################################################

  def checkforterraincollision(self):

    """
    Check if the aircraft has collided with terrain.
    """

    altitudeofterrain = apaltitude.terrainaltitude(self._x, self._y)
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._logevent("aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True
      self._leaveanycloseformation()

  def checkforleavingmap(self):

    """
    Check if the aircraft has left the map.
    """

    if not apmap.isonmap(self._x, self._y):
      self._logevent("aircraft has left the map.")
      self._leftmap = True
      self._leaveanycloseformation()
  
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
    self._damageL, \
    self._damageH, \
    self._damageC, \
    self._damageK, \
    self._powersetting, \
    self._flighttype, \
    self._bank, \
    self._maneuvertype, \
    self._maneuversense, \
    self._maneuverfp, \
    self._maneuverrequiredfp, \
    self._maneuverfacingchange, \
    self._manueversupersonic, \
    self._wasrollingonlastfp, \
    self._fpcarry, \
    self._apcarry, \
    self._gloccheck, \
    self._closeformation, \
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
      self._damageL, \
      self._damageH, \
      self._damageC, \
      self._damageK, \
      self._powersetting, \
      self._flighttype, \
      self._bank, \
      self._maneuvertype, \
      self._maneuversense, \
      self._maneuverfp, \
      self._maneuverrequiredfp, \
      self._maneuverfacingchange, \
      self._manueversupersonic, \
      self._wasrollingonlastfp, \
      self._fpcarry, \
      self._apcarry, \
      self._gloccheck, \
      self._closeformation, \
      self._destroyed, \
      self._leftmap, \
      self._turnsstalled, \
      self._turnsdeparted \
    )

 ################################################################################

  def hasbeenkilled(self):
    ap._checkinturn()
    self._log("has been killed.")
    self._destroyed = True

  ################################################################################

  def _assert(self, position, speed, configuration=None):

    """
    Verify the position and new speed of an aircraft.
    """

    if aplog._error != None:
      print("== assertion failed ===")
      print("== unexpected error: %r" % aplog._error)
      assert aplog._error == None
    if position != None and position != self.position():
      print("== assertion failed ===")
      print("== actual position  : %s" % self.position())
      print("== expected position: %s" % position)
      assert position == self.position()
    if speed is not None:
      if self._newspeed is None:
        if speed != self._speed:
          print("== assertion failed ===")
          print("== actual   speed: %.1f" % self._speed)
          print("== expected speed: %.1f" % speed)
          assert speed == self._speed
      else:
        if speed != self._newspeed:
          print("== assertion failed ===")
          print("== actual   new speed: %.1f" % self._newspeed)
          print("== expected new speed: %.1f" % newspeed)
          assert speed == self._newspeed
    if configuration != None and configuration != self._configuration:
      print("== assertion failed ===")
      print("== actual speed  : %s" % self._configuration)
      print("== expected speed: %s" % configuration)
      assert configuration == self._configuration

  ################################################################################  
