def iscenter(x, y):

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

def isedge(x, y):

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

  return iscenter(x, y) or isedge(x, y)

def areadjacent(x0, y0, x1, y1):

  """
  Return True if the points (x0,y0) and (x1,y1) correspond the the centers of 
  adjacent hexes. Otherwise, return False.
  """

  if not iscenter(x0, y0) or not isoncenter(x1, y1):
    return False
  if abs(x1 - x0) == 1.0 and abs(y1 - y0) == 0.5:
    return True
  elif x1 == x0 and abs(y1 - y0) == 1.0:
    return True
  else:
    return False

def checkisvalidposition(x, y):

  """
  Raise a ValueError exception if the point (x,y) in hex coordinates does not 
  correspond to the center of a hex or to (the center of) the edge of a hex.
  """

  if not isvalidposition(x, y):
    raise ValueError("(%s,%s) is not the center or edge of a hex." % (x,y))

def isvalidfacing(x, y, facing):

  """
  Return True if facing is a valid facing at the point (x, y) in hex 
  coordinates, which must correspond to to the center of a hex or to (the 
  center of) the edge of a hex.
  """

  checkisvalidposition(x, y)

  if iscenter(x, y):
    return facing % 30 == 0

  if x % 2 == 0.5 and y % 1.0 == 0.25:
    return facing % 180 == 120
  elif x % 2 == 0.5 and y % 1.0 == 0.75:
    return facing % 180 == 60
  elif x % 2 == 1.0 and y % 1 == 0.25:
    return facing % 180 == 60
  elif x % 2 == 1.0 and y % 1.0 == 0.75:
    return facing % 180 == 120
  else:
    return facing % 180 == 0

def checkisvalidfacing(x, y, facing):

  """
  Raise a ValueError exception if facing is not a valid facing at the point 
  (x, y) in hex coordinates, which must correspond to to the center of a hex or 
  to (the center of) the edge of a hex.
  """

  if not isvalidfacing(x, y, facing):
    raise ValueError("(%s,%s) is not the center or edge of a hex." % (x,y))
