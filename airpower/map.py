import airpower.azimuth as apazimuth
import airpower.draw    as apdraw
import airpower.hex     as aphex
import airpower.hexcode as aphexcode
import airpower.log     as aplog

import math

_sheetgrid = []
_sheetlist = []
_nxsheetgrid = 0
_nysheetgrid = 0
_compassrose = None

_dxsheet = 20
_dysheet = 15

def setmap(sheetgrid, compassrose):

  """
  Set the arrangement of the sheets that form the map and the position of the 
  compass rose.
  """

  global _sheetgrid
  global _sheetlist
  global _nysheetgrid
  global _nxsheetgrid
  global _compassrose

  # The sheet grid argument follows visual layout, so we need to flip it 
  # vertically so that the lower-left sheet has indices (0,0).

  # TODO: Validate arguments. For example, that sheet grid is not ["A1"].

  _sheetgrid = list(reversed(sheetgrid))
  _nysheetgrid = len(_sheetgrid)
  _nxsheetgrid = len(_sheetgrid[0])

  aplog.log("sheet layout is:")
  aplog.logbreak()
  for iy in range (0, _nysheetgrid):
     aplog.log("  %s" % " ".join(sheetgrid[iy]))

  _sheetlist = []
  for iy in range (0, _nysheetgrid):
    for ix in range (0, _nxsheetgrid):
      if _sheetgrid[iy][ix] != "--":
        _sheetlist.append(_sheetgrid[iy][ix])

  _compassrose = compassrose

def drawmap():

  """
  Draw the map.
  """

  apdraw.setcanvas(_nxsheetgrid * _dxsheet, _nysheetgrid * math.sqrt(3/4) * _dysheet)

  for sheet in sheets():

    xmin, ymin, xmax, ymax = sheetlimits(sheet)
    apdraw.drawline(xmin, ymin, xmin, ymax, color="grey")
    apdraw.drawline(xmax, ymin, xmax, ymax, color="grey")
    apdraw.drawline(xmin, ymin, xmax, ymin, color="grey")
    apdraw.drawline(xmin, ymax, xmax, ymax, color="grey")

    for ix in range(0, _dxsheet + 1):
      for iy in range(0, _dysheet + 1):
        x = xmin + ix
        y = ymin + iy
        if ix % 2 == 1:
          y -= 0.5
        # Draw the hex if it is on the map and either its center or its upper left edge are
        # on this sheet.
        if isonmap(x, y) and (isonsheet(sheet, x, y) or isonsheet(sheet, x - 0.5, y + 0.25)):
          apdraw.drawhex(x, y)
          apdraw.drawhexlabel(x, y, aphexcode.fromxy(x, y))

    x0, y0 = aphexcode.toxy(aphexcode.sheetorigin(sheet), sheet=sheet)
    apdraw.drawtext(x0 + 1.0, y0 + 1.5, 90, sheet, dy=-0.05, size=12, color="grey")

  if _compassrose != None:
    apdraw.drawcompass(*aphexcode.toxy(_compassrose), apazimuth.tofacing("N"), color="grey")

def _dotsheet(sheet):

  """
  Draw dots on all of the hex positions in the specified sheet that are within
  the map.
  """

  x0, y0 = sheetorigin(sheet)
  for ix in range(-2,40):
    x = x0 + ix / 2
    if x % 1 == 0:
      dy = 0
    else:
      dy = 0.25
    for iy in range(-2, 60):
      y = y0 + iy / 2 + dy
      if isonmap(x, y):
        apdraw.drawdot(x, y)

def sheetorigin(sheet):

  """
  Returns the hex coordinates (x0, y0) of the center of the lower left hex in
  the specified sheet.
    
  The specified sheet must be in the map.
  """

  assert sheet in sheets()

  for iy in range (0, _nysheetgrid):
    for ix in range (0, _nxsheetgrid):
      if sheet == _sheetgrid[iy][ix]:
        x0 = ix * _dxsheet
        y0 = iy * _dysheet
        return x0, y0

def sheetlimits(sheet):

  """
  Returns the hex coordinates (xmin, ymax) and (xmin, ymax) a rectangle that 
  contains all of the hex centers and hex edges in the specified sheet. A hex 
  coordinate (x, y) is considered in the sheet if it satisfies:

    xmin < x < xmax and ymin < x < ymax. 
    
  The specified sheet must be in the map.
  """

  assert sheet in sheets()

  for iy in range (0, _nysheetgrid):
    for ix in range (0, _nxsheetgrid):
      if sheet == _sheetgrid[iy][ix]:
        xmin = ix * _dxsheet
        ymin = iy * _dysheet
        xmax = xmin + _dxsheet
        ymax = ymin + _dysheet
        return xmin, ymin, xmax, ymax

def sheets():

  """
  Returns a list of the sheets in the map.
  """

  return _sheetlist

def isonsheet(sheet, x, y):

  """
  Returns True if the hex coordinate (x, y) is on the specified sheet, 
  excluding its edges. Otherwise returns false. The sheet must be in the map.
  """

  assert sheet in sheets()

  xmin, ymin, xmax, ymax = sheetlimits(sheet)

  return xmin < x and x < xmax and ymin < y and y < ymax

def isonmap(x, y):

  """
  Returns True if the hex coordinate (x, y) is on the map, excluding its edges. 
  Otherwise returns false.
  """

  if tosheet(x, y) != None:
    return True

  # The point is either off the map or on the edges between adjacent sheets
  # in the map. So, we check the upper left, upper right, lower left, and lower
  # right edges.

  if tosheet(x + 0.50, y + 0.25) == None:
    return False 
  if tosheet(x - 0.50, y + 0.25) == None:
    return False
  if tosheet(x + 0.50, y - 0.25) == None:
    return False
  if tosheet(x - 0.50, y - 0.25) == None:
    return False

  return True

def tosheet(x, y):

  """
  Returns the sheet containing the hex coordinates (x, y). If no sheet contains 
  the coordinates, returns None.
  """

  for sheet in sheets():
    if isonsheet(sheet, x, y):
      return sheet
  return None
