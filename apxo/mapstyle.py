################################################################################

_style = {}


def getstyle(style):
    if style in _style:
        return _style[style]
    else:
        return None


################################################################################

# The colors in the base style are bright red to make it clear when they are not
# overridden.

_basestyle = {
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
    return list((1 - f) + f * x for x in color)


def darken(color, f):
    return list(min(1, f * x) for x in color)


def equivalentgray(color):
    x = 0.30 * color[0] + 0.59 * color[1] + 0.11 * color[2]
    return [x, x, x]


################################################################################


def _setlandcolors(style, basecolor, dilution):
    level0color = lighten(basecolor, dilution[0])
    level1color = lighten(basecolor, dilution[1])
    level2color = lighten(basecolor, dilution[2])
    level3color = lighten(basecolor, dilution[3])
    level0ridgecolor = level1color
    level1ridgecolor = level2color
    level2ridgecolor = level3color
    style.update(
        {
            "level0color": level0color,
            "level1color": level1color,
            "level2color": level2color,
            "level3color": level3color,
            "level0ridgecolor": level0ridgecolor,
            "level1ridgecolor": level1ridgecolor,
            "level2ridgecolor": level2ridgecolor,
        }
    )


def _setwatercolors(style):
    watercolor = [0.77, 0.89, 0.95]
    # Darken the water to 100% of the grey value of level 0. Do not lighten it.
    level0color = style["level0color"]
    watergrayvalue = equivalentgray(watercolor)[0]
    targetgrayvalue = 1.00 * equivalentgray(level0color)[0]
    if watergrayvalue > targetgrayvalue:
        watercolor = darken(watercolor, targetgrayvalue / watergrayvalue)
    wateroutlinecolor = darken(watercolor, 0.80)
    style.update(
        {
            "watercolor": watercolor,
            "wateroutlinecolor": wateroutlinecolor,
        }
    )


def _setforestcolors(style, factor, alpha=0.5):
    forestcolor = darken([0.50, 0.65, 0.50], factor)
    forestalpha = alpha
    style.update(
        {
            "forestcolor": forestcolor,
            "forestalpha": forestalpha,
        }
    )


def _setgraybuiltcolors(style):
    level0color = style["level0color"]
    gray = equivalentgray(level0color)
    darkergray = darken(gray, 0.7)
    style.update(
        {
            "urbancolor": gray,
            "urbanoutlinecolor": darkergray,
            "roadcolor": gray,
            "roadoutlinecolor": darkergray,
            "dockcolor": gray,
            "dockoutlinecolor": darkergray,
        }
    )


def _setgrayhexcolors(style, allforest=False):
    level0color = style["level0color"]
    gray = equivalentgray(level0color)
    labelcolor = darken(gray, 0.7)
    if allforest:
        hexcolor = darken(gray, 0.7 * 0.7)
    else:
        hexcolor = darken(gray, 0.7)
    style.update(
        {
            "hexcolor": hexcolor,
            "hexalpha": 1.0,
            "labelcolor": labelcolor,
        }
    )


def _setwhitemegahexcolors(style, alpha):
    megahexcolor = [1.00, 1.00, 1.00]
    megahexalpha = alpha
    style.update(
        {
            "megahexcolor": megahexcolor,
            "megahexalpha": megahexalpha,
        }
    )


def _setgraymegahexcolors(style, alpha):
    megahexcolor = [0.00, 0.00, 0.00]
    megahexalpha = alpha
    style.update(
        {
            "megahexcolor": megahexcolor,
            "megahexalpha": megahexalpha,
        }
    )


def _setforest(style, value=True):
    style.update({"forest": value})
    if value == "all":
        _setgrayhexcolors(style, allforest=True)


def _setwilderness(style, value=True):
    style.update({"wilderness": value})


def _setwater(style, value=True):
    style.update({"water": value})


def _setmaxurbansize(style, value):
    style.update({"maxurbansize": value})


def _setsnowycolors(style):
    _setlandcolors(style, [0.85, 0.85, 0.85], [1 / 20, 1 / 2, 2 / 2, 3 / 2])
    watercolor = (0.83, 0.89, 0.95)
    style.update(
        {
            "watercolor": watercolor,
        }
    )
    if style["forest"] == "all":
        _setforestcolors(style, 1.0, 0.7)
        _setgraymegahexcolors(style, 0.04)
    else:
        _setgraymegahexcolors(style, 0.02)


def _setfrozencolors(style):
    level0color = style["level0color"]
    style.update(
        {
            "watercolor": level0color,
            "wateroutlinecolor": level0color,
        }
    )


def _setleveloffset(style, leveloffset):
    style.update(
        {
            "leveloffset": leveloffset,
        }
    )


def _setislands(style):
    style.update(
        {
            "water": "islands",
        }
    )


################################################################################

_thisstyle = _style["airstrike"] = _basestyle.copy()

# The Air Strike colors don't fit into the scheme of increasingly darker
# shades of the same color, so are hard-wired.
_thisstyle.update(
    {
        "level0color": [0.75, 0.85, 0.725],
        "level1color": [0.82, 0.75, 0.65],
        "level2color": [0.77, 0.65, 0.55],
        "level3color": [0.62, 0.52, 0.44],
    }
)
_thisstyle.update(
    {
        "level0ridgecolor": lighten([0.50, 0.70, 0.45], 4 / 6),
        "level1ridgecolor": _thisstyle["level2color"],
        "level2ridgecolor": _thisstyle["level3color"],
    }
)

_setforestcolors(_thisstyle, 0.8)
_setwatercolors(_thisstyle)
_setgraybuiltcolors(_thisstyle)
_setgrayhexcolors(_thisstyle)
_setwhitemegahexcolors(_thisstyle, 0.10)

################################################################################

_thisstyle = _style["airsuperiority"] = _style["airstrike"].copy()
_setwater(_thisstyle, "all")
watercolor = _thisstyle["watercolor"]
_thisstyle.update(
    {
        "watercolor": watercolor,
        "hexcolor": darken(watercolor, 0.7),
        "hexalpha": 1.0,
        "labelcolor": darken(watercolor, 0.7),
    }
)
_setwhitemegahexcolors(_thisstyle, 0.10)

################################################################################

_thisstyle = _style["temperate"] = _basestyle.copy()

_setlandcolors(_thisstyle, [0.50, 0.70, 0.45], [3 / 6, 4 / 6, 5 / 6, 6 / 6])
_setforestcolors(_thisstyle, 0.8)
_setwatercolors(_thisstyle)
_setgraybuiltcolors(_thisstyle)
_setgrayhexcolors(_thisstyle)
_setwhitemegahexcolors(_thisstyle, 0.10)

################################################################################

_thisstyle = _style["temperateforest"] = _style["temperate"].copy()
_setforest(_thisstyle, "all")
_setmaxurbansize(_thisstyle, 4)

################################################################################

_thisstyle = _style["tundra"] = _style["temperate"].copy()
_setforest(_thisstyle, False)
_setwilderness(_thisstyle)

################################################################################

_thisstyle = _style["borealforest"] = _style["temperate"].copy()
_setforest(_thisstyle, "all")
_setwilderness(_thisstyle)

################################################################################

_thisstyle = _style["water"] = _style["temperate"].copy()
_setwater(_thisstyle, "all")

################################################################################

_thisstyle = _style["tropical"] = _style["temperate"].copy()
_setlandcolors(_thisstyle, [0.50, 0.70, 0.45], [4 / 6, 5 / 6, 6 / 6, 7 / 6])
_setforestcolors(_thisstyle, 0.6)
_setwatercolors(_thisstyle)
_setgraybuiltcolors(_thisstyle)
_setgrayhexcolors(_thisstyle)
_setwhitemegahexcolors(_thisstyle, 0.08)

################################################################################

_thisstyle = _style["tropicalforest"] = _style["tropical"].copy()
_setforest(_thisstyle, "all")
_setmaxurbansize(_thisstyle, 4)

################################################################################

_thisstyle = _style["arid"] = _style["temperate"].copy()
_setlandcolors(_thisstyle, [0.80, 0.76, 0.64], [1 / 3, 2 / 3, 3 / 3, 4 / 3])
_setforestcolors(_thisstyle, 1.0)
_setwatercolors(_thisstyle)
_setgraybuiltcolors(_thisstyle)
_setgrayhexcolors(_thisstyle)
_setwhitemegahexcolors(_thisstyle, 0.22)
_setwater(_thisstyle, "arid")

################################################################################

_thisstyle = _style["desert"] = _style["arid"].copy()
_setwilderness(_thisstyle)
_setwater(_thisstyle, "desert")
_setforest(_thisstyle, False)

################################################################################

for style in list(_style.keys()):
    if style != "airsuperiority" and style != "airstrike":
        _thisstyle = _style["snowy" + style] = _style[style].copy()
        _setsnowycolors(_thisstyle)
        _thisstyle = _style["frozen" + style] = _style["snowy" + style].copy()
        _setfrozencolors(_thisstyle)

################################################################################

for style in list(_style.keys()):
    if style != "airsuperiority" and style != "airstrike":
        _thisstyle = _style[style + "hills"] = _style[style].copy()
        _setleveloffset(_thisstyle, -1)
        _thisstyle = _style[style + "plain"] = _style[style].copy()
        _setleveloffset(_thisstyle, -3)
        _thisstyle = _style[style + "islands"] = _style[style].copy()
        _setislands(_thisstyle)

################################################################################
