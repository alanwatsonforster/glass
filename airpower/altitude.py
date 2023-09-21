print("airpower.altitude")

def altitudeband(altitude):
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
