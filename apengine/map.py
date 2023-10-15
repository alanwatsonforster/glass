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

level0color    = ( 0.850, 0.900, 0.850 )
level1color    = ( 0.824, 0.752, 0.640 )
level2color    = ( 0.616, 0.664, 0.560 )
ridgelinecolor = ( 0.600, 0.500, 0.450 )
woodedcolor    = ( 0.000, 0.500, 0.000 )
urbancolor     = ( 0.600, 0.600, 0.600 )
watercolor     = ( 0.650, 0.820, 1.000 )
roadcolor      = ( 0.600, 0.600, 0.600 )
hexcolor       = ( 0.500, 0.500, 0.500 )

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

  def toxy(sheet, x, y):
    XX = int(x + 0.5)
    YY = int(y + 0.5)
    dx = x - XX
    dy = y - YY
    x0, y0 = aphexcode.toxy(XX * 100 + YY, sheet=sheet)
    return x0 + dx, y0 - dy

  #global _saved
  #if _saved:
  #  apdraw.restore()
  #  return

  apdraw.setcanvas(_nxsheetgrid * _dxsheet, _nysheetgrid * _dysheet)

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
  
  # Draw the wooded areas.
  for h in woodedhexcodes:
    if aphexcode.tosheet(h) in sheets():
      apdraw.drawhex(*aphexcode.toxy(h), linecolor=woodedcolor, hatch="o", zorder=0)

  # Draw the urban areas.
  for h in urbanhexcodes:
    if aphexcode.tosheet(h) in sheets():
      apdraw.drawhex(*aphexcode.toxy(h), linecolor=urbancolor, hatch="xx", zorder=0)

  # Draw the rivers.
  for river in rivers:
    sheet = river[0]
    if sheet in sheets():
      p = river[1]
      xy = [toxy(sheet, *p) for p in p]
      x = [xy[0] for xy in xy]
      y = [xy[1] for xy in xy]
      apdraw.drawlines(x, y, color=watercolor, linewidth=7, capstyle="butt", zorder=0)

  # Draw the roads.
  for road in roads:
    sheet = road[0]
    if sheet in sheets():
      p = road[1]
      xy = [toxy(sheet, *p) for p in p]
      x = [xy[0] for xy in xy]
      y = [xy[1] for xy in xy]
      apdraw.drawlines(x, y, color=roadcolor, linewidth=3, capstyle="butt", zorder=0)

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


woodedhexcodes = [
    
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

urbanhexcodes = [
    
  # A1

  1402, 1403,

  1602, 1604, 1605,
  1701, 1702, 1703, 1704, 1705,
  1802,
  1901, 1902, 1903,

  2113,

  2407,

  2603,
  2701, 2702,

  2615,
  2714, 2715,

  2911,

  # A2

  1121, 1125,
  1220, 1221, 1222, 1224, 1225, 1226,
  1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328,
  1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430,
  1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527,
  1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630,
  1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729,
  1823, 1824, 1825, 1826, 1827, 1828, 
  1923, 1924, 1925, 1926, 1927,
  2028, 2029,

  1516,
  1617,

  1919,
  2020, 2021,
  2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127,
  2222,

  2529,
  2628, 2629,
  2728,

  2618,
  2717, 2718,
  2818,

  2921,

  # B1

  3513, 3514,
  3614, 3615,
  3713,

  4708,
  4808,
  4908,

  # B2

  3227,

  3318,
  3418,

  3630,

  4728, 4729,
  4829, 4830,

  4924, 4925,

  # C1

  5110,

  5215,

  6105,

  6514, 6515,
  6615,
  6715,

  # C2

  5427,

  6630,
  6730,

    
]

rivers = [

  ["A1", [[20,1],[20,3],[20.67,3.5],[27.33, 6.5],[28.67, 8.5],[27.33,10.5],
    [29.5,14.25],[29.5,15.25],[30,16]]],
  ["A1", [(19, 15), (20, 16), (20, 16.0)]],
  ["A1", [[10,  1], (11,  1), (11.5, 1.25)]],

  ["A2", [[20,16], [20, 16.5]]],
  ["A2", [[10,16],[11,16],[11.67,16.5],[17.33,18.5],[20,23],[20,27],[20.67,27.5],
    [20.67,28.5],[20.0,30.0],[20.0,31.0]]],
  ["A2", [[15.33, 17.5], [18,22], [20,23]]],
  ["A2", [[17.33, 23.5],[17.67,24.5]]],
  ["A2", [[11.33, 18.5], [15.67, 21.5]]],

  ["B1", [[30, 1], [31, 1],[31, 2],[32,3],[33,2],[34,3],[34,4],[36,3],[36,2],
    [37,1],[38,2],[38,3],[39,3],[40,3],[40,1]]],
  ["B1", [[30,16], [33,14],[34,15],[35,14],[36,15],[37,14],[38,15],[39,14],
    [40,15,],[40,16]]],
  ["B1", [[40,16],[40,15],[39,14],[39,13],[42,12],[46,14],[47,13],[49,14],
    [50,16]]],

  ["B2", [[30,16],[33,17],[33,18],[34,19],[36,18],[37,18],[37,19],[39,20,],
    [39,22],[38,23],[36,22],[35,22],[35,24],[37,25,],[37,26],[35,27],[35,29],
      [36,30],[38,29],[40,30],[40,31]]],
  ["B2", [[35,27],[34,27],[33,27],[32,27],[31,27],[31,29],[30,31]]],
  ["B2", [[50,31],[49.5,29.75],[47,28],[47,27],[48.5,26.25],[48.5,23.5]]],
  ["B2", [[48,27],[47,26]]],
  ["B2", [[48,26],[48.5,26.25]]],
  ["B2", [[40,16],[41,16]]],
  ["B2", [[40,16],[40,17],[41,17],[38,19],[38,20]]],
  ["B2", [[41,17],[41,18],[40,19],[39,18]]],

  ["C1", [[50,1],[51,1],[51,3]]],
  ["C1", [[51,2],[52,2],[53,2]]],
  ["C1", [[60,1],[60,1.5],[61,1],[61,3],[60,4],[60,6],[63,7],[63,8],[60,10],[55,7],
    [54,8],[54,8],[54,9],[55,9],[55,11],[54,12],[54,13],[51,14],[50,16]]],
  ["C1", [[60,16],[60,15],[61,14],[63,15],[65,14],[65,13],[66,13],[67,13],
    [66,14],[66,15],[67,15],[68,15],[68,14],[69,13],[69,14],[70,16]]],

  ["C2", [[50,16],[51,16]]],
  ["C2", [[60,16],[60,17],[59,17],[59,18],[61,17],[61,18],[62,19],[63,18],
    [65,19],[65,22],[66,23],[66,24],[65,24],[65,25],[60,28],[60,31]]],
  ["C2", [[70,31],[69,29]]],
]

roads = [

  ["A1", [[15.0,0.5],[15,9]]],
  ["A1", [[10,6],[12,5],[12,4],[13,3],[17,5],[19,4],[19,2]]],
  ["A1", [[19,4],[25,7],[25,15.5]]],
  ["A1", [[10,11],[13,9],[14,10],[16,9],[18,10],[18,13],[15,14],[15,15.5]]],
  ["A1", [[18,12],[21,13]]],
  ["A1", [[24,7],[25,6]]],
  ["A1", [[25,0.5],[25,3],[26,4],[26,6],[28,5],[30,6]]],
  ["A1", [[30,11],[29,11]]],
  ["A1", [[27,15.5],[27,15]]],
  ["A1", [[27,0.5],[27,1]]],
  
  ["A2", [[15,15.5],[15,16]]],
  ["A2", [[10,21],[15,23],[10,26]]],
  ["A2", [[15,30.5],[15,21]]],
  ["A2", [[15,24],[17,23],[18,24],[18,28]]],
  ["A2", [[15,19],[15,20],[17,21],[17,22],[19,23],[19,27]]],
  ["A2", [[15,23],[24,19],[24,18],[27,16],[27,15.5]]],
  ["A2", [[21,20],[21,26]]],
  ["A2", [[25,15.5],[25,17]]],
  ["A2", [[22,19],[22,20],[25,21],[25,23],[30,26]]],
  ["A2", [[21,25],[25,27],[25,30.5]]],
  ["A2", [[27,30.5],[27,30],[25,29]]],
  ["A2", [[25,29],[27,28],[27,24]]],
  ["A2", [[29,21],[30,21]]],
  
  ["B1", [[30,6],[31,6],[35,4],[35,0.5]]],
  ["B1", [[34,6],[38,7],[38,12],[36,13],[35,12],[32,14],[31,13],[31,12],[32,12],
    [32,11],[31,10],[30,11]]],
  ["B1", [[36,13],[36,14]]],
  ["B1", [[35,15.5],[35,15],[36,15]]],
  ["B1", [[45,0.5],[45,15.5]]],
  ["B1", [[47,15.5],[47,11],[45,10]]],
  ["B1", [[45,9],[46,10],[46,11]]],
  ["B1", [[47,11],[48,12],[50,11]]],
  ["B1", [[47,0.5],[47,1],[48,2],[48,4],[49,4],[49,7],[48,8]]],
  ["B1", [[50,6],[49,6]]],
  
  ["B2", [[30,21],[31,20],[31,18],[32,18],[33,18]]],
  ["B2", [[35,15.5],[35,17],[34,18]]],
  ["B2", [[45,15.5],[45,16],[42,18],[42,19],[41,19],[41,21],[43,22],[43,26],
    [42,27],[42,30],[43,30],[44,30],[45,30],[45,30.5]]],
  ["B2", [[45,30],[47,29],[47,30.5]]],
  ["B2", [[47,15.5],[47,20],[49,21],[50,21]]],
  ["B2", [[49,21],[49,25],[50,26]]],
  ["B2", [[30,26],[32,27]]],
  ["B2", [[35,30.5],[35,30],[35.83,30.17]]],

  ["C1", [[50,6],[51,6],[51,7],[52,8],[53,7],[53,10],[52,11],[51,10],[50,11]]],
  ["C1", [[52,11],[52,12],[53,12],[53,14],[55,15],[55,15.5]]],
  ["C1", [[53,14],[52,15]]],
  ["C1", [[55,0.5],[55,2],[54,3],[54,4],[58,6],[58,7],[60,8],[60,9.75]]],
  ["C1", [[59,7],[59,6],[59.67,6.17]]],
  ["C1", [[65,0.5],[65,1],[63,2],[63,4],[60.33,5.83]]],
  ["C1", [[63,4],[65,5],[65,6],[66,7],[69,5],[70,6]]],
  ["C1", [[60,10.25],[60,12],[61,12],[62,12],[63,12],[64,13], [64,14],[64.67,13.87]]],
  ["C1", [[64,13],[67,11],[68,12],[70,11]]],
  ["C1", [[67,15.5],[67,15.17]]],
  ["C1", [[64,2],[65,2],[67,1],[67,0.5]]],
  ["C1", [[65,15.5],[65,15]]],

  ["C2", [[55,15.5],[55,19],[53,20],[52,20],[50,21]]],
  ["C2", [[50,26],[54,28],[54,29],[55,29],[55,30.5]]],
  ["C2", [[54,28],[54,27],[60,24],[60,20],[61.67,19.17]]],
  ["C2", [[62,18.75],[62,18],[65,16],[65,15.5]]],
  ["C2", [[67,15.5],[67,18],[68,19],[68,21],[69,21]]],
  ["C2", [[65,30.5],[65,29],[68,28],[68,22],[70,21]]],
  ["C2", [[68,25],[70,26]]],

]
