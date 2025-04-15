################################################################################

__all__ = [ "getstyle" ]

################################################################################

_style = {}

def getstyle(stylename):
    """
    Return the style object associated with the stylename argument.

    :param stylename: The stylename argument must be a string corresponding to a
        style. It can be "airstrike", "airsuperiority", or one of the following
        optionally prefixed by "snowy" or "frozen" and optionally suffixed by
        "hills", "plain", or "islands:  "water", "temperate", "temperateforest",
        "tundra", "borealforest", "tropical", "tropicalforest", "arid", and
        "desert".

    :return: The corresponding style object.
    """
    if stylename in _style:
        return _style[stylename]
    else:
        return None


################################################################################

# The colors in the base style are bright red to make it clear when they are not
# overridden.

basestyle = {
    "base": "land",
    "leveloffset": 0,
    "wilderness": False,
    "water": "fresh",
    "forest": True,
    "maxurbansize": 5,
    "hexcolor": (1, 0, 0),
    "hexalpha": 1.0,
    "megahexcolor": (1, 0, 0),
    "megahexalpha": 1.0,
    "labelcolor": (1, 0, 0),
    "level0color": (1, 0, 0),
    "level1color": (1, 0, 0),
    "level2color": (1, 0, 0),
    "level0ridgecolor": (1, 0, 0),
    "level1ridgecolor": (1, 0, 0),
    "level2ridgecolor": (1, 0, 0),
    "watercolor": (1, 0, 0),
    "wateroutlinecolor": (1, 0, 0),
    "urbancolor": (1, 0, 0),
    "urbanoutlinecolor": (1, 0, 0),
    "roadcolor": (1, 0, 0),
    "roadoutlinecolor": (1, 0, 0),
    "dockcolor": (1, 0, 0),
    "dockoutlinecolor": (1, 0, 0),
    "forestcolor": (1, 0, 0),
    "forestalpha": 1,
}


################################################################################

def lighten(color, f):
    """
    Return a lightened color.

    :param color: The color parameter is the original color. It must be a tuple
        or list of three floats.

    :param f: The f parameter is the mixing factor with white.

    :return: The lightened color that is (1-f) times white mixed with f times
        the original color.
    """
    return list((1 - f) + f * x for x in color)


def darken(color, f):
    """
    Return a darkened color.

    :param color: The color parameter is the original color. It must be a tuple
        or list of three floats.

    :param f: The f parameter is the mixing factor with black.

    :return: The darkened color that is (1-f) times black mixed with f times the
        original color.
    """
    return list(min(1, f * x) for x in color)


def equivalentgray(color):
    """
    Return the equivalent gray of a color.

    :param color: The color parameter is the original color. It must be a tuple
        or list of three floats.

    :return: The equivalent gray with the same luma as the original color, according to
    CCIR 601. See https://en.wikipedia.org/wiki/Luma_(video)
    """
    luma = 0.30 * color[0] + 0.59 * color[1] + 0.11 * color[2]
    return [luma, luma, luma]


################################################################################


def _withlandcolors(style, basecolor, f):
    level0color = lighten(basecolor, f[0])
    level1color = lighten(basecolor, f[1])
    level2color = lighten(basecolor, f[2])
    level3color = lighten(basecolor, f[3])
    level0ridgecolor = level1color
    level1ridgecolor = level2color
    level2ridgecolor = level3color
    return style | {
        "level0color": level0color,
        "level1color": level1color,
        "level2color": level2color,
        "level3color": level3color,
        "level0ridgecolor": level0ridgecolor,
        "level1ridgecolor": level1ridgecolor,
        "level2ridgecolor": level2ridgecolor,
    }


def _withwatercolors(style):
    watercolor = [0.77, 0.89, 0.95]
    # Darken the water to the grey value of level 0. Do not lighten it.
    watergrayvalue = equivalentgray(watercolor)[0]
    level0color = style["level0color"]
    level0grayvalue = 1.00 * equivalentgray(level0color)[0]
    if watergrayvalue > level0grayvalue:
        watercolor = darken(watercolor, level0grayvalue / watergrayvalue)
    wateroutlinecolor = darken(watercolor, 0.80)
    return style | {
        "watercolor": watercolor,
        "wateroutlinecolor": wateroutlinecolor,
    }


def _withforestcolors(style, factor, alpha=0.5):
    forestcolor = darken([0.50, 0.65, 0.50], factor)
    forestalpha = alpha
    return style | {
        "forestcolor": forestcolor,
        "forestalpha": forestalpha,
    }


def _withgraybuiltcolors(style):
    level0color = style["level0color"]
    gray = equivalentgray(level0color)
    darkergray = darken(gray, 0.7)
    return style | {
        "urbancolor": gray,
        "urbanoutlinecolor": darkergray,
        "roadcolor": gray,
        "roadoutlinecolor": darkergray,
        "dockcolor": gray,
        "dockoutlinecolor": darkergray,
    }


def _withgrayhexcolors(style, allforest=False):
    level0color = style["level0color"]
    gray = equivalentgray(level0color)
    labelcolor = darken(gray, 0.7)
    if allforest:
        hexcolor = darken(gray, 0.7 * 0.7)
    else:
        hexcolor = darken(gray, 0.7)
    return style | {
        "hexcolor": hexcolor,
        "hexalpha": 1.0,
        "labelcolor": labelcolor,
    }


def _withwhitemegahexcolors(style, alpha):
    megahexcolor = [1.00, 1.00, 1.00]
    megahexalpha = alpha
    return style | {
        "megahexcolor": megahexcolor,
        "megahexalpha": megahexalpha,
    }


def _withgraymegahexcolors(style, alpha):
    megahexcolor = [0.00, 0.00, 0.00]
    megahexalpha = alpha
    return style | {
        "megahexcolor": megahexcolor,
        "megahexalpha": megahexalpha,
    }


def _withforest(style, value=True):
    style = style | {
        "forest": value,
    }
    if value == "all":
        style = _withgrayhexcolors(style, allforest=True)
    return style


def _withwilderness(style, value=True):
    return style | {
        "wilderness": value,
    }


def _withwater(style, value=True):
    return style | {
        "water": value,
    }


def _withmaxurbansize(style, value):
    return style | {
        "maxurbansize": value,
    }


def _withsnowycolors(style):
    style = _withlandcolors(style, [0.85, 0.85, 0.85], [1 / 20, 1 / 2, 2 / 2, 3 / 2])
    watercolor = (0.83, 0.89, 0.95)
    style = style | {
        "watercolor": watercolor,
    }
    if style["forest"] == "all":
        style = _withforestcolors(style, 1.0, 0.7)
        style = _withgraymegahexcolors(style, 0.04)
    else:
        style = _withgraymegahexcolors(style, 0.02)
    return style


def _withfrozencolors(style):
    level0color = style["level0color"]
    return style | {
        "watercolor": level0color,
        "wateroutlinecolor": level0color,
    }


def _withleveloffset(style, leveloffset):
    return style | {
        "leveloffset": leveloffset,
    }


def _withislands(style):
    return style | {
        "water": "islands",
    }


################################################################################

style = basestyle

# The Air Strike land colors don't fit into the scheme of increasingly darker
# shades of the same color, so are hard-wired.

style = style | {
    "level0color": [0.75, 0.85, 0.725],
    "level1color": [0.82, 0.75, 0.65],
    "level2color": [0.77, 0.65, 0.55],
    "level3color": [0.62, 0.52, 0.44],
}
style = style | {
    "level0ridgecolor": lighten([0.50, 0.70, 0.45], 4 / 6),
    "level1ridgecolor": style["level2color"],
    "level2ridgecolor": style["level3color"],
}

style = _withforestcolors(style, 0.8)
style = _withwatercolors(style)
style = _withgraybuiltcolors(style)
style = _withgrayhexcolors(style)
style = _withwhitemegahexcolors(style, 0.10)

_style["airstrike"] = style

################################################################################


style = _style["airstrike"]
style = _withwater(style, "all")
watercolor = style["watercolor"]
style = style | {
    "watercolor": watercolor,
    "hexcolor": darken(watercolor, 0.7),
    "hexalpha": 1.0,
    "labelcolor": darken(watercolor, 0.7),
}
style = _withwhitemegahexcolors(style, 0.10)

_style["airsuperiority"] = style

################################################################################

style = basestyle

style = _withlandcolors(
    style, [0.50, 0.70, 0.45], [3 / 6, 4 / 6, 5 / 6, 6 / 6]
)
style = _withforestcolors(style, 0.8)
style = _withwatercolors(style)
style = _withgraybuiltcolors(style)
style = _withgrayhexcolors(style)
style = _withwhitemegahexcolors(style, 0.10)

_style["temperate"] = style

################################################################################

style = _style["temperate"]
style = _withforest(style, "all")
style = _withmaxurbansize(style, 4)

_style["temperateforest"] = style

################################################################################

style = _style["temperate"]
style = _withforest(style, False)
style = _withwilderness(style)

_style["tundra"] = style

################################################################################

style = _style["temperate"]
style = _withforest(style, "all")
style = _withwilderness(style)

_style["borealforest"] = style

################################################################################

style = _style["temperate"]
style = _withwater(style, "all")

_style["water"] = style

################################################################################

style = _style["temperate"]
style = _withlandcolors(
    style, [0.50, 0.70, 0.45], [4 / 6, 5 / 6, 6 / 6, 7 / 6]
)
style = _withforestcolors(style, 0.6)
style = _withwatercolors(style)
style = _withgraybuiltcolors(style)
style = _withgrayhexcolors(style)
style = _withwhitemegahexcolors(style, 0.08)

_style["tropical"] = style

################################################################################

style = _style["tropical"]
style = _withforest(style, "all")
style = _withmaxurbansize(style, 4)

_style["tropicalforest"] = style

################################################################################

style = _style["temperate"]
style = _withlandcolors(
    style, [0.80, 0.76, 0.64], [1 / 3, 2 / 3, 3 / 3, 4 / 3]
)
style = _withforestcolors(style, 1.0)
style = _withwatercolors(style)
style = _withgraybuiltcolors(style)
style = _withgrayhexcolors(style)
style = _withwhitemegahexcolors(style, 0.22)
style = _withwater(style, "arid")

_style["arid"] = style

################################################################################

style = _style["arid"]
style = _withwilderness(style)
style = _withwater(style, "desert")
style = _withforest(style, False)

_style["desert"] = style

################################################################################

for style in list(_style.keys()):
    if style != "airsuperiority" and style != "airstrike":
        _style["snowy" + style] = _withsnowycolors(_style[style])
        _style["frozen" + style] = _withfrozencolors(_style["snowy" + style])

################################################################################

for style in list(_style.keys()):
    if style != "airsuperiority" and style != "airstrike":
        _style[style + "hills"] = _withleveloffset(_style[style], -1)
        _style[style + "plain"] = _withleveloffset(_style[style], -3)
        _style[style + "islands"] = _withislands(_style[style])

################################################################################
