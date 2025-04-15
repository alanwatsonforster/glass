import math

import apxo.azimuth
import apxo.aircraft
import apxo.draw
import apxo.element
import apxo.gameturn
import apxo.groundunit
import apxo.log
import apxo.map
import apxo.missile
import apxo.order
import apxo.variants
import apxo.scenarios
import apxo.visualsighting

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

    apxo.log.setprint(printlog)
    apxo.log.setwritefiles(writelogfiles)
    apxo.map.setwritefiles(writemapfiles)

    apxo.log.clearerror()
    try:

        apxo.gameturn.startgamesetup()

        apxo.log.logwhat("start of game set-up.")

        apxo.variants.setvariants(variants)

        if scenario != None:
            apxo.log.logwhat("scenario is %s." % scenario)
            sheets = apxo.scenarios.sheets(scenario)
            north = apxo.scenarios.north(scenario)
            allforest = apxo.scenarios.allforest(scenario)
        else:
            apxo.log.logwhat("no scenario specified.")
            apxo.log.logwhat("sheets are %r." % sheets)
            apxo.log.logwhat("north is %s." % north)

        for key in kwargs.keys():
            apxo.log.logwhat("map option %s is %r." % (key, kwargs[key]))

        apxo.map.setmap(sheets, **kwargs)

        apxo.azimuth.setnorth(north)

        apxo.element._startgamesetup()

    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


def endgamesetup():
    """
    End the game set-up.
    """

    try:

        if apxo.log.error() is not None:
            raise RuntimeError(
                "unresolved error at end of game setup: %s" % apxo.log.error()
            )

        apxo.element._endgamesetup()

        apxo.log.logwhat("end of game set-up.")

        apxo.gameturn.endgamesetup()

    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


################################################################################


def startgameturn(note=None):
    """
    Start the next game turn.
    """

    apxo.log.clearerror()
    try:

        apxo.gameturn.startgameturn()

        apxo.log.logwhat("start of game turn.")

        apxo.element._startgameturn()

        if len(apxo.aircraft.aslist()) != 0:
            apxo.log.logwhat(
                "initial aircraft positions, speeds, maneuvers, and previous flight types:"
            )
            for A in apxo.aircraft.aslist():
                A.logwhat(
                    "%s  %4.1f  %-9s  %-3s"
                    % (A.position(), A.speed(), A.maneuver(), A.flighttype()),
                    writefile=False,
                )
        if len(apxo.missile.aslist()) != 0:
            apxo.log.logwhat("initial missile positions and speeds:")
            for M in apxo.missile.aslist():
                M.logwhat("%s  %4.1f" % (M.position(), M.speed()), writefile=False)
        if len(apxo.groundunit.aslist()) != 0:
            apxo.log.logwhat("initial ground element positions and damage:")
            for G in apxo.groundunit.aslist():
                G.logwhat(
                    "%s  %4s  %s" % (G.position(), "", G.damage()), writefile=False
                )
        apxo.log.lognote(None, note)

    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


def endgameturn(note=None):
    """
    End the current turn.
    """

    try:

        if apxo.log.error() is not None:
            raise RuntimeError(
                "unresolved error at end of game turn: %s" % apxo.log.error()
            )

        apxo.element._endgameturn()

        apxo.log.logwhat("end of game turn.")
        apxo.log.lognote(None, note)

        apxo.gameturn.endgameturn()

    except RuntimeError as e:
        apxo.log.logexception(e)

    apxo.log.logbreak()


################################################################################


def startvisualsighting():
    try:
        apxo.gameturn.checkingameturn()
        apxo.visualsighting.startvisualsighting(),
    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


def endvisualsighting():
    try:
        apxo.gameturn.checkingameturn()
        apxo.visualsighting.endvisualsighting(),
    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


################################################################################


def settraining(training):
    try:
        apxo.gameturn.checkinsetup()
        apxo.order.settraining(training)
    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


################################################################################


def orderofflightdeterminationphase(rolls, firstkill=None, mostkills=None):
    try:
        apxo.gameturn.checkingameturn()
        apxo.order.orderofflightdeterminationphase(
            rolls, firstkill=firstkill, mostkills=mostkills
        )
    except RuntimeError as e:
        apxo.log.logexception(e)
    apxo.log.logbreak()


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

            xmin = apxo.element._xminforzoom(withkilled=zoomincludeskilled)
            xmax = apxo.element._xmaxforzoom(withkilled=zoomincludeskilled)
            ymin = apxo.element._yminforzoom(withkilled=zoomincludeskilled)
            ymax = apxo.element._ymaxforzoom(withkilled=zoomincludeskilled)

            if xmin is not None:
                xmin = math.floor(xmin) - zoomborder
            if ymin is not None:
                ymin = math.floor(ymin) - zoomborder
            if xmax is not None:
                xmax = math.ceil(xmax) + zoomborder
            if ymax is not None:
                ymax = math.ceil(ymax) + zoomborder

        apxo.map.startdrawmap(
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            sheets=sheets,
            watermark=watermark,
            compactstacks=compactstacks,
        )

        if drawlimitedarc is True:
            drawlimitedarc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw0line is True:
            draw0line = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw30arc is True:
            draw30arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw60arc is True:
            draw60arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw90arc is True:
            draw90arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw120arc is True:
            draw120arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw150arc is True:
            draw150arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw180arc is True:
            draw180arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if drawL180arc is True:
            drawL180arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if drawR180arc is True:
            drawR180arc = apxo.aircraft.aslist() + apxo.missile.aslist()
        if draw180line is True:
            draw180line = apxo.aircraft.aslist() + apxo.missile.aslist()

        for A in drawlimitedarc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "limited")
        for A in draw0line:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "0")
        for A in draw30arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "30-")
        for A in draw60arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "60-")
        for A in draw90arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "90-")
        for A in draw120arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "120+")
        for A in draw150arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "150+")
        for A in draw180arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "180+")
        for A in drawL180arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "L180+")
        for A in drawR180arc:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "R180+")
        for A in draw180line:
            apxo.draw.drawarc(A.x(), A.y(), A.facing(), "180")

        apxo.element._drawmap()

        for E in drawlos[1:]:
            apxo.draw.drawlos(drawlos[0].x(), drawlos[0].y(), E.x(), E.y())

        apxo.map.enddrawmap(apxo.gameturn.gameturn(), writefiles=writefiles)

    except RuntimeError as e:
        apxo.log.logexception(e)


################################################################################

from apxo.aircraft import Aircraft as setupaircraft
from apxo.groundunit import GroundUnit as setupgroundunit
from apxo.groundunit import HexGroundUnit as setuphexgroundunit
from apxo.marker import Marker as setupmarker
