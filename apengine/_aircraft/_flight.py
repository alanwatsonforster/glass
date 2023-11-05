"""
Aircraft flight.
"""

##############################################################################

import apengine      as ap
import apengine._log as aplog

from ._normalflight import _isdivingflight, _isclimbingflight, _islevelflight
from ._draw import _zorder

##############################################################################

def move(self, flighttype, power, actions, flamedoutengines=0, note=False):

  """
  Start a move, declaring the flight type and power, and possible carrying 
  out some actions.
  """

  aplog.clearerror()
  try:

    ap._checkinturn()

    self._logbreak()
    self._logline()

    global _zorder
    _zorder += 1
    self._zorder = _zorder

    if self._destroyed or self._leftmap:
      self._endmove()
      return

    # We save values of these variables at the end of the previous move.

    self._previouspowersetting  = self._powersetting
    self._previousflighttype    = self._flighttype
    self._previousaltitude      = self._altitude
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
    self._logstart("flight type   is %s." % self._flighttype)

    if flighttype == "SP":
      self._checkspecialflight()
    elif flighttype == "ST":
      self._checkstalledflight()
    elif flighttype == "DP":
      self._checkdepartedflight()
    else:
      self._checknormalflight()

    if flighttype == "SP":
      self._speed = power
    else:
      self._startmovespeed(power, flamedoutengines)
      self._logstart("configuration is %s." % self._configuration)
    self._logstart("altitude band is %s." % self._altitudeband)
    self._logstart("damage        is %s." % self.damage())

    if self._flighttype == "SP":

      self._fpcarry = 0
      self._apcarry = 0
      self._turnsstalled  = 0
      self._turnsdeparted = 0
      self._dospecialflight(actions, note=note)
      self._endmove()
      
    elif self._flighttype == "ST":       

      self._fpcarry = 0
      self._altitudecarry = 0
      self._dostalledflight(actions, note=note)
      self._turnsstalled += 1
      self._endmove()

    elif self._flighttype == "DP":

      self._fpcarry = 0
      self._apcarry = 0
      self._altitudecarry = 0
      self._dodepartedflight(actions, note=note)
      self._turnsdeparted += 1
      self._endmove()

    else:

      # See rule 8.1.4 on altitude carry.
      if not self.climbingflight():
        self._altitudecarry = 0
      
      self._turnsstalled  = 0
      self._turnsdeparted = 0
      self._startnormalflight(actions, note=note)

    self._logline()

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

def continuemove(self, actions, note=False):

  """
  Continue a move that has been started, possible carrying out some actions.
  """

  aplog.clearerror()
  try:

    ap._checkinturn()

    if not self._destroyed and not self._leftmap and self._flighttype != "ST" and self._flighttype != "DP" and self._flighttype != "SP":
      self._continuenormalflight(actions, note=note)
    else:
      self._lognote(note)
    self._logline()

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

def _endmove(self):

  """
  Process the end of a move.
  """

  if self._destroyed:
  
    self._logend("aircraft has been destroyed.")

  elif self._leftmap:

    self._logend("aircraft has left the map.")

  else:

    if self._flighttype == "SP":

      self._newspeed = self._speed

    else:

      self._endmovespeed()

    self._finishedmove = True
  
  self._save(ap.turn())
