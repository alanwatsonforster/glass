"""
Conversion between hex codes and hex coordinates.
"""

import apxo.hex as aphex
import apxo.map as apmap

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

    if apmap.usingfirstgenerationsheets():
        return +0.5
    else:
        return -0.5


def fromxy(x, y, sheet=None):
    """
    Return the hex code corresponding to the hex coordinate (x, y), which must
    correspond to a center or an side. If a sheet is specified, the hex code is
    chosen from that sheet. Otherwise the normal rules are used for sides.
    """

    aphex.checkisvalid(x, y)

    if aphex.iscenter(x, y):

        if sheet == None:
            sheet = apmap.tosheet(x, y)
            if sheet == None:
                raise RuntimeError("position is not within the map.")

        x0, y0 = apmap.sheetorigin(sheet)
        XX0, YY0 = _sheetorigin(sheet)
        XX = XX0 + (x - x0)
        YY = YY0 - (y - y0)
        if XX % 2 == 1:
            YY += yoffsetforoddx()

        return "%s-%02d%02d" % (sheet, XX, YY)

    else:

        x0, y0, x1, y1 = aphex.sidetocenters(x, y)

        if sheet == None:
            sheet0 = apmap.tosheet(x0, y0)
            sheet1 = apmap.tosheet(x1, y1)
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
        x0, y0 = apmap.sheetorigin(sheet)

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

    if apmap.usingfirstgenerationsheets():

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
