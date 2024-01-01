import apxo                as ap
import apxo.aircraftdata   as apaircraftdata
import apxo.altitude       as apaltitude
import apxo.azimuth        as apazimuth
import apxo.configuration  as apconfiguration
import apxo.draw           as apdraw
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

import re

################################################################################

_aircraftlist = []

def _startsetup():
  global _aircraftlist
  global _zorder
  _aircraftlist = []
  _zorder = 0

def _endsetup():
  for a in _aircraftlist:
    a._save(apturn.turn())

def aslist(withdestroyed=False, withleftmap=False):
  alist = _aircraftlist
  if not withdestroyed:
    alist = filter(lambda x: not x._destroyed, alist)
  if not withleftmap:
    alist = filter(lambda x: not x._leftmap, alist)
  return list(alist)

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
    a._startflightpath()
  for a in _aircraftlist:
    a._checkcloseformation()

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
    a._checkcloseformation()
  for a in _aircraftlist:
    a._save(apturn.turn())

def _drawmap():
  for a in _aircraftlist:
    a._drawflightpath()
    a._drawaircraft()

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

from .draw import \
  _zorder

from .normalflight import \
  _isclimbingflight, _isdivingflight, _islevelflight
    
class aircraft:

  from .closeformation import \
    joincloseformation, leavecloseformation, \
    _checkcloseformation, _leaveanycloseformation, _breakdowncloseformation, \
    closeformationsize, closeformationnames

  from .flight import \
    move, continuemove, _endmove

  from .stalledflight import \
    _checkstalledflight, _dostalledflight

  from .departedflight import \
    _checkdepartedflight, _dodepartedflight

  from .normalflight import \
    _checknormalflight, \
    _startnormalflight, _continuenormalflight, _endnormalflight

  from .specialflight import \
    _checkspecialflight, _dospecialflight

  from .speed import \
    _startmovespeed, _endmovespeed

  from .configuration import \
    _updateconfiguration

  from .damage import \
    damage, _takedamage, takedamage, damageatleast, damageatmost

  from .flightcapabilities import \
    power, spbr, fuelrate, powerfade, engines, turndrag, \
    minspeed, maxspeed, cruisespeed, climbspeed, maxdivespeed, ceiling, \
    lowspeedliftdevicename, lowspeedliftdevicelimit, lowspeedliftdeviceselectable, \
    rollhfp, rolldrag, climbcapability, hasproperty, \
    specialclimbcapability, gunarc, \
    visibility, blindarcs, restrictedarcs

  from .draw import \
    _drawaircraft, \
    _startflightpath, _continueflightpath, _drawflightpath

  from .log import \
    _log, _logaction, _logstart, _logend, _logevent, _logline, _logbreak, \
    _lognote, _log1, _log2, \
    _logpositionandmaneuver, _logposition

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
      self._wasrollingonlastfp         = False
      self._fpcarry                    = 0
      self._apcarry                    = 0
      self._gloccheck                  = 0
      self._ETrecoveryfp               = -1
      self._BTrecoveryfp               = -1
      self._HTrecoveryfp               = -1
      self._TTrecoveryfp               = -1
      self._rollrecoveryfp             = -1
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
      self._flightpathx                = []
      self._flightpathy                = []
      self._color                      = color
      self._counter                    = counter
      self._force                      = force
      self._enginesmoking              = False

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

      self._updateconfiguration()
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
    """Return the altitude of the aircraft in altitude levels."""
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
    """Return whether the engine was smoking."""
    return self._enginesmokingonpreviousturn

  #############################################################################

  def position(self):

    if apmap.isonmap(self._x, self._y):
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      hexcode = "-------"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%-12s  %-3s  %2d" % (hexcode, azimuth, altitude)

  #############################################################################

  def maneuver(self):
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

      weapon     = m[1]
      targetname = m[2]
      result     = m[3]

      if targetname == "":
        target = None
      else:
        target = fromname(targetname)
        if target is None:
          raise RuntimeError("unknown target aircraft %s." % targetname)
        
      apairtoair.react(self, weapon, target, result)
    
      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)
    
  #############################################################################

  def angleofftail(self, other, **kwargs):

    """
    Return the angle of the aircraft off the tail of the other aircraft.
    """

    return apgeometry.angleofftail(self, other, **kwargs)

  #############################################################################

  def gunattackrange(self, other, arc=False):

    """
    Return the gun attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return apairtoair.gunattackrange(self, other, arc=arc)

  #############################################################################

  def rocketattackrange(self, other):

    """
    Return the rocket attack range of the other aircraft from the aircraft
    or a string explaining why it cannot be attacked.
    """

    return apairtoair.rocketattackrange(self, other)

  #############################################################################

  def inlimitedradararc(self, other):

    """
    Return True if the other aircraft is in the limited radar arc of the aircraft.
    """

    return apgeometry.inlimitedradararc(self, other)
    
  #############################################################################

  def maxvisualsightingrange(self):

    """
    Return the maximum visual sighting range of the aircraft.
    """

    return apvisualsighting.maxvisualsightingrange(self)

  #############################################################################

  def visualsightingrange(self, target):

    """
    Return the visual sighting range for a visual sighting attempt from the 
    aircraft on the target.
    """

    return apvisualsighting.visualsightingrange(self, target)

  #############################################################################

  def visualsightingcondition(self, target):

    """
    Return a tuple describing the visual sighting condition for a visual
    sighting attempt from the aircraft on the target: a descriptive string,
    a boolean indicating if sighting is possible, and a boolean indicating if
    padlocking is possible.
    """

    return apvisualsighting.visualsightingcondition(self, target)

  ##############################################################################

  def sighted(self):
    return self._sighted

  ##############################################################################

  def padlocks(self, target, note=False):

    aplog.clearerror()
    try:

      apturn.checkinturn()
      self._logbreak()
      self._logline()

      self._log("padlocks %s." % target.name())

      if not target._sightedonpreviousturn:
        raise RuntimeError("%s was not sighted on previous turn." % (target.name()))

      self._logevent("range is %d." % apvisualsighting.visualsightingrange(self, target))
      self._logevent("%s." % apvisualsighting.visualsightingcondition(self, target)[0])

      condition, cansight, canpadlock, restricted = apvisualsighting.visualsightingcondition(self, target)
      if not canpadlock:
        raise RuntimeError("%s cannot padlock %s." % (self.name(), target.name()))

      target._sighted = True
      target._identified = target._identifiedonpreviousturn or apvisualsighting.canidentify(self, target)
      if target._identified:
        self._log("%s is sighted and identified." % target.name())
      else:
        self._log("%s is sighted but not identified." % target.name())

      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  ##############################################################################

  def attemptstosight(self, target, success=None, note=False):

    aplog.clearerror()
    try:

      apturn.checkinturn()
      self._logbreak()
      self._logline()

      self._log("attempts to sight %s." % target.name())
      self._logevent("range is %d." % apvisualsighting.visualsightingrange(self, target))
      self._logevent("%s." % apvisualsighting.visualsightingcondition(self, target)[0])
      
      condition, cansight, canpadlock, restricted = apvisualsighting.visualsightingcondition(self, target)
      if not cansight:
        raise RuntimeError("%s cannot sight %s." % (self.name(), target.name()))

      allrestricted = restricted

      additionalsearchers = 0
      for searcher in aslist():
        if searcher.name() != self.name() and searcher.force() == self.force():
          condition, cansight, canpadlock, restricted = apvisualsighting.visualsightingcondition(searcher, target)
          self._logevent("additional searcher %s: %s." % (searcher.name(), condition))
          if cansight:
            additionalsearchers += 1
            allrestricted = allrestricted and restricted
      if additionalsearchers == 0:
        self._logevent("no additional searchers.")
      else:
        self._logevent("%d additional %s." % (additionalsearchers, aplog.plural(additionalsearchers, "searcher", "searchers")))

      modifier = 0

      dmodifier = apvisualsighting.visualsightingrangemodifier(self, target)
      self._logevent("range modifier        is %+d." % dmodifier)
      modifier += dmodifier

      dmodifier = apvisualsighting.visualsightingallrestrictedmodifier(allrestricted)
      self._logevent("restricted modifier   is %+d." % dmodifier)
      modifier += dmodifier

      dmodifier = apvisualsighting.visualsightingsearchersmodifier(additionalsearchers + 1)
      self._logevent("searchers modifier    is %+d." % dmodifier)
      modifier += dmodifier

      dmodifier = apvisualsighting.visualsightingpaintschememodifier(self, target)
      self._logevent("paint-scheme modifier is %+d." % dmodifier)
      modifier += dmodifier

      dmodifier = apvisualsighting.visualsightingcrewmodifier(self)
      if dmodifier != 0:
        self._logevent("crew modifier         is %+d." % dmodifier)

      dmodifier = apvisualsighting.visualsightingsmokingmodifier(self, target)
      if dmodifier != 0:
        self._logevent("smoking modifier      is %+d." % dmodifier)
      modifier += dmodifier

      self._logevent("total modifier        is %+d." % modifier)
      self._logevent("target visibility is %d." % target.visibility())

      self._lognote(note)

      if success is False:
        self._log("%s is unsighted." % target.name())
      elif success is True:
        target._sighted = True
        target._identified = target._identifiedonpreviousturn or apvisualsighting.canidentify(self, target)
        if target._identified:
          self._log("%s is sighted and identified." % target.name())
        else:
          self._log("%s is sighted but not identified." % target.name())

      self._logline()
    
    except RuntimeError as e:
      aplog.logexception(e)
      
  #############################################################################

  def fuel(self):
    return self._fuel

  def internalfuel(self):
    if self.fuel() is None:
      return None
    else:
      return min(self.fuel(), self.internalfuelcapacity())

  def externalfuel(self):
    if self.fuel() is None:
      return None
    else:
      return max(0, self.fuel() - self.internalfuelcapacity())

  def externalfuelcapacity(self):
    return apstores.totalfuelcapacity(self._stores)

  def internalfuelcapacity(self):
    return self._aircraftdata.internalfuelcapacity()

  #############################################################################

  def showstores(self, note=False):
    """
    Show the aircraft's stores.
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
  
  def showgeometry(self, other, note=False):

    """
    Show the geometry of the other aircraft with respect to the aircraft.
    """

    aplog.clearerror()
    try:

      apturn.checkinturn()
      self._logbreak()
      self._logline()

      selfname = self._name
      othername = other._name

      apturn.checkinsetuporturn()

      angleofftail = self.angleofftail(other)
      if angleofftail == "0 line" or angleofftail == "180 line":
        self._logevent("%s has %s on its %s." % (othername, selfname, angleofftail))
      else:
        self._logevent("%s has %s in its %s." % (othername, selfname, angleofftail))

      angleofftail = other.angleofftail(self)
      if angleofftail == "0 line" or angleofftail == "180 line":
        self._logevent("%s is on the %s of %s." % (othername, angleofftail, selfname))
      else:
        self._logevent("%s is in the %s of %s." % (othername, angleofftail, selfname))

      inlimitedradararc = self.inlimitedradararc(other)
      if inlimitedradararc:
        self._logevent("%s is in the limited radar arc of %s." % (othername, selfname))
      else:
        self._logevent("%s is not in the limited radar arc of %s." % (othername, selfname))  

      self._lognote(note)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)
      
  #############################################################################

  def climbingflight(self, vertical=False):

    """
    Return true if the aircraft is climbing.
    """

    return _isclimbingflight(self._flighttype, vertical=vertical)

  #############################################################################

  def divingflight(self, vertical=False):

    """
    Return true if the aircraft is diving.
    """

    return _isdivingflight(self._flighttype, vertical=vertical)
   
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
      self._logaction("", "aircraft has collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True
      self._leaveanycloseformation()

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
    self._wasrollingonlastfp, \
    self._fpcarry, \
    self._apcarry, \
    self._gloccheck, \
    self._ETrecoveryfp, \
    self._BTrecoveryfp, \
    self._HTrecoveryfp, \
    self._TTrecoveryfp, \
    self._rollrecoveryfp, \
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
      self._wasrollingonlastfp, \
      self._fpcarry, \
      self._apcarry, \
      self._gloccheck, \
      self._ETrecoveryfp, \
      self._BTrecoveryfp, \
      self._HTrecoveryfp, \
      self._TTrecoveryfp, \
      self._rollrecoveryfp, \
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
    ap._checkinturn()
    self._log("has been killed.")
    self._destroyed = True

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

def startvisualsighting():

  aplog.clearerror()
  try:

    apturn.checkinturn()

    for target in aslist():
      aplog.logbreak()
      if target._sightedonpreviousturn:
        aplog.log("%-4s : was sighted on previous turn." % target.name())
      else:
        aplog.log("%-4s : was unsighted on previous turn." % target.name())
      aplog.log("%-4s : maximum visual range is %d." % (target.name(), target.maxvisualsightingrange()))
      for searcher in aslist():
        if target.name() != searcher.name() and target.force() != searcher.force():
          aplog.log("%-4s : searcher %s: range is %2d: %s." % (
            target.name(), searcher.name(), 
            apvisualsighting.visualsightingrange(searcher, target), 
            apvisualsighting.visualsightingcondition(searcher, target)[0]
          ))

  except RuntimeError as e:
    aplog.logexception(e)
      
################################################################################

def endvisualsighting():

  aplog.clearerror()
  try:

    apturn.checkinturn()

    aplog.logbreak()
    for target in aslist():
      if target._sighted and target._identified:
        aplog.log("%-4s : is sighted and identified." % target.name())
      elif target._sighted:
        aplog.log("%-4s : is sighted." % target.name())
      else:
        aplog.log("%-4s : is unsighted." % target.name())

  except RuntimeError as e:
    aplog.logexception(e)
      
################################################################################
