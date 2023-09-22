def isoncenter(x, y):
  if x % 2 == 0.0 and y % 1.0 == 0.00:
    return True
  elif x % 2 == 1.0 and y % 1.0 == 0.50:
    return True
  else:
    return False

def isonedge(x, y):
  if x % 2 == 0.0 and y % 1.0 == 0.50:
    return True
  elif x % 2 == 0.5 and y % 0.5 == 0.25:
    return True
  elif x % 2 == 1.0 and y % 1.0 == 0.00:
    return True
  elif x % 2 == 1.5 and y % 0.5 == 0.25:
    return True
  else:
    return False

def check(x, y):
  if not isoncenter(x, y) and not isonedge(x, y):
    raise ValueError("(%s,%s) are not valid hex coordinates ." % (x,y))
