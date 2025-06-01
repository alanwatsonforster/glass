################################################################################

import glass.log

################################################################################

_storedict = {
    # In the value, [0] is the class, [1] is the weight, and [2] is the
    # load. For FTs, [3] is the empty load and [4] is the fuel capacity.
    # FTs
    "FT/250L": ["FT", 550, 1.5, 1.0, 25],
    "FT/400L": ["FT", 700, 2.0, 1.0, 30],
    "FT/450L": ["FT", 800, 2.5, 1.5, 40],
    "FT/600L": ["FT", 1100, 3.0, 2.0, 50],
    "FT/700L": ["FT", 1300, 3.0, 2.0, 60],
    "FT/850L": ["FT", 1500, 3.5, 2.5, 75],
    "FT/1000L": ["FT", 1800, 3.5, 2.5, 85],
    "FT/1200L": ["FT", 2200, 4.0, 2.5, 100],
    "FT/1250L": ["FT", 2300, 4.0, 2.5, 105],
    "FT/1400L": ["FT", 2700, 4.0, 3.0, 120],
    "FT/1700L": ["FT", 3000, 5.0, 3.5, 140],
    "FT/1800L": ["FT", 3200, 5.0, 3.5, 150],
    "FT/1900L": ["FT", 3500, 6.0, 4.0, 175],
    "FT/2200L": ["FT", 4500, 8.0, 5.0, 200],
    "FT/750gal": ["FT", 6000, 10, 7.0, 240],  # B-52 only
    "FT/3000gal": ["FT", 20000, 20, 14.0, 975],  # B-52 only
    # WRs
    "WR/DR": ["WR", 100, 1.0],
    "WR/TR": ["WR", 100, 1.0],
    "WR/MR": ["WR", 200, 2.0],
    "WR/MDR": ["WR", 100, 1.0],
    "WR/ARM-DR": ["WR", 200, 2.0],
    # RK Weapons
    # US
    "RK/HVAR": ["RK", 140, 1.0],
    "RK/Tiny Tim": ["RK", 1200, 2.0],
    # Soviet
    "RK/S-8": ["RK", 25, 0.5],
    "RK/TRS-190": ["RK", 100, 1.0],
    "RK/ARS-212": ["RK", 260, 1.0],
    "RK/S-24": ["RK", 350, 1.5],
    # RP Weapons
    # US
    "RP/LAU-68": ["RP", 250, 2.0],
    "RP/LAU-3A": ["RP", 450, 3.0],
    "RP/LAU-10": ["RP", 550, 3.0],
    "RP/LAU-33": ["RP", 200, 2.9],  # From errata.
    "RP/LAU-37": ["RP", 850, 3.5],
    # Soviet
    "RP/ORO-8K": ["RP", 175, 2.0],
    "RP/UV-8-57": ["RP", 175, 2.0],
    "RP/UV-16-57": ["RP", 300, 3.0],
    "RP/UV-32-57": ["RP", 500, 3.5],
    # BB Weapons
    # US
    "BB/M30": ["BB", 100, 0.5],
    "BB/M57": ["BB", 250, 1.5],
    "BB/M64": ["BB", 500, 2.0],
    "BB/M65": ["BB", 1000, 3.0],
    "BB/M66": ["BB", 2000, 4.0],
    "BB/M74": ["BB", 100, 0.5],
    "BB/M76": ["BB", 500, 1.5],
    "BB/HD/BLU-1": ["BB", 750, 2.5],  # HD only from errata.
    "BB/M117": ["BB", 750, 2.0],
    "BB/HD/M117": ["BB", 750, 2.0],
    "BB/M118": ["BB", 3000, 5.0],
    "BB/Mk81": ["BB", 250, 1.0],
    "BB/HD/Mk81": ["BB", 250, 1.0],
    "BB/Mk82": ["BB", 500, 1.5],
    "BB/HD/Mk82": ["BB", 500, 1.5],
    "BB/Mk83": ["BB", 1000, 2.5],
    "BB/HD/Mk83": ["BB", 1000, 2.5],
    "BB/Mk84": ["BB", 2000, 3.0],
    "BB/HD/BLU-10": ["BB", 250, 1.0],
    "BB/HD/BLU-11": ["BB", 500, 1.5],
    "BB/HD/BLU-27": ["BB", 750, 2.5],  # Same properties as BLU-1.
    "BB/HD/Mk77": ["BB", 750, 2.0],
    "BB/HD/Mk79": ["BB", 1000, 2.5],
    "BB/CBU-20": ["BB", 500, 1.5],
    "BB/HD/CBU-20": ["BB", 500, 1.5],
    "BB/CBU-41": ["BB", 850, 2.0],
    "BB/HD/CBU-41": ["BB", 850, 2.0],
    "BB/CBU-58": ["BB", 800, 2.0],
    "BB/CBU-59": ["BB", 750, 2.0],
    "BB/HD/CBU-59": ["BB", 750, 2.0],
    "BB/CBU-71": ["BB", 800, 2.0],
    "BB/HD/CBU-71": ["BB", 800, 2.0],
    # Soviet
    "BB/FAB-50": ["BB", 110, 1.0],
    "BB/FAB-100": ["BB", 225, 1.5],
    "BB/FAB-250": ["BB", 550, 2.0],
    "BB/FAB-500": ["BB", 1100, 3.0],
    "BB/FAB-750": ["BB", 1650, 3.5],
    "BB/FAB-1000": ["BB", 2200, 4.0],
    "BB/ZAB-100": ["BB", 225, 1.5],
    "BB/ZAB-250": ["BB", 550, 2.0],
    "BB/ZAB-1000": ["BB", 2200, 4.0],
    "BB/HD/PLAB-250": ["BB", 550, 2.0],
    # Air-to-air missiles
    # US
    "IRM/AIM-9B": ["IRM", 160, 1.0],
    "RHM/AIM-9C": ["RHM", 190, 1.0],
    "IRM/AIM-9D": ["IRM", 200, 1.0],
    "IRM/AIM-9E": ["IRM", 170, 1.0],
    "IRM/AIM-9E2": ["IRM", 170, 1.0],
    "IRM/AIM-9G": ["IRM", 190, 1.0],
    "IRM/AIM-9H": ["IRM", 185, 1.0],
    "IRM/AIM-9J": ["IRM", 175, 1.0],
    "IRM/AIM-9J3": ["IRM", 175, 1.0],
    "IRM/AIM-9N": ["IRM", 175, 1.0],
    "IRM/AIM-9P": ["IRM", 170, 1.0],
    "IRM/AIM-9P2": ["IRM", 170, 1.0],
    "IRM/AIM-9P3": ["IRM", 170, 1.0],
    "IRM/AIM-9P4": ["IRM", 170, 1.0],
    "IRM/AIM-9L": ["IRM", 190, 1.0],
    "IRM/AIM-9M": ["IRM", 190, 1.0],
    "IRM/AIM-9M4": ["IRM", 190, 1.0],
    "IRM/AIM-9M5": ["IRM", 190, 1.0],
    "IRM/AIM-9S": ["IRM", 190, 1.0],
    "IRM/AIM-9X": ["IRM", 190, 1.0],
    "IRM/AIM-9X-II": ["IRM", 190, 1.0],
    "IRM/FGW.2": ["IRM", 170, 1.0],
    # Soviet
    "IRM/AA-2": ["IRM", 160, 1.0],
    "IRM/AA-2A": ["IRM", 160, 1.0],
    "IRM/AA-2B": ["IRM", 180, 1.0],
    "RHM/AA-2C": ["RHM", 200, 1.0],
    "IRM/AA-2D": ["IRM", 200, 1.0],
    "IRM/AA-8": ["IRM", 140, 1.0],
    "IRM/AA-8B": ["IRM", 140, 1.0],
    "IRM/AA-8C": ["IRM", 150, 1.0],
}

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
        return _storedict[storename][3]
    else:
        return _storedict[storename][2]


def _fuelcapacity(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    if _class(storename) == "FT":
        return _storedict[storename][4]
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

    if totalload <= self._aircraftdata.storeslimit("CL"):
        self._configuration = "CL"
    elif totalload <= self._aircraftdata.storeslimit("1/2"):
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
                "  %-2s: %-17s  %2s / %4d / %.1f%s"
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
            "", "stores total load          is %d." % self._storestotalload()
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

    if _class(stores[loadstation]) not in ["IRM", "BRM", "RHM", "AHM"]:
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

    stores = self._stores

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
