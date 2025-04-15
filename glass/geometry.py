##############################################################################
import math
import apxo as ap
import apxo.hex
import apxo.log

##############################################################################


def showgeometry(A, B, note=None):
    """
    Show the geometry of aircraft B with respect to the aircraft A.
    """

    A.logbreak()

    Aname = A._name
    Bname = B._name

    apxo.gameturn.checkingamesetuporgameturn()

    angleofftail = A.angleofftail(B)
    if angleofftail == "0 line" or angleofftail == "180 line":
        A.logcomment("%s has %s on its %s." % (Bname, Aname, angleofftail))
    else:
        A.logcomment("%s has %s in its %s." % (Bname, Aname, angleofftail))

    angleofftail = B.angleofftail(A)
    if angleofftail == "0 line" or angleofftail == "180 line":
        A.logcomment("%s is on the %s of %s." % (Bname, angleofftail, Aname))
    else:
        A.logcomment("%s is in the %s of %s." % (Bname, angleofftail, Aname))

    if A._inlimitedradararc(B):
        A.logcomment("%s is in the limited radar arc of %s." % (Bname, Aname))
    else:
        A.logcomment("%s is not in the limited radar arc of %s." % (Bname, Aname))

    A.lognote(note)


##############################################################################


def _round(x):
    """
    Round x to 1/256 of a unit.
    """
    if x >= 0:
        return int(x * 256 + 0.5) / 256
    else:
        return int(x * 256 - 0.5) / 256


##############################################################################


def samehorizontalposition(A0, A1):
    """
    Return True if aircraft A0 to A1 are in the same horizontal position,
    Bwise return False.
    """

    return A0.x() == A1.x() and A0.y() == A1.y()


##############################################################################


def horizontalrange(A0, A1, x1=None, y1=None):
    """
    Return the horizontal range in hexes from aircraft A0 to A1.
    """

    if A1 is not None:
        x1 = A1.x()
        y1 = A1.y()

    return apxo.hex.distance(A0.x(), A0.y(), x1, y1)


def verticalrange(A0, A1, x1=None, y1=None):
    """
    Return the vertical range in hexes from aircraft A0 to A1.
    """

    if A1 is not None:
        altitude1 = A1.altitude()
    else:
        altitude1 = apxo.map.altitude(x, y)

    return int(abs(A0.altitude() - altitude1) / 2)


def range(A0, A1, x1=None, y1=None):
    """
    Return the range in hexes from aircraft A0 to A1.
    """

    return horizontalrange(A0, A1, x1=x1, y1=y1) + verticalrange(A0, A1, x1=x1, y1=y1)


##############################################################################


def relativepositions(x0, y0, facing0, x1, y1, facing1):

    # Determine the offsets of 1 from 0.

    dx = x1 - x0
    dy = y1 - y0
    dx, dy = apxo.hex.tophysical(dx, dy)

    # Determine the range.

    r = math.sqrt(dx * dx + dy * dy)

    # Determine the angle of 0 off the tail of 1.

    if dx == 0 and dy == 0:
        angleofftail = facing0 - facing1
    else:
        angleofftail = math.degrees(math.atan2(dy, dx)) - facing1
    angleofftail %= 360
    if angleofftail > 180:
        angleofftail -= 360

    # Determine the angle of 1 off the nose of 0.

    if dx == 0 and dy == 0:
        angleoffnose = facing1 - facing0
    else:
        angleoffnose = math.degrees(math.atan2(dy, dx)) - facing0
    angleoffnose %= 360
    if angleoffnose > 180:
        angleoffnose -= 360

    # Determine the coordinates dx and dy of 1, with dx being the
    # coordinate along the flight path of 0 and y being the coordinate
    # perpendicular to the flight path of 0.

    dx = r * math.cos(math.radians(angleoffnose))
    dy = r * math.sin(math.radians(angleoffnose))

    # Round everything.

    angleofftail = _round(angleofftail)
    angleoffnose = _round(angleoffnose)
    r = _round(r)
    dx = _round(dx)
    dy = _round(dy)

    return angleofftail, angleoffnose, r, dx, dy


##############################################################################


def angleofftail(
    A0,
    A1,
    arconly=False,
    resolveborderline="likegunnery",
    x0=None,
    y0=None,
    facing0=None,
    x1=None,
    y1=None,
    facing1=None,
):
    """
    Return the angle of A0 off the tail of A1.
    """

    # See rule 9.2.

    def truegeometry(x0, y0, facing0, x1, y1, facing1):
        angleofftail, angleoffnose, r, dx, dy = relativepositions(
            x0, y0, facing0, x1, y1, facing1
        )
        return angleofftail, angleoffnose, r

    if A0 is not None:
        x0 = A0.x()
        y0 = A0.y()
        facing0 = A0.facing()

    if A1 is not None:
        x1 = A1.x()
        y1 = A1.y()
        facing1 = A1.facing()

    angleofftail, angleoffnose, r = truegeometry(x0, y0, facing0, x1, y1, facing1)

    assert resolveborderline == "likegunnery" or resolveborderline == "likeradar"
    if resolveborderline == "likegunnery":

        if (
            r > 0
            and angleofftail != 0.0
            and angleofftail != 180.0
            and angleofftail % 30 == 0.0
        ):

            # Distinguish cases on the 30, 60, 90, 120, and 150 degree arcs.

            # If 0 is slower, it falls in the rear arc.
            # If 0 is faster and headed behind 0, it falls in the rear arc.
            # If 0 is faster and headed in front of 1, it falls in the front arc.

            inreararc = False
            infrontarc = False
            if A0.speed() < A1.speed():
                inreararc = True
            elif A0.speed() > A1.speed() and angleoffnose != 0:
                if (angleofftail > 0 and angleoffnose > 0) or (
                    angleofftail < 0 and angleoffnose < 0
                ):
                    infrontarc = True
                elif (angleofftail > 0 and angleoffnose < 0) or (
                    angleofftail < 0 and angleoffnose > 0
                ):
                    inreararc = True

            if (infrontarc and angleofftail > 0) or (inreararc and angleofftail < 0):
                angleofftail += 1
            elif (infrontarc and angleofftail < 0) or (inreararc and angleofftail > 0):
                angleofftail -= 1

    else:

        angleofftail += 1

    if not arconly:
        # To be on the 0 or 180 degree lines, the aircraft has to be facing
        # the B.
        if angleofftail == 0 and facing0 == facing1:
            return "0 line"
        elif angleofftail == 180 and abs(facing0 - facing1) == 180:
            return "180 line"

    # Resolve cases on the 30, 60, 90, 120, and 150 degree lines in favor
    # of aircraft 0 (round 120 to 150 and 150 to 180).
    if abs(angleofftail) <= 30:
        return "30 arc"
    elif abs(angleofftail) <= 60:
        return "60 arc"
    elif abs(angleofftail) <= 90:
        return "90 arc"
    elif abs(angleofftail) < 120:
        return "120 arc"
    elif abs(angleofftail) < 150:
        return "150 arc"
    else:
        return "180 arc"


##############################################################################


def inradarverticallimits(A0, A1, arc):

    assert arc in ["limited", "180+", "150+", "120+"]

    from math import inf

    table = {
        "limited": {
            "VD": [-2.0, -9.0],
            "SD": [-0.5, -3.0],
            "LVL": [+0.5, -0.5],
            "SC": [+2.0, +0.0],
            "ZC": [+4.0, +0.5],
            "VC": [+9.0, +2.0],
        },
        "180+": {
            "VD": [-1.0, -inf],
            "SD": [-0.0, -5.0],
            "LVL": [+1.0, -1.0],
            "SC": [+3.0, -0.5],
            "ZC": [+5.0, +0.0],
            "VC": [+inf, +1.0],
        },
        "150+": {
            "VD": [-0.5, -inf],
            "SD": [-0.0, -8.0],
            "LVL": [+2.0, -2.0],
            "SC": [+4.0, -1.0],
            "ZC": [+8.0, +0.0],
            "VC": [+inf, +0.5],
        },
        "120+": {
            "VD": [-0.0, -inf],
            "SD": [+0.5, -inf],
            "LVL": [+4.0, -4.0],
            "SC": [+6.0, -2.0],
            "ZC": [+inf, -0.5],
            "VC": [+inf, +0.0],
        },
    }

    flighttype = A0._flighttype
    if flighttype == "UD":
        flighttype = "SD"

    fmax = table[arc][flighttype][0]
    fmin = table[arc][flighttype][1]

    r = horizontalrange(A0, A1)
    if math.isinf(fmax):
        altitudemax = +inf
    else:
        altitudemax = A0.altitude() + int(fmax * r)
    if math.isinf(fmin):
        altitudemin = -inf
    else:
        altitudemin = A0.altitude() + int(fmin * r)
    return altitudemin <= A1.altitude() and A1.altitude() <= altitudemax


##############################################################################


def inarc(A0, A1, arc, resolveborderline="likegunnery"):
    """
    Return True is A1 is in the specified arc of A0. Vertical limits do not
    apxo.ply. The arc may be: 180+, 150+, 120+, 90-, 60-, or 30-.
    """

    assert arc in [
        "limited",
        "180+",
        "150+",
        "120+",
        "90+",
        "60+",
        "30-",
        "60-",
        "90-",
        "120-",
        "150-",
    ]

    if arc == "limited":
        return inlimitedarc(A0, A1)

    if arc == "180+":
        arcs = ["180 arc"]
    elif arc == "150+":
        arcs = ["180 arc", "150 arc"]
    elif arc == "120+":
        arcs = ["180 arc", "150 arc", "120 arc"]
    elif arc == "90+":
        arcs = ["180 arc", "150 arc", "120 arc", "90 arc"]
    elif arc == "60+":
        arcs = ["180 arc", "150 arc", "120 arc", "90 arc", "60 arc"]
    elif arc == "30-":
        arcs = ["30 arc"]
    elif arc == "60-":
        arcs = ["30 arc", "60 arc"]
    elif arc == "90-":
        arcs = ["30 arc", "60 arc", "90 arc"]
    elif arc == "120-":
        arcs = ["30 arc", "60 arc", "90 arc", "120 arc"]
    elif arc == "150-":
        arcs = ["30 arc", "60 arc", "90 arc", "120 arc", "150 arc"]
    else:
        raise RuntimeError("invalid arc %r" % arc)

    return (
        angleofftail(A1, A0, arconly=True, resolveborderline=resolveborderline) in arcs
    )


##############################################################################


def inradararc(A0, A1, arc):

    assert arc in ["limited", "180+", "150+", "120+"]

    return inarc(A0, A1, arc) and inradarverticallimits(A0, A1, arc)


##############################################################################


def inlimitedarc(A0, A1, x1=None, y1=None, facing1=None):
    """
    Return True if A1 is in the limited arc of A0. Vertical limits do not
    apply to limited arcs.
    """

    x0 = A0.x()
    y0 = A0.y()
    facing0 = A0.facing()

    if A1 != None:
        x1 = A1.x()
        y1 = A1.y()
        facing1 = A1.facing()

    # See the Limited Radar Arc diagram in the sheets.

    angleofftail, angleoffnose, r, dx, dy = relativepositions(
        x0, y0, facing0, x1, y1, facing1
    )

    if dx <= 0:
        return False
    elif dx <= _round(1.25 * math.sqrt(3 / 4)):
        return dy == 0
    elif dx <= _round(5.1 * math.sqrt(3 / 4)):
        return abs(dy) <= 0.6
    elif dx <= _round(10.1 * math.sqrt(3 / 4)):
        return abs(dy) <= 1.1
    else:
        return abs(dy) <= 1.6


##############################################################################
