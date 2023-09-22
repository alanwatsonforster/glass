import airpower.azimuth as apazimuth
import airpower.draw    as apdraw
import airpower.hex     as aphex

import math

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = [7.5, 10]
plt.rcParams.update({'font.size': 10})

_mapsgrid = []
_mapslist = []
_nxmaps = 0
_nymaps = 0
_compassrose = None

def setmaps(mapsgrid, compassrose, verbose=True):

  global _mapsgrid
  global _mapslist
  global _nymaps
  global _nxmaps
  global _compass

  # The maps argument follows visual layout, so we need to flip it vertically 
  # so that the lower-left map has indices (0,0).
  _mapsgrid = list(reversed(mapsgrid))
  _nymaps = len(_mapsgrid)
  _nxmaps = len(_mapsgrid[0])

  if verbose:
    for iy in range (0, _nymaps):
      print("%s" % " ".join(mapsgrid[iy]))

  _mapslist = []
  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if _mapsgrid[iy][ix] != "--":
        _mapslist.append(_mapsgrid[iy][ix])

  _compassrose = compassrose

# x0 and y0 are the hex coordinates of the center of the lower left hex.

def _mapx0(map):
  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if map == _mapsgrid[iy][ix]:
        return ix * 20
  raise ValueError("map %s is not in use." % map)

def _mapy0(map):
  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if map == _mapsgrid[iy][ix]:
        return iy * 15
  raise ValueError("map %s is not in use." % map)

# xx0 and yy0 are the components of the hex code of the lower left hex.
  
def _mapxx0(map):
  mapletter = map[0]
  if mapletter == "A":
    return 11
  elif mapletter == "B":
    return 31
  elif mapletter == "C":
    return 51
  else:
    raise "invalid map %s." % map

def _mapyy0(map):
  mapnumber = map[1]
  if mapnumber == "1":
    return 15
  elif mapnumber == "2":
    return 30
  else:
    raise "invalid map %s." % map

def isoncenter(n):

  if isinstance(n, int):
    return True

  if isinstance(n, float) and n % 1.0 == 0.0:
    return True

  if isinstance(n, str) and n.isdecimal():
    return True

  return False

def isonedge(n):

  if not isinstance(n, str):
    return False

  m = n.split("/")
  if len(m) != 2:
    return False

  if not m[0].isdecimal() and not m[1].isdecimal():
    return False

  # We should really check that they are adjacent.
  return True

def check(n):
  if not isoncenter(n) and not isonedge(n):
    raise ValueError("%s is not a valid hex code." % n)

def _mapfromhexcode(n):

  # This works only for centers and not for edges.
  assert isoncenter(n)

  n = int(n)

  xx = n // 100
  yy = n % 100

  if 11 <= xx and xx <= 30:
    mapletter = "A"
  elif 31 <= xx and xx <= 50:
    mapletter = "B"
  elif 51 <= xx and xx <= 70:
    mapletter = "C"
  else:
    raise ValueError("invalid hex code %d." % n)

  if xx % 2 == 1 and 1 <= yy and yy <= 15:
    mapnumber = "1"
  elif xx % 2 == 0 and 2 <= yy and yy <= 16:
    mapnumber = "1"
  elif xx % 2 == 1 and 16 <= yy and yy <= 30:
    mapnumber = "2"
  elif xx % 2 == 0 and 17 <= yy and yy <= 31:
    mapnumber = "2"
  else:
    raise ValueError("invalid hex code %d." % n)

  return mapletter + mapnumber


def fromhexcode(n):

  check(n)

  try:

    n = int(n)

    map = _mapfromhexcode(n)

    xx = n // 100
    yy = n % 100

    dx = xx - _mapxx0(map)
    dy = _mapyy0(map) - yy
    if xx % 2 == 0:
      dy += 0.5

    x0 = _mapx0(map)
    y0 = _mapy0(map)

    return x0 + dx, y0 + dy

  except:

    m = n.split("/")
    x0, y0 = fromhexcode(m[0])
    x1, y1 = fromhexcode(m[1])

    return 0.5 * (x0 + x1), 0.5 * (y0 + y1)

def _mapfromxy(x, y):
  aphex.check(x, y)
  for map in _mapslist:
    x0 = _mapx0(map)
    y0 = _mapy0(map)    
    if x0 - 0.5 <= x and x < x0 + 19.5 and y0 - 0.5 <= y and y < y0 + 14.5:
      return map
  return None

def tohexcode(x, y):

  aphex.check(x, y)

  if aphex.isoncenter(x, y):

    map = _mapfromxy(x, y)
    x0 = _mapx0(map)
    y0 = _mapy0(map)
    xx0 = _mapxx0(map)
    yy0 = _mapyy0(map)
    xx = xx0 + (x - x0)
    yy = yy0 - (y - y0)
    if xx % 2 == 0:
      yy += 0.5

    return "%04d" % int(xx * 100 + yy)

  else:

    if x % 1 == 0:
      n0 = tohexcode(x, y + 0.5)
      n1 = tohexcode(x, y - 0.5)
    elif x % 2 == 0.5 and y % 1 == 0.25:
      n0 = tohexcode(x - 0.5, y - 0.25)
      n1 = tohexcode(x + 0.5, y + 0.25)
    elif x % 2 == 0.5 and y % 1 == 0.75:
      n0 = tohexcode(x - 0.5, y + 0.25)
      n1 = tohexcode(x + 0.5, y - 0.25)      
    elif x % 2 == 1.5 and y % 1 == 0.25:
      n0 = tohexcode(x - 0.5, y + 0.25)
      n1 = tohexcode(x + 0.5, y - 0.25)   
    elif x % 2 == 1.5 and y % 1 == 0.75:
      n0 = tohexcode(x - 0.5, y - 0.25)
      n1 = tohexcode(x + 0.5, y + 0.25)

    return "%s/%s" % (n0, n1)

def _drawmap(map):

  xx0 = _mapxx0(map)
  yy0 = _mapyy0(map)
  for ix in range(xx0, xx0 + 20):
    if ix % 2 == 1:
      for iy in range(yy0 - 14, yy0 + 1):
        n = ix * 100 + iy
        x, y = fromhexcode(n)
        apdraw.drawhex(x, y)
        apdraw.drawtext(x, y, 90, "%04d" % n, dy=0.3, size=7, color="grey")
    else:
      for iy in range(yy0 - 13, yy0 + 2):
        n = ix * 100 + iy
        x, y = fromhexcode(n)
        apdraw.drawhex(x, y)
        apdraw.drawtext(x, y, 90, "%04d" % n, dy=0.3, size=7, color="grey")

  x0, y0 = fromhexcode(100 * xx0 + yy0)
  apdraw.drawtext(x0, y0, 90, map, dy=-0.05, size=12, color="grey")

  apdraw.drawline(x0 -  0.5, y0 -  0.5, x0 + 19.5, y0 -  0.5, color="grey")
  apdraw.drawline(x0 -  0.5, y0 -  0.5, x0 -  0.5, y0 + 14.5, color="grey")
  apdraw.drawline(x0 -  0.5, y0 + 14.5, x0 + 19.5, y0 + 14.5, color="grey")
  apdraw.drawline(x0 + 19.5, y0 -  0.5, x0 + 19.5, y0 + 14.5, color="grey")

def drawmaps():

  apdraw.setcanvas(_nxmaps * 20, _nymaps * math.sqrt(3/4) * 15)

  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if _mapsgrid[iy][ix] != "--":
        _drawmap(_mapsgrid[iy][ix])

  if _compassrose != None:
    apdraw.drawcompass(*fromhexcode(_compassrose), apazimuth.tofacing("N"))

