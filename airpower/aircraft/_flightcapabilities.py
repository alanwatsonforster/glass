import airpower.speed    as apspeed
import airpower.altitude as apaltitude

def power(self, powersetting):
  return self._aircraftdata.power(self._configuration, powersetting)

def spbr(self):
  return self._aircraftdata.spbr(self._configuration)

def fuelrate(self):
  return self._aircraftdata.fuelrate(self._powersetting)

def turnrates(self):
  return self._aircraftdata.turnrates(self._configuration)

def turndrag(self, turnrate):
  return self._aircraftdata.turndrag(self._configuration, turnrate)

def minspeed(self):
  return self._aircraftdata.minspeed(self._configuration, self._altitudeband)

def maxspeed(self):
  return self._aircraftdata.maxspeed(self._configuration, self._altitudeband)

def cruisespeed(self):
  return self._aircraftdata.cruisespeed()

def climbspeed(self):
  return self._aircraftdata.climbspeed()

def maxdivespeed(self):
  return self._aircraftdata.maxdivespeed(self._altitudeband)

def ceiling(self):
  return self._aircraftdata.ceiling(self._configuration)

def rollhfp(self):
  return self._aircraftdata.rollhfp()

def rolldrag(self, rolltype):
  return self._aircraftdata.rolldrag(rolltype)

def climbcapability(self):
  climbcapability = self._aircraftdata.climbcapability(self._configuration, self._altitudeband, self._powersetting)
  # See rule 6.6 and rule 8.1.4.
  if self._speed >= apspeed.m1speed(self._altitudeband):
    climbcapability = apaltitude.roundaltitudefraction(climbcapability * 2/3)
  return climbcapability

def hasproperty(self, p):
  return self._aircraftdata.hasproperty(p)
