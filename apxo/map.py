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

tunnelinnerwidth = roadwidth + 8
tunnelouterwidth = tunnelinnerwidth + 6

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
  global level0ridgecolor, level1ridgecolor, level2ridgecolor
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
  cityhatch        = "xx"
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
    forestalpha = 0.5
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

    level0ridgecolor = level1color
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

        # Draw levels 0, 1, and 2.
        drawhexes(sheet, _terrain[sheet]["level0hexes"], linewidth=0, fillcolor=level0color)
        drawhexes(sheet, _terrain[sheet]["level1hexes"], linewidth=0, fillcolor=level1color)
        drawhexes(sheet, _terrain[sheet]["level2hexes"], linewidth=0, fillcolor=level2color)

        if not _wilderness:
          drawpaths(sheet, _terrain[sheet]["tunnelpaths"], color=roadoutlinecolor, linewidth=tunnelouterwidth, linestyle=(0,(0.3,0.3)))
          drawpaths(sheet, _terrain[sheet]["tunnelpaths"], color=level1color, linewidth=tunnelinnerwidth)

        # Draw the ridges.
        drawpaths(sheet, _terrain[sheet]["level0ridges"], color=level0ridgecolor, linewidth=ridgewidth)
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
    "level0ridges": [],
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
    "tunnelpaths": [],
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
    "level0ridges": [],
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
    "tunnelpaths": [],
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
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D1": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
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
    "tunnelpaths": [],
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
    "level0ridges": [],
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
    "tunnelpaths": [],
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
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D2": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "A3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "B3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "C3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D3": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "A4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "B4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "C4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D4": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "A5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "B5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "C5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D5": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "A6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "B6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "C6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D6": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "A": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "B": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "C": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "D": {
    "base": "water",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
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
    "level0ridges": [],
    "level1ridges": [],
    "level2ridges": [],
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
         [ 1.00,40.00],[ 8.00,36.00],[15.00,40.00],[17.00,39.00],
         [19.90,40.50],[20.00,40.00]],
        [[15.00,50.50],[15.00,44.00]],
        [[20.00,45.00],[19.90,45.50],
         [15.00,48.00],[10.00,45.00],[ 4.00,48.00],[ 4.00,49.00],
         [5.00,50.00]],
        [[20.00,35.00],[19.90,35.50],[17.00,37.00],
         [ 8.00,41.00],[ 8.00,46.00],[ 7.00,47.00]],
        [[ 9.00,39.00],[ 8.00,39.00],[ 8.00,45.00]],
        [[ 9.00,39.00],[ 8.00,39.00],[ 2.00,36.00],[ 1.00,37.00],[ 2.00,36.00],
         [ 2.00,35.00],],
        [[15.00,41.00],[15.00,36.00]],
        [[18.00,39.00],[17.00,39.00],[17.00,37.00],[18.00,36.00]],
        [[13.00,35.00],[13.00,32.00]],
        [[10.00,37.00],[ 9.00,37.00],[ 9.00,32.00],[10.00,31.00],[10.00,26.00]],
        [[ 4.00,28.00],[ 5.00,28.00],[10.00,30.00],[13.50,28.75],[16.50,28.25],
         [18.00,29.00],[19.90,30.50],[20.00,30.00]],
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
    "tunnelpaths": [],
  },
  "F": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [
      2126, 2127, 2128, 2129,
      2226, 2227, 2228, 2229, 2230,
      2328, 2329, 2330, 2331, 2338, 2339,
      2428, 2429, 2430, 2437, 2438, 2439,
      2525, 2534, 2535, 2536, 2537, 2538, 2539, 2540,
      2632, 2633, 2634, 2635, 2636,  2638, 2639, 2640, 2641,
      2732, 2733, 2734, 2735, 2741, 2742,
      2831, 2832, 2834, 2835, 2841, 2842, 2846,
      2936, 2937, 2939, 2940, 2945, 2946, 2947,
      3037, 3038, 3039, 3043, 3044, 3045, 3046, 3047,
      3132, 3133, 3134, 3138, 3139, 3140, 3147,
      3231, 3234, 3235,
      3332,
      3432, 3433, 3434, 3435, 3436,
      3535, 3536, 3548, 3549,
      3627, 3628, 3642, 3643, 3644, 3645, 3646, 3648, 3649,
      3727, 3728, 3729, 3730, 3743, 3744, 3745, 3746, 3747, 3748, 3749,
      3827, 3828, 3829, 3842, 3843, 3844, 3846, 3847, 3848,
      3944,
    ],
    "level2hexes": [
      2637,
      2736, 2737, 2738, 2739, 2740,
      2836, 2837, 2838, 2839, 2840, 
      2938,
      3232, 3233, 
      3333, 3334,
    ],
    "level0ridges": [
      [[33.67,32.00],[34.33,30.50],[35.33,30.50],[35.67,30.00],[35.67,29.00]],
      [[34.50,33.75],[38.00,32.00],[38.50,31.25],[38.50,29.25]],
    ],
    "level1ridges": [
      [[34.50,33.75],[34.00,34.00],[33.50,34.25]],
      [[33.50,34.25],[34.50,34.25],[34.50,35.75],[34.1,36.40]],
      [[27.00,36.00],[26.33,34.50],[26.33,33.50],[28.00,31.00]],
      [[25.50,37.75],[23.00,39.00],[22.50,38.50]],
      [[30.50,42.75],[30.00,43.00],[30.00,44.00],[28.50,44.75]],
      [[30.00,43.00],[30.00,45.00],[29.00,47.00],[28.50,46.75]],
      [[36.00,49.00],[37.00,49.00],[37.33,48.50],
       [37.33,46.50],[37.00,46.00],[37.00,44.00],[36.33,42.50]],
      [[38.00,43.00],[37.00,44.00],[37.00,45.00]],
      [[37.00,49.00],[36.00,48.00]]
    ],
    "level2ridges": [
      [[27.67,37.50],[27.67,39.00],[28.00,39.00],[28.00,40.25]],
    ],
    "foresthexes": [
      2130, 2131, 2132, 2135,
      2227, 2228, 2229, 2230, 2231, 2234, 2235,
      2327, 2328, 2329, 2330, 2331, 2341, 2342,
      2427, 2429, 2430, 2431, 2432, 2439, 2440,
      2529, 2530, 2531, 2532, 2540, 2541, 2542,
      2629, 2639, 2640, 2641,
      2741, 2742,
      2833, 2841, 2842, 2843,
      2934, 2941, 2942, 2943, 2944,
      3030, 3032, 3033, 3034, 3040, 3041, 3042,
      3131, 3132, 3133, 3134, 3135, 3142, 3143, 3144,
      3230, 3231, 3232, 3241, 3242, 3243, 3244,
      3331, 3332, 3333, 3340, 3341, 3342, 3343, 3344, 3348, 3349, 3350,
      3430, 3432, 3433, 3434, 3435, 3436, 3437, 3441, 3443, 3449,
      3532, 3534, 3535, 3536, 3544,
      3635,
    ],
    "town1hexes": [
      2528,
      2442,
      2643,
      2846,
      3527,
    ],
    "town2hexes": [
      2236, 2337,
      3840, 3941,
    ],
    "town3hexes": [
      3631, 3632, 3732,
    ],
    "town4hexes": [
      3637, 3737, 3738, 3836,
    ],
    "town5hexes": [
      2141, 2239, 2240, 2241, 2339,
    ],
    "cityhexes": [],
    "lakehexes": [
      2232,
    ],
    "riverpaths": [
      [[25.50,33.25],[25.00,33.00],[24.00,33.00],[23.00,33.00],[23.00,32.50],
       [22.70,31.75],[22.00,32.00]],
      [[30.00,25.00],[30.00,27.00],[31.00,28.00],[31.00,31.00],[29.00,32.00],
       [29.00,34.00],[31.00,35.00],[31.00,37.00],[30.00,36.00],[30.00,34.00],
       [31.00,35.00],
       [31.00,37.00],[32.00,37.00],[32.00,40.00],
       [29.50,41.75],[28.50,42.75],
       [28.00,43.00],[26.00,42.00],[25.00,43.00],[25.00,45.00],[27.00,46.00],
       [27.00,47.00],[28.00,47.00],[28.00,49.00],[29.00,50.00],
       [30.00,49.80],[30.00,50.50]],
      [[35.50,44.25],[34.00,43.00],[32.00,43.00],[29.25,42.13],[29.00,42.50]],
    ],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [
      [[35.00,25.50],[35.00,27.00]],
      [[25.00,25.50],[25.00,28.00],[20.05,30.00],[20.00,30.00]],
      [[25.00,27.00],[25.00,28.00],[28.00,29.00],[30.00,29.00],
       [30.60,29.50],[31.40,30.00],[33.00,29.00],[36.00,30.00],
       [36.00,33.00],[39.95,35.50],[40.00,35.00]],
      [[36.00,32.50],[36.00,32.00],[37.00,32.00],
       [39.90,30.50],[40.00,30.00]],
      [[37.00,34.00],[38.00,34.00],[38.00,36.00],[37.00,37.00],
       [36.00,36.00],[35.00,37.00],[35.00,38.00],[39.00,40.00],
       [39.00,45.00],[37.50,45.75]],
      [[39.00,44.00],[39.00,45.00],[39.90,45.50],[40.00,45.00]],
      [[39.00,42.00],[39.00,41.00],[39.90,40.50],[40.00,40.00]],
      [[35.00,37.00],[35.00,38.00],
       [34.50,37.75],
       [33.50,38.25],
       [32.50,36.25],
       [28.50,34.25],[27.50,34.75],
       [22.50,36.75],[22.00,37.50],
       [22.00,41.00],
       [24.00,42.00]],
      [[23.00,42.00],[21.00,41.00],[20.10,40.00],[20.00,40.00]],
      [[24.00,36.00],[23.00,37.00],[22.00,36.00],
       [20.10,35.00],[20.00,35.00]],
      [[25.00,50.50],[25.00,48.00],[21.00,46.00],
       [20.10,45.00],[20.00,45.00]],
      [[25.00,49.00],[25.00,48.00],
       [29.50,45.75],[30.50,45.25],[34.00,47.00],
       [34.00,48.50],[34.50,49.25],[35.00,50.40],[35.00,50.50]],
      [[27.00,47.00],[28.00,46.00],[28.00,44.50],[27.50,44.25],
       [26.00,43.00]],
      [[34.00,48.00],[34.00,47.00],[35.50,46.75]],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
    ],
    "largebridgepaths": [
      [[30.75,29.50],[31.25,30.00]],
      [[29.60,35.30],[31.40,36.20]],
    ],
    "runwaypaths": [],
    "taxiwaypaths": [],
    "dampaths": [],
    "tunnelpaths": [
      [[35.50,46.75],[37.50,45.75]],
    ],
  },
  "G": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [
      4146, 4147,
      4243, 4244, 4245, 4246, 4247,
      4344, 4345, 4346, 4347, 4348, 4349, 
      4446, 4447, 4448,
      4547, 4548,
      4648,
    ],
    "level2hexes": [],
    "level0ridges": [],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [
      4148, 4149,
      4243, 4247, 4248,
      4344, 4345, 4346, 4338,
      4433, 4436, 4444, 4445, 4446,
      4534, 4535, 4536, 4546,
      4634, 4635,
      4734,
      5349,
      5438, 5449,
      5539, 5540, 5549,
      5635, 5638, 5639, 5640, 5642, 5643, 5644, 5649,
      5735, 5741, 5742, 5743, 5744, 5745,
      5835, 5836, 5840, 5841, 5842, 5843, 5844,
      5935, 5936, 5938, 5940, 5941, 5943,
    ],
    "town1hexes": [
      4140,
      4538,
      4829,
      5436,
      5528,
      5550,
    ],
    "town2hexes": [],
    "town3hexes": [
      4934, 4935, 5034,
    ],
    "town4hexes": [],
    "town5hexes": [
      4437, 4438, 4537, 4539, 4639,
    ],
    "cityhexes": [
      4636, 4637, 4638,
      4736, 4737, 4738,
      4834, 4835, 4836,
    ],
    "lakehexes": [
      4929, 4930, 4931,
      5028, 5029, 5030, 5031,
      5130,
    ],
    "riverpaths": [
      [[50.00,25.00],[50.00,28.00]],
      [[50.00,30.00],[53.00,32.00],[53.00,33.00],
       [53.50,33.25],[54.50,32.75],
       [57.00,32.00]],
      [[57.00,33.00],[56.00,32.00],[55.00,33.00]],
      [[49.00,31.00],[47.00,32.00],[47.00,33.00],[48.50,33.25]],
      [[43.00,33.00],[43.00,32.50],
       [43.50,32.25],[46.00,33.00],
       [47.00,33.00],[47.00,32.50]],
      [[42.00,43.00],[42.50,42.75],[43.50,43.25],
       [44.00,43.00],[45.50,42.75],
       [46.00,42.50],[46.00,43.00]],
      [[43.00,45.00],[44.00,44.00],[44.00,43.00],[45.00,43.00]],
      [[50.00,50.00],[50.00,48.50],
       [52.00,45.50],[52.00,44.50],[52.50,43.75],
       [55.00,43.00],[56.00,43.00]],
    ],
    "wideriverpaths": [],
    "clearingpaths": [],
    "roadpaths": [
      [[40.00,30.00],[40.10,30.00],[41.00,30.00],[42.00,30.00],
       [46.00,28.00],[48.00,29.00]],
      [[45.00,25.50],[45.00,27.00],[44.00,27.00],[44.00,29.00],
       [43.00,30.00]],
      [[55.00,25.50],[55.00,28.00],[52.00,29.00],[52.00,29.50],
       [50.50,31.75],[50.00,32.50],[50.00,34.00],
       [55.50,37.25],[56.50,36.75],
       [59.90,35.50],[60.00,35.00]],
      [[54.00,28.00],[55.00,28.00],[56.00,28.00],[56.00,29.00],
       [57.50,30.25],[58.50,29.75],[59.00,30.00],[59.90,30.50],[60.00,30.00]],
      [[58.00,36.00],[57.00,37.00],[57.00,39.00],[58.00,39.00],
       [58.50,40.25],[59.00,41.00],
       [59.90,40.50],[60.00,40.00]],
      [[51.00,35.00],[50.00,34.00],[46.00,36.00],
       [45.33,36.00],[45.00,36.25],
       [45.00,40.50],[46.50,42.25],
       [49.50,44.25],[50.00,44.50],[50.00,45.00],
       [53.50,47.25],[55.50,47.25],[56.00,47.00],
       [59.90,45.50],[60.00,45.00]
       ],
      [[45.00,50.50],[45.00,50.00],[47.00,49.00],[47.00,47.00],
       [50.00,45.00],[51.00,46.00]],
      [[40.00,35.00],[40.10,35.00],[45.00,38.00],[45.00,39.00]],
      [[40.00,40.00],[40.10,40.00],[41.00,40.00],[45.00,38.00],[45.00,37.00]],
      [[40.00,45.00],[40.10,45.00],[41.00,45.00],[41.00,40.00],
       [42.00,39.00]],
      [[55.00,50.50],[55.00,48.50],[55.50,47.75],[57.00,47.00]],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
      [[51.50,46.25],[52.00,46.00]]
    ],
    "largebridgepaths": [
      [[51.10,31.35],[51.40,30.90]],
    ],
    "runwaypaths": [
      [[48.00,41.00],[52.00,39.00]],
      [[51.00,38.70],[51.00,42.20]],
      [[48.80,39.40],[52.20,41.10]],
    ],
    "taxiwaypaths": [],
    "dampaths": [],
    "tunnelpaths": [],
  },
  "H": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [
      [[61.00,28.00],[60.67,27.00],
       [61.00,27.00],[63.00,26.00],[64.00,26.00],
       [64.00,27.00],[62.00,28.00]],
      [[65.67,26.00],[65.33,27.50],[65.67,28.00],[66.33,27.50],
       [67.00,27.00],[66.33,25.50]],
      [[71.67,34.00],[71.67,35.00],[71.33,35.50],[70.67,35.00],
       [70.33,34.50],[70.67,31.00],[71.33,30.50]],
      [[72.33,30.50],[73.67,32.00],[73.67,33.00],[73.33,33.50],[72.67,33.00],[72.33,32.50]],
      [[73.00,29.00],[75.00,30.00],[77.00,29.00],[77.00,28.00]],
      [[73.00,28.00],[76.00,26.00],[76.50,26.25]],
      [[67.67,41.00],[67.33,41.50],[65.50,42.25],
       [65.00,42.00],[64.67,41.00],[64.33,40.50],[64.67,40.00],
       [65.33,40.50],[67.33,40.50]],
    ],
    "level1ridges": [],
    "level2ridges": [],
    "foresthexes": [
      6130, 6132, 6133, 6144, 6145,
      6229, 6230, 6231, 6232, 6233, 6242, 6244, 6245, 6246,
      6330, 6332, 6333, 6334, 6342, 6345, 6346,
      6428, 6430, 6442, 6446,
      6529, 6530, 6531,
      6629, 6633, 
      6733, 6734,
      6947, 6948,
      7047,
      7140,
      7239, 7240, 7242,
      7340, 7341, 7342, 7343,
      7440, 7441, 7442,
      7531, 7532, 7541, 7542, 7544,
      7631, 7632, 7633, 7640, 7644, 7645,
      7731, 7732, 7734, 7735, 7745, 7746, 
      7831, 7833, 7834, 7843, 7844, 7845,
    ],
    "town1hexes": [
      6344,
      6736,
      7046,
      7935,
      7548,
    ],
    "town2hexes": [
      7733, 7832,
      6845, 6945,
    ],
    "town3hexes": [
      6236, 6337, 6436,
    ],
    "town4hexes": [],
    "town5hexes": [
      6937, 6938, 7034, 7035, 7036, 7037, 7136, 7236, 7237, 7337,
    ],
    "cityhexes": [
      7137
    ],
    "lakehexes": [
      6135, 6136,
      6235,
      6343,
      6443, 6444,
      7643,
      7743, 7744,
    ],
    "riverpaths": [
      [[70.00,25.00],[70.00,26.00],[69.50,26.75],[69.50,27.25],[70.50,27.25]],
      [[62.00,35.00],[63.00,35.00],[63.00,34.00],[65.00,33.00],
       [66.00,33.00],[67.00,33.00]],
      [[75.00,34.00],
       [74.50,33.25],[74.50,32.75],
       [75.00,33.00],[75.00,32.00],[75.67,32.00],
       [76.00,32.00],[77.00,32.00]],
       [[61.00,43.00],[62.00,43.00],[63.00,43.00]],
       [[62.00,42.00],[63.00,43.00]],
       [[64.00,45.25],[64.00,44.00]],
      [[64.00,43.00],[67.00,42.00],[68.00,42.00],[71.00,41.00],[76.00,43.00]],
      [[77.00,44.50],[77.50,45.25],[78.00,45.00],[78.00,46.00],
       [76.00,47.00],[75.00,47.00],[73.50,47.75]],
      [[77.00,43.00],[78.00,42.00],[79.00,43.00],[79.50,42.75],[79.50,41.75]],
      [[70.00,50.00],[70.00,49.00],[70.50,48.75]],
    ],
    "wideriverpaths": [
      [[77.00,32.00],[76.50,31.75]],
    ],
    "clearingpaths": [],
    "roadpaths": [
      [[60.00,45.00],[60.10,45.00],[63.00,44.00]],
      [[75.00,50.50],[75.00,48.00],[70.00,45.00],[70.00,30.00],
       [65.00,28.00],[65.00,25.50]],
      [[65.00,50.50],[65.00,49.00],[66.00,48.00],[66.00,47.00],
       [70.00,45.00],[70.00,44.00]],
      [[75.00,48.00],[76.00,48.00],[79.00,47.00],[79.00,41.00],
       [79.90,40.50],[80.00,40.00]],
      [[79.00,46.50],[79.00,46.00],[79.90,45.50],[80.00,45.00]],
      [[79.00,42.00],[79.00,41.00],[78.00,40.00],
       [78.00,39.00],[70.00,35.00],[70.00,34.00]],
      [[79.00,35.00],[79.90,35.50],[80.00,35.00]],
      [[74.00,37.00],[75.00,38.00],[79.90,35.50],[80.00,35.00]],
      [[70.00,39.00],[70.00,38.00],[73.00,37.00],[74.00,37.00]],
      [[70.00,31.00],[70.00,30.00],[77.00,27.00],[79.00,28.00],
       [79.00,32.00],[77.00,33.00]],
      [[79.00,29.00],[79.00,30.00],[79.90,30.50],[80.00,30.00]],
      [[74.00,28.00],[75.00,28.00],[75.00,25.50]],
      [[67.00,29.00],[66.00,28.00],[61.00,31.00],[60.10,30.00],[60.00,30.00]],
      [[60.00,40.00],[60.10,40.00],[63.00,39.00],[63.00,37.00],[65.50,35.75],
       [68.50,35.25],[70.00,36.00],[70.00,37.00]],
      [[63.00,38.00],[63.00,37.00],[62.00,36.00],[60.67,36.00],
       [60.33,35.50],[60.33,35.00],[60.00,35.00]],
    ],
    "dockpaths": [],
    "smallbridgepaths": [
      [[73.70,47.35],[74.30,47.15]],
      [[79.00,42.70],[79.00,43.30]],
    ],
    "largebridgepaths": [
      [[70.00,40.60],[70.00,41.40]],
    ],
    "runwaypaths": [
      [[66.70,38.35],[69.30,38.85]],
    ],
    "taxiwaypaths": [],
    "dampaths": [],
    "tunnelpaths": [],
  },
  "I": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "J": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "K": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
  "L": {
    "base": "land",
    "seahexes": [],
    "level0hexes": [],
    "level1hexes": [],
    "level2hexes": [],
    "level0ridges": [],
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
    "tunnelpaths": [],
  },
}
