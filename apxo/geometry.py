##############################################################################
import math
import apxo      as ap
import apxo.hex as aphex
import apxo.log as aplog

##############################################################################

def showgeometry(A, B, note=False):

  """
  Show the geometry of aircraft B with respect to the aircraft A.
  """

  A._logbreak()
  A._logline()

  Aname = A._name
  Bname = B._name

  apturn.checkinsetuporturn()

  angleofftail = A.angleofftail(B)
  if angleofftail == "0 line" or angleofftail == "180 line":
    A._logevent("%s has %s on its %s." % (Bname, Aname, angleofftail))
  else:
    A._logevent("%s has %s in its %s." % (Bname, Aname, angleofftail))

  angleofftail = B.angleofftail(A)
  if angleofftail == "0 line" or angleofftail == "180 line":
    A._logevent("%s is on the %s of %s." % (Bname, angleofftail, Aname))
  else:
    A._logevent("%s is in the %s of %s." % (Bname, angleofftail, Aname))

  inlimitedradararc = A.inlimitedradararc(B)
  if inlimitedradararc:
    A._logevent("%s is in the limited radar arc of %s." % (Bname, Aname))
  else:
    A._logevent("%s is not in the limited radar arc of %s." % (Bname, Aname))  

  A._lognote(note)
  A._logline()
      
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

def samehorizontalposition(A0, A1):

  """
  Return True if aircraft A0 to A1 are in the same horizontal position, 
  Bwise return False.
  """

  return A0.x() == A1.x() and A0.y() == A1.y()

##############################################################################

def horizontalrange(A0, A1):

  """
  Return the horizontal range in hexes from aircraft A0 to A1.
  """

  return aphex.distance(A0.x(), A0.y(), A1.x(), A1.y())

##############################################################################

def relativepositions(x0, y0, facing0, x1, y1, facing1):

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

def angleofftail(A0, A1, 
  arconly=False,
  x1=None, y1=None, facing1=None):

  """
  Return the angle of A0 off the tail of A1.
  """

  # See rule 9.2.

  def truegeometry(x0, y0, facing0, x1, y1, facing1):
    angleofftail, angleoffnose, r, dx, dy = relativepositions(x0, y0, facing0, x1, y1, facing1)
    return angleofftail, angleoffnose, r

  x0      = A0.x()
  y0      = A0.y()
  facing0 = A0.facing()

  if A1 is not None:
    x1      = A1.x()
    y1      = A1.y()
    facing1 = A1.facing()

  angleofftail, angleoffnose, r = truegeometry(x0, y0, facing0, x1, y1, facing1)

  if r > 0 and angleofftail != 0.0 and angleofftail != 180.0 and angleofftail % 30 == 0.0:

    # Distinguish cases on the 30, 60, 90, 120, and 150 degree arcs.

    # If 0 is slower, it falls in the rear arc.
    # If 0 is faster and headed behind 0, it falls in the rear arc. 
    # If 0 is faster and headed in front of 1, it falls in the front arc.

    inreararc = False
    infrontarc = False
    if A0.speed() < A1.speed():
      inreararc = True
    elif A0.speed() > A1.speed() and angleoffnose != 0:
      if (angleofftail > 0 and angleoffnose > 0) or (angleofftail < 0 and angleoffnose < 0):
        infrontarc = True
      elif (angleofftail > 0 and angleoffnose < 0) or (angleofftail < 0 and angleoffnose > 0):
        inreararc = True

    if (infrontarc and angleofftail > 0) or (inreararc and angleofftail < 0):
        angleofftail += 1
    elif (infrontarc and angleofftail < 0) or (inreararc and angleofftail > 0):
        angleofftail -= 1

  if not arconly:
    # To be on the 0 or 180 degree lines, the aircraft has to be facing
    # the B.
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

def inlimitedradararc(A0, A1, x1=None, y1=None, facing1=None):

  """
  Return True if A1 is is the limited radar arc of A0.
  """

  x0      = A0.x()
  y0      = A0.y()
  facing0 = A0.facing()

  if A1 != None:
    x1      = A1.x()
    y1      = A1.y()
    facing1 = A1.facing()

  # See rule 16.5.

  if A0._flighttype == "VD":
    fmax, fmin = -2.0, -9.0
  elif A0._flighttype == "SD" or A0._flighttype == "UD":
    fmax, fmin = -0.5, -3.0
  elif A0._flighttype == "LVL":
    fmax, fmin = +0.5, -0.5
  elif A0._flighttype == "SC":
    fmax, fmin = +2.0, +0.0
  elif A0._flighttype == "ZC":
    fmax, fmin = +4.0, +0.5
  else:
    fmax, fmin = +9.0, +2.0

  r = horizontalrange(A0, A1)
  altitudemax = A0.altitude() + int(fmax * r)
  altitudemin = A0.altitude() + int(fmin * r)
  if A1.altitude() < altitudemin or altitudemax < A1.altitude():
    return False
  
  # See the Limited Radar Arc diagram in the sheets.

  angleofftail, angleoffnose, r, dx, dy = relativepositions(x0, y0, facing0, x1, y1, facing1)
      
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
    
##############################################################################



