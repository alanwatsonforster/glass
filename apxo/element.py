import apxo.altitude as apaltitude
import apxo.azimuth  as apazimuth
import apxo.hex      as aphex
import apxo.hexcode  as aphexcode
import apxo.speed    as apspeed

# Elements are anything that can be placed on a map: aircraft, missiles,
# ground units, and markers. This class gathers together their common
# properties.


##############################################################################

_elementlist = []

def _startsetup():
  global _elementlist
  _elementlist = []

def _drawmap():
  for E in _elementlist:
    if not E.removed():
      E._draw()

def fromname(name):

  """
  Look for the element with the given name. Return the element or None if 
  no matching element is found.
  """

  for E in _elementlist:
    if E.name() == name:
      return E
  return None
    
##############################################################################

class element:

  ############################################################################

  def __init__(self, 
    name, 
    x=None, y=None, facing=None, 
    hexcode=None, 
    azimuth=None, 
    altitude=None,
    speed=None,
    color=None
  ):

    global _elementlist

    if not isinstance(name, str):
      raise RuntimeError("the name argument must be a string.")
    for E in _elementlist:
      if name == E._name:
        raise RuntimeError("the name argument must be unique.")    
  
    self._name         = name

    if azimuth is not None:
      if not apazimuth.isvalidazimuth(azimuth):
        raise RuntimeError("the azimuth argument is not valid.")
      facing = apazimuth.tofacing(azimuth)

    if hexcode is not None:
      if not aphexcode.isvalidhexcode(hexcode):
        raise RuntimeError("the hexcode argument is not valid.")
      x, y = aphexcode.toxy(hexcode)

    if not aphex.isvalid(x, y, facing):
      raise RuntimeError("the combination of hexcode and facing are not valid.")

    if not apaltitude.isvalidaltitude(altitude):
      raise RuntimeError("the altitude argument is not valid.")

    self._x            = x
    self._y            = y
    self._facing       = facing
    self._altitude     = altitude
    self._altitudeband = apaltitude.altitudeband(self._altitude)
    
    if not apspeed.isvalidspeed(speed):
      raise RuntimeError("the speed argument is not valid.")
    
    self._speed        = speed

    self._color        = color
    self._removed      = False

    _elementlist.append(self)

  ############################################################################

  def setposition(self, 
    x=None, y=None, facing=None, 
    hexcode=None, 
    azimuth=None, 
    altitude=None
  ):

    if hexcode is not None:
      if not aphexcode.isvalidhexcode(hexcode):
        raise RuntimeError("the hexcode argument is not valid.")
      x, y = aphexcode.toxy(hexcode)

    if x in None:
      x = self.x()
    if y is None:
      y = self.y()
      
    if azimuth is not None:
      if not apazimuth.isvalidazimuth(azimuth):
        raise RuntimeError("the azimuth argument is not valid.")
      facing = apazimuth.tofacing(azimuth)

    if facing is None:
      facing = self.facing()

    if not aphex.isvalid(x, y, facing):
      raise RuntimeError("the combination of hexcode and facing are not valid.")

    if altitude is None:
      altitude = self.altitude()
    if not apaltitude.isvalidaltitude(altitude):
      raise RuntimeError("the altitude argument is not valid.")

    self._name         = name
    self._x            = x
    self._y            = y
    self._facing       = facing
    self._altitude     = altitude
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  def setaltitude(self, altitude=None):
    self.setposition(altitude=altitude)

  def setspeed(self, 
    speed=None
  ):
    if speed is None:
      speed = self.speed()
    if not apspeed.isvalidspeed(speed):
      raise RuntimeError("the speed argument is not valid.")
    self._speed = speed
  
  ############################################################################

  def remove(self):
    self._removed = True
  
  ############################################################################

  def name(self):
    return self._name

  def x(self):
    return self._x

  def y(self):
    return self._y

  def xy(self):
    return self._x, self._y

  def facing(self):
    return self._facing

  def altitude(self):
    return self._altitude

  def altitudeband(self):
    return self._altitudeband

  def speed(self):
    return self._speed

  def color(self):
    return self._color

  def removed(self):
    return self._removed

  ############################################################################

