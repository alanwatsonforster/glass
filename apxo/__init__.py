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
    "groundunit",
    "marker",
    "missile",
]

################################################################################


def startgamesetup(scenario, sheets=None, north="up", variants=[], **kwargs):
    """
    Start the game set-up for the specified scenario (or for the specified map layout).
    """

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

    aplog.clearerror()
    try:

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
        aplog.lognote(None, note)

    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


def endgameturn(note=None):
    """
    End the current turn.
    """

    aplog.clearerror()
    try:

        apelement._endgameturn()

        aplog.logwhat("end of game turn.")
        aplog.lognote(None, note)

        apgameturn.endgameturn()

    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


################################################################################


def startvisualsighting():
    aplog.clearerror()
    try:
        apgameturn.checkinturn()
        apvisualsighting.startvisualsighting(),
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


def endvisualsighting():
    aplog.clearerror()
    try:
        apgameturn.checkinturn()
        apvisualsighting.endvisualsighting(),
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


################################################################################


def settraining(training):
    aplog.clearerror()
    try:
        apgameturn.checkinsetup()
        aporder.settraining(training)
    except RuntimeError as e:
        aplog.logexception(e)
    aplog.logbreak()


################################################################################


def orderofflightdeterminationphase(rolls, firstkill=None, mostkills=None):
    aplog.clearerror()
    try:
        apgameturn.checkinturn()
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
    drawlimitedarc=[],
    draw180arc=[],
    draw150arc=[],
    draw120arc=[],
    draw90arc=[],
    draw60arc=[],
    draw30arc=[],
    drawL180arc=[],
    drawR180arc=[],
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

    aplog.clearerror()
    try:

        if zoom:

            xmin = apelement._xminforzoom(withkilled=zoomincludeskilled)
            xmax = apelement._xmaxforzoom(withkilled=zoomincludeskilled)
            ymin = apelement._yminforzoom(withkilled=zoomincludeskilled)
            ymax = apelement._ymaxforzoom(withkilled=zoomincludeskilled)

            xmin -= zoomborder
            ymin -= zoomborder
            xmax += zoomborder
            ymax += zoomborder

        apmap.startdrawmap(
            xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, watermark=watermark
        )

        if drawlimitedarc is True:
            drawlimitedarc = apaircraft.aslist() + apmissile.aslist()
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

        for A in drawlimitedarc:
            apdraw.drawarc(A.x(), A.y(), A.facing(), "limited")
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

        apelement._drawmap()

        apmap.enddrawmap(apgameturn.gameturn(), writefiles=writefiles)

    except RuntimeError as e:
        aplog.logexception(e)


################################################################################

from apxo.aircraft import aircraft
from apxo.groundunit import groundunit
from apxo.marker import marker
