"""
The :mod:`glass.altitude` module contains functions to do with altitude.

Altitudes are non-negative integers.

Altitude carries are represented separately from altitudes. They are numbers
from 0 (inclusive) to 1 (exclusive).


"""

import glass.map
import glass.hex

__all__ = [
    "isvalidaltitude",
    "isvalidaltitudecarry",
    "checkisvalidaltitude",
    "adjustaltitude",
    "altitudeband",
    "terrainaltitude",
]


def isvalidaltitude(value):
    """
    Return whether a value is a valid altitude.

    Valid altitudes are non-negative integers.

    :param value: The value to be checked
    :return: ``True`` if the value is a valid altitude.
    """

    return isinstance(value, int) and 0 <= value


def isvalidaltitudecarry(value):
    """

    Return whether a value is a valid altitude carry.

    Valid altitude carries are numbers from 0 (inclusive) to 1 (exclusive).

    :param value: The value to be checked
    :return: ``True`` if the value is a valid altitude cary.
    """

    return isinstance(value, (int, float)) and value <= x and value < 1


def checkisvalidaltitude(value):
    """
    Raise an exception is a value is not a valid altitude.

    :param value: The value to be checked.
    :returns: ``None``

    :raises RuntimeError: If the given value is not a valid altitude. in
        the sense of :func:`isvalidaltitude`.
    
    """

    if not isvalidaltitude(value):
        raise RuntimeError("%r is not a valid altitude." % value)
    return None


def adjustaltitude(altitude, altitudecarry, altitudechange):
    """
    Return an new altitude and altitude carry after applying an altitude change.

    The new values of the altitude and altitude carry are obtained by summing
    the original ones and the altitude change, and then separating the result
    into integral and fractional parts.

    If the altitude change is negative, it must be integral and the altitude
    carry must be zero.

    :param altitude: The initial altitude.
    :param altitudecarry: The initial altitude carry.
    :param altitudechange: The change in the altitude.
    :returns: A tuple containing the new altitude and the new altitude carry
        after the adjustment.

    """

    # See rule 8.1.4.

    assert isvalidaltitude(altitude)
    assert isvalidaltitudecarry(altitudecarry)
    assert isinstance(altitudechange, (int, float))

    if altitudechange < 0:

        # Carry is only for climbing.
        assert altitudecarry == 0
        assert altitudechange % 1 == 0
        altitude += altitudechange

    else:

        altitude += altitudecarry + altitudechange
        altitudecarry = altitude % 1

    altitude = int(altitude)

    # We're working in float, and altitudecarry can be multiples of 1/12
    # (raw CC of 0.25 multipled by the supersonic factor of 2/3) which
    # can give a rounding error. Therefore, we check against full
    # altitude levels with a tolerance.

    tolerance = 1e-6
    if altitudecarry < tolerance:
        altitudecarry = 0
    elif altitudecarry > 1 - tolerance:
        altitudecarry = 0
        altitude += 1

    if altitude < 0:
        altitude = 0
        altitudecarry = 0

    assert isvalidaltitude(altitude)
    assert isvalidaltitudecarry(altitudecarry)

    return altitude, altitudecarry


def altitudeband(altitude):
    """
    Return the altitude band corresponding to altitude.

    :param altitude: The altitude.
    :returns: A string containing the code for the altitude band.
    """

    assert isvalidaltitude(altitude)

    # See rule 8.0.

    if altitude <= 7:
        return "LO"
    elif altitude <= 16:
        return "ML"
    elif altitude <= 25:
        return "MH"
    elif altitude <= 35:
        return "HI"
    elif altitude <= 45:
        return "VH"
    elif altitude <= 60:
        return "EH"
    else:
        return "UH"


def terrainaltitude(x, y):
    """
    Return the altitude of the terrain.

    :param x:
    :param y: The ``x`` and ``y`` parameters are the hex coordinates of a hex
        location that must correspond to a hex center or hex-side center.
    :return: The terrain altitude at the location.
    """

    assert glass.hex.isvalid(x, y)

    if glass.map.isonmap(x, y):
        return glass.map.altitude(x, y)
    else:
        return 0
