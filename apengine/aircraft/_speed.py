import math

import apengine.speed as apspeed
import apengine.variants as apvariants
from apengine.math import onethird, twothirds

from ._normalflight import _isclimbing, _isdiving

def _startmovespeed(self, power, flamedoutengines):

    """
    Carry out the rules to do with power, speed, and speed-induced drag at the 
    start of a move.
    """

    m1speed = apspeed.m1speed(self._altitudeband)
    htspeed = apspeed.htspeed(self._altitudeband)
    ltspeed = apspeed.ltspeed(self._altitudeband)
    
    def reportspeed():
      if speed < ltspeed:
        self._log("speed         is %.1f." % speed)
      elif speed == ltspeed:
        self._log("speed         is %.1f (LT)." % speed)
      elif speed == htspeed:
        self._log("speed         is %.1f (HT)." % speed)
      else:
        self._log("speed         is %.1f (SS)." % speed)      

    ############################################################################

    # For aircraft with SP flight type, the power is interpreted as the
    # speed and we skip the rest.

    if self._flighttype == "SP":
      speed = power
      reportspeed()
      self._speed        = speed
      self._powersetting = ""
      self._powerap      = 0
      self._speedap      = 0
      return

    ############################################################################

    lastpowersetting = self._previouspowersetting
    speed            = self._speed

    ############################################################################

    # Determine the requested power setting and power AP.

    # Propeller-driver aircraft have ADCs that give "full throttle" and
    # "half-throttle" power ratings, in addition to "normal". These are
    # not mentioned in the AP rules, despite appearing on the ADC for
    # the propeller-driven Skyraider which is included with TSOH.
    # However, we treat them both as the equivalent of M power, except
    # for fuel use. We refer to them as "FT" and "HT". This extension
    # can be disallowed by setting the "disallow HT/FT" variant.

    # One unclear issue is whether an aircraft above its cruise speed
    # needs to use FT to avoid a drag penalty or if HT is sufficient. In
    # the absence of guidance and following the precedence that AB is
    # not required for jet-powered aircraft, I have implemented that HT
    # is sufficient.

    powerapM  = self.power("M")
    powerapAB = self.power("AB")
    if apvariants.withvariant("disallow HT/FT"):
      powerapHT = None
      powerapFT = None
    else:
      powerapHT = self.power("HT")
      powerapFT = self.power("FT")

    jet = (powerapM != None)

    # See rule 8.4.

    if self._altitudeband == "VH":
      if jet and not self.hasproperty("HAE"):
        powerapM  = max(0.5, twothirds(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, twothirds(powerapAB))
    elif (self._altitudeband == "EH" or self._altitudeband == "UH"):
      if jet and not self.hasproperty("HAE"):
        powerapM  = max(0.5, onethird(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, onethird(powerapAB))     

    # Some propeller aircraft lose power at high speed.
    if self.powerfade() != None:
      powerapHT = max(0.0, powerapHT - self.powerfade())
      powerapFT = max(0.0, powerapFT - self.powerfade())

    # See rule 6.1.

    if power == "I":
      powersetting = "I"
      powerap      = 0
    elif power == "N" or power == 0:
      powersetting = "N"
      powerap      = 0
    elif power == "M" and powerapM == None:
      raise RuntimeError("aircraft does not have an M power setting.")
    elif power == "M":
      powersetting = "M"
      powerap      = powerapM
    elif power == "AB" and powerapAB == None:
      raise RuntimeError("aircraft does not have an AB power setting.")
    elif power == "AB":
      powersetting = "AB"
      powerap      = powerapAB
    elif power == "HT" and powerapHT == None:
      raise RuntimeError("aircraft does not have an HT power setting.")
    elif power == "HT":
      powersetting = "HT"
      powerap      = powerapHT
    elif power == "FT" and powerapFT == None:
      raise RuntimeError("aircraft does not have an FT power setting.")
    elif power == "FT":
      powersetting = "FT"
      powerap      = powerapFT
    elif not isinstance(power, (int, float)) or power < 0 or power % 0.25 != 0:
      raise RuntimeError("invalid power %r" % power)
    elif powerapM != None and power <= powerapM:
      powersetting = "M"
      powerap      = power
    elif powerapAB != None and power <= powerapAB:
      powersetting = "AB"
      powerap      = power
    elif powerapHT != None and power <= powerapHT:
      powersetting = "HT"
      powerap      = power
    elif powerapFT != None and power <= powerapFT:
      powersetting = "FT"
      powerap      = power
    else:
      raise RuntimeError("requested power of %s APs exceeds aircraft capability." % power)

    self._log("power setting is %s." % powersetting)

    # See rule 8.4. The reduction was done above, but we report it here.
    if jet and not self.hasproperty("HAE") and (
      self._altitudeband == "VH" or self._altitudeband == "EH" or self._altitudeband == "UH"
    ):
      self._log("- power is reduced in the %s altitude band." % self._altitudeband)
        
    # Again, the reduction was done above, but we report it here.
    if self.powerfade() != None and self.powerfade() > 0.0:
      self._log("- power is reduced by %.2f as the speed is %.1f." % (self.powerfade(), speed))
    
    # See rule 6.7

    flamedoutfraction = flamedoutengines / self.engines()

    if flamedoutfraction == 1:

      if self.engines() == 1:
        self._log("- power setting is treated as idle as the engine is flamed-out.")
      else:
        self._log("- power setting is treated as idle as all %d engines are flamed-out." % self.engines())
      powersetting = "I"
      powerap = 0

    elif flamedoutfraction > 0.5:

      self._log("- power is reduced by one third as %d of the %d engines are flamed-out." % (
        flamedoutengines, self.engines()
      ))
      # 1/3 of APs, quantized in 1/4 units, rounding down.
      powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

      self._log("- power is reduced by one half as %d of the %d engines are flamed-out." % (
        flamedoutengines, self.engines()
      ))
      # 1/2 of APs, quantized in 1/4 units, rounding up.
      powerap = math.ceil(powerap / 2 * 4) / 4

    ############################################################################

    # Warn of the risk of flame-outs.

    # See rules 6.1, 6.7, and 8.5.

    if lastpowersetting == "I" and powersetting == "AB" and not self.hasproperty("RPR"):
      self._log("- check for flame-out as the power setting has increased from I to AB.")

    if powersetting != "I" and self._altitude > self.ceiling():
      self._log("- check for flame-out as the aircraft is above its ceiling and the power setting is %s." % powersetting)

    if self._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
      self._log("- check for flame-out as the aircaft is in departed flight and the power setting is %s." % powersetting)

    ############################################################################

    # Determine the speed.
    
    # See rule 6.4 on recovery from departed flight.

    if self._previousflighttype == "DP" and self._flighttype != "DP" and speed < minspeed:
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

    reportspeed()

    # See rule 6.3 on entering a stall.
      
    minspeed = self.minspeed()
    if speed < minspeed:
      self._log("- speed is below the minimum of %.1f." % minspeed)
      self._log("- aircraft is stalled.")
      if self._flighttype != "ST" and self._flighttype != "DP":
        raise RuntimeError("flight type must be ST or DP.")
    
    ############################################################################

    # Determine the speed-induced drag.

    # The rules implement speed-induced drag as reductions in the power
    # APs. We keep the power APs and speed-induced drag APs separate,
    # for clarity. The two approaches are equivalent.

    # There is some ambiguity in the rules as to whether these effects
    # depend on the speed before or after the reduction for idle power.
    # Here we use it after the reduction.
  
    speedap = 0.0

    # See rule 6.1.

    if speed > self.cruisespeed():
      if powersetting == "I" or powersetting == "N":
        self._log("- insufficient power above cruise speed.")
        speedap -= 1.0

    # See rule 6.6
    
    if speed >= m1speed:
      if powersetting == "I" or powersetting == "N":
        speedap -= 2.0 * (speed - htspeed) / 0.5
        self._log("- insufficient power at supersonic speed.")
      elif powersetting == "M":
        speedap -= 1.5 * (speed - htspeed) / 0.5
        self._log("- insufficient power at supersonic speed.")

    # See rule 6.6

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

    self._speed        = speed
    self._powersetting = powersetting
    self._powerap      = powerap
    self._speedap      = speedap

################################################################################

def _endmovespeed(self):

  """
  Carry out the rules to do with speed, power, and drag at the end of a move.
  """

    # For aircraft with SP flight type, we skip this.

  if self._flighttype == "SP":
    self.apcarry = 0
    self._log("speed is unchanged at %.1f." % self._speed)
    return

  # See the "Departed Flight Procedure" section of rule 6.4

  if self._flighttype == "DP" or self._maneuveringdeparture:
    self.apcarry = 0
    self._log("speed is unchanged at %.1f." % self._speed)
    return

  # See the "Speed Gain" and "Speed Loss" sections of rule 6.2.

  turnsap = self._turnrateap + self._sustainedturnap

  self._log("-- power           APs = %+.2f." % self._powerap)
  self._log("-- speed           APs = %+.2f." % self._speedap)
  self._log("-- altitude        APs = %+.2f." % self._altitudeap)
  self._log("-- turns           APs = %+.2f." % turnsap)
  self._log("-- other maneuvers APs = %+.2f." % self._othermaneuversap)
  self._log("-- speedbrakes     APs = %+.2f." % self._spbrap)
  self._log("-- carry           APs = %+.2f." % self._apcarry)
  ap = \
    self._powerap + \
    self._speedap + \
    self._altitudeap + \
    turnsap + \
    self._othermaneuversap + \
    self._spbrap + \
    self._apcarry
  self._log("-- total           APs = %+.2f." % ap)

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

  altitudeloss = self._previousaltitude - self._altitude
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

  self._log("- is carrying %+.2f APs." % self._apcarry)

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

  if self._previousspeed != self._speed:
    self._log("speed         changed from %.1f to %.1f." % (self._previousspeed, self._speed))
  else:
    self._log("speed         is unchanged at %.1f." % self._speed)

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
