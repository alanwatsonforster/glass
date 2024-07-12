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
    "FT/1400L": ["FT", 2700, 4.0, 3.0, 120],
    "FT/1700L": ["FT", 3000, 5.0, 3.5, 140],
    "FT/1900L": ["FT", 3500, 6.0, 4.0, 175],
    "FT/2200L": ["FT", 4500, 8.0, 5.0, 200],
    "FT/750gal": ["FT", 6000, 10, 7.0, 240],        # B-52 only
    "FT/3000gal": ["FT", 20000, 20, 14.0, 975],     # B-52 only
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
    "RP/LAU-37": ["RP", 850, 3.5],
    # Soviet
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
    "BB/BLU-1": ["BB", 750, 2.5],
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
    "BB/PLAB-250": ["BB", 550, 2.0],
    # Air-to-air missiles
    # Soviet
    "IRM/AA-2"  : ["IRM", 160, 1.0],
    "IRM/AA-2A" : ["IRM", 160, 1.0],
    "IRM/AA-2B" : ["IRM", 180, 1.0],
    "RHM/AA-2C" : ["IRM", 200, 1.0],
    "IRM/AA-2D" : ["IRM", 200, 1.0],
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


def _load(storename, fuel=0):

    # We make the crude assumption that if there is any external fuel,
    # then none of the FTs are empty.

    empty = fuel is None or fuel == 0

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


def totalweight(stores):
    totalweight = 0
    for loadpoint, storename in stores.items():
        totalweight += _weight(storename)
    return totalweight


def totalload(stores, fuel=0):
    totalload = 0
    for loadpoint, storename in stores.items():
        totalload += _load(storename, fuel=fuel)
    # Round down. See 4.3.
    totalload = int(totalload)
    return totalload


def totalfuelcapacity(stores):
    totalfuelcapacity = 0
    for loadpoint, storename in stores.items():
        totalfuelcapacity += _fuelcapacity(storename)
    return totalfuelcapacity


################################################################################


def _showstores(stores, printer=print, fuel=0):

    printer("stores are:")
    for loadpoint, name in sorted(stores.items()):
        printer(
            "  %-2s: %-17s  %2s / %4d / %.1f%s"
            % (
                loadpoint,
                name,
                _class(name),
                _weight(name),
                _load(name, fuel=fuel),
                " / %d" % _fuelcapacity(name) if _class(name) == "FT" else "",
            )
        )
    printer("stores total weight        is %d." % totalweight(stores))
    printer("stores total load          is %d." % totalload(stores, fuel=fuel))
    printer("stores total fuel capacity is %d." % totalfuelcapacity(stores))
    if fuel is not None:
        printer("stores total fuel          is %.1f." % fuel)


################################################################################


def _checkstores(stores):

    newstores = {}

    for loadpoint, name in stores.items():

        if isinstance(loadpoint, int):
            loadpoint = "%d" % loadpoint
        if not isinstance(loadpoint, str):
            raise RuntimeError("invalid load-point %r." % loadpoint)

        if name not in _storedict:
            raise RuntimeError("invalid store %r." % name)

        newstores[loadpoint] = name

    return newstores


################################################################################


def _release(stores, released, printer=print):

    newstores = stores.copy()

    if released in [
        "FT",
        "IRM",
        "BRM",
        "RHM",
        "AHM",
        "ARM",
        "BB",
        "BS",
        "BG",
        "RK",
        "RP",
        "RG",
        "WR",
        "GP",
        "EP",
        "DP",
        "LP",
    ]:

        for loadpoint, name in sorted(stores.items()):
            if _class(name) == released:
                printer("releasing %s: %s." % (loadpoint, name))
                del newstores[loadpoint]

    else:

        loadpoint = released

        if loadpoint not in stores:
            raise RuntimeError("load-point %s is not loaded." % loadpoint)

        printer("releasing %s: %s." % (loadpoint, stores[loadpoint]))
        del newstores[loadpoint]

    return newstores


################################################################################
