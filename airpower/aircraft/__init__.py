import airpower              as ap
import airpower.aircraftdata as apaircraftdata
import airpower.altitude     as apaltitude
import airpower.azimuth      as apazimuth
import airpower.draw         as apdraw
import airpower.hex          as aphex
import airpower.hexcode      as aphexcode
import airpower.log          as aplog
import airpower.map          as apmap
import airpower.turnrate     as apturnrate

import math

from ._normalflight import _isdiving, _isclimbing


################################################################################

_aircraftlist = []

def _restart():
  global _aircraftlist
  _aircraftlist = []

def _allstartturn():
  for a in _aircraftlist:
    a._startturn()

def _allendturn():
  for a in _aircraftlist:
    a._endturn()

def _alldraw():
  for a in _aircraftlist:
    a._draw()

#############################################################################

class aircraft:

  from ._stalledflight import \
    _checkstalledflight, _dostalledflight

  from ._departedflight import \
    _checkdepartedflight, _dodepartedflight

  from ._normalflight import \
    _checknormalflight, \
    _startnormalflight, _continuenormalflight, _endnormalflight

  from ._speed import \
    _startmovespeed, _endmovespeed

  from ._flightcapabilities import \
    power, spbr, fuelrate, powerfade, turndrag, \
    minspeed, maxspeed, cruisespeed, climbspeed, maxdivespeed, ceiling, \
    rollhfp, rolldrag, climbcapability, hasproperty

  from ._draw import \
    _drawatstart, _drawatend, \
    _startflightpath, _continueflightpath, _drawflightpath

  from ._log import \
    _log, _logposition, _logevent, _logbreak

  #############################################################################

  def __init__(self, name, aircraftdata, hexcode, azimuth, altitude, speed, configuration="CL"):

    aplog.clearerror()
    try:

      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)

      apaltitude.checkisvalidaltitude(altitude)
      aphex.checkisvalid(x, y, facing)

      # In addition to the specified position, azimuth, altitude, speed, and 
      # configuration, aircraft initially have level flight, normal power, and
      # no carries.

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
      self._bank          = None
      self._turnrate      = None
      self._turnfp        = 0
      self._fpcarry       = 0
      self._apcarry       = 0
      self._aircraftdata  = apaircraftdata.aircraftdata(aircraftdata)
      self._destroyed     = False
      self._leftmap       = False
      self._turnsstalled  = 0
      self._turnsdeparted = 0
      self._finishedmove  = True
      self._flightpathx   = []
      self._flightpathy   = []

      self._saved = []
      self._save(0)

      global _aircraftlist
      _aircraftlist.append(self)

    except RuntimeError as e:
      aplog.logerror(e)

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

    if not apmap.isonmap(self._x, self._y):
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
    self._bank, \
    self._turnrate, \
    self._turnfp, \
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
      self._bank, \
      self._turnrate, \
      self._turnfp, \
      self._fpcarry, \
      self._apcarry, \
      self._destroyed, \
      self._leftmap, \
      self._turnsstalled, \
      self._turnsdeparted \
    )

  ##############################################################################

  def startmove(self, flighttype, power, actions, flamedoutfraction=0):

    """
    Start a move, declaring the flight type and power, and possible carrying 
    out some actions.
    """

    aplog.clearerror()
    try:

      self._log("--- start of move --")

      self._restore(ap.turn() - 1)

      if self._destroyed or self._leftmap:
        self._endmove()
        return

      self._startflightpath()

      # We save values of these variables at the end of the previous move.

      self._previousconfiguration = self._configuration
      self._previouspowersetting  = self._powersetting
      self._previousflighttype    = self._flighttype
      self._previousaltitude      = self._altitude
      self._previousaltitudeband  = self._altitudeband
      self._previousaltitudecarry = self._altitudecarry
      self._previousspeed         = self._speed

      # These account for the APs associated with power, speed, speed-brakes, 
      # turns (split into the part for the maximum turn rate and the part for 
      # sustained turns), altitude loss or gain, and special maneuvers. They
      # are used in normal flight and stalled flight, but not departed flight.

      self._powerap         = 0
      self._speedap         = 0
      self._spbrap          = 0
      self._turnrateap      = 0
      self._sustainedturnap = 0
      self._altitudeap      = 0
      self._maneuverap      = 0

      # These keep track of the maximum turn rate used in the turn, the
      # number of roll maneuvers, and the effective cliumb capability
      # (the climb capability at the moment the first VFP is used).
      # Again, they are used to calculate the final speed.

      self._maxturnrate     = None
      self._rolls           = 0
      self._effectiveclimbcapability = None

      self._flighttype      = flighttype

      self._speed,          \
      self._powersetting,   \
      self._powerap,        \
      self._speedap         = self._startmovespeed(power, flamedoutfraction)

      self._log("configuration is %s." % self._configuration)
      self._log("altitude band is %s." % self._altitudeband)
      self._log("flight type is %s." % self._flighttype)

      # See rule 8.1.4 on altitude carry.
      if not _isclimbing(self._flighttype):
        self._altitudecarry = 0

      if self._flighttype == "ST":       

        self._fpcarry = 0
        self._turnsstalled += 1
        self._checkstalledflight()
        self._dostalledflight(actions)
        self._endmove()

      elif self._flighttype == "DP":

        self._fpcarry = 0
        self._apcarry = 0
        self._turnsdeparted += 1
        self._checkdepartedflight()
        self._dodepartedflight(actions)
        self._endmove()

      else:

        self._turnsstalled  = 0
        self._turnsdeparted = 0
        self._checknormalflight()
        self._startnormalflight(actions)

    except RuntimeError as e:
      aplog.logerror(e)

  ################################################################################

  def continuemove(self, actions):

    """
    Continue a move that has been started, possible carrying out some actions.
    """

    aplog.clearerror()
    try:

      if self._destroyed or self._leftmap or self._flighttype == "ST" or self._flighttype == "DP":
        return

      self._continuenormalflight(actions)

    except RuntimeError as e:
      aplog.logerror(e)

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
     
      self._endmovespeed()

      if self._previousconfiguration != self._configuration:
        self._log("configuration changed from %s to %s." % (self._previousconfiguration, self._configuration))
      else:
        self._log("configuration is unchanged at %s." % self._configuration)
        
      if self._previousaltitudeband != self._altitudeband:
        self._log("altitude band changed from %s to %s." % (self._previousaltitudeband, self._altitudeband))
      else:
        self._log("altitude band is unchanged at %s." % self._altitudeband)

      if self._altitudecarry != 0:
        self._log("- carrying %.2f altitude levels." % self._altitudecarry)
      if self._flighttype != "DP":
        self._log("- carrying %+.2f APs" % self._apcarry)
      if self._flighttype != "ST" and self._flighttype != "DP":
        self._log("- carrying %.1f FPs." % self._fpcarry)

      self._finishedmove = True
   
    self._save(ap.turn())

    self._log("--- end of move -- ")
    self._logbreak()

  ################################################################################

  def _startturn(self):
    self._finishedmove = False

  ################################################################################

  def _endturn(self):
    if not self._destroyed and not self._leftmap and not self._finishedmove:
      raise RuntimeError("aircraft %s has not finished its move." % self._name)

  ################################################################################

  def _draw(self):
    if self._destroyed or self._finishedmove:
      self._drawflightpath()
      self._drawatend()
    elif not self._leftmap:
      self._drawatstart()

#############################################################################

