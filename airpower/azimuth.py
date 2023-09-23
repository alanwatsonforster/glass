_northfacing = 90

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
    raise ValueError("\"%s\" is not a valid orientation for north.")

def tofacing(azimuth):

  """
  Return the facing corresponding to the azimuth argument, which can be one of 
  the strings "N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", 
  "WNW", or "NNW", or a number, specifying the azimuth in degrees from north 
  through east.

  Note that "NE", "SE", "SW", and "NW" are not valid azimuths.
  """

  named = {
    "N":   0, "NNE":  30, "ENE":  60,
    "E":  90, "ESE": 120, "SSE": 150, 
    "S": 180, "SSW": 210, "WSW": 240, 
    "W": 270, "WNW": 300, "NNW": 330, 
  }
  obsolete = {
    "NE": "ENE", "SE": "ESE", "SW": "WSW", "NW": "WNW"
  }

  if azimuth in named:
    return (_northfacing - named[azimuth]) % 360
  elif azimuth in obsolete:
    raise ValueError("%s is not a valid azimuth (use %s instead)." % (azimuth, superseded[azimuth]))
  else:
    return (_northfacing - azimuth) % 360

def fromfacing(facing):

  """
  Return the azimuth corresponding to the facing argument. If the azimuth
  is a multiple of 30 degrees, the corresponding string "N", "NNE", "ENE", "E", 
  "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", or "NNW" is returned. Otherwise,
  a number is returned, giving the azimuth in degrees from north through east.
  """

  azimuth = (_northfacing - facing) % 360
  if azimuth % 30 == 0:
    named = ["N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", "NNW"]
    return named[azimuth // 30]
  else:
    return azimuth
