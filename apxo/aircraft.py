import apxo                as ap
import apxo.aircraftdata   as apaircraftdata
import apxo.altitude       as apaltitude
import apxo.azimuth        as apazimuth
import apxo.closeformation as apcloseformation
import apxo.configuration  as apconfiguration
import apxo.damage         as apdamage
import apxo.draw           as apdraw
import apxo.flight         as apflight
import apxo.flightpath     as apflightpath
import apxo.hex            as aphex
import apxo.hexcode        as aphexcode
import apxo.log            as aplog
import apxo.map            as apmap
import apxo.speed          as apspeed
import apxo.stores         as apstores
import apxo.turnrate       as apturnrate
import apxo.geometry       as apgeometry
import apxo.airtoair       as apairtoair
import apxo.turn           as apturn
import apxo.visualsighting as apvisualsighting

from apxo.normalflight import _isclimbingflight, _isdivingflight, _islevelflight

import re

################################################################################

_aircraftlist = []
_zorder = 0

def _startsetup():
  global _aircraftlist
  global _zorder
  _aircraftlist = []
  _zorder = 0

def _endsetup():
  for a in _aircraftlist:
    a._save(apturn.turn())

def _startturn():
  global _zorder
  _zorder = 0
  for a in _aircraftlist:
    a._restore(apturn.turn() - 1)
    a._finishedmove = False
    a._sightedonpreviousturn = a._sighted
    a._enginesmokingonpreviousturn = a._enginesmoking
    a._sighted = False
    a._identifiedonpreviousturn = a._identified
    a._identified = False
    a._unspecifiedattackresult = 0
    a._flightpath.start(a._x, a._y)
  for a in _aircraftlist:
    apcloseformation.check(a)

def _endturn():
  for a in _aircraftlist:
    if not a._destroyed and not a._leftmap and not a._finishedmove:
      raise RuntimeError("aircraft %s has not finished its move." % a._name)
    if a._unspecifiedattackresult > 0:
      raise RuntimeError("aircraft %s has %d unspecified attack %s." % (
        a._name, a._unspecifiedattackresult, aplog.plural(a._unspecifiedattackresult, "result", "results")
      ))
  for a in _aircraftlist:
    a._speed = a._newspeed
    a._newspeed = None
  for a in _aircraftlist:
    apcloseformation.check(a)
  for a in _aircraftlist:
    a._save(apturn.turn())

def _drawmap():
  for a in _aircraftlist:
    a._flightpath.draw(a._color, a._zorder)
    a._drawaircraft()

##############################################################################

def aslist(withdestroyed=False, withleftmap=False):
  aircraftlist = _aircraftlist
  if not withdestroyed:
    aircraftlist = filter(lambda x: not x._destroyed, aircraftlist)
  if not withleftmap:
    aircraftlist = filter(lambda x: not x._leftmap, aircraftlist)
  return list(aircraftlist)
  
##############################################################################

def _xminforzoom(withdestroyed=False):
  return min([min(a._x, a._flightpath.xmin()) for a in aslist(withdestroyed=withdestroyed)])

def _xmaxforzoom(withdestroyed=False):
  return max([max(a._x, a._flightpath.xmax()) for a in aslist(withdestroyed=withdestroyed)])

def _yminforzoom(withdestroyed=False):
  return min([min(a._y, a._flightpath.ymin()) for a in aslist(withdestroyed=withdestroyed)])

def _ymaxforzoom(withdestroyed=False):
  return max([max(a._y, a._flightpath.ymax()) for a in aslist(withdestroyed=withdestroyed)])

##############################################################################

def fromname(name):
  """
  Look for the aircraft with the given name. Return the aircraft or None if 
  no matching aircraft is found.
  """
  for a in _aircraftlist:
    if a._name == name:
      return a
  return None

#############################################################################

class aircraft:

  #############################################################################

  def __init__(self, name, force, aircrafttype, hexcode, azimuth, altitude, speed,
    configuration="CL",
    fuel=None, bingofuel=None, 
    gunammunition=None, rocketfactors=None, stores=None, 
    paintscheme="unpainted",
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
      if not aphexcode.isvalidhexcode(hexcode):
        raise RuntimeError("the hexcode argument is not valid.")
      if not apazimuth.isvalidazimuth(azimuth):
        raise RuntimeError("the azimuth argument is not valid.")
      if not apaltitude.isvalidaltitude(altitude):
        raise RuntimeError("the altitude argument is not valid.")
      if not apspeed.isvalidspeed(speed):
        raise RuntimeError("the speed argument is not valid.")
      if not apconfiguration.isvalid(configuration):
        raise RuntimeError("the configuration argument is not valid.")
      if not apvisualsighting.isvalidpaintscheme(paintscheme):
        raise RuntimeError("the paintscheme argument is not valid.")
      
      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)
      if not aphex.isvalid(x, y, facing):
        raise RuntimeError("the combination of hexcode and facing are not valid.")

      # In addition to the specified position, azimuth, altitude, speed, and 
      # configuration, aircraft initially have level flight, normal power, and
      # no carries.

      self._logbreak()
      self._logline()
      self._name                       = name
      self._logaction("", "creating aircraft %s." % name)

      self._x                          = x
      self._y                          = y
      self._facing                     = facing
      self._altitude                   = altitude
      self._altitudeband               = apaltitude.altitudeband(self._altitude)
      self._altitudecarry              = 0
      self._speed                      = speed
      self._newspeed                   = None
      self._damageL                    = 0
      self._damageH                    = 0
      self._damageC                    = 0
      self._damageK                    = 0
      self._flighttype                 = "LVL"
      self._powersetting               = "N"
      self._bank                       = None
      self._maneuvertype               = None
      self._maneuversense              = None
      self._maneuverfp                 = 0
      self._maneuverrequiredfp         = 0
      self._maneuverfacingchange       = None
      self._manueversupersonic         = False
      self._fpcarry                    = 0
      self._apcarry                    = 0
      self._gloccheck                  = 0
      self._unloadedrecoveryfp         = -1
      self._ETrecoveryfp               = -1
      self._BTrecoveryfp               = -1
      self._HTrecoveryfp               = -1
      self._TTrecoveryfp               = -1
      self._rollrecoveryfp             = -1
      self._trackingfp                 = 0
      self._climbslope                 = 0
      self._lowspeedliftdeviceselected = False
      self._closeformation             = []
      self._aircraftdata               = apaircraftdata.aircraftdata(aircrafttype)
      if gunammunition is None:
        self._gunammunition            = self._aircraftdata.gunammunition()
      else:
        self._gunammunition            = gunammunition
      if rocketfactors is None:
        self._rocketfactors            = self._aircraftdata.rocketfactors()
      else:
        self._rocketfactors            = rocketfactors
      self._crew                       = self._aircraftdata.crew()
      self._destroyed                  = False
      self._leftmap                    = False
      self._sighted                    = False
      self._identified                 = False
      self._paintscheme                = paintscheme
      self._turnsstalled               = 0
      self._turnsdeparted              = 0
      self._finishedmove               = True
      self._color                      = color
      self._counter                    = counter
      self._force                      = force
      self._enginesmoking              = False

      self._flightpath = apflightpath.flightpath(self._x, self._y)

      self._logaction("", "force         is %s." % force)
      self._logaction("", "type          is %s." % aircrafttype)
      self._logaction("", "position      is %s." % self.position())
      self._logaction("", "speed         is %.1f." % self._speed)

      # Determine the fuel and bingo levels.
    
      if isinstance(fuel, str) and fuel[-1] == "%" and fuel[:-1].isdecimal():
        fuel = float(fuel[:-1]) / 100
        self._logaction("", "fuel          is %3.0f%% of internal capacity." % (fuel * 100))
        fuel *= self.internalfuelcapacity()
      elif fuel is not None and not isinstance(fuel, int|float):
        raise RuntimeError("invalid fuel value %r" % fuel)
      self._fuel = fuel

      if isinstance(bingofuel, str) and bingofuel[-1] == "%" and bingofuel[:-1].isdecimal():
        bingofuel = float(bingofuel[:-1]) / 100 
        self._logaction("", "bingo fuel    is %3.0f%% of internal capacity." % (bingofuel * 100))
        bingofuel *= self.internalfuelcapacity()
      elif bingofuel is not None and not isinstance(bingofuel, int|float):
        raise RuntimeError("invalid bingo fuel value %r" % bingofuel)
      self._bingofuel = bingofuel

      if not self._fuel is None:
        if self._bingofuel is None:
          self._logaction("", "fuel          is %.1f." % self._fuel)
        else:
          self._logaction("", "fuel          is %.1f and bingo fuel is %.1f." % (self._fuel, self._bingofuel)) 

      # Determine the configuration, either explicitly or from the specified
      # stores.

      if stores is None:

        self._stores        = stores
        self._configuration = configuration

      else:

        self._stores = apstores._checkstores(stores)
        if len(self._stores) != 0:
          apstores._showstores(stores, 
            printer=lambda s: self._logaction("", s), 
            fuel=self.externalfuel())

        if self.fuel() is not None and self.fuel() > self.internalfuelcapacity() + self.externalfuelcapacity():
          raise RuntimeError("total fuel exceeds the internal and external capacity.")

      apconfiguration.update(self)
      self._logaction("", "configuration is %s." % self._configuration)

      global _zorder
      _zorder += 1
      self._zorder = _zorder
    
      self._saved = []

      _aircraftlist.append(self)
      
      self._logline()

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

  def name(self):
    """Return the name of the aircraft."""
    return self._name

  #############################################################################

  def force(self):
    """Return the force of the aircraft."""
    return self._force

  #############################################################################

  def x(self):
    """Return the x hex coordinate of the aircraft."""
    return self._x

  #############################################################################

  def y(self):
    """Return the y hex coordinate of the aircraft."""
    return self._y
    
  #############################################################################

  def facing(self):
    """Return the facing of the aircraft in degrees."""
    return self._facing
      
  #############################################################################

  def altitude(self):
    """Return the altitude of the aircraft in whole altitude levels."""
    return self._altitude
      
  #############################################################################

  def speed(self):
    """Return the speed of the aircraft."""
    return self._speed
      
  #############################################################################

  def paintscheme(self):
    """Return the paint scheme of the aircraft."""
    return self._paintscheme
      
  #############################################################################

  def crew(self):
    """Return the crew of the aircraft."""
    return self._crew
    
  #############################################################################

  def enginesmoking(self):
    """Return whether the engine is smoking."""
    return self._enginesmokingonpreviousturn

  #############################################################################

  def position(self):
    """Return a string describing the current position of the aircraft."""
    if apmap.isonmap(self._x, self._y):
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      hexcode = "-------"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%-12s  %-3s  %2d" % (hexcode, azimuth, altitude)

  #############################################################################

  def maneuver(self):
    """Return a string describing the current maneuver of the aircraft."""
    if self._maneuverfacingchange == 60 or self._maneuverfacingchange == 90:
      return "%s%s %d/%d %d" % (self._maneuvertype, self._maneuversense, self._maneuverfp, self._maneuverrequiredfp, self._maneuverfacingchange)
    elif self._maneuvertype != None:
      return "%s%s %d/%d" % (self._maneuvertype, self._maneuversense, self._maneuverfp, self._maneuverrequiredfp)
    elif self._bank != None:
      return "B%s" % self._bank
    else:
      return "WL"

  #############################################################################

  def flighttype(self):
    """Return the flight type of the aircraft."""
    return self._flighttype

  #############################################################################

  def note(self, s):
    """Write a note to the log."""
    self._lognote(s)
    self._logline()

  #############################################################################

  def react(self, action, note=False):

    """
    Return fire, either with fixed guns or articulated guns.
    """

    aplog.clearerror()
    try:

      apturn.checkinturn()
      self._logaction("react", action)

      m = re.compile("AA" + 3 * r"\(([^)]*)\)").match(action)
      if m is None:
        raise RuntimeError("invalid action %r" % action)

      attacktype   = m[1]
      targetname   = m[2]
      result       = m[3]

      if targetname == "":
        target = None
      else:
        target = fromname(targetname)
        if target is None:
          raise RuntimeError("unknown target aircraft %s." % targetname)
        
      apairtoair.react(self, attacktype, target, result)
    
      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  ##############################################################################

  # Visual Sighting

  ##############################################################################

  def issighted(self):
    return apvisualsighting.issighted(self)

  ##############################################################################

  def padlock(self, other, note=False):

    """
    Padlock another aircraft.
    """

    # TODO: Check we are in the visual sighting phase.

    aplog.clearerror()
    try:
      apturn.checkinturn()
      apvisualsighting.padlock(self, other, note=note)
    except RuntimeError as e:
      aplog.logexception(e)

  ##############################################################################

  def attempttosight(self, other, success=None, note=False):

    """
    Attempt to sight another aircraft.
    """

    aplog.clearerror()
    try:
      apturn.checkinturn()
      apvisualsighting.attempttosight(self, other, success=None, note=False)
    except RuntimeError as e:
      aplog.logexception(e)
      
  #############################################################################

  def setsighted(self):
    """Set the aircraft to be sighted regardless."""
    apvisualsighting.setsighted(self)

  #############################################################################

  def setunsighted(self):
    """Set the aircraft to be unsighted regardless."""
    apvisualsighting.unsetsighted(self)

  #############################################################################

  def _maxvisualsightingrange(self):

    """
    Return the maximum visual sighting range of the aircraft.
    """

    return apvisualsighting.maxvisualsightingrange(self)

  #############################################################################

  def _visualsightingrange(self, target):

    """
    Return the visual sighting range for a visual sighting attempt from the 
    aircraft on the target.
    """

    return apvisualsighting.visualsightingrange(self, target)

  #############################################################################

  def _visualsightingcondition(self, target):

    """
    Return a tuple describing the visual sighting condition for a visual
    sighting attempt from the aircraft on the target: a descriptive string,
    a boolean indicating if sighting is possible, and a boolean indicating if
    padlocking is possible.
    """

    return apvisualsighting.visualsightingcondition(self, target)

  #############################################################################

  # Fuel

  #############################################################################

  def fuel(self):
    """Return the current fuel points."""
    return self._fuel

  def internalfuel(self):
    """Return the current internal fuel points."""
    if self.fuel() is None:
      return None
    else:
      return min(self.fuel(), self.internalfuelcapacity())

  def externalfuel(self):
    """Return the current external fuel points."""
    if self.fuel() is None:
      return None
    else:
      return max(0, self.fuel() - self.internalfuelcapacity())

  def internalfuelcapacity(self):
    """Return the internal fuel capacity."""
    return self._aircraftdata.internalfuelcapacity()
    
  def externalfuelcapacity(self):
    """Return the external fuel capacity."""
    return apstores.totalfuelcapacity(self._stores)

  #############################################################################

  # Stores

  #############################################################################

  def showstores(self, note=False):
    """
    Show the aircraft's stores to the log.
    """

    aplog.clearerror()
    try:

      apturn.checkinsetuporturn()
      self._logbreak()
      self._logline()

      apstores._showstores(self._stores, 
        printer=lambda s: self._log(s),
        fuel=self.externalfuel())
  
      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

  # Geometry
  
  #############################################################################

  def showgeometry(self, other, note=False):

    """
    Show the geometry of the other aircraft with respect to the aircraft.
    """

    aplog.clearerror()
    try:
      apturn.checkinturn()
      showgeometry(self, other, note=False)
    except RuntimeError as e:
      aplog.logexception(e)
      
  #############################################################################

  def _angleofftail(self, other, **kwargs):

    """
    Return the angle of the aircraft off the tail of the other aircraft.
    """

    return apgeometry.angleofftail(self, other, **kwargs)

  #############################################################################

  def _inarc(self, other, arc):

    """
    Return True if the other aircraft is in the specified arc of the aircraft.
    Otherwise, return False.
    """

    return apgeometry.inarc(self, other, arc)
    
  #############################################################################

  def _inradararc(self, other, arc):

    """
    Return True if the other aircraft is in the specified radar arc of the 
    aircraft. Otherwise, return False.
    """

    return apgeometry.inradararc(self, other, arc)
    
  #############################################################################

  def _gunattackrange(self, other, arc=False):

    """
    Return the gun attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return apairtoair.gunattackrange(self, other, arc=arc)

  #############################################################################

  def _rocketattackrange(self, other):

    """
    Return the rocket attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return apairtoair.rocketattackrange(self, other)

  #############################################################################

  def _inlimitedradararc(self, other):

    """
    Return True if the other aircraft is in the limited radar arc of the aircraft.
    """

    return apgeometry.inradararc(self, other, "limited")
    
  #############################################################################

  def isinclimbingflight(self, vertical=False):

    """
    Return true if the aircraft is climbing.
    """

    return _isclimbingflight(self._flighttype, vertical=vertical)

  #############################################################################

  def isindivingflight(self, vertical=False):

    """
    Return true if the aircraft is diving.
    """

    return _isdivingflight(self._flighttype, vertical=vertical)
   
  #############################################################################

  def isinlevelflight(self):

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
      self._logaction("", "aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True
      apcloseformation.leaveany(self)

  def checkforleavingmap(self):

    """
    Check if the aircraft has left the map.
    """

    if not apmap.isonmap(self._x, self._y):
      self._logaction("", "aircraft has left the map.")
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
    self._stores, \
    self._gunammunition, \
    self._fuel, \
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
    self._fpcarry, \
    self._apcarry, \
    self._gloccheck, \
    self._unloadedrecoveryfp, \
    self._ETrecoveryfp, \
    self._BTrecoveryfp, \
    self._HTrecoveryfp, \
    self._TTrecoveryfp, \
    self._rollrecoveryfp, \
    self._climbslope, \
    self._lowspeedliftdeviceselected, \
    self._closeformation, \
    self._destroyed, \
    self._leftmap, \
    self._sighted, \
    self._identified, \
    self._turnsstalled, \
    self._turnsdeparted, \
    self._enginesmoking \
    = self._saved[i]
    self._altitudeband = apaltitude.altitudeband(self._altitude)

    self._startx             = self._x
    self._starty             = self._y
    self._startaltitude      = self._altitude
    self._startfacing        = self._facing
    self._startspeed         = self._speed
    self._startfpcarry       = self._fpcarry
    self._startapcarry       = self._apcarry
    self._startaltitudecarry = self._altitudecarry
    self._startmaneuvertype  = self._maneuvertype
    self._startmaneuversense = self._maneuversense
    self._startmaneuverfp    = self._maneuverfp

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
      self._stores, \
      self._gunammunition, \
      self._fuel, \
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
      self._fpcarry, \
      self._apcarry, \
      self._gloccheck, \
      self._unloadedrecoveryfp, \
      self._ETrecoveryfp, \
      self._BTrecoveryfp, \
      self._HTrecoveryfp, \
      self._TTrecoveryfp, \
      self._rollrecoveryfp, \
      self._climbslope, \
      self._lowspeedliftdeviceselected, \
      self._closeformation, \
      self._destroyed, \
      self._leftmap, \
      self._sighted, \
      self._identified, \
      self._turnsstalled, \
      self._turnsdeparted, \
      self._enginesmoking \
    )

 ################################################################################

  def hasbeenkilled(self):
    apturn.checkinturn()
    self._log("has been killed.")
    self._destroyed = True
    self._color = None

  ################################################################################

  def _assert(self, expectedposition, expectedspeed, expectedconfiguration=None):

    """
    Verify the position and new speed of an aircraft.
    """

    if aplog._error != None:
      print("== assertion failed ===")
      print("== unexpected error: %r" % aplog._error)
      assert aplog._error == None

    expectedposition = re.sub(" +", " ", expectedposition)
    actualposition   = re.sub(" +", " ", self.position())

    if expectedposition != None and expectedposition != actualposition:
      print("== assertion failed ===")
      print("== actual   position: %s" % actualposition)
      print("== expected position: %s" % expectedposition)
      assert expectedposition == actualposition
    if expectedspeed is not None:
      if self._newspeed is None:
        if expectedspeed != self._speed:
          print("== assertion failed ===")
          print("== actual   speed: %.1f" % self._speed)
          print("== expected speed: %.1f" % expectedspeed)
          assert expectedspeed == self._speed
      else:
        if expectedspeed != self._newspeed:
          print("== assertion failed ===")
          print("== actual   new speed: %.1f" % self._newspeed)
          print("== expected new speed: %.1f" % expectedspeed)
          assert expectedspeed == self._newspeed
    if expectedconfiguration != None and expectedconfiguration != self._configuration:
      print("== assertion failed ===")
      print("== actual   configuration: %s" % self._configuration)
      print("== expected configuration: %s" % expectedconfiguration)
      assert expectedconfiguration == self._configuration

  ################################################################################

  def _drawaircraft(self):
    if self._leftmap:
      return
    if self._destroyed:
      color = None
    else:
      color = self._color
    apdraw.drawaircraft(self._x, self._y, self._facing, color, self._name, self._altitude, self._zorder)

  ################################################################################  

  def _startmovespeed(self, power, flamedoutengines, lowspeedliftdeviceselected):
    apspeed.startmovespeed(self, power, flamedoutengines, lowspeedliftdeviceselected)

  def _endmovespeed(self):
    apspeed.endmovespeed(self)

  ################################################################################  

  def joincloseformation(self, other):
    aplog.clearerror()
    try:
      apcloseformation.join(self, other)
    except RuntimeError as e:
      aplog.logexception(e)

  def leavecloseformation(self):
    aplog.clearerror()
    try:    
      apcloseformation.leave(self)
    except RuntimeError as e:
      aplog.logexception(e)

  def closeformationsize(self):
    return apcloseformation.size(self)
    
  def closeformationnames(self):
    return apcloseformation.names(self)

  ################################################################################  

  def move(self, *args, **kwargs):
    aplog.clearerror()
    try:
      apflight.move(self, *args, **kwargs)
    except RuntimeError as e:
      aplog.logexception(e)

  def continuemove(self, *args, **kwargs):
    aplog.clearerror()
    try:
        apflight.continuemove(self, *args, **kwargs)
    except RuntimeError as e:
      aplog.logexception(e)

  ################################################################################  
 
  def takedamage(self, damage, note=False):
    aplog.clearerror()
    try:    
      apdamage.takedamage(self, damage)
      self._lognote(note)
      self._logline()
    except RuntimeError as e:
      aplog.logexception(e)
      
  def damage(self):
    return apdamage.damage(self)

  def damageatleast(self, damage):
    return apdamage.damageatleast(self, damage)

  def damageatmost(self, damage):
    return apdamageatmost(self, damage)

  ################################################################################

  def _logbreak(self):
    aplog.logbreak()
    
  def _log(self, s):
    aplog.log("%-4s : %s" % (self._name, s))

  def _logline(self):
    aplog.log("%-4s : %s :" % ("----", "-----"))
      
  def _log1(self, s, t):
    self._log("%-5s : %s" % (s, t))

  def _log2(self, s, t):
    self._log("%-5s : %-32s : %s" % (s, "", t))

  def _logposition(self, s):
    self._log1(s, self.position())

  def _logpositionandmaneuver(self, s):
    self._log1(s, "%s  %s" % (self.position(), self.maneuver()))

  def _logaction(self, s, t):
    self._log1(s, t)

  def _logevent(self, s):
    self._log2("", s)

  def _logstart(self, s):
    self._log1("start", s)

  def _logend(self, s):
    self._log1("end", s)

  def _lognote(self, note):
    aplog.lognote(self, note)
    
  ################################################################################

  def reportmove(self):

    print()
    print("Game Turn                : %d " % apturn.turn())
    print("Aircraft name            : %s" % self._name)
    if apmap.isonmap(self._startx, self._starty):
      position = aphexcode.fromxy(self._startx, self._starty)
    else:
      position = "not on map"
    print("Start position           : %s" % position)
    print("Start facing             : %s" % apazimuth.fromfacing(self._startfacing))
    print("Start altiude            : %d" % self._startaltitude)
    print("Start speed              : %.1f" % self._speed)
    print("Start FP carry           : %.1f" % self._startfpcarry)
    print("Start AP carry           : %.2f" % self._startapcarry)
    print("Start altitude carry     : %.2f" % self._startaltitudecarry)
    if self._startmaneuvertype != None and self._startmaneuverfp != 0:
      print("Start turn/maneuver carry: %d%s%s" % (self._startmaneuverfp, self._startmaneuvertype, self._startmaneuversense))
    else:
      print("Start turn/maneuver carry: none")
    print("Flight type              : %s%s" % (self._flighttype, "/HRD" if self._hrd else ""))
    print("Power setting            : %s" % self._powersetting)
    print("Actions                  : %s" % self._actions)
    print("Conventional actions     : %s" % self._conventionalactions)

    if apmap.isonmap(self._x, self._y):
      position = aphexcode.fromxy(self._x, self._y)
    else:
      position = "not on map"
    print("End position             : %s" % position)
    print("End facing               : %s" % apazimuth.fromfacing(self._facing))
    print("End altiude              : %d" % self._altitude)
    if self._bank == None:
      print("End bank                 : WL")
    else:
      print("End bank                 : B%s" % self._bank)
    print("Power                APs : %+.2f" % self._powerap)
    print("Speed                APs : %+.2f" % self._speedap)
    print("Altitude             APs : %+.2f" % self._altitudeap)
    print("Turns                APs : %+.2f" % self._turnsap)
    print("Other maneuvers      APs : %+.2f" % self._othermaneuversap)
    print("Speedbrakes          APs : %+.2f" % self._spbrap)
    print("Carry                APs : %+.2f" % self._startapcarry)
    ap = \
      self._powerap + \
      self._speedap + \
      self._altitudeap + \
      self._turnsap + \
      self._othermaneuversap + \
      self._spbrap + \
      self._startapcarry
    print("Total                APs : %+.2f" % ap)
    print("End speed                : %.1f" % self._newspeed)
    print("End FP carry             : %.1f" % self._fpcarry)
    print("End AP carry             : %+.2f" % self._apcarry)
    print("End altitude carry       : %+.2f" % self._altitudecarry)
    if self._maneuvertype != None and self._maneuverfp != 0:
      print("End turn/maneuver carry  : %d%s%s" % (self._maneuverfp, self._maneuvertype, self._maneuversense))
    else:
      print("End turn/maneuver carry  : none")

  ################################################################################

