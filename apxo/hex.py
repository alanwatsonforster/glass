"""
Manipulation of hex coordinates.
"""

import math

def iscenter(x, y):

  """
  Return True if the point (x,y) in hex coordinates corresponds to a center.
  Otherwise, return False.
  """

  if x % 2 == 0.0 and y % 1.0 == 0.00:
    return True
  elif x % 2 == 1.0 and y % 1.0 == 0.50:
    return True
  else:
    return False

def isside(x, y):

  """
  Return True if the point (x,y) in hex coordinates corresponds to a side.
  Otherwise, return False.
  """

  if x % 2 == 0.0 and y % 1.0 == 0.5:
    return True
  elif x % 2 == 0.5 and y % 0.5 == 0.25:
    return True
  elif x % 2 == 1.0 and y % 1.0 == 0.0:
    return True
  elif x % 2 == 1.5 and y % 0.5 == 0.25:
    return True
  else:
    return False

def isvalid(x, y, facing=None):

  """
  Return True if the point (x,y) in hex coordinates corresponds to a center or
  side and the facing, if given, is a multiple of 30 degrees for centers
  and parallel to the side for sides. Otherwise, return False.
  """

  if iscenter(x, y):
    if facing == None:
      return True
    else:
      return facing % 30 == 0
  elif isside(x, y):
    if facing == None:
      return True
    elif (x % 2 == 0.5 and y % 1 == 0.25) or (x % 2 == 1.5 and y % 1 == 0.75):
      return facing % 180 == 120
    elif (x % 2 == 0.5 and y % 1 == 0.75) or (x % 2 == 1.5 and y % 1 == 0.25):
      return facing % 180 == 60
    else:
      return facing % 180 == 0
  else:
    return False

def checkisvalid(x, y, facing=None):

  """
  Raise a RuntimeError exception if the point (x,y) in hex coordinates does not 
  correspond to a center or side.
  """

  if not isvalid(x, y):
    raise RuntimeError("(%r,%r) is not a valid hex center or hex side." % (x, y))

  if facing != None and not isvalid(x, y, facing=facing):
      raise RuntimeError("%r is not a valid facing for (%r,%r)." % (facing, x, y))

def areadjacent(x0, y0, x1, y1):

  """
  Return True if the positions (x0,y0) and (x1,y1) correspond to the centers 
  of adjacent hexes. Otherwise, return False.
  """

  assert isvalid(x0, y0)
  assert isvalid(x1, y1)

  if not iscenter(x0, y0) or not isoncenter(x1, y1):
    return False
  if abs(x1 - x0) == 1.0 and abs(y1 - y0) == 0.5:
    return True
  elif x1 == x0 and abs(y1 - y0) == 1.0:
    return True
  else:
    return False

def forward(x, y, facing):

  """
  Return the coordinates of the next valid position forward from the point (x, y) with 
  respect to the facing.
  """

  assert isvalid(x, y, facing=facing)


  def dxdy(facing,):
    if facing >= 180:
      dx, dy = dxdy(facing - 180)
      return -dx, -dy

    if facing > 90:
      dx, dy = dxdy(180 - facing)
      return -dx, +dy

    i = facing // 30
    return [+1.00, +1.00, +0.50, +0.00][i], [+0.00, +0.50, +0.75, +1.00][i]

  dx, dy = dxdy(facing)

  return x + dx, y + dy

def slide(x, y, facing, sense):

  """
  Return the coordinates after performing a slide from the point (x, y) with 
  respect to the facing and sense. The forward part of the slide has already been
  carried out.
  """

  assert isvalid(x, y, facing=facing)
  assert sense == "R" or sense == "L"

  def dxdy(facing, sense):

    if sense == "R":
      othersense = "L"
    else:
      othersense = "R"

    if facing >= 180:
      dx, dy = dxdy(facing - 180, sense)
      return -dx, -dy

    if facing > 90:
      dx, dy = dxdy(180 - facing, othersense)
      return -dx, +dy

    i = facing // 30
    if sense == "R":
      return [+0.00, +0.00, +0.50, +1.00][i], [-0.50, -1.00, -0.25, -0.50][i]
    else:
      return [+0.00, -1.00, -0.50, -1.00][i], [+0.50, +0.50, +0.25, -0.50][i]

  dx, dy = dxdy(facing, sense)

  return x + dx, y + dy

def displacementroll(x, y, facing, sense):

  """
  Return the coordinates after performing a displacement roll from the point
  (x, y) with respect to the facing and sense. The forward part of the 
  displacement roll has already beeen carried out.
  """

  # It's identical to a slide.

  return slide(x, y, facing, sense)

def lagroll(x, y, facing, sense):

  """
  Return the coordinates after performing a lag roll from the point (x, y) with 
  respect to the facing and sense. The forward part of the lag roll has already been
  carried out.
  """

  assert isvalid(x, y, facing=facing)
  assert sense == "R" or sense == "L"

  if isside(x, y):
    return sidetocenter(x, y, facing, sense)

  lastx, lasty = forward(x, y, (facing + 180) % 360)
  if isside(lastx, lasty):
    return sidetocenter(lastx, lasty, facing, sense)

  return slide(x, y, facing, sense)

def sidetocenter(x, y, facing, sense):

  """
  Return the coordinates of the center adjacent to the side (x, y) in the 
  given sense with respect to the facing.
  """

  assert isside(x, y)
  assert isvalid(x, y, facing=facing)
  assert sense == "R" or sense == "L"

  def dxdy(facing, sense):

    if sense == "R":
      othersense = "L"
    else:
      othersense = "R"

    if facing >= 180:
      dx, dy = dxdy(facing - 180, sense)
      return -dx, -dy

    i = facing // 60
    if sense == "R":
      return [+0.00, +0.50, +0.50][i], [-0.50, -0.25, +0.25][i]
    else:
      return [+0.00, -0.50, -0.50][i], [+0.50, +0.25, -0.25][i]

  dx, dy = dxdy(facing, sense)

  return x + dx, y + dy

def sidetocenters(x, y):

  """
  Return the coordinates (x0, y0) and (x1, y1) of the centers adjacent
  to the side (x, y) as a tuple (x0, y0, x1, y1).
  """

  assert isside(x, y)

  if x % 2 == 0.5 and y % 1 == 0.25:
    x0, y0 = x - 0.5, y - 0.25
    x1, y1 = x + 0.5, y + 0.25
  elif x % 2 == 0.5 and y % 1 == 0.75:
    x0, y0 = x - 0.5, y + 0.25
    x1, y1 = x + 0.5, y - 0.25      
  elif x % 2 == 1.5 and y % 1 == 0.25:
    x0, y0 = x - 0.5, y + 0.25
    x1, y1 = x + 0.5, y - 0.25   
  elif x % 2 == 1.5 and y % 1 == 0.75:
    x0, y0 = x - 0.5, y - 0.25
    x1, y1 = x + 0.5, y + 0.25
  else:
    x0, y0 = x, y - 0.5
    x1, y1 = x, y + 0.5

  return x0, y0, x1, y1

def tophysical(x, y):

  """
  Return the physical coordinates corresponding to the given hex coordinates.
  """

  return x * math.sqrt(3/4), y

def fromphysical(x,y):

  """
  Return the hex coordinates corresponding to the given physical coordinates.
  """

  return x / math.sqrt(3/4), y

def distance(x0, y0, x1, y1):

  """
  Returns the distance in hexes between hex coordinates (x0, y0) and (x1, y1).
  """

  # The errata says this about range: "When determining range where one
  # or more aircraft are on hexsides, count only the full hexes between
  # them. Take the shortest number of hexes."

  # Our algorithm is as follows. While points 0 and 1 are separated by 1
  # unit or more in x or y in the hex grid (i.e., at least one hex),
  # generate six positions around point 0 each offset by 1 hex and move
  # point 0 to the one closest to point 1. Each time point 0 is moved,
  # the distance increases by 1.

  def physicaldistance(x0, y0, x1, y1):
    x0, y0 = tophysical(x0, y0)
    x1, y1 = tophysical(x1, y1)
    return math.hypot(x1 - x0, y1 - y0)
    
  d = 0
  while abs(x1 - x0) >= 1 or abs(y1 - y0) >= 1:
    p = [
      (x0 + 0.0, y0 + 1.0), 
      (x0 + 1.0, y0 + 0.5), 
      (x0 + 1.0, y0 - 0.5), 
      (x0 + 0.0, y0 - 1.0), 
      (x0 - 1.0, y0 - 0.5), 
      (x0 - 1.0, y0 + 0.5)
    ]
    for x, y in p:
      if physicaldistance(x, y, x1, y1) < physicaldistance(x0, y0, x1, y1):
        x0, y0 = x, y
    d += 1  

  return d
