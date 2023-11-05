import apengine._stores       as apstores
import apengine._aircraftdata as apaircraftdata

def configuration(self):

  # If the aircraft type does not have a stores limit configured,
  # assume the configuration is CL.

  if not self._aircraftdata.hasstoreslimits():
    print("no stores limit")
    return "CL"

  # See rule 4.2 and 4.3.

  totalweight = apstores.totalweight(self._stores)
  totalload   = apstores.totalload(self._stores)

  if totalweight > self._aircraftdata.storeslimit("DT"):
    return False
  elif totalload <= self._aircraftdata.storeslimit("CL"):
    return "CL"
  elif totalload <= self._aircraftdata.storeslimit("1/2"):
    return "1/2"
  else:
    return "DT"
