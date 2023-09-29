import airpower.variants as apvariants

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = [7.5, 10]
plt.rcParams.update({'font.size': 10})

_donotdraw = True

def setcanvas(x, y):
  global _donotdraw
  if apvariants.withvariant("do not draw"):
    _donotdraw = True
  if _donotdraw:
    return
  matplotlib.rcParams['figure.figsize'] = [x, y]
  plt.figure()
  plt.axis('equal')
  plt.axis('off')

def cosd(x):
  return np.cos(np.radians(x))
def sind(x):
  return np.sin(np.radians(x))

def hextophysical(x,y):
  return x * np.sqrt(3/4), y
def physicaltohex(x,y):
  return x / np.sqrt(3/4), y

def _drawhexinphysical(x, y, size=1, color="lightgrey"):
  # size is inscribed diameter
  if _donotdraw:
    return
  azimuths = np.array((0, 60, 120, 180, 240, 300, 0))
  xvertices = x + 0.5 * size * cosd(azimuths) / cosd(30)
  yvertices = y + 0.5 * size * sind(azimuths) / cosd(30)
  plt.plot(xvertices, yvertices, color=color, zorder=0)

def _drawdotinphysical(x, y, size=1, facing=0, dx=0, dy=0, color="black"):
  if _donotdraw:
    return
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  plt.plot(x, y, marker=".", color=color, zorder=1)

def _drawsquareinphysical(x, y, facing, size=1, dx=0, dy=0, color="black"):
  # size is diagonal
  if _donotdraw:
    return
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  azimuths = np.array((0, 90, 180, 270, 0))
  if facing == None:
    facing = 45
  xvertices = x + 0.5 * size * cosd(azimuths + facing)
  yvertices = y + 0.5 * size * sind(azimuths + facing)
  plt.plot(xvertices, yvertices, color=color, zorder=1)

def _drawlineinphysical(x0, y0, x1, y1, color="black", linestyle="solid", zorder=1):
  if _donotdraw:
    return
  plt.plot((x0, x1), (y0, y1), linestyle=linestyle, color=color, zorder=zorder)

def _drawarrowinphysical(x, y, facing, size=1.0, dx=0, dy=0, color="black"):
  # size is length
  if _donotdraw:
    return
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  x0 = x - 0.5 * size * cosd(facing)
  y0 = y - 0.5 * size * sind(facing)
  x1 = x0 + 1.0 * size * cosd(facing)
  y1 = y0 + 1.0 * size * sind(facing)
  plt.arrow(x0, y0, x1 - x0, y1 - y0, width=0.01, head_width=0.1, color=color, length_includes_head=True, zorder=1)

def _drawdartinphysical(x, y, facing, size=1.0, dx=0, dy=0, color="black"):
  # size is length
  if _donotdraw:
    return
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  x0 = x - 0.5 * size * cosd(facing)
  y0 = y - 0.5 * size * sind(facing)
  x1 = x0 + 1.0 * size * cosd(facing)
  y1 = y0 + 1.0 * size * sind(facing)
  plt.arrow(x0, y0, x1 - x0, y1 - y0, width=0.02, head_length=size, head_width=0.5*size, color=color, length_includes_head=True, zorder=1)

def _drawtextinphysical(x, y, facing, s, size=10, dx=0, dy=0, color="black"):
  if _donotdraw:
    return
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  plt.text(x, y, s, size=size, rotation=facing - 90,
           color=color,
           horizontalalignment='center',
           verticalalignment='center_baseline',
           rotation_mode="anchor")

def _drawcompassinphysical(x, y, facing):
  if _donotdraw:
    return
  _drawdotinphysical(x, y, size=0.3)
  _drawarrowinphysical(x, y, facing, size=0.8, dy=+0.4)
  _drawtextinphysical(x, y, facing, "N", dy=0.95)
    
def drawhex(x, y, **kwargs):
  if _donotdraw:
    return
  _drawhexinphysical(*hextophysical(x, y), **kwargs)

def drawdot(x, y, **kwargs):
  if _donotdraw:
    return
  _drawdotinphysical(*hextophysical(x, y), **kwargs)

def drawsquare(x, y, facing, **kwargs):
  if _donotdraw:
    return
  _drawsquareinphysical(*hextophysical(x, y), facing, **kwargs)

def drawline(x0, y0, x1, y1, **kwargs):
  if _donotdraw:
    return
  _drawlineinphysical(*hextophysical(x0, y0), *hextophysical(x1, y1), **kwargs)

def drawarrow(x, y, facing, **kwargs):
  if _donotdraw:
    return
  _drawarrowinphysical(*hextophysical(x, y), facing, **kwargs)

def drawdart(x, y, facing, **kwargs):
  if _donotdraw:
    return
  _drawdartinphysical(*hextophysical(x, y), facing, **kwargs)

def drawtext(x, y, facing, s, **kwargs):
  if _donotdraw:
    return
  _drawtextinphysical(*hextophysical(x, y), facing, s, **kwargs)

def drawcompass(x, y, facing, **kwargs):
  if _donotdraw:
    return
  _drawcompassinphysical(*hextophysical(x, y), facing, **kwargs)

def drawflightpath(lastx, lasty, x, y):
  if _donotdraw:
    return
  drawline(lastx, lasty, x, y, color="darkgray", linestyle="dashed", zorder=0.5)

def drawaircraft(x, y, facing, name, altitude, when):
  if _donotdraw:
    return
  if when == "end":
    color = "black"
  else:
    color = "grey"
  drawdart(x, y, facing, dy=-0.02, size=0.5, color=color)
  drawtext(x, y, facing, name, dx=-0.3, dy=0.0, size=7, color=color)
  drawtext(x, y, facing, "%2d" % altitude, dx=+0.3, dy=0.0, size=7, color=color)
