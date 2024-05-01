"""
Departed flight for aircraft.
"""

import math

import apxo.altitude     as apaltitude
import apxo.capabilities as apcapabilities
import apxo.hex          as aphex

def checkflight(A):

  """
  Check departed flight is allowed.
  """

  if apcapabilities.hasproperty(A, "SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform departed flight.")

def doflight(A, action, note=False):

  """
  Carry out departed flight.
  """

  A._logposition("start")   

  # See rule 6.4 "Abnormal FLight (Stalls and Departures)" and rule 7.7 
  # "Manuevering Departures".
      
  # The action specifies a possible shift and the facing change. Valid values 
  # are:
  #
  # - "R30", "R60", "R90", ..., "R300"
  # - "R", "RR", and "RRR" which as usual mean "R30", "R60", and "R90"
  # - the "L" equivalents.

  if action[0:2] == "MD":
    maneuveringdeparture = True
    action = action[2:]
  else:
    maneuveringdeparture = False

  if action == "R":
    action = "R30"
  elif action == "RR":
    action = "R60"
  elif action == "RRR":
    action = "R90"
  elif action == "L":
    action = "L30"
  elif action == "LL":
    action = "L60"
  elif action == "LLL":
    action = "L90"
  
  if len(action) < 3 or (action[0] != "R" and action[0] != "L") or not action[1:].isdecimal():
    raise RuntimeError("invalid action %r for departed flight." % action)

  sense = action[0]
  facingchange = int(action[1:])
  if facingchange % 30 != 0 or facingchange <= 0 or facingchange > 300:
    raise RuntimeError("invalid action %r for departed flight." % action)

  if maneuveringdeparture:

      # Do the first facing change.

      A._doturn(sense, 30)
      A._extendpath()
      facingchange -= 30

      # Shift.

      # See rule 5.4.
      A._maxfp = A.speed() + A._fpcarry
      A._fpcarry = 0

      shift = int((A._maxfp) / 2)
      for i in range(0, shift):
        A._doforward()
        A._extendpath()
        A.checkforterraincollision()
        A.checkforleavingmap()
        if A._destroyed or A._leftmap:
          return

   # Do the (remaining) facing change.

  A._doturn(sense, facingchange)
  A._extendpath()

  # Now lose altitude.

  initialaltitudeband = A.altitudeband()
  altitudechange = math.ceil(A.speed() + 2 * A._turnsdeparted)
  A._dodive(altitudechange)
  
  A._lognote(note)

  A._logposition("end")
  if initialaltitudeband != A.altitudeband():
    A._logevent("altitude band changed from %s to %s." % (initialaltitudeband, A.altitudeband()))
  A.checkforterraincollision()

  A._newspeed = A.speed()
