"""
The :mod:`glass.hex` module contains functions to manipulate hex coordinates.

Glass works with three coordinate systems:

- Hex coordinates. These refer to a hex grid in the normal orientation with two
  side of each hex parallel to the x-axis. The x-coordinate increases by 1 from
  one column to the next. The y-coordinate increases by one from one hex to the
  next. This coordinate system is useful for referring to locations tied to the
  hex grid, but it has the feature that the unit of length is not the same in
  both directions, so the normal rules of geometry in Cartesian coordinates
  cannot be used directly. The origin coincides with a hex center.

- Physical coordinates. The origin and the direction of the axes of the physical
  coordinate system correspond with those in the hex coordinate system. The
  y-coordinates in the physical and hex systems are the same. Furthermore, both
  the x-axis and the y-axis have the same unit of length, so the normal rules of
  geometry in Cartesian coordinates can be used directly.

- Canvas coordinates. These are used for drawing the map and are described in
  :mod:`glass.draw`.
  
To convert an x-coordinate in the hex system to one in the physical system,
multiply it by the square root of 3/4 (about 0.866). To convert an x-coordinate
in the physical system to one in the hex system, divide by the same factor.

One advantage of hex coordinates is that all hex centers and hex-side centers
have coordinates that are multiples of 1/4, and so their coordinates up to very
large magnitudes can be represented exactly as floats.

"""

import math


def tophysicalxy(x, y):
    """
    Return the physical location corresponding to a hex location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location.

    :return: The `x` and `y` coordinates of the physical location corresponding
        to the hex location.
    """

    return x * math.sqrt(3 / 4), y


def fromphysicalxy(x, y):
    """
    Return the hex location corresponding to a physical location.

    :param x: 
    :param y: The `x` and `y` parameters are the coordinates of the physical
        location.

    :return: The `x` and `y` coordinates of the hex location corresponding to
        the physical location.
    """

    return x / math.sqrt(3 / 4), y


def ishex(x, y):
    """
    Return whether a hex location corresponds to a hex center.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location.

    :return: ``True`` if the point (x,y) in hex coordinates corresponds to a hex
        center, otherwise ``False``.
    """

    if x % 2 == 0.0 and y % 1.0 == 0.00:
        return True
    elif x % 2 == 1.0 and y % 1.0 == 0.50:
        return True
    else:
        return False


def ishexside(x, y):
    """
    Return whether a hex location corresponds to a hex-side center.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location.

    :return: ``True`` if the point (x,y) in hex coordinates corresponds to a
        hex-side center, otherwise ``False``.
    """

    if x % 2 == 0.0 and y % 1.0 == 0.5:
        return True
    elif x % 2 == 0.5 and y % 0.5 == 0.25:
        return True
    elif x % 2 == 1.0 and y % 1.0 == 0.0:
        return True
    elif x % 2 == 1.5 and y % 0.5 == 0.25:
        return True
    else:
        return False


def isvalid(x, y, facing=None):
    """
    Return whether a hex location and facing are valid.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location.
    :param facing: Either ``None`` or a number specifying the facing in degrees.

    :return:
        ``True`` if the location (x,y) in hex coordinates corresponds to a hex
        center or hex-side side and the facing, if not ``None``, is a multiple
        of 30 degrees for centers and parallel to the side for hex-sides,
        otherwise ``False``.
    """

    if ishex(x, y):
        if facing == None:
            return True
        else:
            return facing % 30 == 0
    elif ishexside(x, y):
        if facing == None:
            return True
        elif (x % 2 == 0.5 and y % 1 == 0.25) or (x % 2 == 1.5 and y % 1 == 0.75):
            return facing % 180 == 120
        elif (x % 2 == 0.5 and y % 1 == 0.75) or (x % 2 == 1.5 and y % 1 == 0.25):
            return facing % 180 == 60
        else:
            return facing % 180 == 0
    else:
        return False


def checkisvalid(x, y, facing=None):
    """
    Raise an exception is a hex location and facing are not valid.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location.
    :param facing: Either ``None`` or a number specifying the facing in degrees.

    :returns: ``None``

    :raises RuntimeError: If the point (x,y) in hex coordinates and facing do
        not correspond to a valid hex location in the sense of :func:`isvalid`.
    """

    if not isvalid(x, y):
        raise RuntimeError("(%r,%r) is not a valid hex center or hex-side." % (x, y))

    if facing != None and not isvalid(x, y, facing=facing):
        raise RuntimeError("%r is not a valid facing for (%r,%r)." % (facing, x, y))


def areadjacent(x0, y0, x1, y1):
    """
    Return whether two locations correspond to adjacent hexes.

    :param x0: 
    :param y0: The `x0` and `y0` parameters are the coordinates of one hex
        location. The location must be a valid hex or hex-side.
    :param x1: 
    :param y1: The `x1` and `y1` parameters are the coordinates of the other hex
        location. The location must be a valid hex or hex-side.

    :return:
        ``True`` if the locations (x0,y0) and (x1,y1) in hex coordinates
        corresponds the hex centers of adjacent hexes, otherwise ``False``.
    """

    assert isvalid(x0, y0)
    assert isvalid(x1, y1)

    if not ishex(x0, y0) or not ishex(x1, y1):
        return False
    if abs(x1 - x0) == 1.0 and abs(y1 - y0) == 0.5:
        return True
    elif x1 == x0 and abs(y1 - y0) == 1.0:
        return True
    else:
        return False


def forward(x, y, facing):
    """
    Return the hex location forward from a hex location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location. The location must be a valid hex or hex-side.
    :param facing: The facing in degrees. The facing must be valid for the hex
        location.

    :return: The `x` and `y` coordinates next valid location forward from the
        point (x, y) with respect to the facing.
    """

    assert isvalid(x, y, facing=facing)

    def dxdy(
        facing,
    ):
        if facing >= 180:
            dx, dy = dxdy(facing - 180)
            return -dx, -dy

        if facing > 90:
            dx, dy = dxdy(180 - facing)
            return -dx, +dy

        i = facing // 30
        return [+1.00, +1.00, +0.50, +0.00][i], [+0.00, +0.50, +0.75, +1.00][i]

    dx, dy = dxdy(facing)

    return x + dx, y + dy


def backward(x, y, facing):
    """
    Return the hex location backward from a hex location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location. The location must be a valid hex or hex-side.
    :param facing: The facing in degrees. The facing must be valid for the hex
        location.

    :return: The `x` and `y` coordinates next valid location backward from the
        point (x, y) with respect to the facing.
    """

    assert isvalid(x, y, facing=facing)

    def dxdy(
        facing,
    ):
        if facing >= 180:
            dx, dy = dxdy(facing - 180)
            return -dx, -dy

        if facing > 90:
            dx, dy = dxdy(180 - facing)
            return -dx, +dy

        i = facing // 30
        return [+1.00, +1.00, +0.50, +0.00][i], [+0.00, +0.50, +0.75, +1.00][i]

    dx, dy = dxdy(facing)

    return x - dx, y - dy


def slide(x, y, facing, sense):
    """
    Return the hex location after performing a slide from a hex location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location. The location must be a valid hex or hex-side.
    :param facing: The facing in degrees. The facing must be valid for the hex
        location.
    :param sense: The sense of the maneuver, either ``"L"`` or ``"R"``.

    :return: The `x` and `y` coordinates after performing a slide from the point
        (x, y) with respect to the facing and sense. The forward part of the
        slide has already been carried out.
    """

    assert isvalid(x, y, facing=facing)
    assert sense == "R" or sense == "L"

    def dxdy(facing, sense):

        if sense == "R":
            othersense = "L"
        else:
            othersense = "R"

        if facing >= 180:
            dx, dy = dxdy(facing - 180, sense)
            return -dx, -dy

        if facing > 90:
            dx, dy = dxdy(180 - facing, othersense)
            return -dx, +dy

        i = facing // 30
        if sense == "R":
            return [+0.00, +0.00, +0.50, +1.00][i], [-0.50, -1.00, -0.25, -0.50][i]
        else:
            return [+0.00, -1.00, -0.50, -1.00][i], [+0.50, +0.50, +0.25, -0.50][i]

    dx, dy = dxdy(facing, sense)

    return x + dx, y + dy


def displacementroll(x, y, facing, sense):
    """
    Return the hex location after performing a displacement roll from a hex
    location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location. The location must be a valid hex or hex-side.
    :param facing: The facing in degrees. The facing must be valid for the hex
        location.
    :param sense: The sense of the maneuver, either ``"L"`` or ``"R"``.

    :return: The `x` and `y` coordinates after performing a displacement roll
        from the location (x, y) with respect to the facing and sense. The
        forward part of the displacement roll has already been carried out.
    """

    # It's identical to a slide.

    return slide(x, y, facing, sense)


def lagroll(x, y, facing, sense):
    """
    Return the hex location after performing a lag roll from a hex location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location. The location must be a valid hex or hex-side.
    :param facing: The facing in degrees. The facing must be valid for the hex
        location.
    :param sense: The sense of the maneuver, either ``"L"`` or ``"R"``.

    :return: The `x` and `y` coordinates after performing a lag roll from the
        location (x, y) with respect to the facing and sense. The forward part
        of the lag roll has already been carried out.
    """

    assert isvalid(x, y, facing=facing)
    assert sense == "R" or sense == "L"

    if ishexside(x, y):
        return hexsidetohex(x, y, facing, sense)

    lastx, lasty = forward(x, y, (facing + 180) % 360)
    if ishexside(lastx, lasty):
        return hexsidetohex(lastx, lasty, facing, sense)

    return slide(x, y, facing, sense)


def hexsidetohex(x, y, facing, sense):
    """
    Return the hex location of the hex adjacent to a hex location.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex-side
        location. The location must be a valid hex-side.
    :param facing: The facing in degrees. The facing must be valid for the
        hex-side location.
    :param sense: The sense of the hex, either ``"L"`` or ``"R"``.

    :return: The `x` and `y` coordinates of the hex center adjacent to the hex
        side at the location (x, y) with respect to the facing and sense.
    """

    assert ishexside(x, y)
    assert isvalid(x, y, facing=facing)
    assert sense == "R" or sense == "L"

    def dxdy(facing, sense):

        if sense == "R":
            othersense = "L"
        else:
            othersense = "R"

        if facing >= 180:
            dx, dy = dxdy(facing - 180, sense)
            return -dx, -dy

        i = facing // 60
        if sense == "R":
            return [+0.00, +0.50, +0.50][i], [-0.50, -0.25, +0.25][i]
        else:
            return [+0.00, -0.50, -0.50][i], [+0.50, +0.25, -0.25][i]

    dx, dy = dxdy(facing, sense)

    return x + dx, y + dy


def hexsidetohexes(x, y):
    """
    Return the hex locations of the hexes adjacent to a hex-side.

    :param x: 
    :param y: The `x` and `y` parameters are the hex coordinates of the hex
        location. The location must be a valid hex-side.

    :return: A tuple (x0, y0, x1, y0) whose values are the hex coordinates
        (x0,y0) and (x1,y1) of the hex centers adjacent to the hex-side.
    """

    assert ishexside(x, y)

    if x % 2 == 0.5 and y % 1 == 0.25:
        x0, y0 = x - 0.5, y - 0.25
        x1, y1 = x + 0.5, y + 0.25
    elif x % 2 == 0.5 and y % 1 == 0.75:
        x0, y0 = x - 0.5, y + 0.25
        x1, y1 = x + 0.5, y - 0.25
    elif x % 2 == 1.5 and y % 1 == 0.25:
        x0, y0 = x - 0.5, y + 0.25
        x1, y1 = x + 0.5, y - 0.25
    elif x % 2 == 1.5 and y % 1 == 0.75:
        x0, y0 = x - 0.5, y - 0.25
        x1, y1 = x + 0.5, y + 0.25
    else:
        x0, y0 = x, y - 0.5
        x1, y1 = x, y + 0.5

    return x0, y0, x1, y1


def distance(x0, y0, x1, y1):

    """
    Return the distance in hexes between two hex locations.

    :param x0: 
    :param y0: The `x0` and `y0` parameters are the coordinates of one hex
        location. The location must be a valid hex or hex-side.
    :param x1: 
    :param y1: The `x1` and `y1` parameters are the coordinates of the other hex
        location. The location must be a valid hex or hex-side.

    :return:
        The distance between the two hex positions in hexes as an integer. The
        distance is the number of whole hexes on the shortest path.
    """

    # The TSOH errata says this about range: "When determining range where one
    # or more aircraft are on hexsides, count only the full hexes between them.
    # Take the shortest number of hexes."

    # Our algorithm is as follows. While points 0 and 1 not at the same
    # location, generate six locations around point 0 each offset by half a hex
    # hex and move point 0 to the one closest to point 1. Each time point 0 is
    # moved, the distance increases by one half. Return the integer part of the
    # distance.

    assert isvalid(x0, y0)
    assert isvalid(x1, y1)

    def physicaldistance(x0, y0, x1, y1):
        x0, y0 = tophysicalxy(x0, y0)
        x1, y1 = tophysicalxy(x1, y1)
        return math.hypot(x1 - x0, y1 - y0)

    d = 0.0
    while x0 != x1 or y0 != y1:
        p = [
            (x0 + 0.00, y0 + 0.50),
            (x0 + 0.50, y0 + 0.25),
            (x0 + 0.50, y0 - 0.25),
            (x0 + 0.00, y0 - 0.50),
            (x0 - 0.50, y0 - 0.25),
            (x0 - 0.50, y0 + 0.25),
        ]
        for x, y in p:
            if physicaldistance(x, y, x1, y1) < physicaldistance(x0, y0, x1, y1):
                x0, y0 = x, y
        d += 0.5

    return int(d)
