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


def _isvalidstore(storename):
    """
    Return whether a store name is valid.

    :param storename: The name of a store as a string.
    :return: `True` if the store name corresponds to a valid store, otherwise `False`.
    """
    return storename in _storedict


def _storehasproperty(storename, propertyname):
    """
    Return whether a store has a property.

    :param storename: The name of the store as a string.
    :param propertyname: The name of the property as a string.
    :raises RuntimeError: If `storename` does not correspond to a valid store.
    :return: `True` if the store has the name property, otherwise `False`.
    """
    if not _isvalidstore(storename):
        raise RuntimeError("invalid store %r." % storename)
    return propertyname in _storedict[storename]


def _storeproperty(storename, propertyname):
    """
    Return the value of a property of a store.

    :param storename: The name of the store as a string.
    :param propertyname: The name of the property as a string.
    :raises RuntimeError: If `storename` does not correspond to a valid store or
        `propertyname` does not correspond to a valid property of the named
        store.
    :return: The value of the property.
    """
    if not _isvalidstore(storename):
        raise RuntimeError("invalid store %r." % storename)
    if not propertyname in _storedict[storename]:
        raise RuntimeError("invalid property %r." % propertyname)
    return _storedict[storename][propertyname]


def _storeclass(storename):
    """
    Return the class of a store.

    :param storename: The name of the store as a string.
    :param propertyname: The name of the property as a string.
    :raises RuntimeError: If `storename` does not correspond to a valid store.
    :return: The class of the store as a string. One of the following strings:
       `"AHM"`, `"ARM"`, `"ASM"`, `"BB"`, `"BG"`, `"BRM"`, `"BS"`, `"DP"`,
       `"EP"`, `"FT"`, `"GP"`, `"IRM"`, `"LP"`, `"OP"`, `"MRT"`, `"RG"`,
       `"RHM"`, `"RK"`, `"RP"`,  `"RPT"`,`"RS"`, and `"WR"`.
    """
    return _storeproperty(storename, "class")


def _storeweight(storename, storesfuelfraction):
    """
    Return the weight of a store.

    :param storename: The name of the store as a string.
    :param storesfuelfraction: The fraction of fuel in the store. Ignored unless
        the store is an FT/RPT/MRT.
    :raises RuntimeError: If `storename` does not correspond to a valid store.
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
    :param storesfuelfraction: The fraction of fuel in the store. Ignored unless
        the store is an FT/RPT/MRT.
    :raises RuntimeError: If `storename` does not correspond to a valid store.
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
    :raises RuntimeError: If `storename` does not correspond to a valid store.
    :return: The fuel capacity of the store as a number.
    """
    if _storehasproperty(storename, "fuelcapacity"):
        return _storeproperty(storename, "fuelcapacity")
    else:
        return 0


################################################################################


def _storesweight(self, storesfuelfraction):
    """
    Return the total weight of the stores of an aircraft.

    :param storesfuelfraction: The fraction of fuel in each FT/RPT/MRT.
    :raises RuntimeError: If the name of any store does not correspond to a
        valid store.
    :return: The total weight of the stores as a number.
    """
    weight = 0
    for loadstationname, storename in self._stores.items():
        weight += _storeweight(storename, storesfuelfraction)
    return weight


def _storesload(self, storesfuelfraction=1):
    """
    Return the total load of the stores of an aircraft.

    :param storesfuelfraction: The fraction of fuel in each FT/RPT/MRT.
    :raises RuntimeError: If the name of any store does not correspond to a
        valid store.
    :return: The total load of the stores as a number.
    """
    load = 0
    for loadstationname, storename in self._stores.items():
        load += _storeload(storename, storesfuelfraction)
    if not glass.variants.withvariant("use house rules"):
        # Round down. See 4.3.
        load = int(load)
    return load


def _storesfuelcapacity(self):
    """
    Return the total fuel capacity of the stores of an aircraft.

    :raises RuntimeError: If the name of any store does not correspond to a
        valid store.
    :return: The total fuel capacity of the stores as a number.
    """
    fuelcapacity = 0
    for loadstationname, storename in self._stores.items():
        fuelcapacity += _storefuelcapacity(storename)
    return fuelcapacity


def _storesfuelfraction(self):
    """
    Return the fuel fraction of the stores of an aircraft.

    The fuel fraction is 0 if fuel is not being tracked or no stores are
    FTs/RPTs/MRTs. Otherwise it is the total fuel in the stores divided by the
    total fuel capacity of the stores.

    :raises RuntimeError: If the name of any store does not correspond to a
        valid store.
    :return: The fuel fraction of the stores as a number.
    """
    if self.storesfuel() is None or self._storesfuelcapacity() == 0:
        return 0
    else:
        return self.storesfuel() / self._storesfuelcapacity()


################################################################################


def _setstores(self, stores):
    """
    Set the stores of an aircraft.

    :param stores: `None` or a dictionary specifying the stores. If `None`, then
        there are no stores. If a dictionary, the keys are the load station
        names and the values are the corresponding store names.
    :raises RuntimeError: If any load station name is invalid. Valid load
        station names are positive integers and strings.
    :raises RuntimeError: If any store name does not correspond to a valid
        store.
    :raises RuntimeError: If the total stores weight exceeds the aircraft's
        limit.
    """

    if stores is not None:
        # Validate the stores and convert the load station names to strings.
        newstores = {}
        for loadstationname, storename in stores.items():
            if isinstance(loadstationname, int) and loadstationname > 0:
                loadstationname = str(loadstationname)
            if not isinstance(loadstationname, str):
                raise RuntimeError("invalid load station %r." % loadstationname)
            if not _isvalidstore(storename):
                raise RuntimeError("invalid store name %r." % storename)
            newstores[loadstationname] = storename
        stores = newstores

    self._stores = stores

    if stores is not None:
        assert self._aircraftdata.hasstoreslimits()
        storesweight = self._storesweight(self._storesfuelfraction())
        if storesweight > self._aircraftdata.storeslimit("DT"):
            raise RuntimeError("stores weight exceeds the aircraft's limit.")

    self._updateconfiguration()


################################################################################


def _updateconfiguration(self):
    """
    Update the configuration of an aircraft based on its current stores.

    The configuration will be "CL", "1/2", or "DT" depending on the total stores
    load.

    :raises RuntimeError: If any store name does not correspond to a valid
        store.
    """

    if self._stores == None:
        self._configuration = "CL"
    else:
        load = self._storesload(self._storesfuelfraction())
        # The expressions below are correct whether we round down load values or
        # not.
        if load < self._aircraftdata.storeslimit("CL") + 1:
            self._configuration = "CL"
        elif load < self._aircraftdata.storeslimit("1/2") + 1:
            self._configuration = "1/2"
        else:
            self._configuration = "DT"


################################################################################


def _logstores(self):
    """
    Log the stores of an aircraft.
    """

    if len(self._stores) != 0:
        self.logwhenwhat("", "stores are:")
        for loadstationname, name in self._stores.items():
            self.logwhenwhat(
                "",
                "  %-2s: %-17s  %-3s / %4d / %.1f%s"
                % (
                    loadstationname,
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
            self.logwhenwhat(
                "",
                "fuel weight limit           is %4.0f."
                % ((self.internalfuel() + storesallowedfuel) * 20),
            )


################################################################################


def logstores(self, note=None):
    """
    Log the stores of an aircraft

    :param note: An additional note. Defaults to `None`.
    """

    try:
        self._logstores()
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################


def _airtoairlaunch(self, loadstationname, failed=False, failedbeforelaunch=False):
    """
    Launch an air-to-air missile.

    :param loadstationname: The name of the load station of the missile being
        launched. Either an integer or a string.
    :param failed: Whether the missile failed after launch, defaults to False
    :param failedbeforelaunch: Whether the missile failed before launch,
        defaults to False
    :raises RuntimeError: If the specified load station is not loaded.
    :raises RuntimeError: If the specified load station is not loaded with an
        air-to-air missile.
    :return: The name of the missile, if it launched successfully, or `None` if
        it failed to launch.
    """

    loadstationname = str(loadstationname)

    stores = self._stores.copy()

    if loadstationname not in stores:
        raise RuntimeError("load station %s is not loaded." % loadstationname)

    if _storeclass(stores[loadstationname]) not in ["IRM", "BRM", "RHM", "AHM"]:
        raise RuntimeError(
            "load station %s is not loaded with an air-to-air missile."
            % loadstationname
        )

    self.logcomment(
        "launching %s from load station %s."
        % (stores[loadstationname], loadstationname)
    )
    if failedbeforelaunch:
        self.logcomment("launch failed but missile not lost.")
        storename = None
    elif failed:
        self.logcomment("launch failed and missile lost.")
        storename = None
        del stores[loadstationname]
    else:
        self.logcomment("launch succeeded.")
        storename = stores[loadstationname]
        del stores[loadstationname]

    self._stores = stores

    previousconfiguration = self._configuration
    self._updateconfiguration()
    if self._configuration != previousconfiguration:
        self.logwhenwhat(
            "",
            "configuration changes from %s to %s."
            % (previousconfiguration, self._configuration),
        )

    return storename


################################################################################


def _release(self, released):
    """
    Release one or more stores.

    The stores to be released are either specified explicitly by their load
    point names or implicitly when their names match the given prefix.

    :param released: A specification of the idems to be released. This may be a
        single load station name (an integer or string), a list of load station
        names, or a store name prefix.
    :raises RuntimeError: If a specified load point is not loaded.
    :raises RuntimeError: If no store names match the prefix.
    """

    if isinstance(released, int) or isinstance(released, str):
        releasedlist = [released]
    else:
        releasedlist = released
    releasedlist = list(str(releaseditem) for releaseditem in releasedlist)

    stores = self._stores.copy()

    for releaseditem in releasedlist:

        if releaseditem[0] in "0123456789":
            loadstationname = releaseditem
            if loadstationname not in stores.keys():
                raise RuntimeError("load station %s is not loaded." % loadstationname)
            loadstationlist = [loadstationname]
        else:
            loadstationlist = list(
                filter(
                    lambda loadstationname: stores[loadstationname].startswith(
                        releaseditem
                    ),
                    stores.keys(),
                )
            )
            if len(loadstationlist) == 0:
                raise RuntimeError(
                    "no load stations are loaded with %s." % releaseditem
                )

        for loadstationname in loadstationlist:
            self.logwhenwhat(
                "",
                "releases %s on load station %s."
                % (stores[loadstationname], loadstationname),
            )
            del stores[loadstationname]

    self._stores = stores

    previousconfiguration = self._configuration
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
