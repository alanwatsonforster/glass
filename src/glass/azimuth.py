"""
The :mod:`glass.azimuth` module contains functions to convert between azimuths and facings.

An azimuth is a compass direction.

A facing is a direction in the physical coordinate system. It is defined to
be 0 degrees in the direction of the positive x-axis and to increase towards the
positive y-axis. See :mod:`glass.hex` for more details.

By default, north corresponds to a facing of 90 degrees (i.e., parallel to the
positive y-axis in the physical coordinate system). This can be changed by
calling :func:`setnorth`.

"""

import glass.variants

__all__ = [
    "isvalidazimuth",
    "setnorth",
    "tofacing",
    "fromfacing"
]

_northfacing = 90


def isvalidazimuth(value):
    """
    Return whether a value is a valid azimuth.

    Normally, valid azimuths are integer multiples of 30 and the
    strings ``"N"``, ``"NNE"``, ``"NE"``, ``"ENE"``, ``"E"``, ``"SE"``, ``"SSE"``, ``"S"``, ``"SSW"``, ``"SW"``, ``"WSW"``, ``"W"``,
    ``"NW"``, ``"WNW"``, and ``"NNW"``. 

    However if the variant ``"disallow ENE/ESE/WSW/WNW"`` is selected then ``"ENE"``, ``"ESE"``,
    ``"WSW"``, and ``"WNW"`` are not valid azimuths and if the variant ``"disallow
    NE/SE/SW/NW"`` is selected then ``"NE"``, ``"SE"``, ``"SW"``, and ``"NW"`` are not valid azimuths.
    
    :param value: The value to be checked.

    :return: ``True`` if the value is a valid azimuth and ``False`` otherwise.
    
    """

    if isinstance(value, int) and value % 30 == 0:
        return True

    if value in ["N", "NNE", "E", "SSE", "S", "SSW", "W", "NNW"]:
        return True
    if not glass.variants.withvariant("disallow NE/SE/SW/NW") and value in [
        "NE",
        "SE",
        "SW",
        "NW",
    ]:
        return True
    if not glass.variants.withvariant("disallow ENE/ESE/WSW/WNW") and value in [
        "ENE",
        "ESE",
        "WSW",
        "WNW",
    ]:
        return True

    return False


def setnorth(orientation):
    """
    Set the facing of north.

    If the orientation is an integer, this is the facing that corresponds to
    north. If it is one of the strings ``"right"``, ``"up"``, ``"left"``, or ``"down"``, then
    the facing that corresponds to north is 0, 90, 180, or 270, respectively.

    :param orientation:
        The orientation argument can an integer multiple of 30 or of the
        strings ``"up"``, ``"down"``, ``"right"``, or ``"left"``.
    :return: ``None``
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
    elif isinstance(value, int) and value % 30 == 0:
        _northfacing = orientation % 360
    else:
        raise RuntimeError('"%s" is not a valid orientation for north.')


def tofacing(azimuth):
    """
    Return the facing corresponding to an azimuth.

    :param azimuth:
        An azimuth. It must be a valid azimuth in the sense of
        :func:`isvalidazimuth`.
    :return: The facing corresponding to the azimuth argument as an integer
        between 0 and 330 inclusive.
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
    Return the azimuth corresponding to a facing.

    Normally, one of the strings ``"N"``, ``"NNE"``, ``"ENE"``, ``"E"``,
    ``"ESE"``, ``"SSE"``, ``"S"``, ``"SSW"``, ``"WSW"``, ``"W"``, ``"WNW"``, or
    ``"NNW"`` is returned.

    However, if the variant ``"prefer NE/SE/SW/NW"`` is selected, then ``"NE"``,
    ``"SE"``, ``"SW"``, and ``"NW"`` are returned instead of ``"ENE"``,
    ``"ESE"``, ``"WSW"``, and ``"WNW"``.

    :param facing:
        A facing. It must be an integer multiple of 30.
    :return: The azimuth corresponding to the facing argument as a string.
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

    assert isinstance(facing, int) and facing % 30 == 0

    azimuth = (_northfacing - facing) % 360
    if azimuth % 30 == 0:
        return named[azimuth // 30]
    else:
        return azimuth
