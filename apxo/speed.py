import math

import apxo.variants as apvariants
from apxo.math import onethird, twothirds
from apxo.log import plural

################################################################################

def isvalidspeed(speed):

  """
  Return True if the argument is a valid speed.
  """
  
  return isinstance(speed, (int, float)) and speed >= 0

################################################################################

# See the "Transonic/Supersonic Speed Reference Table" chart and the "Speed of 
# Sound" and "Transonic Speeds" section of rule 6.6.

def m1speed(altitudeband):

  """
  Return the M1 speed in the specified altitude band.
  """

  if altitudeband == "LO" or altitudeband == "ML":
    return 7.5
  elif altitudeband == "MH" or altitudeband == "HI":
    return 7.0
  else:
    return 6.5

def htspeed(altitudeband):

  """
  Return the high-transonic speed in the specified altitude band.
  """

  return m1speed(altitudeband) - 0.5

def ltspeed(altitudeband):

  """
  Return the low-transonic speed in the specified altitude band.
  """

  return m1speed(altitudeband) - 1.0

################################################################################


from apxo.aircraft.normalflight import _isclimbingflight, _isdivingflight

def startmovespeed(a, power, flamedoutengines, lowspeedliftdeviceselected):

    """
    Carry out the rules to do with power, speed, and speed-induced drag at the 
    start of a move.
    """

    def reportspeed():
      if speed < ltspeed(a._altitudeband):
        a._logstart("speed         is %.1f." % speed)
      elif speed == ltspeed(a._altitudeband):
        a._logstart("speed         is %.1f (LT)." % speed)
      elif speed == htspeed(a._altitudeband):
        a._logstart("speed         is %.1f (HT)." % speed)
      else:
        a._logstart("speed         is %.1f (SS)." % speed)      

    ############################################################################

    # For aircraft with SP flight type, the power is interpreted as the
    # speed and we skip the rest.

    if a._flighttype == "SP":
      speed = power
      reportspeed()
      a._speed        = speed
      a._powersetting = ""
      a._powerap      = 0
      a._speedap      = 0
      return

    ############################################################################

    lastpowersetting = a._previouspowersetting
    speed            = a._speed

    ############################################################################

    # See rule 29.1.
    if not a._fuel is None:
      if a._fuel == 0:
        if a.engines() == 1:
          a._logevent("the engine is flamed-out from a lack of fuel.")
        else:
          a._logstart("all engines are flamed-out from a lack of fuel.")
        flamedoutengines = a.engines()
      
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

    powerapM  = a.power("M")
    powerapAB = a.power("AB")
    if apvariants.withvariant("disallow HT/FT"):
      powerapHT = None
      powerapFT = None
    else:
      powerapHT = a.power("HT")
      powerapFT = a.power("FT")

    jet = (powerapM != None)

    # See rule 8.4.

    if a._altitudeband == "VH":
      if jet and not a.hasproperty("HAE"):
        powerapM  = max(0.5, twothirds(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, twothirds(powerapAB))
    elif (a._altitudeband == "EH" or a._altitudeband == "UH"):
      if jet and not a.hasproperty("HAE"):
        powerapM  = max(0.5, onethird(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, onethird(powerapAB))     

    # Some propeller aircraft lose power at high speed.
    if a.powerfade() != None:
      powerapHT = max(0.0, powerapHT - a.powerfade())
      powerapFT = max(0.0, powerapFT - a.powerfade())

    # See "Aircraft Damage Effects" in the Play Aids.
    if a.damageatleast("H"):
      if jet:
        powerapM /= 2
        if powerapAB != None:
          powerapAB /= 2
      else:
        powerapHT /= 2
        powerapFT /= 2
    if a.damageatleast("C"):
      if jet:
        powerapAB = None
      else:
        powerapFT = None

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
      raise RuntimeError("requested power of %s exceeds aircraft capability." % (
        plural(power, "1 AP", "%s APs" % power)))

    a._logstart("power setting is %s." % powersetting)

    # See rule 8.4. The reduction was done above, but we report it here.
    if jet and not a.hasproperty("HAE") and (
      a._altitudeband == "VH" or a._altitudeband == "EH" or a._altitudeband == "UH"
    ):
      a._logevent("power is reduced in the %s altitude band." % a._altitudeband)
        
    # Again, the reduction was done above, but we report it here.
    if a.powerfade() != None and a.powerfade() > 0.0:
      a._logevent("power is reduced as the speed is %.1f." % speed)
    
    # Again, the reduction was done above, but we report it here.
    if a.damageatleast("H"):
      a._logevent("power is reduced as damage is %s." % a.damage())

    # Is the engine smoking?
    a._enginesmoking = (a.hasproperty("SMP") and powersetting == "M")
    if a._enginesmoking:
      a._logevent("engine is smoking.")

    # See rule 6.7

    flamedoutfraction = flamedoutengines / a.engines()

    if flamedoutfraction == 1:

      if a.engines() == 1:
        a._logevent("power setting is treated as I as the engine is flamed-out.")
      else:
        a._logevent("power setting is treated as I as all %d engines are flamed-out." % a.engines())
      powersetting = "I"
      powerap = 0

    elif flamedoutfraction > 0.5:

      a._logevent("maximum power is reduced by one third as %d of the %d engines are flamed-out." % (
        flamedoutengines, a.engines()
      ))
      # 1/3 of APs, quantized in 1/4 units, rounding down.
      powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

      a._logevent("maximum power is reduced by one half as %d of the %d engines are flamed-out." % (
        flamedoutengines, a.engines()
      ))
      # 1/2 of APs, quantized in 1/4 units, rounding up.
      powerap = math.ceil(powerap / 2 * 4) / 4

    a._logevent("power is %.2f AP." % powerap)

    ############################################################################

    # Warn of the risk of flame-outs.

    # See rules 6.1, 6.7, and 8.5.

    if lastpowersetting == "I" and powersetting == "AB" and not a.hasproperty("RPR"):
      a._logevent("check for flame-out as the power setting has increased from I to AB.")

    if powersetting != "I" and a._altitude > a.ceiling():
      a._logevent("check for flame-out as the aircraft is above its ceiling and the power setting is %s." % powersetting)

    if a._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
      a._logevent("check for flame-out as the aircaft is in departed flight and the power setting is %s." % powersetting)

    if apvariants.withvariant("use version 2.4 rules"):
      if speed >= m1speed(a._altitudeband) and (powersetting == "I" or powersetting == "M"):
        a._logevent("check for flame-out as the speed is supersonic and the power setting is %s." % powersetting)

    ############################################################################

    # Determine the speed.
    
    # See rule 6.4 on recovery from departed flight.

    if a._previousflighttype == "DP" and a._flighttype != "DP" and speed < minspeed:
      speed = minspeed
      a._logevent("increasing speed to %.1f after recovering from departed flight." % minspeed)
      
    # See rules 6.1 and 6.6 on idle power setting, and compared with the new rule in version 2.4.

    if not apvariants.withvariant("use version 2.4 rules"):
      if powersetting == "I":
        speedchange = a.power("I")
        if a._speed >= m1speed(a._altitudeband):
          speedchange += 0.5
        # This keeps the speed non-negative. See rule 6.2.
        speedchange = min(speedchange, a._speed)
        speed -= speedchange
        a._logevent("reducing speed to %.1f as the power setting is I." % speed)

    reportspeed()
    
    ############################################################################

    # See the "Aircraft Damage Effects" in the Play Aids.

    if speed >= m1speed(a._altitudeband) and a.damageatleast("H"):
      a._logevent("check for progressive damage as damage is %s at supersonic speed." % a.damage())

    ############################################################################

    # Low-speed lift devices (e.g., slats or flaps).

    if a.lowspeedliftdevicelimit() is None:

      a._lowspeedliftdeviceextended = False
 
    else:
      
      if apvariants.withvariant("use version 2.4 rules") and a.lowspeedliftdeviceselectable():

        if lowspeedliftdeviceselected is not None:
          a._lowspeedliftdeviceselected = lowspeedliftdeviceselected

        if a._lowspeedliftdeviceselected:
          a._logevent("%s selected." % a.lowspeedliftdevicename())
        else:
          a._logevent("%s not selected." % a.lowspeedliftdevicename())

        a._lowspeedliftdeviceextended = a._lowspeedliftdeviceselected and (speed <= a.lowspeedliftdevicelimit())

      else:

        a._lowspeedliftdeviceextended = (speed <= a.lowspeedliftdevicelimit())

      if a._lowspeedliftdeviceextended:
        a._logevent("%s extended." % a.lowspeedliftdevicename())
      else:
        a._logevent("%s retracted." % a.lowspeedliftdevicename())

    a._logevent("minumum speed is %.1f." % a.minspeed())
    
    ############################################################################

    # See rule 6.3 on entering a stall.
      
    minspeed = a.minspeed()
    if speed < minspeed:
      a._logevent("speed is below the minimum of %.1f." % minspeed)
      a._logevent("aircraft is stalled.")
      if a._flighttype != "ST" and a._flighttype != "DP":
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

    if speed > a.cruisespeed():
      if powersetting == "I" or powersetting == "N":
        a._logevent("insufficient power above cruise speed (%.1f)." % a.cruisespeed())
        speedap -= 1.0

    # See rules 6.1 and 6.6 in version 2.4.

    if apvariants.withvariant("use version 2.4 rules"):
      if powersetting == "I":
        a._logevent("idle power.")
        speedap -= a.power("I")
        if speed >= m1speed(a._altitudeband):
          speedap -= 1.0

    # See rule 6.6
    
    if speed >= m1speed(a._altitudeband):
      if powersetting == "I" or powersetting == "N":
        speedap -= 2.0 * (speed - htspeed(a._altitudeband)) / 0.5
        a._logevent("insufficient power at supersonic speed (%.1f or more)." % m1speed(a._altitudeband))
      elif powersetting == "M":
        speedap -= 1.5 * (speed - htspeed(a._altitudeband)) / 0.5
        a._logevent("insufficient power at supersonic speed (%.1f or more)." % m1speed(a._altitudeband))

    # See rule 6.6

    if ltspeed(a._altitudeband) <= speed and speed <= m1speed(a._altitudeband):
      a._logevent("transonic drag.")
      if speed == ltspeed(a._altitudeband):
        speedap -= 0.5
      elif speed == htspeed(a._altitudeband):
        speedap -= 1.0
      elif speed == m1speed(a._altitudeband):
        speedap -= 1.5
      if a.hasproperty("LTD"):
        speedap += 0.5
      elif a.hasproperty("HTD"):
        speedap -= 0.5

    ############################################################################

    a._speed        = speed
    a._powersetting = powersetting
    a._powerap      = powerap
    a._speedap      = speedap
    
    ############################################################################

    # Report fuel.

    if not a._fuel is None:
      if a._bingofuel is None:
        a._logevent("fuel is %.1f." % a._fuel)
      else:
        a._logevent("fuel is %.1f and bingo fuel is %.1f." % (a._fuel, a._bingofuel))
      
    # Determine the fuel consumption. See rule 29.1.

    if not a._fuel is None:
      a._fuelconsumption = min(a._fuel, a.fuelrate() * (1 - flamedoutfraction))

################################################################################

def endmovespeed(a):

  """
  Carry out the rules to do with speed, power, and drag at the end of a move.
  """

  # For aircraft with SP flight type, we skip this.

  if a._flighttype == "SP":
    a.apcarry = 0
    a._logevent("speed is unchanged at %.1f." % a._speed)
    return

  # Report fuel.

  if not a._fuel is None:

    previousexternalfuel = a.externalfuel()
    previousinternalfuel = a.internalfuel()

    a._logevent("fuel consumption was %.1f." % a._fuelconsumption)
    a._fuel -= a._fuelconsumption
      
    if a._bingofuel is None:
      a._logevent("fuel is %.1f." % a._fuel)
    else:
      a._logevent("fuel is %.1f and bingo fuel is %.1f." % (a._fuel, a._bingofuel))
      if a._fuel < a._bingofuel:
        a._logevent("fuel is below bingo fuel.")

    if a.internalfuel() == 0:
      a._logend("fuel is exhausted.")

    if previousexternalfuel > 0 and a.externalfuel() == 0:
      a._logevent("external fuel is exhausted.")
      previousconfiguration = a._configuration
      a._updateconfiguration()
      if a._configuration != previousconfiguration:
        a._logevent("changed configuration from %s to %s." % (
          previousconfiguration, a._configuration
        ))

  # See the "Departed Flight Procedure" section of rule 6.4

  if a._flighttype == "DP" or a._maneuveringdeparture:
    a.apcarry = 0
    a._logevent("speed is unchanged at %.1f." % a._speed)
    return

  # See the "Speed Gain" and "Speed Loss" sections of rule 6.2.

  turnsap = a.turnrateap + a._sustainedturnap

  a._logevent("power           APs = %+.2f." % a._powerap)
  a._logevent("speed           APs = %+.2f." % a._speedap)
  a._logevent("altitude        APs = %+.2f." % a._altitudeap)
  a._logevent("turns           APs = %+.2f." % turnsap)
  a._logevent("other maneuvers APs = %+.2f." % a._othermaneuversap)
  a._logevent("speedbrakes     APs = %+.2f." % a._spbrap)
  a._logevent("carry           APs = %+.2f." % a._apcarry)
  ap = \
    a._powerap + \
    a._speedap + \
    a._altitudeap + \
    turnsap + \
    a._othermaneuversap + \
    a._spbrap + \
    a._apcarry
  a._logevent("total           APs = %+.2f." % ap)

  # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
  # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

  if ap < 0:
    aprate = -2.0
  elif a.hasproperty("RA"):
    if a._speed >= m1speed(a._altitudeband):
      aprate = +2.0
    else:
      aprate = +1.5
  else:
    if a._speed >= m1speed(a._altitudeband):
      aprate = +3.0
    else:
      aprate = +2.0

  # The speed is limited to the maximum dive speed if the aircraft dived at least
  # two levels. See rules 6.3 and 8.2.

  altitudeloss = a._previousaltitude - a._altitude
  usemaxdivespeed = (altitudeloss >= 2) and not a.damageatleast("H")
  
  # See rules 6.2, 6.3, and 8.2.

  if usemaxdivespeed:
    maxspeed = a.maxdivespeed()
    maxspeedname = "maximum dive speed"
  else:
    maxspeed = a.maxspeed()
    maxspeedname = "maximum speed"

  # See the Aircraft Damage Effects Table. We interpret its prohibition
  # on SS flight as follows: If an aircraft has at least H damage and
  # its speed exceeds HT speed, it performs a fadeback to HT speed. Its
  # maximum level speed and maximum dive speed are limited to HT speed.

  if maxspeed >= m1speed(a._altitudeband) and a.damageatleast("H"):
    a._logevent("maximum speed limited to HT speed by damage.")
    usedivespeed = False
    maxspeed = htspeed(a._altitudeband)
    maxspeedname = "HT speed"

  a._newspeed = a._speed

  if ap == 0:

    a._apcarry = 0

  elif ap < 0:

    # See the "Speed Loss" and "Maximum Deceleration" sections of rule 6.2.

    a._newspeed -= 0.5 * (ap // aprate)
    a._apcarry = ap % aprate

    if a._newspeed <= 0:
      a._newspeed = 0
      if a._apcarry < 0:
        a._apcarry = 0        

  elif ap > 0:

    if a._speed >= maxspeed and ap >= aprate:
      a._logevent("acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
      a._apcarry = aprate - 0.5
    elif a._speed >= maxspeed:
      a._apcarry = ap
    elif a._speed + 0.5 * (ap // aprate) > maxspeed:
      a._logevent("acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
      a._newspeed = maxspeed
      a._apcarry = aprate - 0.5
    else:
      a._newspeed += 0.5 * (ap // aprate)
      a._apcarry = ap % aprate

  if usemaxdivespeed:
    if a._newspeed > maxspeed:
      a._logevent("speed will be reduced to maximum dive speed of %.1f." % maxspeed)
      a._newspeed = maxspeed
  else:
    if a._newspeed > maxspeed:
      a._logevent("speed will be faded back from %.1f." % a._newspeed)
      a._newspeed = max(a._newspeed - 1, maxspeed)

  if a._speed != a._newspeed:
    a._logevent("speed will change from %.1f to %.1f." % (a._speed, a._newspeed))
  else:
    a._logevent("speed will be unchanged at %.1f." % a._newspeed)

  a._logevent("will carry %+.2f APs." % a._apcarry)

  # See rule 6.4.

  minspeed = a.minspeed()
  if a._newspeed < minspeed:
    a._logevent("speed will be below the minimum of %.1f." % minspeed)
  if a._newspeed >= minspeed and a._flighttype == "ST":
    a._logevent("aircraft will no longer be stalled.")
  elif a._newspeed < minspeed and a._flighttype == "ST":
    a._logevent("aircraft will still stalled.")
  elif a._newspeed < minspeed:
    a._logevent("aircraft will have stalled.")

################################################################################
