import apxo.altitude as apaltitude
import apxo.azimuth  as apazimuth
import apxo.path     as appath
import apxo.hex      as aphex
import apxo.hexcode  as aphexcode
import apxo.map      as apmap
import apxo.speed    as apspeed

# Elements are anything that can be placed on a map: aircraft, missiles,
# ground units, and markers. This class gathers together their common
# properties.


##############################################################################

_elementlist = []

def _startsetup():
  global _elementlist
  _elementlist = []
  
def _startturn():
  for E in _elementlist:
    E._startpath()

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

def aslist(withdestroyed=False, withleftmap=False):
  elementlist = _elementlist
  #if not withdestroyed:
  #  elementlist = filter(lambda x: not x.removed(), elementlist)
  #if not withleftmap:
  #  elementlist = filter(lambda x: not x._leftmap, elementlist)
  return list(elementlist)
  
##############################################################################

def _xminforzoom(withdestroyed=False):
  return min([min(E.x(), E._path.xmin()) for E in aslist(withdestroyed=withdestroyed)])

def _xmaxforzoom(withdestroyed=False):
  return max([max(E.x(), E._path.xmax()) for E in aslist(withdestroyed=withdestroyed)])

def _yminforzoom(withdestroyed=False):
  return min([min(E._y, E._path.ymin()) for E in aslist(withdestroyed=withdestroyed)])

def _ymaxforzoom(withdestroyed=False):
  return max([max(E._y, E._path.ymax()) for E in aslist(withdestroyed=withdestroyed)])
  
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

    self._x             = x
    self._y             = y
    self._facing        = facing
    self._altitude      = altitude
    self._altitudeband  = apaltitude.altitudeband(self._altitude)
    self._altitudecarry = 0
    
    if not apspeed.isvalidspeed(speed):
      raise RuntimeError("the speed argument is not valid.")
    
    self._speed        = speed

    self._path   = appath.path(x, y, facing, altitude)

    self._color        = color
    self._removed      = False

    _elementlist.append(self)

  ############################################################################

  def _setposition(self, 
    x=None, y=None, facing=None, 
    hexcode=None, 
    azimuth=None, 
    altitude=None, altitudecarry=None
  ):

    if hexcode is not None:
      if not aphexcode.isvalidhexcode(hexcode):
        raise RuntimeError("the hexcode argument is not valid.")
      x, y = aphexcode.toxy(hexcode)

    if x is None:
      x = self._x
    if y is None:
      y = self._y
      
    if azimuth is not None:
      if not apazimuth.isvalidazimuth(azimuth):
        raise RuntimeError("the azimuth argument is not valid.")
      facing = apazimuth.tofacing(azimuth)

    if facing is None:
      facing = self._facing

    if not aphex.isvalid(x, y, facing):
      raise RuntimeError("the combination of hexcode and facing are not valid.")

    if altitude is None:
      altitude = self._altitude
    if not apaltitude.isvalidaltitude(altitude):
      raise RuntimeError("the altitude argument is not valid.")
      
    if altitudecarry is None:
      altitudecarry = self._altitudecarry

    self._x             = x
    self._y             = y
    self._facing        = facing
    self._altitude      = altitude
    self._altitudeband  = apaltitude.altitudeband(self._altitude)
    self._altitudecarry = altitudecarry
        
  ############################################################################

  def _setxy(self, x=None, y=None):
    self._setposition(x=x, y=y)
    
  def _setfacing(self, facing):
    self._setposition(facing=facing)

  def _setaltitude(self, altitude=None):
    self._setposition(altitude=altitude)
    
  def _setaltitudecarry(self, altitudecarry=None):
    self._setposition(altitudecarry=altitudecarry)
    
  def _setspeed(self, 
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

  def hexcode(self):
    if apmap.isonmap(self.x(), self.y()):
      return aphexcode.fromxy(self.x(), self.y())
    else:
      return None
      
  def facing(self):
    return self._facing

  def azimuth(self):
    return apazimuth.fromfacing(self.facing())
    
  def altitude(self):
    return self._altitude

  def altitudeband(self):
    return self._altitudeband
    
  def altitudecarry(self):
    return self._altitudecarry
    
  def position(self):
    hexcode = self.hexcode()
    if hexcode is None:
      hexcode = "-------"
    azimuth = self.azimuth()
    if azimuth is None:
      azimuth = "---"
    return "%-12s  %-3s  %2d" % (hexcode, azimuth, self.altitude())
      
  def speed(self):
    return self._speed

  def color(self):
    return self._color

  def removed(self):
    return self._removed

  ############################################################################

  def _doforward(self):
    self._setxy(*aphex.forward(self.x(), self.y(), self.facing()))
  
  def _doclimb(self, altitudechange):
    altitude, altitudecarry = apaltitude.adjustaltitude(self.altitude(), self.altitudecarry(), +altitudechange)
    self._setposition(altitude=altitude, altitudecarry=altitudecarry)

  def _dodive(self, altitudechange):
    altitude, altitudecarry = apaltitude.adjustaltitude(self.altitude(), self.altitudecarry(), -altitudechange)
    self._setposition(altitude=altitude, altitudecarry=altitudecarry)
    
  def _doturn(self, sense, facingchange):
    if aphex.isside(self.x(), self.y()):
      self._setxy(*aphex.sidetocenter(self.x(), self.y(), self.facing(), sense))
    if sense == "L":
      self._setfacing((self.facing() + facingchange) % 360)
    else:
      self._setfacing((self.facing() - facingchange) % 360)  

  def _doslide(self, sense):
    self._setxy(*aphex.slide(self.x(), self.y(), self.facing(), sense))
    
  def _dodisplacementroll(self, sense):
    self._setxy(*aphex.displacementroll(self.x(), self.y(), self.facing(), sense))
    
  def _dolagroll(self, sense):
    self._setxy(*aphex.lagroll(self.x(), self.y(), self.facing(), sense))
    if sense == "R":
      self._setfacing((self.facing() + 30) % 360)
    else:
      self._setfacing((self.facing() - 30) % 360)  
      
  def _doverticalroll(self, sense, facingchange, shift):
    if aphex.isside(self.x(), self.y()) and shift:
      self._setxy(*aphex.sidetocenter(self.x(), self.y(), self.facing(), sense))
    if sense == "L":
      self._setfacing((self.facing() + facingchange) % 360)
    else:
      self._setfacing((self.facing() - facingchange) % 360)      
      
  ############################################################################

  def _startpath(self):
    self._path.start(self.x(), self.y(), self.facing(), self.altitude())
    
  def _extendpath(self):
    self._path.extend(self.x(), self.y(), self.facing(), self.altitude())
    
  def _drawpath(self, color, zorder, annotate=True):
    self._path.draw(color, zorder, annotate=annotate)
    
  ############################################################################


  