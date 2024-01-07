import math

import apxo.capabilities  as apcapabilities
import apxo.configuration as apconfiguration
import apxo.variants      as apvariants

from apxo.math         import onethird, twothirds
from apxo.normalflight import _isclimbingflight, _isdivingflight
from apxo.log           import plural

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

def startmovespeed(A, power, flamedoutengines, lowspeedliftdeviceselected):

    """
    Carry out the rules to do with power, speed, and speed-induced drag at the 
    start of a move.
    """

    def reportspeed():
      if speed < ltspeed(A._altitudeband):
        A._logstart("speed         is %.1f." % speed)
      elif speed == ltspeed(A._altitudeband):
        A._logstart("speed         is %.1f (LT)." % speed)
      elif speed == htspeed(A._altitudeband):
        A._logstart("speed         is %.1f (HT)." % speed)
      else:
        A._logstart("speed         is %.1f (SS)." % speed)      

    ############################################################################

    # For aircraft with SP flight type, the power is interpreted as the
    # speed and we skip the rest.

    if A._flighttype == "SP":
      speed = power
      reportspeed()
      A._speed        = speed
      A._powersetting = ""
      A._powerap      = 0
      A._speedap      = 0
      return

    ############################################################################

    lastpowersetting = A._previouspowersetting
    speed            = A._speed

    ############################################################################

    # See rule 29.1.
    if not A._fuel is None:
      if A._fuel == 0:
        if apcapabilities.engines(A) == 1:
          A._logevent("the engine is flamed-out from a lack of fuel.")
        else:
          A._logstart("all engines are flamed-out from a lack of fuel.")
        flamedoutengines = apcapabilities.engines(A)
      
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

    powerapM  = apcapabilities.power(A, "M")
    powerapAB = apcapabilities.power(A, "AB")
    if apvariants.withvariant("disallow HT/FT"):
      powerapHT = None
      powerapFT = None
    else:
      powerapHT = apcapabilities.power(A, "HT")
      powerapFT = apcapabilities.power(A, "FT")

    jet = (powerapM != None)

    # See rule 8.4.

    if A._altitudeband == "VH":
      if jet and not apcapabilities.hasproperty(A, "HAE"):
        powerapM  = max(0.5, twothirds(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, twothirds(powerapAB))
    elif (A._altitudeband == "EH" or A._altitudeband == "UH"):
      if jet and not apcapabilities.hasproperty(A, "HAE"):
        powerapM  = max(0.5, onethird(powerapM))
        if powerapAB != None:
          powerapAB = max(0.5, onethird(powerapAB))     

    # Some propeller aircraft lose power at high speed.
    if apcapabilities.powerfade(A) != None:
      powerapHT = max(0.0, powerapHT - apcapabilities.powerfade(A))
      powerapFT = max(0.0, powerapFT - apcapabilities.powerfade(A))

    # See "Aircraft Damage Effects" in the Play Aids.
    if A.damageatleast("H"):
      if jet:
        powerapM /= 2
        if powerapAB != None:
          powerapAB /= 2
      else:
        powerapHT /= 2
        powerapFT /= 2
    if A.damageatleast("C"):
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

    A._logstart("power setting is %s." % powersetting)

    # See rule 8.4. The reduction was done above, but we report it here.
    if jet and not apcapabilities.hasproperty(A, "HAE") and (
      A._altitudeband == "VH" or A._altitudeband == "EH" or A._altitudeband == "UH"
    ):
      A._logevent("power is reduced in the %s altitude band." % A._altitudeband)
        
    # Again, the reduction was done above, but we report it here.
    if apcapabilities.powerfade(A) != None and apcapabilities.powerfade(A) > 0.0:
      A._logevent("power is reduced as the speed is %.1f." % speed)
    
    # Again, the reduction was done above, but we report it here.
    if A.damageatleast("H"):
      A._logevent("power is reduced as damage is %s." % A.damage())

    # Is the engine smoking?
    A._enginesmoking = (apcapabilities.hasproperty(A, "SMP") and powersetting == "M")
    if A._enginesmoking:
      A._logevent("engine is smoking.")

    # See rule 6.7

    flamedoutfraction = flamedoutengines / apcapabilities.engines(A)

    if flamedoutfraction == 1:

      if apcapabilities.engines(A) == 1:
        A._logevent("power setting is treated as I as the engine is flamed-out.")
      else:
        A._logevent("power setting is treated as I as all %d engines are flamed-out." % apcapabilities.engines(A))
      powersetting = "I"
      powerap = 0

    elif flamedoutfraction > 0.5:

      A._logevent("maximum power is reduced by one third as %d of the %d engines are flamed-out." % (
        flamedoutengines, apcapabilities.engines(A)
      ))
      # 1/3 of APs, quantized in 1/4 units, rounding down.
      powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

      A._logevent("maximum power is reduced by one half as %d of the %d engines are flamed-out." % (
        flamedoutengines, apcapabilities.engines(A)
      ))
      # 1/2 of APs, quantized in 1/4 units, rounding up.
      powerap = math.ceil(powerap / 2 * 4) / 4

    A._logevent("power is %.2f AP." % powerap)

    ############################################################################

    # Warn of the risk of flame-outs.

    # See rules 6.1, 6.7, and 8.5.

    if lastpowersetting == "I" and powersetting == "AB" and not apcapabilities.hasproperty(A, "RPR"):
      A._logevent("check for flame-out as the power setting has increased from I to AB.")

    if powersetting != "I" and A._altitude > apcapabilities.ceiling(A):
      A._logevent("check for flame-out as the aircraft is above its ceiling and the power setting is %s." % powersetting)

    if A._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
      A._logevent("check for flame-out as the aircaft is in departed flight and the power setting is %s." % powersetting)

    if apvariants.withvariant("use version 2.4 rules"):
      if speed >= m1speed(A._altitudeband) and (powersetting == "I" or powersetting == "M"):
        A._logevent("check for flame-out as the speed is supersonic and the power setting is %s." % powersetting)

    ############################################################################

    # Determine the speed.
    
    # See rule 6.4 on recovery from departed flight.

    if A._previousflighttype == "DP" and A._flighttype != "DP" and speed < minspeed:
      speed = minspeed
      A._logevent("increasing speed to %.1f after recovering from departed flight." % minspeed)
      
    # See rules 6.1 and 6.6 on idle power setting, and compared with the new rule in version 2.4.

    if not apvariants.withvariant("use version 2.4 rules"):
      if powersetting == "I":
        speedchange = apcapabilities.power(A, "I")
        if A._speed >= m1speed(A._altitudeband):
          speedchange += 0.5
        # This keeps the speed non-negative. See rule 6.2.
        speedchange = min(speedchange, A._speed)
        speed -= speedchange
        A._logevent("reducing speed to %.1f as the power setting is I." % speed)

    reportspeed()
    
    ############################################################################

    # See the "Aircraft Damage Effects" in the Play Aids.

    if speed >= m1speed(A._altitudeband) and A.damageatleast("H"):
      A._logevent("check for progressive damage as damage is %s at supersonic speed." % A.damage())

    ############################################################################

    # Low-speed lift devices (e.g., slats or flaps).

    if apcapabilities.lowspeedliftdevicelimit(A) is None:

      A._lowspeedliftdeviceextended = False
 
    else:
      
      if apvariants.withvariant("use version 2.4 rules") and apcapabilities.lowspeedliftdeviceselectable(A):

        if lowspeedliftdeviceselected is not None:
          A._lowspeedliftdeviceselected = lowspeedliftdeviceselected

        if A._lowspeedliftdeviceselected:
          A._logevent("%s selected." % apcapabilities.lowspeedliftdevicename(A))
        else:
          A._logevent("%s not selected." % apcapabilities.lowspeedliftdevicename(A))

        A._lowspeedliftdeviceextended = A._lowspeedliftdeviceselected and (speed <= apcapabilities.lowspeedliftdevicelimit(A))

      else:

        A._lowspeedliftdeviceextended = (speed <= apcapabilities.lowspeedliftdevicelimit(A))

      if A._lowspeedliftdeviceextended:
        A._logevent("%s extended." % apcapabilities.lowspeedliftdevicename(A))
      else:
        A._logevent("%s retracted." % apcapabilities.lowspeedliftdevicename(A))

    A._logevent("minumum speed is %.1f." % apcapabilities.minspeed(A))
    
    ############################################################################

    # See rule 6.3 on entering a stall.
      
    minspeed = apcapabilities.minspeed(A)
    if speed < minspeed:
      A._logevent("speed is below the minimum of %.1f." % minspeed)
      A._logevent("aircraft is stalled.")
      if A._flighttype != "ST" and A._flighttype != "DP":
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

    if speed > apcapabilities.cruisespeed(A):
      if powersetting == "I" or powersetting == "N":
        A._logevent("insufficient power above cruise speed (%.1f)." % apcapabilities.cruisespeed(A))
        speedap -= 1.0

    # See rules 6.1 and 6.6 in version 2.4.

    if apvariants.withvariant("use version 2.4 rules"):
      if powersetting == "I":
        A._logevent("idle power.")
        speedap -= apcapabilities.power(A, "I")
        if speed >= m1speed(A._altitudeband):
          speedap -= 1.0

    # See rule 6.6
    
    if speed >= m1speed(A._altitudeband):
      if powersetting == "I" or powersetting == "N":
        speedap -= 2.0 * (speed - htspeed(A._altitudeband)) / 0.5
        A._logevent("insufficient power at supersonic speed (%.1f or more)." % m1speed(A._altitudeband))
      elif powersetting == "M":
        speedap -= 1.5 * (speed - htspeed(A._altitudeband)) / 0.5
        A._logevent("insufficient power at supersonic speed (%.1f or more)." % m1speed(A._altitudeband))

    # See rule 6.6

    if ltspeed(A._altitudeband) <= speed and speed <= m1speed(A._altitudeband):
      A._logevent("transonic drag.")
      if speed == ltspeed(A._altitudeband):
        speedap -= 0.5
      elif speed == htspeed(A._altitudeband):
        speedap -= 1.0
      elif speed == m1speed(A._altitudeband):
        speedap -= 1.5
      if apcapabilities.hasproperty(A, "LTD"):
        speedap += 0.5
      elif apcapabilities.hasproperty(A, "HTD"):
        speedap -= 0.5

    ############################################################################

    A._speed        = speed
    A._powersetting = powersetting
    A._powerap      = powerap
    A._speedap      = speedap
    
    ############################################################################

    # Report fuel.

    if not A._fuel is None:
      if A._bingofuel is None:
        A._logevent("fuel is %.1f." % A._fuel)
      else:
        A._logevent("fuel is %.1f and bingo fuel is %.1f." % (A._fuel, A._bingofuel))
      
    # Determine the fuel consumption. See rule 29.1.

    if not A._fuel is None:
      A._fuelconsumption = min(A._fuel, apcapabilities.fuelrate(A) * (1 - flamedoutfraction))

################################################################################

def endmovespeed(A):

  """
  Carry out the rules to do with speed, power, and drag at the end of a move.
  """

  # For aircraft with SP flight type, we skip this.

  if A._flighttype == "SP":
    A.apcarry = 0
    A._logevent("speed is unchanged at %.1f." % A._speed)
    return

  # Report fuel.

  if not A._fuel is None:

    previousexternalfuel = A.externalfuel()
    previousinternalfuel = A.internalfuel()

    A._logevent("fuel consumption was %.1f." % A._fuelconsumption)
    A._fuel -= A._fuelconsumption
      
    if A._bingofuel is None:
      A._logevent("fuel is %.1f." % A._fuel)
    else:
      A._logevent("fuel is %.1f and bingo fuel is %.1f." % (A._fuel, A._bingofuel))
      if A._fuel < A._bingofuel:
        A._logevent("fuel is below bingo fuel.")

    if A.internalfuel() == 0:
      A._logend("fuel is exhausted.")

    if previousexternalfuel > 0 and A.externalfuel() == 0:
      A._logevent("external fuel is exhausted.")
      previousconfiguration = A._configuration
      apconfiguration.update(A)
      if A._configuration != previousconfiguration:
        A._logevent("changed configuration from %s to %s." % (
          previousconfiguration, A._configuration
        ))

  # See the "Departed Flight Procedure" section of rule 6.4

  if A._flighttype == "DP" or A._maneuveringdeparture:
    A.apcarry = 0
    A._logevent("speed is unchanged at %.1f." % A._speed)
    return

  # See the "Speed Gain" and "Speed Loss" sections of rule 6.2.

  A._turnsap = A._turnrateap + A._sustainedturnap

  A._logevent("power           APs = %+.2f." % A._powerap)
  A._logevent("speed           APs = %+.2f." % A._speedap)
  A._logevent("altitude        APs = %+.2f." % A._altitudeap)
  A._logevent("turns           APs = %+.2f." % A._turnsap)
  A._logevent("other maneuvers APs = %+.2f." % A._othermaneuversap)
  A._logevent("speedbrakes     APs = %+.2f." % A._spbrap)
  A._logevent("carry           APs = %+.2f." % A._apcarry)
  ap = \
    A._powerap + \
    A._speedap + \
    A._altitudeap + \
    A._turnsap + \
    A._othermaneuversap + \
    A._spbrap + \
    A._apcarry
  A._logevent("total           APs = %+.2f." % ap)

  # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
  # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

  if ap < 0:
    aprate = -2.0
  elif apcapabilities.hasproperty(A, "RA"):
    if A._speed >= m1speed(A._altitudeband):
      aprate = +2.0
    else:
      aprate = +1.5
  else:
    if A._speed >= m1speed(A._altitudeband):
      aprate = +3.0
    else:
      aprate = +2.0

  # The speed is limited to the maximum dive speed if the aircraft dived at least
  # two levels. See rules 6.3 and 8.2.

  altitudeloss = A._previousaltitude - A._altitude
  usemaxdivespeed = (altitudeloss >= 2) and not A.damageatleast("H")
  
  # See rules 6.2, 6.3, and 8.2.

  if usemaxdivespeed:
    maxspeed = apcapabilities.maxdivespeed(A)
    maxspeedname = "maximum dive speed"
  else:
    maxspeed = apcapabilities.maxspeed(A)
    maxspeedname = "maximum speed"

  # See the Aircraft Damage Effects Table. We interpret its prohibition
  # on SS flight as follows: If an aircraft has at least H damage and
  # its speed exceeds HT speed, it performs a fadeback to HT speed. Its
  # maximum level speed and maximum dive speed are limited to HT speed.

  if maxspeed >= m1speed(A._altitudeband) and A.damageatleast("H"):
    A._logevent("maximum speed limited to HT speed by damage.")
    usedivespeed = False
    maxspeed = htspeed(A._altitudeband)
    maxspeedname = "HT speed"

  A._newspeed = A._speed

  if ap == 0:

    A._apcarry = 0

  elif ap < 0:

    # See the "Speed Loss" and "Maximum Deceleration" sections of rule 6.2.

    A._newspeed -= 0.5 * (ap // aprate)
    A._apcarry = ap % aprate

    if A._newspeed <= 0:
      A._newspeed = 0
      if A._apcarry < 0:
        A._apcarry = 0        

  elif ap > 0:

    if A._speed >= maxspeed and ap >= aprate:
      A._logevent("acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
      A._apcarry = aprate - 0.5
    elif A._speed >= maxspeed:
      A._apcarry = ap
    elif A._speed + 0.5 * (ap // aprate) > maxspeed:
      A._logevent("acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed))
      A._newspeed = maxspeed
      A._apcarry = aprate - 0.5
    else:
      A._newspeed += 0.5 * (ap // aprate)
      A._apcarry = ap % aprate

  if usemaxdivespeed:
    if A._newspeed > maxspeed:
      A._logevent("speed will be reduced to maximum dive speed of %.1f." % maxspeed)
      A._newspeed = maxspeed
  else:
    if A._newspeed > maxspeed:
      A._logevent("speed will be faded back from %.1f." % A._newspeed)
      A._newspeed = max(A._newspeed - 1, maxspeed)

  if A._speed != A._newspeed:
    A._logevent("speed will change from %.1f to %.1f." % (A._speed, A._newspeed))
  else:
    A._logevent("speed will be unchanged at %.1f." % A._newspeed)

  A._logevent("will carry %+.2f APs." % A._apcarry)

  # See rule 6.4.

  minspeed = apcapabilities.minspeed(A)
  if A._newspeed < minspeed:
    A._logevent("speed will be below the minimum of %.1f." % minspeed)
  if A._newspeed >= minspeed and A._flighttype == "ST":
    A._logevent("aircraft will no longer be stalled.")
  elif A._newspeed < minspeed and A._flighttype == "ST":
    A._logevent("aircraft will still stalled.")
  elif A._newspeed < minspeed:
    A._logevent("aircraft will have stalled.")

################################################################################
