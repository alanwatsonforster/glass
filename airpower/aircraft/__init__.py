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

def _startsetup():
  global _aircraftlist
  _aircraftlist = []

def _endsetup():
  for a in _aircraftlist:
    a._save(ap.turn())

def _startturn():
  for a in _aircraftlist:
    a._finishedmove = False
    a._checkcloseformation()

def _endturn():
  for a in _aircraftlist:
    if not a._destroyed and not a._leftmap and not a._finishedmove:
      raise RuntimeError("aircraft %s has not finished its move." % a._name)
    a._checkcloseformation()
    a._save(ap.turn())

def _drawmap():
  for a in _aircraftlist:
    if a._destroyed or a._finishedmove:
      a._drawflightpath()
      a._drawatend()
    elif not self._leftmap:
      a._drawatstart()

#############################################################################

class aircraft:

  from ._closeformation import \
    joincloseformation, leavecloseformation, \
    _checkcloseformation, _leaveanycloseformation, _breakdowncloseformation, \
    closeformationsize, closeformationnames

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
    power, spbr, fuelrate, powerfade, engines, turndrag, \
    minspeed, maxspeed, cruisespeed, climbspeed, maxdivespeed, ceiling, \
    rollhfp, rolldrag, climbcapability, hasproperty

  from ._draw import \
    _drawatstart, _drawatend, \
    _startflightpath, _continueflightpath, _drawflightpath

  from ._log import \
    _log, _logaction, _logevent, _logbreak

  #############################################################################

  def __init__(self, name, aircraftdata, hexcode, azimuth, altitude, speed, configuration):

    aplog.clearerror()
    try:

      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)

      apaltitude.checkisvalidaltitude(altitude)
      aphex.checkisvalid(x, y, facing)

      # In addition to the specified position, azimuth, altitude, speed, and 
      # configuration, aircraft initially have level flight, normal power, and
      # no carries.

      self._name                 = name
      self._x                    = x
      self._y                    = y
      self._facing               = facing
      self._altitude             = altitude
      self._altitudeband         = apaltitude.altitudeband(self._altitude)
      self._altitudecarry        = 0
      self._speed                = speed
      self._configuration        = configuration
      self._flighttype           = "LVL"
      self._powersetting         = "N"
      self._bank                 = None
      self._maneuvertype         = None
      self._maneuversense        = None
      self._maneuverfp           = 0
      self._maneuveraltitudeband = None
      self._wasrollingonlastfp   = False
      self._fpcarry              = 0
      self._apcarry              = 0
      self._gloccheck            = 0
      self._closeformation       = []
      self._aircraftdata         = apaircraftdata.aircraftdata(aircraftdata)
      self._destroyed            = False
      self._leftmap              = False
      self._turnsstalled         = 0
      self._turnsdeparted        = 0
      self._finishedmove         = True
      self._flightpathx          = []
      self._flightpathy          = []

      self._saved = []

      global _aircraftlist
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
    self._powersetting, \
    self._flighttype, \
    self._bank, \
    self._maneuvertype, \
    self._maneuversense, \
    self._maneuverfp, \
    self._maneuveraltitudeband, \
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
      self._powersetting, \
      self._flighttype, \
      self._bank, \
      self._maneuvertype, \
      self._maneuversense, \
      self._maneuverfp, \
      self._maneuveraltitudeband, \
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

  ##############################################################################

  def move(self, flighttype, power, actions, flamedoutengines=0):

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

      self._powerap          = 0
      self._speedap          = 0
      self._spbrap           = 0
      self._turnrateap       = 0
      self._sustainedturnap  = 0
      self._altitudeap       = 0
      self._othermaneuversap = 0

      # These keep track of the maximum turn rate used in the turn, the
      # number of roll maneuvers, and the effective cliumb capability
      # (the climb capability at the moment the first VFP is used).
      # Again, they are used to calculate the final speed.

      self._maxturnrate              = None
      self._effectiveclimbcapability = None

      # This flags whether a maneuvering departure has occured.
      
      self._maneuveringdeparture = False
      
      self._flighttype = flighttype

      self._startmovespeed(power, flamedoutengines)

      self._log("configuration is %s." % self._configuration)
      self._log("altitude band is %s." % self._altitudeband)
      self._log("flight type   is %s." % self._flighttype)

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
      aplog.logexception(e)

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
      aplog.logexception(e)


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

      self._finishedmove = True
   
    self._save(ap.turn())

    self._log("--- end of move -- ")
    self._logbreak()

  ################################################################################

  def _assert(self, position, speed, configuration=None):

    """
    Verify the position and speed of an aircraft.
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
    if speed != None and speed != self._speed:
      print("== assertion failed ===")
      print("== actual speed  : %.1f" % self._speed)
      print("== expected speed: %.1f" % position)
      assert speed == self._speed
    if configuration != None and configuration != self._configuration:
      print("== assertion failed ===")
      print("== actual speed  : %s" % self._configuration)
      print("== expected speed: %s" % configuration)
      assert configuration == self._configuration

  ################################################################################  
