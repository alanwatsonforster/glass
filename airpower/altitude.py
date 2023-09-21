import math

print("airpower.altitude")

# _altitudequantum must be 1 over an integral power of 2.
_altitudequantum = 1/8

def _checkaltitude(altitude):
  if not isinstance(altitude, (int, float)) or altitude % 1 != 0 or altitude < 1:
    raise ValueError("invalid altitude %s." % altitude)

def _adjustaltitude(altitude, altitudecarry, altitudechange):

    # Here we do altitude arithmetic, ensuring that _altitude stays as an
    # integer and keeping track of fractions in _altitudecarry. We require 
    # altitude changes to be multiples of _altitudequantum.

    assert altitude % 1 == 0 and altitude > 0
    assert altitudecarry % _altitudequantum == 0
    assert altitudechange % _altitudequantum == 0

    altitude = altitude + altitudecarry + altitudechange
    if altitudechange >= 0:
      altitudecarry = altitude - math.floor(altitude)
    else:
      altitudecarry = altitude - math.ceil(altitude)
    altitude = altitude - altitudecarry

    assert altitude % 1 == 0
    assert altitudecarry % _altitudequantum == 0

    return altitude, altitudecarry

def _formataltitudecarry(altitudecarry):

  assert altitudecarry % _altitudequantum == 0

  n = altitudecarry / _altitudequantum
  m = 1 / _altitudequantum

  if n == 0:
    return "0"

  while n % 2 == 0:
    n = n / 2
    m = m / 2
  return "%+d/%d" % (n, m)
  
def _altitudeband(altitude):

  assert altitude % 1 == 0 and altitude > 0

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
