import apxo.stores       as apstores
import apxo.aircraftdata as apaircraftdata

def _updateconfiguration(self):

  """
  Updated the configuration based on the current stores.
  """

  # If no stores are specified, do nothing.
  if self.stores == None:
    return

  assert self._aircraftdata.hasstoreslimits()

  # See rule 4.2 and 4.3.

  totalweight = apstores.totalweight(self.stores)
  totalload   = apstores.totalload(self.stores, fuel=self.externalfuel())

  if totalweight > self._aircraftdata.storeslimit("DT"):
    raise RuntimeError("total stores weight exceeds the aircraft capacity.")

  if totalload <= self._aircraftdata.storeslimit("CL"):
    self.configuration = "CL"
  elif totalload <= self._aircraftdata.storeslimit("1/2"):
    self.configuration = "1/2"
  else:
    self.configuration = "DT"
