import apxo.variants as apvariants


_missiledict = {
    #  In the value: [0] is the type and [1] is the base speed.
    "IRM/AIM-9B": ["IRM", 10.0],
    "RHM/AIM-9C": ["RHM", 18.0],
    "IRM/AIM-9D": ["IRM", 18.0],
    "IRM/AIM-9E": ["IRM", 10.0],
    "IRM/AIM-9E2": ["IRM", 12.0],
    "IRM/AIM-9G": ["IRM", 18.0],
    "IRM/AIM-9H": ["IRM", 18.0],
    "IRM/AIM-9J": ["IRM", 12.0],
    "IRM/AIM-9J3": ["IRM", 16.0],
    "IRM/AIM-9N": ["IRM", 16.0],
    "IRM/AIM-9P": ["IRM", 16.0],
    "IRM/AIM-9P2": ["IRM", 16.0],
    "IRM/AIM-9P3": ["IRM", 16.0],
    "IRM/AIM-9P4": ["IRM", 16.0],
    "IRM/AIM-9L": ["IRM", 14.0],
    "IRM/AIM-9M": ["IRM", 14.0],
    "IRM/AIM-9M4": ["IRM", 16.0],
    "IRM/AIM-9M5": ["IRM", 16.0],
    "IRM/AIM-9S": ["IRM", 18.0],
    "IRM/AIM-9X": ["IRM", 18.0],
    "IRM/AIM-9X-II": ["IRM", 19.0],
    "IRM/FGW.2": ["IRM", 12.0],
    "IRM/AA-2": ["IRM", 9.0],
    "IRM/AA-2A": ["IRM", 10.0],
    "IRM/AA-2B": ["IRM", 14.0],
    "RHM/AA-2C": ["RHM", 14.0],
    "IRM/AA-2D": ["IRM", 14.0],
    "IRM/AA-8": ["IRM", 15.0],
    "IRM/AA-8B": ["IRM", 15.0],
    "IRM/AA-8C": ["IRM", 15.0],
}


def basespeed(name):
    if not name in _missiledict:
        raise RuntimeError("unknown missile %r." % name)
    return _missiledict[name][1]
