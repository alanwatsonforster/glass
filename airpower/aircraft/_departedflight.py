"""
Departed flight for the aircraft class.
"""

import math

import airpower.altitude as apaltitude
import airpower.hex      as aphex

def _dodepartedflight(self, action):

  """
  Carry out departed flight.
  """

  # See rule 6.4.

  altitudechange = math.ceil(self._speed + 2 * self._turnsdeparted)

  initialaltitudeband = self._altitudeband
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)

  self._logposition("end", action)

  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
  self.checkforterraincollision()
      
  # The action specifies the facing change. Valid values are:
  #
  # - "R30", "R60", "R90", ..., "R300"
  # - "R", "RR", and "RRR" which as usual mean "R30", "R60", and "R90"
  # - the "L" equivalents.

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
    raise ValueError("invalid action %r for departed flight." % action)

  facingchange = int(action[1:])
  if facingchange % 30 != 0 or facingchange <= 0 or facingchange > 300:
    raise ValueError("invalid action %r for departed flight." % action)

  if action[0] == "R":
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
    self._facing = (self._facing - facingchange) % 360
  else:
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
    self._facing = (self._facing + facingchange) % 360  