import glass.variants


_missiledict = {
    #  In the value: [0] is the type, [1] is the base speed, [2] is the turn rate, [3] is the turn rate divisor.
    "IRM/AIM-9B": ["IRM", 10.0, "HT/2"],
    "RHM/AIM-9C": ["RHM", 18.0, "HT/2"],
    "IRM/AIM-9D": ["IRM", 18.0, "HT/2"],
    "IRM/AIM-9E": ["IRM", 10.0, "BT/2"],
    "IRM/AIM-9E2": ["IRM", 12.0, "BT/2"],
    "IRM/AIM-9G": ["IRM", 18.0, "BT/2"],
    "IRM/AIM-9H": ["IRM", 18.0, "ET/2"],
    "IRM/AIM-9J": ["IRM", 12.0, "ET/2"],
    "IRM/AIM-9J3": ["IRM", 16.0, "ET/2"],
    "IRM/AIM-9N": ["IRM", 16.0, "ET/2"],
    "IRM/AIM-9P": ["IRM", 16.0, "ET/2"],
    "IRM/AIM-9P2": ["IRM", 16.0, "ET/2"],
    "IRM/AIM-9P3": ["IRM", 16.0, "ET/2"],
    "IRM/AIM-9P4": ["IRM", 16.0, "ET/2"],
    "IRM/AIM-9L": ["IRM", 14.0, "ET/3"],
    "IRM/AIM-9M": ["IRM", 14.0, "ET/3"],
    "IRM/AIM-9M4": ["IRM", 16.0, "ET/3"],
    "IRM/AIM-9M5": ["IRM", 16.0, "ET/3"],
    "IRM/AIM-9S": ["IRM", 18.0, "ET/3"],
    "IRM/AIM-9X": ["IRM", 18.0, "ET/4"],
    "IRM/AIM-9X-II": ["IRM", 19.0, "ET/4"],
    "IRM/FGW.2": ["IRM", 12.0, "BT/2"],
    "IRM/AA-2": ["IRM", 9.0, "HT/2"],
    "IRM/AA-2A": ["IRM", 10.0, "HT/2"],
    "RHM/AA-2C": ["RHM", 14.0, "BT/1"],
    "IRM/AA-2B": ["IRM", 14.0, "ET/2"],
    "IRM/AA-2D": ["IRM", 14.0, "ET/3"],
    "IRM/AA-8": ["IRM", 15.0, "ET/3"],
    "IRM/AA-8B": ["IRM", 15.0, "ET/3"],
    "IRM/AA-8C": ["IRM", 15.0, "ET/3"],
}


def basespeed(name):
    if not name in _missiledict:
        raise RuntimeError("unknown missile %r." % name)
    return _missiledict[name][1]


def turnrate(name):
    if not name in _missiledict:
        raise RuntimeError("unknown missile %r." % name)
    rate, divisor = _missiledict[name][2].split("/")
    return rate, int(divisor)
