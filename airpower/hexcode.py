import airpower.hex  as aphex
import airpower.maps as apmaps

def _split(h):

  """ 
  Split the hex code h of the form XXYY and return XX and YY as integers.
  """

  assert isoncenter(h)

  h = int(h)
  XX = h // 100
  YY = h % 100
  return XX, YY

def _join(XX, YY):

  """
  Return the hex code XXYY corresponding to the integers XX and YY.
  """

  return 100 * XX + YY

def _inrange(h):

  """
  Return True if h is within the range of valid hex codes of the form XXYY. 
  Otherwise return False.
  """

  return 1000 <= h and h <= 9999

def isoncenter(h):

  """
  Return True if h is grammatically a hex code that corresponds to a hex 
  center. Otherwise return False.
  """

  if isinstance(h, int) and _inrange(h):
    return True

  if isinstance(h, float) and h % 1.0 == 0.0 and _inrange(h):
    return True

  if isinstance(h, str) and h.isdecimal() and _inrange(int(h)):
    return True

  return False

def isonedge(h):

  """
  Return True if h is grammatically a hex code that corresponds to (the center 
  of) the edge of a hex. Otherwise return False.
  """

  if not isinstance(h, str):
    return False

  m = h.split("/")
  if len(m) != 2:
    return False

  if not m[0].isdecimal() or not _inrange(int(m[0])):
    return False

  if not m[1].isdecimal() or not _inrange(int(m[2])):
    return False

  return True

def check(h):

  """
  Raise a ValueError exception if h is not a gramatically valid hex code.
  """

  if not isoncenter(h) and not isonedge(h):
    raise ValueError("%s is not a valid hex code." % h)

def fromxy(x, y):

  """
  Return the hex code corresponding to the hex coordinate (x, y).
  """

  aphex.checkiscenteroredge(x, y)

  if aphex.iscenter(x, y):

    map = apmaps.fromxy(x, y)
    x0, y0 = apmaps.maporigin(map)
    XX0, YY0 = _split(maporigin(map))
    XX = XX0 + (x - x0)
    YY = YY0 - (y - y0)
    if XX % 2 == 0:
      YY += 0.5

    return _join(XX, YY)

  else:

    if x % 1 == 0:
      n0 = fromxy(x, y + 0.5)
      n1 = fromxy(x, y - 0.5)
    elif x % 2 == 0.5 and y % 1 == 0.25:
      n0 = fromxy(x - 0.5, y - 0.25)
      n1 = fromxy(x + 0.5, y + 0.25)
    elif x % 2 == 0.5 and y % 1 == 0.75:
      n0 = fromxy(x - 0.5, y + 0.25)
      n1 = fromxy(x + 0.5, y - 0.25)      
    elif x % 2 == 1.5 and y % 1 == 0.25:
      n0 = fromxy(x - 0.5, y + 0.25)
      n1 = fromxy(x + 0.5, y - 0.25)   
    elif x % 2 == 1.5 and y % 1 == 0.75:
      n0 = fromxy(x - 0.5, y - 0.25)
      n1 = fromxy(x + 0.5, y + 0.25)

    if n0 < n1:
      return "%s/%s" % (n0, n1)
    else:
      return "%s/%s" % (n1, n0)

def toxy(h):

  """
  Return the hex coordinate (x, y) corresponding to the hex code h.
  """

  check(h)

  if isoncenter(h):

    XX, YY = _split(h)

    map = tomap(h)
    XX0, YY0 = _split(maporigin(map))
    x0, y0 = apmaps.maporigin(map)

    dx = XX - XX0
    dy = YY0 - YY
    if XX % 2 == 0:
      dy += 0.5

    return x0 + dx, y0 + dy

  else:

    m = h.split("/")
    x0, y0 = toxy(m[0])
    x1, y1 = toxy(m[1])

    return 0.5 * (x0 + x1), 0.5 * (y0 + y1)

def maporigin(map):

  """
  Return the hex code of the center of the lower left hex in the specified map.
  """

  mapletter = map[0]
  if mapletter == "A":
    XX = 11
  elif mapletter == "B":
    XX = 31
  elif mapletter == "C":
    XX = 51
  else:
    raise "invalid map %s." % map

  mapnumber = map[1]
  if mapnumber == "1":
    YY = 15
  elif mapnumber == "2":
    YY = 30
  else:
    raise "invalid map %s." % map

  return _join(XX, YY)

def isonmap(h, map):

  """
  Return True if the hex code h is on the specified map. The hex code must
  correspond to the center of a hex, not an edge.
  """

  assert isoncenter(h)

  XX, YY = _split(h)
  XX0, YY0 = _split(maporigin(map))

  if XX < XX0 or XX >= XX + 20:
    return False
  elif XX % 2 == 1 and YY > YY0 or YY < YY0 - 14:
    return False
  elif YY > YY0 + 1 or YY < YY0 - 13:
    return False

  return True


def tomap(h):

  """
  Returns the map containing the hex code h, which must refer to a hex center.
  """

  assert isoncenter(h)

  XX, YY = _split(h)

  if 11 <= XX and XX <= 30:
    mapletter = "A"
  elif 31 <= XX and XX <= 50:
    mapletter = "B"
  elif 51 <= XX and XX <= 70:
    mapletter = "C"
  else:
    raise ValueError("invalid hex code %d." % h)

  if XX % 2 == 1 and 1 <= YY and YY <= 15:
    mapnumber = "1"
  elif XX % 2 == 0 and 2 <= YY and YY <= 16:
    mapnumber = "1"
  elif XX % 2 == 1 and 16 <= YY and YY <= 30:
    mapnumber = "2"
  elif XX % 2 == 0 and 17 <= YY and YY <= 31:
    mapnumber = "2"
  else:
    raise ValueError("invalid hex code %d." % h)

  return mapletter + mapnumber

def hexcodes(map):

  """
  Return a list of the hex codes of the centers of the hexes on the specified
  map.
  """

  XX0, YY0 = _split(maporigin(map))

  hexcodes = []
  for XX in range(XX0, XX0 + 20):
    if XX % 2 == 1:
      for YY in range(YY0 - 14, YY0 + 1):
        hexcodes.append(_join(XX,YY))
    else:
      for YY in range(YY0 - 13, YY0 + 2):
        hexcodes.append(_join(XX,YY))

  return hexcodes
