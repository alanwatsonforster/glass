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

def iscenteroredge(x, y):
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

def checkiscenteroredge(x, y):
  """
  Raise a ValueError exception if the point (x,y) in hex coordinates does not 
  correspond to the center of a hex or to (the center of) the edge of a hex
  """
  if not iscenteroredge(x, y):
    raise ValueError("(%s,%s) is not the center or edge of a hex." % (x,y))
