import apxo.altitude as apaltitude
import apxo.speed    as apspeed
import apxo.variants as apvariants

def power(self, powersetting):
  return self._aircraftdata.power(self._configuration, powersetting)

def spbr(self):
  return self._aircraftdata.spbr(self._configuration)

def fuelrate(self):
  return self._aircraftdata.fuelrate(self._powersetting)

def engines(self):
  return self._aircraftdata.engines()

def powerfade(self):
  return self._aircraftdata.powerfade(self._speed, self._altitude)

def lowspeedliftdevicename(self):
    return self._aircraftdata.lowspeedliftdevicename()

def lowspeedliftdevicelimit(self):
    return self._aircraftdata.lowspeedliftdevicelimit()
    
def lowspeedliftdeviceselectable(self):
    return self._aircraftdata.lowspeedliftdeviceselectable()
    
def turndrag(self, turnrate):

  def rawturndrag(turnrate):
    lowspeedliftdevicelimit = self._aircraftdata.lowspeedliftdevicelimit()
    if lowspeedliftdevicelimit == None:
      return self._aircraftdata.turndrag(self._configuration, turnrate)
    elif self._lowspeedliftdeviceextended:
      return self._aircraftdata.turndrag(self._configuration, turnrate, lowspeedliftdevice=True)
    else:
      return self._aircraftdata.turndrag(self._configuration, turnrate)
  
  if turnrate == "EZ":
      return 0.0

  # See rule 6.6  
  if self.hasproperty("PSSM") and self._speed >= apspeed.m1speed(self._altitudeband):
    # The aircraft has its maximum the turn rate reduced by one level, but not 
    # to less than HT.
    if turnrate == "ET":
      return None
    if turnrate == "BT" and rawturndrag("ET") == None:
      return None

  return rawturndrag(turnrate)

def minspeed(self):

  minspeed = self._aircraftdata.minspeed(self._configuration, self._altitudeband)

  if minspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      minspeed = self._aircraftdata.minspeed(self._configuration, altitudeband)
      if minspeed != None:
        break

  if apvariants.withvariant("use version 2.4 rules"):
    # See rule 7.6 in version 2.4.
    if self.lowspeedliftdeviceselectable() and self._lowspeedliftdeviceextended:
      minspeed -= 0.5

  return minspeed

def maxspeed(self):

  maxspeed = self._aircraftdata.maxspeed(self._configuration, self._altitudeband)

  if maxspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      maxspeed = self._aircraftdata.maxspeed(self._configuration, altitudeband)
      if maxspeed != None:
        break

  if self._aircraftdata.hasproperty("ABSF"):
    if self._powersetting != "AB":
      maxspeed -= self._aircraftdata._data["ABSFamount"]

  return maxspeed

def cruisespeed(self):
  return self._aircraftdata.cruisespeed(self._configuration)

def climbspeed(self):
  return self._aircraftdata.climbspeed()

def blindarcs(self):
  return self._aircraftdata.blindarcs()

def restrictedarcs(self):
  return self._aircraftdata.restrictedarcs()

def visibility(self):
  return self._aircraftdata.visibility()

def maxdivespeed(self):
  raw = self._aircraftdata.maxdivespeed(self._altitudeband)
  if raw != None:
    return raw
  # The aircraft is temporarily above its ceiling, so take the speed from the
  # highest band in the table.
  for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
    raw = self._aircraftdata.maxdivespeed(altitudeband)
    if raw != None:
      return raw

def ceiling(self):
  return self._aircraftdata.ceiling(self._configuration)

def rollhfp(self):
  # See rule 7.4.
  fp = self._aircraftdata.rollhfp()
  if self.hasproperty("LRR"):
    fp += 1
  return fp

def rolldrag(self, rolltype):
  return self._aircraftdata.rolldrag(rolltype)

def climbcapability(self):
  climbcapability = self._aircraftdata.climbcapability(self._configuration, self._altitudeband, self._powersetting)
  if climbcapability == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      climbcapability = self._aircraftdata.climbcapability(self._configuration, altitudeband, self._powersetting)
      if climbcapability != None:
        break
  # See the Aircraft Damage Effects Table in the charts.
  if self.damageatleast("H"):
    climbcapability *= 0.5
  # See rule 6.6 and rule 8.1.4.
  if self._speed >= apspeed.m1speed(self._altitudeband):
    climbcapability *= 2/3
  return climbcapability

def hasproperty(self, p):

  # See "Aircraft Damage Effects" in the Play Aids.
  if p == "HPR" and self.damageatleast("L"):
    return False
  if p == "HRR" and self.damageatleast("L"):
    return False
  if p == "LRR" and self.damageatleast("L"):
    return True
  if p == "NRM" and self.damageatleast("H"):
    return True

  if self._aircraftdata.hasproperty(p):
    return True

  if p == "HRR" and self._aircraftdata.hasproperty("HRRCL"):
    return self._configuration == "CL"
  if p == "LRR" and self._aircraftdata.hasproperty("LRRHS"):
    return self._speed >= self._aircraftdata["LRRHSlimit"]

  return False

def specialclimbcapability(self):
  return self._aircraftdata.specialclimbcapability()

def gunarc(self):
  return self._aircraftdata.gunarc()

def blindarcs(self):
  return self._aircraftdata.blindarcs()
