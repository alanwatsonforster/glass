"""
The map.
"""

import apxo.azimuth  as apazimuth
import apxo.draw     as apdraw
import apxo.hex      as aphex
import apxo.hexcode  as aphexcode

_drawterrain = True
_drawlabels  = True

_gdwsheets = False

_dxsheet = 20
_dysheet = 15

_sheetgrid      = []
_loweredgeonmap = {}
_rightedgeonmap = {}
_sheetlist      = []
_nxsheetgrid    = 0
_nysheetgrid    = 0

_xmin           = None
_xmax           = None
_ymin           = None
_ymax           = None
_dotsperhex     = None
_writefile      = None

_saved = False

_allwater = False

missingcolor     = [ 1.00, 1.00, 1.00 ]

ridgewidth       = 14
roadwidth        = 5
dockwidth        = 5
clearingwidth    = 20
bridgeinnerwidth = roadwidth + 8
bridgeouterwidth = bridgeinnerwidth + 6
runwaywidth      = 10
taxiwaywidth     = 7
damwidth         = 14
hexwidth         = 0.5
megahexwidth     = 7

roadoutlinewidth  = 2
dockoutlinewidth  = 2
waterourlinewidth = 2

def gdwsheets():
  return _gdwsheets

def setmap(sheetgrid, 
  drawterrain=True, drawlabels=True, 
  xmin=0, ymin=0, xmax=None, ymax=None, dotsperhex=80, writefile=False,
  style="original", 
  wilderness=None, forest=None, rivers=None, allforest=None, maxurbansize=None
  ):

  """
  Set the arrangement of the sheets that form the map and the position of the 
  compass rose.
  """

  global _gdwsheets
  global _dxsheet
  global _dysheet

  global _drawterrain
  global _drawlabels

  global _sheetgrid
  global _sheetlist
  global _loweredgeonmap
  global _rightedgeonmap
  global _nysheetgrid
  global _nxsheetgrid
  global _xmin
  global _ymin
  global _xmax
  global _ymax
  global _dotsperhex
  global _writefile

  blanksheets = ["", "-", "--"]
  gdwsheets = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]
  coasheets = [
      "A1", "B1", "C1", "D1",
      "A2", "B2", "C2", "D2",
      "A3", "B3", "C3", "D3",
      "A4", "B4", "C4", "D4",
      "A5", "B5", "C5", "D5",
      "A6", "B6", "C6", "D6",
  ]

  _gdwsheets = None

  if not isinstance(sheetgrid, list):
    raise RuntimeError("the sheet grid is not a list of lists.")
  for row in sheetgrid:
    if not isinstance(row, list):
      raise RuntimeError("the sheet grid is not a list of lists.")
    if len(row) != len(sheetgrid[0]):
      raise RuntimeError("the sheet grid is not rectangular.")
    for sheet in row:
      if sheet in blanksheets:
        pass
      elif _gdwsheets is not False and sheet in gdwsheets:
        _gdwsheets = True
      elif _gdwsheets is not True and sheet in coasheets:
        _gdwsheets = False
      else:
        raise RuntimeError("invalid sheet %s." % sheet)

  if _gdwsheets:
    _dxsheet = 20
    _dysheet = 25
  else:
    _dxsheet = 20
    _dysheet = 15    

  # The sheet grid argument follows visual layout, so we need to flip it 
  # vertically so that the lower-left sheet has indices (0,0).
  _sheetgrid = list(reversed(sheetgrid))

  _nysheetgrid = len(_sheetgrid)
  _nxsheetgrid = len(_sheetgrid[0])
  
  _drawterrain = drawterrain
  _drawlabels  = drawlabels

  _xmin = xmin if xmin is not None else 0
  _xmax = xmax if xmax is not None else _dxsheet * _nxsheetgrid
  _ymin = ymin if ymin is not None else 0
  _ymax = ymax if ymax is not None else _dysheet * _nysheetgrid
  _dotsperhex  = dotsperhex
  _writefile   = writefile

  def sheettoright(iy, ix):
    if ix < _nxsheetgrid - 1:
      return _sheetgrid[iy][ix + 1]
    else:
      return ""

  def sheetbelow(iy, ix):
    if iy > 0:
      return _sheetgrid[iy - 1][ix]
    else:
      return ""

  _sheetlist = []
  for iy in range (0, _nysheetgrid):
    for ix in range (0, _nxsheetgrid):
      sheet = _sheetgrid[iy][ix]
      if sheet not in blanksheets:
        _sheetlist.append(sheet)
        _loweredgeonmap.update({ sheet: sheetbelow(iy, ix) != ""})
        _rightedgeonmap.update({ sheet: sheettoright(iy, ix) != ""})

  global _saved
  _saved = False

  global _allwater, _forest, _allforest, _rivers, _wilderness, _maxurbansize

  global level0color, level1color, level2color, level3color
  global level1ridgecolor, level2ridgecolor
  global forestcolor, forestalpha, foresthatch
  global urbancolor, urbanalpha, urbanoutlinecolor, townhatch, cityhatch
  global megahexcolor, megahexalpha
  global roadcolor, roadoutlinecolor
  global dockcolor, dockoutlinecolor
  global watercolor, wateroutlinecolor
  global riverwidth, wideriverwidth
  global hexcolor, hexalpha
  global labelcolor

  def lighten(color, f):
    return list((1 - f) + f * x for x in color)

  def darken(color, f):
    return list(min(1, f * x) for x in color)

  def equivalentgray(color):
    x = (0.30 * color[0] + 0.59 * color[1] + 0.11 * color[2])
    return [x, x, x]

  # Defaults

  _allwater        = False
  _allforest       = False
  _forest          = True
  _maxurbansize    = 5
  _rivers          = True
  _frozen          = False
  _wilderness      = False

  riverwidth       = 14
  wideriverwidth   = 35

  townhatch        = "xx"
  cityhatch        = "xxx"
  foresthatch      = ".o"

  if not _drawterrain:

    hexcolor = [ 0.50, 0.50, 0.50 ]
    hexalpha = 1.0
    labelcolor = hexcolor

  elif style == "openwater":

    _allwater  = True
    watercolor = [ 0.77, 0.89, 0.95 ]

    megahexcolor = [ 1.00, 1.00, 1.00 ]
    megahexalpha = 0.12
      
    hexcolor = darken(watercolor, 0.7)
    hexalpha = 1.0
    labelcolor = hexcolor
    
  elif style == "seaice":

    _allwater  = True
    # This is the same color as level 0 of winter tundra below.
    watercolor = lighten([ 0.85, 0.85, 0.85 ], 1/20)

    hexcolor = [ 0.7, 0.80, 0.90 ]
    hexalpha = 1.0
    labelcolor = hexcolor

    megahexcolor = hexcolor
    megahexalpha = 0.025
        
  else:

    _allwater = False
    forestalpha = 0.3
    forestcolor  = [ 0.50, 0.65, 0.50 ]
    
    if style == "wintertundra" or \
       style == "winterborealforest":

      basecolor    = [ 0.85, 0.85, 0.85 ]
      dilution     = [ 1/20, 1/2, 2/2, 3/2 ]
      
      megahexcolor = [ 0.00, 0.00, 0.00 ]
      megahexalpha = 0.015

      _forest       = False
      _wilderness   = True
      _maxurbansize = 0
      _frozen       = True
      if style == "winterborealforest":
        _allforest = True
        megahexcolor = forestcolor
        megahexalpha = 0.07

    elif style == "arid" or \
         style == "desert":

      basecolor    = [ 0.78, 0.76, 0.67 ]
      dilution     = [ 1/3, 2/3, 3/3, 4/3 ]

      megahexcolor = [ 1.00, 1.00, 1.00 ]
      megahexalpha = 0.22

      riverwidth = 9

      if style == "desert":
        _wilderness   = True
        _forest       = False
        _rivers       = False
        _maxurbansize = 0

    elif style == "temperate" or \
         style == "summertundra" or \
         style == "original":

      basecolor    = [ 0.50, 0.70, 0.45 ]
      dilution     = [ 2/6, 3/6, 4/6, 5/6 ]

      megahexcolor = [ 1.00, 1.00, 1.00 ]
      megahexalpha = 0.12

      if style == "summertundra":
        _forest       = False
        _wilderness   = True
        _maxurbansize = 0

    elif style == "tropical" or \
         style == "tropicalforest" or \
         style == "summerborealforest":

      basecolor    = [ 0.50, 0.70, 0.45 ]
      dilution     = [ 3/6, 4/6, 5/6, 6/6 ]

      forestcolor  = darken(forestcolor, 0.8)

      megahexcolor = [ 1.00, 1.00, 1.00 ]
      megahexalpha = 0.08

      if style == "tropicalforest":
        _allforest    = True
        _wilderness   = False
        _maxurbansize = 4                
      elif style == "summerborealforest":
        _allforest    = True
        _wilderness   = True
        _maxurbansize = 0

    else:

      raise RuntimeError("invalid map style %r." % style)

    level0color = lighten(basecolor, dilution[0])
    level1color = lighten(basecolor, dilution[1])
    level2color = lighten(basecolor, dilution[2])
    level3color = lighten(basecolor, dilution[3])

    if style == "original":
      level1color       = [ 0.87, 0.85, 0.78 ]
      level2color       = [ 0.82, 0.75, 0.65 ]
      level3color       = [ 0.77, 0.65, 0.55 ] 

    level1ridgecolor = level2color
    level2ridgecolor = level3color

    if _frozen:
      watercolor = lighten([ 0.85, 0.85, 0.85 ], 1/20)
      wateroutlinecolor = watercolor
    else:        
      watercolor = [ 0.77, 0.89, 0.95 ]
      # Darken the water to 100% of the grey value of level 0. Do not lighten it.
      watergrayvalue  = equivalentgray(watercolor)[0]
      targetgrayvalue = 1.00 * equivalentgray(level0color)[0]
      if watergrayvalue > targetgrayvalue:
        watercolor = darken(watercolor, targetgrayvalue / watergrayvalue)
      wateroutlinecolor = darken(watercolor, 0.80)

    urbancolor        = equivalentgray(level0color)
    urbanoutlinecolor = darken(urbancolor, 0.7)
    roadcolor         = urbancolor
    roadoutlinecolor  = urbanoutlinecolor
    dockcolor         = urbancolor
    dockoutlinecolor  = urbanoutlinecolor

    hexcolor = urbanoutlinecolor
    hexalpha = 1.0
  
    labelcolor = urbanoutlinecolor

  if allforest != None:
    _allforest = allforest
  if forest != None:
    _forest = forest
  if wilderness != None:
    _wilderness = wilderness
  if rivers != None:
    _rivers = rivers
  if maxurbansize != None:
    _maxurbansize = maxurbansize

  if _allforest:
    hexcolor = darken(hexcolor, 0.7)
  if _frozen:
    forestalpha += 0.20

def startdrawmap(show=False):

  """
  Draw the map.
  """

  def toxy(sheet, x, y):
    XX = int(x)
    YY = int(y)
    dx = x - XX
    dy = y - YY
    x0, y0 = aphexcode.toxy(XX * 100 + YY, sheet=sheet)
    return x0 + dx, y0 - dy

  def drawhexes(sheet, hexcodes, **kwargs):
    for h in hexcodes:
      apdraw.drawhex(*aphexcode.toxy(h, sheet=sheet), zorder=0, **kwargs)
          
  def drawpaths(sheet, paths, **kwargs):
    for path in paths:
      xy = [toxy(sheet, *hxy) for hxy in path]
      x = [xy[0] for xy in xy]
      y = [xy[1] for xy in xy]
      apdraw.drawlines(x, y, zorder=0, **kwargs)

  global _saved
  if _saved:
    apdraw.restore()
    return

  if _xmax != None and _ymax != None:
    apdraw.setcanvas(_xmin, _ymin, _xmax, _ymax, dotsperhex=_dotsperhex)
  else:
    apdraw.setcanvas(_xmin, _ymin, _nxsheetgrid * _dxsheet, _nysheetgrid * _dysheet, dotsperhex=_dotsperhex)

  if _drawterrain:

    if _allwater:

      # Draw the sheets and level 0.
      for sheet in sheets():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        apdraw.drawrectangle(xmin, ymin, xmax, ymax, linewidth=0, fillcolor=watercolor, zorder=0)

      # Draw the megahexes.
      for sheet in sheets():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        for ix in range(0, _dxsheet):
          for iy in range(0, _dysheet):
            x = xmin + ix
            y = ymin + iy
            if ix % 2 == 1:
              y -= 0.5
            if (x % 10 == 0 and y % 5 == 0) or (x % 10 == 5 and y % 5 == 2.5):
              apdraw.drawhex(x, y, size=5, linecolor=megahexcolor, linewidth=megahexwidth, alpha=megahexalpha)
              
    else:

      # Draw the sheets and level 0.
      for sheet in sheets():
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        base = _terrain[sheet]["base"]
        if base == "water":
          apdraw.drawrectangle(xmin, ymin, xmax, ymax, linewidth=0, fillcolor=watercolor, zorder=0)
        else:
          apdraw.drawrectangle(xmin, ymin, xmax, ymax, linewidth=0, fillcolor=level0color, zorder=0)
          if _allforest:
            apdraw.drawrectangle(xmin, ymin, xmax, ymax, \
              hatch=foresthatch, linecolor=forestcolor, alpha=forestalpha, linewidth=0, fillcolor=None, zorder=0)
      
      for sheet in sheets():

        # Draw level 0.
        drawhexes(sheet, _terrain[sheet]["level0hexes"], linewidth=0, fillcolor=level0color)

        # Draw level 1.
        drawhexes(sheet, _terrain[sheet]["level1hexes"], linewidth=0, fillcolor=level1color)

        # Draw level 2.
        drawhexes(sheet, _terrain[sheet]["level2hexes"], linewidth=0, fillcolor=level2color)

        # Draw the ridges.
        drawpaths(sheet, _terrain[sheet]["level1ridges"], color=level1ridgecolor, linewidth=ridgewidth)
        drawpaths(sheet, _terrain[sheet]["level2ridges"], color=level2ridgecolor, linewidth=ridgewidth)

        if _allforest:

          drawhexes(sheet, _terrain[sheet]["level0hexes"], linewidth=0, linecolor=forestcolor, 
              hatch=foresthatch, alpha=forestalpha)
          drawhexes(sheet, _terrain[sheet]["level1hexes"], linewidth=0, linecolor=forestcolor, 
              hatch=foresthatch, alpha=forestalpha)
          drawhexes(sheet, _terrain[sheet]["level2hexes"], linewidth=0, linecolor=forestcolor, 
              hatch=foresthatch, alpha=forestalpha)
            
        elif _forest:

          # Draw the forest areas.
          drawhexes(sheet, _terrain[sheet]["foresthexes"], linewidth=0, linecolor=forestcolor, 
              hatch=foresthatch, alpha=forestalpha)

        if not _wilderness:

          # Draw the road clearings.
          drawpaths(sheet, _terrain[sheet]["clearingpaths"], color=level0color, linewidth=clearingwidth)

          # Draw the urban areas.

          townhexes = []
          if _maxurbansize >= 1:
            townhexes += _terrain[sheet]["town1hexes"]
          if _maxurbansize >= 2:
            townhexes += _terrain[sheet]["town2hexes"]
          if _maxurbansize >= 3:
            townhexes += _terrain[sheet]["town3hexes"]
          if _maxurbansize >= 4:
            townhexes += _terrain[sheet]["town4hexes"]
          if _maxurbansize >= 5:
            townhexes += _terrain[sheet]["town5hexes"]
          drawhexes(sheet, townhexes, linewidth=0, fillcolor=None, linecolor=urbanoutlinecolor, hatch=townhatch)

          if _maxurbansize >= 5:
            drawhexes(sheet, _terrain[sheet]["cityhexes"], linewidth=0, fillcolor=urbancolor, linecolor=urbanoutlinecolor, hatch=cityhatch)

      if _rivers:

        # Draw water and rivers.

        for sheet in sheets():
          # Do not outline sea hexes.
          drawhexes(sheet, _terrain[sheet]["lakehexes"], fillcolor=watercolor, linecolor=wateroutlinecolor, linewidth=waterourlinewidth)
          drawpaths(sheet, _terrain[sheet]["riverpaths"], color=wateroutlinecolor, linewidth=riverwidth+waterourlinewidth, capstyle="projecting")
          drawpaths(sheet, _terrain[sheet]["wideriverpaths"], color=wateroutlinecolor, linewidth=wideriverwidth+waterourlinewidth, capstyle="projecting")
            
        for sheet in sheets():
          drawhexes(sheet, _terrain[sheet]["seahexes"], linewidth=0, fillcolor=watercolor)
          drawhexes(sheet, _terrain[sheet]["lakehexes"], fillcolor=watercolor, linewidth=0)
          drawpaths(sheet, _terrain[sheet]["riverpaths"], color=watercolor, linewidth=riverwidth, capstyle="projecting")
          drawpaths(sheet, _terrain[sheet]["wideriverpaths"], color=watercolor, linewidth=wideriverwidth, capstyle="projecting")

      for sheet in sheets():
        # Draw the megahexes.
        xmin, ymin, xmax, ymax = sheetlimits(sheet)
        for ix in range(0, _dxsheet):
          for iy in range(0, _dysheet):
            x = xmin + ix
            y = ymin + iy
            if ix % 2 == 1:
              y -= 0.5
            if (x % 10 == 0 and y % 5 == 0) or (x % 10 == 5 and y % 5 == 2.5):
              apdraw.drawhex(x, y, size=5, linecolor=megahexcolor, linewidth=megahexwidth, alpha=megahexalpha, zorder=0)

      if not _wilderness:

        if _rivers:

          # Draw the bridges.
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["smallbridgepaths"], color=urbanoutlinecolor, linewidth=bridgeouterwidth, capstyle="butt")  
            drawpaths(sheet, _terrain[sheet]["smallbridgepaths"], color=urbancolor, linewidth=bridgeinnerwidth, capstyle="butt")  
            drawpaths(sheet, _terrain[sheet]["smallbridgepaths"], color=roadcolor, linewidth=roadwidth, capstyle="projecting")
            drawpaths(sheet, _terrain[sheet]["largebridgepaths"], color=urbanoutlinecolor, linewidth=bridgeouterwidth, capstyle="butt")  
            drawpaths(sheet, _terrain[sheet]["largebridgepaths"], color=urbancolor, linewidth=bridgeinnerwidth, capstyle="butt")  
            drawpaths(sheet, _terrain[sheet]["largebridgepaths"], color=roadcolor, linewidth=roadwidth, capstyle="projecting")

          # Draw the roads.
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["roadpaths"], color=roadoutlinecolor, linewidth=roadwidth+roadoutlinewidth, capstyle="projecting")
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["roadpaths"], color=roadcolor, linewidth=roadwidth, capstyle="projecting")

          # Draw the docks.
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["dockpaths"], color=dockoutlinecolor, linewidth=dockwidth+dockoutlinewidth, capstyle="projecting")
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["dockpaths"], color=dockcolor, linewidth=dockwidth, capstyle="projecting")

        if not _allforest:

          # Draw the runways and taxiways.
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["runwaypaths"], color=roadoutlinecolor, linewidth=runwaywidth+roadoutlinewidth, capstyle="projecting")
            drawpaths(sheet, _terrain[sheet]["taxiwaypaths"], color=roadoutlinecolor, linewidth=taxiwaywidth+roadoutlinewidth, joinstyle="miter", capstyle="projecting")
            drawpaths(sheet, _terrain[sheet]["runwaypaths"], color=roadcolor, linewidth=runwaywidth, capstyle="projecting")
            drawpaths(sheet, _terrain[sheet]["taxiwaypaths"], color=roadcolor, linewidth=taxiwaywidth, joinstyle="miter", capstyle="projecting")
            
        if _rivers:

          # Draw the dams.
          for sheet in sheets():
            drawpaths(sheet, _terrain[sheet]["dampaths"], color=roadoutlinecolor, linewidth=damwidth+roadoutlinewidth, capstyle="projecting")
            drawpaths(sheet, _terrain[sheet]["dampaths"], color=roadcolor, linewidth=damwidth, capstyle="projecting")
      
  # Draw missing sheets.
  for iy in range (0, _nysheetgrid):
    for ix in range (0, _nxsheetgrid):
      if _sheetgrid[iy][ix] == "--":
        xmin = ix * _dxsheet
        xmax = xmin + _dxsheet
        ymin = iy * _dysheet
        ymax = ymin + _dysheet
        apdraw.drawrectangle(xmin, ymin, xmax, ymax, linecolor=None, fillcolor=missingcolor, zorder=0)
            
  # Draw and label the hexes.
  for sheet in sheets():
    xmin, ymin, xmax, ymax = sheetlimits(sheet)
    for ix in range(0, _dxsheet + 1):
      for iy in range(0, _dysheet + 1):
        x = xmin + ix
        y = ymin + iy
        if ix % 2 == 1:
          y -= 0.5
          #aphexode.yoffsetforoddx()
        # Draw the hex if it is on the map and either its center or the center 
        # of its upper left edge are on this sheet.
        if isonmap(x, y) and (isonsheet(sheet, x, y) or isonsheet(sheet, x - 0.5, y + 0.25)):
          apdraw.drawhex(x, y, linecolor=hexcolor, alpha=hexalpha, linewidth=hexwidth, zorder=0)
          if _drawlabels:
            apdraw.drawhexlabel(x, y, aphexcode.fromxy(x, y), color=hexcolor, alpha=hexalpha, zorder=0)
            
  if _drawlabels:

    # Label the sheets.
    for sheet in sheets():
      xmin, ymin, xmax, ymax = sheetlimits(sheet)
      dx = 1.0
      dy = 0.5
      if isonmap(xmin + dx, ymin + dy):
        apdraw.drawtext(xmin + dx, ymin + dy, 90, sheet, dy=-0.05, size=24, color=labelcolor, alpha=1, zorder=0)

    # Draw the compass rose in the bottom sheet in the leftmost column.
    for iy in range (0, _nysheetgrid):
      sheet = _sheetgrid[iy][0]
      xmin, ymin, xmax, ymax = sheetlimits(sheet)
      dx = 1.0
      dy = 1.5
      if sheet != "--" and isonmap(xmin + dx, ymin + dy):
        apdraw.drawcompass(xmin + dx, ymin + dy, apazimuth.tofacing("N"), color=labelcolor, alpha=1, zorder=0)
        break

  apdraw.save()
  _saved = True

def enddrawmap(turn):
  apdraw.show()
  if _writefile:
    apdraw.writefile("turn-%02d.png" % turn)

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
  Returns True if the hex coordinate (x, y) is on the specified sheet.
  Otherwise returns false. The sheet must be in the map.
  """

  assert sheet in sheets()

  xmin, ymin, xmax, ymax = sheetlimits(sheet)

  if _rightedgeonmap[sheet] and _loweredgeonmap[sheet]:
    return xmin < x and x <= xmax and ymin <= y and y < ymax
  elif _rightedgeonmap[sheet]:
    return xmin < x and x <= xmax and ymin < y and y < ymax
  elif _loweredgeonmap[sheet]:
    return xmin < x and x < xmax and ymin <= y and y < ymax
  else:
    return xmin < x and x < xmax and ymin < y and y < ymax

def tosheet(x, y):

  """
  Returns the sheet containing the hex coordinates (x, y). If no sheet contains 
  the coordinates, returns None.
  """

  for sheet in sheets():
    if isonsheet(sheet, x, y):
      return sheet
  return None
  
def isonmap(x, y):

  """
  Returns True if the hex coordinate (x, y) is on the map. 
  Otherwise returns false.
  """

  return tosheet(x, y) != None and (_xmin < x and x < _xmax and _ymin < y and y < _ymax)

def altitude(x, y, sheet=None):

  """
  Returns the altitude of the hex at the position (x, y), which must refer to a
  hex center.
  """

  assert aphex.isvalid(x, y)

  if aphex.iscenter(x, y):

    if _allwater:
      return 0

    if sheet is None:
      sheet = tosheet(x, y)
    h = int(aphexcode.fromxy(x, y, sheet=sheet))
    if h in _terrain[sheet]["level2hexes"]:
      return 2
    elif h in _terrain[sheet]["level1hexes"]:
      return 1
    else:
      return 0

  else:

    x0, y0, x1, y1 = aphex.sidetocenters(x, y)
    sheet0 = tosheet(x0, y0)
    sheet1 = tosheet(x1, y1)
    assert sheet0 != None or sheet1 != None
    if sheet0 == None:
      sheet0 = sheet1
    if sheet1 == None:
      sheet1 = sheet0
    return max(altitude(x0, y0, sheet=sheet0), altitude(x1, y1, sheet=sheet1))

################################################################################

_terrain = {
  "A1": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [
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
    ],
    "town1hexes": [
        2113,
        2407,
        2911,
    ],
    "town2hexes": [
        1402, 1403,
    ],
    "town3hexes": [
        2603, 2701, 2702,
        2615, 2714, 2715,
    ],
    "town4hexes": [],
    "town5hexes": [
        1602, 1604, 1605,
        1701, 1702, 1703, 1704, 1705,
        1802,
        1901, 1902, 1903,
    ],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [
        [[20.00, 0.50],[20.00, 3.00],[21.00, 4.00],[28.00, 8.00],[28.67, 9.00],
              [27.33,10.50],[29.50,13.75],[29.50,14.75],[30.00,16.00],[30.50,16.25],],
        [[19.00,15.00],[20.00,16.00],[20.00,16.50],],
        [[ 9.67, 0.00],[10.00, 1.00],[11.00, 1.00],[11.50, 0.75],],
    ],
    "wideriverpaths": [],
    "clearingpaths": [
        [[15.00,15.00],[15.00,14.00],[18.00,13.00],[18.00,10.00],],
        [[18.00,12.00],[21.00,13.00],],
    ],
    "roadpaths": [
        [[15.00, 0.50],[15.00, 9.00],[14.50, 9.75]],
        [[10.00, 6.00],[12.00, 5.00],[12.00, 4.00],[13.00, 3.00],[17.00, 5.00],[19.00, 4.00],[19.00, 2.00],],
        [[19.00, 4.00],[25.00, 7.00],[25.00,15.50],],
        [[10.00,11.00],[13.00, 9.00],[14.00,10.00],[16.00, 9.00],[18.00,10.00],[18.00,13.00],[15.00,14.00],[15.00,15.50],],
        [[18.00,11.00],[18.00,12.00],[21.00,13.00],],
        [[23.00, 6.00],[24.00, 7.00],[26.00, 6.00],],
        [[25.00, 0.50],[25.00, 3.00],[26.00, 4.00],[26.00, 6.00],[28.00, 5.00],[30.00, 6.00],],
        [[30.00,11.00],[29.00,11.00],],
        [[27.00,15.50],[27.00,15.00],],
        [[27.00, 0.50],[27.00, 1.00],],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
        [[24.75, 6.625],[25.25, 5.875],],   # 2506
    ],
    "largebridgepaths": [],
    "runwaypaths": [
        [[12.63, 4.50],[13.80, 5.75],]
    ],
    "taxiwaypaths": [
        [[12.70, 4.60],[13.20, 4.10],[13.00, 4.60],]
    ],
    "dampaths": [],
  },
  "B1": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [
        3309, 
        3407, 3408, 3409,
        3506, 3507, 3508, 3509,
        3607, 3608, 3609,
        3707, 3708,
    ],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [
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
    ],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [
        4708, 4808, 4908,
    ],
    "town4hexes": [],
    "town5hexes": [
        3513, 3514, 3614, 3615, 3713,      
    ],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [
        [[29.67, 0.00],[30.00, 1.00],[31.00, 1.00],[31.00, 2.00],[32.00, 3.00],
         [33.00, 2.00],[34.00, 3.00],[34.33, 3.50],[35.67, 3.00],[36.00, 3.00],
         [36.00, 2.00],[37.00, 1.00],[38.00, 2.00],[38.00, 3.00],[39.00, 3.00],
         [40.00, 3.00],[40.00, 0.50],],
        [[30.00,16.00],[32.00,15.00],[38.00,15.00],[39.00,14.00],[40.00,15.00],
         [40.00,16.00],],
        [[40.00,16.50],[40.00,15.00],[39.00,14.00],[39.00,13.00],[42.00,12.00],
         [45.00,13.00],[47.00,13.00],[49.00,14.00],[50.00,16.00],[50.50,16.25],],
    ],
    "wideriverpaths": [],
    "clearingpaths": [
        [[31.00, 6.00],[34.00, 5.00],],
        [[35.00, 0.50],[35.00, 2.50],],
    ],
    "roadpaths": [
        [[30.00, 6.00],[31.00, 6.00],[35.00, 4.00],[35.00, 0.50],],
        [[33.00, 5.00],[34.00, 5.00],[38.00, 7.00],[38.00,12.00],[36.00,13.00],[35.00,12.00],[32.00,14.00],[31.00,13.00],[31.00,12.00],[32.00,12.00],[32.00,11.00],[31.00,10.00],[30.00,11.00],],
        [[35.00,15.50],[35.41,14.875],[36.00,15.375],[36.00,13.00],],
        [[45.00, 0.50],[45.00,15.50],],
        [[47.00,15.50],[47.00,11.00],[45.00,10.00],[45.00, 9.00]],
        [[45.00, 8.00],[45.00, 9.00],[46.00,10.00],[46.00,11.00],[47.00,11.00]],
        [[45.00, 8.00],[45.00, 9.00],[46.30,10.150],[46.30,11.150],[47.00,11.00]],
        [[45.00, 8.00],[45.00, 9.00],[46.15,10.075],[46.15,11.075],[47.00,11.00]],
        [[45.00, 8.00],[45.00, 9.00],[45.85, 9.425],[45.85,10.425],[47.00,11.00]],
        [[45.00, 8.00],[45.00, 9.00],[45.70, 9.350],[45.70,10.350],[47.00,11.00]],
        [[47.00,11.00],[48.00,12.00],[50.00,11.00],],
        [[47.00, 0.50],[47.00, 1.00],[48.00, 2.00],[48.00, 4.00],[49.00, 4.00],[49.00, 7.00],[48.00, 8.00],],
        [[50.00, 6.00],[49.00, 6.00],[49.00, 6.50]],
   ],
    "dockpaths": [],
    "smallbridgepaths": [
        [[36.00,14.75 ],[36.00,15.25 ],],   # 3615
    ],
    "largebridgepaths": [
        [[35.00, 2.75 ],[35.00, 3.25 ],],   # 3503 - original
        [[45.00,12.75 ],[45.00,13.25 ],],   # 4513 - original
        [[47.00,12.75 ],[47.00,13.25 ],],   # 4713 - original
    ],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C1": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [
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
    ],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [
      6502, 6503,
      6602, 6603, 6605, 6608,
      6701, 6702, 6703, 6704, 6705, 6706, 6707, 6708,
      6802, 6803, 6804, 6805, 6806, 6807, 6808, 6809,
      6903, 6904, 6905, 6906, 6907, 6908, 6909,
      6611, 6612, 6613, 6614, 
      6710, 6711, 6712, 6713, 6714,
      6811, 6813, 6814, 6815,
      6913, 6914, 6915,
    ],
    "town1hexes": [
        5110,
        5215,
        6105,
    ],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [
        6514, 6515, 6615, 6715,
    ],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [
        [[49.67, 0.00],[50.00, 1.00],[51.00, 1.00],[51.00, 3.00],],
        [[51.00, 3.00],[51.00, 2.00],[52.00, 2.00],[53.00, 2.00],],
        [[60.00, 0.50],[60.00, 1.25],[61.00, 1.00],[61.00, 3.00],[60.00, 4.00],
          [60.00, 6.00],[63.00, 7.00],[63.00, 8.00],[60.00,10.00],[55.00, 7.00],
          [54.00, 8.00],[54.00, 8.00],[54.00, 9.00],[55.00, 9.00],[55.00,11.00],
          [54.00,12.00],[54.00,13.00],[51.00,14.00],[50.00,16.00],],
        [[60.00,16.50],[60.00,15.00],[61.00,14.00],[63.00,15.00],[65.00,14.00],
         [65.00,13.00],[66.00,13.00],[66.50,13.25],[66.50,13.75],[66.00,14.00],[66.00,15.00],
         [67.00,15.00],[68.00,15.00],[68.00,14.00],[68.50,13.75],[69.00,13.50],[69.00,14.00],
         [70.00,16.00],[70.50,16.25],],
    ],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [
        [[50.00, 6.00],[51.00, 6.00],[51.00, 7.00],[51.50, 7.25],[53.00, 7.25],[53.00,10.00],[52.00,11.00],[51.00,10.00],[50.00,11.00],],
        [[52.00,11.00],[52.00,12.00],[53.00,12.00],[53.00,14.00],[55.00,15.00],[55.00,15.50],],
        [[53.00,14.00],[52.00,15.00],],
        [[55.00, 0.50],[55.00, 2.00],[54.00, 3.00],[54.00, 4.00],[58.00, 6.00],
              [58.00, 7.00],[60.00, 8.00],[60.00,12.00],[61.00,12.00],[62.00,12.00],
              [63.00,12.00],[64.00,13.00],[64.00,14.00],[65.00,14.00],
              [65.38,14.19],
              [65.00,14.78],[65.00,15.50],],
        [[65.00, 0.50],[65.00, 1.00],[63.00, 2.00],[63.00, 4.00],[59.00, 6.00],[59.00, 7.00],[59.50, 7.25]],
        [[63.00, 4.00],[65.00, 5.00],[65.00, 6.00],[66.00, 7.00],[69.00, 5.00],[70.00, 6.00],],
        [[64.00,13.00],[67.00,11.00],[68.00,12.00],[70.00,11.00],],
        [[67.00,15.50],[67.00,15.17],],
        [[63.50, 1.75],[64.00, 2.00],[65.00, 2.00],[67.00, 1.00],[67.00, 0.50],],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
        [[53.00,12.75 ],[53.00,13.25 ],],   # 5313
        [[60.00, 9.75 ],[60.00,10.25 ],],   # 6010
        [[59.75, 5.625],[60.25, 5.875],],   # 6006
        [[64.75,14.375],[65.25,14.125],],   # 6514
    ],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "D1": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "A2": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [
        2921,
    ],
    "town2hexes": [
        1516, 1617,
    ],
    "town3hexes": [],
    "town4hexes": [
        1721, 1722, 1822, 1823, 
        2020, 2021, 2120, 2121, 
        2529, 2628, 2629, 2728,
        2618, 2717, 2718, 2818,      
    ],
    "town5hexes": [],
    "cityhexes": [
        1121, 1125,
        1220, 1221, 1222, 1224, 1225, 1226,
        1320, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328,
        1421, 1422, 1423, 1424, 1425, 1426, 1427, 1428, 1429, 1430,
        1519, 1520, 1521, 1522, 1523, 1524, 1525, 1526, 1527,
        1620, 1621, 1622, 1623, 1624, 1625, 1626, 1627, 1628, 1629, 1630,
        1720, 1721, 1722, 1723, 1724, 1725, 1726, 1727, 1728, 1729,
        1822, 1823,1824, 1825, 1826, 1827, 1828, 
        1922, 1923, 1924, 1925, 1926, 1927,
        2028, 2029,
        1919,
        2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027,
        2120, 2121, 2122, 2123, 2124, 2125, 2126, 2127,
        2222,  
    ],
    "lakehexes": [
        1219, 1319, 1420,
    ],
    "riverpaths": [
        [[20.00,15.50],[20.00,16.50],],
        [[29.50,29.75],[30.00,31.00],[30.50,31.25],],
        [[13.83,19.75],[14.33,20.50],[16.33,21.50],],
        [[17.33,23.50],[17.67,24.00],],
    ],
    "wideriverpaths": [
      [[ 9.67,15.00],[10.00,16.00],[11.00,16.00],[12.00,16.50],
         [19.00,19.50],[19.50,20.25],[19.67,21.50],
         [20.00,23.50],[20.00,27.00],[20.67,28.00],[20.67,29.00],[20.00,30.00],[20.00,31.50]],
      [[15.00,17.50],
         [16.00,18.50],[18.50,22.25],[19.50,21.75],
         [20.00,23.50],[20.00,24.00],],
    ],
    "clearingpaths": [],
    "roadpaths": [
        [[15.00,15.50],[15.00,16.00],],
        [[10.00,21.00],[15.00,23.00],[10.00,26.00],],
        [[15.00,30.50],[15.00,21.00],],
        [[15.00,25.00],[15.00,24.00],[17.00,23.00],[18.00,24.00],[18.00,28.00],],
        [[15.00,19.00],[15.00,20.00],[17.00,21.00],[17.00,22.00],[19.00,23.00],[19.00,27.00],],
        [[15.00,23.00],[24.00,19.00],[24.00,18.00],[27.00,16.00],[27.00,15.50],],
        [[22.00,20.00],[21.00,20.00],[21.00,26.00],],
        [[25.00,15.50],[25.00,17.00],[24.50,17.75]],
        [[22.00,18.75],[22.00,20.00],[25.00,21.00],[25.00,23.00],[30.00,26.00],],
        [[22.15,18.75],[22.15,19.35],[21.85,18.85],[21.85,18.25],[22.15,18.75],],
        [[21.70,18.25],[22.30,18.75],[22.30,18.75],[22.30,19.35],[21.70,18.85],[21.70,18.25],[22.30,18.75],],
        [[21.00,24.00],[21.00,25.00],[25.00,27.00],[25.00,30.50],],
        [[27.00,30.50],[27.00,30.00],[25.00,29.00],[25.00,28.00]],
        [[25.00,30.00],[25.00,29.00],[27.00,28.00],[27.00,24.00],[26.00,24.00]],
        [[29.00,21.00],[30.00,21.00],],
    ],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [
        [[17.65,21.675],[20.35,20.825],],   # 1822/1921/2012 - original
    ],
    "runwaypaths": [
        [[22.60,23.25],[25.40,24.25],],
        [[23.00,22.60],[23.00,25.40],],
    ],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "B2": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [
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
    ],
    "level2hexes": [
        4320, 4321,
        4421, 4422, 4423,
        4521, 4522, 4523, 4524, 4525,
        4622, 4623, 4624, 4625,
        4722      
    ],
    "level1ridges": [
        [[45.00,25.50],[45.00,27.00],[44.00,28.00],[43.33,28.50],],
    ],
    "level2ridges": [
        [[44.33,21.50],[45.00,22.00],[46.00,23.00],[46.00,24.00],[45.00,24.00],[45.00,25.50],],
    ],
    "foresthexes": [
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
    ],
    "town1hexes": [
        3227,
        3630,
    ],
    "town2hexes": [
      3318, 3418,
      4924, 4925,
    ],
    "town3hexes": [],
    "town4hexes": [
        4728, 4729, 4829, 4830,
    ],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [
        [[29.67,15.00],[30.00,16.00],[33.00,17.00],[33.00,18.00],
          [34.00,19.00],[36.00,18.00],[37.00,18.00],[37.00,19.00],[39.00,20.00],
          [39.00,22.00],[38.00,23.00],[36.00,22.00],[35.00,22.00],[35.00,24.00],
          [37.00,25.00],[37.00,26.00],[35.00,27.00],[35.00,29.00],[36.00,30.00],
          [38.00,29.00],[40.00,30.00],[40.00,31.50],],
        [[35.00,27.00],[34.50,27.25],[31.50,26.75],[31.00,27.00],[31.00,29.00],
          [30.00,31.00],[29.67,30.00],],
        [[50.50,31.25],[50.00,31.00],[49.50,29.75],[49.50,29.25],[47.00,28.00],
          [47.00,27.00],[48.50,26.75],[48.50,24.00],],
        [[47.00,26.00],[48.00,27.00],[48.50,26.75],[48.50,24.00],],
        [[48.00,26.00],[48.50,26.25],[48.50,26.75],[48.00,27.00],],
        [[40.00,15.50],[40.00,16.25],[41.00,16.00],],
        [[40.00,15.50],[40.00,17.00],[41.00,17.00],
          [41.00,18.25],[40.00,19.25],[39.00,18.25],
          [38.00,19.25],[38.00,20.00],[39.00,20.00],[39.00,21.00],],
        [[39.00,18.25],[41.00,17.25],[41.00,17.00],[40.00,17.00],[40.00,15.50]],
    ],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [
        [[30.00,21.00],[31.00,20.00],[31.00,18.50],[31.50,17.75],[32.35,18.25],[32.625,18.688],[33.00,18.00],[35.00,17.00],[35.00,15.50]],
        [[45.00,15.50],[45.00,16.00],[42.00,18.00],[42.00,19.00],[41.00,19.00],[41.00,21.00],[43.00,22.00],[43.00,26.00],[42.00,27.00],[42.00,30.00],[43.00,30.00],[44.00,30.00],[45.00,30.00],[45.00,30.50],],
        [[45.00,30.00],[47.00,29.00],[47.00,30.50],],
        [[47.00,15.50],[47.00,20.00],[49.00,21.00],[50.00,21.00],],
        [[49.00,21.00],[49.00,25.00],[50.00,26.00],],
        [[30.00,26.00],[32.00,27.00],],
        [[35.00,30.50],[35.00,30.00],[35.83,29.67],],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
        [[32.75,18.625],[33.25,17.875],],   # 3318
        [[36.00,14.75 ],[36.00,15.25 ],],   # 3615
    ],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C2": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [
      5217, 5218, 5219,
      5316, 5317, 5318, 5319,
      5417, 5418, 5419,
      5517, 5518,
      5617, 5618, 5619, 5620,
      5716, 5717, 5718, 5719, 5720,
      5817, 5818, 5819, 5820, 5821,
      5919, 5920, 5921,
      6025, 6026, 6027,
      6121, 6122, 6124, 6125, 6126, 6128,
      6220, 6221, 6222, 6223, 6224, 6225, 6226, 6228, 6229,
      6319, 6320, 6321, 6322, 6323, 6324, 6325, 6327, 6328, 6329,
      6420, 6421, 6422, 6423, 6424, 6425, 6427, 6428, 6429,
      6523, 6526,
    ],
    "level2hexes": [],
    "level1ridges": [
      [[52.50,17.25],[54.00,18.00],[54.67,18.00],],
      [[55.33,17.50],[56.00,18.00],[57.00,18.00],[57.00,19.00],[58.50,20.25],],
      [[63.00,19.50],[63.00,24.00],[60.50,25.75],],      
    ],
    "level2ridges": [],
    "foresthexes": [
      5221, 5222,
      5320, 5321,
      5420, 5421, 5422,
      5520, 5521,
      5621, 5622, 5623,
      5721, 5722, 5723,
      5822, 5823, 5824,
    ],
    "town1hexes": [
        5427,
    ],
    "town2hexes": [
        6630, 6730,
    ],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [
      6127, 6227,
    ],
    "riverpaths": [
      [[49.67,15.00],[50.00,16.00],[51.00,16.00],],
      [[60.00,15.50],[60.00,17.00],[59.00,17.00],[59.00,18.00],[59.50,18.25],
        [60.00,18.50],[60.00,18.00],[60.33,17.50],[61.00,17.00],
        [61.33,17.50],
        [61.00,18.00],[61.33,18.50],[62.00,19.00],[62.50,18.75],[63.50,18.25],
        [65.00,19.00],
        [65.00,22.00],
        [66.00,23.00],[66.00,24.00],[65.00,24.00],[65.00,25.00],[60.00,28.00],
        [60.00,31.50],],
      [[70.50,31.25],[70.00,31.00],[69.00,29.00],],      
    ],
    "wideriverpaths": [],
    "clearingpaths": [
        [[52.00,20.00],[53.00,20.00],[55.00,19.00],],
    ],
    "roadpaths": [
        [[55.00,15.50],[55.00,19.00],[53.00,20.00],[52.00,20.00],[50.00,21.00],],
        [[50.00,26.00],[54.00,28.00],[54.00,29.00],[55.00,29.00],[55.00,30.50],],
        [[54.00,28.00],[54.00,27.00],[60.00,24.00],[60.00,20.00],[61.25,18.875],[62.00,19.375],[62.00,18.00],[65.00,16.00],[65.00,15.50],],
        [[67.00,15.50],[67.00,17.50],[68.00,19.50],[68.00,21.00],[69.00,21.00],[70.00,21.00]],
        [[65.00,30.50],[65.00,29.00],[68.00,28.00],[68.00,22.00],[70.00,21.00],],
        [[68.00,24.00],[68.00,25.00],[70.00,26.00],],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
        [[62.00,18.75 ],[62.00,19.25 ],],   # 6219
    ],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [
      [[60.23,27.35],[60.77,28.15],]
    ],
  },
  "D2": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "A3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "B3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "D3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "A4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "B4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "D4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "A5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "B5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "D5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "A6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "B6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "D6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "A": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "B": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "C": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "D": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "E": {
    "base": "land",
    "seahexes": [
      25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
      126, 127, 128, 129, 130, 131, 132, 133, 146, 147, 148, 149, 150,
      225, 226, 227, 228, 229, 230, 231, 232, 233,
      325, 326, 327, 328, 330, 331, 332, 333,
      425, 426, 429, 430, 
      526,
      625,
      726,
      825,
      1025,
      1225,
      1325,
      1425, 1427,
      1526, 1528,
      1625, 1626, 1627,
      1726,
      1825,
      2025,      
    ],
    "level0hexes": [],
    "level1hexes": [
      1347, 1348, 1349,
      1445, 1446, 1447, 1448, 1449,
      1545, 1546, 1547, 1548, 1549, 1550,
      1644, 1645, 1646, 1647, 1648, 1649,
      1745, 1746, 1747, 1748, 1749,
      1843, 1844, 1845,
    ],
    "level2hexes": [],
    "level1ridges": [],
    "foresthexes": [
      950,
      1044, 1045, 1048, 1049,
      1144, 1145, 1146, 1147, 1148,
      1245, 1246,
      1341,
      1643, 1647, 1648,
      1742, 1743, 1744, 1748, 1749, 1750,
      1837, 1839, 1847, 1848, 1849,
      1938, 1939, 1947,
    ],
    "level2ridges": [],
    "town1hexes": [
      138,
      239,
      433,
      841,
      1339,
      1544
    ],
    "town2hexes": [],
    "town3hexes": [
      1447, 1547, 1548,
    ],
    "town4hexes": [
      1539, 1540, 1541, 1639,
      1733, 1734, 1833, 1934,

    ],
    "town5hexes": [
      746, 845, 846, 945, 946,
      246, 247, 248, 347, 348, 349, 449,
      634, 635, 636, 637, 736, 737, 836, 838, 839, 937, 938, 939, 1037, 1138, 1237, 1337,
      531, 532, 629, 630, 731, 733, 831, 832, 932,
    ],
    "cityhexes": [
      528, 529, 530, 627, 628, 727, 728, 729, 826, 827, 
      439, 539, 540, 541, 542, 639, 640, 641, 
      135, 136, 137, 234, 235, 236, 335, 334, 
      835, 935, 936, 1034, 1035, 1036, 1135, 1136, 1137,1234, 1235, 1236, 
      1335, 1336, 1434, 1435, 1436, 1535, 1536,
      930, 930, 931, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1128, 1129, 1130, 1131, 1132, 1229, 1230, 1231,
      1331, 1332, 1429, 1430, 1530, 1531, 1629, 1630, 1631, 1730, 1731,
      1826, 1827, 1828, 1829, 1830, 1927, 1928, 1929

    ],
    "lakehexes": [
       1834,
    ],
    "riverpaths": [
      [[18.00,34.00],[17.00,34.00],[17.00,33.00],[16.00,32.00],[14.00,33.00],
       [13.00,33.00],[11.00,34.00],[10.00,33.00],[ 8.00,34.00],[ 3.00,32.00],],
      [[16.00,43.00],[14.00,42.00],[10.00,44.00],[ 8.00,43.00],[ 7.00,44.00],
       [ 5.00,43.00],[ 4.00,43.00],[ 4.00,45.00],[ 1.00,47.00]],
      [[12.00,47.00],[11.50,47.25],[11.00,47.50],[11.00,49.00],[10.00,49.00],[10.00,50.00],],
    ],
    "wideriverpaths": [
      [[ 2.33,28.50],[ 2.66,28.00],[ 3.33,28.50],[ 3.66,29.00],
       [ 3.33,29.50],[ 2.66,29.00],[ 2.33,28.50]],
    ],
    "clearingpaths": [],
    "roadpaths": [
        [[ 5.00,50.50],[ 5.00,50.00],[ 2.00,48.00],[ 2.00,45.00],[ 1.00, 45.00],
         [ 1.00,40.00],[ 8.00,36.00],[15.00,40.00],[17.00,39.00],[20.00,40.00],
         [21.00,40.00]],
        [[15.00,50.00],[15.00,44.00]],
        [[20.00,45.00],[15.00,48.00],[10.00,45.00],[ 4.00,48.00],[ 4.00,49.00],[5.00,50.00]],
        [[20.00,35.00],[ 8.00,41.00],[ 8.00,46.00],[ 7.00,47.00]],
        [[ 9.00,39.00],[ 8.00,39.00],[ 8.00,45.00]],
        [[ 9.00,39.00],[ 8.00,39.00],[ 2.00,36.00],[ 1.00,37.00],[ 2.00,36.00],[ 2.00,35.00],],
        [[15.00,41.00],[15.00,36.00]],
        [[18.00,39.00],[17.00,39.00],[17.00,37.00],[18.00,36.00]],
        [[13.00,35.00],[13.00,32.00]],
        [[10.00,37.00],[ 9.00,37.00],[ 9.00,32.00],[10.00,31.00],[10.00,26.00]],
        [[ 4.00,28.00],[ 5.00,28.00],[10.00,30.00],[13.50,28.75],[16.50,28.25],
         [20.00,30.00]],
        [[ 5.00,31.00],[ 5.00,29.00],[ 6.00,28.00],[ 7.00,29.00]],
        [[17.00,27.00],[17.00,29.00],[18.00,29.00]],
        [[17.20,27.00],[17.20,29.10],[18.00,29.00]],
        [[16.80,26.50],[16.80,28.40],[18.00,29.00]],
        [[16.60,27.50],[16.60,28.30],[18.00,29.00]],

    ],
    "dockpaths": [
        [[ 0.75,47.00],[ 0.75,47.375],[ 1.50,48.25]],
        [[ 1.00,47.00],[ 1.50,47.25]],
    ],
    "smallbridgepaths": [
      [[ 8.00,42.75],[ 8.00,43.25]],
      [[ 2.00,45.75],[ 2.00,46.25]],
    ],
    "largebridgepaths": [
      [[ 9.00,33.75],[ 9.00,34.25]],
      [[13.00,32.75],[13.00,33.25]],
    ],
    "runwaypaths": [
      [[ 2.00,44.30],[ 2.00,41.00]],
      [[ 1.80,44.50],[ 3.20,41.90]]
    ],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "F": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "G": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "foresthexes": [],
    "level2ridges": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "H": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "foresthexes": [],
    "level2ridges": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "I": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "foresthexes": [],
    "level2ridges": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "J": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "K": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "foresthexes": [],
    "level2ridges": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
  "L": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [],
    "town1hexes": [],
    "town2hexes": [],
    "town3hexes": [],
    "town4hexes": [],
    "town5hexes": [],
    "cityhexes": [],
    "lakehexes": [],
    "riverpaths": [],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [],
    "dockpaths": [],
    "smallbridgepaths": [],
    "largebridgepaths": [],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
  },
}
