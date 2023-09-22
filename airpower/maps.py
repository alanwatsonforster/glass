import airpower.azimuth as apazimuth
import airpower.draw    as apdraw
import airpower.hex     as aphex
import airpower.hexcode as aphexcode

import math

_mapsgrid = []
_mapslist = []
_nxmaps = 0
_nymaps = 0
_compassrose = None

_dxmap = 20
_dymap = 15

def setmaps(mapsgrid, compassrose, verbose=True):

  """
  Set the arrangement of the maps and the position of the compass rose.
  """

  global _mapsgrid
  global _mapslist
  global _nymaps
  global _nxmaps
  global _compassrose

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

def drawmaps():

  """
  Draw the maps.
  """

  apdraw.setcanvas(_nxmaps * _dxmap, _nymaps * math.sqrt(3/4) * _dymap)

  for map in inusemaps():

    hexcodes = aphexcode.hexcodes(map)

    for hexcode in hexcodes:
      x, y = aphexcode.toxy(hexcode)
      apdraw.drawhex(x, y)
      apdraw.drawtext(x, y, 90, "%d" % hexcode, dy=0.3, size=7, color="grey")

    xmin, ymin, xmax, ymax = maplimits(map)
    apdraw.drawline(xmin, ymin, xmin, ymax, color="grey")
    apdraw.drawline(xmax, ymin, xmax, ymax, color="grey")
    apdraw.drawline(xmin, ymin, xmax, ymin, color="grey")
    apdraw.drawline(xmin, ymax, xmax, ymax, color="grey")

    x0, y0 = aphexcode.toxy(aphexcode.maporigin(map))
    apdraw.drawtext(x0, y0, 90, map, dy=-0.05, size=12, color="grey")

  if _compassrose != None:
    apdraw.drawcompass(*aphexcode.toxy(_compassrose), apazimuth.tofacing("N"))


def maporigin(map):

  """
  Returns the hex coordinates (x0, y0) of the center of the lower left hex in
  the specified map.
    
  The specified map must be used.
  """

  assert isinuse(map)

  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if map == _mapsgrid[iy][ix]:
        x0 = ix * _dxmap
        y0 = iy * _dymap
        return x0, y0

def maplimits(map):

  """
  Returns the hex coordinates (xmin, ymax) and (xmin, ymax) a rectangle that 
  contains all of the hex centers and hex edges in the specified map. A hex 
  coordinate (x, y) is considered in the map if it satisfies:

    xmin <= x < xmax and ymin <= x < ymax. 
    
  The specified map must be in use.
  """

  assert isinuse(map)

  for iy in range (0, _nymaps):
    for ix in range (0, _nxmaps):
      if map == _mapsgrid[iy][ix]:
        xmin = ix * _dxmap - 0.5
        ymin = iy * _dymap - 0.5
        xmax = xmin + _dxmap
        ymax = ymin + _dymap
        return xmin, ymin, xmax, ymax

def isinuse(map):

  """
  Returns True if the map is in use. Otherwise returns False.
  """

  return map in _mapslist

def inusemaps():

  """
  Returns a list of the in use maps.
  """

  return _mapslist

def isinmap(map, x, y):

  """
  Returns True if the map contains the hex coordinate (x, y). Otherwise returns 
  false. The map must be in use.
  """

  assert isinuse(map)

  xmin, ymin, xmax, ymax = maplimits(map)

  return xmin <= x and x < xmax and ymin <= y and y < ymax

def fromxy(x, y):

  """
  Returns the map containing the hex coordinates (x, y). If no map contains the 
  coordinates, returns None.
  """

  for map in inusemaps():
    if isinmap(map, x, y):
      return map
  return None

