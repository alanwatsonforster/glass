print("airpower.draw")

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = [7.5, 10]
plt.rcParams.update({'font.size': 10})

def cosd(x):
  return np.cos(np.radians(x))
def sind(x):
  return np.sin(np.radians(x))

def hextophysical(x,y):
  return x * np.sqrt(3/4), y
def physicaltohex(x,y):
  return x / np.sqrt(3/4), y

def drawhex(x, y, size=1, color="lightgrey"):
  # size is inscribed diameter
  azimuths = np.array((0, 60, 120, 180, 240, 300, 0))
  xvertices = x + 0.5 * size * cosd(azimuths) / cosd(30)
  yvertices = y + 0.5 * size * sind(azimuths) / cosd(30)
  plt.plot(xvertices, yvertices, color=color, zorder=0)

def drawdot(x, y, size=1, facing=0, dx=0, dy=0, color="black"):
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  plt.plot(x, y, marker=".", color=color, zorder=1)

def drawsquare(x, y, facing, size=1, dx=0, dy=0, color="black"):
  # size is diagonal
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  azimuths = np.array((0, 90, 180, 270, 0))
  if facing == None:
    facing = 45
  xvertices = x + 0.5 * size * cosd(azimuths + facing)
  yvertices = y + 0.5 * size * sind(azimuths + facing)
  plt.plot(xvertices, yvertices, color=color, zorder=1)

def drawline(x0, y0, x1, y1, color="black", linestyle="solid", zorder=1):
  plt.plot((x0, x1), (y0, y1), linestyle=linestyle, color=color, zorder=zorder)

def drawarrow(x, y, facing, size=1.0, dx=0, dy=0, color="black"):
  # size is length
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  x0 = x - 0.5 * size * cosd(facing)
  y0 = y - 0.5 * size * sind(facing)
  x1 = x0 + 1.0 * size * cosd(facing)
  y1 = y0 + 1.0 * size * sind(facing)
  plt.arrow(x0, y0, x1 - x0, y1 - y0, width=0.02*size, head_width=0.1*size, color=color, length_includes_head=True, zorder=1)

def drawdart(x, y, facing, size=1.0, dx=0, dy=0, color="black"):
  # size is length
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  x0 = x - 0.5 * size * cosd(facing)
  y0 = y - 0.5 * size * sind(facing)
  x1 = x0 + 1.0 * size * cosd(facing)
  y1 = y0 + 1.0 * size * sind(facing)
  plt.arrow(x0, y0, x1 - x0, y1 - y0, width=0.02, head_length=size, head_width=0.5*size, color=color, length_includes_head=True, zorder=1)

def drawtext(x, y, facing, s, size=10, dx=0, dy=0, color="black"):
  x = x + dx * sind(facing) + dy * cosd(facing)
  y = y - dx * cosd(facing) + dy * sind(facing)
  plt.text(x, y, s, size=size, rotation=facing - 90,
           color=color,
           horizontalalignment='center',
           verticalalignment='center_baseline',
           rotation_mode="anchor")

def drawhexinhex(x, y, **kwargs):
  drawhex(*hextophysical(x, y), **kwargs)

def drawdotinhex(x, y, **kwargs):
  drawdot(*hextophysical(x, y), **kwargs)

def drawsquareinhex(x, y, pointing, **kwargs):
  drawsquare(*hextophysical(x, y), pointing, **kwargs)

def drawlineinhex(x0, y0, x1, y1, **kwargs):
  drawline(*hextophysical(x0, y0), *hextophysical(x1, y1), **kwargs)

def drawarrowinhex(x, y, pointing, **kwargs):
  drawarrow(*hextophysical(x, y), pointing, **kwargs)

def drawdartinhex(x, y, pointing, **kwargs):
  drawdart(*hextophysical(x, y), pointing, **kwargs)

def drawtextinhex(x, y, pointing, s, **kwargs):
  drawtext(*hextophysical(x, y), pointing, s, **kwargs)

def drawhexgrid(sx, sy, nx, ny):
  matplotlib.rcParams['figure.figsize'] = [nx, ny * np.sqrt(3/4)]
  plt.figure()
  plt.axis('equal')
  plt.axis('off')
  for ix in range(sx, sx + nx):
    for iy in range(sy, sy + ny):
      drawhexinhex(ix, iy + 0.5 * (ix % 2))

def drawinhex(x, y, facing):
  #drawsquareinhex(x, y, facing, size=0.866)
  drawdartinhex(x, y, facing, dy=-0.02, size=0.5)
  drawtextinhex(x, y, facing, "F1", dx=-0.3, dy=0.0, size=7)
  drawtextinhex(x, y, facing, "10", dx=+0.3, dy=0.0, size=7)

def numbertohex(n):

  # The hexes in the TSOH maps are numbered as XXYY, where XX is the column number and YY is the row number, in this sense:
  #
  #     0201
  # 0101    0301
  #     0202
  # 0102    0302
  #     0203
  # 0103    0303

  x = n // 100
  y = - (n % 100)
  if x % 2 == 1:
    y -= 0.5
  return x, y

def drawhexnumber(n):
  drawtextinhex(*numbertohex(n), 90, "%04d" % n, dy=0.3, size=7, color="grey")

def drawmapA1():
  drawhexgrid(11,-16,19,15)
  for x in range(11,30):
    for y in range(1,16):
      drawhexnumber(x * 100 + y)

def drawmapC1():
  drawhexgrid(51,-16,19,15)
  for x in range(51,70):
    for y in range(1,16):
      drawhexnumber(x * 100 + y)