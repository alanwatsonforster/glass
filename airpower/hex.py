"""
Manipulation of hex coordinates.
"""


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

def isedge(x, y):

  """
  Return True if the point (x,y) in hex coordinates corresponds to an edge.
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
  edge and the facing, if given, is a multiple of 30 degrees for centers
  and parallel to the edge foe edges. Otherwise, return False.
  """

  if iscenter(x, y):
    if facing == None:
      return True
    else:
      return facing % 30 == 0
  elif isedge(x, y):
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
  correspond to a center or edge.
  """

  if not isvalid(x, y):
    raise RuntimeError("(%r,%r) is not the center or edge of a hex." % (x, y))

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

def next(x, y, facing):

  """
  Return the coordinates of the next valid position after the point (x, y) with 
  respect to the facing.
  """

  assert isvalid(x, y, facing=facing)

  if facing == 0:
    x += +1.00
    y += +0.00
  elif facing == 30:
    x += +1.00
    y += +0.50
  elif facing == 60:
    x += +0.50
    y += +0.75
  elif facing == 90:
    x += +0.00
    y += +1.00
  elif facing == 120:
    x += -0.50
    y += +0.75
  elif facing == 150:
    x += -1.00
    y += +0.50
  elif facing == 180:
    x += -1.00
    y += +0.00
  elif facing == 210:
    x += -1.00
    y += -0.50
  elif facing == 240:
    x += -0.50
    y += -0.75
  elif facing == 270:
    x += -0.00
    y += -1.00
  elif facing == 300:
    x += +0.50
    y += -0.75
  elif facing == 330:
    x += +1.00
    y += -0.50
  
  return x, y

def slide(x, y, facing, sense):

  """
  Return the coordinates of the next valid slide position after the point (x, y) with 
  respect to the facing and sense. The forward part of the slide has already been
  carried out.
  """

  assert isvalid(x, y, facing=facing)
  assert sense == "R" or sense == "L"

  if facing == 0:
    if sense == "R":
      y += -0.5
    else:
      y += +0.5
  elif facing == 30:
    if sense == "R":
      y += -1.0
    else:
      x += -1.0
      y += +0.5
  elif facing == 60:
    if sense == "R":
      x += +0.50
      y += -0.25
    else:
      x += -0.50
      y += +0.25
  elif facing == 90:
    if sense == "R":
      x += +1.0
      y += -0.5
    else:
      x += -1.0
      y += -0.5
  elif facing == 120:
    if sense == "R":
      x += +0.50
      y += +0.25
    else:
      x += -0.50
      y += -0.25
  elif facing == 150:
    if sense == "R":
      x += +1.00
      y += +0.50
    else:
      y += -1.0
  elif facing == 180:
    if sense == "R":
      y += +0.5
    else:
      y += -0.5
  elif facing == 210:
    if sense == "R":
      y += +1.0
    else:
      x += +1.0
      y += -0.5
  elif facing == 240:
    if sense == "R":
      x += -0.50
      y += +0.25
    else:
      x += +0.50
      y += -0.25
  elif facing == 270:
    if sense == "R":
      x += -1.0
      y += +0.5
    else:
      x += +1.0
      y += +0.5
  elif facing == 300:
    if sense == "R":
      x += -0.50
      y += -0.25
    else:
      x += +0.50
      y += +0.25
  elif facing == 330:
    if sense == "R":
      x += -1.00
      y += -0.50
    else:
      y += +1.0

  return x, y

def edgetocenter(x, y, facing, sense):

  """
  Return the coordinates of the center adjacent to the edge (x, y) in the 
  given sense with respect to the facing.
  """

  assert isedge(x, y)
  assert isvalid(x, y, facing=facing)
  assert sense == "L" or sense == "R"

  if sense == "L":
    if facing == 0:
      y += 0.5
    elif facing == 60:
      x -= 0.50
      y += 0.25
    elif facing == 120:
      x -= 0.50
      y -= 0.25
    elif facing == 180:
      y -= 0.5
    elif facing == 240:
      x += 0.50
      y -= 0.25
    elif facing == 300:
      x += 0.50
      y += 0.25
  elif sense == "R":
    if facing == 0:
      y -= 0.5
    elif facing == 60:
      x += 0.50
      y -= 0.25
    elif facing == 120:
      x += 0.50
      y += 0.25
    elif facing == 180:
      y += 0.5
    elif facing == 240:
      x -= 0.50
      y += 0.25
    elif facing == 300:
      x -= 0.50
      y -= 0.25
    
  return x, y

def edgetocenters(x, y):

  """
  Returns the coordinates (x0, y0) and (x1, y1) of the centers adjacent
  to the edge (x, y) as a tuple (x0, y0, x1, y1).
  """

  assert isedge(x, y)

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
