import math

import apxo.hex as aphex
import apxo.variants as apvariants

import pickle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image

################################################################################

plt.rcParams.update({"figure.max_open_warning": 0})

################################################################################

_fig = None
_ax = None


def setcanvas(xmin, ymin, xmax, ymax, dotsperhex=100):
    global _fig, _ax
    xmin, ymin = aphex.tophysical(xmin, ymin)
    xmax, ymax = aphex.tophysical(xmax, ymax)
    _fig = plt.figure(
        figsize=[(xmax - xmin), (ymax - ymin)],
        frameon=False,
        dpi=dotsperhex,
    )

    plt.axis("off")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    _ax = plt.gca()
    _ax.set_position([0, 0, 1, 1])
    _ax.add_artist(
        patches.Polygon(
            [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]],
            edgecolor="None",
            facecolor="white",
            fill=True,
            linewidth=0,
            zorder=0,
        )
    )


def save():
    pickle.dump(_fig, open("apxo.pickle", "wb"))


def restore():
    global _fig, _ax
    _fig = pickle.load(open("apxo.pickle", "rb"))
    _ax = plt.gca()


def show():
    # Avoid "UserWarning: FigureCanvasAgg is non-interactive, and thus
    # cannot be shown". Ommiting the _fig.show() works in a Jupyter
    # notebook since it is implicit at the end of each cell.
    # _fig.show()
    pass


def writefile(name, rotation=0):
    _fig.savefig(name)
    if rotation != 0:
        # Attempt to rotate the file. This works for pixelated formats supported by PIL,
        # but not for vector format, so we catch failures.
        try:
            Image.open(name).rotate(rotation, expand=True).save(name)
        except:
            pass


################################################################################


def cosd(x):
    return math.cos(math.radians(x))


def sind(x):
    return math.sin(math.radians(x))


################################################################################


def _drawhexinphysical(
    x,
    y,
    size=1,
    linecolor="black",
    linewidth=0.5,
    fillcolor=None,
    linestyle="solid",
    rotation=0,
    hatch=None,
    alpha=1.0,
    zorder=1,
):
    if linecolor is None:
        linewidth = 0
    # size is inscribed diameter
    _ax.add_artist(
        patches.RegularPolygon(
            [x, y],
            6,
            radius=size * 0.5 * math.sqrt(4 / 3),
            orientation=math.pi / 6 + math.radians(rotation),
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
            linestyle=linestyle,
            hatch=hatch,
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawcircleinphysical(
    x,
    y,
    size=1,
    linecolor="black",
    linewidth=0.5,
    fillcolor=None,
    hatch=None,
    alpha=1.0,
    zorder=1,
):
    if linecolor is None:
        linewidth = 0
    _ax.add_artist(
        patches.Circle(
            [x, y],
            radius=0.5 * size,
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
            hatch=hatch,
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawsquareinphysical(
    x,
    y,
    size=1,
    facing=0,
    linecolor="black",
    linewidth=0.5,
    fillcolor=None,
    hatch=None,
    alpha=1.0,
    zorder=1,
):
    # size is circumscribed diameter
    if linecolor is None:
        linewidth = 0
    _ax.add_artist(
        patches.RegularPolygon(
            [x, y],
            4,
            radius=size * 0.5,
            orientation=math.radians(facing),
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
            hatch=hatch,
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawdotinphysical(
    x,
    y,
    size=1,
    facing=0,
    dx=0,
    dy=0,
    fillcolor="black",
    linecolor="black",
    linewidth=0.5,
    alpha=1.0,
    zorder=1,
):
    if linecolor is None:
        linewidth = 0
    x = x + dx * sind(facing) + dy * cosd(facing)
    y = y - dx * cosd(facing) + dy * sind(facing)
    _ax.add_artist(
        patches.Circle(
            [x, y],
            radius=0.5 * size,
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawlinesinphysical(
    x,
    y,
    linecolor="black",
    linewidth=0.5,
    linestyle="solid",
    joinstyle="miter",
    capstyle="butt",
    alpha=1.0,
    zorder=1,
):
    if linecolor is None:
        linewidth = 0
    plt.plot(
        x,
        y,
        linewidth=linewidth,
        linestyle=linestyle,
        color=_mapcolor(linecolor),
        solid_joinstyle=joinstyle,
        solid_capstyle=capstyle,
        alpha=alpha,
        zorder=zorder,
    )


def _drawarrowinphysical(
    x,
    y,
    facing,
    size=1.0,
    dx=0,
    dy=0,
    linecolor="black",
    fillcolor="black",
    linewidth=0.5,
    alpha=1.0,
    zorder=1,
):
    # size is length
    if linecolor is None:
        linewidth = 0
    x = x + dx * sind(facing) + dy * cosd(facing)
    y = y - dx * cosd(facing) + dy * sind(facing)
    dx = size * cosd(facing)
    dy = size * sind(facing)
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
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(linecolor),
            fill=(fillcolor != None),
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawdoublearrowinphysical(x, y, facing, **kwargs):
    _drawarrowinphysical(x, y, facing, **kwargs)
    _drawarrowinphysical(x, y, facing + 180, **kwargs)


def _drawdartinphysical(
    x,
    y,
    facing,
    size=1.0,
    dx=0,
    dy=0,
    linecolor="black",
    fillcolor="black",
    linewidth=0.5,
    alpha=1.0,
    zorder=1,
):
    # size is length
    if linecolor is None:
        linewidth = 0
    x = x + dx * sind(facing) + dy * cosd(facing)
    y = y - dx * cosd(facing) + dy * sind(facing)
    dx = size * cosd(facing)
    dy = size * sind(facing)
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
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawtextinphysical(
    x,
    y,
    facing,
    s,
    dx=0,
    dy=0,
    color="black",
    size=10,
    alpha=1.0,
    zorder=1,
    alignment="center",
):
    x = x + dx * sind(facing) + dy * cosd(facing)
    y = y - dx * cosd(facing) + dy * sind(facing)
    # For reasons I do not understand, the alignment seems to be wrong for
    # rotated short strings. One fix is to pad the strings with spaces.
    if alignment == "left":
        s = "  " + s
    elif alignment == "center":
        s = "  " + s + "  "
    elif alignment == "right":
        s = s + "  "
    plt.text(
        x,
        y,
        s,
        size=size,
        rotation=facing - 90,
        color=_mapcolor(color),
        alpha=alpha,
        horizontalalignment=alignment,
        verticalalignment="center_baseline",
        rotation_mode="anchor",
        clip_on=True,
        zorder=zorder,
    )


def _drawpolygoninphysical(
    x,
    y,
    linecolor="black",
    fillcolor=None,
    linewidth=0.5,
    hatch=None,
    alpha=1.0,
    zorder=1,
):
    if linecolor is None:
        linewidth = 0
    _ax.add_artist(
        patches.Polygon(
            list(zip(x, y)),
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
            linewidth=linewidth,
            hatch=hatch,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawrectangleinphysical(xmin, ymin, xmax, ymax, **kwargs):
    _drawpolygoninphysical([xmin, xmin, xmax, xmax], [ymin, ymax, ymax, ymin], **kwargs)


def _drawcompassinphysical(x, y, facing, color="black", alpha=1.0, zorder=1):
    _drawdotinphysical(
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
    _drawarrowinphysical(
        x,
        y,
        facing,
        size=0.5,
        dy=0,
        linecolor=color,
        fillcolor=color,
        linewidth=0.5,
        alpha=alpha,
        zorder=zorder,
    )
    _drawtextinphysical(
        x,
        y,
        facing,
        "N",
        size=14,
        dx=-0.15,
        dy=-0.05,
        color=color,
        alpha=alpha,
        zorder=zorder,
    )


################################################################################


def drawhex(x, y, **kwargs):
    _drawhexinphysical(*aphex.tophysical(x, y), **kwargs)


def drawcircle(x, y, **kwargs):
    _drawcircleinphysical(*aphex.tophysical(x, y), **kwargs)


def drawsquare(x, y, **kwargs):
    _drawsquareinphysical(*aphex.tophysical(x, y), **kwargs)


def drawhexlabel(x, y, label, dy=0.35, size=9, color="lightgrey", **kwargs):
    drawtext(x, y, 90, label, dy=dy, size=size, color=color, **kwargs)


def drawdot(x, y, **kwargs):
    _drawdotinphysical(*aphex.tophysical(x, y), **kwargs)


def drawlines(x, y, **kwargs):
    xy = [aphex.tophysical(xy[0], xy[1]) for xy in zip(x, y)]
    x = [xy[0] for xy in xy]
    y = [xy[1] for xy in xy]
    _drawlinesinphysical(x, y, **kwargs)


def drawarrow(x, y, facing, **kwargs):
    _drawarrowinphysical(*aphex.tophysical(x, y), facing, **kwargs)


def drawdoublearrow(x, y, facing, **kwargs):
    _drawdoublearrowinphysical(*aphex.tophysical(x, y), facing, **kwargs)


def drawdart(x, y, facing, **kwargs):
    _drawdartinphysical(*aphex.tophysical(x, y), facing, **kwargs)


def drawtext(x, y, facing, s, **kwargs):
    _drawtextinphysical(*aphex.tophysical(x, y), facing, s, **kwargs)


def drawpolygon(x, y, **kwargs):
    x, y = (aphex.tophysical(*xy) for xy in zip(x, y))
    _drawpolygoninphysical(x, y, **kwargs)


def drawrectangle(xmin, ymin, xmax, ymax, **kwargs):
    xmin, ymin = aphex.tophysical(xmin, ymin)
    xmax, ymax = aphex.tophysical(xmax, ymax)
    _drawrectangleinphysical(xmin, ymin, xmax, ymax, **kwargs)


def drawcompass(x, y, facing, **kwargs):
    _drawcompassinphysical(*aphex.tophysical(x, y), facing, **kwargs)


################################################################################

arccolor = (0.70, 0.70, 0.70)
arclinewidth = 2.0
arclinestyle = "dashed"


def drawarc(x0, y0, facing, arc):

    def drawdxdy(dxdy, reflect=False):

        # dxdy = [aphex.tophysical(dxdy[0], dxdy[1]) for dxdy in dxdy]

        x = [x0 + dxdy[0] * cosd(facing) - dxdy[1] * sind(facing) for dxdy in dxdy]
        y = [y0 + dxdy[0] * sind(facing) + dxdy[1] * cosd(facing) for dxdy in dxdy]
        _drawlinesinphysical(
            x,
            y,
            linecolor=arccolor,
            linewidth=arclinewidth,
            linestyle=arclinestyle,
            zorder=0,
        )

    x0, y0 = aphex.tophysical(x0, y0)

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
            dxdy = [aphex.tophysical(dxdy[0], dxdy[1]) for dxdy in dxdy]

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

            dxdy = [[0, 0], [100 * cosd(halfangle), 100 * sind(halfangle)]]

        drawdxdy(dxdy)

        if arc[0] == "L" or arc[0] == "R":
            drawdxdy([[0, 0], [+100, 0]])
        else:
            drawdxdy([[dxdy[0], -dxdy[1]] for dxdy in dxdy])


################################################################################

loscolor = (0.00, 0.00, 0.00)
loslinewidth = 1.0
loslinestyle = "solid"
losdotsize = 0.05


def drawlos(x0, y0, x1, y1):

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

pathcolor = (0.00, 0.00, 0.00)
pathlinewidth = 2.0
pathlinestyle = "dotted"
pathdotsize = 0.1
aircrafttextsize = 10
aircraftcounterlinewidth = 2
killedfillcolor = None
killedlinecolor = (0.60, 0.60, 0.60)
aircraftlinecolor = (0.00, 0.00, 0.00)
aircraftlinewidth = 1
textcolor = (0.00, 0.00, 0.00)


def _drawannotation(x, y, facing, position, text, zorder):
    textdx = 0.08
    textdy = 0.15
    if position[0] == "u":
        textdy = +textdy
    elif position[0] == "c":
        textdy = 0
    else:
        textdy = -textdy
    if position[1] == "l":
        alignment = "right"
        textdx = -textdx
    else:
        alignment = "left"
        textdx = +textdx
    drawtext(
        x,
        y,
        facing,
        text,
        dx=textdx,
        dy=textdy,
        size=aircrafttextsize,
        color=textcolor,
        alignment=alignment,
        zorder=zorder,
    )


def drawpath(x, y, facing, altitude, speed, color, killed, annotate):
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
            zorder=0.9,
        )
        zorder = altitude[0] + 1
        drawdot(
            x[0],
            y[0],
            fillcolor=fillcolor,
            linecolor=linecolor,
            linewidth=aircraftlinewidth,
            size=pathdotsize,
            zorder=zorder,
        )
        if annotate:
            _drawannotation(
                x[0], y[0], facing[0], "cl", "%d" % altitude[0], zorder=zorder
            )
            if speed is not None:
                _drawannotation(
                    x[0],
                    y[0],
                    facing[0],
                    "ll",
                    "%.1f" % speed,
                    zorder=zorder,
                )


def drawaircraft(x, y, facing, color, name, altitude, speed, flighttype, killed):
    if killed:
        fillcolor = killedfillcolor
        linecolor = killedlinecolor
    else:
        fillcolor = color
        linecolor = aircraftlinecolor
    zorder = altitude + 1
    if apvariants.withvariant("draw counters"):
        drawsquare(
            x,
            y,
            facing=facing,
            size=1,
            linecolor="black",
            linewidth=counterlinewidth,
            fillcolor=a._color,
            zorder=zorder,
        )
        drawdart(
            x,
            y,
            facing,
            size=0.4,
            fillcolor="black",
            linewidth=1,
            linecolor="black",
            zorder=zorder,
        )
    else:
        drawdart(
            x,
            y,
            facing,
            size=0.4,
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


def drawmissile(x, y, facing, color, name, altitude, speed, annotate):
    fillcolor = color
    linecolor = aircraftlinecolor
    zorder = altitude + 1
    if apvariants.withvariant("draw counters"):
        drawsquare(
            x,
            y,
            facing=facing,
            size=1,
            linecolor="black",
            linewidth=counterlinewidth,
            fillcolor=a._color,
            zorder=zorder,
        )
        drawarrow(
            x,
            y,
            facing,
            size=0.4,
            fillcolor="black",
            linewidth=1,
            linecolor="black",
            zorder=zorder,
        )
    else:
        drawdart(
            x,
            y,
            facing,
            size=0.2,
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

barragefirelinecolor = (0.5, 0.5, 0.5)
barragefirelinewidth = 2.0
barragefirelinestyle = "dotted"


def drawbarragefire(x, y, altitude):
    zorder = altitude + 1.5
    drawhex(
        x,
        y,
        size=2.0 + math.sqrt(3 / 4),
        rotation=30,
        linecolor=barragefirelinecolor,
        fillcolor=None,
        linestyle=barragefirelinestyle,
        linewidth=barragefirelinewidth,
        zorder=zorder,
    )


################################################################################

plottedfirelinecolor = (0.5, 0.5, 0.5)
plottedfirelinewidth = 2.0
plottedfirelinestyle = "dashed"


def drawplottedfire(x, y, altitude):
    zorder = altitude + 3.5
    drawhex(
        x,
        y,
        size=2.0 + math.sqrt(3 / 4),
        rotation=30,
        linecolor=plottedfirelinecolor,
        fillcolor=None,
        linestyle=plottedfirelinestyle,
        linewidth=plottedfirelinewidth,
        zorder=zorder,
    )


################################################################################

blastzonelinecolor = (0.5, 0.5, 0.5)
blastzonelinewidth = 2.0
blastzonelinestyle = "dotted"


def drawblastzone(x, y, altitude):
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


def drawbomb(x, y, altitude, facing):
    fillcolor = bombcolor
    linecolor = bomblinecolor
    zorder = altitude + 1.5
    drawdart(
        x,
        y,
        facing,
        size=0.2,
        fillcolor=fillcolor,
        linewidth=aircraftlinewidth,
        linecolor=linecolor,
        zorder=zorder,
    )


################################################################################

watermarkcolor = (0.70, 0.70, 0.70)


def drawwatermark(s, xmin, ymin, xmax, ymax):
    # The math below puts the text at the center of each megahex,
    dx = 5
    dy = 5
    for ix in range(int(xmin / dx), int(xmax / dx) + 1):
        for iy in range(int(ymin / dy), int(ymax / dy) + 1):
            x = ix * dx
            y = iy * dy
            if ix % 2 == 1:
                y += 0.5 * dy
            drawtext(x, y, 120, s, color=watermarkcolor, size=24)


################################################################################

compactstacks = True


def setcompactstacks(value):
    global compactstacks
    compactstacks = value


################################################################################

groundunitlinewidth = 1
groundunitdx = 0.6
groundunitdy = 0.4


def drawgroundunit(
    x, y, symbols, uppertext, lowertext, facing, color, name, stack, killed
):
    _drawgroundunitinphysical(
        *aphex.tophysical(x, y),
        symbols,
        uppertext,
        lowertext,
        facing,
        color,
        name,
        stack,
        killed
    )


def _drawgroundunitinphysical(
    x0, y0, symbols, uppertext, lowertext, facing, color, name, stack, killed
):

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

    if compactstacks:
        stackdx = 0.09
        stackdy = 0.07
        if stack == "1/2":
            x = x0 - 1.0 * stackdx
            y = y0 - 1.5 * stackdy
            zorder = 0.2
        elif stack == "2/2":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.5 * stackdy
            zorder = 0.1
        elif stack == "1/3":
            x = x0 + 1.0 * stackdx
            y = y0 - 1.5 * stackdy
            zorder = 0.3
        elif stack == "2/3":
            x = x0 - 1.0 * stackdx
            y = y0
            zorder = 0.2
        elif stack == "3/3":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.5 * stackdy
            zorder = 0.1
        elif stack == "1/4":
            x = x0 - 1.0 * stackdx
            y = y0 - 1.5 * stackdy
            zorder = 0.4
        elif stack == "2/4":
            x = x0 + 1.0 * stackdx
            y = y0 - 0.5 * stackdy
            zorder = 0.3
        elif stack == "3/4":
            x = x0 - 1.0 * stackdx
            y = y0 + 0.5 * stackdy
            zorder = 0.2
        elif stack == "4/4":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.5 * stackdy
            zorder = 0.1
        else:
            x = x0
            y = y0
            zorder = 0.1
    else:
        stackdx = 0.5 * groundunitdx + 0.03 * groundunitdx
        stackdy = 0.5 * groundunitdy + 0.03 * groundunitdx
        if stack == "1/2":
            x = x0 - 0.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.2
        elif stack == "2/2":
            x = x0 + 0.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.1
        elif stack == "1/3":
            x = x0 + 1.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.3
        elif stack == "2/3":
            x = x0 - 1.0 * stackdx
            y = y0
            zorder = 0.2
        elif stack == "3/3":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.1
        elif stack == "1/4":
            x = x0 - 1.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.4
        elif stack == "2/4":
            x = x0 + 1.0 * stackdx
            y = y0 - 1.0 * stackdy
            zorder = 0.3
        elif stack == "3/4":
            x = x0 - 1.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.2
        elif stack == "4/4":
            x = x0 + 1.0 * stackdx
            y = y0 + 1.0 * stackdy
            zorder = 0.1
        else:
            x = x0
            y = y0
            zorder = 0.1

    def drawinfantrysymbol():
        _drawlinesinphysical(
            [x - groundunitdx / 2, x + groundunitdx / 2],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesinphysical(
            [x - groundunitdx / 2, x + groundunitdx / 2],
            [y + groundunitdy / 2, y - groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawantiarmorsymbol():
        _drawlinesinphysical(
            [x - groundunitdx / 2, x],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesinphysical(
            [x + groundunitdx / 2, x],
            [y - groundunitdy / 2, y + groundunitdy / 2],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawreconnaissancesymbol():
        _drawlinesinphysical(
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
                return +fx * groundunitdx + fy * groundunitdy * cosd(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fx * groundunitdx + fy * groundunitdy * cosd(theta)

        def dy(theta):
            return fy * groundunitdy * sind(theta)

        _drawlinesinphysical(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawartillerysymbol():
        ry = 0.1
        _drawcircleinphysical(
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
            return x + groundunitdx / 2 * cosd(theta)

        def airdefencey(theta):
            return y - groundunitdy / 2 + fy * groundunitdy * sind(theta)

        _drawrectangleinphysical(
            x + groundunitdx * (-0.5),
            y + groundunitdy * (-0.5),
            x + groundunitdx * (+0.5),
            y + groundunitdy * (-0.5 + fy),
            linecolor=None,
            fillcolor=fillcolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

        _drawlinesinphysical(
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
            return ry * groundunitdy * cosd(theta)

        def dy(theta):
            return ry * groundunitdy * sind(theta)

        _drawlinesinphysical(
            list([x + dx(theta) for theta in theta]),
            list([y0 + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        dx = ry * groundunitdy * cosd(theta0)
        dy = ry * groundunitdy * sind(theta0)
        _drawlinesinphysical(
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
        _drawlinesinphysical(
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
            _drawlinesinphysical(
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
            return fx * groundunitdx * cosd(theta)

        def dy(theta):
            if theta == 0 or theta == 180:
                return fy0 * groundunitdy
            else:
                return fy1 * groundunitdy + fx * groundunitdx * (sind(theta) - 1)

        _drawlinesinphysical(
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
            return fx0 * groundunitdx * cosd(theta)

        def dy(theta):
            if theta == 0 or theta == 180:
                return -fy0 * groundunitdy
            else:
                return fy0 * groundunitdy + fx0 * groundunitdx * (sind(theta) - 1)

        _drawlinesinphysical(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesinphysical(
            [x - fx1 * groundunitdx, x + fx1 * groundunitdx],
            [y - fy0 * groundunitdy, y - fy0 * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawfuelsymbol():
        fx = 0.15
        fy0 = 0.20
        _drawlinesinphysical(
            [x, x, x - 0.5 * fx * groundunitdx, x + 0.5 * fx * groundunitdx, x],
            [
                y - fy0 * groundunitdy,
                y + fy0 * groundunitdy - fx * groundunitdx * cosd(30),
                y + fy0 * groundunitdy,
                y + fy0 * groundunitdy,
                y + fy0 * groundunitdy - fx * groundunitdx * cosd(30),
            ],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawordnancesymbol():
        ry0 = 0.20
        ry1 = 0.35
        for theta in range(45, 180, 90):
            dx = ry1 * groundunitdy * cosd(theta)
            dy = ry1 * groundunitdy * sind(theta)
            _drawlinesinphysical(
                [x - dx, x + dx],
                [y - dy, y + dy],
                linecolor=linecolor,
                linewidth=groundunitlinewidth,
                zorder=zorder,
            )
        _drawcircleinphysical(
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
        _drawlinesinphysical(
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
        _drawcircleinphysical(
            x - fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleinphysical(
            x,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleinphysical(
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
        _drawcircleinphysical(
            x - fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleinphysical(
            x + fx * groundunitdx,
            y - fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawsupplysymbol():
        fy = 0.25
        _drawlinesinphysical(
            [x - 0.5 * groundunitdx, x + 0.5 * groundunitdx],
            [y + (fy - 0.5) * groundunitdy, y + (fy - 0.5) * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawheadquarterssymbol():
        fy = 0.25
        _drawlinesinphysical(
            [x - 0.5 * groundunitdx, x + 0.5 * groundunitdx],
            [y + fy * groundunitdy, y + fy * groundunitdy],
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )

    def drawtransportationsymbol():
        ry = 0.25
        fy = 0.0
        _drawcircleinphysical(
            x,
            y + fy * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        for theta in range(0, 180, 45):
            dx = ry * groundunitdy * cosd(theta)
            dy = ry * groundunitdy * sind(theta)
            _drawlinesinphysical(
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
        _drawpolygoninphysical(
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
            return fx0 * groundunitdx * cosd(theta)

        def dy(theta):
            return fy0 * groundunitdy - fy1 * groundunitdy * sind(theta)

        _drawlinesinphysical(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesinphysical(
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
        _drawcircleinphysical(
            x - fx2 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleinphysical(
            x - fx1 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleinphysical(
            x + fx1 * groundunitdx,
            y - fy2 * groundunitdy,
            2 * ry * groundunitdy,
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawcircleinphysical(
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
            return fx0 * groundunitdx * cosd(theta)

        def dy(theta):
            return fy0 * groundunitdy - fy1 * groundunitdy * sind(theta)

        _drawlinesinphysical(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesinphysical(
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
        _drawlinesinphysical(
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
        _drawpolygoninphysical(
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
        _drawpolygoninphysical(
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
        _drawlinesinphysical(
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
        _drawlinesinphysical(
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
            return fx0 * groundunitdx * cosd(theta)

        def dy(theta):
            return fy0 * groundunitdy + fy1 * groundunitdy * sind(theta)

        _drawlinesinphysical(
            list([x + dx(theta) for theta in theta]),
            list([y + dy(theta) for theta in theta]),
            linecolor=linecolor,
            linewidth=groundunitlinewidth,
            zorder=zorder,
        )
        _drawlinesinphysical(
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
                return +fx * groundunitdx + fy * groundunitdy * cosd(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fx * groundunitdx + fy * groundunitdy * cosd(theta)

        def dy(theta):
            if theta < 90 or theta > 270:
                return +fy * groundunitdy * sind(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fy * groundunitdy * sind(theta)

        _drawpolygoninphysical(
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
                return +fy * groundunitdy * sind(theta)
            elif theta == 90 or theta == 270:
                return 0
            else:
                return -fy * groundunitdy * sind(theta)

        _drawpolygoninphysical(
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
        _drawtextinphysical(
            x,
            y,
            90,
            text,
            dx=0,
            dy=+groundunitdy * 0.32,
            size=7,
            color=linecolor,
            alignment="center",
            zorder=zorder,
        )

    def drawlowertext(text):
        _drawtextinphysical(
            x,
            y,
            90,
            text,
            dx=0,
            dy=-groundunitdy * 0.36,
            size=7,
            color=linecolor,
            alignment="center",
            zorder=zorder,
        )

    if facing is not None:
        _drawarrowinphysical(
            x0,
            y0,
            facing,
            0.7,
            dy=0.35,
            linewidth=1,
            linecolor=linecolor,
            zorder=0,
        )

    if "hex" not in symbols:
        _drawrectangleinphysical(
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

        _drawrectangleinphysical(
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
                _drawtextinphysical(
                    x,
                    y,
                    90,
                    name,
                    dx=groundunitdx / 2 - 0.05,
                    dy=-0.01,
                    size=aircrafttextsize,
                    color=textcolor,
                    alignment="left",
                    zorder=zorder,
                )
            else:
                _drawtextinphysical(
                    x,
                    y,
                    90,
                    name,
                    dx=-groundunitdx / 2 + 0.05,
                    dy=-0.01,
                    size=aircrafttextsize,
                    color=textcolor,
                    alignment="right",
                    zorder=zorder,
                )

    else:

        _drawhexinphysical(
            x,
            y,
            size=0.9,
            linewidth=groundunitlinewidth,
            fillcolor=None,
            linecolor=linecolor,
            zorder=0,
        )


################################################################################

# I determine colors from images using the Digital Color Meter on macOS. I use
# native RGB values. However, colors are often perceived to be darker when seen
# in small areas. To counter this, I lighten certain colors.


def _lighten(color, factor):
    return list([min(1.0, component * factor) for component in color])


_colors = {
    # This is a mapping from "aircraft color" to "CSS color".
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
    "aluminum": "css:lightgray",
    "aluminium": "aluminum",
    "unpainted": "aluminum",
    "white": "css:white",
    "black": "css:black",
    "darkblue": "css:midnightblue",
    "green": "olivedrab",
    "olivedrab": "css:olivedrab",
    "lightgreen": "lightolivedrab",
    "lightolivedrab": "#9fb670",
    "tan": "css:tan",
    "darktan": "#937e62",
    "sand": "#f0ead6",
    "darkgray": "css:slategray",
    "darkgrey": "darkgray",
    "lightgray": "css:silver",
    "lightgrey": "lightgray",
    # The blue of the IAF roundel.
    # https://en.wikipedia.org/wiki/General_Dynamics_F-16_Fighting_Falcon_variants#F-16I_Sufa
    # This blue is darker and more saturated that the NATO blue.
    "iafblue": _lighten((0 / 255, 138 / 255, 192 / 255), 1.4),
    # Pan-Arab colors.
    # https://en.wikipedia.org/wiki/Pan-Arab_colors
    # https://en.wikipedia.org/wiki/Pan-Arab_colors#/media/File:Flag_of_Hejaz_1917.svg
    # This red is darker and more saturated than the NATO red. This green is lighter and
    # more saturated than the standard green.
    "panarabred": _lighten((199 / 255, 18 / 255, 34 / 244), 1.4),
    "panarabgreen": _lighten((9 / 255, 111 / 255, 53 / 255), 1.4),
}


def _mapcolor(color):

    if not isinstance(color, str):
        return color
    elif color[0:4] == "css:":
        return color[4:]
    elif color in _colors:
        return _mapcolor(_colors[color])
    else:
        return color


################################################################################
