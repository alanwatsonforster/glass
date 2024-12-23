import math

import apxo.capabilities as apcapabilities
import apxo.gameturn as apgameturn
import apxo.variants as apvariants

from apxo.rounding import *
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


def missilemaxspeed(altitudeband):
    table = {"LO": 24, "ML": 26, "MH": 28, "HI": 30, "VH": 32, "EH": 34, "UH": 36}
    return table[altitudeband]


def missileminspeed(altitudeband):
    table = {"LO": 2, "ML": 3, "MH": 3, "HI": 4, "VH": 4, "EH": 5, "UH": 7}
    return table[altitudeband]


def missilemaneuverspeed(altitudeband):
    table = {"LO": 4, "ML": 5, "MH": 6, "HI": 7, "VH": 8, "EH": 10, "UH": 14}
    return table[altitudeband]


################################################################################


def _startaircraftspeed(
    A,
    power,
    flamedoutengines=None,
    lowspeedliftdeviceselected=None,
    speedbrakes=None,
    **kwargs
):
    """
    Carry out the rules to do with power, speed, and speed-induced drag at the
    start of a move.
    """

    previouspowersetting = A._powersetting

    # These account for the APs associated with power, speed, speed-brakes,
    # turns (split into the part for the maximum turn rate and the part for
    # sustained turns), altitude loss or gain, and special maneuvers. They
    # are used in normal flight and stalled flight, but not departed flight.

    A._powerap = 0
    A._speedap = 0
    A._speedbrakeap = 0
    A._turnrateap = 0
    A._sustainedturnap = 0
    A._altitudeap = 0
    A._othermaneuversap = 0

    # These keep track of the maximum turn rate used in the turn, the
    # number of roll maneuvers, and the effective climb capability
    # (the climb capability at the moment the first VFP is used).
    # Again, they are used to calculate the final speed.

    A._maxturnrate = None
    A._effectiveclimbcapability = None

    ############################################################################

    # Determine the speed.

    if A._flighttype == "SP":
        speed = power
        A._setspeed(speed)
        A._powersetting = ""
        A._powerap = 0
        A._speedap = 0

    speed = A.speed()

    # See rule 6.4 on recovery from departed flight.

    if A._previousflighttype == "DP" and A._flighttype != "DP" and speed < minspeed:
        speed = minspeed
        A.logcomment(
            "increasing speed to %.1f after recovering from departed flight." % minspeed
        )

    A.logstart("speed            is %.1f." % speed)

    if speed < ltspeed(A.altitudeband()):
        A.logcomment("speed is subsonic and below low transsonic.")
    elif speed == ltspeed(A.altitudeband()):
        A.logcomment("speed is low transonic.")
    elif speed == htspeed(A.altitudeband()):
        A.logcomment("speed is high transonic.")
    else:
        A.logcomment("speed is supersonic.")

    ############################################################################

    A.logstart("configuration    is %s." % A._configuration)
    A.logstart("damage           is %s." % A.damage())

    ############################################################################

    if A._flighttype == "SP":
        return

    ############################################################################

    # See rule 29.1.
    if not A._fuel is None:
        if A._fuel == 0:
            if apcapabilities.engines(A) == 1:
                A.logcomment("the engine is flamed-out from a lack of fuel.")
            else:
                A.logstart("all engines are flamed-out from a lack of fuel.")
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

    powerapM = apcapabilities.power(A, "M")
    powerapAB = apcapabilities.power(A, "AB")
    if apvariants.withvariant("disallow HT/FT"):
        powerapHT = None
        powerapFT = None
    else:
        powerapHT = apcapabilities.power(A, "HT")
        powerapFT = apcapabilities.power(A, "FT")

    jet = powerapM != None

    # See rule 8.4.

    if A.altitudeband() == "VH":
        if jet and not A.hasproperty("HAE"):
            powerapM = max(0.5, twothirdsfromtable(powerapM))
            if powerapAB != None:
                powerapAB = max(0.5, twothirdsfromtable(powerapAB))
    elif A.altitudeband() == "EH" or A.altitudeband() == "UH":
        if jet and not A.hasproperty("HAE"):
            powerapM = max(0.5, onethirdfromtable(powerapM))
            if powerapAB != None:
                powerapAB = max(0.5, onethirdfromtable(powerapAB))

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
        powerap = 0
    elif power == "N":
        powersetting = "N"
        powerap = 0
    elif power == "M" and powerapM == None:
        raise RuntimeError("aircraft does not have an M power setting.")
    elif power == "M":
        powersetting = "M"
        powerap = powerapM
    elif power == "AB" and powerapAB == None:
        raise RuntimeError("aircraft does not have an AB power setting.")
    elif power == "AB":
        powersetting = "AB"
        powerap = powerapAB
    elif power == "HT" and powerapHT == None:
        raise RuntimeError("aircraft does not have an HT power setting.")
    elif power == "HT":
        powersetting = "HT"
        powerap = powerapHT
    elif power == "FT" and powerapFT == None:
        raise RuntimeError("aircraft does not have an FT power setting.")
    elif power == "FT":
        powersetting = "FT"
        powerap = powerapFT
    elif not isinstance(power, (int, float)) or power < 0 or power % 0.25 != 0:
        raise RuntimeError("invalid power %r" % power)
    elif powerapM != None and power <= powerapM:
        powersetting = "M"
        powerap = power
    elif powerapAB != None and power <= powerapAB:
        powersetting = "AB"
        powerap = power
    elif powerapHT != None and power <= powerapHT:
        powersetting = "HT"
        powerap = power
    elif powerapFT != None and power <= powerapFT:
        powersetting = "FT"
        powerap = power
    else:
        raise RuntimeError(
            "requested power of %s exceeds aircraft capability."
            % (plural(power, "1 AP", "%s APs" % power))
        )

    A.logstart("power setting    is %s." % powersetting)

    # See rule 8.4. The reduction was done above, but we report it here.
    if (
        jet
        and not A.hasproperty("HAE")
        and (
            A.altitudeband() == "VH"
            or A.altitudeband() == "EH"
            or A.altitudeband() == "UH"
        )
    ):
        A.logcomment("power is reduced in the %s altitude band." % A.altitudeband())

    # Again, the reduction was done above, but we report it here.
    if apcapabilities.powerfade(A) != None and apcapabilities.powerfade(A) > 0.0:
        A.logcomment("power is reduced as the speed is %.1f." % speed)

    # Again, the reduction was done above, but we report it here.
    if A.damageatleast("H"):
        A.logcomment("power is reduced as damage is %s." % A.damage())

    # Is the engine smoking?
    A._enginesmoking = A.hasproperty("SMP") and powersetting == "M"
    if A._enginesmoking:
        A.logcomment("engine is smoking.")

    # See rule 6.7

    flamedoutfraction = flamedoutengines / apcapabilities.engines(A)

    if flamedoutfraction == 1:

        if apcapabilities.engines(A) == 1:
            A.logcomment("power setting is treated as I as the engine is flamed-out.")
        else:
            A.logcomment(
                "power setting is treated as I as all %d engines are flamed-out."
                % apcapabilities.engines(A)
            )
        powersetting = "I"
        powerap = 0

    elif flamedoutfraction > 0.5:

        A.logcomment(
            "maximum power is reduced by one third as %d of the %d engines are flamed-out."
            % (flamedoutengines, apcapabilities.engines(A))
        )
        # 1/3 of APs, quantized in 1/4 units, rounding down.
        powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

        A.logcomment(
            "maximum power is reduced by one half as %d of the %d engines are flamed-out."
            % (flamedoutengines, apcapabilities.engines(A))
        )
        # 1/2 of APs, quantized in 1/4 units, rounding up.
        powerap = math.ceil(powerap / 2 * 4) / 4

    A.logcomment("%s power (%+.1f AP)." % (powersetting, powerap))

    ############################################################################

    # Warn of the risk of flame-outs.

    # See rules 6.1, 6.7, and 8.5.

    if (
        previouspowersetting == "I"
        and powersetting == "AB"
        and not A.hasproperty("RPR")
    ):
        A.logcomment(
            "check for flame-out as the power setting has increased from I to AB."
        )

    if powersetting != "I" and A.altitude() > apcapabilities.ceiling(A):
        A.logcomment(
            "check for flame-out as the aircraft is above its ceiling and the power setting is %s."
            % powersetting
        )

    if A._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
        A.logcomment(
            "check for flame-out as the aircraft is in departed flight and the power setting is %s."
            % powersetting
        )

    if speed >= m1speed(A.altitudeband()) and (
        powersetting == "I" or powersetting == "N"
    ):
        A.logcomment(
            "%s flame-out as the speed is supersonic and the power setting is %s."
            % (plural(apcapabilities.engines(A), "engine", "engines"), powersetting)
        )

    ############################################################################

    # See the "Aircraft Damage Effects" in the Play Aids.

    if speed >= m1speed(A.altitudeband()) and A.damageatleast("H"):
        A.logcomment(
            "check for progressive damage as damage is %s at supersonic speed."
            % A.damage()
        )

    ############################################################################

    # Low-speed lift devices (e.g., slats or flaps).

    if apcapabilities.lowspeedliftdevicelimit(A) is None:

        A._lowspeedliftdeviceextended = False

    else:

        if apcapabilities.lowspeedliftdeviceselectable(A):

            if lowspeedliftdeviceselected is not None:
                A._lowspeedliftdeviceselected = lowspeedliftdeviceselected

            if A._lowspeedliftdeviceselected:
                A.logcomment("%s selected." % apcapabilities.lowspeedliftdevicename(A))
            else:
                A.logcomment(
                    "%s not selected." % apcapabilities.lowspeedliftdevicename(A)
                )

            A._lowspeedliftdeviceextended = A._lowspeedliftdeviceselected and (
                speed <= apcapabilities.lowspeedliftdevicelimit(A)
            )

        else:

            A._lowspeedliftdeviceextended = (
                speed <= apcapabilities.lowspeedliftdevicelimit(A)
            )

        if A._lowspeedliftdeviceextended:
            A.logcomment("%s extended." % apcapabilities.lowspeedliftdevicename(A))
        else:
            A.logcomment("%s retracted." % apcapabilities.lowspeedliftdevicename(A))

    A.logcomment("minumum speed is %.1f." % apcapabilities.minspeed(A))

    ############################################################################

    # See rule 6.3 on entering a stall.

    minspeed = apcapabilities.minspeed(A)
    if speed < minspeed:
        A.logcomment("speed is below the minimum of %.1f." % minspeed)
        A.logcomment("aircraft is stalled.")
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
            dspeedap = -1.0
            speedap += dspeedap
            A.logcomment(
                "%s power above cruise speed (%+.1f AP)." % (powersetting, dspeedap)
            )

    # See rules 6.1 and 6.6 in version 2.4.

    if powersetting == "I":
        dspeedap = -apcapabilities.power(A, "I")
        speedap += dspeedap
        A.logcomment("%s power (%+.1f AP)." % (powersetting, dspeedap))
        if speed >= m1speed(A.altitudeband()):
            dspeedap = -1.0
            speedap += dspeedap
            A.logcomment(
                "%s power at supersonic speed (%+.1f AP)." % (powersetting, dspeedap)
            )

    # See rule 6.6

    if speed >= m1speed(A.altitudeband()):
        if powersetting == "I" or powersetting == "N":
            dspeedap = -2.0 * (speed - htspeed(A.altitudeband())) / 0.5
            speedap += dspeedap
            A.logcomment(
                "%s power at supersonic speed (%+.1f AP)." % (powersetting, dspeedap)
            )
        elif powersetting == "M":
            dspeedap = -1.5 * (speed - htspeed(A.altitudeband())) / 0.5
            speedap += dspeedap
            A.logcomment(
                "%s power at supersonic speed (%+.1f AP)." % (powersetting, dspeedap)
            )

    # See rule 6.6

    if ltspeed(A.altitudeband()) <= speed and speed <= m1speed(A.altitudeband()):
        if speed == ltspeed(A.altitudeband()):
            dspeedap = -0.5
        elif speed == htspeed(A.altitudeband()):
            dspeedap = -1.0
        elif speed == m1speed(A.altitudeband()):
            dspeedap = -1.5
        if A.hasproperty("LTD"):
            dspeedap += 0.5
        elif A.hasproperty("HTD"):
            dspeedap -= 0.5
        speedap += dspeedap
        A.logcomment("transonic drag (%+.1f AP)." % dspeedap)

    ############################################################################

    A._setspeed(speed)
    A._powersetting = powersetting
    A._powerap = powerap
    A._speedap = speedap

    ############################################################################

    # Report fuel.

    if not A._fuel is None:
        if A._bingofuel is None:
            A.logcomment("fuel is %.1f." % A._fuel)
        else:
            A.logcomment(
                "fuel is %.1f and bingo fuel is %.1f." % (A._fuel, A._bingofuel)
            )

    # Determine the fuel consumption. See rule 29.1.

    if not A._fuel is None:
        A._fuelconsumption = min(
            A._fuel, apcapabilities.fuelrate(A) * (1 - flamedoutfraction)
        )

    ############################################################################

    # Determine effects of speed brakes.

    if speedbrakes is not None:

        maxspeedbrakes = apcapabilities.speedbrake(A)
        if maxspeedbrakes is None:
            raise RuntimeError("aircraft does not have speedbrakes.")

        if A.speed() >= m1speed(A.altitudeband()):
            maxspeedbrakes += 2.0

        if speedbrakes is True:
            speedbrakes = maxspeedbrakes

        if speedbrakes > maxspeedbrakes:
            raise RuntimeError(
                plural(
                    maxspeedbrakes,
                    "speedbrake capability is only 1.0 DP.",
                    "speedbrake capability is only %.1f DPs." % maxspeedbrakes,
                )
            )
        A._speedbrakeap = -speedbrakes
        A.logcomment("speedbrakes (%+.1f AP)." % A._speedbrakeap)


################################################################################


def _endaircraftspeed(A):
    """
    Carry out the rules to do with speed, power, and drag at the end of a move.
    """

    if A._flighttype == "SP" or A._flighttype == "DP":
        A._newspeed = A.speed()
        A.logcomment("speed is unchanged at %.1f." % A.speed())
        return

    # Report fuel.

    if not A._fuel is None:

        previousexternalfuel = A.externalfuel()
        previousinternalfuel = A.internalfuel()

        A.logcomment("fuel consumption was %.1f." % A._fuelconsumption)
        A._fuel -= A._fuelconsumption

        if A._bingofuel is None:
            A.logcomment("fuel is %.1f." % A._fuel)
        else:
            A.logcomment(
                "fuel is %.1f and bingo fuel is %.1f." % (A._fuel, A._bingofuel)
            )
            if A._fuel < A._bingofuel:
                A.logcomment("fuel is below bingo fuel.")

        if A.internalfuel() == 0:
            A.logend("fuel is exhausted.")

        if previousexternalfuel > 0 and A.externalfuel() == 0:
            A.logcomment("external fuel is exhausted.")
            previousconfiguration = A._configuration
            A._updateconfiguration()
            if A._configuration != previousconfiguration:
                A.logcomment(
                    "changed configuration from %s to %s."
                    % (previousconfiguration, A._configuration)
                )

    # See the "Departed Flight Procedure" section of rule 6.4

    if A._flighttype == "DP" or A._maneuveringdeparture:
        A.apcarry = 0
        A.logcomment("speed is unchanged at %.1f." % A.speed())
        return

    # See the "Speed Gain" and "Speed Loss" sections of rule 6.2.

    A._turnsap = A._turnrateap + A._sustainedturnap

    A.logcomment("power           APs = %+.2f." % A._powerap)
    A.logcomment("speed           APs = %+.2f." % A._speedap)
    A.logcomment("altitude        APs = %+.2f." % A._altitudeap)
    A.logcomment("turns           APs = %+.2f." % A._turnsap)
    A.logcomment("other maneuvers APs = %+.2f." % A._othermaneuversap)
    A.logcomment("speedbrakes     APs = %+.2f." % A._speedbrakeap)
    A.logcomment("carry           APs = %+.2f." % A._apcarry)
    ap = (
        A._powerap
        + A._speedap
        + A._altitudeap
        + A._turnsap
        + A._othermaneuversap
        + A._speedbrakeap
        + A._apcarry
    )
    A.logcomment("total           APs = %+.2f." % ap)

    # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
    # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

    if ap < 0:
        aprate = -2.0
    elif A.hasproperty("RA"):
        if A.speed() >= m1speed(A.startaltitudeband()):
            aprate = +2.0
        else:
            aprate = +1.5
    else:
        if A.speed() >= m1speed(A.startaltitudeband()):
            aprate = +3.0
        else:
            aprate = +2.0

    # The speed is limited to the maximum dive speed if the aircraft dived at least
    # two levels. See rules 6.3 and 8.2.

    altitudeloss = A.startaltitude() - A.altitude()
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

    if maxspeed >= m1speed(A.altitudeband()) and A.damageatleast("H"):
        A.logcomment("maximum speed limited to HT speed by damage.")
        usedivespeed = False
        maxspeed = htspeed(A.altitudeband())
        maxspeedname = "HT speed"

    A._newspeed = A.speed()

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

        if apvariants.withvariant("use house rules"):
            maxapcarrybeyondmaxspeed = 0.0
        else:
            maxapcarrybeyondmaxspeed = aprate - 0.5

        if A.speed() >= maxspeed:
            A._apcarry = ap
            if A._apcarry > maxapcarrybeyondmaxspeed:
                A.logcomment(
                    "acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed)
                )
                A._apcarry = maxapcarrybeyondmaxspeed
        elif A.speed() + 0.5 * (ap // aprate) > maxspeed:
            A.logcomment(
                "acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed)
            )
            A._newspeed = maxspeed
            A._apcarry = maxapcarrybeyondmaxspeed
        else:
            A._newspeed += 0.5 * (ap // aprate)
            A._apcarry = ap % aprate
            if A._newspeed >= maxspeed and A._apcarry > maxapcarrybeyondmaxspeed:
                A.logcomment(
                    "acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed)
                )
                A._apcarry = maxapcarrybeyondmaxspeed

    if usemaxdivespeed:
        if A._newspeed > maxspeed:
            A.logcomment(
                "speed will be reduced to maximum dive speed of %.1f." % maxspeed
            )
            A._newspeed = maxspeed
    else:
        if A._newspeed > maxspeed:
            A.logcomment("speed will be faded back from %.1f." % A._newspeed)
            A._newspeed = max(A._newspeed - 1, maxspeed)

    A.logend("speed will be %.1f." % A._newspeed)
    if A._newspeed < m1speed(A.altitudeband()):
        A.logcomment("speed will be subsonic.")
    else:
        A.logcomment("speed will be supersonic.")

    # See rule 6.4.

    minspeed = apcapabilities.minspeed(A)
    if A._newspeed < minspeed:
        A.logcomment("speed will be below the minimum of %.1f." % minspeed)
    if A._newspeed >= minspeed and A._flighttype == "ST":
        A.logcomment("aircraft will no longer be stalled.")
    elif A._newspeed < minspeed and A._flighttype == "ST":
        A.logcomment("aircraft will still stalled.")
    elif A._newspeed < minspeed:
        A.logcomment("aircraft will have stalled.")

    A.logend("will carry %+.2f APs." % A._apcarry)


################################################################################


def _startmissilespeed(M):

    def attenuationfactor(altitudeband, flightgameturn):
        table = {
            "LO": [0.6, 0.6, 0.7, 0.8, 0.8, 0.8],
            "ML": [0.7, 0.7, 0.7, 0.8, 0.8, 0.8],
            "MH": [0.7, 0.7, 0.7, 0.8, 0.8, 0.9],
            "HI": [0.8, 0.8, 0.8, 0.8, 0.8, 0.9],
            "VH": [0.8, 0.8, 0.8, 0.8, 0.9, 0.9],
            "EH": [0.9, 0.9, 0.9, 0.9, 0.9, 0.9],
            "UH": [1.0, 0.9, 0.9, 0.9, 0.9, 0.9],
        }
        return table[altitudeband][min(flightgameturn, 6) - 1]

    M.logstart("start speed      is %.1f." % M.speed())

    if M.speed() > missilemaxspeed(M.altitudeband()):
        M.logcomment("reducing speed to maximum for altitude band.")
        M.setspeed(_missilemaxspeed(M.altitudeband()))
        M.logstart("start speed      is %.1f." % M.speed())

    if M.speed() < missilemaneuverspeed(M.altitudeband()):
        M.logcomment("cannot maneuver.")

    flightgameturn = apgameturn.gameturn() - M._launchgameturn
    M.logstart("flight game turn is %d." % flightgameturn)

    M._maxfp = int(
        M.speed() * attenuationfactor(M.altitudeband(), flightgameturn) + 0.5
    )
    M._setspeed(M._maxfp)

    M.logstart("average speed    is %.1f." % M.speed())
    if M.speed() < m1speed(M.altitudeband()):
        M.logcomment("speed is subsonic.")
    else:
        M.logcomment("speed is supersonic.")

    M.logcomment("has %d FPs." % M._maxfp)


################################################################################


def _endmissilespeed(M):

    turningfp = -M._turnfacingchanges

    altitudechange = M.altitude() - M.startaltitude()
    if altitudechange >= M._speed:
        altitudefp = -2
    elif altitudechange >= M._speed / 2:
        altitudefp = -1
    elif altitudechange <= -M._speed:
        altitudefp = +2
    elif altitudechange <= -M._speed / 2:
        altitudefp = +1
    else:
        altitudefp = 0

    M.logcomment("turning  FPs = %+.1f." % turningfp)
    M.logcomment("altitude FPs = %+.1f." % altitudefp)

    M._newspeed = M._speed + turningfp + altitudefp

    if M.speed() != M._newspeed:
        M.logcomment("speed will change from %.1f to %.1f." % (M.speed(), M._newspeed))
    else:
        M.logcomment("speed will be unchanged at %.1f." % M._newspeed)
    if M._newspeed < m1speed(M.altitudeband()):
        M.logcomment("speed will be subsonic.")
    else:
        M.logcomment("speed will be supersonic.")


################################################################################
