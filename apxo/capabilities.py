import apxo.altitude as apaltitude
import apxo.speed    as apspeed
import apxo.variants as apvariants

def power(a, powersetting):
  return a._aircraftdata.power(a._configuration, powersetting)

def spbr(a):
  return a._aircraftdata.spbr(a._configuration)

def fuelrate(a):
  return a._aircraftdata.fuelrate(a._powersetting)

def engines(a):
  return a._aircraftdata.engines()

def powerfade(a):
  return a._aircraftdata.powerfade(a._speed, a._altitude)

def lowspeedliftdevicename(a):
    return a._aircraftdata.lowspeedliftdevicename()

def lowspeedliftdevicelimit(a):
    return a._aircraftdata.lowspeedliftdevicelimit()
    
def lowspeedliftdeviceselectable(a):
    return a._aircraftdata.lowspeedliftdeviceselectable()
    
def turndrag(a, turnrate):

  def rawturndrag(turnrate):
    lowspeedliftdevicelimit = a._aircraftdata.lowspeedliftdevicelimit()
    if lowspeedliftdevicelimit == None:
      return a._aircraftdata.turndrag(a._configuration, turnrate)
    elif a._lowspeedliftdeviceextended:
      return a._aircraftdata.turndrag(a._configuration, turnrate, lowspeedliftdevice=True)
    else:
      return a._aircraftdata.turndrag(a._configuration, turnrate)
  
  if turnrate == "EZ":
      return 0.0

  # See rule 6.6  
  if hasproperty(a, "PSSM") and a._speed >= apspeed.m1speed(a._altitudeband):
    # The aircraft has its maximum the turn rate reduced by one level, but not 
    # to less than HT.
    if turnrate == "ET":
      return None
    if turnrate == "BT" and rawturndrag("ET") == None:
      return None

  return rawturndrag(turnrate)

def minspeed(a):

  minspeed = a._aircraftdata.minspeed(a._configuration, a._altitudeband)

  if minspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      minspeed = a._aircraftdata.minspeed(a._configuration, altitudeband)
      if minspeed != None:
        break

  if apvariants.withvariant("use version 2.4 rules"):
    # See rule 7.6 in version 2.4.
    if lowspeedliftdeviceselectable(a) and a._lowspeedliftdeviceextended:
      minspeed -= 0.5

  return minspeed

def maxspeed(a):

  maxspeed = a._aircraftdata.maxspeed(a._configuration, a._altitudeband)

  if maxspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      maxspeed = a._aircraftdata.maxspeed(a._configuration, altitudeband)
      if maxspeed != None:
        break

  if hasproperty(a, "ABSF"):
    if a._powersetting != "AB":
      maxspeed -= a._aircraftdata._data["ABSFamount"]

  return maxspeed

def cruisespeed(a):
  return a._aircraftdata.cruisespeed(a._configuration)

def climbspeed(a):
  return a._aircraftdata.climbspeed()

def blindarcs(a):
  return a._aircraftdata.blindarcs()

def restrictedarcs(a):
  return a._aircraftdata.restrictedarcs()

def visibility(a):
  return a._aircraftdata.visibility()

def maxdivespeed(a):
  raw = a._aircraftdata.maxdivespeed(a._altitudeband)
  if raw != None:
    return raw
  # The aircraft is temporarily above its ceiling, so take the speed from the
  # highest band in the table.
  for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
    raw = a._aircraftdata.maxdivespeed(altitudeband)
    if raw != None:
      return raw

def ceiling(a):
  return a._aircraftdata.ceiling(a._configuration)

def rollhfp(a):
  # See rule 7.4.
  fp = a._aircraftdata.rollhfp()
  if hasproperty(a, "LRR"):
    fp += 1
  return fp

def rolldrag(a, rolltype):
  return a._aircraftdata.rolldrag(rolltype)

def climbcapability(a):
  climbcapability = a._aircraftdata.climbcapability(a._configuration, a._altitudeband, a._powersetting)
  if climbcapability == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      climbcapability = a._aircraftdata.climbcapability(a._configuration, altitudeband, a._powersetting)
      if climbcapability != None:
        break
  # See the Aircraft Damage Effects Table in the charts.
  if a.damageatleast("H"):
    climbcapability *= 0.5
  # See rule 6.6 and rule 8.1.4.
  if a._speed >= apspeed.m1speed(a._altitudeband):
    climbcapability *= 2/3
  return climbcapability

def hasproperty(a, p):

  # See "Aircraft Damage Effects" in the Play Aids.
  if p == "HPR" and a.damageatleast("L"):
    return False
  if p == "HRR" and a.damageatleast("L"):
    return False
  if p == "LRR" and a.damageatleast("L"):
    return True
  if p == "NRM" and a.damageatleast("H"):
    return True

  if a._aircraftdata.hasproperty(p):
    return True

  if p == "HRR" and a._aircraftdata.hasproperty("HRRCL"):
    return a._configuration == "CL"
  if p == "LRR" and a._aircraftdata.hasproperty("LRRHS"):
    return a._speed >= a._aircraftdata["LRRHSlimit"]

  return False

def specialclimbcapability(a):
  return a._aircraftdata.specialclimbcapability()

def gunarc(a):
  return a._aircraftdata.gunarc()
