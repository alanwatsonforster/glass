def turnrequirement(altitudeband, speed, rate):

  """
  Determine the turn requirement accoring to the Air Power Integrated Turn 
  Charts.
  """

  speed = int(speed)
  if speed < 8:
    ispeed = speed - 1
  elif speed < 10:
    ispeed = 7
  elif speed < 12:
    ispeed = 8
  elif speed < 14:
    ispeed = 9
  else:
    ispeed = 10
  
  irate = ["EZ", "TT", "HT", "BT", "ET"].index(rate)

  if altitudeband == "LO" or altitudeband == "ML":
    raw = [
      [ 60,  1,  2,  3,  4,  6,  8, 10, 12, 14, 16, 20, ],
      [ 90, 60,  1,  2,  3,  4,  5,  6,  8, 19, 12, 14, ],
      [  0, 90, 60,  1,  2,  2,  3,  4,  6,  8, 10, 12, ],
      [  0,  0, 90, 60,  1,  1,  2,  3,  4,  6,  8, 10, ],
      [  0,  0,  0, 60, 60,  1,  1,  2,  3,  4,  6,  8, ],
    ][irate][ispeed]
  elif altitudeband == "MH":
    raw = [
      [  1,  2,  3,  4,  6,  8, 10, 12, 14, 16, 18, 22, ],
      [ 60,  1,  2,  3,  4,  6,  7,  8, 10, 12, 14, 18, ],
      [  0, 60,  1,  2,  3,  4,  5,  6,  8, 10, 12, 14, ],
      [  0,  0, 60,  1,  2,  2,  3,  4,  6,  7, 10, 11, ],
      [  0,  0,  0, 60,  1,  1,  2,  2,  4,  5,  7,  9, ],
    ][irate][ispeed]
  elif altitudeband == "HI":
    raw = [
      [  2,  3,  4,  6,  8, 10, 12, 14, 16, 18, 20, 24, ],
      [  1,  2,  3,  4,  5,  6,  8, 10, 12, 14, 16, 20, ],
      [  0,  1,  2,  3,  4,  5,  6,  8,  9, 10, 13, 16, ],
      [  0,  0,  1,  2,  3,  3,  4,  6,  7,  8, 10, 12, ],
      [  0,  0,  0,  1,  2,  2,  3,  4,  5,  6,  8, 10, ],
    ][irate][ispeed]
  elif altitudeband == "VH":
    raw = [
      [  2,  4,  6,  8, 10, 12, 14, 16, 18, 20, 22, 24, ],
      [  1,  2,  4,  6,  8,  9, 10, 13, 15, 17, 20, 22, ],
      [  0,  0,  3,  4,  6,  7,  8, 10, 12, 14, 17, 20, ],
      [  0,  0,  0,  3,  4,  5,  6,  7,  9, 11, 14, 16, ],
      [  0,  0,  0,  0,  3,  4,  5,  6,  7,  8, 10, 12, ],
    ][irate][ispeed]
  else:
    raw = [
      [  3,  6,  8, 10, 12, 14, 16, 18, 20, 22, 24, 28, ],
      [  0,  4,  6,  8, 10, 12, 13, 14, 16, 18, 21, 24, ],
      [  0,  0,  4,  6,  7,  8, 10, 11, 13, 15, 18, 21, ],
      [  0,  0,  0,  4,  5,  6,  7,  8, 10, 12, 14, 18, ],
      [  0,  0,  0,  0,  4,  5,  6,  7,  9, 10, 12, 14, ],
    ][irate][ispeed]
    if altitudeband == "UH" and raw != 0:
      raw += 2
  
  if raw == 0:
    return None
  else:
    return raw

def determineturnrate(altitudeband, speed, turnfp, facingchange):

  """
  Return the minimum turn rate capable of a turn of the given facing change 
  after expending the given number of FPs. If no turn rate is capable, return 
  None.
  """

  for rate in ["EZ", "TT", "HT", "BT", "ET"]:
    requirement = turnrequirement(altitudeband, speed, rate)
    if requirement == None:
      return None
    if facingchange == 30 and turnfp >= requirement:
      return rate
    elif facingchange <= requirement:
      return rate
