"""
Stalled flight for the aircraft class.
"""

import math

import apengine._altitude as apaltitude

def _checkstalledflight(self):

  if self.hasproperty("SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform stalled flight.")

  # See rule 6.3.

  if self._speed >= self.minspeed():
      raise RuntimeError("flight type cannot be ST as aircraft is not stalled.")

  self._logstart("- speed is below the minimum of %.1f." % self.minspeed())
  self._logstart("- aircraft is stalled.")

def _dostalledflight(self, action, note=False):

  """
  Carry out stalled flight.
  """

  def dojettison(configuration):

    """
    Jetison stores to achieve the specified configuration.
    """

    # See rule 4.4. 
  
    if self._configuration == configuration:
      raise RuntimeError("configuration is already %s." % configuration)
    if self._configuration == "CL" or configuration == "DT":
      raise RuntimeError("attempt to change from configuration %s to %s." % (self._configuration, configuration))
    self._logevent("jettisoned stores.")
    self._logevent("configuration changed from %s to %s." % (self._configuration, configuration))
    self._configuration = configuration  

  # See rule 6.4.
      
  self._logstart("- carrying %+.2f APs." % self._apcarry)
  self._logline()
  self._logaction("start", "", self.position())   

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

  self._logaction("end", action, self.position())

  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))

  self.checkforterraincollision()
  if self._destroyed:
    return

  # The only valid action is to do nothing or to jettison stores.

  if action == "J1/2":
    dojettison("1/2")
  elif action == "JCL":
    dojettison("CL")
  elif action != "":
    raise RuntimeError("invalid action %r for stalled flight." % action)

  self._logline()
