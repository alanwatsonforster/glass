import apassistant._map  as apmap
import apassistant._hex as aphex

def isvalidaltitude(x):

  """
  Return True if altitude is a valid altitude.
  """

  return isinstance(x, int) and 0 <= x

def isvalidaltitudecarry(x):

  """
  Return true if the argument is a valid altitude carry.
  """

  return isinstance(x, (int, float)) and 0 <= x and x < 1

def checkisvalidaltitude(x):

  """
  Raise a RuntimeError exception if the argument is not a valid altitude.
  """

  if not isvalidaltitude(x):
    raise RuntimeError("%r is not a valid altitude." % x)

def adjustaltitude(altitude, altitudecarry, altitudechange):

    """
    Adjust altitude by altitudechange, taking into account altitudecarry. 
    Return the new altitude and altitudecarry. 
    """

    # See rule 8.1.4.

    assert isvalidaltitude(altitude)
    assert isvalidaltitudecarry(altitudecarry)
    assert isinstance(altitudechange, (int, float))

    if altitudechange < 0:

      # Carry is only for climbing.
      assert altitudecarry == 0
      assert altitudechange % 1 == 0
      altitude += altitudechange

    else:

      altitude += altitudecarry + altitudechange
      altitudecarry = altitude % 1

    altitude = int(altitude)

    # We're working in float, and altitudecarry can be multiples of 1/12
    # (raw CC of 0.25 multipled by the supersonic factor of 2/3) which
    # can give a rounding error. Therefore, we check against full
    # altitude levels with a tolerance.

    tolerance = 1e-6
    if altitudecarry < tolerance:
      altitudecarry = 0
    elif altitudecarry > 1 - tolerance:
      altitudecarry = 0
      altitude += 1

    if altitude < 0:
      altitude = 0
      altitudecarry = 0

    assert isvalidaltitude(altitude)
    assert isvalidaltitudecarry(altitudecarry)

    return altitude, altitudecarry
  
def altitudeband(altitude):

  """
  Return the altitude band corresponding to altitude.
  """

  assert isvalidaltitude(altitude)

  # See rule 8.0.

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

def terrainaltitude(x, y):

  """
  Return the altitude of the terrain.
  """

  assert aphex.isvalid(x, y)

  if apmap.isonmap(x, y):
    return apmap.altitude(x, y)
  else:
    return 0
