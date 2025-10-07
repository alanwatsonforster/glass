"""
The :mod:`glass.color` module has procedures for translating between color
specifiers and the native representation of colors.

The native representation of a color is either:

- A list or tuple of length three with each element being a number and
  representing a luminance between 0 and 1. The order of the luminances is red,
  green, and blue.

- `None` indicating transparency.

A color specifier may be:

- The native representation of a color.

- The hex representation of the color. This is a string consisting of "#"
  followed by three two-digit hex numbers giving the RGB luminance components as
  numbers between 0 and 255.

- The name of a color. This is a string. Valid color names are defined in the
  color data file `color.json`.

"""

################################################################################

__all__ = ["nativecolor"]

################################################################################

import os
import re

import glass.jsonc

################################################################################

_colorsdict = {}

"""
A dictionary containing the colors. 

The keys are the color names as strings. 

The values are color specifiers.

"""

################################################################################

_hexre = re.compile("#[0-9a-fA-F]{6}")


def nativecolor(color):
    """
    Return the native color representation of a color specifier.

    :param color:
        A color specifier (a native representation, a hex representation, or a color name).
    :raises RuntimeError: If the color is not valid.
    :return:
        The native representation of the color specifier.
    """

    def ishexrepresentation(x):
        return isinstance(x, str) and _hexre.fullmatch(x) is not None

    def isluminancecomponent(x):
        return isinstance(x, int | float) and 0 <= x and x <= 1

    def isnumericrepresentation(x):
        return (
            isinstance(x, list | tuple)
            and len(x) == 3
            and isluminancecomponent(x[0])
            and isluminancecomponent(x[1])
            and isluminancecomponent(x[2])
        )

    if color is None:
        return color
    elif ishexrepresentation(color):
        r = int(color[1:3], 16) / 255
        g = int(color[3:5], 16) / 255
        b = int(color[5:7], 16) / 255
        return [r, g, b]
    elif isnumericrepresentation(color):
        return color
    elif color in _colorsdict:
        return nativecolor(_colorsdict[color])
    else:
        raise RuntimeError("invalid color specifier %r" % color)


################################################################################


def _loadcolors():
    """
    Load the colors from the colors data file.

    The color data file is `data/color.json`. It defines a mapping between
    color names and color specifiers.

    :raises RuntimeError: If the colors data file cannot be opened or read.
    :raises RuntimeError: If any of the colors are invalid.
    """

    global _colorsdict

    _colorsdict = {}

    path = os.path.join(os.path.dirname(__file__), "data", "color.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            _colorsdict.update(glass.jsonc.load(f))
    except PermissionError:
        raise RuntimeError('unable to open the color data file "%s".' % path)
    except glass.jsonc.JSONDecodeError as e:
        raise RuntimeError(
            'unable to read the color data file "%s": line %d: %s.'
            % (path, e.lineno, e.msg.lower())
        )

    # Make sure all colors are valid.
    for color in _colorsdict:
        nativecolor(color)


_loadcolors()


################################################################################

# This code simply prints the hex representation of all defined colors. It is
# used for testing and debugging.

if False:
    for color in _colorsdict:
        values = nativecolor(color)
        r = int(values[0] * 255 + 0.5)
        g = int(values[1] * 255 + 0.5)
        b = int(values[2] * 255 + 0.5)
        print('    "%s": "#%02x%02x%02x",' % (color, r, g, b))

################################################################################
