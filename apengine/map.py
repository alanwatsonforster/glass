"""
The map.
"""

import apengine.azimuth as apazimuth
import apengine.draw    as apdraw
import apengine.hex     as aphex
import apengine.hexcode as aphexcode
import apengine.log     as aplog

import math
import numpy as np

_sheetgrid = []
_sheetlist = []
_nxsheetgrid = 0
_nysheetgrid = 0
_compassrose = None

_dxsheet = 20
_dysheet = 15

_saved = False

level0color    = ( 0.850, 0.900, 0.850)
level1color    = ( 0.824, 0.752, 0.640)
level2color    = ( 0.616, 0.664, 0.560)
ridgelinecolor = ( 0.500, 0.500, 0.450)
woodcolor = (0.0, 0.5, 0.0)
hexcolor       = ( 0.500, 0.500, 0.500)

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

  global _saved
  _saved = False

def startdrawmap():

  """
  Draw the map.
  """

  #global _saved
  #if _saved:
  #  apdraw.restore()
  #  return

  apdraw.setcanvas(_nxsheetgrid * math.sqrt(3/4) * _dxsheet, _nysheetgrid * _dysheet)

  # Draw the sheets and level 0.
  for sheet in sheets():
    xmin, ymin, xmax, ymax = sheetlimits(sheet)
    apdraw.drawrectangle(xmin, ymin, xmax, ymax, linecolor="black", fillcolor=level0color, zorder=0)
    # Unless I add these lines, the rectangle gets clipped. I don't understand why.
    apdraw.drawline(xmin, ymin, xmin, ymax, color="grey")
    apdraw.drawline(xmax, ymin, xmax, ymax, color="grey")
    apdraw.drawline(xmin, ymin, xmax, ymin, color="grey")
    apdraw.drawline(xmin, ymax, xmax, ymax, color="grey")

  # Draw level 1.
  for h in level1hexcodes:
    if aphexcode.tosheet(h) in sheets():
      apdraw.drawhex(*aphexcode.toxy(h), fillcolor=level1color, zorder=0)

  # Draw level 2.
  for h in level2hexcodes:
    if aphexcode.tosheet(h) in sheets():
      apdraw.drawhex(*aphexcode.toxy(h), fillcolor=level2color, zorder=0)

  # Draw the ridgeline on sheets B2 and C2.
  if "B2" in sheets():
    x0, y0 = aphexcode.toxy(4522)
    dx = np.array([ -0.67, +0.00, +1.00, +1.00, +0.00, +0.00, -1.00, -1.67 ])
    dy = np.array([ +1.00, +0.00, -0.50, -1.50, -2.00, -5.00, -5.50, -6.50 ])
    apdraw.drawlines(x0 + dx, y0 + dy, linewidth=7, color=ridgelinecolor, zorder=0)
  if "C2" in sheets():
    x0, y0 = aphexcode.toxy(5317)
    dx = np.array([ -0.50, +1.00, +1.67 ])
    dy = np.array([ +0.25, -0.50, -0.50 ])
    apdraw.drawlines(x0 + dx, y0 + dy, linewidth=7, color=ridgelinecolor, zorder=0)
    x0, y0 = aphexcode.toxy(5618)
    dx = np.array([ -0.67, +0.00, +1.00, +1.00, +2.50 ])
    dy = np.array([ +0.00, +0.00, -0.50, -1.50, -2.25 ])
    apdraw.drawlines(x0 + dx, y0 + dy, linewidth=7, color=ridgelinecolor, zorder=0)    
    x0, y0 = aphexcode.toxy(6320)
    dx = np.array([ +0.00, +0.00, -2.50 ])
    dy = np.array([ +0.50, -4.00, -5.25 ])
    apdraw.drawlines(x0 + dx, y0 + dy, linewidth=7, color=ridgelinecolor, zorder=0)
  
  # Draw the woods.
  for h in woodshexcodes:
    if aphexcode.tosheet(h) in sheets():
      apdraw.drawhex(*aphexcode.toxy(h), linecolor=woodcolor, hatch="o", zorder=0)

  # Draw and label the hexes.
  for sheet in sheets():
    xmin, ymin, xmax, ymax = sheetlimits(sheet)
    for ix in range(0, _dxsheet + 1):
      for iy in range(0, _dysheet + 1):
        x = xmin + ix
        y = ymin + iy
        if ix % 2 == 1:
          y -= 0.5
        # Draw the hex if it is on the map and either its center or the center 
        # of its upper left edge are on this sheet.
        if isonmap(x, y) and (isonsheet(sheet, x, y) or isonsheet(sheet, x - 0.5, y + 0.25)):
          apdraw.drawhex(x, y, linecolor=hexcolor, zorder=0.5)
          apdraw.drawhexlabel(x, y, aphexcode.fromxy(x, y), color=hexcolor, zorder=0.5)

  # Label the sheets.
  for sheet in sheets():
    xmin, ymin, xmax, ymax = sheetlimits(sheet)
    apdraw.drawtext(xmin + 1.0, ymin + 1.5, 90, sheet, dy=-0.05, size=12, color=hexcolor)

  # Draw the compass rose.
  if _compassrose != None:
    apdraw.drawcompass(*aphexcode.toxy(_compassrose), apazimuth.tofacing("N"), color=hexcolor, zorder=0.5)

  #apdraw.save()
  #_saved = True

def enddrawmap():
  apdraw.show()

def sheetorigin(sheet):

  """
  Returns the hex coordinates (x0, y0) of the lower left corner of the 
  specified sheet.
    
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
  Returns the hex coordinates (xmin, ymin) and (xmax, ymax) the lower left
  and upper right corners of the specified sheet.
  """

  assert sheet in sheets()

  xmin, ymin = sheetorigin(sheet)

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

################################################################################

level1hexcodes = [

  # B1
  3309, 
  3407, 3408, 3409,
  3506, 3507, 3508, 3509,
  3607, 3608, 3609,
  3707, 3708,

  # B2
  3123, 3124,
  3223, 3224, 3225,
  3322, 3323, 3324, 3325, 3326,
  3425, 3426,
  3525, 3526,
  3626,

  3723,
  3824,
  3923, 3924,
  4020, 4021, 4022, 4023, 4024, 4025, 
  4120, 4121, 4122, 4123, 4124,
  4220, 4221, 4222, 4223, 4224, 
  4318, 4319, 4322, 4323, 4324, 4327, 4328, 4329,
  4418, 4419, 4420, 4424, 4425, 4426, 4427, 4428, 4429,
  4518, 4519, 4520, 4526, 4527, 4528,
  4621, 4626, 4627, 4628,
  4721, 4723, 4724, 4725,
  4822, 4823,

  # C1

  5406, 5407,
  5505, 5506,
  5605, 5606, 5607,
  5704, 5705, 5706, 5707,
  5804, 5805, 5806, 5807, 5808,
  5904, 5905, 5906, 5907, 5908,
  6007, 6008, 6009,
  6107, 6108,

  5613, 5614,
  5711, 5712, 5713,
  5812, 5813,
  5911, 5912, 5913,
  6011, 6012, 6013, 6014,
  6111, 6112, 6113,
  6211, 6212, 6213,
  6310, 6311, 6312, 6313,
  6410, 6411, 6412, 6413,
  6509, 6510, 6511, 6512,
  6609, 6610, 6611, 6612,
  6709, 6710, 6711,
  6810, 6811, 6812,
  6910, 6911,

  # C2

  5217, 5218, 5219,
  5316, 5317, 5318, 5319,
  5417, 5418, 5419,
  5517, 5518,
  5617, 5618, 5619, 5620,
  5716, 5717, 5718, 5719, 5720,
  5817, 5818, 5819, 5820, 5821,
  5919, 5920, 5921,

  6025, 6026, 6027,
  6121, 6122, 6124, 6125, 6126, 6127, 6128,
  6220, 6221, 6222, 6223, 6224, 6225, 6226, 6227, 6228, 6229,
  6319, 6320, 6321, 6322, 6323, 6324, 6325, 6326, 6327, 6328, 6329,
  6420, 6421, 6422, 6423, 6424, 6426, 6426, 6427, 6428, 6429,
  6523, 6526,

]

level2hexcodes = [

  # B2
  4320, 4321,
  4421, 4422, 4423,
  4521, 4522, 4523, 4524, 4525,
  4622, 4623, 4624, 4625,
  4722

]


woodshexcodes = [
    
  # A1
  1111, 1112,
  1211, 1212, 1213, 1214, 1215,
  1310, 1311, 1312, 1313, 1314, 
  1411, 1412, 1413, 1414, 1415,
  1510, 1511, 1512, 1513, 1514, 
  1610, 1611, 1612, 1613, 1614, 1615,
  1710, 1711, 1712, 1713, 1714, 1715,
  1811, 1812, 1813, 1814, 1815,
  1910, 1911, 1912, 1913, 1914, 
  2009, 2010, 2011, 2012, 2013, 2014, 2015,
  2109, 2110, 2111, 2112, 2114, 2115,
  2211, 2212, 2214, 2215,
  2310, 2311, 2312, 2314,
  2411, 2412,

  # A2 has no woods.

  # B1

  3103, 3104, 3105, 3108, 3109,
  3202, 3203, 3204, 3205, 3206, 3207, 3208, 3209, 3210,
  3301, 3302, 3303, 3304, 3305, 3306, 3307, 3308,
  3402, 3407, 3408, 3409,
  3501, 3502, 3506, 3507, 3508,
  3602, 3603, 3604, 3605, 3607, 3608,
  3701, 3702, 3703, 3704,
  3802, 3803, 3804, 3805, 3806,
  3901, 3902, 3903, 3904, 3905, 3906, 3907,
  4003, 4004, 4005, 4006, 4007,
  4102, 4103, 4104, 4105,
  4203, 4204, 4205,

  3213,
  3312,
  3411, 3412,

  4606, 4607, 4608,
  4703, 4704, 4706, 4707,
  4803, 4804, 4805, 4806, 4807,
  4902, 4903, 4904, 4905,

  # B2

  3219, 3220,
  3319,

  3123, 3124,
  3223, 3224, 3225,
  3322, 3323, 3324, 3325, 3326,
  3422, 3425, 3426,
  3519, 3521, 3525, 3526,
  3619, 3620, 3621, 3622, 3623, 3624, 3626, 3628, 3629,
  3717, 3718, 3719, 3722, 3723, 3724, 3727, 3728,
  3817, 3818, 3819, 3824, 3825, 3826, 3827, 3828,
  3917, 3918, 3919, 3923, 3924, 3925, 3926, 3927, 3928,
  4018, 4019, 4020, 4021, 4022, 4023, 4024, 4025, 4026, 4027, 4028, 4029,
  4118, 4119, 4122, 4123, 4124, 4125, 4126, 4127,
  4223, 4224, 4225, 4226,


  4418, 4419, 4420,
  4517, 4518, 4519, 4520,
  4617, 4618, 4619, 4620, 4621,

  4820,
  4919, 4920,

  # C1

  6502, 6503,
  6602, 6603, 6605, 6608,
  6701, 6702, 6703, 6704, 6705, 6706, 6707, 6708,
  6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809,
  6903, 6904, 6905, 6906, 6907, 6908, 6909,

  6611, 6612, 6613, 6614, 
  6710, 6711, 6712, 6713, 6714,
  6811, 6813, 6814, 6815,
  6913, 6914, 6915,

  # C2

  5221, 5222,
  5320, 5321,
  5420, 5421, 5422,
  5520, 5521,
  5621, 5622, 5623,
  5721, 5722, 5723,
  5822, 5823, 5824,

]
