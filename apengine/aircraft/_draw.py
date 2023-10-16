"""
Drawing for the aircraft class.
"""

import apengine.draw as apdraw

flightpathcolor=( 0.30, 0.30, 0.30 )

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
    apdraw.drawdot(x[0], y[0], color=flightpathcolor, size=0.1, zorder=0.5)
    apdraw.drawlines(x, y, color=flightpathcolor, linewidth=3, linestyle="dashed", zorder=0.5)

def _drawatstart(self):
  _drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, "start", color=self._color)

def _drawatend(self):
  _drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, "end", color=self._color)

def _drawaircraft(x, y, facing, name, altitude, when, color):
  if when == "end":
    facecolor = color
  else:
    facecolor = "white"
  apdraw.drawdart(x, y, facing, dy=-0.02, size=0.4, facecolor=facecolor, edgecolor=color)
  apdraw.drawtext(x, y, facing, name, dx=-0.25, dy=0.0, size=7, color="black")
  apdraw.drawtext(x, y, facing, "%2d" % altitude, dx=+0.25, dy=0.0, size=7, color="black")
