"""
Stalled flight for the aircraft class.
"""

import math
import re

import apxo.altitude as apaltitude
import apxo.stores   as apstores

def _checkstalledflight(self):

  if self.hasproperty("SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform stalled flight.")

  # See rule 6.3.

  if self._speed >= self.minspeed():
      raise RuntimeError("flight type cannot be ST as aircraft is not stalled.")

  self._logstart("speed is below the minimum of %.1f." % self.minspeed())
  self._logstart("aircraft is stalled.")

def _dostalledflight(self, action, note=False):

  """
  Carry out stalled flight.
  """

  def dojettison(m):

    # See rule 4.4.   
    # We implement the delay of 1 FP by making this an other element.
    
    previousconfiguration = self.configuration

    for released in m[1].split("+"):
      self.stores = apstores._release(self.stores, released,
        printer=lambda s: self._logevent(s)
      )

    self._updateconfiguration()

    if self.configuration != previousconfiguration:
      self._logevent("configuration changed from %s to %s." % (
        previousconfiguration, self.configuration
      ))
  
  # See rule 6.4.
      
  self._logevent("is carrying %+.2f APs." % self._apcarry)

  self._logposition("start")   

  altitudechange = math.ceil(self._speed + self._turnsstalled)

  initialaltitude = self._altitude    
  initialaltitudeband = self._altitudeband
  self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
  self._altitudeband = apaltitude.altitudeband(self._altitude)
  altitudechange = initialaltitude - self._altitude
    
  if self._turnsstalled == 0:
    self._altitudeap = 0.5 * altitudechange
  else:
    self._altitudeap = 1.0 * altitudechange

  self._lognote(note)

  self._logposition("end")

  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))

  self.checkforterraincollision()
  if self._destroyed:
    return

  # The only valid actions are to do nothing or to jettison stores.

  fullaction = action
  while action != "":
    m = re.compile(r"J\(([^)]*)\)").match(action)
    if not m:
      raise RuntimeError("invalid action %r for stalled flight." % fullaction)
    dojettison(m)  
    action = action[len(m.group()):]


  self._logline()
