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
    "setupship",
    "setcolor",
]

################################################################################


def startgamesetup(
    scenario,
    sheets=None,
    north="up",
    variants=[],
    printlog=True,
    writelogfiles=True,
    writemapfiles=True,
    **kwargs
):
    """
    Start the game set-up for the specified scenario (or for the specified map layout).
    """

    glass.log.setprint(printlog)
    glass.log.setwritefiles(writelogfiles)
    glass.map.setwritefiles(writemapfiles)
    glass.flight.startgamesetup()

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

        glass.map.setupmap(sheets, **kwargs)

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
        glass.flight.startgameturn()

        glass.log.logwhat("start of game turn.")

        glass.element._startgameturn()

        if len(glass.aircraft.aslist()) != 0:
            glass.log.logwhat(
                "initial aircraft position, speed, bank, maneuver, previous flight type, and damage:"
            )
            for A in glass.aircraft.aslist():
                A.logwhat(
                    "%s  %4.1f  %-9s  %-3s  %-5s"
                    % (
                        A.position(),
                        A.speed(),
                        A.maneuver(),
                        A.flighttype(),
                        A.damage(),
                    ),
                    writefile=False,
                )
        if len(glass.missile.aslist()) != 0:
            glass.log.logwhat("initial missile position and speed:")
            for M in glass.missile.aslist():
                M.logwhat("%s  %4.1f" % (M.position(), M.speed()), writefile=False)
        if len(glass.groundunit.aslist()) != 0:
            glass.log.logwhat(
                "initial ground element position, damage, and transported unit:"
            )
            for G in glass.groundunit.aslist():
                if G.istransporting():
                    transporting = "(%s)" % G.transporting().name()
                else:
                    transporting = ""
                G.logwhat(
                    "%s  %4s                  %-5s  %s"
                    % (G.position(), "", G.damage(), transporting),
                    writefile=False,
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

        glass.flight.endgameturn()
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
    zoomincludesonlyairelements=False,
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
    draw180Larc=[],
    draw180Rarc=[],
    draw150arc=[],
    draw150Lline=[],
    draw150Rline=[],
    draw120arc=[],
    draw120Lline=[],
    draw120Rline=[],
    draw90arc=[],
    draw90Lline=[],
    draw90Rline=[],
    draw60arc=[],
    draw60Lline=[],
    draw60Rline=[],
    draw30arc=[],
    draw30Lline=[],
    draw30Rline=[],
    draw0line=[],
    drawlos=[],
    allsighted=False,
    allidentified=False,
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

            xmin = glass.element._xminforzoom(
                withkilled=zoomincludeskilled,
                withairelementsonly=zoomincludesonlyairelements,
            )
            xmax = glass.element._xmaxforzoom(
                withkilled=zoomincludeskilled,
                withairelementsonly=zoomincludesonlyairelements,
            )
            ymin = glass.element._yminforzoom(
                withkilled=zoomincludeskilled,
                withairelementsonly=zoomincludesonlyairelements,
            )
            ymax = glass.element._ymaxforzoom(
                withkilled=zoomincludeskilled,
                withairelementsonly=zoomincludesonlyairelements,
            )

            if xmin is not None:
                xmin = 0.5 * math.floor(2.0 * xmin) - zoomborder
            if ymin is not None:
                ymin = 0.5 * math.floor(2.0 * ymin) - zoomborder
            if xmax is not None:
                xmax = 0.5 * math.ceil(2.0 * xmax) + zoomborder
            if ymax is not None:
                ymax = 0.5 * math.ceil(2.0 * ymax) + zoomborder

        glass.map.startdrawmap(
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
            sheets=sheets,
            compactstacks=compactstacks,
        )

        if drawlimitedarc is True:
            drawlimitedarc = glass.aircraft.aslist() + glass.missile.aslist()

        if draw0line is True:
            draw0line = glass.aircraft.aslist() + glass.missile.aslist()

        if draw30arc is True:
            draw30arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw30Lline is True:
            draw30Lline = glass.aircraft.aslist() + glass.missile.aslist()
        if draw30Rline is True:
            draw30Rline = glass.aircraft.aslist() + glass.missile.aslist()

        if draw60arc is True:
            draw60arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw60Lline is True:
            draw60Lline = glass.aircraft.aslist() + glass.missile.aslist()
        if draw60Rline is True:
            draw60Rline = glass.aircraft.aslist() + glass.missile.aslist()

        if draw90arc is True:
            draw90arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw90Lline is True:
            draw90Lline = glass.aircraft.aslist() + glass.missile.aslist()
        if draw90Rline is True:
            draw90Rline = glass.aircraft.aslist() + glass.missile.aslist()

        if draw120arc is True:
            draw120arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw120Lline is True:
            draw120Lline = glass.aircraft.aslist() + glass.missile.aslist()
        if draw120Rline is True:
            draw120Rline = glass.aircraft.aslist() + glass.missile.aslist()

        if draw150arc is True:
            draw150arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw150Lline is True:
            draw150Lline = glass.aircraft.aslist() + glass.missile.aslist()
        if draw150Rline is True:
            draw150Rline = glass.aircraft.aslist() + glass.missile.aslist()

        if draw180arc is True:
            draw180arc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw180Larc is True:
            draw180Larc = glass.aircraft.aslist() + glass.missile.aslist()
        if draw180Rarc is True:
            draw180Rarc = glass.aircraft.aslist() + glass.missile.aslist()

        if draw180line is True:
            draw180line = glass.aircraft.aslist() + glass.missile.aslist()

        for Elist, arc in [
            [drawlimitedarc, "limited"],
            [draw0line, "0"],
            [draw30arc, "30-"],
            [draw30Lline, "30L"],
            [draw30Rline, "30R"],
            [draw60arc, "60-"],
            [draw60Lline, "60L"],
            [draw60Rline, "60R"],
            [draw90arc, "90-"],
            [draw90Lline, "90L"],
            [draw90Rline, "90R"],
            [draw120arc, "120+"],
            [draw120Lline, "120L"],
            [draw120Rline, "120R"],
            [draw150arc, "150+"],
            [draw150Lline, "150L"],
            [draw150Rline, "150R"],
            [draw180arc, "180+"],
            [draw180Larc, "180L"],
            [draw180Rarc, "180R"],
            [draw180line, "180"],
        ]:
            for E in Elist:
                if E.facing() is None:
                    raise RuntimeError(
                        "unable to draw arc for element %s as it does not have a facing."
                        % E.name()
                    )
                glass.draw.drawarc(E.x(), E.y(), E.facing(), arc)

        glass.element._drawmap(allsighted, allidentified)

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
from glass.ship import Ship as setupship
from glass.color import setcolor
