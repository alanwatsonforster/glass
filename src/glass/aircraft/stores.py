################################################################################

import glass.jsonc
import glass.log
import glass.variants

import os
import glob
import math

################################################################################

_storedict = {}

"""
A dictionary containing the stores. The keys are the store names and the values
are the store properties. The store properties are each in turn a dictionary in
which the keys are the property names and the values are the property values.
"""


def _loadstores():
    """
    Load the stores from the stores data files.

    The stores data files are `../storesdata/*.json`.

    :raises RuntimeError: If a stores data file cannot be opened or read.
    """

    global _storedict

    _storedict = {}

    storesdatadir = os.path.join(os.path.dirname(__file__), "..", "storesdata")

    for path in sorted(glob.glob(os.path.join(storesdatadir, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                _storedict.update(glass.jsonc.load(f))
        except PermissionError:
            raise RuntimeError('unable to open stores data file "%s".' % path)
        except glass.jsonc.JSONDecodeError as e:
            raise RuntimeError(
                'unable to read stores data file "%s": line %d: %s.'
                % (path, e.lineno, e.msg.lower())
            )


_loadstores()

################################################################################


def _storehasproperty(storename, propertyname):
    """
    Return whether a store has a property.

    :param storename: The name of a store.
    :param propertyname: The name of the property.
    :raises RuntimeError: If `storename` does not correspond to a store.
    :return: ``True`` if the store has the name property, otherwise `False`.
    """
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    return propertyname in _storedict[storename]


def _storeproperty(storename, propertyname):
    """
    Return the value of a property of a store.

    :param storename: The name of a store.
    :param propertyname: The name of the property.
    :raises RuntimeError: If `storename` does not correspond to a store or
        `propertyname` does not correspond to a property of the named store.
    :return: The value of the property.
    """
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    if not propertyname in _storedict[storename]:
        raise RuntimeError("unknown property %r." % propertyname)
    return _storedict[storename][propertyname]


def _storeclass(storename):
    """
    Return the class of a store.

    :param storename: The name of a store.
    :param propertyname: The name of the property.
    :raises RuntimeError: If `storename` does not correspond to a store or
        `propertyname` does not correspond to a property of the named store.
    :return: The class of the store as a string. One of the following strings:
       `"AHM"`, `"ARM"`, `"ASM"`, `"BB"`, `"BG"`, `"BRM"`, `"BS"`, `"DP"`,
       `"EP"`, `"FT"`, `"GP"`, `"IRM"`, `"LP"`, `"OP"`, `"RG"`, `"RHM"`, `"RK"`,
       `"RP"`, `"RS"`, and `"WR"`.
    """
    return _storeproperty(storename, "class")


def _storeweight(storename, storesfuelfraction):
    """
    Return the weight of a store.

    :param storename: The name of the store.
    :param storesfuelfraction: The fraction of fuel in the store, if the store is an FT.
    :raises RuntimeError: If `storename` does not correspond to a store.
    :return: The weight of the store as a number.
    """
    weight = _storeproperty(storename, "weight")
    if _storehasproperty(storename, "emptyweight"):
        emptyweight = _storeproperty(storename, "emptyweight")
    else:
        emptyweight = 0
    if _storehasproperty(storename, "fuelcapacity"):
        return emptyweight + storesfuelfraction * (weight - emptyweight)
    else:
        return weight


def _storeload(storename, storesfuelfraction):
    """
    Return the load of a store.

    :param storename: The name of the store.
    :param storesfuelfraction: The fraction of fuel in the store, if the store is an FT.
    :raises RuntimeError: If `storename` does not correspond to a store.
    :return: The load of the store as a number.
    """
    if _storehasproperty(storename, "emptyload") and storesfuelfraction == 0:
        return _storeproperty(storename, "emptyload")
    else:
        return _storeproperty(storename, "load")


def _storefuelcapacity(storename):
    """
    Return the fuel capacity of a store.

    :param storename: The name of the store.
    :raises RuntimeError: If `storename` does not correspond to a store.
    :return: The fuel capacity of the store as a number.
    """
    if _storehasproperty(storename, "fuelcapacity"):
        return _storeproperty(storename, "fuelcapacity")
    else:
        return 0


################################################################################


def _storesweight(self, storesfuelfraction=1):
    totalweight = 0
    for loadstation, storename in self._stores.items():
        totalweight += _storeweight(storename, storesfuelfraction)
    return totalweight


def _storesload(self, storesfuelfraction=1):
    totalload = 0
    for loadstation, storename in self._stores.items():
        totalload += _storeload(storename, storesfuelfraction)
    if not glass.variants.withvariant("use house rules"):
        # Round down. See 4.3.
        totalload = int(totalload)
    return totalload


def _storesfuelcapacity(self):
    totalfuelcapacity = 0
    for loadstation, storename in self._stores.items():
        totalfuelcapacity += _storefuelcapacity(storename)
    return totalfuelcapacity


def _storesfuelfraction(self):
    if self.storesfuel() is None or self._storesfuelcapacity() == 0:
        return 0
    else:
        return self.storesfuel() / self._storesfuelcapacity()


################################################################################


def _initstores(self, stores):

    newstores = {}
    for loadstation, name in stores.items():
        if isinstance(loadstation, int):
            loadstation = str(loadstation)
        if not isinstance(loadstation, str):
            raise RuntimeError("invalid load station %r." % loadstation)
        if name not in _storedict:
            raise RuntimeError("invalid store %r." % name)
        newstores[loadstation] = name
    self._stores = newstores

    self._showstores()
    self._updateconfiguration()


################################################################################


def _updateconfiguration(self):
    """
    Updated the configuration based on the current stores.
    """

    # If no stores are specified, do nothing.
    if self._stores == None:
        return

    assert self._aircraftdata.hasstoreslimits()

    # See rule 4.2 and 4.3.

    storesweight = self._storesweight(self._storesfuelfraction())
    storesload = self._storesload(self._storesfuelfraction())

    if storesweight > self._aircraftdata.storeslimit("DT"):
        raise RuntimeError("stores weight exceeds the aircraft's limit.")

    # The expressions below are correct whether we round down load values or not.
    if storesload < self._aircraftdata.storeslimit("CL") + 1:
        self._configuration = "CL"
    elif storesload < self._aircraftdata.storeslimit("1/2") + 1:
        self._configuration = "1/2"
    else:
        self._configuration = "DT"


################################################################################


def _showstores(self):

    if len(self._stores) != 0:
        self.logwhenwhat("", "stores are:")
        for loadstation, name in self._stores.items():
            self.logwhenwhat(
                "",
                "  %-2s: %-17s  %-3s / %4d / %.1f%s"
                % (
                    loadstation,
                    name,
                    _storeclass(name),
                    _storeweight(name, storesfuelfraction=self._storesfuelfraction()),
                    _storeload(name, storesfuelfraction=self._storesfuelfraction()),
                    (
                        " / %d"
                        % (_storefuelcapacity(name) * self._storesfuelfraction())
                        if _storeclass(name) == "FT"
                        else ""
                    ),
                ),
            )

        storesweight = self._storesweight(self._storesfuelfraction())

        self.logwhenwhat(
            "",
            "stores load                 is %.1f."
            % self._storesload(self._storesfuelfraction()),
        )

        self.logwhenwhat(
            "",
            "stores weight               is %d." % storesweight,
        )

        storesallowedweight = self._aircraftdata.storeslimit("DT")
        self.logwhenwhat(
            "",
            "stores weight limit         is %d." % storesallowedweight,
        )

        if self.storesfuel() is not None:

            storesnonfuelweight = self._storesweight(0)
            storesfuelweight = storesweight - storesnonfuelweight

            self.logwhenwhat(
                "",
                "stores non-fuel weight      is %d." % storesnonfuelweight,
            )
            self.logwhenwhat(
                "", "stores fuel weight          is %d." % storesfuelweight
            )

            storesfuelweightcapacity = self._storesweight(1) - storesnonfuelweight
            self.logwhenwhat(
                "",
                "stores fuel weight capacity is %d." % storesfuelweightcapacity,
            )

            storesfuelweightlimit = min(
                storesfuelweightcapacity,
                max(0, storesallowedweight - storesnonfuelweight),
            )
            self.logwhenwhat(
                "",
                "stores fuel weight limit    is %d." % storesfuelweightlimit,
            )

            self.logwhenwhat(
                "",
                "stores fuel                 is %5.1f or %3.0f%% of internal capacity."
                % (
                    self.storesfuel(),
                    math.floor(100 * self.storesfuel() / self.internalfuel()),
                ),
            )
            self.logwhenwhat(
                "",
                "stores fuel capacity.       is %5.1f or %3.0f%% of internal capacity."
                % (
                    self._storesfuelcapacity(),
                    math.floor(100 * self._storesfuelcapacity() / self.internalfuel()),
                ),
            )
            if storesfuelweightcapacity == 0:
                storesallowedfuel = 0
            else:
                storesallowedfuel = self._storesfuelcapacity() * min(
                    1, storesfuelweightlimit / storesfuelweightcapacity
                )
            self.logwhenwhat(
                "",
                "stores fuel limit           is %5.1f or %3.0f%% of internal capacity."
                % (
                    storesallowedfuel,
                    math.floor(100 * storesallowedfuel / self.internalfuel()),
                ),
            )
            self.logwhenwhat(
                "",
                "fuel limit                  is %5.1f or %3.0f%% of internal capacity."
                % (
                    self.internalfuel() + storesallowedfuel,
                    100 + math.floor(100 * storesallowedfuel / self.internalfuel()),
                ),
            )


################################################################################


def showstores(self, note=None):
    """
    Show the aircraft's stores to the log.
    """
    try:
        self._showstores()
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################


def _airtoairlaunch(stores, launched, printer=print):

    newstores = stores.copy()

    loadstation = str(launched)

    if loadstation not in stores:
        raise RuntimeError("load station %s is not loaded." % loadstation)

    if _storeclass(stores[loadstation]) not in ["IRM", "BRM", "RHM", "AHM"]:
        raise RuntimeError(
            "load station %s is not loaded with an air-to-air missile." % loadstation
        )

    missiletype = stores[loadstation]

    printer("launching %s from load station %s." % (stores[loadstation], loadstation))
    del newstores[loadstation]

    return missiletype, newstores


################################################################################


def _release(self, released):

    previousconfiguration = self._configuration

    if isinstance(released, int) or isinstance(released, str):
        releasedlist = [released]
    else:
        releasedlist = released
    releasedlist = list(str(releaseditem) for releaseditem in releasedlist)

    stores = self._stores.copy()

    for releaseditem in releasedlist:

        if releaseditem[0] in "0123456789":
            loadstation = releaseditem
            if loadstation not in stores.keys():
                raise RuntimeError("load station %s is not loaded." % loadstation)
            loadstationlist = [loadstation]
        else:
            loadstationlist = list(
                filter(
                    lambda loadstation: stores[loadstation].startswith(releaseditem),
                    stores.keys(),
                )
            )
            if len(loadstationlist) == 0:
                raise RuntimeError(
                    "no load stations are loaded with %s." % releaseditem
                )

        for loadstation in loadstationlist:
            self.logwhenwhat(
                "",
                "releases %s on load station %s." % (stores[loadstation], loadstation),
            )
            del stores[loadstation]

    self._stores = stores
    self._updateconfiguration()

    if self._configuration != previousconfiguration:
        self.logwhenwhat(
            "",
            "configuration changes from %s to %s."
            % (previousconfiguration, self._configuration),
        )


################################################################################


def release(self, *args):
    try:
        self._release(*args)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################
