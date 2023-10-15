import numpy as np
import pickle

import matplotlib.pyplot as plt
import matplotlib.patches as patches

################################################################################

_fig = None
_ax = None

def setcanvas(x, y):
  global _fig, _ax
  _fig = plt.figure(figsize=[x*np.sqrt(3/4),y])
  plt.axis('equal')
  plt.axis('off')
  _ax = plt.gca()


def save():
  pickle.dump(_fig, open("apengine.pickle", "wb"))

def restore():
  global _fig, _ax
  _fig = pickle.load(open("apengine.pickle", "rb"))
  _ax = plt.gca()

def show():
  _fig.show()

################################################################################

def cosd(x):
  return np.cos(np.radians(x))
def sind(x):
  return np.sin(np.radians(x))

def hextophysical(x,y):
  return np.array(x) * np.sqrt(3/4), y
def physicaltohex(x,y):
  return np.array(x) / np.sqrt(3/4), y

################################################################################

def _drawhexinphysical(x, y, size=1, linecolor="lightgrey", linewidth=0.5, fillcolor=None, hatch=None, zorder=1):
  # size is inscribed diameter
  _ax.add_artist(patches.RegularPolygon(
    [x,y], 6, 
    radius=size*0.5*np.sqrt(4/3), orientation=np.pi/6, 
    edgecolor=linecolor, facecolor=fillcolor, fill=(fillcolor != None), hatch=hatch, 
    linewidth=linewidth,
    zorder=zorder
  ))

def _drawdotinphysical(x, y, size=1, facing=0, dx=0, dy=0, color="black", zorder=1):
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  _ax.add_artist(patches.Circle(
    [x,y],
    radius=0.5*size,
    color=color,
    zorder=zorder
  ))

def _drawlineinphysical(x0, y0, x1, y1, 
    color="black", linewidth=0.5, linestyle="solid", capstyle="butt", zorder=1
  ):
  plt.plot((x0, x1), (y0, y1), 
    linewidth=linewidth, linestyle=linestyle, color=color, solid_capstyle=capstyle,
    zorder=zorder)

from matplotlib.patches import Rectangle

def _drawlinesinphysical(x, y, 
  color="black", linewidth=0.5, linestyle="solid", capstyle="butt",zorder=1
):
  plt.plot(x, y, 
    linewidth=linewidth, linestyle=linestyle, color=color, solid_capstyle=capstyle,
    zorder=zorder)
  
def _drawarrowinphysical(x, y, facing, size=1.0, dx=0, dy=0, color="black", zorder=1):
  # size is length
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  dx = size * cosd(facing)
  dy = size * sind(facing)
  x -= 0.5 * dx
  y -= 0.5 * dy
  _ax.add_artist(patches.FancyArrow(
    x, y, dx, dy,
    width=0.01, head_width=0.1, color=color, length_includes_head=True, 
    zorder=zorder
  ))

def _drawdartinphysical(x, y, facing, size=1.0, dx=0, dy=0, facecolor="black", edgecolor="black", zorder=1):
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
    facecolor=facecolor, edgecolor=edgecolor, \
    zorder=zorder
  ))

def _drawtextinphysical(x, y, facing, s, size=10, dx=0, dy=0, color="black", zorder=1):
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  plt.text(x, y, s, size=size, rotation=facing - 90,
           color=color,
           horizontalalignment='center',
           verticalalignment='baseline',
           rotation_mode="anchor",
           zorder=zorder)

def _drawcompassinphysical(x, y, facing, color="black", zorder=1):
  _drawdotinphysical(x, y, size=0.1, color=color, zorder=zorder)
  _drawarrowinphysical(x, y, facing, size=0.8, dy=+0.4, color=color, zorder=zorder)
  _drawtextinphysical(x, y, facing, "N", dy=0.95, color=color, zorder=zorder)

def _drawpolygoninphysical(xy, linecolor="black", fillcolor=None, linewidth=0.5, zorder=1):
  _ax.add_artist(patches.Polygon(
    xy,
    edgecolor=linecolor, facecolor=fillcolor, fill=(fillcolor != None), linewidth=linewidth,
    zorder=zorder
  ))  

################################################################################
    
def drawhex(x, y, **kwargs):
  _drawhexinphysical(*hextophysical(x, y), **kwargs)

def drawhexlabel(x, y, label, dy=0.3, size=7, color="lightgrey", **kwargs):
  drawtext(x, y, 90, label, dy=dy, size=size, color=color, **kwargs)        

def drawdot(x, y, **kwargs):
  _drawdotinphysical(*hextophysical(x, y), **kwargs)

def drawline(x0, y0, x1, y1, **kwargs):
  _drawlineinphysical(*hextophysical(x0, y0), *hextophysical(x1, y1), **kwargs)

def drawlines(x, y, **kwargs):
  _drawlinesinphysical(*hextophysical(x, y), **kwargs)

def drawarrow(x, y, facing, **kwargs):
  _drawarrowinphysical(*hextophysical(x, y), facing, **kwargs)

def drawdart(x, y, facing, **kwargs):
  _drawdartinphysical(*hextophysical(x, y), facing, **kwargs)

def drawtext(x, y, facing, s, **kwargs):
  _drawtextinphysical(*hextophysical(x, y), facing, s, **kwargs)

def drawpolygon(xy, **kwargs):
  _drawpolygoninphysical([hextophysical(*xy) for xy in xy], **kwargs)

def drawrectangle(xmin, ymin, xmax, ymax, **kwargs):
  drawpolygon([[xmin,ymin],[xmin,ymax],[xmax,ymax],[xmax,ymin]], **kwargs)

def drawcompass(x, y, facing, **kwargs):
  _drawcompassinphysical(*hextophysical(x, y), facing, **kwargs)

################################################################################

flightpathcolor=( 0.30, 0.30, 0.30 )

def drawflightpath(x, y):
  drawdot(x[0], y[0], color=flightpathcolor, size=0.1, zorder=0.5)
  drawlines(x, y, color=flightpathcolor, linewidth=2, linestyle="dashed", zorder=0.5)

def drawaircraft(x, y, facing, name, altitude, when, color):
  if when == "end":
    facecolor = color
  else:
    facecolor = "white"
  drawdart(x, y, facing, dy=-0.02, size=0.4, facecolor=facecolor, edgecolor=color)
  drawtext(x, y, facing, name, dx=-0.25, dy=0.0, size=7, color="black")
  drawtext(x, y, facing, "%2d" % altitude, dx=+0.25, dy=0.0, size=7, color="black")
