import glass.variants

_northfacing = 90


def isvalidazimuth(azimuth):
    """
    Return True if the argument is a valid azimuth, otherwise return
    False.

    Normally, valid azimuths are integers and the strings: N, NNE, NE,
    ENE, E, SE, SSE, S, SSW, SW, WSW, W, NW, WNW, NNW. However If the
    variant "disallow ENE/ESE/WSW/WNW" is selected, these are not valid
    azimuths and if the variant "disallow NE/SE/SW/NW" is selected, these
    are also not valid azimuths.
    """

    if isinstance(azimuth, int):
        return True

    if azimuth in ["N", "NNE", "E", "SSE", "S", "SSW", "W", "NNW"]:
        return True
    if not glass.variants.withvariant("disallow NE/SE/SW/NW") and azimuth in [
        "NE",
        "SE",
        "SW",
        "NW",
    ]:
        return True
    if not glass.variants.withvariant("disallow ENE/ESE/WSW/WNW") and azimuth in [
        "ENE",
        "ESE",
        "WSW",
        "WNW",
    ]:
        return True

    return False


def setnorth(orientation):
    """
    Set the orientation of north. The orientation argument can be one of the
    strings "up", "down", "right", or "left".
    """

    global _northfacing
    if orientation == "right":
        _northfacing = 0
    elif orientation == "up":
        _northfacing = 90
    elif orientation == "left":
        _northfacing = 180
    elif orientation == "down":
        _northfacing = 270
    else:
        raise RuntimeError('"%s" is not a valid orientation for north.')


def tofacing(azimuth):
    """
    Return the facing corresponding to the azimuth argument.
    """

    if not isvalidazimuth(azimuth):
        raise RuntimeError("invalid azimuth %r." % azimuth)

    named = {
        "N": 0,
        "NNE": 30,
        "NE": 60,
        "ENE": 60,
        "E": 90,
        "SE": 120,
        "ESE": 120,
        "SSE": 150,
        "S": 180,
        "SSW": 210,
        "SW": 240,
        "WSW": 240,
        "W": 270,
        "NW": 300,
        "WNW": 300,
        "NNW": 330,
    }
    if azimuth in named:
        azimuth = named[azimuth]

    return (_northfacing - azimuth) % 360


def fromfacing(facing):
    """
    Return the azimuth corresponding to the facing argument.

    If the azimuth is a multiple of 30 degrees, the corresponding string
    "N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW",
    or "NNW" is returned. Otherwise, a number is returned, giving the
    azimuth in degrees from north through east.

    If the variant "prefer NE/SE/SW/NW" is selected, these are returned
    instead of ENE/ESE/WSW/WNW.
    """

    if glass.variants.withvariant("prefer NE/SE/SW/NW"):
        named = ["N", "NNE", "NE", "E", "SE", "SSE", "S", "SSW", "SW", "W", "NW", "NNW"]
    else:
        named = [
            "N",
            "NNE",
            "ENE",
            "E",
            "ESE",
            "SSE",
            "S",
            "SSW",
            "WSW",
            "W",
            "WNW",
            "NNW",
        ]

    azimuth = (_northfacing - facing) % 360
    if azimuth % 30 == 0:
        return named[azimuth // 30]
    else:
        return azimuth
