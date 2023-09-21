print("airpower.azimuth")

_northfacing = 90

def setnorth(s):
  global _northfacing
  if s == "right":
    _northfacing = 0
  elif s == "up":
    _northfacing = 90
  elif s == "left":
    _northfacing = 180
  elif s == "down":
    _northfacing = 270
  else:
    raise ValueError("\"%s\" is not a valid orientation.")

def tofacing(azimuth):
  named = {
    "N":   0, "NNE":  30, "ENE":  60,
    "E":  90, "ESE": 120, "SSE": 150, 
    "S": 180, "SSW": 210, "WSW": 240, 
    "W": 270, "WNW": 300, "NNW": 330, 
  }
  superseded = {
    "NE": "ENE", "SE": "ESE", "SW": "WSW", "NW": "WNW"
  }
  if azimuth in named:
    azimuth = named[azimuth]
  elif azimuth in superseded:
    raise ValueError("use azimuth \"%s\" instead of \"%s\"" % (superseded[azimuth], azimuth))
  return (_northfacing - azimuth) % 360

def toazimuth(facing):
  azimuth = (_northfacing - facing) % 360
  if azimuth % 30 == 0:
    named = ["N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", "NNW"]
    return named[azimuth // 30]
  else:
    return azimuth
