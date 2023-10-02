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

  self._log("---")
  self._logposition("start", "")

  # See rule 6.4 "Abnormal FLight (Stalls and Departures)" and rule 7.7 
  # "Manuevering Departures".
      
  # The action specifies a possible shift and the facing change. Valid values 
  # are a possible leading S (for a shift) folllowed by:
  #
  # - "R30", "R60", "R90", ..., "R300"
  # - "R", "RR", and "RRR" which as usual mean "R30", "R60", and "R90"
  # - the "L" equivalents.

  if action != "" and action[0] == "S":
    action = action[1:]
    shift = True
  else:
    shift = False

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

  facingchange = int(action[1:])
  if facingchange % 30 != 0 or facingchange <= 0 or facingchange > 300:
    raise RuntimeError("invalid action %r for departed flight." % action)

  # Do the first facing change.

  if action[0] == "R":
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
    self._facing = (self._facing - 30) % 360
  else:
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
    self._facing = (self._facing + 30) % 360
  self._continueflightpath()
  facingchange -= 30

  # Possibly shift.

  if shift:
    i = self._speed // 2
    for i in range(0, int(self._speed / 2)):
      lastx, lasty = self._x, self._y
      self._x, self._y = aphex.nextposition(self._x, self._y, self._facing)
      self._drawflightpath(lastx, lasty)
      self.checkforterraincollision()
      self.checkforleavingmap()
      if self._destroyed or self._leftmap:
        return

  # Do any remaining facing changes.

  lastx, lasty = self._x, self._y
  if action[0] == "R":
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoright(self._x, self._y, self._facing)
    self._facing = (self._facing - facingchange) % 360
  else:
    if aphex.isedgeposition(self._x, self._y):
      self._x, self._y = aphex.centertoleft(self._x, self._y, self._facing)
    self._facing = (self._facing + facingchange) % 360
  self._drawflightpath(lastx, lasty)

  # Now lose altitude.

  altitudechange = math.ceil(self._speed + 2 * self._turnsdeparted)

  initialaltitudeband = self._altitudeband
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)
  
  self._logposition("end", action)
  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
  self.checkforterraincollision()

  self._log("---")

