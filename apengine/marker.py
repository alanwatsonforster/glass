import apengine.azimuth as apazimuth
import apengine.draw    as apdraw
import apengine.hexcode as aphexcode
import apengine.log     as aplog

_markerlist = []

def _startsetup():
  global _markerlist
  _markerlist = []
  
def _drawmap():
  for a in _markerlist:
      a._draw()

class marker:

  def __init__(self, type, hexcode, azimuth=0, color="black"):

    aplog.clearerror()
    try:

      if not type in ["dot"]:
        raise RuntimeError("invalid marker type.")

      x, y = aphexcode.toxy(hexcode)
      facing = apazimuth.tofacing(azimuth)
      
      self._type    = type
      self._x       = x
      self._y       = y
      self._color   = color
      self._removed = False

      global _markerlist
      _markerlist.append(self)

    except RuntimeError as e:
      aplog.logexception(e)

  def move(self, hexcode):

    aplog.clearerror()
    try:

      x, y = aphexcode.toxy(hexcode)
      
      self._x     = x
      self._y     = y

    except RuntimeError as e:
      aplog.logexception(e)

  def remove(self):
    self._removed = True
    
  def _draw(self):

    if self._removed:
      return

    if self._type == "dot":
      apdraw.drawdot(self._x, self._y, size=0.1, color=self._color)