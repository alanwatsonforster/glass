import math
import apengine.hex as aphex

def angleoff(self, other):

  """
  Determine the angle-off another aircraft's tail.
  """

  # See rule 9.2.

  def fromxy(xself, yself, facingself, xother, yother, facingother):

    dx = xother - xself
    dy = yother - yself

    if dx == 0 and dy == 0:
      dtheta = facingself - facingother
    else:
      dtheta = math.degrees(math.atan2(dy, dx)) - facingother

    dtheta %= 360
    if dtheta > 180:
      dtheta -= 360
    dtheta = dtheta

    # Round to 1/16 of a degree
    if dtheta >= 0:
      dtheta = int(dtheta * 16 + 0.5) / 16
    else:
      dtheta = int(dtheta * 16 - 0.5) / 16

    return dtheta

  xself       = self._x
  yself       = self._y
  facingself  = self._facing

  xother      = other._x
  yother      = other._y
  facingother = other._facing

  dtheta = fromxy(xself, yself, facingself, xother, yother, facingother)

  # If the aircraft fall on the 30, 60, 90, 120, or 150 degree lines and
  # one aircraft is faster than the other, move the faster aircraft
  # forward one hex and recompute.
  if dtheta != 0 and abs(dtheta) != 180 and dtheta % 30 == 0:
    if self._speed > other._speed:
      xself, yself = aphex.forward(xself, yself, facingself)
    elif other._speed > self._speed:
      xother, yother = aphex.forward(xother, yother, facingother)
    dtheta = fromxy(xself, yself, facingself, xother, yother, facingother)

  # To be on the 0 or 180 degree lines, the aircraft has to be facing
  # the other.
  if dtheta == 0 and facingself == facingother:
    return "0 line"
  elif dtheta == 180 and abs(facingself -facingother) == 180:
    return "180 line"
    
  # Resolve cases on the 30, 60, 90, 120, and 150 degree lines in favor
  # of the aircraft (round 150 to 180).
  if abs(dtheta) <= 30:
    return "30 arc"
  elif abs(dtheta) <= 60:
    return "60 arc"
  elif abs(dtheta) <= 90:
    return "90 arc"
  elif abs(dtheta) <= 120:
    return "120 arc"
  elif abs(dtheta) < 150:
    return "150 arc"
  else:
    return "180 arc"

