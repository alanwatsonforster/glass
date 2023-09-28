"""
Stalled flight for the aircraft class.
"""

import math

import airpower.altitude as apaltitude

def _dostalledflight(self, action):

  """
  Carry out stalled flight.
  """

  # See rule 6.4.

  altitudechange = math.ceil(self._speed + self._turnsstalled)

  initialaltitude = self._altitude    
  initialaltitudeband = self._altitudeband
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)
  altitudechange = initialaltitude - self._altitude
    
  if self._turnsstalled == 1:
    self._altitudeap = 0.5 * altitudechange
  else:
    self._altitudeap = 1.0 * altitudechange

  self._logposition("end", action)

  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))

  self.checkforterraincollision()
  if self._destroyed:
    return

  # The only valid action is to do nothing or to jettison stores.

  if action == "J1/2":
    self._J("1/2")
  elif action == "JCL":
    self._J("CL")
  elif action != "":
    raise ValueError("invalid action %r for stalled flight." % action)
