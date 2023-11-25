import math
import apxo      as ap
import apxo.hex as aphex
import apxo.log as aplog

##############################################################################

def _round(x):

  """
  Round x to 1/256 of a unit.
  """
  if x >= 0:
    return int(x * 256 + 0.5) / 256
  else:
    return int(x * 256 - 0.5) / 256 
      
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

  angleofftail = _round(angleofftail)
  angleoffnose = _round(angleoffnose)
  r            = _round(r)
  dx           = _round(dx)
  dy           = _round(dy)

  return angleofftail, angleoffnose, r, dx, dy

##############################################################################

def angleofftail(a0, a1):

  """
  Return the angle of a0 off the tail of a1.
  """

  # See rule 9.2.

  def truegeometry(x0, y0, facing0, x1, y1, facing1):
    angleofftail, angleoffnose, r, dx, dy = _relativepositions(x0, y0, facing0, x1, y1, facing1)
    return angleofftail, angleoffnose, r

  x0      = a0._x
  y0      = a0._y
  facing0 = a0._facing

  x1      = a1._x
  y1      = a1._y
  facing1 = a1._facing

  angleofftail, angleoffnose, r = truegeometry(x0, y0, facing0, x1, y1, facing1)

  if r > 0 and angleofftail != 0.0 and angleofftail != 180.0 and angleofftail % 30 == 0.0:

    # Distinguish cases on the 30, 60, 90, 120, and 150 degree arcs.

    # If 0 is slower, it falls in the rear arc.
    # If 0 is faster and headed behind 0, it falls in the rear arc. 
    # If 0 is faster and headed in front of 1, it falls in the front arc.
  
    inreararc = False
    infrontarc = False
    if a0._speed < a1._speed:
      inreararc = True
    elif a0._speed > a1._speed and angleoffnose != 0:
      if (angleofftail > 0 and angleoffnose > 0) or (angleofftail < 0 and angleoffnose < 0):
        infrontarc = True
      elif (angleofftail > 0 and angleoffnose < 0) or (angleofftail < 0 and angleoffnose > 0):
        inreararc = True

    if (infrontarc and angleofftail > 0) or (inreararc and angleofftail < 0):
        angleofftail += 1
    elif (infrontarc and angleofftail < 0) or (inreararc and angleofftail > 0):
        angleofftail -= 1

  # To be on the 0 or 180 degree lines, the aircraft has to be facing
  # the other.
  if angleofftail == 0 and facing0 == facing1:
    return "0 line"
  elif angleofftail == 180 and abs(facing0 - facing1) == 180:
    return "180 line"

  # Resolve cases on the 30, 60, 90, 120, and 150 degree lines in favor
  # of aircraft 0 (round 120 to 150 and 150 to 180).
  if abs(angleofftail) <= 30:
    return "30 arc"
  elif abs(angleofftail) <= 60:
    return "60 arc"
  elif abs(angleofftail) <= 90:
    return "90 arc"
  elif abs(angleofftail) < 120:
    return "120 arc"
  elif abs(angleofftail) < 150:
    return "150 arc"
  else:
    return "180 arc"

##############################################################################

def gunattackrange(attacker, target, arc=False):

  """
  Returns the range of an air-to-air gun attack from the attacker on the target
  or the reason the attack is forbidden.
  """

  # See rule 9.1 and the Air-to-Air Gun Attack diagram in the sheets.

  def horizontalrange(x0, y0, facing0, x1, y1, facing1):
    
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

  def verticalrange():
    return int(abs(attacker._altitude - target._altitude) / 2)

  if arc:

    rmin = False
    for facing in range(0, 361, 30):
      r = horizontalrange(
        attacker._x, attacker._y, facing, 
        target._x, target._y, target._facing
      )
      if rmin is False:
        rmin = r
      elif r is not False:
        rmin = min(r, rmin)
    r = rmin

    if r is False:
      return "the target is not in the weapon range or arc."

    angleoff = target.angleofftail(attacker)
    if arc == "30-":
      allowedangleoff = [ "0 line", "30 arc" ]
    elif arc == "60-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc" ]
    elif arc == "90-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc" ]
    elif arc == "120-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc" ]
    elif arc == "150-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc", "150 arc" ]
    elif arc == "180-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc", "150 arc", "180 arc", "180 line" ]
    else:
      raise RuntimeError("invalid arc %r." % arc)

    if not angleoff in allowedangleoff:
      return "the target is not in the weapon range or arc."
      
    r += verticalrange()
    if r > 2:
      return "the target is not in the weapon range or arc."
    else:
      return r
    
  else:
    
    r = horizontalrange(
      attacker._x, attacker._y, attacker._facing, 
      target._x, target._y, target._facing
    )

    if r is False:
      return "the target is not in the weapon range or arc."

    # Apply the relative altitude restrictions for climbing, diving, and level flight.
    if attacker.climbingflight() and attacker._altitude > target._altitude:
      return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
    if attacker.divingflight() and attacker._altitude < target._altitude:
      return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
    if attacker.levelflight():
      if r == 0 and attacker._altitude != target._altitude:
        return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
      if r > 0 and abs(attacker._altitude - target._altitude) > 1:
        return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
        
    r += verticalrange()
    if r > 2:
      return "the target is not in the weapon range or arc."
    else:
      return r

##############################################################################

def rocketattackrange(attacker, target):

  # See rule 9.3.

  def horizontalrange():
    return aphex.distance(attacker._x, attacker._y, target._x, target._y)

  def verticalrange():
    return int(abs(attacker._altitude - target._altitude) / 2)
    
  if not attacker.inlimitedradararc(target):
    return "the target is not in the weapon range or arc."

  r = horizontalrange()

  # Apply the relative altitude restrictions for climbing, diving, and level flight.
  if attacker.climbingflight() and attacker._altitude > target._altitude:
    return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
  if attacker.divingflight() and attacker._altitude < target._altitude:
    return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
  if attacker.levelflight():
    if r == 0 and attacker._altitude != target._altitude:
      return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
    if r > 0 and abs(attacker._altitude - target._altitude) > 1:
      return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
  
  r += verticalrange()
  if r == 0 or r > 4:
    return "the target is not in the weapon range or arc."
  else:
    return r

##############################################################################

def inlimitedradararc(a0, a1, x1=None, y1=None, facing1=None):

  """
  Return True if a1 is is the limited radar arc of a0.
  """

  # See the Limited Radar Arc diagram in the sheets.

  x0      = a0._x
  y0      = a0._y
  facing0 = a0._facing

  if a1 != None:
    x1      = a1._x
    y1      = a1._y
    facing1 = a1._facing
  
  angleofftail, angleoffnose, r, dx, dy = _relativepositions(x0, y0, facing0, x1, y1, facing1)
      
  if dx <= 0:
    return False
  elif dx <= _round(1.25 * math.sqrt(3/4)):
    return dy == 0
  elif dx <= _round(5.1 * math.sqrt(3/4)):
    return abs(dy) <= 0.6
  elif dx <= _round(10.1 * math.sqrt(3/4)):
    return abs(dy) <= 1.1
  else:
    return abs(dy) <= 1.6

  r += verticalrange()
  if r > 4:
    return False
  else:
    return r
    
##############################################################################
