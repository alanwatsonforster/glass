"""
Conversion between hex codes and hex coordinates.
"""

import airpower.hex as aphex
import airpower.map as apmap

def isvalidhexcodeforcenter(h):

  """
  Return True if h is grammatically a hex code for a center. 
  Otherwise return False.
  """

  if isinstance(h, int) and _inrange(h):
    return True

  if isinstance(h, float) and h % 1.0 == 0.0 and _inrange(h):
    return True

  if isinstance(h, str) and h.isdecimal() and _inrange(int(h)):
    return True

  return False

def checkisvalidhexcodeforcenter(h):

  """
  Raise a RuntimeError exception if h is not a gramatically valid hex code for
  a center.
  """

  if not isvalidhexcodeforcenter(h):
    raise RuntimeError("%r is not a valid hex code for a center." % h)

def isvalidhexcodeforedge(h):

  """
  Return True if h is grammatically a hex code for an edge. Otherwise return 
  False.
  """

  if not isinstance(h, str):
    return False

  m = h.split("/")
  if len(m) != 2:
    return False

  if not m[0].isdecimal() or not _inrange(int(m[0])):
    return False

  if not m[1].isdecimal() or not _inrange(int(m[1])):
    return False

  return True

def checkvalidhexcodeforedge(h):

  """
  Raise a RuntimeError exception if h is not a gramatically valid hex code for
  an edge.
  """

  if not isvalidhexcodeforedge(h):
    raise RuntimeError("%r is not a valid hex code for an edge." % h)

def isvalidhexcode(h):

  """
  Return True if h is a grammatically valid hex code. Otherwise return False.
  """

  return isvalidhexcodeforcenter(h) or isvalidhexcodeforedge(h)

def checkisvalidhexcode(h):

  """
  Raise a RuntimeError exception if h is not a gramatically valid hex code.
  """

  if not isvalidhexcode(h):
    raise RuntimeError("%r is not a valid hex code." % h)

def fromxy(x, y, sheet=None):

  """
  Return the hex code corresponding to the hex coordinate (x, y), which must
  correspond to a center or an edge. If a sheet is specified, the hex code is 
  chosen from that sheet. Otherwise the normal rules are used for edges.
  """

  aphex.checkisvalid(x, y)

  if aphex.iscenter(x, y):

    if sheet == None:
      sheet = apmap.tosheet(x, y)
      # Check the upper right edge.
      if sheet == None:
        sheet = apmap.tosheet(x - 0.50, y + 0.25)
      if sheet == None:
        raise RuntimeError("position is not within the map.")

    x0, y0 = apmap.sheetorigin(sheet)
    XX0, YY0 = _split(_sheetorigin(sheet))
    XX = XX0 + (x - x0)
    YY = YY0 - (y - y0)
    if XX % 2 == 1:
      YY -= 0.5

    return _join(XX, YY)

  else:

    x0, y0, x1, y1 = aphex.edgetocenters(x, y)

    if sheet == None:
      sheet0 = apmap.tosheet(x0, y0)
      sheet1 = apmap.tosheet(x1, y1)
      if sheet0 != None:
        sheet = sheet0
      elif sheet1 != None:
        sheet = sheet1
      else:
        raise RuntimeError("position is not within the map.")

    h0 = fromxy(x0, y0, sheet=sheet)
    h1 = fromxy(x1, y1, sheet=sheet)

    if h0 < h1:
      return "%04d/%04d" % (h0, h1)
    else:
      return "%04d/%04d" % (h1, h0)      

def toxy(h, sheet=None):

  """
  Return the hex coordinate (x, y) corresponding to the hex code h.
  """

  checkisvalidhexcode(h)

  if isvalidhexcodeforcenter(h):

    XX, YY = _split(h)

    if sheet == None:
      sheet = _tosheet(h, includerightedge=True, includebottomedge=True)
      if sheet == None:
        raise RuntimeError("hex code %r is not within the map." % h)

    XX0, YY0 = _split(_sheetorigin(sheet))
    x0, y0 = apmap.sheetorigin(sheet)

    dx = XX - XX0
    dy = YY0 - YY
    if XX % 2 == 1:
      dy -= 0.5
    
    return x0 + dx, y0 + dy

  else:

    m = h.split("/")
    h0 = m[0]
    h1 = m[1]

    if sheet == None:
      sheet0 = _tosheet(h0)
      sheet1 = _tosheet(h1)
      if sheet0 == None:
        sheet0 = sheet1
      elif sheet1 == None:
        sheet1 = sheet0

    x0, y0 = toxy(h0, sheet=sheet0)
    x1, y1 = toxy(h1, sheet=sheet1)

    return 0.5 * (x0 + x1), 0.5 * (y0 + y1)

def _split(h):

  """ 
  Split the hex code h of the form XXYY and return XX and YY as integers.
  """

  assert isvalidhexcodeforcenter(h)

  h = int(h)
  XX = h // 100
  YY = h % 100
  return XX, YY

def _join(XX, YY):

  """
  Return the hex code XXYY corresponding to the integers XX and YY.
  """

  assert 00 <= XX and XX <= 99 and XX % 1 == 0
  assert 00 <= YY and YY <= 99 and YY % 1 == 0

  return int(100 * XX + YY)

def _inrange(h):

  """
  Return True if h is within the range of valid hex codes of the form XXYY. 
  Otherwise return False.
  """

  return 0 <= h and h <= 9999

def _sheetorigin(sheet):

  """
  Return the hex code of the center of the lower left hex in the specified sheet.
  """

  sheetletter = sheet[0]
  if sheetletter == "A":
    XX = 10
  elif sheetletter == "B":
    XX = 30
  elif sheetletter == "C":
    XX = 50
  else:
    raise RuntimeError("%r is not a valid sheet." % sheet)

  sheetnumber = sheet[1]
  if sheetnumber == "1":
    YY = 16
  elif sheetnumber == "2":
    YY = 31
  else:
    raise RuntimeError("%r is not a valid sheet." % sheet)

  return _join(XX, YY)

def _tosheet(h, 
  includerightedge=False, includeleftedge=False,
  includebottomedge=False, includetopedge=False
  ):

  """
  Returns the sheet containing the hex code h, which must refer to a center.
  Hexes on the edges are excluded unless explicity includeded by the keyword
  arguments.
  """

  assert isvalidhexcodeforcenter(h)

  XX, YY = _split(h)

  if includerightedge:
    dXXleft = -1
  else:
    dXXleft = 0
  if includeleftedge:
    dXXright = +1
  else:
    dXXright = 0

  if 11 + dXXleft <= XX and XX <= 29 + dXXright:
    sheetletter = "A"
  elif 31 + dXXleft <= XX and XX <= 49 + dXXright:
    sheetletter = "B"
  elif 51 + dXXleft <= XX and XX <= 69 + dXXright:
    sheetletter = "C"
  else:
    return None

  if includetopedge:
    dYYtop = -1
  else:
    dYYtop = 0
  if includebottomedge:
    dYYbottom = 0
  else:
    dYYbottom = +1
    
  if XX % 2 == 1 and 1 <= YY and YY <= 15:
    sheetnumber = "1"
  elif XX % 2 == 0 and 2 + dYYtop <= YY and YY <= 15 + dYYbottom:
    sheetnumber = "1"
  elif XX % 2 == 1 and 16 <= YY and YY <= 30:
    sheetnumber = "2"
  elif XX % 2 == 0 and 17 + dYYtop <= YY and YY <= 30 + dYYbottom:
    sheetnumber = "2"
  else:
    return None

  return sheetletter + sheetnumber
