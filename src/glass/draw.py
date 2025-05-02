"""
The :mod:`glass.draw` module has procedures for drawing the map, aircraft,
missiles, ground units, and other markers.

Other Keyword Parameters
------------------------

Many of the drawing functions have additional keyword parameters from this list:

* ``linewidth``:
    The ``linewidth`` argument must be ``None``, number giving the line width in
    hexes or one of the strings ``"thin"``, ``"normal"``, or ``"thick"``. If it
    is ``None``, the line is not drawn.
* ``linecolor``:
* ``fillcolor``:
    The ``linecolor`` and ``fillcolor`` arguments must be ``None``, a tuple or
    list of three numbers, or a string naming a color. If it is ``None``, the
    line is not drawn or the region not filled. The numbers in the tuple or list
    are the red, green, and blue components from 0 to 1. Named colors are:
    ``"white"``, ``"gray90"``, ``"gray80"``, ``"gray70"``, ``"gray60"``,
    ``"gray50"``, ``"gray40"``, ``"gray30"``, ``"gray20"``, ``"gray10"``,
    ``"black"``, ``"grey90"``, ``"grey80"``, ``"grey70"``, ``"grey60"``,
    ``"grey50"``, ``"grey40"``, ``"grey30"``, ``"grey20"``, ``"grey10"``,
    ``"aluminum"``, ``"aluminium"``, ``"unpainted"``, ``"darkblue"``,
    ``"skyblue"``, ``"green"``, ``"olivedrab"``, ``"lightgreen"``,
    ``"lightolivedrab"``, ``"tan"``, ``"darktan"``, ``"sand"``, ``"darkgray"``,
    ``"mediumgray"``, ``"mediumgrey"``, ``"lightgray"``, ``"lightgrey"``,
    ``"slategray"``, ``"slategrey"``, ``"natoblue"``, ``"natored"``,
    ``"natogreen"``, ``"natoyellow"``, ``"natofriendly"``, ``"natohostile"``,
    ``"natoneutral"``, ``"natounknown"``, ``"iafblue"``, ``"panarabred"``, and
    ``"panarabgreen"``. Note that both American and British versions of "gray"
    and "aluminum" are present.
* ``linestyle``:
    The ``linestyle`` argument must to one of the strings ``"solid"``,
    ``"dashed"``, or ``"dotted"``.
* ``joinstyle``:
    The default is "miter".
* ``capstyle``:
    The default is "butt".
* ``hatch``:
    The ``hatch`` argument must be ``None`` or one of the strings ``"city"``,
    ``"town"``, or ``"forest"``. If it is ``None``, the region is not hatched.
* ``alpha``:
    The ``alpha`` argument must be a number between 0 and 1. It set the
    transparency of whatever is drawn.
* ``zorder``:
    The ``zorder`` argument must be a number between 0 and 1. It set the zorder
    of whatever is drawn.

zorder
------

The zorder parameter is important to give a correct sense of altitude. The following values are used:

* 0: map, arcs, hex ground units
* 0.1: surface element path lines
* 0.1 to 0.4: ground units
* 0.5: ships, surface element path dots
* 0.9: air element path lines
* altitude + 0.9: air element path dots
* altitude + 1.0: aircraft
* altitude + 1.1: missiles, bombs
* altitude + 1.5:  barrage fire, blast zones
* altitude + 3.5:  plotted fire
* 100: lines of sight

"""

import math

import pickle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

import glass.hex

################################################################################

plt.rcParams.update({"figure.max_open_warning": 0})

################################################################################

"""
Drawing is largely performed in the canvas coordinate system. This is equivalent
to the physical coodinate system (defined in :mod:`glass.hex`) rotated about the
origin by :data:`_canvasrotation`, with a positive rotation corresponding to a
counterclockwise rotation from the physical to coordinate system. Thus, a value
of 90 puts the “top” of the map sheets on the left and a value of -90 puts it on
the right.
"""

_canvasrotation = 0
"""
The value of ``_canvasrotation`` determines the rotation of the canvas
coordinate frame from the hex and physical coordinate frames, with a positive
rotation corresponding to a counterclockwise rotation. It must be an integer
value and a multiple of 90.
"""


def _tocanvasxy(x, y):
    """
    Return the canvas position corresponding to a hex position.

    :param x:
    :param y: The `x` and `y` parameters are the coordinates of the hex
        position.

    :return: The `x` and `y` coordinates of the canvas position corresponding to
        the hex position.
    """
    x, y = glass.hex.tophysicalxy(x, y)
    if _canvasrotation == 0:
        return x, y
    elif _canvasrotation == 180:
        return -x, -y
    elif _canvasrotation == 90:
        return -y, x
    elif _canvasrotation == 270:
        return y, -x


def _tocanvasfacing(facing):
    """
    Return the canvas facing corresponding to a hex facing.

    :param facing: The hex facing.

    :return: The canvas facing corresponding to the hex facing.
    """
    return facing + _canvasrotation


_canvasxmin = None
_canvasymin = None
_canvasxmax = None
_canvasymax = None
"""
The values of ``_canvasxmin``, ``_canvasymin``, ``_canvasxmax``, and ``_canvasxmax``
are the limits in canvas coordinates of the canvas currently being drawn.
"""

################################################################################


_pointsperhex = 72

_fig = None
_ax = None


def startcanvas(xmin, ymin, xmax, ymax, rotation=0, dotsperhex=100):
    """
    Start a new canvas.

    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
        The ``xmin``, ``ymin``, ``xmax``, and ``xmax`` arguments are the limits
        in hex coordinates of the canvas to be drawn. They must be numbers.
    :param rotation:
        The ``rotation`` argument is the rotation of the canvas in degrees, with
        a positive rotation corresponding to a counterclockwise rotation. It
        must be an integer value and a multiple of 90.
    :param dotsperhex:
        The ``dotsperhex`` argument must be an integer. It specifies the
        resolution of pixelated output files in dots per hex (or more precisely
        dots between hex centers).
    """

    global _fig, _ax

    global _canvasrotation
    assert isinstance(rotation, int) and rotation % 360 in [0, 90, 180, 270]
    _canvasrotation = rotation % 360

    global _canvasxmin, _canvasxmax, _canvasymin, _canvasymax
    _canvasxmin, _canvasymin = _tocanvasxy(xmin, ymin)
    _canvasxmax, _canvasymax = _tocanvasxy(xmax, ymax)
    _canvasxmin, _canvasxmax = min(_canvasxmin, _canvasxmax), max(
        _canvasxmin, _canvasxmax
    )
    _canvasymin, _canvasymax = min(_canvasymin, _canvasymax), max(
        _canvasymin, _canvasymax
    )

    # Set the canvas size and resolution. The figsize argument below implicitly
    # set a scale of 1 hex = 1 inch = 72 points.
    _fig = plt.figure(
        figsize=[abs(_canvasxmax - _canvasxmin), abs(_canvasymax - _canvasymin)],
        frameon=False,
        dpi=dotsperhex,
    )

    # Set the coordinate system.
    plt.axis("off")
    plt.xlim(_canvasxmin, _canvasxmax)
    plt.ylim(_canvasymin, _canvasymax)
    _ax = plt.gca()
    _ax.set_position([0, 0, 1, 1])

    # Draw a plain white background.
    _ax.add_artist(
        patches.Polygon(
            [
                [_canvasxmin, _canvasymin],
                [_canvasxmin, _canvasymax],
                [_canvasxmax, _canvasymax],
                [_canvasxmax, _canvasymin],
            ],
            edgecolor=None,
            facecolor="white",
            fill=True,
            linewidth=0,
            zorder=0,
        )
    )


def savecanvas():
    """
    Save the current canvas.

    Save the current canvas in the file ``glass.pickle`` in the current
    directory.

    Saving and restoring canvases can be quicker than starting anew each time,
    especially for large canvases.
    """
    pickle.dump(_fig, open("glass.pickle", "wb"))


def restorecanvas():
    """
    Restore a previously saved canvas.

    Restore the current canvas from the file ``glass.pickle`` in the current
    directory.
    """
    global _fig, _ax
    _fig = pickle.load(open("glass.pickle", "rb"))
    _ax = plt.gca()


def showcanvas():
    """
    Show the current canvas in the current Jupyter or iPython notebook.
    """
    # See https://github.com/alanwatsonforster/glass/issues/204
    #_fig.show()
    return


def writecanvastofile(filename):
    """
    Write the current canvas to a file.

    :param filename: The ``filename`` argument names the file to be written. Its
        type is determined by the suffix. Supported suffixes include ``".png"``
        and `".pdf"``.
    """
    _fig.savefig(filename)


################################################################################


def drawhex(x, y, size=1, facing=0, **kwargs):
    """
    Draw a hex.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the center of the hex in hex
        coordinates.
    :param size: The ``size`` argument gives the inscribed diameter in physical coordinates.
    :param facing:
        The ``facing`` argument gives the facing of the hex in degrees. The
        default is 0, which draw the hex with two sides parallel to the x-axis.
    :return: ``None``
    """
    _drawhexincanvas(
        *_tocanvasxy(x, y), size=size, facing=_tocanvasfacing(facing), **kwargs
    )
    return


def drawcircle(x, y, size=1, **kwargs):
    """
    Draw a circle.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the center of the circle in hex
        coordinates.
    :param size: The ``size`` argument gives the diameter in physical coordinates.
    :return: ``None``
    """
    _drawcircleincanvas(*_tocanvasxy(x, y), **kwargs)
    return


def drawhexlabel(x, y, label, dy=0.35, size="small", textcolor="lightgrey", **kwargs):
    """
    Draw a hex label.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the center of the hex in hex
        coordinates.
    :param label:
        The ``label`` argument gives the label text as a string.
    :param dy:
        The ``dy`` argument gives the offset in y between the center of the hex
        and the label in physical coordinates. It defaults to 0.35.
    :param size: The ``size`` argument gives the size of the text in points. It
        defaults to "small".
    :param textcolor: The ``textcolor`` argument gives the color of the text. It
        defaults to "lightgrey"
    :return: ``None``
    """
    drawtext(
        x, y, label, facing=90, dx=0, dy=dy, size=size, textcolor=textcolor, **kwargs
    )
    return


def drawsheetlabel(x, y, label, dy=-0.05, size="HUGE", textcolor="lightgrey", **kwargs):
    """
    Draw a sheet label.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the center of the hex in hex
        coordinates.
    :param label:
        The ``label`` argument gives the label text as a string.
    :param dy:
        The ``dy`` argument gives the offset in y between the center of the hex
        and the label in physical coordinates. It defaults to -0.05.
    :param size: The ``size`` argument gives the size of the text in points. It
        defaults to "HUGE".
    :param textcolor: The ``textcolor`` argument gives the color of the text. It
        defaults to "lightgrey"
    :return: ``None``
    """
    drawtext(
        x, y, label, facing=90, dx=0, dy=dy, size=size, textcolor=textcolor, **kwargs
    )
    return


def drawdot(x, y, size=1, dx=0, dy=0, facing=0, **kwargs):
    """
    Draw a dot.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the center of the dot in hex
        coordinates.
    :param size: The ``size`` argument gives the diameter in physical
        coordinates.
    :param dx:
    :param dy:
    :param facing:
        The ``dx``, ``dy``, and ``facing`` arguments specify an offset of the
        center of the dot in physical coordinates from the position
        (``x``, ``y``). The axis for the offset are rotated by ``facing`` in
        degrees. The defaults for the offsets and facing are 0.
    :return: ``None``
    """
    _drawdotincanvas(
        *_tocanvasxy(x, y),
        size=size,
        dx=dx,
        dy=dy,
        facing=_tocanvasfacing(facing),
        **kwargs,
    )
    return


def drawlines(x, y, **kwargs):
    """
    Draw continuous straight lines.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the coordinates of the lines in hex coordinates.
    :return: ``None``
    """
    xy = [_tocanvasxy(xy[0], xy[1]) for xy in zip(x, y)]
    x = [xy[0] for xy in xy]
    y = [xy[1] for xy in xy]
    _drawlinesincanvas(x, y, **kwargs)
    return


def drawarrow(x, y, size, facing, dx=0, dy=0, **kwargs):
    """
    Draw an arrow.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the coordinates of the center of the
        arrow in hex coordinates.
    :param size:
        The ``size`` argument gives the length of the arrow in physical
        coordinates.
    :param facing:
    :param dx:
    :param dy:
        The ``dx``, ``dy``, and ``facing`` arguments specify an offset of the
        center of the arrow in physical coordinates from the position (``x``,
        ``y``). The axis for the offset and the direction of the arrow are
        rotated by ``facing`` in degrees. The defaults for the offsets are 0.
    :return: ``None``
    """
    _drawarrowincanvas(
        *_tocanvasxy(x, y), size, _tocanvasfacing(facing), dx, dy, **kwargs
    )


def drawdart(x, y, size, facing, dx=0, dy=0, **kwargs):
    """
    Draw a dart (an arrow head).

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the coordinates of the center of the
        dart in hex coordinates.
    :param size:
        The ``size`` argument gives the length of the dart in physical
        coordinates.
    :param facing:
    :param dx:
    :param dy:
        The ``dx``, ``dy``, and ``facing`` arguments specify an offset of the
        center of the dart in physical coordinates from the position (``x``,
        ``y``). The axis for the offset and the direction of the dark are
        rotated by ``facing`` in degrees. The defaults for the offsets are 0.
    :return: ``None``
    """
    _drawdartincanvas(
        *_tocanvasxy(x, y),
        size=size,
        facing=_tocanvasfacing(facing),
        dx=dx,
        dy=dy,
        **kwargs,
    )


def drawtext(x, y, text, facing, dx=0, dy=0, **kwargs):
    """
    Draw a text.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the coordinates of the center of the
        dart in hex coordinates.
    :param text:
        The ``text`` argument is a strong giving the text to be written.
    :param facing:
    :param dx:
    :param dy:
        The ``dx``, ``dy``, and ``facing`` arguments specify an offset of the
        text in physical coordinates from the position (``x``,
        ``y``). The axis for the offset and text are
        rotated by ``facing`` in degrees. The defaults for the offsets are 0.
    :return: ``None``
    """
    _drawtextincanvas(
        *_tocanvasxy(x, y), text, _tocanvasfacing(facing), dx, dy, **kwargs
    )


def drawpolygon(x, y, **kwargs):
    """
    Draw a polygon.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the coordinates of the vertices of
        the polygon in hex coordinates.
    :return: ``None``
    """
    x, y = (_tocanvasxy(*xy) for xy in zip(x, y))
    _drawpolygonincanvas(x, y, **kwargs)


def drawrectangle(xmin, ymin, xmax, ymax, **kwargs):
    """
    Draw a rectangle.

    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
        The ``xmin``, ``ymin``, ``xmax``, and ``ymax`` arguments give the
        coordinates of the rectangle in hex coordinates.
    :return: ``None``
    """
    xmin, ymin = _tocanvasxy(xmin, ymin)
    xmax, ymax = _tocanvasxy(xmax, ymax)
    _drawrectangleincanvas(xmin, ymin, xmax, ymax, **kwargs)


def drawcompass(x, y, facing, **kwargs):
    """
    Draw a compass.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the coordinates of the compass in hex
        coordinates.
    :param facing:
        The ``facing`` argument specifies the direction of north in degrees.
    :return: ``None``
    """
    _drawcompassincanvas(*_tocanvasxy(x, y), _tocanvasfacing(facing), **kwargs)


def drawborder(xmin, ymin, xmax, ymax, width, **kwargs):
    """
    Draw a border.

    :param xmin:
    :param ymin:
    :param xmax:
    :param ymax:
        The ``xmin``, ``ymin``, ``xmax``, and ``ymax`` arguments give the
        coordinates of the external rectangle of the border in hex coordinates.
    :param width:
        The ``width`` argument specifies the width of the border in physical
        coordinates.
    :return: ``None``
    """
    _drawborderincanvas(
        *_tocanvasxy(xmin, ymin), *_tocanvasxy(xmax, ymax), width, **kwargs
    )


################################################################################


def _cosd(x):
    """Return the cosine of ``x`` in degrees."""
    return math.cos(math.radians(x))


def _sind(x):
    """Return the since of ``x`` in degrees."""
    return math.sin(math.radians(x))


################################################################################


def _drawhexincanvas(
    x,
    y,
    size=1,
    facing=0,
    linecolor="black",
    linewidth="normal",
    linestyle="solid",
    fillcolor=None,
    hatch=None,
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawhex` in canvas coordinates.
    """
    # size is inscribed diameter
    _ax.add_artist(
        patches.RegularPolygon(
            [x, y],
            6,
            radius=size * 0.5 * math.sqrt(4 / 3),
            orientation=math.pi / 6 + math.radians(facing),
            edgecolor=_nativecolor(linecolor),
            facecolor=_nativecolor(fillcolor),
            fill=(fillcolor != None),
            linestyle=linestyle,
            hatch=_nativehatchpattern(hatch),
            linewidth=_nativelinewidth(linewidth, linecolor),
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawcircleincanvas(
    x,
    y,
    size=1,
    linecolor="black",
    linewidth="normal",
    linestyle="solid",
    fillcolor=None,
    hatch=None,
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawcircle` in canvas coordinates.
    """
    # size is inscribed diameter
    _ax.add_artist(
        patches.Circle(
            [x, y],
            radius=0.5 * size,
            edgecolor=_nativecolor(linecolor),
            facecolor=_nativecolor(fillcolor),
            fill=(fillcolor != None),
            hatch=_nativehatchpattern(hatch),
            linewidth=_nativelinewidth(linewidth, linecolor),
            linestyle=linestyle,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawdotincanvas(
    x,
    y,
    size=1,
    facing=0,
    dx=0,
    dy=0,
    linecolor="black",
    linewidth="normal",
    fillcolor="black",
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawdot` in canvas coordinates.
    """
    x = x + dx * _sind(facing) + dy * _cosd(facing)
    y = y - dx * _cosd(facing) + dy * _sind(facing)
    _ax.add_artist(
        patches.Circle(
            [x, y],
            radius=0.5 * size,
            edgecolor=_nativecolor(linecolor),
            facecolor=_nativecolor(fillcolor),
            fill=(fillcolor != None),
            linewidth=_nativelinewidth(linewidth, linecolor),
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawlinesincanvas(
    x,
    y,
    linecolor="black",
    linewidth="normal",
    linestyle="solid",
    joinstyle="miter",
    capstyle="butt",
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawlines` in canvas coordinates.
    """
    plt.plot(
        x,
        y,
        linewidth=_nativelinewidth(linewidth, linecolor),
        linestyle=linestyle,
        color=_nativecolor(linecolor),
        solid_joinstyle=joinstyle,
        solid_capstyle=capstyle,
        alpha=alpha,
        zorder=zorder,
    )


def _drawarrowincanvas(
    x,
    y,
    size,
    facing,
    dx=0,
    dy=0,
    linecolor="black",
    linewidth="normal",
    fillcolor="black",
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawarrow` in canvas coordinates.
    """
    # size is length
    x = x + dx * _sind(facing) + dy * _cosd(facing)
    y = y - dx * _cosd(facing) + dy * _sind(facing)
    dx = size * _cosd(facing)
    dy = size * _sind(facing)
    x -= 0.5 * dx
    y -= 0.5 * dy
    _ax.add_artist(
        patches.FancyArrow(
            x,
            y,
            dx,
            dy,
            width=0.01,
            head_width=0.1,
            length_includes_head=True,
            edgecolor=_nativecolor(linecolor),
            facecolor=_nativecolor(linecolor),
            fill=(fillcolor != None),
            linewidth=_nativelinewidth(linewidth, linecolor),
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawdartincanvas(
    x,
    y,
    size,
    facing,
    dx=0,
    dy=0,
    linecolor="black",
    linewidth="normal",
    fillcolor="black",
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawdart` in canvas coordinates.
    """
    # size is length
    x = x + dx * _sind(facing) + dy * _cosd(facing)
    y = y - dx * _cosd(facing) + dy * _sind(facing)
    dx = size * _cosd(facing)
    dy = size * _sind(facing)
    x -= 0.5 * dx
    y -= 0.5 * dy
    _ax.add_artist(
        patches.FancyArrow(
            x,
            y,
            dx,
            dy,
            width=0.02,
            head_length=size,
            head_width=0.5 * size,
            length_includes_head=True,
            edgecolor=_nativecolor(linecolor),
            facecolor=_nativecolor(fillcolor),
            fill=(fillcolor != None),
            linewidth=_nativelinewidth(linewidth, linecolor),
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawtextincanvas(
    x,
    y,
    text,
    facing,
    dx=0,
    dy=0,
    textcolor="black",
    size="normal",
    alignment="center",
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawtext` in canvas coordinates.
    """
    x = x + dx * _sind(facing) + dy * _cosd(facing)
    y = y - dx * _cosd(facing) + dy * _sind(facing)
    # For reasons I do not understand, the alignment seems to be wrong for
    # rotated short strings. One fix is to pad the strings with spaces.
    if alignment == "left":
        text = "  " + text
    elif alignment == "center":
        text = "  " + text + "  "
    elif alignment == "right":
        text = text + "  "
    plt.text(
        x,
        y,
        text,
        size=_nativetextsize(size),
        rotation=facing - 90,
        color=_nativecolor(textcolor),
        alpha=alpha,
        horizontalalignment=alignment,
        verticalalignment="center_baseline",
        rotation_mode="anchor",
        clip_on=True,
        zorder=zorder,
    )


def _drawpolygonincanvas(
    x,
    y,
    linecolor="black",
    linewidth="normal",
    linestyle="solid",
    fillcolor=None,
    hatch=None,
    alpha=1.0,
    zorder=0,
):
    """
    The counterpart of :func:`drawpolygon` in canvas coordinates.
    """
    _ax.add_artist(
        patches.Polygon(
            list(zip(x, y)),
            edgecolor=_nativecolor(linecolor),
            facecolor=_nativecolor(fillcolor),
            fill=(fillcolor != None),
            linewidth=_nativelinewidth(linewidth, linecolor),
            linestyle=linestyle,
            hatch=_nativehatchpattern(hatch),
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawrectangleincanvas(xmin, ymin, xmax, ymax, **kwargs):
    """
    The counterpart of :func:`drawrectangle` in canvas coordinates.
    """
    _drawpolygonincanvas([xmin, xmin, xmax, xmax], [ymin, ymax, ymax, ymin], **kwargs)


def _drawcompassincanvas(x, y, facing, color="black", alpha=1.0, zorder=0):
    """
    The counterpart of :func:`drawcompass` in canvas coordinates.
    """
    _drawdotincanvas(
        x,
        y,
        facing=facing,
        size=0.07,
        dy=-0.25,
        linecolor=None,
        fillcolor=color,
        alpha=alpha,
        zorder=zorder,
    )
    _drawarrowincanvas(
        x,
        y,
        size=0.5,
        facing=facing,
        dy=0,
        linecolor=color,
        fillcolor=color,
        linewidth="thin",
        alpha=alpha,
        zorder=zorder,
    )
    _drawtextincanvas(
        x,
        y,
        "N",
        facing=facing,
        dx=-0.15,
        dy=-0.05,
        size="Large",
        textcolor=color,
        alpha=alpha,
        zorder=zorder,
    )


def _drawborderincanvas(xmin, ymin, xmax, ymax, width, fillcolor=None):
    """
    The counterpart of :func:`drawborder` in canvas coordinates.
    """
    _drawrectangleincanvas(
        xmin,
        ymin,
        xmax,
        ymin + width,
        fillcolor=fillcolor,
        linecolor=None,
    )
    _drawrectangleincanvas(
        xmin,
        ymax - width,
        xmax,
        ymax,
        fillcolor=fillcolor,
        linecolor=None,
    )
    _drawrectangleincanvas(
        xmin,
        ymin,
        xmin + width,
        ymax,
        fillcolor=fillcolor,
        linecolor=None,
    )
    _drawrectangleincanvas(
        xmax - width,
        ymin,
        xmax,
        ymax,
        fillcolor=fillcolor,
        linecolor=None,
    )


################################################################################

arccolor = "gray70"
arclinewidth = "thick"
arclinestyle = "dashed"


def drawarc(x, y, facing, arc):
    """
    Draw an arc.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the hex coordinates for the arc.
    :param facing:
       The ``facing`` argument gives the facing for the arc.
    :param arc:
        The ``arc`` argument is a string and specifies the arc. It must be one
        of: ``"0"`` (0 line), ``"180"`` (180 line), ``"limited"``, ``"180+"``,
        ``"L180+"`` (left 180+ arc), ``"R180+"`` (right 180+ arc), ``"150+"``,
        ``"120+"``, ``"90-"``, ``"60-"``, or ``"30-"``.
    :return:
        ``None``
    """

    def drawdxdy(dxdy, reflect=False):
        _drawlinesincanvas(
            [x + dxdy[0] * _cosd(facing) - dxdy[1] * _sind(facing) for dxdy in dxdy],
            [y + dxdy[0] * _sind(facing) + dxdy[1] * _cosd(facing) for dxdy in dxdy],
            linecolor=arccolor,
            linewidth=arclinewidth,
            linestyle=arclinestyle,
            zorder=0,
        )

    x, y = _tocanvasxy(x, y)
    facing = _tocanvasfacing(facing)

    if arc == "0":

        drawdxdy([[0, 0], [-100, 0]])

    elif arc == "180":

        drawdxdy([[0, 0], [+100, 0]])

    else:

        if arc == "limited":

            dxdy = [
                [0.333, +0.0],
                [1.5, +0.625],
                [5.0, +0.625],
                [6.0, +1.125],
                [10.0, +1.125],
                [11.0, +1.625],
                [100.0, +1.625],
            ]
            dxdy = [glass.hex.tophysicalxy(dxdy[0], dxdy[1]) for dxdy in dxdy]

        else:

            if arc == "180+" or arc == "L180+":
                halfangle = 30
            elif arc == "R180+":
                halfangle = -30
            elif arc == "150+":
                halfangle = 60
            elif arc == "120+" or arc == "90-":
                halfangle = 90
            elif arc == "60-":
                halfangle = 120
            elif arc == "30-":
                halfangle = 150
            else:
                raise RuntimeError("invalid arc %s." % arc)

            dxdy = [[0, 0], [100 * _cosd(halfangle), 100 * _sind(halfangle)]]

        drawdxdy(dxdy)

        if arc[0] == "L" or arc[0] == "R":
            drawdxdy([[0, 0], [+100, 0]])
        else:
            drawdxdy([[dxdy[0], -dxdy[1]] for dxdy in dxdy])


################################################################################

loscolor = arccolor
loslinewidth = "thick"
loslinestyle = "dashed"
losdotsize = 0.05


def drawlos(x0, y0, x1, y1):
    """
    Draw a line-of-sight between two elements.

    :param x0:
    :param y0:
        The ``x0`` and ``y0`` arguments give the hex coordinates for first
        element.
    :param x1:
    :param y1:
        The ``x1`` and ``y1`` arguments give the hex coordinates for second
        element.
    :return:
        ``None``
    """

    zorder = 100

    drawdot(
        x0,
        y0,
        fillcolor=loscolor,
        linecolor=loscolor,
        linewidth=loslinewidth,
        size=losdotsize,
        zorder=zorder,
    )
    drawdot(
        x1,
        y1,
        fillcolor=loscolor,
        linecolor=loscolor,
        linewidth=loslinewidth,
        size=losdotsize,
        zorder=zorder,
    )
    drawlines(
        [x0, x1],
        [y0, y1],
        linecolor=loscolor,
        linewidth=loslinewidth,
        linestyle=loslinestyle,
        zorder=zorder,
    )


################################################################################

annotationtextsize = "normal"
annotationtextcolor = "black"


def _drawannotation(
    x,
    y,
    facing,
    textposition,
    text,
    textsize=annotationtextsize,
    textcolor=annotationtextcolor,
    zorder=0,
):
    """
    Draw an element annotation.

    The notation can be drawn in one of six positions relative to the element:
    upper left, center left, lower left, upper right, center right, and center
    left.

    For aircraft and missiles, the conventional use of these positons are: -
    center right: name - upper left: flight type - center left: altitude - lower
    left: speed

    For other elements, the conventional use of these positions are: - center
    right: name - center left: alternative position for name when ground
    elements are stacked

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the hex coordinates of the element.
    :param facing:
       The ``facing`` argument gives the facing of the element.
    :param textposition:
        The ``textposition`` argument gives the position of the text relative to
        the element. It must be one of the strings ``"ul"`` (upper left),
        ``"cl"`` (center left), ``"ll"`` (lower left), ``"ur"`` (upper right),
        ``"cr"`` (center right), or ``"cl"`` (center left).
    :param text:
        The ``text`` argument gives text relative to be written. It must be a
        string.
    :return:
        ``None``
    """
    textdx = 0.08
    textdy = 0.15
    if not isinstance(textposition, str) or len(textposition) != 2:
        raise RuntimeError("invalid text position %r" % textposition)
    if textposition[0] == "u":
        textdy = +textdy
    elif textposition[0] == "c":
        textdy = 0
    elif textposition[0] == "l":
        textdy = -textdy
    else:
        raise RuntimeError("invalid text position %r" % textposition)
    if textposition[1] == "l":
        alignment = "right"
        textdx = -textdx
    elif textposition[1] == "r":
        alignment = "left"
        textdx = +textdx
    else:
        raise RuntimeError("invalid text position %r" % textposition)
    drawtext(
        x,
        y,
        text,
        facing=facing,
        dx=textdx,
        dy=textdy,
        size=textsize,
        textcolor=textcolor,
        alignment=alignment,
        zorder=zorder,
    )


################################################################################

pathcolor = "black"
pathlinewidth = "thick"
pathlinestyle = "dotted"
pathdotsize = 0.1


def drawpath(x, y, facing, altitude, speed, color, killed, annotate, surfaceelement):
    """
    Draw a path to show the movement of an element.

    :param x:
    :param y:
    :param facing:
    :param altitude:
        The ``x``, ``y``, ``facing``, and ``altitude`` arguments are lists
        giving the hex coordinates of the element, its facing, and its altitude.
        All must have the same length.
    :param speed:
        The ``speed`` argument must be ``None`` or a number giving the initial
        speed of the element.
    :param color:
        The ``color`` argument must be a color and should be the color of the
        element.
    :param killed:
        The ``killed`` argument must be a boolean value. If true, the path is
        drawn in a style appropriate for a killed element.
    :param annotate:
        The ``annotate`` argument must be a boolean value. If true, the initial
        point is annotated with the initial altitude in the center left position
        and this speed (if not ``None``) in the lower left position.
    :return:
        ``None``
    """
    if surfaceelement:
        linezorder = 0.1
        dotzorder = 0.5
    else:
        linezorder = 0.9
        dotzorder = altitude[0] + 0.9
    if killed:
        fillcolor = killedfillcolor
        linecolor = killedlinecolor
    else:
        fillcolor = color
        linecolor = pathcolor
    if len(x) > 1:
        drawlines(
            x,
            y,
            linecolor=linecolor,
            linewidth=pathlinewidth,
            linestyle=pathlinestyle,
            zorder=linezorder,
        )
        drawdot(
            x[0],
            y[0],
            fillcolor=fillcolor,
            linecolor=linecolor,
            linewidth=aircraftlinewidth,
            size=pathdotsize,
            zorder=dotzorder,
        )
        if annotate:
            _drawannotation(
                x[0], y[0], facing[0], "cl", "%d" % altitude[0], zorder=dotzorder
            )
            if speed is not None:
                _drawannotation(
                    x[0],
                    y[0],
                    facing[0],
                    "ll",
                    "%.1f" % speed,
                    zorder=dotzorder,
                )


################################################################################


aircraftlinecolor = "black"
aircraftlinewidth = "normal"


killedlinecolor = "gray60"
killedfillcolor = None


def drawaircraft(x, y, facing, altitude, speed, flighttype, name, color, killed):
    """
    Draw an aircraft.

    Draw an aircraft and annotate it with the first two letters of its flight
    type, its altitude, its speed, and its name.

    :param x:
    :param y:
    :param facing:
    :param altitude:
        The ``x``, ``y``, ``facing``, and ``altitude`` arguments are the hex
        coordinates of the aircraft, its facing, and its altitude.
    :param speed:
        The ``speed`` argument must be ``None`` or a number giving the initial
        speed of the aircraft.
    :param flighttype:
        The ``flighttype`` argument must be a string giving the flight type of
        the aircraft.
    :param name:
        The ``name`` argument must be a string giving the name of the aircraft.
    :param color:
        The ``color`` argument must be a color and should be the color of the
        aircraft.
    :param killed:
        The ``killed`` argument must be a boolean value. If true, the aircraft
        is drawn in a style appropriate for a killed element.
    :return:
        ``None``
    """
    if killed:
        fillcolor = killedfillcolor
        linecolor = killedlinecolor
    else:
        fillcolor = color
        linecolor = aircraftlinecolor
    zorder = altitude + 1.0
    drawdart(
        x,
        y,
        size=0.4,
        facing=facing,
        fillcolor=fillcolor,
        linewidth=aircraftlinewidth,
        linecolor=linecolor,
        zorder=zorder,
    )
    if not killed:
        _drawannotation(
            x,
            y,
            facing,
            "cr",
            name,
            zorder=zorder,
        )
        _drawannotation(
            x,
            y,
            facing,
            "ul",
            flighttype[:2],
            zorder=zorder,
        )
        _drawannotation(
            x,
            y,
            facing,
            "cl",
            "%2d" % altitude,
            zorder=zorder,
        )
        _drawannotation(
            x,
            y,
            facing,
            "ll",
            ("%.1f" % speed) if speed is not None else "",
            zorder=zorder,
        )


################################################################################


def drawmissile(x, y, facing, altitude, speed, name, color, annotate):
    """
    Draw a missile.

    Draw a missile and optionally annotate it with its altitude, its speed, and
    its name.

    :param x:
    :param y:
    :param facing:
    :param altitude:
        The ``x``, ``y``, ``facing``, and ``altitude`` arguments are the hex
        coordinates of the missile, its facing, and its altitude.
    :param speed:
        The ``speed`` argument must be ``None`` or a number giving the initial
        speed of the missile.
    :param name:
        The ``name`` argument must be a string giving the name of the missile.
    :param color:
        The ``color`` argument must be a color and should be the color of the
        missile.
    :param annotate:
        The ``annotate`` argument must be a boolean value. If true, the missile
        is annotated.
    :return:
        ``None``
    """
    fillcolor = color
    linecolor = aircraftlinecolor
    zorder = altitude + 1.1
    drawdart(
        x,
        y,
        size=0.2,
        facing=facing,
        fillcolor=fillcolor,
        linewidth=aircraftlinewidth,
        linecolor=linecolor,
        zorder=zorder,
    )
    if annotate:
        _drawannotation(
            x,
            y,
            facing,
            "cr",
            name,
            zorder=zorder,
        )
        _drawannotation(
            x,
            y,
            facing,
            "cl",
            "%d" % altitude,
            zorder=zorder,
        )
        _drawannotation(
            x,
            y,
            facing,
            "ll",
            "%.1f" % speed,
            zorder=zorder,
        )


################################################################################

barragefirelinecolor = "gray50"
barragefirelinewidth = "thick"
barragefirelinestyle = "dotted"


def drawbarragefire(x, y, altitude):
    """
    Draw a barrage fire marker

    :param x:
    :param y:
        The ``x`` and ``y`` arguments are the hex coordinates of the barrage
        fire.
    :param altitude:
        The ``altitude`` argument is the altitude to which the barrage fire
        extends.
    :return:
        ``None``
    """
    zorder = altitude + 1.5
    drawhex(
        x,
        y,
        size=2.0 + math.sqrt(3 / 4),
        facing=30,
        linecolor=barragefirelinecolor,
        fillcolor=None,
        linestyle=barragefirelinestyle,
        linewidth=barragefirelinewidth,
        zorder=zorder,
    )


################################################################################

plottedfirelinecolor = "gray50"
plottedfirelinewidth = "thick"
plottedfirelinestyle = "dashed"


def drawplottedfire(x, y, altitude):
    """
    Draw a plotted fire marker

    :param x:
    :param y:
        The ``x`` and ``y`` arguments are the hex coordinates of the plotted
        fire.
    :param altitude:
        The ``altitude`` argument is the altitude of the plotted fire.
    :return:
        ``None``
    """
    zorder = altitude + 3.5
    drawhex(
        x,
        y,
        size=2.0 + math.sqrt(3 / 4),
        facing=30,
        linecolor=plottedfirelinecolor,
        fillcolor=None,
        linestyle=plottedfirelinestyle,
        linewidth=plottedfirelinewidth,
        zorder=zorder,
    )


################################################################################

blastzonelinecolor = "gray50"
blastzonelinewidth = "thick"
blastzonelinestyle = "dotted"


def drawblastzone(x, y, altitude):
    """
    Draw a blast zone marker

    :param x:
    :param y:
        The ``x`` and ``y`` arguments are the hex coordinates of the blast zone.
    :param altitude:
        The ``altitude`` argument is the altitude to which the blast zone extends.
    :return:
        ``None``
    """
    zorder = altitude + 1.5
    drawhex(
        x,
        y,
        size=1.15,
        linecolor=blastzonelinecolor,
        fillcolor=None,
        linestyle=blastzonelinestyle,
        linewidth=blastzonelinewidth,
        zorder=zorder,
    )


################################################################################

bombcolor = "black"
bomblinecolor = "black"


def drawbomb(x, y, facing, altitude):
    """
    Draw a bomb.

    :param x:
    :param y:
    :param facing:
    :param altitude:
        The ``x``, ``y``, ``facing``, and ``altitude`` arguments are the hex
        coordinates of the bomb, its facing, and its altitude.
    :return:
        ``None``
    """
    zorder = altitude + 1.1
    drawdart(
        x,
        y,
        size=0.2,
        facing=facing,
        fillcolor=bombcolor,
        linewidth=aircraftlinewidth,
        linecolor=bomblinecolor,
        zorder=zorder,
    )


################################################################################

compactstacks = True


def setcompactstacks(value):
    global compactstacks
    compactstacks = value


################################################################################

groundunitlinewidth = "normal"
groundunittextsize = "scriptsize"
groundunitdx = 0.6
groundunitdy = 0.4


def drawgroundunit(
    x, y, facing, symbols, uppertext, lowertext, name, color, stack="1/1", killed=False
):
    """
    _summary_

    :param x:
    :param y:
    :param facing:
    :param altitude:
        The ``x``, ``y``, and ``facing`` arguments are the hex coordinates of
        the ground unit and its facing. If the unit does not have a facing, the
        ``facing`` argument should be ``None``.
    :param symbols:
        The ``symbols`` argument is a list of strings that describe how the
        ground unit is drawn. If the list contains ``"hex"``, the unit is drawn
        as with a hex outline; this is suitable for infrastructure targets such
        as buildings. If it does not contain ``"hex"``, it is drawn with a
        rectangular outline. The list can also contain any number of the
        following strings, which indicate the symbols to be drawn:
        ``"airdefense"``, ``"ammunition"``, ``"antiarmor"``, ``"armor"``,
        ``"artillery"``, ``"barge"``, ``"building"``, ``"fixedwing"``,
        ``"fuel"``, ``"gun"``, ``"hangar"``, ``"headquarters"``, ``"infantry"``,
        ``"junk"``, ``"limitedwheeled"``, ``"locomotive"``, ``"missile"``,
        ``"motorized"``, ``"multiplerocket"``, ``"ordnance"``, ``"radar"``,
        ``"railcar"``, ``"reconnaissance"``, ``"rotarywing"``, ``"supply"``,
        ``"tower"``, ``"transportation"``, ``"truck"``, and ``"wheeled"``.
    :param uppertext:
    :param lowertext:
        The ``uppertext`` and ``lowertext`` arguments are strings that we drawn
        in the upper and lower positions in the ground unit.
    :param name:
        The ``name`` argument is a string that names the ground unit.
    :param color:
        The ``color`` argument is a color and is the color of the ground unit.
    :param stack:
        The ``stack`` argument must be one of the strings ``"1/1"``, ``"1/2"``,
        ``"2/2"``, ``"1/3"``, ``"2/3"``, ``"3/3"``, ``"1/4"``, ``"2/4"``,
        ``"3/4"``, or ``"4/4"``. It indicates the position in a stack (e.g,
        ``"1/2"`` indicates the top unit in a stack of two and ``"2/3"``
        indicates the middle unit in a stack of three). The default is
        ``"1/1"``.
    :param killed:
    :param killed:
        The ``killed`` argument must be a boolean value. If true, the ground
        unit is drawn in a style appropriate for a killed element.
    :return:
        ``None``
    """
    _drawgroundunitincanvas(
        *_tocanvasxy(x, y),
        facing,
        symbols,
        uppertext,
        lowertext,
        name,
        color,
        stack,
        killed,
    )


def _drawgroundunitincanvas(
    x0,
    y0,
    facing,
    symbols,
    uppertext,
    lowertext,
    name,
    color,
    stack="1/1",
    killed=False,
):
    """
    The counterpart of :func:`drawgroundunit` in canvas coordinates.
    """
    if killed:
        fillcolor = killedfillcolor
        linecolor = killedlinecolor
        nametext = ""
    else:
        fillcolor = color
        linecolor = aircraftlinecolor
        nametext = name

    textdx = 0
    textdy = 0.3

    if hex in symbols:
        x = x0
        y = y0
        zorder = 0.0
    elif compactstacks:
        stackdx = 0.09
        stackdy = 0.07
        if stack == "1/2":
            x = x0 - 1.0 * stackdx
            y = y0 - 1.5 * stackdy
            zorder = 0.3
        elif stack == "2/2":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.5 * stackdy
            zorder = 0.2
        elif stack == "1/3":
            x = x0 + 1.0 * stackdx
            y = y0 - 1.5 * stackdy
            zorder = 0.4
        elif stack == "2/3":
            x = x0 - 1.0 * stackdx
            y = y0
            zorder = 0.3
        elif stack == "3/3":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.5 * stackdy
            zorder = 0.2
        elif stack == "1/4":
            x = x0 - 1.0 * stackdx
            y = y0 - 1.5 * stackdy
            zorder = 0.5
        elif stack == "2/4":
            x = x0 + 1.0 * stackdx
            y = y0 - 0.5 * stackdy
            zorder = 0.4
        elif stack == "3/4":
            x = x0 - 1.0 * stackdx
            y = y0 + 0.5 * stackdy
            zorder = 0.3
        elif stack == "4/4":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.5 * stackdy
            zorder = 0.2
        else:
            x = x0
            y = y0
            zorder = 0.2
    else:
        stackdx = 0.5 * groundunitdx + 0.03 * groundunitdx
        stackdy = 0.5 * groundunitdy + 0.03 * groundunitdx
        if stack == "1/2":
            x = x0 - 0.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.3
        elif stack == "2/2":
            x = x0 + 0.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.2
        elif stack == "1/3":
            x = x0 + 1.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.4
        elif stack == "2/3":
            x = x0 - 1.0 * stackdx
            y = y0
            zorder = 0.3
        elif stack == "3/3":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.2
        elif stack == "1/4":
            x = x0 - 1.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.5
        elif stack == "2/4":
            x = x0 + 1.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.4
        elif stack == "3/4":
            x = x0 - 1.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.3
        elif stack == "4/4":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.2
        else:
            x = x0
            y = y0
            zorder = 0.2

    def drawinfantrysymbol():
        _drawlinesincanvas(
            [x - groundunitdx / 2, x + groundunitdx / 2],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [x - groundunitdx / 2, x + groundunitdx / 2],
            [y + groundunitdy / 2, y - groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawantiarmorsymbol():
        _drawlinesincanvas(
            [x - groundunitdx / 2, x],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [x + groundunitdx / 2, x],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawreconnaissancesymbol():
        _drawlinesincanvas(
            [x - groundunitdx / 2, x + groundunitdx / 2],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawarmorsymbol():
        fx = 0.15
        fy = 0.2
        theta = range(0, 361)

        def dx(theta):
            if theta < 90 or theta > 270:
                return +fx * groundunitdx + fy * groundunitdy * _cosd(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fx * groundunitdx + fy * groundunitdy * _cosd(theta)

        def dy(theta):
            return fy * groundunitdy * _sind(theta)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawartillerysymbol():
        ry = 0.1
        _drawcircleincanvas(
            x,
            y,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            fillcolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawairdefensesymbol():
        fy = 0.30
        theta = range(0, 180)

        def airdefencex(theta):
            return x + groundunitdx / 2 * _cosd(theta)

        def airdefencey(theta):
            return y - groundunitdy / 2 + fy * groundunitdy * _sind(theta)

        _drawrectangleincanvas(
            x + groundunitdx * (-0.5),
            y + groundunitdy * (-0.5),
            x + groundunitdx * (+0.5),
            y + groundunitdy * (-0.5 + fy),
            linecolor=None,
            fillcolor=fillcolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

        _drawlinesincanvas(
            list([airdefencex(theta) for theta in theta]),
            list([airdefencey(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawradarsymbol():
        fy0 = 0.05
        fy1 = 0.04
        ry = 0.18
        y0 = y + fy0 * groundunitdy
        theta0 = 45
        theta = range(90 + theta0, 270 + theta0)

        def dx(theta):
            return ry * groundunitdy * _cosd(theta)

        def dy(theta):
            return ry * groundunitdy * _sind(theta)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y0 + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        dx = ry * groundunitdy * _cosd(theta0)
        dy = ry * groundunitdy * _sind(theta0)
        _drawlinesincanvas(
            [x - dx, x, x, x + dx],
            [
                y0 - dy,
                y0 + fy1 * groundunitdy,
                y0 - fy1 * groundunitdy,
                y0 + dy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawgunsymbol():
        fx = 0.15
        _drawlinesincanvas(
            [x + (fx - 0.5) * groundunitdx, x + (fx - 0.5) * groundunitdx],
            [y - 0.5 * groundunitdy, y + 0.5 * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawmultiplerocketsymbol():
        fx0 = 0.10
        fy0 = 0.10
        fy1 = 0.10
        fy2 = 0.15
        for i in range(2):
            _drawlinesincanvas(
                [x - fx0 * groundunitdx, x, x + fx0 * groundunitdx],
                [
                    y + (fy0 + i * fy1) * groundunitdy,
                    y + (fy0 + i * fy1 + fy2) * groundunitdy,
                    y + (fy0 + i * fy1) * groundunitdy,
                ],
                linecolor=linecolor,
                linewidth=groundunitlinewidth,
                zorder=zorder,
            )

    def drawmissilesymbol():
        fx = 0.07
        fy0 = -0.5
        fy1 = 0.15
        theta = range(0, 181)

        def dx(theta):
            return fx * groundunitdx * _cosd(theta)

        def dy(theta):
            if theta == 0 or theta == 180:
                return fy0 * groundunitdy
            else:
                return fy1 * groundunitdy + fx * groundunitdx * (_sind(theta) - 1)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawammunitionsymbol():
        fx0 = 0.1
        fx1 = 0.15
        fy0 = 0.20
        theta = range(0, 181)

        def dx(theta):
            return fx0 * groundunitdx * _cosd(theta)

        def dy(theta):
            if theta == 0 or theta == 180:
                return -fy0 * groundunitdy
            else:
                return fy0 * groundunitdy + fx0 * groundunitdx * (_sind(theta) - 1)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [x - fx1 * groundunitdx, x + fx1 * groundunitdx],
            [y - fy0 * groundunitdy, y - fy0 * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawfuelsymbol():
        fx = 0.15
        fy0 = 0.20
        _drawlinesincanvas(
            [x, x, x - 0.5 * fx * groundunitdx, x + 0.5 * fx * groundunitdx, x],
            [
                y - fy0 * groundunitdy,
                y + fy0 * groundunitdy - fx * groundunitdx * _cosd(30),
                y + fy0 * groundunitdy,
                y + fy0 * groundunitdy,
                y + fy0 * groundunitdy - fx * groundunitdx * _cosd(30),
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawordnancesymbol():
        ry0 = 0.20
        ry1 = 0.35
        for theta in range(45, 180, 90):
            dx = ry1 * groundunitdy * _cosd(theta)
            dy = ry1 * groundunitdy * _sind(theta)
            _drawlinesincanvas(
                [x - dx, x + dx],
                [y - dy, y + dy],
                linecolor=linecolor,
                linewidth=groundunitlinewidth,
                zorder=zorder,
            )
        _drawcircleincanvas(
            x,
            y,
            2 * ry0 * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            fillcolor=linecolor,
            zorder=zorder,
        )

    def drawmotorizedsymbol():
        fx = 0.12
        _drawlinesincanvas(
            [x, x],
            [y - 0.5 * groundunitdy, y + 0.5 * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawwheeledsymbol():
        fx = 0.12
        fy = 0.38
        ry = 0.05
        _drawcircleincanvas(
            x - fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleincanvas(
            x,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleincanvas(
            x + fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawlimitedwheeledsymbol():
        fx = 0.12
        fy = 0.38
        ry = 0.05
        _drawcircleincanvas(
            x - fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleincanvas(
            x + fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawsupplysymbol():
        fy = 0.25
        _drawlinesincanvas(
            [x - 0.5 * groundunitdx, x + 0.5 * groundunitdx],
            [y + (fy - 0.5) * groundunitdy, y + (fy - 0.5) * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawheadquarterssymbol():
        fy = 0.25
        _drawlinesincanvas(
            [x - 0.5 * groundunitdx, x + 0.5 * groundunitdx],
            [y + fy * groundunitdy, y + fy * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawtransportationsymbol():
        ry = 0.25
        fy = 0.0
        _drawcircleincanvas(
            x,
            y + fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        for theta in range(0, 180, 45):
            dx = ry * groundunitdy * _cosd(theta)
            dy = ry * groundunitdy * _sind(theta)
            _drawlinesincanvas(
                [x - dx, x + dx],
                [y + fy * groundunitdy - dy, y + fy * groundunitdy + dy],
                linecolor=linecolor,
                linewidth=groundunitlinewidth,
                zorder=zorder,
            )

    def drawlocomotivesymbol():
        fx = 0.25
        fy = 0.25
        dx = fx * groundunitdx
        dy = fy * groundunitdy
        _drawpolygonincanvas(
            [
                x - dx,
                x - dx,
                x,
                x,
                x + dx,
                x + dx,
            ],
            [
                y - dy,
                y + dy,
                y + dy,
                y,
                y,
                y - dy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        drawrailsymbol()

    def drawcarsymbol():
        fx0 = 0.25
        fy0 = 0.25
        fy1 = 0.15
        theta = range(0, 181)

        def dx(theta):
            return fx0 * groundunitdx * _cosd(theta)

        def dy(theta):
            return fy0 * groundunitdy - fy1 * groundunitdy * _sind(theta)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [
                x - fx0 * groundunitdx,
                x - fx0 * groundunitdx,
                x + fx0 * groundunitdx,
                x + fx0 * groundunitdx,
            ],
            [
                y + fy0 * groundunitdy,
                y - fy0 * groundunitdy,
                y - fy0 * groundunitdy,
                y + fy0 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawrailsymbol():
        fx1 = 0.20
        fx2 = 0.10
        fy2 = 0.38
        ry = 0.05
        _drawcircleincanvas(
            x - fx2 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleincanvas(
            x - fx1 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleincanvas(
            x + fx1 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleincanvas(
            x + fx2 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawrailcarsymbol():
        drawcarsymbol()
        drawrailsymbol()

    def drawtrucksymbol():
        drawcarsymbol()
        drawlimitedwheeledsymbol()

    def drawbargesymbol():
        fx0 = 0.25
        fx1 = 0.12
        fy0 = -0.1
        fy1 = 0.1
        fy2 = 0.0
        fy3 = 0.3
        fy4 = 0.2
        theta = range(0, 181)

        def dx(theta):
            return fx0 * groundunitdx * _cosd(theta)

        def dy(theta):
            return fy0 * groundunitdy - fy1 * groundunitdy * _sind(theta)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [
                x - fx0 * groundunitdx,
                x + fx0 * groundunitdx,
            ],
            [
                y + fy0 * groundunitdy,
                y + fy0 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawjunksymbol():
        fx0 = 0.25
        fx1 = 0.12
        fy0 = -0.1
        fy1 = 0.1
        fy2 = 0.0
        fy3 = 0.3
        fy4 = 0.2
        drawbargesymbol()
        _drawlinesincanvas(
            [
                x,
                x,
            ],
            [
                y + fy0 * groundunitdy,
                y + 0.5 * (fy3 + fy4) * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawpolygonincanvas(
            [
                x - fx1 * groundunitdx,
                x - fx1 * groundunitdx,
                x + fx1 * groundunitdx,
                x + fx1 * groundunitdx,
            ],
            [
                y + fy2 * groundunitdy,
                y + fy3 * groundunitdy,
                y + fy4 * groundunitdy,
                y + fy2 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawbuildingsymbol():
        fx0 = 0.2
        fy0 = -0.2
        fy1 = 0.25
        fy2 = 0.15
        _drawpolygonincanvas(
            [
                x - fx0 * groundunitdx,
                x - fx0 * groundunitdx,
                x + fx0 * groundunitdx,
                x + fx0 * groundunitdx,
            ],
            [
                y + fy0 * groundunitdy,
                y + fy1 * groundunitdy,
                y + fy2 * groundunitdy,
                y + fy0 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawtowersymbol():
        fx0 = 0.125
        fx1 = 0.075
        fy0 = -0.2
        fy1 = 0.15
        fy2 = 0.30
        _drawlinesincanvas(
            [
                x - fx0 * groundunitdx,
                x - fx1 * groundunitdx,
                x - fx1 * groundunitdx,
                x + fx1 * groundunitdx,
                x + fx1 * groundunitdx,
                x + fx0 * groundunitdx,
            ],
            [
                y + fy0 * groundunitdy,
                y + fy1 * groundunitdy,
                y + fy2 * groundunitdy,
                y + fy2 * groundunitdy,
                y + fy1 * groundunitdy,
                y + fy0 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [
                x - fx1 * groundunitdx,
                x + fx1 * groundunitdx,
            ],
            [
                y + fy1 * groundunitdy,
                y + fy1 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawhangarsymbol():
        fx0 = 0.25
        fy0 = -0.2
        fy1 = 0.3
        theta = range(0, 181)

        def dx(theta):
            return fx0 * groundunitdx * _cosd(theta)

        def dy(theta):
            return fy0 * groundunitdy + fy1 * groundunitdy * _sind(theta)

        _drawlinesincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesincanvas(
            [
                x - fx0 * groundunitdx,
                x + fx0 * groundunitdx,
            ],
            [
                y + fy0 * groundunitdy,
                y + fy0 * groundunitdy,
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawfixedwingsymbol():
        fx = 0.15
        fy = 0.1
        theta = range(0, 361)

        def dx(theta):
            if theta < 90 or theta > 270:
                return +fx * groundunitdx + fy * groundunitdy * _cosd(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fx * groundunitdx + fy * groundunitdy * _cosd(theta)

        def dy(theta):
            if theta < 90 or theta > 270:
                return +fy * groundunitdy * _sind(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fy * groundunitdy * _sind(theta)

        _drawpolygonincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            fillcolor=linecolor,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawrotarywingsymbol():
        fx = 0.15
        fy = 0.1
        theta = range(0, 361)

        def dx(theta):
            if theta < 90 or theta > 270:
                return +fx * groundunitdx
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fx * groundunitdx

        def dy(theta):
            if theta < 90 or theta > 270:
                return +fy * groundunitdy * _sind(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fy * groundunitdy * _sind(theta)

        _drawpolygonincanvas(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            fillcolor=linecolor,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawaircraftsymbol(text):
        drawuppertext(text)

    def drawuppertext(text):
        _drawtextincanvas(
            x,
            y,
            text,
            facing=90,
            dx=0,
            dy=+groundunitdy * 0.32,
            size=groundunittextsize,
            textcolor=linecolor,
            alignment="center",
            zorder=zorder,
        )

    def drawlowertext(text):
        _drawtextincanvas(
            x,
            y,
            text,
            facing=90,
            dx=0,
            dy=-groundunitdy * 0.36,
            size=groundunittextsize,
            textcolor=linecolor,
            alignment="center",
            zorder=zorder,
        )

    if facing is not None:
        _drawarrowincanvas(
            x0,
            y0,
            size=0.7,
            facing=facing,
            dy=0.35,
            linewidth=1,
            linecolor=linecolor,
            zorder=0,
        )

    if "hex" not in symbols:
        _drawrectangleincanvas(
            x - groundunitdx / 2,
            y - groundunitdy / 2,
            x + groundunitdx / 2,
            y + groundunitdy / 2,
            linewidth=groundunitlinewidth,
            fillcolor=fillcolor,
            linecolor=None,
            zorder=zorder,
        )

    # Draw missile and air defences first, since air defense missile is
    # different to surface-to-surface missile.
    if "missile" in symbols:
        drawmissilesymbol()
    if "airdefense" in symbols:
        drawairdefensesymbol()

    if "infantry" in symbols:
        drawinfantrysymbol()
    if "armor" in symbols:
        drawarmorsymbol()
    if "artillery" in symbols:
        drawartillerysymbol()
    if "reconnaissance" in symbols:
        drawreconnaissancesymbol()
    if "antiarmor" in symbols:
        drawantiarmorsymbol()
    if "supply" in symbols:
        drawsupplysymbol()
    if "headquarters" in symbols:
        drawheadquarterssymbol()
    if "transportation" in symbols:
        drawtransportationsymbol()
    if "radar" in symbols:
        drawradarsymbol()
    if "ammunition" in symbols:
        drawammunitionsymbol()
    if "fuel" in symbols:
        drawfuelsymbol()
    if "ordnance" in symbols:
        drawordnancesymbol()

    if "gun" in symbols or "cannon" in symbols:
        drawgunsymbol()
    if "multiplerocket" in symbols:
        drawmultiplerocketsymbol()
    if "motorized" in symbols:
        drawmotorizedsymbol()
    if "wheeled" in symbols:
        drawwheeledsymbol()
    if "limitedwheeled" in symbols:
        drawlimitedwheeledsymbol()

    if "locomotive" in symbols:
        drawlocomotivesymbol()
    if "railcar" in symbols:
        drawrailcarsymbol()
    if "truck" in symbols:
        drawtrucksymbol()
    if "barge" in symbols:
        drawbargesymbol()
    if "junk" in symbols:
        drawjunksymbol()
    if "building" in symbols:
        drawbuildingsymbol()
    if "tower" in symbols:
        drawtowersymbol()
    if "hangar" in symbols:
        drawhangarsymbol()

    if "fixedwing" in symbols:
        drawfixedwingsymbol()
    if "rotarywing" in symbols:
        drawrotarywingsymbol()

    if uppertext is not None:
        drawuppertext(uppertext)
    if lowertext is not None:
        drawlowertext(lowertext)

    if "hex" not in symbols:

        _drawrectangleincanvas(
            x - groundunitdx / 2,
            y - groundunitdy / 2,
            x + groundunitdx / 2,
            y + groundunitdy / 2,
            linewidth=groundunitlinewidth,
            fillcolor=None,
            linecolor=linecolor,
            zorder=zorder,
        )

        if not killed:
            if x >= x0:
                _drawtextincanvas(
                    x,
                    y,
                    name,
                    facing=90,
                    dx=groundunitdx / 2 - 0.05,
                    dy=-0.01,
                    size=annotationtextsize,
                    textcolor=annotationtextcolor,
                    alignment="left",
                    zorder=zorder,
                )
            else:
                _drawtextincanvas(
                    x,
                    y,
                    name,
                    facing=90,
                    dx=-groundunitdx / 2 + 0.05,
                    dy=-0.01,
                    size=annotationtextsize,
                    textcolor=annotationtextcolor,
                    alignment="right",
                    zorder=zorder,
                )

    else:

        _drawhexincanvas(
            x,
            y,
            size=0.9,
            linewidth=groundunitlinewidth,
            fillcolor=None,
            linecolor=linecolor,
            zorder=zorder,
        )


################################################################################

shiplinecolor = aircraftlinecolor
shiplinewidth = aircraftlinewidth


def drawship(
    x,
    y,
    facing,
    large,
    name,
    color,
    stack,
    killed,
):
    """
    Draw a ship.

    :param x:
    :param y:
        The ``x`` and ``y`` arguments give the hex coordinates of the ship.
    :param facing:
        The ``facing`` argument gives the facing of the ship.
    :param large:
        The ``large`` argument determines if the ship is a large ship.
    :param name:
        The ``name`` argument gives the name of the ship.
    :param color:
        The ``color`` argument gives the color of the ship.
    :param stack:
        The ``stack`` argument must be one of the strings ``"1/1"``, ``"1/2"``,
        ``"2/2"``. It indicates the position in a stack (e.g,
        ``"1/2"`` indicates the top unit in a stack of two and ``"2/2"``
        indicates the top unit in a stack of two). The default is
        ``"1/1"``.
    :param killed:
        The ``killed`` argument determines whether the ship has been killed. If so, it is drawn in outline only.
    :return:
        ``None``
    """
    _drawshipincanvas(
        *_tocanvasxy(x, y),
        _tocanvasfacing(facing),
        name,
        color,
        killed,
        large=large,
    )
    if not killed:
        _drawannotation(
            x,
            y,
            facing,
            "cr",
            name,
            zorder=0.2,
        )


def _drawshipincanvas(
    x,
    y,
    facing,
    name,
    color,
    killed,
    large=False,
):

    if killed:
        fillcolor = killedfillcolor
        linecolor = killedlinecolor
    else:
        fillcolor = color
        linecolor = aircraftlinecolor

    if large:
        sizefactor = 1.5
    else:
        sizefactor = 1.1

    length = 0.50
    bow = 0.20
    beam = 0.12
    dx0 = [
        +0.5 * length,
        +0.5 * length - bow,
        -0.5 * length,
        -0.5 * length,
        +0.5 * length - bow,
    ]
    dy0 = [0.0, +0.5 * beam, +0.5 * beam, -0.5 * beam, -0.5 * beam]
    x = list(
        x + sizefactor * (dx0 * _cosd(facing) - dy0 * _sind(facing))
        for dx0, dy0 in zip(dx0, dy0)
    )
    y = list(
        y + sizefactor * (dx0 * _sind(facing) + dy0 * _cosd(facing))
        for dx0, dy0 in zip(dx0, dy0)
    )
    _drawpolygonincanvas(
        x,
        y,
        linecolor=linecolor,
        linewidth=shiplinewidth,
        fillcolor=fillcolor,
        zorder=0.2,
    )


################################################################################


def _nativelinewidth(linewidth, linecolor):
    """
    Return the native line width.

    :param linewidth:
        The `linewidth`` argument must be ``None``, number giving the line width
        in hexes or one of the strings ``"thin"``, ``"normal"``, or ``"thick"``.
    :param linecolor: A line color.
    :return: 0 if ``linecolor`` is ``None``, otherwise the native line width
        corresponding to the ``linewidth`` argument.
    """
    if linecolor is None or linewidth is None:
        return 0
    elif linewidth == "thin":
        return 0.5
    elif linewidth == "normal":
        return 1.0
    elif linewidth == "thick":
        return 2.0
    else:
        # Native line widths are in points.
        return int(linewidth * _pointsperhex + 0.5)


def _nativetextsize(textsize):
    """
    Return the native text size

    :param textsize:
        The ``textsize`` argument is a number giving the text size in hexes or one of
        the strings ``"tiny"``, ``"scriptsize"``, ``"footnotesize"``,
        ``"small"``, ``"normal"``, ``"large"``, ``"Large"``, ``"LARGE"``,
        ``"huge"``, and ``"HUGE"``.
    :return: The native text size corresponding to the ``textsize``a argument.
    """
    # The correspondence between names and sizes are approximately the LaTeX
    # font sizes in 10 pt documents and are appropriate for 1 hex = 1 inch.
    if textsize == "tiny":
        return 5
    elif textsize == "scriptsize":
        return 7
    elif textsize == "footnotesize":
        return 8
    elif textsize == "small":
        return 9
    elif textsize == "normal":
        return 10
    elif textsize == "large":
        return 12
    elif textsize == "Large":
        return 14
    elif textsize == "LARGE":
        return 18
    elif textsize == "huge":
        return 21
    elif textsize == "HUGE":
        return 24
    else:
        # Native text sizes are in points.
        return int(textsize * _pointsperhex + 0.5)


def _nativehatchpattern(hatchpattern):
    """
    Return the native hatch pattern.

    :param hatchpattern:
        The ``hatchpattern`` argument must be ``None`` or one of the strings
        ``"forsest"``, ``"city"``, or ``"town"``.
    :return: The native hatch pattern corresponding to the ``hatchpattern``a
        argument.
    """
    if hatchpattern is None:
        return None
    elif hatchpattern == "forest":
        return ".o"
    elif hatchpattern == "town" or hatchpattern == "city":
        return "xx"
    else:
        raise RuntimeError("invalid hatch pattern %r" % hatchpattern)


# I determine colors from images using the Digital Color Meter on macOS. I use
# native RGB values.

_colormap = {
    # Grays
    "white": (1.00, 1.00, 1.00),
    "gray95": (0.95, 0.95, 0.95),
    "gray90": (0.90, 0.90, 0.90),
    "gray85": (0.85, 0.85, 0.85),
    "gray80": (0.80, 0.80, 0.80),
    "gray75": (0.75, 0.75, 0.75),
    "gray70": (0.70, 0.70, 0.70),
    "gray65": (0.65, 0.65, 0.65),
    "gray60": (0.60, 0.60, 0.60),
    "gray55": (0.55, 0.55, 0.55),
    "gray50": (0.50, 0.50, 0.50),
    "gray45": (0.45, 0.45, 0.45),
    "gray40": (0.40, 0.40, 0.40),
    "gray35": (0.35, 0.35, 0.35),
    "gray30": (0.30, 0.30, 0.30),
    "gray25": (0.25, 0.25, 0.25),
    "gray20": (0.20, 0.20, 0.20),
    "gray15": (0.15, 0.15, 0.15),
    "gray10": (0.10, 0.10, 0.10),
    "gray05": (0.05, 0.05, 0.05),
    "black": (0.00, 0.00, 0.00),
    "grey95": "gray95",
    "grey90": "gray90",
    "grey85": "gray85",
    "grey80": "gray80",
    "grey75": "gray75",
    "grey70": "gray70",
    "grey65": "gray65",
    "grey60": "gray60",
    "grey55": "gray55",
    "grey50": "gray50",
    "grey45": "gray45",
    "grey40": "gray40",
    "grey35": "gray35",
    "grey30": "gray30",
    "grey25": "gray25",
    "grey20": "gray20",
    "grey15": "gray15",
    "grey10": "gray10",
    "grey05": "gray05",
    # Generic colors
    "aluminum": "gray80",
    "aluminium": "aluminum",
    "unpainted": "aluminum",
    # https://www.theworldwars.net/resources/file.php?r=camo_usn#korea
    "darkblue": (0.110, 0.220, 0.310),
    "skyblue": (0.490, 0.780, 0.910),
    "green": "olivedrab",
    "olivedrab": (0.420, 0.557, 0.137),  # CSS olive drab
    "lightgreen": "lightolivedrab",
    "lightolivedrab": (0.624, 0.714, 0.439),
    "tan": (0.824, 0.706, 0.549),  # CSS tan
    "darktan": (0.576, 0.494, 0.384),
    "sand": (0.941, 0.918, 0.839),
    "darkgray": "gray40",
    "darkgrey": "darkgray",
    "mediumgray": "gray60",
    "mediumgrey": "mediumgray",
    "lightgray": "gray70",
    "lightgrey": "lightgray",
    "slategray": (0.439, 0.502, 0.565),  # CSS slategray
    "slategrey": "slategray",
    # Approximations to NATO blue, red, green, and yellow.
    # https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology#APP-6A_affiliation
    "natoblue": (0.45, 0.87, 1.00),
    "natored": (1.00, 0.45, 0.45),
    "natogreen": (0.55, 1.00, 0.55),
    "natoyellow": (1.00, 1.00, 0.46),
    "natofriendly": "natoblue",
    "natohostile": "natored",
    "natoneutral": "natogreen",
    "natounknown": "natoyellow",
    # The blue of the IAF roundel.
    # https://en.wikipedia.org/wiki/General_Dynamics_F-16_Fighting_Falcon_variants#F-16I_Sufa
    # This blue is darker and more saturated that the NATO blue.
    "iafblue": (0.000, 0.541, 0.753),
    # Pan-Arab colors.
    # https://en.wikipedia.org/wiki/Pan-Arab_colors
    # https://en.wikipedia.org/wiki/Pan-Arab_colors#/media/File:Flag_of_Hejaz_1917.svg
    # This red is darker and more saturated than the NATO red. This green is lighter and
    # more saturated than the standard green.
    "panarabred": (0.780, 0.071, 0.133),
    "panarabgreen": (0.035, 0.435, 0.208),
}


def _nativecolor(color):
    """
    Return the native color.

    :param color:
        A color name or a list or tuple of the three RGB components as numbers
        from 0 to 1.
    :return:
        The color represented as a tuple of the three RGB components as numbers
        from 0 to 1.
    """

    if not isinstance(color, str):
        return color
    elif color in _colormap:
        return _nativecolor(_colormap[color])
    else:
        return color


################################################################################
