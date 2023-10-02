"""
Drawing for the aircraft class.
"""

import airpower.draw as apdraw

def _startflightpath(self):
  self._flightpathx = [self._x]
  self._flightpathy = [self._y]

def _continueflightpath(self):
  self._flightpathx.append(self._x)
  self._flightpathy.append(self._y)

def _drawflightpath(self):
  if self._flightpathx != [] and self._flightpathy != []:
    apdraw.drawflightpath(self._flightpathx, self._flightpathy)

def _drawatstart(self):
  apdraw.drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, "start")

def _drawatend(self):
  apdraw.drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, "end")