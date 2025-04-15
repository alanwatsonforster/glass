################################################################################

__all__ = ["getstyle"]

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

# Colors are represented as lists of three RGB components from 0 to 1.

white = [1.0, 1.0, 1.0]
black = [0.0, 0.0, 0.0]
red = [1.0, 0.0, 0.0]

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
    "hexcolor": red,
    "hexalpha": 1.0,
    "megahexcolor": red,
    "megahexalpha": 1.0,
    "labelcolor": red,
    "level0color": red,
    "level1color": red,
    "level2color": red,
    "level0ridgecolor": red,
    "level1ridgecolor": red,
    "level2ridgecolor": red,
    "watercolor": red,
    "wateroutlinecolor": red,
    "urbancolor": red,
    "urbanoutlinecolor": red,
    "roadcolor": red,
    "roadoutlinecolor": red,
    "dockcolor": red,
    "dockoutlinecolor": red,
    "forestcolor": red,
    "forestalpha": 1.0,
}

################################################################################


def lighten(color, factor):
    """
    Return a lightened color.

    :param color: The color parameter is the original color.

    :param f: The factor parameter is the mixing factor with white.

    :return: The lightened color that is (1-factor) times white mixed with
        factor times the original color.
    """
    return list(min(1, (1.0 - factor) * 1.0 + factor * component) for component in color)


def darken(color, factor):
    """
    Return a darkened color.

    :param color: The color parameter is the original color.

    :param f: The factor parameter is the mixing factor with black.

    :return: The darkened color that is (1-factor) times black mixed with factor
        times the original color.
    """
    return list(min(1, (1.0 - factor) * 0.0 + factor * component) for component in color)


def equivalentgray(color):
    """
    Return the equivalent gray of a color.

    :param color: The color parameter is the original color.

    :return: The equivalent gray with the same luma as the original color, according to
    CCIR 601. See https://en.wikipedia.org/wiki/Luma_(video)
    """
    luma = 0.30 * color[0] + 0.59 * color[1] + 0.11 * color[2]
    return [luma, luma, luma]


################################################################################


def withlandcolors(style, basecolor, factor):
    """Return a new style with new land colors."""
    level0color = lighten(basecolor, factor[0])
    level1color = lighten(basecolor, factor[1])
    level2color = lighten(basecolor, factor[2])
    level3color = lighten(basecolor, factor[3])
    return style | {
        "level0color": level0color,
        "level1color": level1color,
        "level2color": level2color,
        "level3color": level3color,
        "level0ridgecolor": level1color,
        "level1ridgecolor": level2color,
        "level2ridgecolor": level3color,
    }


def withwatercolors(style):
    """Return a new style with new water colors."""
    watercolor = [0.77, 0.89, 0.95]
    # Darken the water to the grey value of level 0. Do not lighten it.
    watergrayvalue = equivalentgray(watercolor)[0]
    level0color = style["level0color"]
    level0grayvalue = equivalentgray(level0color)[0]
    if watergrayvalue > level0grayvalue:
        watercolor = darken(watercolor, level0grayvalue / watergrayvalue)
    wateroutlinecolor = darken(watercolor, 0.80)
    return style | {
        "watercolor": watercolor,
        "wateroutlinecolor": wateroutlinecolor,
    }


def withforestcolors(style, factor, alpha=0.5):
    """Return a new style with new forest colors."""
    forestcolor = darken([0.50, 0.65, 0.50], factor)
    forestalpha = alpha
    return style | {
        "forestcolor": forestcolor,
        "forestalpha": forestalpha,
    }


def withgraybuiltcolors(style):
    """Return a new style with new built terrain colors."""
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


def withgrayhexcolors(style, allforest=False):
    """Return a new style with new gray hex colors."""
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


def withwhitemegahexcolors(style, alpha):
    """Return a new style with new white mega-hex colors."""
    megahexcolor = white
    megahexalpha = alpha
    return style | {
        "megahexcolor": megahexcolor,
        "megahexalpha": megahexalpha,
    }


def withgraymegahexcolors(style, alpha):
    """Return a new style with new gray mega-hex colors."""
    megahexcolor = black
    megahexalpha = alpha
    return style | {
        "megahexcolor": megahexcolor,
        "megahexalpha": megahexalpha,
    }


def withforest(style, value=True):
    """Return a new style with a new forest value."""
    assert value in [True, False, "all"]
    style = style | {
        "forest": value,
    }
    if value == "all":
        style = withgrayhexcolors(style, allforest=True)
    return style


def withwilderness(style, value=True):
    """Return a new style with a new wilderness value."""
    assert value in [True, False]
    return style | {
        "wilderness": value,
    }


def withwater(style, value=True):
    """Return a new style with a new water value."""
    assert value in [True, False, "all", "arid", "desert"]
    return style | {
        "water": value,
    }


def withmaxurbansize(style, value):
    """Return a new style with a new maxurbansize value."""
    assert value in [0, 1, 2, 3, 4, 5]
    return style | {
        "maxurbansize": value,
    }


def withsnowycolors(style):
    """Return a new style with a snowy land and water colors."""
    style = withlandcolors(style, [0.85, 0.85, 0.85], [1 / 20, 1 / 2, 2 / 2, 3 / 2])
    watercolor = (0.83, 0.89, 0.95)
    style = style | {
        "watercolor": watercolor,
    }
    if style["forest"] == "all":
        style = withforestcolors(style, 1.0, 0.7)
        style = withgraymegahexcolors(style, 0.04)
    else:
        style = withgraymegahexcolors(style, 0.02)
    return style


def withfrozencolors(style):
    """Return a new style with a frozen water colors."""
    level0color = style["level0color"]
    return style | {
        "watercolor": level0color,
        "wateroutlinecolor": level0color,
    }


def withleveloffset(style, value):
    """Return a new style with a level offset."""
    assert value in [0, -1, -2, -3]
    return style | {
        "leveloffset": value,
    }


def withislands(style):
    """Return a new style with islands."""
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

style = withforestcolors(style, 0.8)
style = withwatercolors(style)
style = withgraybuiltcolors(style)
style = withgrayhexcolors(style)
style = withwhitemegahexcolors(style, 0.10)

_style["airstrike"] = style

################################################################################

style = _style["airstrike"]
style = withwater(style, "all")
watercolor = style["watercolor"]
style = style | {
    "watercolor": watercolor,
    "hexcolor": darken(watercolor, 0.7),
    "hexalpha": 1.0,
    "labelcolor": darken(watercolor, 0.7),
}
style = withwhitemegahexcolors(style, 0.10)

_style["airsuperiority"] = style

################################################################################

style = basestyle

style = withlandcolors(style, [0.50, 0.70, 0.45], [3 / 6, 4 / 6, 5 / 6, 6 / 6])
style = withforestcolors(style, 0.8)
style = withwatercolors(style)
style = withgraybuiltcolors(style)
style = withgrayhexcolors(style)
style = withwhitemegahexcolors(style, 0.10)

_style["temperate"] = style

################################################################################

style = _style["temperate"]
style = withforest(style, "all")
style = withmaxurbansize(style, 4)

_style["temperateforest"] = style

################################################################################

style = _style["temperate"]
style = withforest(style, False)
style = withwilderness(style)

_style["tundra"] = style

################################################################################

style = _style["temperate"]
style = withforest(style, "all")
style = withwilderness(style)

_style["borealforest"] = style

################################################################################

style = _style["temperate"]
style = withwater(style, "all")

_style["water"] = style

################################################################################

style = _style["temperate"]
style = withlandcolors(style, [0.50, 0.70, 0.45], [4 / 6, 5 / 6, 6 / 6, 7 / 6])
style = withforestcolors(style, 0.6)
style = withwatercolors(style)
style = withgraybuiltcolors(style)
style = withgrayhexcolors(style)
style = withwhitemegahexcolors(style, 0.08)

_style["tropical"] = style

################################################################################

style = _style["tropical"]
style = withforest(style, "all")
style = withmaxurbansize(style, 4)

_style["tropicalforest"] = style

################################################################################

style = _style["temperate"]
style = withlandcolors(style, [0.80, 0.76, 0.64], [1 / 3, 2 / 3, 3 / 3, 4 / 3])
style = withforestcolors(style, 1.0)
style = withwatercolors(style)
style = withgraybuiltcolors(style)
style = withgrayhexcolors(style)
style = withwhitemegahexcolors(style, 0.22)
style = withwater(style, "arid")

_style["arid"] = style

################################################################################

style = _style["arid"]
style = withwilderness(style)
style = withwater(style, "desert")
style = withforest(style, False)

_style["desert"] = style

################################################################################

for style in list(_style.keys()):
    if style != "airsuperiority" and style != "airstrike":
        _style["snowy" + style] = withsnowycolors(_style[style])
        _style["frozen" + style] = withfrozencolors(_style["snowy" + style])

################################################################################

for style in list(_style.keys()):
    if style != "airsuperiority" and style != "airstrike":
        _style[style + "hills"] = withleveloffset(_style[style], -1)
        _style[style + "plain"] = withleveloffset(_style[style], -3)
        _style[style + "islands"] = withislands(_style[style])

################################################################################
