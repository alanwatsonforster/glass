import airpower.draw as apdraw

import math

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = [7.5, 10]
plt.rcParams.update({'font.size': 10})

_maps = []
_nxmaps = 0
_nymaps = 0

def setmaps(maps, verbose=True):

  global _maps
  global _nymaps
  global _nxmaps

  # The maps argument follows visual layout, so we need to flip it vertically 
  # so that the lower-left map has indices (0,0).
  _maps = list(reversed(maps))
  _nymaps = len(maps)
  _nxmaps = len(maps[0])

  if verbose:
    for iy in range (0, _nymaps):
      print("%s" % " ".join(maps[iy]))

# x0 and y0 are the hex coordinates of the lower left hex.

def _mapx0(map):
  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if map == _maps[iy][ix]:
        return ix * 20
  raise ValueError("map %s is not in use." % map)

def _mapy0(map):
  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if map == _maps[iy][ix]:
        return iy * 15
  raise ValueError("map %s is not in use." % map)

# xx0 and yy0 are the components of the hex number of the lower left hex.
  
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

def numbertomap(n):

  xx = n // 100
  yy = n % 100

  if 11 <= xx and xx <= 30:
    mapletter = "A"
  elif 31 <= xx and xx <= 50:
    mapletter = "B"
  elif 51 <= xx and xx <= 70:
    mapletter = "C"
  else:
    raise ValueError("invalid map number %d." % n)

  if xx % 2 == 1 and 1 <= yy and yy <= 15:
    mapnumber = "1"
  elif xx % 2 == 0 and 2 <= yy and yy <= 16:
    mapnumber = "1"
  elif xx % 2 == 1 and 16 <= yy and yy <= 30:
    mapnumber = "2"
  elif xx % 2 == 0 and 17 <= yy and yy <= 31:
    mapnumber = "2"
  else:
    raise ValueError("invalid map number %d." % n)

  return mapletter + mapnumber

def numbertohex(n):

  map = numbertomap(n)

  xx = n // 100
  yy = n % 100

  dx = xx - _mapxx0(map)
  dy = _mapyy0(map) - yy
  if xx % 2 == 0:
    dy += 0.5

  x0 = _mapx0(map)
  y0 = _mapy0(map)

  return x0 + dx, y0 + dy

def _drawmap(map):
  xx0 = _mapxx0(map)
  yy0 = _mapyy0(map)
  for ix in range(xx0, xx0 + 20):
    if ix % 2 == 1:
      for iy in range(yy0 - 14, yy0 + 1):
        n = ix * 100 + iy
        x, y = numbertohex(n)
        apdraw.drawhex(x, y)
        apdraw.drawtext(x, y, 90, "%04d" % n, dy=0.3, size=7, color="grey")
    else:
      for iy in range(yy0 - 13, yy0 + 2):
        n = ix * 100 + iy
        x, y = numbertohex(n)
        apdraw.drawhex(x, y)
        apdraw.drawtext(x, y, 90, "%04d" % n, dy=0.3, size=7, color="grey")

  x0, y0 = numbertohex(100 * xx0 + yy0)

  apdraw.drawtext(x0, y0, 90, map, dy=-0.05, size=12, color="grey")

  apdraw.drawline(x0 -  0.5, y0 -  0.5, x0 + 19.5, y0 -  0.5, color="grey")
  apdraw.drawline(x0 -  0.5, y0 -  0.5, x0 -  0.5, y0 + 14.5, color="grey")
  apdraw.drawline(x0 -  0.5, y0 + 14.5, x0 + 19.5, y0 + 14.5, color="grey")
  apdraw.drawline(x0 + 19.5, y0 -  0.5, x0 + 19.5, y0 + 14.5, color="grey")

def drawmaps():

  apdraw.setcanvas(_nxmaps * 20, _nymaps * math.sqrt(3/4) * 15)

  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if _maps[iy][ix] != "--":
        _drawmap(_maps[iy][ix])
