"""
The map.
"""

import apxo.azimuth as apazimuth
import apxo.draw as apdraw
import apxo.hex as aphex
import apxo.hexcode as aphexcode

import os
import ast

_terrain = {}

_drawterrain = True
_drawlabels = True

_usingfirstgenerationsheets = False

_dxsheet = 20
_dysheet = 15

_sheetgrid = []
_loweredgeonmap = {}
_rightedgeonmap = {}
_sheetlist = []
_nxsheetgrid = 0
_nysheetgrid = 0

_xmin = None
_xmax = None
_ymin = None
_ymax = None
_dotsperhex = None
_writefiletypes = None

_saved = False

_allwater = False

missingcolor = [1.00, 1.00, 1.00]

ridgewidth = 14
roadwidth = 5
dockwidth = 5
clearingwidth = 20
bridgeinnerwidth = roadwidth + 8
bridgeouterwidth = bridgeinnerwidth + 6
runwaywidth = 10
taxiwaywidth = 7
damwidth = 14
hexwidth = 0.5
megahexwidth = 7

roadoutlinewidth = 2
dockoutlinewidth = 2
waterourlinewidth = 2

tunnelinnerwidth = roadwidth + 8
tunnelouterwidth = tunnelinnerwidth + 6

blanksheets = ["", "-", "--"]
firstgenerationsheets = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

secondgenerationsheets = [
    "A1",
    "B1",
    "C1",
    "D1",
    "A2",
    "B2",
    "C2",
    "D2",
    "A3",
    "B3",
    "C3",
    "D3",
    "A4",
    "B4",
    "C4",
    "D4",
    "A5",
    "B5",
    "C5",
    "D5",
    "A6",
    "B6",
    "C6",
    "D6",
]


def usingfirstgenerationsheets():
    return _usingfirstgenerationsheets


def setmap(
    sheetgrid,
    drawterrain=True,
    drawlabels=True,
    dotsperhex=80,
    writefiletypes=[],
    style="original",
    wilderness=None,
    forest=None,
    freshwater=None,
    allforest=None,
    maxurbansize=None,
):
    """
    Set the arrangement of the sheets that form the map and the position of the
    compass rose.
    """

    global _usingfirstgenerationsheets
    global _dxsheet
    global _dysheet

    global _drawterrain
    global _drawlabels

    global _sheetgrid
    global _sheetlist
    global _loweredgeonmap
    global _rightedgeonmap
    global _nysheetgrid
    global _nxsheetgrid
    global _xmin
    global _ymin
    global _xmax
    global _ymax
    global _dotsperhex
    global _writefiletypes

    _usingfirstgenerationsheets = None

    if not isinstance(sheetgrid, list):
        raise RuntimeError("the sheet grid is not a list of lists.")
    for row in sheetgrid:
        if not isinstance(row, list):
            raise RuntimeError("the sheet grid is not a list of lists.")
        if len(row) != len(sheetgrid[0]):
            raise RuntimeError("the sheet grid is not rectangular.")
        for sheet in row:
            if sheet in blanksheets:
                pass
            elif (
                _usingfirstgenerationsheets is not False
                and sheet in firstgenerationsheets
            ):
                _usingfirstgenerationsheets = True
            elif (
                _usingfirstgenerationsheets is not True
                and sheet in secondgenerationsheets
            ):
                _usingfirstgenerationsheets = False
            else:
                raise RuntimeError("invalid sheet %s." % sheet)

    if _usingfirstgenerationsheets:
        _dxsheet = 20
        _dysheet = 25
    else:
        _dxsheet = 20
        _dysheet = 15

    # The sheet grid argument follows visual layout, so we need to flip it
    # vertically so that the lower-left sheet has indices (0,0).
    _sheetgrid = list(reversed(sheetgrid))

    _nysheetgrid = len(_sheetgrid)
    _nxsheetgrid = len(_sheetgrid[0])

    _drawterrain = drawterrain
    _drawlabels = drawlabels

    _dotsperhex = dotsperhex
    _writefiletypes = writefiletypes

    _xmin = 0
    _xmax = _dxsheet * _nxsheetgrid
    _ymin = 0
    _ymax = _dysheet * _nysheetgrid

    def sheettoright(iy, ix):
        if ix < _nxsheetgrid - 1:
            return _sheetgrid[iy][ix + 1]
        else:
            return ""

    def sheetbelow(iy, ix):
        if iy > 0:
            return _sheetgrid[iy - 1][ix]
        else:
            return ""

    _sheetlist = []
    for iy in range(0, _nysheetgrid):
        for ix in range(0, _nxsheetgrid):
            sheet = _sheetgrid[iy][ix]
            if sheet not in blanksheets:
                _sheetlist.append(sheet)
                _loweredgeonmap.update({sheet: sheetbelow(iy, ix) != ""})
                _rightedgeonmap.update({sheet: sheettoright(iy, ix) != ""})

    for sheet in _sheetlist:
        filename = os.path.join(os.path.dirname(__file__), "mapsheets", sheet + ".py")
        with open(filename, "r", encoding="utf-8") as f:
            s = f.read(-1)
            _terrain[sheet] = ast.literal_eval(s)

    global _saved
    _saved = False

    global _allwater, _forest, _allforest, _freshwater, _wilderness, _maxurbansize

    global level0color, level1color, level2color, level3color
    global level0ridgecolor, level1ridgecolor, level2ridgecolor
    global forestcolor, forestalpha, foresthatch
    global urbancolor, urbanalpha, urbanoutlinecolor, townhatch, cityhatch
    global megahexcolor, megahexalpha
    global roadcolor, roadoutlinecolor
    global dockcolor, dockoutlinecolor
    global watercolor, wateroutlinecolor
    global riverwidth, wideriverwidth
    global hexcolor, hexalpha
    global labelcolor

    def lighten(color, f):
        return list((1 - f) + f * x for x in color)

    def darken(color, f):
        return list(min(1, f * x) for x in color)

    def equivalentgray(color):
        x = 0.30 * color[0] + 0.59 * color[1] + 0.11 * color[2]
        return [x, x, x]

    # Defaults

    _allwater = False
    _allforest = False
    _forest = True
    _maxurbansize = 5
    _freshwater = True
    _frozen = False
    _wilderness = False

    riverwidth = 14
    wideriverwidth = 35

    townhatch = "xx"
    cityhatch = "xx"
    foresthatch = ".o"

    if not _drawterrain:

        hexcolor = [0.50, 0.50, 0.50]
        hexalpha = 1.0
        labelcolor = hexcolor

    elif style == "openwater":

        _allwater = True
        watercolor = [0.77, 0.89, 0.95]

        megahexcolor = [1.00, 1.00, 1.00]
        megahexalpha = 0.12

        hexcolor = darken(watercolor, 0.7)
        hexalpha = 1.0
        labelcolor = hexcolor

    elif style == "seaice":

        _allwater = True
        # This is the same color as level 0 of winter tundra below.
        watercolor = lighten([0.85, 0.85, 0.85], 1 / 20)

        hexcolor = [0.7, 0.80, 0.90]
        hexalpha = 1.0
        labelcolor = hexcolor

        megahexcolor = hexcolor
        megahexalpha = 0.025

    else:

        _allwater = False
        forestalpha = 0.5
        forestcolor = [0.50, 0.65, 0.50]

        if style == "wintertundra" or style == "winterborealforest":

            basecolor = [0.85, 0.85, 0.85]
            dilution = [1 / 20, 1 / 2, 2 / 2, 3 / 2]

            megahexcolor = [0.00, 0.00, 0.00]
            megahexalpha = 0.015

            _forest = False
            _wilderness = True
            _maxurbansize = 0
            _frozen = True
            if style == "winterborealforest":
                _allforest = True
                megahexcolor = forestcolor
                megahexalpha = 0.07

        elif style == "arid" or style == "desert":

            basecolor = [0.78, 0.76, 0.67]
            dilution = [1 / 3, 2 / 3, 3 / 3, 4 / 3]

            megahexcolor = [1.00, 1.00, 1.00]
            megahexalpha = 0.22

            riverwidth = 9

            if style == "desert":
                _wilderness = True
                _forest = False
                _freshwater = False
                _maxurbansize = 0

        elif style == "temperate" or style == "summertundra" or style == "original":

            basecolor = [0.50, 0.70, 0.45]
            dilution = [2 / 6, 3 / 6, 4 / 6, 5 / 6]

            megahexcolor = [1.00, 1.00, 1.00]
            megahexalpha = 0.12

            if style == "summertundra":
                _forest = False
                _wilderness = True
                _maxurbansize = 0

        elif (
            style == "tropical"
            or style == "tropicalforest"
            or style == "summerborealforest"
        ):

            basecolor = [0.50, 0.70, 0.45]
            dilution = [3 / 6, 4 / 6, 5 / 6, 6 / 6]

            forestcolor = darken(forestcolor, 0.8)

            megahexcolor = [1.00, 1.00, 1.00]
            megahexalpha = 0.08

            if style == "tropicalforest":
                _allforest = True
                _wilderness = False
                _maxurbansize = 4
            elif style == "summerborealforest":
                _allforest = True
                _wilderness = True
                _maxurbansize = 0

        else:

            raise RuntimeError("invalid map style %r." % style)

        level0color = lighten(basecolor, dilution[0])
        level1color = lighten(basecolor, dilution[1])
        level2color = lighten(basecolor, dilution[2])
        level3color = lighten(basecolor, dilution[3])

        level0ridgecolor = level1color
        level1ridgecolor = level2color
        level2ridgecolor = level3color

        if style == "original":
            # The original colors don't fit into the scheme of increasingly darker
            # shades of the same color, so are hard wired.
            level1color = [0.87, 0.85, 0.78]
            level2color = [0.82, 0.75, 0.65]
            level3color = [0.77, 0.65, 0.55]
            level0ridgecolor = lighten(basecolor, 1 / 2)
            level1ridgecolor = level2color
            level2ridgecolor = level3color

        if _frozen:
            watercolor = lighten([0.85, 0.85, 0.85], 1 / 20)
            wateroutlinecolor = watercolor
        else:
            watercolor = [0.77, 0.89, 0.95]
            # Darken the water to 100% of the grey value of level 0. Do not lighten it.
            watergrayvalue = equivalentgray(watercolor)[0]
            targetgrayvalue = 1.00 * equivalentgray(level0color)[0]
            if watergrayvalue > targetgrayvalue:
                watercolor = darken(watercolor, targetgrayvalue / watergrayvalue)
            wateroutlinecolor = darken(watercolor, 0.80)

        urbancolor = equivalentgray(level0color)
        urbanoutlinecolor = darken(urbancolor, 0.7)
        roadcolor = urbancolor
        roadoutlinecolor = urbanoutlinecolor
        dockcolor = urbancolor
        dockoutlinecolor = urbanoutlinecolor

        hexcolor = urbanoutlinecolor
        hexalpha = 1.0

        labelcolor = urbanoutlinecolor

    if allforest != None:
        _allforest = allforest
    if forest != None:
        _forest = forest
    if wilderness != None:
        _wilderness = wilderness
    if freshwater != None:
        _freshwater = freshwater
    if maxurbansize != None:
        _maxurbansize = maxurbansize

    if _allforest:
        hexcolor = darken(hexcolor, 0.7)
    if _frozen:
        forestalpha += 0.20


def startdrawmap(
    show=False, xmin=None, ymin=None, xmax=None, ymax=None, watermark=None
):
    """
    Draw the map.
    """

    def toxy(sheet, x, y):
        XX = int(x)
        YY = int(y)
        dx = x - XX
        dy = y - YY
        x0, y0 = aphexcode.toxy("%s-%02d%02d" % (sheet, XX, YY))
        return x0 + dx, y0 - dy

    def drawhexes(sheet, labels, **kwargs):
        for label in labels:
            apdraw.drawhex(
                *aphexcode.toxy("%s-%04d" % (sheet, label)), zorder=0, **kwargs
            )

    def drawpaths(sheet, paths, **kwargs):
        for path in paths:
            xy = [toxy(sheet, *hxy) for hxy in path]
            x = [xy[0] for xy in xy]
            y = [xy[1] for xy in xy]
            apdraw.drawlines(x, y, zorder=0, **kwargs)

    fullmap = (xmin is None) and (xmax is None) and (ymin is None) and (ymax is None)

    global _saved
    if fullmap and _saved:
        apdraw.restore()
        return

    xmin = xmin if xmin is not None else 0
    xmax = xmax if xmax is not None else _dxsheet * _nxsheetgrid
    ymin = ymin if ymin is not None else 0
    ymax = ymax if ymax is not None else _dysheet * _nysheetgrid

    canvasxmin = max(_xmin, xmin)
    canvasxmax = min(_xmax, xmax)
    canvasymin = max(_ymin, ymin)
    canvasymax = min(_ymax, ymax)

    apdraw.setcanvas(
        canvasxmin, canvasymin, canvasxmax, canvasymax, dotsperhex=_dotsperhex
    )

    if _drawterrain:

        if _allwater:

            # Draw the sheets and level 0.
            for sheet in sheets():
                xmin, ymin, xmax, ymax = sheetlimits(sheet)
                apdraw.drawrectangle(
                    xmin, ymin, xmax, ymax, linewidth=0, fillcolor=watercolor, zorder=0
                )

            # Draw the megahexes.
            for sheet in sheets():
                xmin, ymin, xmax, ymax = sheetlimits(sheet)
                for ix in range(0, _dxsheet):
                    for iy in range(0, _dysheet):
                        x = xmin + ix
                        y = ymin + iy
                        if ix % 2 == 1:
                            y -= 0.5
                        if (x % 10 == 0 and y % 5 == 0) or (
                            x % 10 == 5 and y % 5 == 2.5
                        ):
                            apdraw.drawhex(
                                x,
                                y,
                                size=5,
                                linecolor=megahexcolor,
                                linewidth=megahexwidth,
                                alpha=megahexalpha,
                            )

        else:

            # Draw the sheets and level 0.
            for sheet in sheets():
                xmin, ymin, xmax, ymax = sheetlimits(sheet)
                base = _terrain[sheet]["base"]
                if base == "water":
                    apdraw.drawrectangle(
                        xmin,
                        ymin,
                        xmax,
                        ymax,
                        linewidth=0,
                        fillcolor=watercolor,
                        zorder=0,
                    )
                else:
                    apdraw.drawrectangle(
                        xmin,
                        ymin,
                        xmax,
                        ymax,
                        linewidth=0,
                        fillcolor=level0color,
                        zorder=0,
                    )
                    if _allforest:
                        apdraw.drawrectangle(
                            xmin,
                            ymin,
                            xmax,
                            ymax,
                            hatch=foresthatch,
                            linecolor=forestcolor,
                            alpha=forestalpha,
                            linewidth=0,
                            fillcolor=None,
                            zorder=0,
                        )

            for sheet in sheets():

                # Draw levels 0, 1, and 2.
                drawhexes(
                    sheet,
                    _terrain[sheet]["level0hexes"],
                    linewidth=0,
                    fillcolor=level0color,
                )
                drawhexes(
                    sheet,
                    _terrain[sheet]["level1hexes"],
                    linewidth=0,
                    fillcolor=level1color,
                )
                drawhexes(
                    sheet,
                    _terrain[sheet]["level2hexes"],
                    linewidth=0,
                    fillcolor=level2color,
                )

                if not _wilderness:
                    drawpaths(
                        sheet,
                        _terrain[sheet]["tunnelpaths"],
                        color=roadoutlinecolor,
                        linewidth=tunnelouterwidth,
                        linestyle=(0, (0.3, 0.3)),
                    )
                    drawpaths(
                        sheet,
                        _terrain[sheet]["tunnelpaths"],
                        color=level1color,
                        linewidth=tunnelinnerwidth,
                    )

                # Draw the ridges.
                drawpaths(
                    sheet,
                    _terrain[sheet]["level0ridges"],
                    color=level0ridgecolor,
                    linewidth=ridgewidth,
                )
                drawpaths(
                    sheet,
                    _terrain[sheet]["level1ridges"],
                    color=level1ridgecolor,
                    linewidth=ridgewidth,
                )
                drawpaths(
                    sheet,
                    _terrain[sheet]["level2ridges"],
                    color=level2ridgecolor,
                    linewidth=ridgewidth,
                )

                if _allforest:

                    drawhexes(
                        sheet,
                        _terrain[sheet]["level0hexes"],
                        linewidth=0,
                        linecolor=forestcolor,
                        hatch=foresthatch,
                        alpha=forestalpha,
                    )
                    drawhexes(
                        sheet,
                        _terrain[sheet]["level1hexes"],
                        linewidth=0,
                        linecolor=forestcolor,
                        hatch=foresthatch,
                        alpha=forestalpha,
                    )
                    drawhexes(
                        sheet,
                        _terrain[sheet]["level2hexes"],
                        linewidth=0,
                        linecolor=forestcolor,
                        hatch=foresthatch,
                        alpha=forestalpha,
                    )

                elif _forest:

                    # Draw the forest areas.
                    drawhexes(
                        sheet,
                        _terrain[sheet]["foresthexes"],
                        linewidth=0,
                        linecolor=forestcolor,
                        hatch=foresthatch,
                        alpha=forestalpha,
                    )

                if not _wilderness:

                    # Draw the road clearings.
                    drawpaths(
                        sheet,
                        _terrain[sheet]["clearingpaths"],
                        color=level0color,
                        linewidth=clearingwidth,
                    )

                    # Draw the urban areas.

                    townhexes = []
                    if _maxurbansize >= 1:
                        townhexes += _terrain[sheet]["town1hexes"]
                    if _maxurbansize >= 2:
                        townhexes += _terrain[sheet]["town2hexes"]
                    if _maxurbansize >= 3:
                        townhexes += _terrain[sheet]["town3hexes"]
                    if _maxurbansize >= 4:
                        townhexes += _terrain[sheet]["town4hexes"]
                    if _maxurbansize >= 5:
                        townhexes += _terrain[sheet]["town5hexes"]
                    drawhexes(
                        sheet,
                        townhexes,
                        linewidth=0,
                        fillcolor=None,
                        linecolor=urbanoutlinecolor,
                        hatch=townhatch,
                    )

                    if _maxurbansize >= 5:
                        drawhexes(
                            sheet,
                            _terrain[sheet]["cityhexes"],
                            linewidth=0,
                            fillcolor=urbancolor,
                            linecolor=urbanoutlinecolor,
                            hatch=cityhatch,
                        )

            if _freshwater:
                # Draw water and rivers.
                for sheet in sheets():
                    drawhexes(
                        sheet,
                        _terrain[sheet]["lakehexes"],
                        fillcolor=watercolor,
                        linecolor=wateroutlinecolor,
                        linewidth=waterourlinewidth,
                    )
                    drawpaths(
                        sheet,
                        _terrain[sheet]["riverpaths"],
                        color=wateroutlinecolor,
                        linewidth=riverwidth + waterourlinewidth,
                        capstyle="projecting",
                    )
                    drawpaths(
                        sheet,
                        _terrain[sheet]["wideriverpaths"],
                        color=wateroutlinecolor,
                        linewidth=wideriverwidth + waterourlinewidth,
                        capstyle="projecting",
                    )
                for sheet in sheets():
                    drawhexes(
                        sheet,
                        _terrain[sheet]["lakehexes"],
                        fillcolor=watercolor,
                        linewidth=0,
                    )
                    drawpaths(
                        sheet,
                        _terrain[sheet]["riverpaths"],
                        color=watercolor,
                        linewidth=riverwidth,
                        capstyle="projecting",
                    )
                    drawpaths(
                        sheet,
                        _terrain[sheet]["wideriverpaths"],
                        color=watercolor,
                        linewidth=wideriverwidth,
                        capstyle="projecting",
                    )

            for sheet in sheets():
                # Do not outline sea hexes.
                drawpaths(
                    sheet,
                    _terrain[sheet]["seapaths"],
                    color=wateroutlinecolor,
                    linewidth=riverwidth + waterourlinewidth,
                    capstyle="projecting",
                )
                drawpaths(
                    sheet,
                    _terrain[sheet]["wideseapaths"],
                    color=wateroutlinecolor,
                    linewidth=wideriverwidth + waterourlinewidth,
                    capstyle="projecting",
                )
            for sheet in sheets():
                drawhexes(
                    sheet,
                    _terrain[sheet]["seahexes"],
                    linewidth=0,
                    fillcolor=watercolor,
                )
                drawpaths(
                    sheet,
                    _terrain[sheet]["seapaths"],
                    color=watercolor,
                    linewidth=riverwidth,
                    capstyle="projecting",
                )
                drawpaths(
                    sheet,
                    _terrain[sheet]["wideseapaths"],
                    color=watercolor,
                    linewidth=wideriverwidth,
                    capstyle="projecting",
                )

            for sheet in sheets():
                # Draw the megahexes.
                xmin, ymin, xmax, ymax = sheetlimits(sheet)
                for ix in range(0, _dxsheet):
                    for iy in range(0, _dysheet):
                        x = xmin + ix
                        y = ymin + iy
                        if ix % 2 == 1:
                            y -= 0.5
                        if (x % 10 == 0 and y % 5 == 0) or (
                            x % 10 == 5 and y % 5 == 2.5
                        ):
                            apdraw.drawhex(
                                x,
                                y,
                                size=5,
                                linecolor=megahexcolor,
                                linewidth=megahexwidth,
                                alpha=megahexalpha,
                                zorder=0,
                            )

            if not _wilderness:

                if _freshwater:

                    # Draw the bridges.
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["smallbridgepaths"],
                            color=urbanoutlinecolor,
                            linewidth=bridgeouterwidth,
                            capstyle="butt",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["smallbridgepaths"],
                            color=urbancolor,
                            linewidth=bridgeinnerwidth,
                            capstyle="butt",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["smallbridgepaths"],
                            color=roadcolor,
                            linewidth=roadwidth,
                            capstyle="projecting",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["largebridgepaths"],
                            color=urbanoutlinecolor,
                            linewidth=bridgeouterwidth,
                            capstyle="butt",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["largebridgepaths"],
                            color=urbancolor,
                            linewidth=bridgeinnerwidth,
                            capstyle="butt",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["largebridgepaths"],
                            color=roadcolor,
                            linewidth=roadwidth,
                            capstyle="projecting",
                        )

                    # Draw the trails. We assume they are at level 0.
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["trailpaths"],
                            color=roadoutlinecolor,
                            linewidth=roadwidth + roadoutlinewidth,
                            capstyle="projecting",
                            linestyle=(0, (1, 1)),
                        )
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["trailpaths"],
                            color=level0color,
                            linewidth=roadwidth,
                            capstyle="projecting",
                        )

                    # Draw the roads.
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["roadpaths"],
                            color=roadoutlinecolor,
                            linewidth=roadwidth + roadoutlinewidth,
                            capstyle="projecting",
                        )
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["roadpaths"],
                            color=roadcolor,
                            linewidth=roadwidth,
                            capstyle="projecting",
                        )

                    # Draw the docks.
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["dockpaths"],
                            color=dockoutlinecolor,
                            linewidth=dockwidth + dockoutlinewidth,
                            capstyle="projecting",
                        )
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["dockpaths"],
                            color=dockcolor,
                            linewidth=dockwidth,
                            capstyle="projecting",
                        )

                if not _allforest:

                    # Draw the runways and taxiways.
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["runwaypaths"],
                            color=roadoutlinecolor,
                            linewidth=runwaywidth + roadoutlinewidth,
                            capstyle="projecting",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["taxiwaypaths"],
                            color=roadoutlinecolor,
                            linewidth=taxiwaywidth + roadoutlinewidth,
                            joinstyle="miter",
                            capstyle="projecting",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["runwaypaths"],
                            color=roadcolor,
                            linewidth=runwaywidth,
                            capstyle="projecting",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["taxiwaypaths"],
                            color=roadcolor,
                            linewidth=taxiwaywidth,
                            joinstyle="miter",
                            capstyle="projecting",
                        )

                if _freshwater:

                    # Draw the dams.
                    for sheet in sheets():
                        drawpaths(
                            sheet,
                            _terrain[sheet]["dampaths"],
                            color=roadoutlinecolor,
                            linewidth=damwidth + roadoutlinewidth,
                            capstyle="projecting",
                        )
                        drawpaths(
                            sheet,
                            _terrain[sheet]["dampaths"],
                            color=roadcolor,
                            linewidth=damwidth,
                            capstyle="projecting",
                        )

    # Draw and label the hexes.
    for sheet in sheets():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        for ix in range(0, _dxsheet + 1):
            for iy in range(0, _dysheet + 1):
                x = xmin + ix
                y = ymin + iy
                if ix % 2 == 1:
                    y -= 0.5
                    # aphexode.yoffsetforoddx()
                # Draw the hex if it is on the map and either its center or the center
                # of its upper left edge are on this sheet.
                if isonmap(x, y) and (
                    isonsheet(sheet, x, y) or isonsheet(sheet, x - 0.5, y + 0.25)
                ):
                    apdraw.drawhex(
                        x,
                        y,
                        linecolor=hexcolor,
                        alpha=hexalpha,
                        linewidth=hexwidth,
                        zorder=0,
                    )
                    if _drawlabels:
                        label = aphexcode.tolabel(aphexcode.fromxy(x, y))
                        apdraw.drawhexlabel(
                            x, y, label, color=hexcolor, alpha=hexalpha, zorder=0
                        )

    # Draw missing sheets.
    for iy in range(0, _nysheetgrid):
        for ix in range(0, _nxsheetgrid):
            if _sheetgrid[iy][ix] in blanksheets:
                xmin = ix * _dxsheet
                xmax = xmin + _dxsheet
                ymin = iy * _dysheet
                ymax = ymin + _dysheet
                apdraw.drawrectangle(
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                    linecolor=None,
                    fillcolor=missingcolor,
                    zorder=0,
                )

    if _drawlabels:

        # Label the sheets.
        for sheet in sheets():
            xmin, ymin, xmax, ymax = sheetlimits(sheet)
            dx = 1.0
            dy = 0.5
            if isonmap(xmin + dx, ymin + dy):
                apdraw.drawtext(
                    xmin + dx,
                    ymin + dy,
                    90,
                    sheet,
                    dy=-0.05,
                    size=24,
                    color=labelcolor,
                    alpha=1,
                    zorder=0,
                )

        # Draw the compass rose in the bottom sheet in the leftmost column.
        for iy in range(0, _nysheetgrid):
            sheet = _sheetgrid[iy][0]
            if sheet not in blanksheets:
                xmin, ymin, xmax, ymax = sheetlimits(sheet)
                dx = 1.0
                dy = 1.5
                apdraw.drawcompass(
                    xmin + dx,
                    ymin + dy,
                    apazimuth.tofacing("N"),
                    color=labelcolor,
                    alpha=1,
                    zorder=0,
                )
                break

    if watermark is not None:
        apdraw.drawwatermark(watermark, canvasxmin, canvasymin, canvasxmax, canvasymax)

    if fullmap:
        apdraw.save()
        _saved = True


def enddrawmap(turn, writefiles=True):
    if writefiles:
        for filetype in _writefiletypes:
            apdraw.writefile("map-%02d.%s" % (turn, filetype))
    apdraw.show()


def sheetorigin(sheet):
    """
    Returns the hex coordinates (x0, y0) of the lower left corner of the
    specified sheet.

    The specified sheet must be in the map.
    """

    assert sheet in sheets()

    for iy in range(0, _nysheetgrid):
        for ix in range(0, _nxsheetgrid):
            if sheet == _sheetgrid[iy][ix]:
                x0 = ix * _dxsheet
                y0 = iy * _dysheet
                return x0, y0


def sheetlimits(sheet):
    """
    Returns the hex coordinates (xmin, ymin) and (xmax, ymax) the lower left
    and upper right corners of the specified sheet.
    """

    assert sheet in sheets()

    xmin, ymin = sheetorigin(sheet)

    xmax = xmin + _dxsheet
    ymax = ymin + _dysheet

    return xmin, ymin, xmax, ymax


def sheets():
    """
    Returns a list of the sheets in the map.
    """

    return _sheetlist


def isonsheet(sheet, x, y):
    """
    Returns True if the hex coordinate (x, y) is on the specified sheet.
    Otherwise returns false. The sheet must be in the map.
    """

    assert sheet in sheets()

    xmin, ymin, xmax, ymax = sheetlimits(sheet)

    if _rightedgeonmap[sheet] and _loweredgeonmap[sheet]:
        return xmin < x and x <= xmax and ymin <= y and y < ymax
    elif _rightedgeonmap[sheet]:
        return xmin < x and x <= xmax and ymin < y and y < ymax
    elif _loweredgeonmap[sheet]:
        return xmin < x and x < xmax and ymin <= y and y < ymax
    else:
        return xmin < x and x < xmax and ymin < y and y < ymax


def tosheet(x, y):
    """
    Returns the sheet containing the hex coordinates (x, y). If no sheet contains
    the coordinates, returns None.
    """

    for sheet in sheets():
        if isonsheet(sheet, x, y):
            return sheet
    return None


def isonmap(x, y):
    """
    Returns True if the hex coordinate (x, y) is on the map.
    Otherwise returns false.
    """

    return tosheet(x, y) != None and (
        _xmin < x and x < _xmax and _ymin < y and y < _ymax
    )


def altitude(x, y, sheet=None):
    """
    Returns the altitude of the hex at the position (x, y), which must refer to a
    hex center.
    """

    assert aphex.isvalid(x, y)

    if aphex.iscenter(x, y):

        if _allwater:
            return 0

        if sheet is None:
            sheet = tosheet(x, y)
        label = int(aphexcode.tolabel(aphexcode.fromxy(x, y, sheet=sheet)))
        if label in _terrain[sheet]["level2hexes"]:
            return 2
        elif label in _terrain[sheet]["level1hexes"]:
            return 1
        else:
            return 0

    else:

        x0, y0, x1, y1 = aphex.sidetocenters(x, y)
        sheet0 = tosheet(x0, y0)
        sheet1 = tosheet(x1, y1)
        assert sheet0 != None or sheet1 != None
        if sheet0 == None:
            sheet0 = sheet1
        if sheet1 == None:
            sheet1 = sheet0
        return max(altitude(x0, y0, sheet=sheet0), altitude(x1, y1, sheet=sheet1))


################################################################################
