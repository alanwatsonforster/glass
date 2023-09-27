# See the "Transonic/Supersonic Speed Reference Table" chart and the "Speed of 
# Sound" and "Transonic Speeds" section of rule 6.6.

def m1speed(altitudeband):

  """
  Return the M1 speed in the specified altitude band.
  """

  if altitudeband == "LO" or altitudeband == "ML":
    return 7.5
  elif altitudeband == "MH" or altitudeband == "HI":
    return 7.0
  else:
    return 6.5

def htspeed(altitudeband):

  """
  Return the high-transonic speed in the specified altitude band.
  """

  return m1speed(altitudeband) - 0.5

def ltspeed(altitudeband):

  """
  Return the low-transonic speed in the specified altitude band.
  """

  return m1speed(altitudeband) - 1.0
