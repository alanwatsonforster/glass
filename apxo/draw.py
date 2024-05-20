import math

import apxo.hex as aphex
import apxo.variants as apvariants

import pickle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
        figsize=[(xmax - xmin), (ymax - ymin)], frameon=False, dpi=dotsperhex
    )
    plt.axis("off")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    _ax = plt.gca()
    _ax.set_position([0, 0, 1, 1])
    _ax.add_artist(
        patches.Polygon(
            [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]],
            edgecolor=None,
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
    _fig.show()


def writefile(name):
    _fig.savefig(name)


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
    hatch=None,
    alpha=1.0,
    zorder=1,
):
    # size is inscribed diameter
    _ax.add_artist(
        patches.RegularPolygon(
            [x, y],
            6,
            radius=size * 0.5 * math.sqrt(4 / 3),
            orientation=math.pi / 6,
            edgecolor=_mapcolor(linecolor),
            facecolor=_mapcolor(fillcolor),
            fill=(fillcolor != None),
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
    x = x + dx * sind(facing) + dy * cosd(facing)
    y = y - dx * cosd(facing) + dy * sind(facing)
    _ax.add_artist(
        patches.Circle(
            [x, y],
            radius=0.5 * size,
            facecolor=_mapcolor(fillcolor),
            edgecolor=_mapcolor(linecolor),
            linewidth=linewidth,
            alpha=alpha,
            zorder=zorder,
        )
    )


def _drawlinesinphysical(
    x,
    y,
    color="black",
    linewidth=0.5,
    linestyle="solid",
    joinstyle="miter",
    capstyle="butt",
    alpha=1.0,
    zorder=1,
):
    plt.plot(
        x,
        y,
        linewidth=linewidth,
        linestyle=linestyle,
        color=_mapcolor(color),
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
        verticalalignment="center",
        rotation_mode="anchor",
        clip_on=True,
        zorder=zorder,
    )


def _drawpolygoninphysical(
    xy,
    linecolor="black",
    fillcolor=None,
    linewidth=0.5,
    hatch=None,
    alpha=1.0,
    zorder=1,
):
    _ax.add_artist(
        patches.Polygon(
            xy,
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
    _drawpolygoninphysical(
        [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]], **kwargs
    )


def _drawcompassinphysical(x, y, facing, color="black", alpha=1.0, zorder=1):
    _drawdotinphysical(
        x,
        y,
        facing=facing,
        size=0.07,
        dy=-0.3,
        linecolor=None,
        fillcolor=color,
        alpha=alpha,
        zorder=zorder,
    )
    _drawarrowinphysical(
        x,
        y,
        facing,
        size=0.6,
        dy=0,
        linecolor=color,
        fillcolor=color,
        linewidth=1,
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


def drawpolygon(xy, **kwargs):
    _drawpolygoninphysical([aphex.tophysical(*xy) for xy in xy], **kwargs)


def drawrectangle(xmin, ymin, xmax, ymax, **kwargs):
    xmin, ymin = aphex.tophysical(xmin, ymin)
    xmax, ymax = aphex.tophysical(xmax, ymax)
    _drawrectangleinphysical(xmin, ymin, xmax, ymax, **kwargs)


def drawcompass(x, y, facing, **kwargs):
    _drawcompassinphysical(*aphex.tophysical(x, y), facing, **kwargs)


################################################################################

arccolor = (0.00, 0.00, 0.00)
arclinewidth = 1.0
arclinestyle = "dashed"


def drawarc(x0, y0, facing, arc):

    def drawdxdy(dxdy, reflect=False):

        # dxdy = [aphex.tophysical(dxdy[0], dxdy[1]) for dxdy in dxdy]

        x = [x0 + dxdy[0] * cosd(facing) - dxdy[1] * sind(facing) for dxdy in dxdy]
        y = [y0 + dxdy[0] * sind(facing) + dxdy[1] * cosd(facing) for dxdy in dxdy]
        _drawlinesinphysical(
            x, y, color=arccolor, linewidth=arclinewidth, linestyle=arclinestyle
        )

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

    x0, y0 = aphex.tophysical(x0, y0)

    drawdxdy(dxdy)

    if arc[0] != "L" and arc[0] != "R":
        drawdxdy([[dxdy[0], -dxdy[1]] for dxdy in dxdy])

    if arc[-1] == "+":
        drawdxdy([[0, 0], [+100, 0]])
    elif arc[-1] == "-":
        drawdxdy([[0, 0], [-100, 0]])


################################################################################

pathcolor = (0.00, 0.00, 0.00)
pathlinewidth = 2.0
pathlinestyle = "dotted"
pathdotsize = 0.1
aircrafttextsize = 10
aircraftcounterlinewidth = 2
aircraftdestroyedfillcolor = (0.50, 0.50, 0.50)
aircraftdestroyedlinecolor = (0.50, 0.50, 0.50)
aircraftlinecolor = (0.00, 0.00, 0.00)
aircraftlinewidth = 1
textcolor = (0.00, 0.00, 0.00)


def drawpath(x, y, facing, altitude, color, annotate=True):
    if color is None:
        fillcolor = aircraftdestroyedfillcolor
    else:
        fillcolor = color
    if len(x) > 1:
        drawlines(
            x,
            y,
            color=pathcolor,
            linewidth=pathlinewidth,
            linestyle=pathlinestyle,
            zorder=0,
        )
        zorder = altitude[0]
        drawdot(
            x[0],
            y[0],
            fillcolor=fillcolor,
            linecolor=pathcolor,
            linewidth=aircraftlinewidth,
            size=pathdotsize,
            zorder=zorder,
        )
        if annotate:
            drawtext(
                x[0],
                y[0],
                facing[0],
                "%02d" % altitude[0],
                dx=-0.08,
                dy=0.0,
                size=aircrafttextsize,
                color=textcolor,
                alignment="right",
                zorder=zorder,
            )


def drawaircraft(x, y, facing, color, name, altitude, speed, flighttype):
    zorder = altitude + 1
    if color is None:
        fillcolor = aircraftdestroyedfillcolor
        linecolor = aircraftdestroyedlinecolor
        nametext = ""
        altitudetext = ""
        speedtext = ""
        flighttypetext = ""
    else:
        fillcolor = color
        linecolor = aircraftlinecolor
        nametext = name
        altitudetext = "%2d" % altitude
        speedtext = "%.1f" % speed
        flighttypetext = flighttype[:2]
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
        textdx = 0.08
        textdy = 0.15
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
        drawtext(
            x,
            y,
            facing,
            nametext,
            dx=+textdx,
            dy=0,
            size=aircrafttextsize,
            color=textcolor,
            alignment="left",
            zorder=zorder,
        )
        drawtext(
            x,
            y,
            facing,
            flighttypetext,
            dx=-textdx,
            dy=+textdy,
            size=aircrafttextsize,
            color=textcolor,
            alignment="right",
            zorder=zorder,
        )
        drawtext(
            x,
            y,
            facing,
            altitudetext,
            dx=-textdx,
            dy=0,
            size=aircrafttextsize,
            color=textcolor,
            alignment="right",
            zorder=zorder,
        )
        drawtext(
            x,
            y,
            facing,
            speedtext,
            dx=-textdx,
            dy=-textdy,
            size=aircrafttextsize,
            color=textcolor,
            alignment="right",
            zorder=zorder,
        )


def drawmissile(x, y, facing, color, name, altitude, speed):
    zorder = altitude + 1
    if color is None:
        fillcolor = aircraftdestroyedfillcolor
        linecolor = aircraftdestroyedlinecolor
        altitudetext = ""
    else:
        fillcolor = color
        linecolor = aircraftlinecolor
        altitudetext = "%2d" % altitude
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
        textdx = 0.08
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
        drawtext(
            x,
            y,
            facing,
            name,
            dx=+textdx,
            dy=0,
            size=aircrafttextsize,
            color=textcolor,
            alignment="left",
            zorder=zorder,
        )
        drawtext(
            x,
            y,
            facing,
            altitudetext,
            dx=-textdx,
            dy=0,
            size=aircrafttextsize,
            color=textcolor,
            alignment="right",
            zorder=zorder,
        )


def drawgroundunit(x, y, type, color, name):
    zorder = 0
    if color is None:
        fillcolor = aircraftdestroyedfillcolor
        linecolor = aircraftdestroyedlinecolor
        nametext = ""
    else:
        fillcolor = color
        linecolor = aircraftlinecolor
        nametext = name
    textdx = 0.0
    textdy = 0.0
    drawsquare(
        x,
        y,
        facing=45,
        size=0.7,
        linecolor="black",
        linewidth=2,
        fillcolor=color,
        zorder=zorder,
    )
    drawtext(
        x,
        y,
        90,
        nametext,
        dx=+textdx,
        dy=0,
        size=aircrafttextsize,
        color=textcolor,
        alignment="center",
        zorder=zorder,
    )


################################################################################

# I determine colors from images using the Digital Color Meter on macOS. I use
# native RGB values. However, colors are often percieved to be darker when seen
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
    "green": "css:olivedrab",
    "tan": "css:tan",
    "sand": "css:blanchedalmond",
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
