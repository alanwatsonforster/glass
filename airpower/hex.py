from os import X_OK


def iscenterposition(x, y):

  """
  Return True if the point (x,y) in hex coordinates corresponds to the center 
  of a hex. Otherwise, return False.
  """

  if x % 2 == 0.0 and y % 1.0 == 0.00:
    return True
  elif x % 2 == 1.0 and y % 1.0 == 0.50:
    return True
  else:
    return False

def isedgeposition(x, y):

  """
  Return True if the point (x,y) in hex coordinates corresponds to (the center 
  of) the edge of a hex. Otherwise, return False.
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

def isvalidposition(x, y):

  """
  Return True if the point (x,y) in hex coordinates corresponds to the center 
  of a hex or to (the center of) the edge of a hex. Otherwise, return False.
  """

  return iscenterposition(x, y) or isedgeposition(x, y)

def areadjacent(x0, y0, x1, y1):

  """
  Return True if the positions (x0,y0) and (x1,y1) correspond the the centers 
  of adjacent hexes. Otherwise, return False.
  """

  assert isvalidposition(x0, y0)
  assert isvalidposition(x1, y1)

  if not iscenterposition(x0, y0) or not isoncenter(x1, y1):
    return False
  if abs(x1 - x0) == 1.0 and abs(y1 - y0) == 0.5:
    return True
  elif x1 == x0 and abs(y1 - y0) == 1.0:
    return True
  else:
    return False

def checkisvalidposition(x, y):

  """
  Raise a RuntimeError exception if the point (x,y) in hex coordinates does not 
  correspond to the center of a hex or to (the center of) the edge of a hex.
  """

  if not isvalidposition(x, y):
    raise RuntimeError("(%s,%s) is not the center or edge of a hex." % (x,y))

def isvalidfacing(x, y, facing):

  """
  Return True if facing is a valid facing at the position (x, y) in hex 
  coordinates, which must correspond to to the center of a hex or to (the 
  center of) the edge of a hex.
  """

  assert isvalidposition(x, y)

  if iscenterposition(x, y):
    return facing % 30 == 0

  if x % 2 == 0.5 and y % 1.0 == 0.25:
    return facing % 180 == 120
  elif x % 2 == 0.5 and y % 1.0 == 0.75:
    return facing % 180 == 60
  elif x % 2 == 1.5 and y % 1 == 0.25:
    return facing % 180 == 60
  elif x % 2 == 1.5 and y % 1.0 == 0.75:
    return facing % 180 == 120
  else:
    return facing % 180 == 0

def checkisvalidfacing(x, y, facing):

  """
  Raise a RuntimeError exception if facing is not a valid facing at the position 
  (x, y) in hex coordinates, which must correspond to to the center of a hex or 
  to (the center of) the edge of a hex.
  """

  assert isvalidposition(x, y)

  if not isvalidfacing(x, y, facing):
    raise RuntimeError("(%s,%s) is not the center or edge of a hex." % (x,y))

def nextposition(x, y, facing):

  """
  Return the coordinates of the next valid position after the point (x, y) with 
  respect to the facing.
  """

  assert isvalidposition(x, y)
  assert isvalidfacing(x, y, facing)

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

def centertoleft(x, y, facing):

  """
  Return the coordinates of the hex center to the left of the edge
  position (x, y) and where left is defined with respect to the facing.
  """

  assert isedgeposition(x, y)
  assert isvalidfacing(x, y, facing)

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

  return x, y
 
def centertoright(x, y, facing):

  """
  Return the coordinates of the hex center to the left of the edge
  position (x, y) and where right is defined with respect to the facing.
  """
  assert isedgeposition(x, y)
  assert isvalidfacing(x, y, facing)

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

