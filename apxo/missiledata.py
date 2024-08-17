import apxo.variants as apvariants


_missiledict = {
    #  In the value: [0] is the type and [1] is the base speed.
    "IRM/AIM-9L": ["IRM", 14.0],
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
