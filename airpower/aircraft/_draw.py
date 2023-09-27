"""
Drawing for the aircraft class.
"""

import airpower.draw as apdraw

def _drawflightpath(self, lastx, lasty):
  apdraw.drawflightpath(lastx, lasty, self._x, self._y)

def _drawaircraft(self, when):
  apdraw.drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, when)
        