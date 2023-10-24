"""
Drawing for the aircraft class.
"""

import apengine._draw as apdraw

flightpathcolor     = ( 0.00, 0.00, 0.00 )
flightpathwidth     = 2.0
flightpathlinestyle = "dotted"
flightpathdotsize   = 0.05
edgecolor           = ( 0.00, 0.00, 0.00 )
textsize            = 10
textcolor           = ( 0.00, 0.00, 0.00 )

def _startflightpath(self):
  self._flightpathx = [self._x]
  self._flightpathy = [self._y]

def _continueflightpath(self):
  self._flightpathx.append(self._x)
  self._flightpathy.append(self._y)

def _drawflightpath(self):
  x = self._flightpathx
  y = self._flightpathy
  if x != [] and y != []:
    apdraw.drawdot(x[0], y[0], color=flightpathcolor, size=flightpathdotsize, zorder=0.5)
    apdraw.drawlines(x, y, color=flightpathcolor, linewidth=flightpathwidth, linestyle=flightpathlinestyle, zorder=0.5)

def _drawaircraft(self):
  if self._leftmap:
    return
  if self._destroyed:
    facecolor = "black"
    altitude  = "--"
  else:
    facecolor = self._color
    altitude  = "%2d" % self._altitude
  x = self._x
  y = self._y
  facing = self._facing
  apdraw.drawdart(x, y, facing, dy=-0.02, size=0.4, facecolor=facecolor, linewidth=1, edgecolor=edgecolor, zorder=1)
  apdraw.drawtext(x, y, facing, self._name, dx=-0.25, dy=0.0, size=textsize, color=textcolor, zorder=1)
  apdraw.drawtext(x, y, facing, altitude  , dx=+0.25, dy=0.0, size=textsize, color=textcolor, zorder=1)
