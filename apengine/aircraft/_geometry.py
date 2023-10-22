import math
import apengine     as ap
import apengine.hex as aphex
import apengine.log as aplog

##############################################################################

def _relativepositions(x0, y0, facing0, x1, y1, facing1):

  # Determine the offsets of 1 from 0.

  dx = x1 - x0
  dy = y1 - y0  
  dx, dy = aphex.tophysical(dx, dy)

  # Determine the range.

  r = math.sqrt(dx * dx + dy * dy)

  # Determine the angle of 0 off the tail of 1.

  if dx == 0 and dy == 0:
    angleofftail = facing0 - facing1
  else:
    angleofftail = math.degrees(math.atan2(dy, dx)) - facing1
  angleofftail %= 360
  if angleofftail > 180:
    angleofftail -= 360

  # Determine the angle of 1 off the nose of 0.

  if dx == 0 and dy == 0:
    angleoffnose = facing1 - facing0
  else:
    angleoffnose = math.degrees(math.atan2(dy, dx)) - facing0
  angleoffnose %= 360
  if angleoffnose > 180:
    angleoffnose -= 360

  # Determine the coordinates dx and dy of 1, with dx being the
  # coordinate along the flight path of 0 and y being the coordinate
  # perpendicular to the flight path of 0.

  dx = r * math.cos(math.radians(angleoffnose))
  dy = r * math.sin(math.radians(angleoffnose))

  # Round everything.

  def _round(x):

    """
    Round x to 1/256 of a unit.
    """
    if x >= 0:
      return int(x * 256 + 0.5) / 256
    else:
      return int(x * 256 - 0.5) / 256    

  r            = _round(r)
  angleoffnose = _round(angleoffnose)
  angleofftail = _round(angleofftail)
  dx           = _round(dx)
  dy           = _round(dy)

  return angleofftail, angleoffnose, r, dx, dy

##############################################################################

def _angleofftail(a0, a1):

  """
  Return the angle of a0 off the tail of a1.
  """

  # See rule 9.2.

  def trueangleofftail(x0, y0, facing0, x1, y1, facing1):
    angleofftail, angleoffnose, r, dx, dy = _relativepositions(x0, y0, facing0, x1, y1, facing1)
    return angleofftail

  x0      = a0._x
  y0      = a0._y
  facing0 = a0._facing

  x1      = a1._x
  y1      = a1._y
  facing1 = a1._facing

  angleofftail = trueangleofftail(x0, y0, facing0, x1, y1, facing1)

  # If the aircraft fall on the 30, 60, 90, 120, or 150 degree lines and
  # one aircraft is faster than the other, move the faster aircraft
  # forward one hex and recompute.
  if angleofftail != 0 and abs(angleofftail) != 180 and angleofftail % 30 == 0:
    if a0._speed > a1._speed:
      x0, y0 = aphex.forward(x0, y0, facing0)
    elif a1._speed > a0._speed:
      x1, y1 = aphex.forward(x1, y1, facing1)
    angleofftail = trueangleofftail(x0, y0, facing0, x1, y1, facing1)

  # To be on the 0 or 180 degree lines, the aircraft has to be facing
  # the other.
  if angleofftail == 0 and facing0 == facing1:
    return "0 line"
  elif angleofftail == 180 and abs(facing0 - facing1) == 180:
    return "180 line"


  # Resolve cases on the 30, 60, 90, 120, and 150 degree lines in favor
  # of aircraft 0 (round 150 to 180).
  if abs(angleofftail) <= 30:
    return "30 arc"
  elif abs(angleofftail) <= 60:
    return "60 arc"
  elif abs(angleofftail) <= 90:
    return "90 arc"
  elif abs(angleofftail) <= 120:
    return "120 arc"
  elif abs(angleofftail) < 150:
    return "150 arc"
  else:
    return "180 arc"

##############################################################################

def _gunattackrange(a0, a1):

  """
  Returns the range of an air-to-air gun attack from a0 on a1.
  """

  # See the Air-to-Air Gun Attack diagram in the sheets.

  # TODO: include altitude difference.

  def verticalrange():

    altitude0 = a0._altitude
    altitude1 = a1._altitude
    return int(abs(altitude0 - altitude1) / 2)

  def horizontalrange():

    x0      = a0._x
    y0      = a0._y
    facing0 = a0._facing

    x1      = a1._x
    y1      = a1._y
    facing1 = a1._facing
    
    angleofftail, angleoffnose, r, dx, dy = _relativepositions(x0, y0, facing0, x1, y1, facing1)

    if dx < 0:
      return False
    elif dx == 0:
      if dy == 0:
        return 0
      else:
        return False
    elif dx <= 1.0:
      if dy == 0:
        return 1
      else:
        return False
    elif dx < 1.5:
      if abs(dy) <= 0.5:
        return 1
      else:
        return False
    elif dx <= 2.2:
      if abs(dy) <= 0.5:
        return 2
      else:
        return False
    else:
      return False

  r = horizontalrange()
  if r is False:
    return False

  # Apply the relative altitude restrictions for climbing, diving, and level flight.
  if a0.climbingflight() and a0._altitude > a1._altitude:
    return False
  if a0.divingflight() and a0._altitude < a1._altitude:
    return False
  if a0.levelflight():
    if r == 0 and a0._altitude != a1._altitude:
      return False
    if r > 0 and abs(a0._altitude - a1._altitude) > 1:
      return False

  r += verticalrange()
  if r > 2:
    return False
  else:
    return r

##############################################################################

def _inlimitedradararc(a0, a1):

  """
  Return True if a1 is is the limited radar arc of a0.
  """

  # See the Limited Radar Arc diagram in the sheets.

  x0      = a0._x
  y0      = a0._y
  facing0 = a0._facing

  x1      = a1._x
  y1      = a1._y
  facing1 = a1._facing
  
  angleofftail, angleoffnose, r, dx, dy = _relativepositions(x0, y0, facing0, x1, y1, facing1)
      
  if dx <= 0:
    return False
  elif dx <= 1:
    return dy == 0
  elif dx <= 4.0:
    return abs(dy) <= 0.5
  elif dx <= 9.0:
    return abs(dy) <= 1.0
  else:
    return abs(dy) <= 2.0
    
##############################################################################

def _showgeometry(a0, a1):

  """
  Show the angle-off another aircraft's tail.
  """

  aplog.clearerror()
  try:

    name0 = a0._name
    name1 = a1._name

    ap._checkinstartuporturn()

    angleofftail = a0.angleofftail(a1)
    if angleofftail == "0 line" or angleofftail == "180 line":
      a0._log("the target %s has %s on its %s." % (name1, name0, angleofftail))
    else:
      a0._log("the target %s has %s in its %s." % (name1, name0, angleofftail))

    angleofftail = a1.angleofftail(a0)
    if angleofftail == "0 line" or angleofftail == "180 line":
      a0._log("the target %s is on the %s of %s." % (name1, angleofftail, name0))
    else:
      a0._log("the target %s is in the %s of %s." % (name1, angleofftail, name0))

    inlimitedradararc = a0.inlimitedradararc(a1)
    if inlimitedradararc:
      a0._log("the target %s is in the limited radar arc of %s." % (name1, name0))
    else:
      a0._log("the target %s is not in the limited radar arc of %s." % (name1, name0))      

    gunattackrange = a0.gunattackrange(a1)
    if gunattackrange is False:
      a0._log("the target %s cannot be attacked with guns." % (name1))
    else:
      a0._log("the target %s can be attacked with guns at a range of %d." % (name1, gunattackrange))
      
  except RuntimeError as e:
    aplog.logexception(e)

