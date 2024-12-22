import apxo.aircraft.stores as apstores
import apxo.aircraftdata as apaircraftdata


def isvalid(configuration):
    """
    Return True if the argument is a valid configuration.
    """

    return configuration in ["CL", "1/2", "DT"]


def update(A):
    """
    Updated the configuration based on the current stores.
    """

    # If no stores are specified, do nothing.
    if A._stores == None:
        return

    assert A._aircraftdata.hasstoreslimits()

    # See rule 4.2 and 4.3.

    totalweight = apstores.totalweight(A._stores)
    totalload = apstores.totalload(A._stores, fuel=A.externalfuel())

    if totalweight > A._aircraftdata.storeslimit("DT"):
        raise RuntimeError("total stores weight exceeds the aircraft capacity.")

    if totalload <= A._aircraftdata.storeslimit("CL"):
        A._configuration = "CL"
    elif totalload <= A._aircraftdata.storeslimit("1/2"):
        A._configuration = "1/2"
    else:
        A._configuration = "DT"
