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

from ._normalflight import _isdiving, _isclimbing
    
class aircraft:

  from ._departedflight import _dodepartedflight
  from ._draw           import _drawaircraft, _drawflightpath
  from ._log            import _log, _logposition, _logevent, _logbreak
  from ._normalflight   import \
    _donormalflight, _doaction, _getelementdispatchlist, \
    _A, _C, _D, _H, _J, _K, _TD, _TL, _TR, _S
  from ._speed          import _startmovespeed, _endmovespeed
  from ._stalledflight  import _dostalledflight

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

    # These account for the APs associated with power, drag (from insufficient
    # power or high speed), speed-brakes, turns (split into the part for the 
    # maximum turn rate and the part for sustained turns), and altitude loss
    # or gain.

    self._powerap          = 0
    self._dragap           = 0
    self._spbrap           = 0
    self._turnrateap       = 0
    self._sustainedturnap  = 0
    self._altitudeap       = 0

    self._speed, self._powersetting, self._powerap, self._dragap = \
      self._startmovespeed(power, flamedoutfraction)
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
        self._log("no turns.")
      else:
        self._log("maximum turn rate is %s." % self._maxturnrate)
        
      self._endmovespeed()

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
