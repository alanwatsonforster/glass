import math

import glass.azimuth
import glass.aircraft
import glass.draw
import glass.element
import glass.gameturn
import glass.groundunit
import glass.log
import glass.map
import glass.missile
import glass.order
import glass.variants
import glass.scenarios
import glass.visualsighting

__all__ = [
    "startgamesetup",
    "endgamesetup",
    "startgameturn",
    "endgameturn",
    "startvisualsighting",
    "endvisualsighting",
    "settraining",
    "orderofflightdeterminationphase",
    "drawmap",
    "setupaircraft",
    "bomb",
    "setupgroundunit",
    "setuphexgroundunit",
    "setupmarker",
]

################################################################################


def startgamesetup(scenario, sheets=None, north="up", variants=[], printlog=True, writelogfiles=True, writemapfiles=True, **kwargs):
    """
    Start the game set-up for the specified scenario (or for the specified map layout).
    """

    glass.log.setprint(printlog)
    glass.log.setwritefiles(writelogfiles)
    glass.map.setwritefiles(writemapfiles)

    glass.log.clearerror()
    try:

        glass.gameturn.startgamesetup()

        glass.log.logwhat("start of game set-up.")

        glass.variants.setvariants(variants)

        if scenario != None:
            glass.log.logwhat("scenario is %s." % scenario)
            sheets = glass.scenarios.sheets(scenario)
            north = glass.scenarios.north(scenario)
            allforest = glass.scenarios.allforest(scenario)
        else:
            glass.log.logwhat("no scenario specified.")
            glass.log.logwhat("sheets are %r." % sheets)
            glass.log.logwhat("north is %s." % north)

        for key in kwargs.keys():
            glass.log.logwhat("map option %s is %r." % (key, kwargs[key]))

        glass.map.setmap(sheets, **kwargs)

        glass.azimuth.setnorth(north)

        glass.element._startgamesetup()

    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


def endgamesetup():
    """
    End the game set-up.
    """

    try:

        if glass.log.error() is not None:
            raise RuntimeError(
                "unresolved error at end of game setup: %s" % glass.log.error()
            )

        glass.element._endgamesetup()

        glass.log.logwhat("end of game set-up.")

        glass.gameturn.endgamesetup()

    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


################################################################################


def startgameturn(note=None):
    """
    Start the next game turn.
    """

    glass.log.clearerror()
    try:

        glass.gameturn.startgameturn()

        glass.log.logwhat("start of game turn.")

        glass.element._startgameturn()

        if len(glass.aircraft.aslist()) != 0:
            glass.log.logwhat(
                "initial aircraft positions, speeds, maneuvers, and previous flight types:"
            )
            for A in glass.aircraft.aslist():
                A.logwhat(
                    "%s  %4.1f  %-9s  %-3s"
                    % (A.position(), A.speed(), A.maneuver(), A.flighttype()),
                    writefile=False,
                )
        if len(glass.missile.aslist()) != 0:
            glass.log.logwhat("initial missile positions and speeds:")
            for M in glass.missile.aslist():
                M.logwhat("%s  %4.1f" % (M.position(), M.speed()), writefile=False)
        if len(glass.groundunit.aslist()) != 0:
            glass.log.logwhat("initial ground element positions and damage:")
            for G in glass.groundunit.aslist():
                G.logwhat(
                    "%s  %4s  %s" % (G.position(), "", G.damage()), writefile=False
                )
        glass.log.lognote(None, note)

    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


def endgameturn(note=None):
    """
    End the current turn.
    """

    try:

        if glass.log.error() is not None:
            raise RuntimeError(
                "unresolved error at end of game turn: %s" % glass.log.error()
            )

        glass.element._endgameturn()

        glass.log.logwhat("end of game turn.")
        glass.log.lognote(None, note)

        glass.gameturn.endgameturn()

    except RuntimeError as e:
        glass.log.logexception(e)

    glass.log.logbreak()


################################################################################


def startvisualsighting():
    try:
        glass.gameturn.checkingameturn()
        glass.visualsighting.startvisualsighting(),
    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


def endvisualsighting():
    try:
        glass.gameturn.checkingameturn()
        glass.visualsighting.endvisualsighting(),
    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


################################################################################


def settraining(training):
    try:
        glass.gameturn.checkinsetup()
        glass.order.settraining(training)
    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


################################################################################


def orderofflightdeterminationphase(rolls, firstkill=None, mostkills=None):
    try:
        glass.gameturn.checkingameturn()
        glass.order.orderofflightdeterminationphase(
            rolls, firstkill=firstkill, mostkills=mostkills
        )
    except RuntimeError as e:
        glass.log.logexception(e)
    glass.log.logbreak()


################################################################################


def drawmap(
    zoom=True,
    zoomincludeskilled=False,
    zoomborder=2,
    xmin=None,
    ymin=None,
    xmax=None,
    ymax=None,
    sheets=None,
    compactstacks=True,
    drawlimitedarc=[],
    draw180line=[],
    draw180arc=[],
    drawL180arc=[],
    drawR180arc=[],
    draw150arc=[],
    draw120arc=[],
    draw90arc=[],
    draw60arc=[],
    draw30arc=[],
    draw0line=[],
    drawlos=[],
    watermark=None,
    writefiles=True,
):
    """
    Draw the map, with aircraft and markers at their current positions.

    If zoom is True, zoom the map to include region including the
    aircraft, missiles, and markers with a border of zoomborder hexes. If
    zoomincludeskilled is True, include killed aircraft in the zoom.

    If zoom is False, use xmin, xmax, ymin, and ymax to defined the area
    drawn. If these are None, use the natural border of the map. Otherwise
    use their value.
    """

    try:

        if zoom:

            xmin = glass.element._xminforzoom(withkilled=zoomincludeskilled)
            xmax = glass.element._xmaxforzoom(withkilled=zoomincludeskilled)
            ymin = glass.element._yminforzoom(withkilled=zoomincludeskilled)
            ymax = glass.element._ymaxforzoom(withkilled=zoomincludeskilled)

            if xmin is not None:
                xmin = math.floor(xmin) - zoomborder
            if ymin is not None:
                ymin = math.floor(ymin) - zoomborder
            if xmax is not None:
                xmax = math.ceil(xmax) + zoomborder
            if ymax is not None:
                ymax = math.ceil(ymax) + zoomborder

        glass.map.startdrawmap(
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            sheets=sheets,
            watermark=watermark,
            compactstacks=compactstacks,
        )

        if drawlimitedarc is True:
            drawlimitedarc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw0line is True:
            draw0line = glass.aircraft.aslist() + glass.missile.aslist()
        if draw30arc is True:
            draw30arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw60arc is True:
            draw60arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw90arc is True:
            draw90arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw120arc is True:
            draw120arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw150arc is True:
            draw150arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw180arc is True:
            draw180arc = glass.aircraft.aslist() + glass.missile.aslist()
        if drawL180arc is True:
            drawL180arc = glass.aircraft.aslist() + glass.missile.aslist()
        if drawR180arc is True:
            drawR180arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw180line is True:
            draw180line = glass.aircraft.aslist() + glass.missile.aslist()

        for A in drawlimitedarc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "limited")
        for A in draw0line:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "0")
        for A in draw30arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "30-")
        for A in draw60arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "60-")
        for A in draw90arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "90-")
        for A in draw120arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "120+")
        for A in draw150arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "150+")
        for A in draw180arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "180+")
        for A in drawL180arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "L180+")
        for A in drawR180arc:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "R180+")
        for A in draw180line:
            glass.draw.drawarc(A.x(), A.y(), A.facing(), "180")

        glass.element._drawmap()

        for E in drawlos[1:]:
            glass.draw.drawlos(drawlos[0].x(), drawlos[0].y(), E.x(), E.y())

        glass.map.enddrawmap(glass.gameturn.gameturn(), writefiles=writefiles)

    except RuntimeError as e:
        glass.log.logexception(e)


################################################################################

from glass.aircraft import Aircraft as setupaircraft
from glass.groundunit import GroundUnit as setupgroundunit
from glass.groundunit import HexGroundUnit as setuphexgroundunit
from glass.marker import Marker as setupmarker
