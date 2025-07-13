################################################################################

import glass.jsonc
import glass.log
import glass.variants

import os
import glob

################################################################################

_storedict = {}

def _loadstores():

    global _storedict

    _storedict = {}
    
    storesdatadir = os.path.join(
        os.path.dirname(__file__), "..", "storesdata"
    )
    
    for path in sorted(glob.glob(os.path.join(storesdatadir, "*.json"))):
        try:
            with open(path, "r", encoding="utf-8") as f:
                _storedict.update(glass.jsonc.load(f))
        except FileNotFoundError:
            raise RuntimeError(
                'unable to find stores data file "%s".' % path
            )
        except glass.jsonc.JSONDecodeError as e:
            raise RuntimeError(
                'unable to read stores data file "%s": line %d: %s.'
                % (path, e.lineno, e.msg.lower())
            )

_loadstores()

################################################################################

def _class(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    return _storedict[storename][0]


def _weight(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    return _storedict[storename][1]


def _load(storename, storesfuel=0):

    # We make the crude assumption that if there is any stores fuel,
    # then none of the FTs are empty.

    empty = storesfuel is None or storesfuel == 0

    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)

    if _class(storename) == "FT" and empty:
        return _additionaldata(storename)["emptyload"]
    else:
        return _storedict[storename][2]


def _additionaldata(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    return  _storedict[storename][3]

def _fuelcapacity(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    if _class(storename) == "FT":
        return _additionaldata(storename)["fuelcapacity"]
    else:
        return 0


################################################################################


def _storestotalweight(self):
    totalweight = 0
    for loadstation, storename in self._stores.items():
        totalweight += _weight(storename)
    return totalweight


def _storestotalload(self):
    totalload = 0
    for loadstation, storename in self._stores.items():
        totalload += _load(storename, storesfuel=self.storesfuel())
    if not glass.variants.withvariant("use house rules"):
        # Round down. See 4.3.
        totalload = int(totalload)
    return totalload


def _storestotalfuelcapacity(self):
    totalfuelcapacity = 0
    for loadstation, storename in self._stores.items():
        totalfuelcapacity += _fuelcapacity(storename)
    return totalfuelcapacity


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

    totalweight = self._storestotalweight()
    totalload = self._storestotalload()

    if totalweight > self._aircraftdata.storeslimit("DT"):
        raise RuntimeError("total stores weight exceeds the aircraft capacity.")

    # The expressions below are correct whether we round down load values or not.
    if totalload < self._aircraftdata.storeslimit("CL") + 1:
        self._configuration = "CL"
    elif totalload < self._aircraftdata.storeslimit("1/2") + 1:
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
                    _class(name),
                    _weight(name),
                    _load(name, storesfuel=self.storesfuel()),
                    " / %d" % _fuelcapacity(name) if _class(name) == "FT" else "",
                ),
            )

        self.logwhenwhat(
            "", "stores total weight        is %d." % self._storestotalweight()
        )
        self.logwhenwhat(
            "", "stores total load          is %.1f." % self._storestotalload()
        )
        self.logwhenwhat(
            "", "stores total fuel capacity is %d." % self._storestotalfuelcapacity()
        )
        if self.storesfuel() is not None:
            self.logwhenwhat(
                "", "stores total fuel          is %.1f." % self.storesfuel()
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

    if _class(stores[loadstation]) not in [ "IRM", "BRM", "RHM", "AHM"]:
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
