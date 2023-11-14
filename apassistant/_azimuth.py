import apassistant._variants as apvariants

_northfacing = 90

def isvalidazimuth(azimuth):
  try:
    facing = tofacing(azimuth)
    return True
  except:
    return False

def setnorth(orientation):

  """
  Set the orientation of north. The orientation argument can be one of the 
  strings "up", "down", "right", or "left".
  """

  global _northfacing
  if orientation == "right":
    _northfacing = 0
  elif orientation == "up":
    _northfacing = 90
  elif orientation == "left":
    _northfacing = 180
  elif orientation == "down":
    _northfacing = 270
  else:
    raise RuntimeError("\"%s\" is not a valid orientation for north.")

def tofacing(azimuth):

  """
  Return the facing corresponding to the azimuth argument, which can be one of 
  the strings "N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", 
  "WNW", or "NNW", or a number, specifying the azimuth in degrees from north 
  through east.

  If the variant "disallow ENE/ESE/WSW/WNW" is selected, these are not valid 
  azimuths. 
  
  If the variant "disallow NE/SE/SW/NW" is selected, these are also not valid 
  azimuths.
  """

  named = {
    "N"  :   0, 
    "NNE":  30, 
    "E"  :  90, 
    "SSE": 150, 
    "S"  : 180, 
    "SSW": 210, 
    "W"  : 270, 
    "NNW": 330, 
  }
  if azimuth in named:
    azimuth = named[azimuth]

  if not apvariants.withvariant("disallow NE/SE/SW/NW"):
    named = {
      "NE":  60,
      "SE": 120,
      "SW": 240, 
      "NW": 300,
    }
    if azimuth in named:
      azimuth = named[azimuth]

  if not apvariants.withvariant("disallow ENE/ESE/WSW/WNW"):
    named = {
      "ENE":  60,
      "ESE": 120,
      "WSW": 240, 
      "WNW": 300,
    }
    if azimuth in named:
      azimuth = named[azimuth]

  if not isinstance(azimuth, int):
    raise RuntimeError("invalid azimuth %r." % azimuth)
  
  return (_northfacing - azimuth) % 360

def fromfacing(facing):

  """
  Return the azimuth corresponding to the facing argument. If the azimuth
  is a multiple of 30 degrees, the corresponding string "N", "NNE", "ENE", "E", 
  "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", or "NNW" is returned. Otherwise,
  a number is returned, giving the azimuth in degrees from north through east.

  If the variant "prefer NE/SE/SW/NW" is selected, these are returned instead 
  of ENE/ESE/WSW/WNW.
  """

  if apvariants.withvariant("prefer NE/SE/SW/NW"):
    named = ["N", "NNE", "NE" , "E", "SE" , "SSE", "S", "SSW", "SW" , "W", "NW" , "NNW"]
  else:
    named = ["N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", "NNW"]

  azimuth = (_northfacing - facing) % 360
  if azimuth % 30 == 0:
    return named[azimuth // 30]
  else:
    return azimuth
