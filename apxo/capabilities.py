import apxo.altitude as apaltitude
import apxo.speed    as apspeed
import apxo.variants as apvariants

def power(A, powersetting):
  return A._aircraftdata.power(A._configuration, powersetting)

def spbr(A):
  return A._aircraftdata.spbr(A._configuration)

def fuelrate(A):
  return A._aircraftdata.fuelrate(A._powersetting)

def engines(A):
  return A._aircraftdata.engines()

def powerfade(A):
  return A._aircraftdata.powerfade(A._speed, A._altitude)

def lowspeedliftdevicename(A):
    return A._aircraftdata.lowspeedliftdevicename()

def lowspeedliftdevicelimit(A):
    return A._aircraftdata.lowspeedliftdevicelimit()
    
def lowspeedliftdeviceselectable(A):
    return A._aircraftdata.lowspeedliftdeviceselectable()
    
def turndrag(A, turnrate):

  def rawturndrag(turnrate):
    lowspeedliftdevicelimit = A._aircraftdata.lowspeedliftdevicelimit()
    if lowspeedliftdevicelimit == None:
      return A._aircraftdata.turndrag(A._configuration, turnrate)
    elif A._lowspeedliftdeviceextended:
      return A._aircraftdata.turndrag(A._configuration, turnrate, lowspeedliftdevice=True)
    else:
      return A._aircraftdata.turndrag(A._configuration, turnrate)
  
  if turnrate == "EZ":
      return 0.0

  # See rule 6.6  
  if hasproperty(A, "PSSM") and A._speed >= apspeed.m1speed(A._altitudeband):
    # The aircraft has its maximum the turn rate reduced by one level, but not 
    # to less than HT.
    if turnrate == "ET":
      return None
    if turnrate == "BT" and rawturndrag("ET") == None:
      return None

  return rawturndrag(turnrate)

def minspeed(A):

  minspeed = A._aircraftdata.minspeed(A._configuration, A._altitudeband)

  if minspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      minspeed = A._aircraftdata.minspeed(A._configuration, altitudeband)
      if minspeed != None:
        break

  if apvariants.withvariant("use version 2.4 rules"):
    # See rule 7.6 in version 2.4.
    if lowspeedliftdeviceselectable(A) and A._lowspeedliftdeviceextended:
      minspeed -= 0.5

  return minspeed

def maxspeed(A):

  maxspeed = A._aircraftdata.maxspeed(A._configuration, A._altitudeband)

  if maxspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      maxspeed = A._aircraftdata.maxspeed(A._configuration, altitudeband)
      if maxspeed != None:
        break

  if hasproperty(A, "ABSF"):
    if A._powersetting != "AB":
      maxspeed -= A._aircraftdata._data["ABSFamount"]

  return maxspeed

def cruisespeed(A):
  return A._aircraftdata.cruisespeed(A._configuration)

def climbspeed(A):
  return A._aircraftdata.climbspeed()

def blindarcs(A):
  return A._aircraftdata.blindarcs()

def restrictedarcs(A):
  return A._aircraftdata.restrictedarcs()

def visibility(A):
  return A._aircraftdata.visibility()

def sizemodifier(A):
  return A._aircraftdata.sizemodifier()

def maxdivespeed(A):
  raw = A._aircraftdata.maxdivespeed(A._altitudeband)
  if raw != None:
    return raw
  # The aircraft is temporarily above its ceiling, so take the speed from the
  # highest band in the table.
  for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
    raw = A._aircraftdata.maxdivespeed(altitudeband)
    if raw != None:
      return raw

def ceiling(A):
  return A._aircraftdata.ceiling(A._configuration)

def rollhfp(A):
  # See rule 7.4.
  fp = A._aircraftdata.rollhfp()
  if hasproperty(A, "LRR"):
    fp += 1
  return fp

def rolldrag(A, rolltype):
  return A._aircraftdata.rolldrag(rolltype)

def climbcapability(A):
  climbcapability = A._aircraftdata.climbcapability(A._configuration, A._altitudeband, A._powersetting)
  if climbcapability == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      climbcapability = A._aircraftdata.climbcapability(A._configuration, altitudeband, A._powersetting)
      if climbcapability != None:
        break
  # See the Aircraft Damage Effects Table in the charts.
  if A.damageatleast("H"):
    climbcapability *= 0.5
  # See rule 6.6 and rule 8.1.4.
  if A._speed >= apspeed.m1speed(A._altitudeband):
    climbcapability *= 2/3
  return climbcapability

def hasproperty(A, p):

  # See "Aircraft Damage Effects" in the Play Aids.
  if p == "HPR" and A.damageatleast("L"):
    return False
  if p == "HRR" and A.damageatleast("L"):
    return False
  if p == "LRR" and A.damageatleast("L"):
    return True
  if p == "NRM" and A.damageatleast("H"):
    return True

  if A._aircraftdata.hasproperty(p):
    return True

  if p == "HRR" and A._aircraftdata.hasproperty("HRRCL"):
    return A._configuration == "CL"
  if p == "LRR" and A._aircraftdata.hasproperty("LRRHS"):
    return A._speed >= A._aircraftdata["LRRHSlimit"]

  return False

def specialclimbcapability(A):
  return A._aircraftdata.specialclimbcapability()

def gunarc(A):
  return A._aircraftdata.gunarc()

def gunsightmodifier(A, turnrate):
  return A._aircraftdata.gunsightmodifier(turnrate)
