import math

import apxo.azimuth as apazimuth
import apxo.aircraft as apaircraft
import apxo.draw as apdraw
import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.groundunit as apgroundunit
import apxo.log as aplog
import apxo.map as apmap
import apxo.missile as apmissile
import apxo.order as aporder
import apxo.variants as apvariants
import apxo.scenarios as apscenarios
import apxo.visualsighting as apvisualsighting

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
    "aircraft",
    "bomb",
    "groundunit",
    "hexgroundunit",
    "marker",
    "missile",
]

################################################################################


def startgamesetup(scenario, sheets=None, north="up", variants=[], writelogfiles=True, writemapfiles=True, **kwargs):
    """
    Start the game set-up for the specified scenario (or for the specified map layout).
    """

    aplog.setwritefiles(writelogfiles)
    apmap.setwritefiles(writemapfiles)

    aplog.clearerror()
    try:

        apgameturn.startgamesetup()

        aplog.logwhat("start of game set-up.")

        apvariants.setvariants(variants)

        if scenario != None:
            aplog.logwhat("scenario is %s." % scenario)
            sheets = apscenarios.sheets(scenario)
            north = apscenarios.north(scenario)
            allforest = apscenarios.allforest(scenario)
        else:
            aplog.logwhat("no scenario specified.")
            aplog.logwhat("sheets are %r." % sheets)
            aplog.logwhat("north is %s." % north)

        for key in kwargs.keys():
            aplog.logwhat("map option %s is %r." % (key, kwargs[key]))

        apmap.setmap(sheets, **kwargs)

        apazimuth.setnorth(north)

        apelement._startgamesetup()

    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


def endgamesetup():
    """
    End the game set-up.
    """

    try:

        if aplog.error() is not None:
            raise RuntimeError(
                "unresolved error at end of game setup: %s" % aplog.error()
            )

        apelement._endgamesetup()

        aplog.logwhat("end of game set-up.")

        apgameturn.endgamesetup()

    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


################################################################################


def startgameturn(note=None):
    """
    Start the next game turn.
    """

    aplog.clearerror()
    try:

        apgameturn.startgameturn()

        aplog.logwhat("start of game turn.")

        apelement._startgameturn()

        if len(apaircraft.aslist()) != 0:
            aplog.logwhat(
                "initial aircraft positions, speeds, maneuvers, and previous flight types:"
            )
            for A in apaircraft.aslist():
                A.logwhat(
                    "%s  %4.1f  %-9s  %-3s"
                    % (A.position(), A.speed(), A.maneuver(), A.flighttype()),
                    writefile=False,
                )
        if len(apmissile.aslist()) != 0:
            aplog.logwhat("initial missile positions and speeds:")
            for M in apmissile.aslist():
                M.logwhat("%s  %4.1f" % (M.position(), M.speed()), writefile=False)
        if len(apgroundunit.aslist()) != 0:
            aplog.logwhat("initial ground element positions and damage:")
            for G in apgroundunit.aslist():
                G.logwhat(
                    "%s  %4s  %s" % (G.position(), "", G.damage()), writefile=False
                )
        aplog.lognote(None, note)

    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


def endgameturn(note=None):
    """
    End the current turn.
    """

    try:

        if aplog.error() is not None:
            raise RuntimeError(
                "unresolved error at end of game turn: %s" % aplog.error()
            )

        apelement._endgameturn()

        aplog.logwhat("end of game turn.")
        aplog.lognote(None, note)

        apgameturn.endgameturn()

    except RuntimeError as e:
        aplog.logexception(e)

    aplog.logbreak()


################################################################################


def startvisualsighting():
    try:
        apgameturn.checkingameturn()
        apvisualsighting.startvisualsighting(),
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


def endvisualsighting():
    try:
        apgameturn.checkingameturn()
        apvisualsighting.endvisualsighting(),
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


################################################################################


def settraining(training):
    try:
        apgameturn.checkinsetup()
        aporder.settraining(training)
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


################################################################################


def orderofflightdeterminationphase(rolls, firstkill=None, mostkills=None):
    try:
        apgameturn.checkingameturn()
        aporder.orderofflightdeterminationphase(
            rolls, firstkill=firstkill, mostkills=mostkills
        )
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


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

            xmin = apelement._xminforzoom(withkilled=zoomincludeskilled)
            xmax = apelement._xmaxforzoom(withkilled=zoomincludeskilled)
            ymin = apelement._yminforzoom(withkilled=zoomincludeskilled)
            ymax = apelement._ymaxforzoom(withkilled=zoomincludeskilled)

            if xmin is not None:
                xmin = math.floor(xmin) - zoomborder
            if ymin is not None:
                ymin = math.floor(ymin) - zoomborder
            if xmax is not None:
                xmax = math.ceil(xmax) + zoomborder
            if ymax is not None:
                ymax = math.ceil(ymax) + zoomborder

        apmap.startdrawmap(
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            sheets=sheets,
            watermark=watermark,
            compactstacks=compactstacks,
        )

        if drawlimitedarc is True:
            drawlimitedarc = apaircraft.aslist() + apmissile.aslist()
        if draw0line is True:
            draw0line = apaircraft.aslist() + apmissile.aslist()
        if draw30arc is True:
            draw30arc = apaircraft.aslist() + apmissile.aslist()
        if draw60arc is True:
            draw60arc = apaircraft.aslist() + apmissile.aslist()
        if draw90arc is True:
            draw90arc = apaircraft.aslist() + apmissile.aslist()
        if draw120arc is True:
            draw120arc = apaircraft.aslist() + apmissile.aslist()
        if draw150arc is True:
            draw150arc = apaircraft.aslist() + apmissile.aslist()
        if draw180arc is True:
            draw180arc = apaircraft.aslist() + apmissile.aslist()
        if drawL180arc is True:
            drawL180arc = apaircraft.aslist() + apmissile.aslist()
        if drawR180arc is True:
            drawR180arc = apaircraft.aslist() + apmissile.aslist()
        if draw180line is True:
            draw180line = apaircraft.aslist() + apmissile.aslist()

        for A in drawlimitedarc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "limited")
        for A in draw0line:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "0")
        for A in draw30arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "30-")
        for A in draw60arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "60-")
        for A in draw90arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "90-")
        for A in draw120arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "120+")
        for A in draw150arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "150+")
        for A in draw180arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "180+")
        for A in drawL180arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "L180+")
        for A in drawR180arc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "R180+")
        for A in draw180line:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "180")

        apelement._drawmap()

        for E in drawlos[1:]:
            apdraw.drawlos(drawlos[0].x(), drawlos[0].y(), E.x(), E.y())

        apmap.enddrawmap(apgameturn.gameturn(), writefiles=writefiles)

    except RuntimeError as e:
        aplog.logexception(e)


################################################################################

from apxo.aircraft import aircraft
from apxo.groundunit import groundunit
from apxo.groundunit import hexgroundunit
from apxo.marker import marker
