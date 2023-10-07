import math

import airpower.speed as apspeed
from airpower.math import onethird, twothirds

from ._normalflight import _isclimbing, _isdiving

def _startmovespeed(self, power, flamedoutfraction):

    """
    Carry out the rules to do with power, speed, and speed-induced drag at the 
    start of a move.
    """

    ############################################################################

    lastpowersetting = self._lastpowersetting
    speed  = self._speed

    ############################################################################

    # Determine the requested power setting and power AP

    powerapM  = self.power("M")
    powerapAB = self.power("AB")

    # See rule 8.4.

    if not self.hasproperty("HAE"):
      if self._altitudeband == "VH":
        powerapM  = max(0.5, twothirds(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, twothirds(powerapAB))
      elif self._altitudeband == "EH" or self._altitudeband == "UH":
        powerapM  = max(0.5, onethird(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, onethird(powerapAB))        

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
      raise RuntimeError("aircraft does not have AB.")
    elif power == "AB":
      powersetting = "AB"
      powerap      = powerapAB
    elif not isinstance(power, (int, float)) or power < 0 or power % 0.25 != 0:
      raise RuntimeError("invalid power %r" % power)
    elif power <= powerapM:
      powersetting = "M"
      powerap      = power
    elif powerapAB != None and power <= powerapAB:
      powersetting = "AB"
      powerap      = power
    else:
      raise RuntimeError("requested power of %s APs exceeds aircraft capability." % power)

    self._log("power setting is %s." % powersetting)

    # See rule 8.4. The reduction was done above, but we report it here.
    if not self.hasproperty("HAE") and (
      self._altitudeband == "VH" or self._altitudeband == "EH" or self._altitudeband == "UH"
    ):
      self._log("- power is reduced in the %s altitude band." % self._altitudeband)
        
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

    # See the "Rapid Power Response" section of rule 6.1 and the "When Does a 
    # Jet Flame-Out?" section of rule 6.7

    if lastpowersetting == "I" and powersetting == "AB" and not self.hasproperty("RPR"):
      self._log("- risk of flame-out as power setting has increased from I to AB.")

    if powersetting != "I" and self._altitude > self.ceiling():
      self._log("- risk of flame-out as aircraft is above its ceiling and power setting is %s." % powersetting)

    if self._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
      self._log("- risk of flame-out as aircaft is in departed flight and power setting is %s." % powersetting)

    ############################################################################

    # Determine the speed.
    
    m1speed = apspeed.m1speed(self._altitudeband)
    htspeed = apspeed.htspeed(self._altitudeband)
    ltspeed = apspeed.ltspeed(self._altitudeband)
    minspeed = self.minspeed()

    if speed < ltspeed:
      self._log("speed is %.1f." % speed)
    elif speed == ltspeed:
      self._log("speed is %.1f (LT)." % speed)
    elif speed == htspeed:
      self._log("speed is %.1f (HT)." % speed)
    else:
      self._log("speed is %.1f (SS)." % speed)

    # See rule 6.4 on recovery from departed flight.

    if self._lastflighttype == "DP" and self._flighttype != "DP" and speed < minspeed:
      speed = minspeed
      self._log("- increasing speed to %.1f after recovering from departed flight." % minspeed)
      
    # See rules 6.1 and 6.6 on idle power setting.

    if powersetting == "I":
      speedchange = self.power("I")
      if self._speed >= m1speed:
        speedchange += 0.5
      # This keeps the speed non-negative. See rule 6.2.
      speedchange = min(speedchange, self._speed)
      speed -= speedchange
      self._log("- reducing speed to %.1f as the power setting is I." % speed)

    # See rule 6.3 on entering a stall.
      
    if speed < minspeed:
      self._log("- speed is below the minimum of %.1f." % minspeed)
      self._log("- aircraft is stalled.")
      if self._flighttype != "ST" and self._flighttype != "DP":
        raise RuntimeError("flight type must be ST or DP.")
    
    ############################################################################

    # Determine the speed-induced drag.

    # There is some ambiguity in the rules as to whether these effects depend 
    # on the speed before or after the reduction for idle power. Here we use it 
    # after the reduction.
  
    speedap = 0.0

    # See the "Decel Point Penalty for Insufficient Power" section of rule 6.1.

    if speed > self.cruisespeed():
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
      if self.hasproperty("LTD"):
        speedap += 0.5
      elif self.hasproperty("HTD"):
        speedap -= 0.5

    ############################################################################

    return speed, powersetting, powerap, speedap

################################################################################

def _endmovespeed(self):

  """
  Carry out the rules to do with speed, power, and drag at the end of a move.
  """

  # See the "Departed Flight Procedure" section of rule 6.4

  if self._flighttype == "DP":
    self.apcarry = 0
    self._log("speed is unchanged at %.1f." % self._speed)
    return

  # See the "Speed Gain" and "Speed Loss" sections of rule 6.2.

  self._log("- power          APs = %+.2f." % self._powerap)
  self._log("- speed          APs = %+.2f." % self._speedap)
  self._log("- altitude       APs = %+.2f." % self._altitudeap)
  self._log("- turn rate      APs = %+.2f." % self._turnrateap)
  self._log("- sustained turn APs = %+.2f." % self._sustainedturnap)
  self._log("- maneuver       APs = %+.2f." % self._maneuverap)
  self._log("- speedbrakes    APs = %+.2f." % self._spbrap)
  self._log("- carry          APs = %+.2f." % self._apcarry)
  ap = \
    self._powerap + \
    self._speedap + \
    self._altitudeap + \
    self._turnrateap + \
    self._sustainedturnap + \
    self._maneuverap + \
    self._spbrap + \
    self._apcarry
  self._log("- total          APs = %+.2f." % ap)

  # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
  # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

  if ap < 0:
    aprate = -2.0
  elif self.hasproperty("RA"):
    if self._speed >= apspeed.m1speed(self._altitudeband):
      aprate = +2.0
    else:
      aprate = +1.5
  else:
    if self._speed >= apspeed.m1speed(self._altitudeband):
      aprate = +3.0
    else:
      aprate = +2.0

  # The speed is limited to the maximum dive speed if the aircraft dived at least
  # two levels. See rules 6.3 and 8.2.

  altitudeloss = self._lastaltitude - self._altitude
  usemaxdivespeed = (altitudeloss >= 2)
  
  if ap == 0:

    self._apcarry = 0

  elif ap < 0:

    # See the "Speed Loss" and "Maximum Deceleration" sections of rule 6.2.

    self._speed -= 0.5 * (ap // aprate)
    self._apcarry = ap % aprate

    if self._speed <= 0:
      self._speed = 0
      if self._apcarry < 0:
        self._apcarry = 0        

  elif ap > 0:

    # See rules 6.2, 6.3, and 8.2.

    if usemaxdivespeed:
      maxspeed = self.maxdivespeed()
      maxspeedname = "maximum dive speed"
    else:
      maxspeed = self.maxspeed()
      maxspeedname = "maximum speed"

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

  if usemaxdivespeed:
    maxspeed = self.maxdivespeed()
    if self._speed > maxspeed:
      self._log("- speed is reduced to maximum dive speed of %.1f." % maxspeed)
      self._speed = maxspeed
  else:
    maxspeed = self.maxspeed()
    if self._speed > maxspeed:
      self._log("- speed is faded back from %.1f." % self._speed)
      self._speed = max(self._speed - 1, maxspeed)

  if self._lastspeed != self._speed:
    self._log("speed changed from %.1f to %.1f." % (self._lastspeed, self._speed))
  else:
    self._log("speed is unchanged at %.1f." % self._speed)

  # See rule 6.4.

  minspeed = self.minspeed()
  if self._speed < minspeed:
    self._log("- speed is below the minimum of %.1f." % minspeed)
  if self._speed >= minspeed and self._flighttype == "ST":
    self._log("- aircraft is no longer stalled.")
  elif self._speed < minspeed and self._flighttype == "ST":
    self._log("- aircraft is still stalled.")
  elif self._speed < minspeed:
    self._log("- aircraft has stalled.")

