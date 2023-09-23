# _altitudequantum must be 1 over an integral power of 2.
_altitudequantum = 1/8

def isvalidaltitude(altitude):

  """
  Return True if altitude is a valid altitude.
  """
  return isinstance(altitude, (int, float)) and altitude % 1 == 0 and altitude >= 0

def checkisvalidaltitude(altitude):

  """
  Raise a ValueError exception if z is not a valid altitude.
  """

  if not isvalidaltitude(altitude):
    raise ValueError("%s is not a valid altitude." % altitude)

def adjustaltitude(altitude, altitudecarry, altitudechange):

    """
    Adjust altitude by altitudechange, taking into account altitudecarry. 
    Return the new altitude and altitudecarry. 
    """

    # Here we do altitude arithmetic, ensuring that _altitude stays as an
    # non-negative integer and keeping track of fractions in _altitudecarry. 
    # We require altitude changes to be multiples of _altitudequantum.

    assert altitude % 1 == 0 and altitude >= 0
    assert abs(altitudecarry) < 1 and altitudecarry % _altitudequantum == 0
    assert altitudechange % _altitudequantum == 0

    altitude = altitude + altitudecarry + altitudechange
    if altitudechange >= 0:
      altitudecarry = altitude % +1
    else:
      altitudecarry = altitude % -1
    altitude = altitude - altitudecarry

    if altitude < 0:
      altitude = 0
      altitudecarry = 0

    assert altitude % 1 == 0 and altitude >= 0
    assert abs(altitudecarry) < 1 and altitudecarry % _altitudequantum == 0

    return altitude, altitudecarry

def formataltitudecarry(altitudecarry):

  """
  Return altitudecarry formatted as a signed fraction.
  """

  assert abs(altitudecarry) < 1 and altitudecarry % _altitudequantum == 0

  n = altitudecarry / _altitudequantum
  m = 1 / _altitudequantum

  if n == 0:
    return "0"

  while n % 2 == 0:
    n = n / 2
    m = m / 2
  return "%+d/%d" % (n, m)
  
def altitudeband(altitude):

  """
  Return the altitude band corresponding to altitude.
  """

  assert altitude % 1 == 0 and altitude >= 0

  if altitude <= 7:
    return "LO"
  elif altitude <= 16:
    return "ML"
  elif altitude <= 25:
    return "MH"
  elif altitude <= 35:
    return "HI"
  elif altitude <= 45:
    return "VH"
  elif altitude <= 60:
    return "EH"
  else:
    return "UH"

def terrainaltitude():

  """
  Return the altitude of the terrain.
  """

  return 0
