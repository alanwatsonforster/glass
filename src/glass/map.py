"""
The :mod:`glass.map` module contains functions to specify, draw, and query the
map.

The map is set up by calling :func:`.setupmap`. It is then drawn by calling
:func:`.startdrawmap`, then drawing individual elements by calling their
:meth:`draw` methods, and then by calling :func:`.enddrawmap`.

The map is automatically shown in a Python notebook. It can also be written to
files by specifying file types using :func:`setwritefiletypes`; by default PNG
files are written. The file names are of the form ``"map-XX.SUFFIX"`` in which
XX is the game turn padded if necessary to two character with a leading zero
(and 00 prior to the first game turn) and SUFFIX is the file suffix. Writing
files can be turned on and off by calling :func:`setwritefiles`.

Certain properties of the map can be queried by :func:`altitude`,
:func:`crossesridgeline`, :func:`iscity`, :func:`isonmap`, :func:`sheetorigin`,
:func:`tosheet`, and :func:`usingfirstgeneratuonsheets`.

For information on map styling, see :mod:`glass.mapstyle.`

Terrain
-------

The terrain in the maps is defined by JSON files in the glass/mapsheetdata/
directory (and can subsequently be modified by the map style). The file name
corresponds to the sheet name. Each file contains a single JSON object. The
members are:

- ``"base"``: This is either ``"land"`` for sheets based on land or ``"water"``
  for sheets based on water, and determines whether hexes that are not
  explicitly listed in ``"level0hexes"``, ``"level1hexes"``, or
  ``"level2hexes"`` are land or water.
- ``"center"``: The hex coordinates of the sheet center as a list [x,y].
- ``"cityhexes"``: A list of city hexes.
- ``"clearingpaths"``: A list road or trail clearing paths through forest.
- ``"dampaths"``: A list of dam paths (see sheet C2).
- ``"dockpaths"``: A list of dock paths (see sheet E).
- ``"foresthexes"``: A list of forest hexes.
- ``"generation"``: Either 1 or 2.
- ``"lakehexes"``: A list of lake hexes.
- ``"largebridgepaths"``: A list of large bridge paths (see sheets A2, B1, E, F,
  G, H, and J).
- ``"level0hexes"``: A list of level 0 land hexes.
- ``"level0ridgepaths"``: A list of level 0 ridge paths.
- ``"level1hexes"``: A list of level 1 land hexes.
- ``"level1ridgepaths"``: A list of level 1 ridge paths.
- ``"level2hexes"``: A list of level 2 land hexes.
- ``"level2ridgepaths"``: A list of level 2 ridge paths.
- ``"riverpaths"``: A list of river paths.
- ``"roadpaths"``: A list of road paths.
- ``"runwaypaths"``: A list of runway paths (see sheets A1, A2, E, G, H, and K).
- ``"seahexes"``: A list of sea hexes (see sheet E).
- ``"seapaths"``: A list of sea paths (see sheet E).
- ``"smallbridgepaths"``: A list of small bridge paths (see sheets B1, B2, C1,
  C2, E, G, H, and I).
- ``"taxiwaypaths"``: A list of taxiway paths (see sheet A1).
- ``"town1hexes"``: A list of town or village hexes for towns with 1 hex.
- ``"town2hexes"``: A list of town or village hexes for towns with 2 hexes.
- ``"town3hexes"``: A list of town or village hexes for towns with 3 hexes.
- ``"town4hexes"``: A list of town or village hexes for towns with 4 hexes.
- ``"town5hexes"``: A list of town or village hexes for towns with 5 or more
  hexes.
- ``"trailpaths"``: A list of trail paths (see sheets K, L, and N).
- ``"tunnelpaths"``: A list of tunnel paths (see sheet F).
- ``"wideriverpaths"``: A list of wide river paths (see sheets A1, A2, H, K, and
  N).
- ``"wideseapaths"``: A list of wide sea paths (see sheet E).

In lists of hexes, each hex is represented by its label as a string (e.g.,
``"1504"``).

In lists of paths, each path is represented by a list of points. Each point is a
list of three elements: a hex, an offset in x, and an offset in y. The hex is
represented by its label as a string (e.g., ``"1504"``). The offsets are floats.
The point is the position in hex space displaced from the hex center by the
offsets in x and y.

There are several blank maps in each generation that can be adapted to new
terrain.

Furthermore, adding new first-generation maps is just a case of creating a new
JSON file in the glass/mapsheetdata/ directory with a new unique name. This is
not the case for second-generation maps, as they have a defined relation between
hex label and map sheet.

Being on a Sheet
----------------

We say that the edge of a sheet is *internal* if it is adjacent to another
non-blank sheet in the map and is external otherwise.

We say a location is *on a sheet* if it is strictly within the boundaries of the
sheet, if it is on the right edge of the sheet if this is an internal edge, or
if it is on the bottom edge of the sheet if this is an internal edge. The sense
of right and bottom are in the normal orientation of the map, prior to any
requested rotation.

Being on the Map
----------------

We say that a position is *on the map* if it is strictly within the boundary of
the map. The boundary of the map is formed by the external edges of the sheets.

Note that a location on an external edge of a sheet or, equivalently, on the
boundary of the map, is not considered to be *on a sheet* or *on the map*.

API
---
"""

################################################################################

__all__ = [
    "setupmap",
    "setwritefiles",
    "setwritefiletypes",
    "startdrawmap",
    "enddrawmap",
    "usingfirstgenerationsheets",
    "isonmap",
    "isonsheet",
    "tosheet",
    "sheetorigin",
    "altitude",
    "iscity",
    "crossesridgeline",
]

################################################################################

import glass.azimuth
import glass.draw
import glass.hex
import glass.hex
import glass.hexcode
import glass.mapstyle

import json
import math
import os

################################################################################

_writefiles = True


def setwritefiles(flag):
    """
    Set the flag for writing map files.

    :param flag:
        If the flag argument is false, do not write map files. Otherwise, write the map files.
    """
    global _writefiles
    _writefiles = flag


_writefiletypes = ["png"]


def setwritefiletypes(suffixlist):
    """
    Set the types of the map files.

    :param suffixlist:
        The value argument must be a list of strings of the suffixes of supported map file types.
        Supported suffixes include ``"png"`` and ``"pdf"``.
    """
    global _writefiletypes
    _writefiletypes = suffixlist


################################################################################


_terrain = {}

_generation = None

_dxsheet = 20
_dysheet = 15

_sheetgrid = []
_loweredgeisinternal = {}
_rightedgeisinternal = {}
_sheetlist = []
_nxsheetgrid = 0
_nysheetgrid = 0

_borderxmin, _borderymin, _borderxmax, _borderymax = None, None, None, None
"""
The `_borderxmin`, `_borderymin`, `_borderxmax`, and `_borderymax` variables
give the limits of the border in hex coordinates.
"""

_dotsperhex = None

_saved = False

_rotation = 0

"""
Whether to outline the sheets.
"""
_outlinesheets = False

ridgewidth = 14 / 72
roadwidth = 5 / 72
dockwidth = 5 / 72
clearingwidth = 20 / 72
bridgeinnerwidth = roadwidth + 8 / 72
bridgeouterwidth = bridgeinnerwidth + 6 / 72
runwaywidth = 10 / 72
taxiwaywidth = 7 / 72
damwidth = 14 / 72
hexwidth = "thin"
megahexwidth = 7 / 72

roadoutlinewidth = 2 / 72
dockoutlinewidth = 2 / 72
waterourlinewidth = 2 / 72

tunnelinnerwidth = roadwidth + 8 / 72
tunnelouterwidth = tunnelinnerwidth + 6 / 72

narrowriverwidth = 9 / 72
defaultriverwidth = 14 / 72
wideriverwidth = 35 / 72

borderwidth = 0.25

blanksheets = ["", "-", "--"]


def usingfirstgenerationsheets():
    """
    Return whether the is using first-generation map sheets.

    :returns: ``True`` if the map is using first-generation map sheets, otherwise ``False``.

    """
    return _generation == 1


def setupmap(
    sheets,
    invertedsheets=[],
    dotsperhex=80,
    style="airstrike",
    leveloffset=0,
    levelincrement=1,
    rotation=0,
    outlinesheets=False,
    sheetset="default",
):
    """
    Set up the map.

    :param sheets: The ``sheets`` argument must be a 2D array of sheet names.
        The sheets are ordered top-to-bottom and left-to-right. All of the rows
        must be the same length. No sheet name can be used more than once and
        all sheets must be from the same generation.

        The first-generation sheet names are: ``"A"``, ``"B"``, ``"C"``, ...,
        ``"Z"``.

        The second-generation sheet names are: ``"A1"``, ``"A2"``, ``"A3"``,
        ..., ``"A6"``, ``"B1"``, ..., ``"B6"``, ``"C1"``, ..., ``"C6"``,
        ``"D1"``, ..., ``"D6"``.

    :param invertedsheets: A list of strings naming sheets that are inverted in
        the map.

    :param dotsperhex: The ``dotsperhex`` argument must be an integer. It
        specifies the resolution of pixelated output files in dots per hex (or
        more precisely dots between hex centers).

    :param style: The ``style`` argument must be a string corresponding to a
        style.

        It can be one of the original styles (``"airstrike"`` or
        ``"airsuperiority"``), one of the base styles (``"water"``,
        ``"temperate"``, ``"temperateforest"``, ``"tundra"``,
        ``"borealforest"``, ``"tropical"``, ``"tropicalforest"``, ``"arid"``, or
        ``"desert"``), or one of the base styles with an optional prefix
        (``"snowy"`` or ``"frozen"``) and an optional suffix (``"hills"``,
        ``"plain"``, or ``"islands"``).

    :param leveloffset:
    :param levelincrement: The ``leveloffset`` and ``levelincrement`` arguments
        define the mapping from terrain levels to altitude levels. The altitude
        corresponding to a terrain level is ``leveloffset`` plus the terrain
        level times the ``levelincrement``. For example, if ``leveloffset`` is 3
        and ``levelincrement`` is 2, then terrain levels 0, 1, and 2 correspond
        to altitude levels 3, 5, and 7.

    :param rotation: The ``rotation`` parameter define the rotation in degrees
        of the map with respect to the normal orientation. It must be an integer
        and a multiple of 90. Positive values correspond to counterclockwise
        rotations.
    """

    global _dotsperhex
    _dotsperhex = dotsperhex

    global _outlinesheets
    _outlinesheets = outlinesheets

    global _rotation
    _rotation = rotation

    global _leveloffset, _levelincrement
    _leveloffset = leveloffset
    _levelincrement = levelincrement

    global _style
    _style = glass.mapstyle.getstyle(style)
    if _style == None:
        raise RuntimeError("invalid style %r." % style)

    # Check the sheet grid has the right structure.
    global _sheetgrid
    _sheetgrid = sheets
    if not isinstance(_sheetgrid, list):
        raise RuntimeError("the sheet grid is not a list of lists.")
    for row in _sheetgrid:
        if not isinstance(row, list):
            raise RuntimeError("the sheet grid is not a list of lists.")
        if len(row) != len(_sheetgrid[0]):
            raise RuntimeError("the sheet grid is not rectangular.")

    # The sheet grid argument follows visual layout, so we need to flip it
    # vertically so that the lower-left sheet has indices (0,0).
    _sheetgrid = list(reversed(_sheetgrid))

    global _nysheetgrid
    global _nxsheetgrid
    _nysheetgrid = len(_sheetgrid)
    _nxsheetgrid = len(_sheetgrid[0])

    global _generation
    _generation = None
    global _sheetlist
    _sheetlist = []
    global _loweredgeisinternal, _rightedgeisinternal
    _loweredgeisinternal = {}
    _rightedgeisinternal = {}
    for iy in range(0, _nysheetgrid):
        for ix in range(0, _nxsheetgrid):
            fullsheet = _sheetgrid[iy][ix]
            if fullsheet not in blanksheets:
                sheet = fullsheet.split("/")[-1]
                _sheetgrid[iy][ix] = sheet
                if sheet in _sheetlist:
                    raise RuntimeError("sheet %s is used more than once." % sheet)
                _sheetlist.append(sheet)
                _loweredgeisinternal |= {sheet: iy != 0 and _sheetgrid[iy - 1][ix] not in blanksheets}
                _rightedgeisinternal |= {sheet: ix != _nxsheetgrid - 1 and _sheetgrid[iy][ix + 1] not in blanksheets}
                try:
                    terrain = _loadterrain(fullsheet)
                except:
                    raise RuntimeError("invalid sheet %s." % fullsheet)
                if _generation is None:
                    _generation = terrain["generation"]
                elif _generation != terrain["generation"]:
                    raise RuntimeError("invalid sheet %s." % fullsheet)
                if sheet in invertedsheets:
                    terrain = _invertterrain(terrain)
                terrain = glass.mapstyle.styleterrain(terrain, _style)
                terrain = _prepareterrain(terrain)
                _terrain[sheet] = terrain

    global _dxsheet, _dysheet
    if _generation == 1:
        _dxsheet = 20
        _dysheet = 25
    else:
        _dxsheet = 20
        _dysheet = 15

    # Determine the limits of the map grid.
    _mapxmin = 0.33
    _mapxmax = _dxsheet * _nxsheetgrid - 0.33
    _mapymin = 0
    _mapymax = _dysheet * _nysheetgrid

    # Determine the limits of the border taking into account that the border
    # width is constant in physical coordinates.
    global _borderxmin, _borderymin, _borderxmax, _borderymax
    _borderxmin, _borderymin = glass.hex.tophysicalxy(_mapxmin, _mapymin)
    _borderxmax, _borderymax = glass.hex.tophysicalxy(_mapxmax, _mapymax)
    _borderxmin -= borderwidth
    _borderymin -= borderwidth
    _borderxmax += borderwidth
    _borderymax += borderwidth
    _borderxmin, _borderymin = glass.hex.fromphysicalxy(_borderxmin, _borderymin)
    _borderxmax, _borderymax = glass.hex.fromphysicalxy(_borderxmax, _borderymax)

    global _saved
    _saved = False


################################################################################


def _loadterrain(fullsheet):
    """
    Load a terrain object from a file and return it.

    :param fullsheet: The fullsheet parameter is the full sheet name, including
        any subdirectories. It must be a string and correspond to a valid sheet.

    :returns: The terrain object for the sheet.
    """
    filename = os.path.join(os.path.dirname(__file__), "mapsheetdata", fullsheet + ".json")
    with open(filename, "r", encoding="utf-8") as f:
        terrain = json.load(f)
    return terrain


def _invertterrain(terrain):
    """ "
    Return an inverted terrain object.

    :param terrain: The terrain parameter must be a terrain object.

    :returns: An inverted copy of the terrain parameter.
    """

    xcenter = terrain["center"][0]
    ycenter = terrain["center"][1]
    generation = terrain["generation"]

    def inverthexes(oldhexes):
        return list(inverthex(oldhex) for oldhex in oldhexes)

    def inverthex(oldhex):
        oldx = int(oldhex) // 100
        oldy = int(oldhex) % 100
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
        return "%04d" % newhex

    def invertpaths(oldpaths):
        return list(invertpath(oldpath) for oldpath in oldpaths)

    def invertpath(oldpath):
        return list(invertpathpoint(oldxy) for oldxy in oldpath)

    def invertpathpoint(oldpathpoint):
        oldhex = oldpathpoint[0]
        olddx = oldpathpoint[1]
        olddy = oldpathpoint[2]
        newhex = inverthex(oldhex)
        newdx = -olddx
        newdy = -olddy
        return [newhex, newdx, newdy]

    newterrain = {}
    for key in terrain.keys():
        if key[-5:] == "hexes":
            newterrain[key] = inverthexes(terrain[key])
        elif key[-5:] == "paths":
            newterrain[key] = invertpaths(terrain[key])
        else:
            newterrain[key] = terrain[key]
    return newterrain


def _prepareterrain(terrain):
    """
    Return a terrain object prepared for making the map.

    :param terrain: A styled terrain object.

    :returns: A terrain object prepared for making the map. Specifically, with
        the townhexes values split according to their terrain level.
    """

    newterrain = terrain.copy()

    # Add the town hexes according to their terrain level.
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
    newterrain["level0townhexes"] = level0townhexes
    newterrain["level1townhexes"] = level1townhexes
    newterrain["level2townhexes"] = level2townhexes

    return newterrain


################################################################################


def startdrawmap(
    show=False,
    xmin=None,
    ymin=None,
    xmax=None,
    ymax=None,
    sheets=None,
    compactstacks=True,
):
    """
    Start to draw the map.

    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax: The ``xmin``, ``ymin``, ``xmax``, and ``xmax`` arguments can determine the region of the map that will be drawn. If any is not ``None``, all must be numbers, they must specify two positions that are on the map, and the value of the ``sheets`` argument must be ``None``.
    :param sheets: The ``sheets`` argument can determine the region of the map that will be drawn. If it is not ``None``, it must be a list of sheets that are part of the map and the values of the ``xmin``, ``ymin``, ``xmax``, and ``xmax`` argument must be ``None``.
    :param compactstacks: The ``compactstacks`` argument determines whether stacks of ground units are drawn in the compact or spread style. If it is true, they are drawn in the compact style, otherwise they are drawn in the spread style.

    :notes: If the region is not specified either by the ``xmin``, ``ymin``, ``xmax``, and ``xmax`` arguments or by the ``sheets`` argument, the whole map is drawn.

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
    if _style["riverwidth"] == "narrow":
        riverwidth = narrowriverwidth
    else:
        riverwidth = defaultriverwidth

    def drawhexes(sheet, labels, **kwargs):
        for label in labels:
            x, y = glass.hexcode.toxy("%s-%s" % (sheet, label))
            if isnearcanvas(x, y):
                glass.draw.drawhex(x, y, **kwargs)

    def drawpaths(sheet, paths, **kwargs):
        for path in paths:
            xy = [pathpointtoxy(sheet, pathpoint) for pathpoint in path]
            # Do not use the naive isnearcanvas optimization used above in
            # drawhexes, as paths can cross the canvas without their endpoints
            # being near to it.
            x = [xy[0] for xy in xy]
            y = [xy[1] for xy in xy]
            glass.draw.glass.draw.drawlines(x, y, **kwargs)

    if xmin is not None and xmax is not None and ymin is not None and ymax is not None:

        canvasxmin = max(_borderxmin, xmin)
        canvasymin = max(_borderymin, ymin)
        canvasxmax = min(_borderxmax, xmax)
        canvasymax = min(_borderymax, ymax)

    elif sheets is not None:

        canvasxmin = _borderxmax
        canvasymin = _borderymax
        canvasxmax = _borderxmin
        canvasymax = _borderymin
        for sheet in sheets:
            sheetxmin, sheetymin, sheetxmax, sheetymax = sheetlimits(sheet)
            canvasxmin = min(canvasxmin, sheetxmin)
            canvasymin = min(canvasymin, sheetymin)
            canvasxmax = max(canvasxmax, sheetxmax)
            canvasymax = max(canvasymax, sheetymax)

    else:

        canvasxmin = _borderxmin
        canvasymin = _borderymin
        canvasxmax = _borderxmax
        canvasymax = _borderymax

    fullmap = (
        canvasxmin == _borderxmin
        and canvasymin == _borderymin
        and canvasxmax == _borderxmax
        and canvasymax == _borderymax
    )

    global _saved
    if fullmap and _saved:
        glass.draw.restorecanvas()
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

    glass.draw.startcanvas(
        canvasxmin,
        canvasymin,
        canvasxmax,
        canvasymax,
        dotsperhex=_dotsperhex,
        rotation=_rotation,
    )

    if all(_terrain[sheet]["base"] == "water" for sheet in _sheetlist):
        bordercolor = watercolor
    elif all(_terrain[sheet]["base"] == "land" for sheet in _sheetlist):
        bordercolor = level0color
    else:
        bordercolor = hexcolor

    glass.draw.drawrectangle(
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
        glass.draw.drawrectangle(
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
            glass.draw.drawrectangle(
                xmin,
                ymin,
                xmax,
                ymax,
                hatch="forest",
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
                hatch="forest",
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
            hatch="town",
        )

        drawhexes(
            sheet,
            _terrain[sheet]["cityhexes"],
            linewidth=0,
            fillcolor=urbancolor,
            linecolor=urbanoutlinecolor,
            hatch="city",
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
                glass.draw.drawhex(
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

    glass.draw.drawborder(
        _borderxmin, _borderymin, _borderxmax, _borderymax, borderwidth, fillcolor=bordercolor
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
                # Draw the hex if it is on the map, is near the canvas, and
                # either its center or the center of its upper left edge are on
                # this sheet.
                if (
                    isonmap(x, y)
                    and isnearcanvas(x, y)
                    and (isonsheet(sheet, x, y) or isonsheet(sheet, x - 0.5, y + 0.25))
                ):
                    glass.draw.drawhex(
                        x,
                        y,
                        linecolor=hexcolor,
                        alpha=hexalpha,
                        linewidth=hexwidth,
                    )
                    label = glass.hexcode.tolabel(glass.hexcode.fromxy(x, y))
                    glass.draw.drawhexlabel(x, y, label, textcolor=hexcolor, alpha=hexalpha)

    # Label the sheets.

    # Draw the compass rose in the lower left corner of the canvas.
    # Find the first column whose center is no closer than 0.25 to the left
    # edge. Then find the first hex in that column whose center is no closer
    # than 0.5 to the lower edge.
    compassx = math.ceil(canvasxmin + 0.25)
    if compassx % 2 == 1:
        compassy = math.ceil(canvasymin) + 0.5
    else:
        compassy = math.ceil(canvasymin + 0.5)

    for sheet in sheetsnearcanvas():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        if usingfirstgenerationsheets():
            dx = 1.0
            dy = 24.5
        else:
            dx = 1.0
            dy = 0.5
        if isonmap(xmin + dx, ymin + dy):
            glass.draw.drawsheetlabel(xmin + dx, ymin + dy, sheet, textcolor=labelcolor)
            # Move the compass one hex up if it coincides with a sheet label.
            if xmin + dx == compassx and ymin + dy == compassy:
                compassy += 1.0

    glass.draw.drawcompass(
        compassx,
        compassy,
        glass.azimuth.tofacing("N"),
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
                glass.draw.drawrectangle(
                    xmin - 0.33,
                    ymin,
                    xmax + 0.33,
                    ymax,
                    linecolor=None,
                    fillcolor=level0color,
                )


    # Draw sheet borders.

    if _outlinesheets:
        for iy in range(0, _nysheetgrid):
            for ix in range(0, _nxsheetgrid):
                xmin = ix * _dxsheet
                xmax = xmin + _dxsheet
                ymin = iy * _dysheet
                ymax = ymin + _dysheet
                glass.draw.drawrectangle(
                    xmin,
                    ymin,
                    xmax,
                    ymax,
                    linecolor=hexcolor,
                    fillcolor=None,
                )

    glass.draw.setcompactstacks(compactstacks)

    if fullmap and _writefiles:
        glass.draw.savecanvas()
        _saved = True


def enddrawmap(turn, writefiles=True):
    if _writefiles and writefiles:
        for filetype in _writefiletypes:
            glass.draw.writecanvastofile("map-%02d.%s" % (turn, filetype))
    glass.draw.showcanvas()


def sheetorigin(sheet):
    """
    Return the hex coordinates (x, y) of the lower left corner of the specified
    sheet.

    :param sheet: The ``sheet`` argument specifies the sheet name. It must be a
        string and must be part of the map.
    :returns:  The hex coordinates (x, y) of the lower left corner of the
        specified sheet as two values.
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
    Return whether the position is on the sheet.

    :param sheet: The ``sheet`` argument specifies the sheet name. It must be a
        string and must be part of the map.
    :param x:
    :param y: The ``x`` and ``y`` arguments specify the position. They must form
        a valid hex position.
    :returns: ``True`` if the position is on the sheet, otherwise ``False``.

    :note:

        The edge of a sheet is *internal* if it is adjacent to another non-blank
        sheet in the map and is *external* otherwise. A position is on a sheet
        if it is strictly within the boundaries of the sheet if it is on the
        rightmost edge of the sheet if this is an inner edge, or if it is on the
        bottom edge of the sheet if this is an inner edge. These directions are
        considered with the map in the normal orientation before any requested
        rotation.

    """

    assert sheet in sheets()

    xmin, ymin, xmax, ymax = sheetlimits(sheet)

    if _rightedgeisinternal[sheet] and _loweredgeisinternal[sheet]:
        return xmin < x and x <= xmax and ymin <= y and y < ymax
    elif _rightedgeisinternal[sheet]:
        return xmin < x and x <= xmax and ymin < y and y < ymax
    elif _loweredgeisinternal[sheet]:
        return xmin < x and x < xmax and ymin <= y and y < ymax
    else:
        return xmin < x and x < xmax and ymin < y and y < ymax


def tosheet(x, y):
    """
    Return the name of the sheet the position is on or ``None`` if the position is not on any sheet.


    :param x:
    :param y: The ``x`` and ``y`` arguments specify the position. They must form
        a valid hex position.
    :returns: The name of sheet the position is on or ``None`` if the position is not on any sheet.

    :note:

        See :func:`isonsheet` for a precise definition of being “on a sheet.”
    """

    for sheet in sheets():
        if isonsheet(sheet, x, y):
            return sheet
    return None


def isonmap(x, y):
    """
    Return whether the position is on the map.


    :param x:
    :param y: The ``x`` and ``y`` arguments specify the position. They must form
        a valid hex position.
    :returns: ``True`` if the position is on the map, otherwise ``False``.

    """

    return tosheet(x, y) != None


def pathpointtoxy(sheet, pathpoint):
    if isinstance(pathpoint, str):
        hexcode = pathpoint
        dx = 0
        dy = 0
    else:
        hexcode = pathpoint[0]
        dx = pathpoint[1]
        dy = pathpoint[2]
    x0, y0 = glass.hexcode.toxy("%s-%s" % (sheet, hexcode))
    return x0 + dx, y0 + dy


def altitude(x, y, sheet=None):
    """
    Return the altitude at the position.

    :param x:
    :param y: The ``x`` and ``y`` arguments specify the position. They must form
        a valid hex position.
    :returns: The altitude at the specified position.

    :notes:

        Each hex is at terrain level 0, 1, or 2. The altitude is a hex is value
        of ``leveloffset`` plus its terrain level times the value of
        ``levelincrement``. The altitude of a hex side is higher of the
        altitudes of the two adjacent hexes.

        The values of ``leveloffset`` and ``levelincrement`` are set by the
        ``setupmap`` function.
    """

    assert glass.hex.isvalid(x, y)

    if glass.hex.ishex(x, y):

        if sheet is None:
            sheet = tosheet(x, y)
        label = glass.hexcode.tolabel(glass.hexcode.fromxy(x, y, sheet=sheet))
        if label in _terrain[sheet]["level2hexes"]:
            return _leveloffset + 2 * _levelincrement
        elif label in _terrain[sheet]["level1hexes"]:
            return _leveloffset + 1 * _levelincrement
        else:
            return _leveloffset

    else:

        x0, y0, x1, y1 = glass.hex.hexsidetohexes(x, y)
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
    Return whether the position is a city hex or a hex side of a city hex.


    :param x:
    :param y: The ``x`` and ``y`` arguments specify the position. They must form
        a valid hex position.
    :returns: ``True`` if the position is a city hex or a hex side of a city
        hex, otherwise ``False``.

    """

    assert glass.hex.isvalid(x, y)

    if glass.hex.ishex(x, y):

        if sheet is None:
            sheet = tosheet(x, y)
        label = glass.hexcode.tolabel(glass.hexcode.fromxy(x, y, sheet=sheet))
        return label in _terrain[sheet]["cityhexes"]

    else:

        x0, y0, x1, y1 = glass.hex.hexsidetohexes(x, y)
        sheet0 = tosheet(x0, y0)
        sheet1 = tosheet(x1, y1)
        assert sheet0 != None or sheet1 != None
        if sheet0 == None:
            sheet0 = sheet1
        if sheet1 == None:
            sheet1 = sheet0
        return iscity(x0, y0, sheet=sheet0) or iscity(x1, y1, sheet=sheet1)


def crossesridgeline(x0, y0, x1, y1):
    """
    Return whether a line segment crosses a ridgeline on the map.

    :param x0:
    :param y0:
    :param x1:
    :param y1: The ``x0``, ``y0``, ``x1``, and ``y1`` arguments define the line segment from (``x0``, ``y0``) to (``x1``, ``y1``).

    :return: ``True`` if the line segment crosses a ridge line on the map, otherwise ``False``.
    """

    # This code uses the algorithm described here:
    #
    #   https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

    class point:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def onsegment(p, q, r):
        """
        Return true if q lies on the line segment pr, assuming p, q, and r are colinear.
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
        where 0 means colinear, +1 means clockwise, and -1 means anticlockwise.
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

        # Find the 4 orientations required for the general and special cases
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
        """
        Return whether the line segment (p, q) intersects the ridgepath.
        """
        i = 0
        while i < len(ridgepath) - 1:
            r = point(*pathpointtoxy(sheet, ridgepath[i + 0]))
            s = point(*pathpointtoxy(sheet, ridgepath[i + 1]))
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
