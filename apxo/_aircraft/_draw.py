"""
Drawing for the aircraft class.
"""

import apxo._draw as apdraw

flightpathcolor            = ( 0.00, 0.00, 0.00 )
flightpathlinewidth        = 2.0
flightpathlinestyle        = "dotted"
flightpathdotsize          = 0.1
textsize                   = 10
counterlinewidth           = 2
destroyedaircraftfillcolor = ( 0.50, 0.50, 0.50 )
destroyedaircraftlinecolor = ( 0.50, 0.50, 0.50 )
aircraftlinecolor          = ( 0.00, 0.00, 0.00 )
aircraftlinewidth          = 1

_zorder = 0

def _startflightpath(self):
  self._flightpathx = [self._x]
  self._flightpathy = [self._y]

def _continueflightpath(self):
  self._flightpathx.append(self._x)
  self._flightpathy.append(self._y)

def _drawflightpath(self):
  if self._destroyed:
    fillcolor = destroyedaircraftfillcolor
  else:
    fillcolor = self._color
  x = self._flightpathx
  y = self._flightpathy
  if len(x) > 1:
    apdraw.drawlines(x, y, color=flightpathcolor, linewidth=flightpathlinewidth, linestyle=flightpathlinestyle, zorder=0.1)
    apdraw.drawdot(x[0], y[0], fillcolor=fillcolor, linecolor=flightpathcolor, linewidth=aircraftlinewidth, size=flightpathdotsize, zorder=self._zorder)

def _drawaircraft(self):
  if self._leftmap:
    return
  if self._destroyed:
    fillcolor = destroyedaircraftfillcolor
    linecolor = destroyedaircraftlinecolor
    altitude  = ""
  else:
    fillcolor = self._color
    linecolor = aircraftlinecolor
    altitude  = "%2d" % self._altitude
  x = self._x
  y = self._y
  facing = self._facing
  zorder = self._zorder
  if self._counter:
    apdraw.drawsquare(x, y, facing=facing, size=1, linecolor="black", linewidth=counterlinewidth, fillcolor=self._color, zorder=zorder)
    apdraw.drawdart(x, y, facing, size=0.4, fillcolor="black", linewidth=1, linecolor="black", zorder=zorder)
  else:
    apdraw.drawdart(x, y, facing, dy=-0.02, size=0.4, fillcolor=fillcolor, linewidth=aircraftlinewidth, linecolor=linecolor, zorder=zorder)
    apdraw.drawtext(x, y, facing, self._name, dx=-0.25, dy=0.0, size=textsize, color=linecolor, zorder=zorder)
    apdraw.drawtext(x, y, facing, altitude  , dx=+0.25, dy=0.0, size=textsize, color=linecolor, zorder=zorder)
