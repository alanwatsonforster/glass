import math

import apassistant._hex as aphex

import pickle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

################################################################################

_fig = None
_ax = None

def setcanvas(xmin, ymin, xmax, ymax, dpi=100):
  global _fig, _ax
  xmin, ymin = aphex.tophysical(xmin, ymin)
  xmax, ymax = aphex.tophysical(xmax, ymax)
  _fig = plt.figure(figsize=[(xmax-xmin),(ymax-ymin)], frameon=False, dpi=dpi)
  plt.axis('off')
  plt.xlim(xmin,xmax)
  plt.ylim(ymin,ymax)
  _ax = plt.gca()
  _ax.set_position([0,0,1,1])
  _ax.add_artist(patches.Polygon(
    [[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin]],
    edgecolor=None, facecolor="white", 
    fill=True, linewidth=0, 
    zorder=0
  ))  

def save():
  pickle.dump(_fig, open("apassistant.pickle", "wb"))

def restore():
  global _fig, _ax
  _fig = pickle.load(open("apassistant.pickle", "rb"))
  _ax = plt.gca()

def show():
  _fig.show()

def writefile(name):
  _fig.savefig(name)

################################################################################

def cosd(x):
  return math.cos(math.radians(x))
def sind(x):
  return math.sin(math.radians(x))

################################################################################

def _drawhexinphysical(x, y, size=1, 
  linecolor="black", linewidth=0.5, fillcolor=None, hatch=None, alpha=1.0,
  zorder=1):
  # size is inscribed diameter
  _ax.add_artist(patches.RegularPolygon(
    [x,y], 6, 
    radius=size*0.5*math.sqrt(4/3), orientation=math.pi/6, 
    edgecolor=_mapcolor(linecolor), facecolor=_mapcolor(fillcolor), fill=(fillcolor != None), hatch=hatch, 
    linewidth=linewidth, alpha=alpha,
    zorder=zorder
  ))

def _drawcircleinphysical(x, y, size=1, 
  linecolor="black", linewidth=0.5, fillcolor=None, hatch=None, alpha=1.0,
  zorder=1):
  _ax.add_artist(patches.Circle(
    [x,y],
    radius=0.5*size, 
    edgecolor=_mapcolor(linecolor), facecolor=_mapcolor(fillcolor), fill=(fillcolor != None), hatch=hatch, 
    linewidth=linewidth, alpha=alpha,
    zorder=zorder
  ))

def _drawsquareinphysical(x, y, size=1, facing=0,
  linecolor="black", linewidth=0.5, fillcolor=None, hatch=None, alpha=1.0,
  zorder=1):
  # size is circumscribed diameter
  _ax.add_artist(patches.RegularPolygon(
    [x,y], 4, 
    radius=size*0.5, orientation=math.radians(facing), 
    edgecolor=_mapcolor(linecolor), facecolor=_mapcolor(fillcolor), fill=(fillcolor != None), hatch=hatch, 
    linewidth=linewidth, alpha=alpha,
    zorder=zorder
  ))

def _drawdotinphysical(x, y, size=1, facing=0, dx=0, dy=0, 
  fillcolor="black", linecolor="black", linewidth=0.5, alpha=1.0,
  zorder=1):
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  _ax.add_artist(patches.Circle(
    [x,y],
    radius=0.5*size, 
    facecolor=_mapcolor(fillcolor), edgecolor=_mapcolor(linecolor), 
    linewidth=linewidth, alpha=alpha, 
    zorder=zorder
  ))

def _drawlinesinphysical(x, y, 
  color="black", linewidth=0.5, linestyle="solid", joinstyle="miter", capstyle="butt", alpha=1.0,
  zorder=1):
  plt.plot(x, y, 
    linewidth=linewidth, linestyle=linestyle, color=_mapcolor(color), solid_joinstyle=joinstyle, solid_capstyle=capstyle, alpha=alpha, 
    zorder=zorder)
  
def _drawarrowinphysical(x, y, facing, size=1.0, dx=0, dy=0, 
  linecolor="black", fillcolor="black", linewidth=0.5, alpha=1.0,
  zorder=1):
  # size is length
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  dx = size * cosd(facing)
  dy = size * sind(facing)
  x -= 0.5 * dx
  y -= 0.5 * dy
  _ax.add_artist(patches.FancyArrow(
    x, y, dx, dy,
    width=0.01, head_width=0.1, length_includes_head=True, 
    edgecolor=_mapcolor(linecolor), facecolor=_mapcolor(linecolor), linewidth=linewidth, alpha=alpha, 
    zorder=zorder
  ))

def _drawdoublearrowinphysical(x, y, facing, **kwargs):
  _drawarrowinphysical(x, y, facing, **kwargs)
  _drawarrowinphysical(x, y, facing + 180, **kwargs)

def _drawdartinphysical(x, y, facing, size=1.0, dx=0, dy=0, 
  linecolor="black", fillcolor="black", linewidth=0.5, alpha=1.0,
  zorder=1):
  # size is length
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  dx = size * cosd(facing)
  dy = size * sind(facing)
  x -= 0.5 * dx
  y -= 0.5 * dy
  _ax.add_artist(patches.FancyArrow(
    x, y, dx, dy,
    width=0.02, head_length=size, head_width=0.5*size, length_includes_head=True, 
    edgecolor=_mapcolor(linecolor), facecolor=_mapcolor(fillcolor), linewidth=linewidth, alpha=alpha, 
    zorder=zorder
  ))

def _drawtextinphysical(x, y, facing, s, dx=0, dy=0, 
  color="black", size=10, alpha=1.0,
  zorder=1):
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  plt.text(x, y, s, size=size, rotation=facing - 90,
           color=_mapcolor(color), alpha=alpha, 
           horizontalalignment='center',
           verticalalignment='center',
           rotation_mode="anchor",
           zorder=zorder)

def _drawpolygoninphysical(xy, 
  linecolor="black", fillcolor=None, linewidth=0.5, hatch=None, alpha=1.0,
  zorder=1):
  _ax.add_artist(patches.Polygon(
    xy,
    edgecolor=_mapcolor(linecolor), facecolor=_mapcolor(fillcolor), 
    fill=(fillcolor != None), linewidth=linewidth, hatch=hatch, alpha=alpha, 
    zorder=zorder
  ))  

def _drawrectangleinphysical(xmin, ymin, xmax, ymax, **kwargs): 
  _drawpolygoninphysical([[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin]], **kwargs)

def _drawcompassinphysical(x, y, facing, color="black", alpha=1.0, zorder=1):
  _drawdotinphysical(x, y, facing=facing, size=0.07, dy=-0.3, linecolor=None, fillcolor=color, alpha=alpha, zorder=zorder)
  _drawarrowinphysical(x, y, facing, size=0.6, dy=0, linecolor=color, fillcolor=color, linewidth=1, alpha=alpha, zorder=zorder)
  _drawtextinphysical(x, y, facing, "N", size=14, dx=-0.15, dy=-0.05, color=color, alpha=alpha, zorder=zorder)
  
################################################################################
    
def drawhex(x, y, **kwargs):
  _drawhexinphysical(*aphex.tophysical(x, y), **kwargs)

def drawcircle(x, y, **kwargs):
  _drawcircleinphysical(*aphex.tophysical(x, y), **kwargs)

def drawsquare(x, y, **kwargs):
  _drawsquareinphysical(*aphex.tophysical(x, y), **kwargs)
  
def drawhexlabel(x, y, label, dy=0.35, size=9, color="lightgrey", **kwargs):
  drawtext(x, y, 90, label, dy=dy, size=size, color=color, **kwargs)        

def drawdot(x, y, **kwargs):
  _drawdotinphysical(*aphex.tophysical(x, y), **kwargs)

def drawlines(x, y, **kwargs):
  xy = [aphex.tophysical(xy[0], xy[1]) for xy in zip(x, y)]
  x = [xy[0] for xy in xy]
  y = [xy[1] for xy in xy]
  _drawlinesinphysical(x, y, **kwargs)

def drawarrow(x, y, facing, **kwargs):
  _drawarrowinphysical(*aphex.tophysical(x, y), facing, **kwargs)

def drawdoublearrow(x, y, facing, **kwargs):
  _drawdoublearrowinphysical(*aphex.tophysical(x, y), facing, **kwargs)
  
def drawdart(x, y, facing, **kwargs):
  _drawdartinphysical(*aphex.tophysical(x, y), facing, **kwargs)

def drawtext(x, y, facing, s, **kwargs):
  _drawtextinphysical(*aphex.tophysical(x, y), facing, s, **kwargs)

def drawpolygon(xy, **kwargs):
  _drawpolygoninphysical([aphex.tophysical(*xy) for xy in xy], **kwargs)

def drawrectangle(xmin, ymin, xmax, ymax, **kwargs):
  xmin, ymin = aphex.tophysical(xmin, ymin)
  xmax, ymax = aphex.tophysical(xmax, ymax)
  _drawrectangleinphysical(xmin, ymin, xmax, ymax, **kwargs)
  
def drawcompass(x, y, facing, **kwargs):
  _drawcompassinphysical(*aphex.tophysical(x, y), facing, **kwargs)

################################################################################

_colors = {

  # This is a mapping from "aircraft color" to "CSS color".

  # Approximations to NATO blue, red, green, and yellow.
  # https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology#APP-6A_affiliation

  "natoblue"    : (0.45, 0.87, 1.00),
  "natored"     : (1.00, 0.45, 0.45),
  "natogreen"   : (0.55, 1.00, 0.55),
  "natoyellow"  : (1.00, 1.00, 0.46),
  "natofriendly": "natoblue",
  "natohostile" : "natored",
  "natoneutral" : "natogreen",
  "natounknown" : "natoyellow",

  "aluminum"    : "css:lightgray",
  "aluminium"   : "aluminum",
  "unpainted"   : "aluminum",

  "white"       : "css:white",
  "darkblue"    : "css:midnightblue",
  "green"       : "css:olivedrab",
  "tan"         : "css:tan",
  "sand"        : "css:blanchedalmond",
  "darkgray"    : "css:slategray",
  "darkgrey"    : "darkgray",
  "lightgray"   : "css:silver",
  "lightgrey"   : "lightgray",

}

def _mapcolor(color):

  if not isinstance(color, str):
    return color
  elif color[0:4] == "css:":
    return color[4:]
  elif color in _colors:
    return _mapcolor(_colors[color])
  else:
    return color

################################################################################

