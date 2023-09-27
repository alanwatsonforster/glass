import math

import airpower.speed as apspeed

from ._normalflight import _isclimbing, _isdiving

def _startmovespeed(self, power, flamedoutfraction):

    """
    Carry out the rules to do with power, speed, and speed-induced drag at the 
    start of a move.
    """

    ############################################################################

    lastpowersetting = self._lastpowersetting
    speed            = self._speed

    ############################################################################

    # Determine the requested power setting and power AP

    powerapM  = self._aircrafttype.power(self._configuration, "M")
    powerapAB = self._aircrafttype.power(self._configuration, "AB")

    # See rule 6.1.

    if power == "I":
      powersetting = "I"
      powerap      = 0
    elif power == "N" or power == 0:
      powersetting = "N"
      powerap      = 0
    elif power == "M":
      powersetting = "M"
      powerap      = powerapM
    elif power == "AB" and powerapAB == None:
      raise ValueError("aircraft does not have AB.")
    elif power == "AB":
      powersetting = "AB"
      powerap      = powerapAB
    elif not isinstance(power, (int, float)) or power < 0 or power % 0.25 != 0:
      raise ValueError("invalid power %r" % power)
    elif power <= powerapM:
      powersetting = "M"
      powerap      = power
    elif powerapAB != None and power <= powerapAB:
      powersetting = "AB"
      powerap      = power
    else:
      raise ValueError("requested power of %s APs exceeds aircraft capability." % power)

    self._log("power setting is %s." % powersetting)

    # See the "Effects of Flame-Out" section of rule 6.7

    if flamedoutfraction == 1:

      self._log("- power setting is treated as idle as all engines are flamed-out.")
      powersetting = "I"
      powerap = 0

    elif flamedoutfraction > 0.5:

      self._log("- power is reduced by one third as more than half of engines are flamed-out.")
      # 1/3 of APs, quantized in 1/4 units, rounding down.
      powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

      self._log("- power is reduced by one half as less than half of engines are flamed-out.")
      # 1/2 of APs, quantized in 1/4 units, rounding up.
      powerap = math.ceil(powerap / 2 * 4) / 4

    ############################################################################

    # Warn of the risk of flame-outs.

    # See the "When Does a Jet Flame-Out?" section of rule 6.7 
    # See the "Rapid Power Response" section of rule 6.1.

    if lastpowersetting == "I" and powersetting == "AB" and not self._aircrafttype.hasproperty("RPR"):
      self._log("- risk of flame-out as power setting has increased from I to AB.")

    if powersetting != "I" and self._altitude > self._aircrafttype.ceiling(self._configuration):
      self._log("- risk of flame-out as aircraft is above its ceiling and power setting is %s." % powersetting)

    if self._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
      self._log("- risk of flame-out as aircaft is in departed flight and power setting is %s." % powersetting)

    ############################################################################

    # Determine the speed.
        
    m1speed = apspeed.m1speed(self._altitudeband)
    htspeed = apspeed.htspeed(self._altitudeband)
    ltspeed = apspeed.ltspeed(self._altitudeband)

    if self._speed < ltspeed:
      self._log("speed is %.1f" % speed)
    elif self._speed == ltspeed:
      self._log("speed is %.1f (LT)" % speed)
    elif self._speed == htspeed:
      self._log("speed is %.1f (HT)" % speed)
    else:
      self._log("speed is %.1f (SS)" % speed)

    # See the "Idle" section of rule 6.1 and the "Supersonic Speeds" section of rule 6.6

    if powersetting == "I":
      speedchange = self._aircrafttype.power(self._configuration, "I")
      if self._speed >= m1speed:
        speedchange += 0.5
      # This keeps the speed non-negative. See rule 6.2.
      speedchange = min(speedchange, self._speed)
      speed -= speedchange
      self._log("- reducing speed to %.1f as the power setting is I." % speed)

    ############################################################################

    # Determine the speed-induced drag.

    # There is some ambiguity in the rules as to whether these effects depend 
    # on the speed before or after the reduction for idle power. Here we use it 
    # after the reduction.
    
    speedap = 0.0

    # See the "Decel Point Penalty for Insufficient Power" section of rule 6.1.

    if speed > self._aircrafttype.cruisespeed():
      if powersetting == "I" or powersetting == "N":
        self._log("- insufficient power above cruise speed.")
        speedap -= 1.0

    # See the "Supersonic Speeds" section of rule 6.6
    
    if speed >= m1speed:
      if powersetting == "I" or powersetting == "N":
        speedap -= 2.0 * (speed - htspeed) / 0.5
        self._log("- insufficient power at supersonic speed.")
      elif powersetting == "M":
        speedap -= 1.5 * (speed - htspeed) / 0.5
        self._log("- insufficient power at supersonic speed.")

    # See the "Transonic Speeds" section of rule 6.6

    if ltspeed <= speed and speed <= m1speed:
      self._log("- transonic drag.")
      if speed == ltspeed:
        speedap -= 0.5
      elif speed == htspeed:
        speedap -= 1.0
      elif speed == m1speed:
        speedap -= 1.5
      if self._aircrafttype.hasproperty("LTD"):
        speedap += 0.5
      elif self._aircrafttype.hasproperty("HTD"):
        speedap -= 0.5

    ############################################################################

    return speed, powersetting, powerap, speedap

################################################################################

def _endmovespeed(self):

  """
  Carry out the rules to do with speed, power, and drag at the end of a move.
  """

  # See rule 6.2.

  self._log("- power          APs = %+.2f." % self._powerap)
  self._log("- speed          APs = %+.2f." % self._speedap)
  self._log("- altitude       APs = %+.2f." % self._altitudeap)
  self._log("- turn rate      APs = %+.2f and %+.2f." % (self._turnrateap, self._sustainedturnap))
  self._log("- sustained turn APs = %+.2f and %+.2f." % (self._turnrateap, self._sustainedturnap))
  self._log("- speedbrakes    APs = %+.2f." % self._speedbrakesap)
  ap = self._turnrateap + self._sustainedturnap + self._altitudeap + self._speedbrakesap + self._powerap + self._speedap
  self._log("- total          APs = %+.2f with %+.2f carry = %+.2f." % (ap, self._apcarry, ap + self._apcarry))
  ap += self._apcarry

  # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
  # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

  if ap < 0:
    aprate = -2.0
  elif self._aircrafttype.hasproperty("RA"):
    if self._speed >= apspeed.m1speed(self._altitudeband):
      aprate = +2.0
    else:
      aprate = +1.5
  else:
    if self._speed >= apspeed.m1speed(self._altitudeband):
      aprate = +3.0
    else:
      aprate = +2.0

  # See rule 6.2 and 6.3

  if ap < 0:

    assert self._flighttype != "DP"

    self._speed -= 0.5 * (ap // aprate)
    self._apcarry = ap % aprate

    # See the "Maximum Deceleration" section of rule 6.2.

    if self._speed <= 0:
      self._speed = 0
      if self._apcarry < 0:
        self._apcarry = 0        

  elif ap > 0:

    assert self._flighttype != "DP"

    # See rule 6.2 and the "Acceleration limits" section of rule 6.3.

    if self._flighttype == "LVL" or _isclimbing(self._flighttype):
      maxspeed = self._aircrafttype.maxspeed(self._configuration, self._altitudeband)
      maxspeedname = "maximum speed"
    elif _isdiving(self._flighttype) or self._flighttype == "ST":
      maxspeed = self._aircrafttype.maxdivespeed(self._altitudeband)
      maxspeedname = "maximum dive speed"

    if self._speed >= maxspeed and ap >= aprate:
      self._log("- acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
      self._apcarry = aprate - 0.5
    elif self._speed >= maxspeed:
      self._apcarry = ap
    elif self._speed + 0.5 * (ap // aprate) > maxspeed:
      self._log("- acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
      self._speed = maxspeed
      self._apcarry = aprate - 0.5
    else:
      self._speed += 0.5 * (ap // aprate)
      self._apcarry = ap % aprate

  # See rule 6.3.

  if self._flighttype == "LVL" or _isclimbing(self._flighttype):

    # See the "Speed Fadeback" section of rule 6.3.

    maxspeed = self._aircrafttype.maxspeed(self._configuration, self._altitudeband)
    if self._speed > maxspeed:
      self._log("- speed is faded back from %.1f." % self._speed)
      self._speed = max(self._speed - 1, maxspeed)

  elif _isdiving(self._flighttype) or self._flighttype == "ST" or self._flighttype == "DP":

    # See the "Diving Speed Limits" section of rule 6.3.

    maxspeed = self._aircrafttype.maxdivespeed(self._altitudeband)
    if self._speed > maxspeed:
      self._log("- speed is reduced to maximum dive speed of %.1f." % maxspeed)
      self._speed = maxspeed

  if self._lastspeed != self._speed:
    self._log("speed changed from %.1f to %.1f." % (self._lastspeed, self._speed))
  else:
    self._log("speed is unchanged at %.1f." % self._speed)

  if self._flighttype == "ST":
    if self._speed >= self._aircrafttype.minspeed(self._configuration, self._altitudeband):
      self._log("- aircraft has exited from stall.")
    else:
      self._log("- aircraft is still stalled.")
