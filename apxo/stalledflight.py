"""
Stalled flight for aircraft.
"""

import math
import re

import apxo.altitude      as apaltitude
import apxo.capabilities  as apcapabilities
import apxo.configuration as apconfiguration
import apxo.stores        as apstores

def checkflight(a):

  if apcapabilities.hasproperty(a, "SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform stalled flight.")

  # See rule 6.3.

  if a._speed >= apcapabilities.minspeed(a):
      raise RuntimeError("flight type cannot be ST as aircraft is not stalled.")

  a._logstart("speed is below the minimum of %.1f." % apcapabilities.minspeed(a))
  a._logstart("aircraft is stalled.")

def doflight(a, action, note=False):

  """
  Carry out stalled flight.
  """

  def dojettison(m):

    # See rule 4.4.   
    # We implement the delay of 1 FP by making this an other element.
    
    previousconfiguration = a._configuration

    for released in m[1].split("+"):
      a._stores = apstores._release(a._stores, released,
        printer=lambda s: a._logevent(s)
      )

    apconfiguration.update(a)

    if a._configuration != previousconfiguration:
      a._logevent("configuration changed from %s to %s." % (
        previousconfiguration, a._configuration
      ))
  
  # See rule 6.4.
      
  a._logevent("is carrying %+.2f APs." % a._apcarry)

  a._logposition("start")   

  altitudechange = math.ceil(a._speed + a._turnsstalled)

  initialaltitude = a._altitude    
  initialaltitudeband = a._altitudeband
  a._altitude, a._altitudecarry = apaltitude.adjustaltitude(a._altitude, a._altitudecarry, -altitudechange)
  a._altitudeband = apaltitude.altitudeband(a._altitude)
  altitudechange = initialaltitude - a._altitude
    
  if a._turnsstalled == 0:
    a._altitudeap = 0.5 * altitudechange
  else:
    a._altitudeap = 1.0 * altitudechange

  a._lognote(note)

  a._logposition("end")

  if initialaltitudeband != a._altitudeband:
    a._logevent("altitude band changed from %s to %s." % (initialaltitudeband, a._altitudeband))

  a.checkforterraincollision()
  if a._destroyed:
    return

  # The only valid actions are to do nothing or to jettison stores.

  fullaction = action
  while action != "":
    m = re.compile(r"J\(([^)]*)\)").match(action)
    if not m:
      raise RuntimeError("invalid action %r for stalled flight." % fullaction)
    dojettison(m)  
    action = action[len(m.group()):]


  a._logline()
