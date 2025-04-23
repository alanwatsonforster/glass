"""
The :mod:`hexcode` module handles conversions between hex codes and hex coordinates.

We distinguish hex *labels* and hex *codes*. Hex labels are the four-digit labels that appear on the map sheets. Hex codes, discussed in section, are a means to refer to a specific hex on the map.

Hex Labels
----------

The hexes in the map sheets are labeled XXYY, where XX is the column number and YY is the row number. Grammatically, a hex label XXYY can have XX and YY from 00 to 99. Within a map, the labels obey:

- The XX increases from left to right.
- The YY increases from up to down.
- In first-generation sheets, the YY in columns with XX even refers to hexes below those columns with XX odd.
- In second-generation sheets, the YY in columns with XX even refers to hexes above those columns with XX odd.

The complete hexes in the original first-generation sheets are labeled as follows:

- XX from 01 to 19.
- YY from 01 to 25 (XX odd) or 01 to 24 (XX even).
- The half-hexes along the bottom of the sheet have YY of 25.

The complete hexes in the second-generation sheets are labeled as follows:

- The A maps have XX from 11 to 29.
- The B maps have XX from 31 to 49.
- The C maps have XX from 51 to 69.
- The D maps have XX from 71 to 89.
- The 1 map sheets have YY from 01 to 15 (XX odd) or 02 to 15 (XX even). 
- The 2 map sheets have YY from 16 to 30 (XX odd) or 17 to 30 (XX even). 
- The 3 map sheets have YY from 31 to 45 (XX odd) or 32 to 45 (XX even). 
- The 4 map sheets have YY from 46 to 60 (XX odd) or 47 to 60 (XX even). 
- The 5 map sheets have YY from 61 to 75 (XX odd) or 62 to 75 (XX even). 
- The 6 map sheets have YY from 76 to 90 (XX odd) or 77 to 90 (XX even). 


Along the edges of the sheets are half hexes and in the corners are quarter hexes. 

In the original first-generation maps, the half hexes along the bottom of the sheet are labeled and have YY of 25. The other partial hexes have no labels.

In the original second-generation maps, the column of half hexes along the left edges is labeled with just YY, the column of half hexes along the right edge is labeled with just XX, the half hexes along the top edge have no labels, and the half hexes along the bottom edge are labeled XXYY. 

For example, in sheet A1:

- Along the top edge the complete hexes are labeled 1101, 1301, 1501, ..., 2901, and the half hexes are unlabeled but, extrapolating, they correspond to 1201, 1401, 1601, ..., 2801.
- Along the bottom edge of sheet A1 the complete hexes are labeled 1115, 1315, 1515, ..., 2916, and the half hexes are labeled 1216, 1416, 1616, ..., 2816.
- Along the left edge, the half hexes are unlabeled but, extrapolating, they correspond to 1002, 1003, 1004, ... 1015.
- Along the right edge, the half hexes are labeled only with the XX part, 30, but, extrapolating, they correspond to 3002, 3003, 3004, ..., 3015.
- Extrapolating, the quarter hexes in the corners correspond to 1001, 1016, 3001, and 3016.

When the sheets are arranged as follows::

  A1 B1 C1 D1
  A2 B2 C2 D2
  A3 B3 C3 D3
  A4 B4 C4 D4
  A5 B5 C5 D5
  A6 B6 C6 D6

the partial hexes and their labels line up to give a hex grid in which the hexes are labeled continuously with XX from 11 to 89 and YY from 01 to 90. If we notionally include the partial hexes and extrapolate the labels, the map is labeled continuously with XX from 10 to 90 and YY from 01 to 91. However, in many scenarios, the sheets are not arranged this way.

Hex Codes
---------

We use hex codes to refer to a specific hex or hex side in the map. (Formally, we use them to refer to hex centers or hex side centers, but we often drop the word center.)

Hex codes are different from hex labels. As we shall see below, there are certain ambiguities in hex labels that hex codes must resolve:

- All of the first-generation sheets share the same hex labels.
- The second-generation sheets can be arranged so that hex labels are duplicated. For example, if the sheets are arranged as follows::

    A1 B1
    A2 C1

  Then the hexes with apparent labels from 3002 to 3016 appear twice, once on the edge between sheets A1 and B1 and then once again on the edge between sheets A2 and C1. A similar ambiguity can occur with the 50YY and 70YY columns.

  Furthermore, if the maps are arranged like this::

    A1
    B1

  Then it is not clear if the hex labels of the form 30YY refer to those on the right side of sheet A1 or the left side of sheet B1. Again, similar ambiguities occur with the 50YY and 70YY columns.

  These two ambiguities are slightly different. The first one is an ambiguity of full hexes on the internal edges between sheets. The second is an ambiguity between partial hexes on the external edges of the sheets. Since an aircraft or other element in a partial hex on the edge of the map is considered to have left the map, these partial hexes are only relevant for specifying the hex edges that are within the map.

Therefore, we have chosen the following scheme for hex codes to resolve these ambiguities.
The hex code for a hex center is:

- The sheet name.
- A hyphen.
- The hex label.

For example, A-1211 refers to the hex with label 1211 in sheet A. 

The hex labels of the partial hexes on the edge of a sheet are obtained by extrapolating the pattern of the hex labels within the sheet.

Hexes on internal edges can have more than one hex code. For example, hexes in a vertical edge can be referred to with hex codes from the sheets to the left or right. The implementation accepts all on input, but on output gives the hex code for the sheet 

The hex code for a hex-side center is:

- The sheet name.
- A hyphen.
- The hex label of one of the hexes adjacent to the side.
- A slash.
- The hex label of one of the other hex adjacent to the side.

Both of the hex labels are determined using the pattern for the specified sheet. For example, C2-6028/6127 refers to the hex side between the hexes with labels 6028 and 6127 in sheet C2.

A hex side can potentially be coded in two ways, according to which of the two adjacent hexes is listed first. The implementation accepts both on input, but on output gives the hexes in numerical order.

API
---
"""

import glass.hex
import glass.map

import re

hexcodeforcenterre = re.compile(r"([A-Z]+[0-9]?)-([0-9][0-9][0-9][0-9])")
hexcodeforsidere = re.compile(
    r"([A-Z]+[0-9]?)-([0-9][0-9][0-9][0-9])/([0-9][0-9][0-9][0-9])"
)


def isvalidhexcodeforcenter(h):
    """
    Return True if h is grammatically a hex code that corresponds to a center.
    Otherwise return False.
    """

    return isinstance(h, str) and hexcodeforcenterre.fullmatch(h) is not None


def checkisvalidhexcodeforcenter(h):
    """
    Raise a RuntimeError exception if h is not a gramatically valid hex code that
    corresponds to a center.
    """

    if not isvalidhexcodeforcenter(h):
        raise RuntimeError("%r is not a valid hex code for a hex." % h)


def isvalidhexcodeforside(h):
    """
    Return True if h is grammatically a hex code that corresponds to an side.
    Otherwise return False.
    """

    return isinstance(h, str) and hexcodeforsidere.fullmatch(h) is not None


def checkvalidhexcodeforside(h):
    """
    Raise a RuntimeError exception if h is not a gramatically valid hex code that
    corresponds to an side.
    """

    if not isvalidhexcodeforside(h):
        raise RuntimeError("%r is not a valid hex code for an side." % h)


def isvalidhexcode(h):
    """
    Return True if h is a grammatically valid hex code. Otherwise return False.
    """

    return isvalidhexcodeforcenter(h) or isvalidhexcodeforside(h)


def checkisvalidhexcode(h):
    """
    Raise a RuntimeError exception if h is not a gramatically valid hex code.
    """

    if not isvalidhexcode(h):
        raise RuntimeError("%r is not a valid hex code." % h)


def yoffsetforoddx():
    """
    Return the offset in y for odd rows in x. This differs between GDW
    and TSOH sheets.
    """

    if glass.map.usingfirstgenerationsheets():
        return +0.5
    else:
        return -0.5


def fromxy(x, y, sheet=None):
    """
    Return the hex code corresponding to the hex coordinate (x, y), which must
    correspond to a center or an side. If a sheet is specified, the hex code is
    chosen from that sheet. Otherwise the normal rules are used for sides.
    """

    glass.hex.checkisvalid(x, y)

    if glass.hex.ishex(x, y):

        if sheet == None:
            sheet = glass.map.tosheet(x, y)
            if sheet == None:
                raise RuntimeError("position is not within the map.")

        x0, y0 = glass.map.sheetorigin(sheet)
        XX0, YY0 = _sheetorigin(sheet)
        XX = XX0 + (x - x0)
        YY = YY0 - (y - y0)
        if XX % 2 == 1:
            YY += yoffsetforoddx()

        return "%s-%02d%02d" % (sheet, XX, YY)

    else:

        x0, y0, x1, y1 = glass.hex.hexsidetohexes(x, y)

        if sheet == None:
            sheet0 = glass.map.tosheet(x0, y0)
            sheet1 = glass.map.tosheet(x1, y1)
            if sheet0 != None:
                sheet = sheet0
            elif sheet1 != None:
                sheet = sheet1
            else:
                raise RuntimeError("position is not within the map.")

        sheet0, label0 = _splithexcodeforcenter(fromxy(x0, y0, sheet=sheet))
        sheet1, label1 = _splithexcodeforcenter(fromxy(x1, y1, sheet=sheet))

        if label0 < label1:
            return "%s-%s/%s" % (sheet, label0, label1)
        else:
            return "%s-%s/%s" % (sheet, label1, label0)


def toxy(h):
    """
    Return the hex coordinate (x, y) corresponding to the hex code h.
    """

    checkisvalidhexcode(h)

    if isvalidhexcodeforcenter(h):

        sheet, label = _splithexcodeforcenter(h)
        XX, YY = _splitlabelforcenter(label)

        XX0, YY0 = _sheetorigin(sheet)
        x0, y0 = glass.map.sheetorigin(sheet)

        dx = XX - XX0
        dy = YY0 - YY
        if XX % 2 == 1:
            dy += yoffsetforoddx()

        return x0 + dx, y0 + dy

    else:

        sheet, label0, label1 = _splithexcodeforside(h)

        x0, y0 = toxy("%s-%s" % (sheet, label0))
        x1, y1 = toxy("%s-%s" % (sheet, label1))

        return 0.5 * (x0 + x1), 0.5 * (y0 + y1)


def tosheet(h):
    """
    Return the sheet corresponding to the hex code h.
    """

    checkisvalidhexcode(h)
    if isvalidhexcodeforcenter(h):
        sheet, label = _splithexcodeforcenter(h)
    else:
        sheet, label0, label1 = _splithexcodeforside(h)
    return sheet


def tolabel(h):
    """
    Return the label corresponding to the hex code h.
    """

    checkisvalidhexcode(h)
    if isvalidhexcodeforcenter(h):
        sheet, label = _splithexcodeforcenter(h)
        return label
    else:
        sheet, label0, label1 = _splithexcodeforside(h)
        return "%s/%s" % (label0, label1)


def _splitlabelforcenter(label):
    """
    Return the XX and YY components of a center label as integers.
    """

    n = int(label)
    XX = n // 100
    YY = n % 100
    return XX, YY


def _splithexcodeforcenter(h):
    """
    Return the sheet and label for the hexcode, which must correspond to a hex
    center.
    """

    assert isvalidhexcodeforcenter(h)

    m = hexcodeforcenterre.fullmatch(h)
    sheet = m[1]
    label = m[2]
    return sheet, label


def _splithexcodeforside(h):
    """
    Return the sheet and labels for the hexcode, which must correspond to a hex
    side.
    """

    assert isvalidhexcodeforside(h)

    m = hexcodeforsidere.fullmatch(h)
    sheet = m[1]
    label0 = m[2]
    label1 = m[3]
    return sheet, label0, label1


def _sheetorigin(sheet):
    """
    Return the hex code of the center of the lower left hex in the specified sheet.
    """

    if glass.map.usingfirstgenerationsheets():

        # The first-generation maps are all labeled identically.

        XX = 0
        YY = 25

    else:

        sheetletter = sheet[0]
        if sheetletter == "A":
            XX = 10
        elif sheetletter == "B":
            XX = 30
        elif sheetletter == "C":
            XX = 50
        elif sheetletter == "D":
            XX = 70
        else:
            raise RuntimeError("%r is not a valid sheet." % sheet)

        sheetnumber = sheet[1]
        if sheetnumber == "1":
            YY = 16
        elif sheetnumber == "2":
            YY = 31
        elif sheetnumber == "3":
            YY = 46
        elif sheetnumber == "4":
            YY = 61
        elif sheetnumber == "5":
            YY = 76
        elif sheetnumber == "6":
            YY = 91
        else:
            raise RuntimeError("%r is not a valid sheet." % sheet)

    return XX, YY
