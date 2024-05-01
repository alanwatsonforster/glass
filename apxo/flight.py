"""
Aircraft flight.
"""

##############################################################################

import apxo                as ap
import apxo.aircraft       as apxoaircraft
import apxo.departedflight as apdepartedflight
import apxo.log            as aplog
import apxo.normalflight   as apnormalflight
import apxo.specialflight  as apspecialflight
import apxo.stalledflight  as apstalledflight
import apxo.turn           as apturn

from apxo.normalflight import _isdivingflight, _isclimbingflight, _islevelflight

##############################################################################

def move(A, flighttype, power, actions="", 
  flamedoutengines=0, lowspeedliftdeviceselected=None, note=False):

  """
  Start a move, declaring the flight type and power, and possible carrying 
  out some actions.
  """

  apturn.checkinturn()

  A._logbreak()
  A._logline()

  apxoaircraft._zorder += 1
  A._zorder = apxoaircraft._zorder

  if A._destroyed or A._leftmap:
    A._endmove()
    return

  # We save values of these variables at the end of the previous move.

  A._previouspowersetting  = A._powersetting
  A._previousflighttype    = A._flighttype
  A._previousaltitude      = A.altitude()
  A._previousaltitudecarry = A.altitudecarry()
  A._previousspeed         = A.speed()

  # These account for the APs associated with power, speed, speed-brakes, 
  # turns (split into the part for the maximum turn rate and the part for 
  # sustained turns), altitude loss or gain, and special maneuvers. They
  # are used in normal flight and stalled flight, but not departed flight.

  A._powerap          = 0
  A._speedap          = 0
  A._spbrap           = 0
  A._turnrateap       = 0
  A._sustainedturnap  = 0
  A._altitudeap       = 0
  A._othermaneuversap = 0

  # These keep track of the maximum turn rate used in the turn, the
  # number of roll maneuvers, and the effective cliumb capability
  # (the climb capability at the moment the first VFP is used).
  # Again, they are used to calculate the final speed.

  A._maxturnrate              = None
  A._effectiveclimbcapability = None

  # This flags whether a maneuvering departure has occured.
  
  A._maneuveringdeparture = False
  
  A._flighttype = flighttype
  A._logstart("flight type   is %s." % A._flighttype)

  if flighttype == "SP":
    apspecialflight.checkflight(A)
  elif flighttype == "ST":
    apstalledflight.checkflight(A)
  elif flighttype == "DP":
    apdepartedflight.checkflight(A)
  else:
    apnormalflight.checkflight(A)

  if flighttype == "SP":
    A._setspeed(power)
  else:
    A._startmovespeed(power, flamedoutengines, lowspeedliftdeviceselected)
    A._logstart("configuration is %s." % A._configuration)
  A._logstart("altitude band is %s." % A.altitudeband())
  A._logstart("damage        is %s." % A.damage())

  if A._flighttype == "SP":

    A._fpcarry = 0
    A._apcarry = 0
    A._turnsstalled  = 0
    A._turnsdeparted = 0
    apspecialflight.doflight(A, actions, note=note)
    endmove(A)
    
  elif A._flighttype == "ST":       

    A._fpcarry = 0
    A._setaltitudecarry(0)
    apstalledflight.doflight(A, actions, note=note)
    A._turnsstalled += 1
    endmove(A)

  elif A._flighttype == "DP":

    A._fpcarry = 0
    A._apcarry = 0
    A._setaltitudecarry(0)
    apdepartedflight.doflight(A, actions, note=note)
    A._turnsdeparted += 1
    endmove(A)

  else:

    # See rule 8.1.4 on altitude carry.
    if not A.isinclimbingflight():
      A._setaltitudecarry(0)

    A._turnsstalled  = 0
    A._turnsdeparted = 0
    apnormalflight.startflight(A, actions, note=note)

  A._logline()


################################################################################

def continuemove(A, actions="", note=False):

  """
  Continue a move that has been started, possible carrying out some actions.
  """

  apturn.checkinturn()

  if not A._destroyed and not A._leftmap and A._flighttype != "ST" and A._flighttype != "DP" and A._flighttype != "SP":
    apnormalflight.continueflight(A, actions, note=note)
  else:
    A._lognote(note)
  A._logline()


################################################################################

def endmove(A):

  """
  Process the end of a move.
  """

  if A._destroyed:
  
    A._logend("aircraft has been destroyed.")

  elif A._leftmap:

    A._logend("aircraft has left the map.")

  else:

    if A._flighttype == "SP":

      A._newspeed = A.speed()

    else:

      A._endmovespeed()

    A._finishedmove = True
  
  A._save(apturn.turn())
