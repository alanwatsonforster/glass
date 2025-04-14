"""
The map.
"""

import apxo.azimuth as apazimuth
import apxo.draw as apdraw
import apxo.hex as aphex
import apxo.hexcode as aphexcode
import apxo.mapstyle as apmapstyle

import json
import math
import os

################################################################################

_writefiles = True


def setwritefiles(value):
    """
    Set the flag for writing map files.

    If the value argument is false, do not write map files. Otherwise, write the map files.
    """
    global _writefiles
    _writefiles = value


_writefiletypes = ["png"]


def setwritefiletypes(value):
    """
    Set the types of the map files.

    The value argument must be a list of strings of the suffixes of supported map file types. 
    Supported suffixes include "png and "pdf".
    """
    global _writefiletypes
    _writefiletypes = value


_watermark = None


def setwatermark(value):
    """
    Set the watermark  for maps.

    The value argument must be a string.
    """
    global _watermark
    _watermark = value


################################################################################


_terrain = {}

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

_saved = False

_rotation = 0

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

riverwidth = 14
wideriverwidth = 35

townhatch = "xx"
cityhatch = "xx"
foresthatch = ".o"

borderwidth = 0.02

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
    """
    Return true if the map is using first-generation map sheets, otherwise return false.
    """
    return _usingfirstgenerationsheets


def setmap(
    sheetgrid,
    dotsperhex=80,
    style="airstrike",
    levelincrement=1,
    rotation=0,
):
    """
    Set up the map.

    The sheetgrid argument must be a 2D array of sheet specificiers. The sheets
    are ordered top-to-bottom and left-to-right. All of the rows must be the
    same length. Each sheet specifier must be a string consisting of a sheet
    name optionally followed by "/i" if the sheet is inverted. No sheet name can
    be used more than once and all sheets must be from the same generation.

    The first-generation sheet names are: "A", "B", "C", ..., "Z".

    The second-generation sheet names are: "A1", "A2, "A3, ..., "A6", "B1", ...,
    "B6", "C1", ..., "C6", "D1", ..., "D6.

    The dotsperhex argument must be an integer. It specifies the resolution of
    pixelated output files in dots per hex (or more precisely dots between hex
    centers).

    The style argument must be a string corresponding to a style. It can be
    "airstrike", "airsuperiority", or one of the following optionally prefixed
    by "snowy" or "frozen" and optionally suffixed by "hills", "plain", or
    "islands:  "water", "temperate", "temperateforest", "tundra",
    "borealforest", "tropical", "tropicalforest", "arid", and "desert".

    The levelincrement argument gives the number of altitude levels
    corresponding to one terrain level. It must be a positive integer. For
    example, if levelincrement is 1, then terrain levels 0, 1, and 2 correspond
    to altitude levels 0, 1, and 2, but if levelincrement is 2, then they
    correspond to altitude levels 0, 2, and 4.

    The rotation parameter determines the rotation of the map with respect to
    the normal orientation.
    """

    global _usingfirstgenerationsheets
    global _dxsheet
    global _dysheet

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
    global _rotation

    _usingfirstgenerationsheets = None

    if not isinstance(sheetgrid, list):
        raise RuntimeError("the sheet grid is not a list of lists.")
    for row in sheetgrid:
        if not isinstance(row, list):
            raise RuntimeError("the sheet grid is not a list of lists.")
        if len(row) != len(sheetgrid[0]):
            raise RuntimeError("the sheet grid is not rectangular.")
        for sheet in row:
            if sheet[-2:] == "/i":
                sheet = sheet[:-2]
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

    _dotsperhex = dotsperhex

    _xmin = +0.33 - borderwidth
    _xmax = _dxsheet * _nxsheetgrid - 0.33 + borderwidth
    _ymin = -borderwidth
    _ymax = _dysheet * _nysheetgrid + borderwidth

    global _saved
    _saved = False

    global _style
    _style = apmapstyle.getstyle(style)
    if _style == None:
        raise RuntimeError("invalid style %r." % style)

    _rotation = rotation

    global _levelincrement
    _levelincrement = levelincrement

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
            if sheet[-2:] == "/i":
                sheet = sheet[:-2]
                inverted = True
            else:
                inverted = False
            _sheetgrid[iy][ix] = sheet
            if sheet not in blanksheets:
                _sheetlist.append(sheet)
                _loweredgeonmap.update({sheet: sheetbelow(iy, ix) != ""})
                _rightedgeonmap.update({sheet: sheettoright(iy, ix) != ""})
                terrain = _loadterrain(sheet)
                if inverted:
                    terrain = _invertterrain(terrain)
                terrain = _styleterrain(terrain)
                _terrain[sheet] = terrain


################################################################################


def _loadterrain(sheet):
    filename = os.path.join(os.path.dirname(__file__), "mapsheetdata", sheet + ".json")
    with open(filename, "r", encoding="utf-8") as f:
        terrain = json.load(f)
    return terrain

def _styleterrain(terrain):

    wilderness = _style["wilderness"]
    water = _style["water"]
    forest = _style["forest"]
    maxurbansize = _style["maxurbansize"]
    leveloffset = _style["leveloffset"]

    if water == "all" or water == "islands":
        terrain["base"] = "water"

    if water == "all":
        terrain["level0hexes"] = []
        terrain["level0ridgepaths"] = []
        terrain["level1hexes"] = []
        terrain["level2hexes"] = []
        terrain["level1ridgepaths"] = []
        terrain["level2ridgepaths"] = []
    elif water == "islands":
        terrain["level0hexes"] = terrain["level1hexes"]
        terrain["level1hexes"] = terrain["level2hexes"]
        terrain["level2hexes"] = []
        terrain["level0ridgepaths"] = terrain["level1ridgepaths"]
        terrain["level1ridgepaths"] = terrain["level2ridgepaths"]
        terrain["level2ridgepaths"] = []
    elif leveloffset == -1:
        terrain["level1hexes"] = terrain["level2hexes"]
        terrain["level2hexes"] = []
        terrain["level0ridgepaths"] = terrain["level1ridgepaths"]
        terrain["level1ridgepaths"] = terrain["level2ridgepaths"]
        terrain["level2ridgepaths"] = []
    elif leveloffset == -2:
        terrain["level1hexes"] = []
        terrain["level2hexes"] = []
        terrain["level0ridgepaths"] = terrain["level2ridgepaths"]
        terrain["level1ridgepaths"] = []
        terrain["level2ridgepaths"] = []
    elif leveloffset == -3:
        terrain["level1hexes"] = []
        terrain["level2hexes"] = []
        terrain["level1ridgepaths"] = []
        terrain["level2ridgepaths"] = []

    if wilderness or water == "all":
        terrain["townhexes"] = []
    else:
        terrain["townhexes"] = []
        if maxurbansize >= 1:
            terrain["townhexes"] += terrain["town1hexes"]
        if maxurbansize >= 2:
            terrain["townhexes"] += terrain["town2hexes"]
        if maxurbansize >= 3:
            terrain["townhexes"] += terrain["town3hexes"]
        if maxurbansize >= 4:
            terrain["townhexes"] += terrain["town4hexes"]
        if maxurbansize >= 5:
            terrain["townhexes"] += terrain["town5hexes"]
    if water == "islands":
        newtownhexes = []
        for townhex in terrain["townhexes"]:
            if (
                townhex
                in terrain["level0hexes"]
                + terrain["level1hexes"]
                + terrain["level2hexes"]
            ):
                newtownhexes.append(townhex)
        terrain["townhexes"] = newtownhexes

    level0townhexes = []
    level1townhexes = []
    level2townhexes = []
    for townhex in terrain["townhexes"]:
        if townhex in terrain["level2hexes"]:
            level2townhexes.append(townhex)
        elif townhex in terrain["level1hexes"]:
            level1townhexes.append(townhex)
        else:
            level0townhexes.append(townhex)
    terrain["level0townhexes"] = level0townhexes
    terrain["level1townhexes"] = level1townhexes
    terrain["level2townhexes"] = level2townhexes

    if wilderness or water == "all" or water == "islands" or maxurbansize < 5:
        terrain["cityhexes"] = []

    if wilderness or water == "desert" or water == "all" or water == "islands":
        terrain["smallbridgepaths"] = []
        terrain["largebridgepaths"] = []

    if water == "all" or water == "islands" or wilderness:
        terrain["dampaths"] = []

    global riverwidth
    if water == "arid":
        riverwidth = 9
    else:
        riverwidth = 14

    if water == "desert" or water == "all" or water == "islands":
        terrain["lakehexes"] = []
        terrain["riverpaths"] = []
        terrain["wideriverpaths"] = []

    if wilderness or water == "all" or water == "islands":
        terrain["roadpaths"] = []
        terrain["trailpaths"] = []
        terrain["dockpaths"] = []
        terrain["clearingpaths"] = []

    if wilderness or water == "all" or water == "islands":
        terrain["tunnelpaths"] = []
    elif leveloffset != 0:
        terrain["roadpaths"] += terrain["tunnelpaths"]
        terrain["tunnelpaths"] = []

    if wilderness or water == "all" or water == "islands" or forest == "all":
        terrain["runwaypaths"] = []
        terrain["taxiwaypaths"] = []

    if forest is False or water == "all":
        terrain["foresthexes"] = []
    elif water == "islands":
        if forest == "all":
            terrain["foresthexes"] = (
                terrain["level0hexes"] + terrain["level1hexes"] + terrain["level2hexes"]
            )
        else:
            newforesthexes = []
            for foresthex in terrain["foresthexes"]:
                if (
                    foresthex
                    in terrain["level0hexes"]
                    + terrain["level1hexes"]
                    + terrain["level2hexes"]
                ):
                    newforesthexes.append(foresthex)
            terrain["foresthexes"] = newforesthexes
        terrain["forest"] = True
    elif forest == "all":
        terrain["foresthexes"] = "all"

    return terrain


def _invertterrain(oldterrain):

    xcenter = oldterrain["center"][0]
    ycenter = oldterrain["center"][1]
    generation = oldterrain["generation"]

    def duplicatehexes(oldhexes):
        return list(duplicatehex(oldhex) for oldhex in oldhexes)

    def duplicatehex(oldhex):
        oldx = oldhex // 100
        oldy = oldhex % 100
        if int(oldx) % 2 == 1:
            if generation == 1:
                oldy -= 0.5
            else:
                oldy += 0.5
        newx = xcenter - (oldx - xcenter)
        newy = ycenter - (oldy - ycenter)
        if int(newx) % 2 == 1:
            if generation == 1:
                newy += 0.5
            else:
                newy -= 0.5
        newhex = newx * 100 + newy
        return int(newhex)

    def duplicatepaths(oldpaths):
        return list(duplicatepath(oldpath) for oldpath in oldpaths)

    def duplicatepath(oldpath):
        return list(duplicatexy(oldxy) for oldxy in oldpath)

    def duplicatexy(oldxy):
        oldx = oldxy[0]
        oldy = oldxy[1]
        if int(oldx) % 2 == 1:
            if generation == 1:
                oldy -= 0.5
            else:
                oldy += 0.5
        newx = xcenter - (oldx - xcenter)
        newy = ycenter - (oldy - ycenter)
        if int(newx) % 2 == 1:
            if generation == 1:
                newy += 0.5
            else:
                newy -= 0.5
        newxy = [newx, newy]
        return newxy

    newterrain = {}
    for key in oldterrain.keys():
        if key[-5:] == "hexes":
            newterrain[key] = duplicatehexes(oldterrain[key])
        elif key[-5:] == "paths":
            newterrain[key] = duplicatepaths(oldterrain[key])
        else:
            newterrain[key] = oldterrain[key]
    return newterrain


################################################################################


def startdrawmap(
    show=False,
    xmin=None,
    ymin=None,
    xmax=None,
    ymax=None,
    sheets=None,
    watermark=None,
    compactstacks=True,
):
    """
    Start to draw the map.
    """

    level0color = _style["level0color"]
    level1color = _style["level1color"]
    level2color = _style["level2color"]
    level0ridgecolor = _style["level0ridgecolor"]
    level1ridgecolor = _style["level1ridgecolor"]
    level2ridgecolor = _style["level2ridgecolor"]
    forestcolor = _style["forestcolor"]
    forestalpha = _style["forestalpha"]
    urbancolor = _style["urbancolor"]
    urbanoutlinecolor = _style["urbanoutlinecolor"]
    megahexcolor = _style["megahexcolor"]
    megahexalpha = _style["megahexalpha"]
    roadcolor = _style["roadcolor"]
    roadoutlinecolor = _style["roadoutlinecolor"]
    dockcolor = _style["dockcolor"]
    dockoutlinecolor = _style["dockoutlinecolor"]
    watercolor = _style["watercolor"]
    wateroutlinecolor = _style["wateroutlinecolor"]
    hexcolor = _style["hexcolor"]
    hexalpha = _style["hexalpha"]
    labelcolor = _style["labelcolor"]

    def drawhex(x, y, label=False, **kwargs):
        apdraw.drawhex(x, y, zorder=0, **kwargs)

    def drawhexlabel(x, y, label, **kwargs):
        apdraw.drawhexlabel(x, y, label, zorder=0, **kwargs)

    def drawhexes(sheet, labels, **kwargs):
        for label in labels:
            x, y = aphexcode.toxy("%s-%04d" % (sheet, label))
            if isnearcanvas(x, y):
                drawhex(x, y, **kwargs)

    def drawpaths(sheet, paths, **kwargs):
        for path in paths:
            xy = [toxy(sheet, *hxy) for hxy in path]
            # Do not use the naive isnearcanvas optimization used above in
            # drawhexes, as paths can cross the canvas without their endpoints
            # being near to it.
            x = [xy[0] for xy in xy]
            y = [xy[1] for xy in xy]
            apdraw.drawlines(x, y, zorder=0, **kwargs)

    def drawrectangle(xmin, ymin, xmax, ymax, **kwargs):
        apdraw.drawrectangle(xmin, ymin, xmax, ymax, zorder=0, **kwargs)

    def drawtext(x, y, angle, text, **kwargs):
        apdraw.drawtext(x, y, angle, text, zorder=0, **kwargs)

    def drawcompass(x, y, facing, **kwargs):
        apdraw.drawcompass(x, y, facing, zorder=0, **kwargs)

    def drawwatermark(text, xmin, ymin, xmax, ymax, **kwargs):
        apdraw.drawwatermark(text, xmin, ymin, xmax, ymax, zorder=0, **kwargs)

    if xmin is not None and xmax is not None and ymin is not None and ymax is not None:

        canvasxmin = max(_xmin, xmin)
        canvasxmax = min(_xmax, xmax)
        canvasymin = max(_ymin, ymin)
        canvasymax = min(_ymax, ymax)

    elif sheets is not None:

        canvasxmin = _xmax
        canvasymin = _ymax
        canvasxmax = _xmin
        canvasymax = _ymin
        for sheet in sheets:
            sheetxmin, sheetymin, sheetxmax, sheetymax = sheetlimits(sheet)
            canvasxmin = min(canvasxmin, sheetxmin)
            canvasymin = min(canvasymin, sheetymin)
            canvasxmax = max(canvasxmax, sheetxmax)
            canvasymax = max(canvasymax, sheetymax)

    else:

        canvasxmin = _xmin
        canvasymin = _ymin
        canvasxmax = _xmax
        canvasymax = _ymax

    fullmap = (
        canvasxmin == _xmin
        and canvasymin == _ymin
        and canvasxmax == _xmax
        and canvasymax == _ymax
    )

    global _saved
    if fullmap and _saved:
        apdraw.restore()
        return

    def isnearcanvas(x, y):
        """
        Return True is (x, y) is on the canvas or within 0.5 unit of it.
        """
        return (
            x >= canvasxmin - 0.5
            and x <= canvasxmax + 0.5
            and y >= canvasymin - 0.5
            and y <= canvasymax + 0.5
        )

    def issheetnearcanvas(sheet):
        """
        Return True is any part of the sheet is on the canvas or within 0.5 unit of it.
        """
        sheetxmin, sheetymin, sheetxmax, sheetymax = sheetlimits(sheet)
        return (
            sheetxmax >= canvasxmin - 0.5
            and sheetxmin <= canvasxmax + 0.5
            and sheetymax >= canvasymin - 0.5
            and sheetymin <= canvasymax + 0.5
        )

    def sheetsnearcanvas():
        return filter(lambda sheet: issheetnearcanvas(sheet), _sheetlist)

    apdraw.setcanvas(
        canvasxmin, canvasymin, canvasxmax, canvasymax, dotsperhex=_dotsperhex
    )

    if all(_terrain[sheet]["base"] == "water" for sheet in _sheetlist):
        bordercolor = watercolor
    elif all(_terrain[sheet]["base"] == "land" for sheet in _sheetlist):
        bordercolor = level0color
    else:
        bordercolor = hexcolor

    drawrectangle(
        canvasxmin,
        canvasymin,
        canvasxmax,
        canvasymax,
        fillcolor=bordercolor,
        linecolor=None,
    )

    # Draw the sheets, base, and levels 0 to 2.

    for sheet in sheetsnearcanvas():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)

        # Draw base.

        if _terrain[sheet]["base"] == "water":
            basecolor = watercolor
        else:
            basecolor = level0color
        drawrectangle(
            xmin,
            ymin,
            xmax,
            ymax,
            linewidth=0,
            fillcolor=basecolor,
        )

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

        drawpaths(
            sheet,
            _terrain[sheet]["tunnelpaths"],
            linecolor=roadoutlinecolor,
            linewidth=tunnelouterwidth,
            linestyle=(0, (0.3, 0.3)),
        )
        drawpaths(
            sheet,
            _terrain[sheet]["tunnelpaths"],
            linecolor=level1color,
            linewidth=tunnelinnerwidth,
        )

        # Draw the ridges.

        drawpaths(
            sheet,
            _terrain[sheet]["level0ridgepaths"],
            linecolor=level0ridgecolor,
            linewidth=ridgewidth,
        )
        drawpaths(
            sheet,
            _terrain[sheet]["level1ridgepaths"],
            linecolor=level1ridgecolor,
            linewidth=ridgewidth,
        )
        drawpaths(
            sheet,
            _terrain[sheet]["level2ridgepaths"],
            linecolor=level2ridgecolor,
            linewidth=ridgewidth,
        )

        # Draw the forest areas.

        if _terrain[sheet]["foresthexes"] == "all":
            drawrectangle(
                xmin,
                ymin,
                xmax,
                ymax,
                hatch=foresthatch,
                linecolor=forestcolor,
                alpha=forestalpha,
                linewidth=0,
                fillcolor=None,
            )
            drawhexes(
                sheet,
                _terrain[sheet]["level0townhexes"],
                linewidth=0,
                fillcolor=level0color,
            )
            drawhexes(
                sheet,
                _terrain[sheet]["level1townhexes"],
                linewidth=0,
                fillcolor=level1color,
            )
            drawhexes(
                sheet,
                _terrain[sheet]["level2townhexes"],
                linewidth=0,
                fillcolor=level2color,
            )
        else:
            drawhexes(
                sheet,
                _terrain[sheet]["foresthexes"],
                hatch=foresthatch,
                linecolor=forestcolor,
                alpha=forestalpha,
                linewidth=0,
                fillcolor=None,
            )

        # Draw the road clearings.

        drawpaths(
            sheet,
            _terrain[sheet]["clearingpaths"],
            linecolor=level0color,
            linewidth=clearingwidth,
        )

        # Draw the urban areas.

        drawhexes(
            sheet,
            _terrain[sheet]["townhexes"],
            linewidth=0,
            fillcolor=None,
            linecolor=urbanoutlinecolor,
            hatch=townhatch,
        )

        drawhexes(
            sheet,
            _terrain[sheet]["cityhexes"],
            linewidth=0,
            fillcolor=urbancolor,
            linecolor=urbanoutlinecolor,
            hatch=cityhatch,
        )

    # Draw water and rivers.

    for sheet in sheetsnearcanvas():
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
            linecolor=wateroutlinecolor,
            linewidth=riverwidth + waterourlinewidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["wideriverpaths"],
            linecolor=wateroutlinecolor,
            linewidth=wideriverwidth + waterourlinewidth,
            capstyle="projecting",
        )
    for sheet in sheetsnearcanvas():
        drawhexes(
            sheet,
            _terrain[sheet]["lakehexes"],
            fillcolor=watercolor,
            linewidth=0,
        )
        drawpaths(
            sheet,
            _terrain[sheet]["riverpaths"],
            linecolor=watercolor,
            linewidth=riverwidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["wideriverpaths"],
            linecolor=watercolor,
            linewidth=wideriverwidth,
            capstyle="projecting",
        )

    for sheet in sheetsnearcanvas():
        # Do not outline sea hexes.
        drawpaths(
            sheet,
            _terrain[sheet]["seapaths"],
            linecolor=wateroutlinecolor,
            linewidth=riverwidth + waterourlinewidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["wideseapaths"],
            linecolor=wateroutlinecolor,
            linewidth=wideriverwidth + waterourlinewidth,
            capstyle="projecting",
        )
    for sheet in sheetsnearcanvas():
        drawhexes(
            sheet,
            _terrain[sheet]["seahexes"],
            linewidth=0,
            fillcolor=watercolor,
        )
        drawpaths(
            sheet,
            _terrain[sheet]["seapaths"],
            linecolor=watercolor,
            linewidth=riverwidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["wideseapaths"],
            linecolor=watercolor,
            linewidth=wideriverwidth,
            capstyle="projecting",
        )

    # Draw the mega-hexes.

    for x in range(0, _nxsheetgrid * _dxsheet + 5):
        for y in range(0, _nysheetgrid * _dysheet + 5):
            if x % 2 == 1:
                y -= 0.5
            if (x % 10 == 0 and y % 5 == 0) or (x % 10 == 5 and y % 5 == 2.5):
                drawhex(
                    x,
                    y,
                    size=5,
                    linecolor=megahexcolor,
                    linewidth=megahexwidth,
                    alpha=megahexalpha,
                )

    # Draw the bridges.
    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["smallbridgepaths"],
            linecolor=urbanoutlinecolor,
            linewidth=bridgeouterwidth,
            capstyle="butt",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["smallbridgepaths"],
            linecolor=urbancolor,
            linewidth=bridgeinnerwidth,
            capstyle="butt",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["smallbridgepaths"],
            linecolor=roadcolor,
            linewidth=roadwidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["largebridgepaths"],
            linecolor=urbanoutlinecolor,
            linewidth=bridgeouterwidth,
            capstyle="butt",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["largebridgepaths"],
            linecolor=urbancolor,
            linewidth=bridgeinnerwidth,
            capstyle="butt",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["largebridgepaths"],
            linecolor=roadcolor,
            linewidth=roadwidth,
            capstyle="projecting",
        )

    # Draw the trails. We assume they are at level 0.

    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["trailpaths"],
            linecolor=roadoutlinecolor,
            linewidth=roadwidth + roadoutlinewidth,
            capstyle="projecting",
            linestyle=(0, (1, 1)),
        )
    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["trailpaths"],
            linecolor=level0color,
            linewidth=roadwidth,
            capstyle="projecting",
        )

    # Draw the roads.

    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["roadpaths"],
            linecolor=roadoutlinecolor,
            linewidth=roadwidth + roadoutlinewidth,
            capstyle="projecting",
        )
    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["roadpaths"],
            linecolor=roadcolor,
            linewidth=roadwidth,
            capstyle="projecting",
        )

    # Draw the docks.

    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["dockpaths"],
            linecolor=dockoutlinecolor,
            linewidth=dockwidth + dockoutlinewidth,
            capstyle="projecting",
        )
    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["dockpaths"],
            linecolor=dockcolor,
            linewidth=dockwidth,
            capstyle="projecting",
        )

    # Draw the runways and taxiways.

    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["runwaypaths"],
            linecolor=roadoutlinecolor,
            linewidth=runwaywidth + roadoutlinewidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["taxiwaypaths"],
            linecolor=roadoutlinecolor,
            linewidth=taxiwaywidth + roadoutlinewidth,
            joinstyle="miter",
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["runwaypaths"],
            linecolor=roadcolor,
            linewidth=runwaywidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["taxiwaypaths"],
            linecolor=roadcolor,
            linewidth=taxiwaywidth,
            joinstyle="miter",
            capstyle="projecting",
        )

    # Draw the dams.

    for sheet in sheetsnearcanvas():
        drawpaths(
            sheet,
            _terrain[sheet]["dampaths"],
            linecolor=roadoutlinecolor,
            linewidth=damwidth + roadoutlinewidth,
            capstyle="projecting",
        )
        drawpaths(
            sheet,
            _terrain[sheet]["dampaths"],
            linecolor=roadcolor,
            linewidth=damwidth,
            capstyle="projecting",
        )

    # Draw the border.

    drawrectangle(
        _xmin,
        _ymin,
        _xmax,
        _ymin + borderwidth,
        fillcolor=bordercolor,
        linecolor=None,
    )
    drawrectangle(
        _xmin,
        _ymax - borderwidth,
        _xmax,
        _ymax,
        fillcolor=bordercolor,
        linecolor=None,
    )
    drawrectangle(
        _xmin,
        _ymin,
        _xmin + borderwidth,
        _ymax,
        fillcolor=bordercolor,
        linecolor=None,
    )
    drawrectangle(
        _xmax - borderwidth,
        _ymin,
        _xmax,
        _ymax,
        fillcolor=bordercolor,
        linecolor=None,
    )

    # Draw and label the hexes.

    for sheet in sheetsnearcanvas():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        for ix in range(0, _dxsheet + 1):
            for iy in range(0, _dysheet + 1):
                x = xmin + ix
                y = ymin + iy
                if ix % 2 == 1:
                    y -= 0.5
                    # aphexode.yoffsetforoddx()
                # Draw the hex if it is on the map, is near the canvas, and
                # either its center or the center of its upper left edge are on
                # this sheet.
                if (
                    isonmap(x, y)
                    and isnearcanvas(x, y)
                    and (isonsheet(sheet, x, y) or isonsheet(sheet, x - 0.5, y + 0.25))
                ):
                    drawhex(
                        x,
                        y,
                        linecolor=hexcolor,
                        alpha=hexalpha,
                        linewidth=hexwidth,
                    )
                    label = aphexcode.tolabel(aphexcode.fromxy(x, y))
                    drawhexlabel(x, y, label, color=hexcolor, alpha=hexalpha)

    # Label the sheets.

    for sheet in sheetsnearcanvas():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        dx = 1.0
        dy = 0.5
        if isonmap(xmin + dx, ymin + dy):
            drawtext(
                xmin + dx,
                ymin + dy,
                90,
                sheet,
                dy=-0.05,
                size=24,
                color=labelcolor,
                alpha=1,
            )

    # Draw the compass rose in the lower left corner of the canvas.

    compassx = math.ceil(canvasxmin + 1)
    compassy = math.ceil(canvasymin + 1)
    if compassx % 2 == 1:
        compassy += 0.5
    drawcompass(
        compassx,
        compassy,
        apazimuth.tofacing("N"),
        color=labelcolor,
        alpha=1,
    )

    # Draw missing sheets.

    for iy in range(0, _nysheetgrid):
        for ix in range(0, _nxsheetgrid):
            if _sheetgrid[iy][ix] in blanksheets:
                xmin = ix * _dxsheet
                xmax = xmin + _dxsheet
                ymin = iy * _dysheet
                ymax = ymin + _dysheet
                drawrectangle(
                    xmin - 0.33,
                    ymin,
                    xmax + 0.33,
                    ymax,
                    linecolor=None,
                    fillcolor=level0color,
                )

    # Draw watermarks.

    if _watermark is not None:
        drawwatermark(_watermark, canvasxmin, canvasymin, canvasxmax, canvasymax)
    elif watermark is not None:
        drawwatermark(watermark, canvasxmin, canvasymin, canvasxmax, canvasymax)

    apdraw.setcompactstacks(compactstacks)

    if fullmap and _writefiles:
        apdraw.save()
        _saved = True


def enddrawmap(turn, writefiles=True):
    if _writefiles and writefiles:
        for filetype in _writefiletypes:
            apdraw.writefile("map-%02d.%s" % (turn, filetype), rotation=_rotation)
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


def toxy(sheet, x, y):
    XX = int(x)
    YY = int(y)
    dx = x - XX
    dy = y - YY
    x0, y0 = aphexcode.toxy("%s-%02d%02d" % (sheet, XX, YY))
    return x0 + dx, y0 - dy


def altitude(x, y, sheet=None):
    """
    Returns the altitude of the hex at the position (x, y), which must refer to a
    hex center.
    """

    assert aphex.isvalid(x, y)

    if aphex.iscenter(x, y):

        if sheet is None:
            sheet = tosheet(x, y)
        label = int(aphexcode.tolabel(aphexcode.fromxy(x, y, sheet=sheet)))
        if label in _terrain[sheet]["level2hexes"]:
            return 2 * _levelincrement
        elif label in _terrain[sheet]["level1hexes"]:
            return 1 * _levelincrement
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


def iscity(x, y, sheet=None):
    """
    Returns whether the position is a city hex or a hex side of a city hex.
    """

    assert aphex.isvalid(x, y)

    if aphex.iscenter(x, y):

        if sheet is None:
            sheet = tosheet(x, y)
        label = int(aphexcode.tolabel(aphexcode.fromxy(x, y, sheet=sheet)))
        return label in _terrain[sheet]["cityhexes"]

    else:

        x0, y0, x1, y1 = aphex.sidetocenters(x, y)
        sheet0 = tosheet(x0, y0)
        sheet1 = tosheet(x1, y1)
        assert sheet0 != None or sheet1 != None
        if sheet0 == None:
            sheet0 = sheet1
        if sheet1 == None:
            sheet1 = sheet0
        return iscity(x0, y0, sheet=sheet0) or iscity(x1, y1, sheet=sheet1)


def crossesridgeline(x0, y0, x1, y1):

    # See https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

    class point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def onsegment(p, q, r):
        """
        Return true if q lines on the line segment pr, assuming p, q, and r are colinear.
        """

        return (
            (q.x <= max(p.x, r.x))
            and (q.x >= min(p.x, r.x))
            and (q.y <= max(p.y, r.y))
            and (q.y >= min(p.y, r.y))
        )

    def orientation(p, q, r):
        """
        Return the orientation of an ordered triplet of points (p, q, r),
        where 0 means colinear, 1 means clockwise, and -1 means anticlockwise.
        """
        v = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if v > 0:
            return +1
        elif v < 0:
            return -1
        else:
            return 0

    def intersect(p1, q1, p2, q2):
        """
        Return whether the line segment (p1, q1) intersects with the line segment (p2, q2).
        """

        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # General case
        if (o1 != o2) and (o3 != o4):
            return True

        # Special Cases

        # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
        if (o1 == 0) and onsegment(p1, p2, q1):
            return True

        # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
        if (o2 == 0) and onsegment(p1, q2, q1):
            return True

        # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
        if (o3 == 0) and onsegment(p2, p1, q2):
            return True

        # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
        if (o4 == 0) and onsegment(p2, q1, q2):
            return True

        # If none of the cases
        return False

    def crossesridgepath(p, q, sheet, ridgepath):
        i = 0
        while i < len(ridgepath) - 1:
            r = point(*toxy(sheet, *ridgepath[i + 0]))
            s = point(*toxy(sheet, *ridgepath[i + 1]))
            if intersect(p, q, r, s):
                return True
            i += 1
        return False

    p = point(x0, y0)
    q = point(x1, y1)
    for sheet in _sheetlist:
        for ridgepath in (
            _terrain[sheet]["level0ridgepaths"]
            + _terrain[sheet]["level1ridgepaths"]
            + _terrain[sheet]["level2ridgepaths"]
        ):
            if crossesridgepath(p, q, sheet, ridgepath):
                return True
    return False


################################################################################
