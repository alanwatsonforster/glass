import apxo.speed    as apspeed
import apxo.altitude as apaltitude

def power(self, powersetting):
  return self._aircraftdata.power(self.configuration, powersetting)

def spbr(self):
  return self._aircraftdata.spbr(self.configuration)

def fuelrate(self):
  return self._aircraftdata.fuelrate(self._powersetting)

def engines(self):
  return self._aircraftdata.engines()

def powerfade(self):
  return self._aircraftdata.powerfade(self._speed, self._altitude)

def turndrag(self, turnrate):

  def rawturndrag(turnrate):
    lowspeedturnlimit = self._aircraftdata.lowspeedturnlimit()
    if lowspeedturnlimit == None:
      return self._aircraftdata.turndrag(self.configuration, turnrate)
    elif self._speed <= lowspeedturnlimit:
      return self._aircraftdata.turndrag(self.configuration, turnrate, lowspeed=True)
    else:
      return self._aircraftdata.turndrag(self.configuration, turnrate, highspeed=True)
  
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

  lowspeedturnlimit = self._aircraftdata.lowspeedturnlimit()
  if lowspeedturnlimit == None:
    return self._aircraftdata.turndrag(self.configuration, turnrate)
  elif self._speed <= lowspeedturnlimit:
    return self._aircraftdata.turndrag(self.configuration, turnrate, lowspeed=True)
  else:
    return self._aircraftdata.turndrag(self.configuration, turnrate, highspeed=True)

def minspeed(self):
  minspeed = self._aircraftdata.minspeed(self.configuration, self._altitudeband)
  if minspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      minspeed = self._aircraftdata.minspeed(self.configuration, altitudeband)
      if minspeed != None:
        break
  return minspeed

def maxspeed(self):

  maxspeed = self._aircraftdata.maxspeed(self.configuration, self._altitudeband)

  if maxspeed == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      maxspeed = self._aircraftdata.maxspeed(self.configuration, altitudeband)
      if maxspeed != None:
        break

  if self._aircraftdata.hasproperty("ABSF"):
    if self._powersetting != "AB":
      maxspeed -= self._aircraftdata._data["ABSFamount"]

  return maxspeed

def cruisespeed(self):
  return self._aircraftdata.cruisespeed()

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
  return self._aircraftdata.ceiling(self.configuration)

def rollhfp(self):
  # See rule 7.4.
  fp = self._aircraftdata.rollhfp()
  if self.hasproperty("LRR"):
    fp += 1
  return fp

def rolldrag(self, rolltype):
  return self._aircraftdata.rolldrag(rolltype)

def climbcapability(self):
  climbcapability = self._aircraftdata.climbcapability(self.configuration, self._altitudeband, self._powersetting)
  if climbcapability == None:
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
      climbcapability = self._aircraftdata.climbcapability(self.configuration, altitudeband, self._powersetting)
      if climbcapability != None:
        break
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
    return self.configuration == "CL"
  if p == "LRR" and self._aircraftdata.hasproperty("LRRHS"):
    return self._speed >= self._aircraftdata["LRRHSlimit"]

  return False

def specialclimbcapability(self):
  return self._aircraftdata.specialclimbcapability()

def gunarc(self):
  return self._aircraftdata.gunarc()

def blindarcs(self):
  return self._aircraftdata.blindarcs()
