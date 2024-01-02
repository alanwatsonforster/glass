"""
Departed flight for aircraft.
"""

import math

import apxo.altitude     as apaltitude
import apxo.capabilities as apcapabilities
import apxo.hex          as aphex

def checkflight(a):

  """
  Check departed flight is allowed.
  """

  if apcapabilities.hasproperty(a, "SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform departed flight.")

def doflight(a, action, note=False):

  """
  Carry out departed flight.
  """

  a._logposition("start")   

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

      if aphex.isside(a._x, a._y):
        a._x, a._y = aphex.centertoright(a._x, a._y, a._facing, sense)
      if action[0] == "L":
        a._facing = (a._facing + 30) % 360
      else:
        a._facing = (a._facing - 30) % 360
      a._continueflightpath()
      facingchange -= 30

      # Shift.

      # See rule 5.4.
      a._maxfp = a._speed + a._fpcarry
      a._fpcarry = 0

      shift = int((a._maxfp) / 2)
      for i in range(0, shift):
        a._x, a._y = aphex.forward(a._x, a._y, a._facing)
        a.checkforterraincollision()
        a.checkforleavingmap()
        if a._destroyed or a._leftmap:
          return

   # Do the (remaining) facing change.

  if aphex.isside(a._x, a._y):
    a._x, a._y = aphex.sidetocenter(a._x, a._y, a._facing, sense)
  if action[0] == "L":
    a._facing = (a._facing + facingchange) % 360
  else:
    a._facing = (a._facing - facingchange) % 360
  a._continueflightpath()

  # Now lose altitude.

  initialaltitudeband = a._altitudeband
  altitudechange = math.ceil(a._speed + 2 * a._turnsdeparted)
  a._altitude, a._altitudecarry = apaltitude.adjustaltitude(a._altitude, a._altitudecarry, -altitudechange)
  a._altitudeband = apaltitude.altitudeband(a._altitude)
  
  a._lognote(note)

  a._logposition("end")
  if initialaltitudeband != a._altitudeband:
    a._logevent("altitude band changed from %s to %s." % (initialaltitudeband, a._altitudeband))
  a.checkforterraincollision()

  a._newspeed = a._speed
