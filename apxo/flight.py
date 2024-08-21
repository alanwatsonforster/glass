import math
import re

import apxo.aircraftflight as apaircraftflight
import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.gameturn as apgameturn
import apxo.hex as aphex
import apxo.missileflight as apmissileflight
import apxo.speed as apspeed
import apxo.variants as apvariants

from apxo.math import *
from apxo.log import plural

################################################################################


def _move(E, flighttype, power, actions, **kwargs):

    # We save values of these variables at the end of the previous move.

    E._previousflighttype = E._flighttype
    E._previousaltitude = E.altitude()
    E._previousaltitudecarry = E.altitudecarry()
    E._previousspeed = E.speed()
    if E.isaircraft():
        E._previouspowersetting = E._powersetting

    E._flighttype = flighttype

    _checkflighttype(E)

    E._logstart("flight type    is %s." % E._flighttype)
    E._logstart("altitude band  is %s." % E.altitudeband())
    E._logevent("speed of sound is %.1f." % apspeed.m1speed(E.altitudeband()))

    _startspeed(E, power, **kwargs)

    if E._flighttype == "MS":
        apmissileflight._startmove(E, **kwargs)
        apmissileflight._continuemove(E, actions)
    else:
        apaircraftflight._startmove(E, E._flighttype, power, actions, **kwargs)
        apaircraftflight._continuemove(E, actions, True)


def _continuemove(E, actions):

    if E._flighttype == "MS":
        apmissileflight._continuemove(E, actions)
    else:
        apaircraftflight._continuemove(E, actions, False)


################################################################################


def _checkflighttype(E):

    if (
        E._flighttype == "LVL"
        or E._flighttype == "ZC"
        or E._flighttype == "SC"
        or E._flighttype == "VC"
        or E._flighttype == "SD"
        or E._flighttype == "SD/HRD"
        or E._flighttype == "UD"
        or E._flighttype == "VD"
        or E._flighttype == "VD/HRD"
    ):
        _checknormalflight(E)
    elif E._flighttype == "ST":
        _checkstalledflighttype(E)
    elif E._flighttype == "DP":
        return
        _checkdepartedflighttype(E)
    elif E._flighttype == "SP":
        _checkspecialflighttype(E)
    elif E._flighttype == "MS":
        _checkmissileflighttype(E)
    else:
        raise RuntimeError("invalid flight type %r." % E._flighttype)


########################################


def _checknormalflight(E):

    if E.ismissile():
        raise RuntimeError("missiles cannot perform normal flight.")

    if apcapabilities.hasproperty(E, "SPFL"):
        raise RuntimeError("special-flight aircraft cannot perform normal flight.")

    # See rule 13.3.5. A HRD is signalled by appending "/HRD" to the flight type.
    if E._flighttype[-4:] == "/HRD":

        if apcapabilities.hasproperty(E, "NRM"):
            raise RuntimeError("aircraft cannot perform rolling maneuvers.")

        hrd = True
        E._flighttype = E._flighttype[:-4]
        E._flighttype = E._flighttype

        # See rule 7.7.
        if E.altitude() > apcapabilities.ceiling(E):
            E._logevent(
                "check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll."
            )
        elif E.altitudeband() == "EH" or E.altitudeband() == "UH":
            E._logevent(
                "check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll."
                % E.altitudeband()
            )

    else:

        hrd = False

    E._hrd = hrd

    if E._flighttype not in ["LVL", "SC", "ZC", "VC", "SD", "UD", "VD"]:
        raise RuntimeError("invalid flight type %r." % E._flighttype)

    # See rule 13.3.5 for restrictions on HRDs.

    if hrd:
        if E._previousflighttype == "LVL" and E._flighttype == "VD":
            pass
        elif (
            E._previousflighttype == "ZC" or E._previousflighttype == "SC"
        ) and E._flighttype == "VD":
            pass
        elif E._previousflighttype == "VC" and E._flighttype == "SD":
            pass
        else:
            raise RuntimeError(
                "flight type immediately after %s cannot be %s with a HRD."
                % (E._previousflighttype, E._flighttype)
            )

    if E._previousflighttype == "DP":

        # See rule 6.4 on recovering from departed flight.

        if _isclimbingflight(E._flighttype):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )
        elif E._flighttype == "LVL" and not apcapabilities.hasproperty(E, "HPR"):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )

    if E._previousflighttype == "ST":

        # See rule 6.4 on recovering from stalled flight.

        if _isclimbingflight(E._flighttype):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )

    if E._flighttype == "LVL":

        # See rule 8.2.3 on VD recovery.

        if E._previousflighttype == "VD":
            if E.speed() <= 2.0:
                pass
            elif not apcapabilities.hasproperty(E, "HPR"):
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (E._previousflighttype, E._flighttype)
                )
            elif E.speed() >= 3.5:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (for HPR aircraft at high speed)."
                    % (E._previousflighttype, E._flighttype)
                )

    elif E._flighttype == "ZC":

        # See rule 8.2.3 on VD recovery.

        if E._previousflighttype == "VD":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )

    elif E._flighttype == "SC":

        # See rule 8.1.2 on SC prerequsistes.

        if E.speed() < apcapabilities.minspeed(E) + 1:
            raise RuntimeError("insufficient speed for SC.")

        # See rule 8.2.3 on VD recovery.

        if E._previousflighttype == "VD":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )

    elif E._flighttype == "VC":

        # See rule 8.1.3 on VC prerequisites.

        if _isdivingflight(E._previousflighttype):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )
        if E._previousflighttype == "LVL":
            if not apcapabilities.hasproperty(E, "HPR"):
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (E._previousflighttype, E._flighttype)
                )
            elif E.speed() >= 4.0:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (for HPR aircraft at high speed)."
                    % (E._previousflighttype, E._flighttype)
                )

        # See rule 8.2.3 on VD recovery.

        if E._previousflighttype == "VD":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )

    elif E._flighttype == "SD":

        # See rule 8.1.3 on VC restrictions.
        # See rule 13.3.5 on HRD restrictions.

        if E._previousflighttype == "VC" and not (
            apcapabilities.hasproperty(E, "HPR") or hrd
        ):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s (without a HRD)."
                % (E._previousflighttype, E._flighttype)
            )

    elif E._flighttype == "UD":

        # See rule 8.2.2 on VC restrictions.

        if apvariants.withvariant("use version 2.4 rules"):

            # I interpret the text "start from level flight" to mean that the aircraft
            # must have been in level flight on the previous turn.

            if E._previousflighttype != "LVL":
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (E._previousflighttype, E._flighttype)
                )

        else:

            # See rule 8.1.3 on VC restrictions.

            if E._previousflighttype == "VC" and not apcapabilities.hasproperty(
                E, "HPR"
            ):
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (E._previousflighttype, E._flighttype)
                )

    elif E._flighttype == "VD":

        # See rule 8.2.3 (with errata) on VD restrictions.
        # See rule 13.3.5 on HRD restrictions.

        if E._previousflighttype == "LVL":
            if not hrd:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (without a HRD)."
                    % (E._previousflighttype, E._flighttype)
                )
        elif E._previousflighttype == "ZC" or E._previousflighttype == "SC":
            if hrd and E.speed() > 4.0:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (without a low-speed HRD)."
                    % (E._previousflighttype, E._flighttype)
                )
        elif E._previousflighttype == "VC":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )

        # See rule 8.1.3 on VC restrictions. This duplicates the restriction above.

        if E._previousflighttype == "VC":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (E._previousflighttype, E._flighttype)
            )


########################################


def _checkstalledflighttype(E):

    if E.ismissile():
        raise RuntimeError("missiles cannot perform stalled flight.")

    if apcapabilities.hasproperty(E, "SPFL"):
        raise RuntimeError("special-flight aircraft cannot perform stalled flight.")

    # See rule 6.3.

    if E.speed() >= apcapabilities.minspeed(E):
        raise RuntimeError("flight type cannot be ST as aircraft is not stalled.")

    E._logstart("speed is below the minimum of %.1f." % apcapabilities.minspeed(E))
    E._logstart("aircraft is stalled.")


########################################


def _checkdepartedflight(E):

    if E.ismissile():
        raise RuntimeError("missiles cannot perform departed flight.")

    if apcapabilities.hasproperty(E, "SPFL"):
        raise RuntimeError("special-flight aircraft cannot perform departed flight.")


########################################


def _checkspecialflighttype(E):

    if E.ismissile():
        raise RuntimeError("missiles cannot perform special flight.")

    if not apcapabilities.hasproperty(E, "SPFL"):
        raise RuntimeError("normal-flight aircraft cannot perform special flight.")


########################################


def _checkmissileflighttype(E):

    if E.isaircraft():
        raise RuntimeError("aircraft cannot perform missile flight.")


################################################################################


def _startspeed(E, power, **kwargs):

    if E._flighttype == "MS":
        _startspeedmissile(E)
    else:
        _startspeedaircraft(E, power, **kwargs)


########################################


def _startspeedaircraft(A, power, flamedoutengines=None, lowspeedliftdeviceselected=None, speedbrakes=None, **kwargs):

    """
    Carry out the rules to do with power, speed, and speed-induced drag at the
    start of a move.
    """
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


    def reportspeed():
        A._logstart("speed         is %.1f." % speed)
        if speed < apspeed.ltspeed(A.altitudeband()):
            A._logevent("speed is subsonic and below low transsonic.")
        elif speed == apspeed.ltspeed(A.altitudeband()):
            A._logevent("speed is low transonic.")
        elif speed == apspeed.htspeed(A.altitudeband()):
            A._logevent("speed is high transonic.")
        else:
            A._logevent("speed is supersonic.")

    if A._flighttype == "SP":
        speed = power
        reportspeed()
        A._setspeed(speed)
        A._powersetting = ""
        A._powerap = 0
        A._speedap = 0
        return

    ############################################################################

    lastpowersetting = A._previouspowersetting
    speed = A.speed()

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
        if jet and not apcapabilities.hasproperty(A, "HAE"):
            powerapM = max(0.5, twothirdsfromtable(powerapM))
            if powerapAB != None:
                powerapAB = max(0.5, twothirdsfromtable(powerapAB))
    elif A.altitudeband() == "EH" or A.altitudeband() == "UH":
        if jet and not apcapabilities.hasproperty(A, "HAE"):
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
    elif power == "N" or power == 0:
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

    A._logstart("power setting is %s." % powersetting)

    # See rule 8.4. The reduction was done above, but we report it here.
    if (
        jet
        and not apcapabilities.hasproperty(A, "HAE")
        and (
            A.altitudeband() == "VH"
            or A.altitudeband() == "EH"
            or A.altitudeband() == "UH"
        )
    ):
        A._logevent("power is reduced in the %s altitude band." % A.altitudeband())

    # Again, the reduction was done above, but we report it here.
    if apcapabilities.powerfade(A) != None and apcapabilities.powerfade(A) > 0.0:
        A._logevent("power is reduced as the speed is %.1f." % speed)

    # Again, the reduction was done above, but we report it here.
    if A.damageatleast("H"):
        A._logevent("power is reduced as damage is %s." % A.damage())

    # Is the engine smoking?
    A._enginesmoking = apcapabilities.hasproperty(A, "SMP") and powersetting == "M"
    if A._enginesmoking:
        A._logevent("engine is smoking.")

    # See rule 6.7

    flamedoutfraction = flamedoutengines / apcapabilities.engines(A)

    if flamedoutfraction == 1:

        if apcapabilities.engines(A) == 1:
            A._logevent("power setting is treated as I as the engine is flamed-out.")
        else:
            A._logevent(
                "power setting is treated as I as all %d engines are flamed-out."
                % apcapabilities.engines(A)
            )
        powersetting = "I"
        powerap = 0

    elif flamedoutfraction > 0.5:

        A._logevent(
            "maximum power is reduced by one third as %d of the %d engines are flamed-out."
            % (flamedoutengines, apcapabilities.engines(A))
        )
        # 1/3 of APs, quantized in 1/4 units, rounding down.
        powerap = math.floor(powerap / 3 * 4) / 4

    elif flamedoutfraction > 0:

        A._logevent(
            "maximum power is reduced by one half as %d of the %d engines are flamed-out."
            % (flamedoutengines, apcapabilities.engines(A))
        )
        # 1/2 of APs, quantized in 1/4 units, rounding up.
        powerap = math.ceil(powerap / 2 * 4) / 4

    A._logevent("power is %.2f AP." % powerap)

    ############################################################################

    # Warn of the risk of flame-outs.

    # See rules 6.1, 6.7, and 8.5.

    if (
        lastpowersetting == "I"
        and powersetting == "AB"
        and not apcapabilities.hasproperty(A, "RPR")
    ):
        A._logevent(
            "check for flame-out as the power setting has increased from I to AB."
        )

    if powersetting != "I" and A.altitude() > apcapabilities.ceiling(A):
        A._logevent(
            "check for flame-out as the aircraft is above its ceiling and the power setting is %s."
            % powersetting
        )

    if A._flighttype == "DP" and (powersetting == "M" or powersetting == "AB"):
        A._logevent(
            "check for flame-out as the aircraft is in departed flight and the power setting is %s."
            % powersetting
        )

    if speed >= apspeed.m1speed(A.altitudeband()) and (
        powersetting == "I" or powersetting == "N"
    ):
        A._logevent(
            "%s flame-out as the speed is supersonic and the power setting is %s."
            % (plural(apcapabilities.engines(A), "engine", "engines"), powersetting)
        )

    ############################################################################

    # Determine the speed.

    # See rule 6.4 on recovery from departed flight.

    if A._previousflighttype == "DP" and A._flighttype != "DP" and speed < minspeed:
        speed = minspeed
        A._logevent(
            "increasing speed to %.1f after recovering from departed flight." % minspeed
        )

    reportspeed()

    ############################################################################

    # See the "Aircraft Damage Effects" in the Play Aids.

    if speed >= apspeed.m1speed(A.altitudeband()) and A.damageatleast("H"):
        A._logevent(
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
                A._logevent("%s selected." % apcapabilities.lowspeedliftdevicename(A))
            else:
                A._logevent(
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
            A._logevent(
                "insufficient power above cruise speed (%.1f)."
                % apcapabilities.cruisespeed(A)
            )
            speedap -= 1.0

    # See rules 6.1 and 6.6 in version 2.4.

    if powersetting == "I":
        A._logevent("idle power.")
        speedap -= apcapabilities.power(A, "I")
        if speed >= apspeed.m1speed(A.altitudeband()):
            speedap -= 1.0

    # See rule 6.6

    if speed >= apspeed.m1speed(A.altitudeband()):
        if powersetting == "I" or powersetting == "N":
            speedap -= 2.0 * (speed - apspeed.htspeed(A.altitudeband())) / 0.5
            A._logevent(
                "insufficient power at supersonic speed (%.1f or more)."
                % apspeed.m1speed(A.altitudeband())
            )
        elif powersetting == "M":
            speedap -= 1.5 * (speed - apspeed.htspeed(A.altitudeband())) / 0.5
            A._logevent(
                "insufficient power at supersonic speed (%.1f or more)."
                % apspeed.m1speed(A.altitudeband())
            )

    # See rule 6.6

    if apspeed.ltspeed(A.altitudeband()) <= speed and speed <= apspeed.m1speed(A.altitudeband()):
        A._logevent("transonic drag.")
        if speed == apspeed.ltspeed(A.altitudeband()):
            speedap -= 0.5
        elif speed == apspeed.htspeed(A.altitudeband()):
            speedap -= 1.0
        elif speed == apspeed.m1speed(A.altitudeband()):
            speedap -= 1.5
        if apcapabilities.hasproperty(A, "LTD"):
            speedap += 0.5
        elif apcapabilities.hasproperty(A, "HTD"):
            speedap -= 0.5

    ############################################################################

    A._setspeed(speed)
    A._powersetting = powersetting
    A._powerap = powerap
    A._speedap = speedap

    ############################################################################

    # Report fuel.

    if not A._fuel is None:
        if A._bingofuel is None:
            A._logevent("fuel is %.1f." % A._fuel)
        else:
            A._logevent(
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

        if A.speed() >= apspeed.m1speed(A.altitudeband()):
            maxspeedbrakes += 2.0

        if speedbrakes > maxspeedbrakes:
            raise RuntimeError(
                plural(
                    maxspeedbrakes,
                    "speedbrake capability is only 1 DP.",
                    "speedbrake capability is only %.1f DPs." % maxspeedbrakes,
                )
            )
        A._speedbrakeap = -speedbrakes
        A._logevent(
            plural(
                speedbrakes,
                "using speedbrakes for 1 DP.",
                "using speedbrakes for %.1f DPs." % speedbrakes,
            )
        )




########################################


def _startspeedmissile(M):

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

    M._logstart("start speed   is %.1f." % M.speed())

    if M.speed() > apspeed.missilemaxspeed(M.altitudeband()):
        M._logevent("reducing speed to maximum for altitude band.")
        M.setspeed(_missilemaxspeed(M.altitudeband()))
        M._logstart("start speed   is %.1f." % M.speed())

    if M.speed() < apspeed.missilemaneuverspeed(M.altitudeband()):
        M._logevent("cannot maneuver.")

    flightgameturn = apgameturn.gameturn() - M._launchgameturn
    M._logstart("flight game turn is %d." % flightgameturn)

    M._maxfp = int(
        M.speed() * attenuationfactor(M.altitudeband(), flightgameturn) + 0.5
    )
    M._setspeed(M._maxfp)

    M._logstart("average speed is %.1f." % M.speed())
    if M.speed() < apspeed.m1speed(M.altitudeband()):
        M._logevent("speed is subsonic.")
    else:
        M._logevent("speed is supersonic.")

    M._logevent("has %d FPs." % M._maxfp)


################################################################################


def dotasks(E, tasks, actiondispatchlist, start=False, afterFP=None, aftertask=None):
    """
    Carry out flight tasks.
    """

    if start:

        # The number of FPs, HFPs, and VFPs used and the number of FPs lost to
        # speedbrakes. They are used to ensure that the right mix of HFPs and
        # VFPs are used and to determine when the turn ends.

        E._fp = 0
        E._hfp = 0
        E._vfp = 0

        # The number of unloaded HFPs and the indices of the first and last
        # unloaded HFPs in an UD. They are then used to ensure that the
        # unloaded HFPs are continuous.

        E._unloadedhfp = 0
        E._firstunloadedfp = None
        E._lastunloadedfp = None

        # Whether the aircraft has used a superclimb (C3).
        E._usedsuperclimb = False

        # The aircraft being tracked and the number of FPs expended
        # while tracking.

        E._tracking = None
        E._trackingfp = 0

        # This keeps track of the number of turns, rolls, and vertical rolls.

        E._turnmaneuvers = 0
        E._rollmaneuvers = 0
        E._verticalrolls = 0

        # The number of slides performed and the FP of the last one performed.

        E._slides = 0
        E._slidefp = 0

        # Whether flight is currently supersonic.
        E._supersonic = E.speed() >= apspeed.m1speed(E.altitudeband())

    if tasks != "":
        for task in re.split(r"[, ]", tasks):
            if not E.killed() and not E.removed():
                dotask(E, task, actiondispatchlist, afterFP, aftertask)


################################################################################


def dotask(E, task, actiondispatchlist, afterFP, aftertask):
    """
    Carry out a flight task.
    """

    E._log1("FP %d" % (E._fp + 1), task)

    # Check we have at least one FP remaining.
    if E._fp + 1 > E._maxfp:
        raise RuntimeError(
            plural(
                E._maxfp,
                "only 1 FP is available",
                "only %.1f FPs are available." % E._maxfp,
            )
        )

    # Determine if this FP is the last FP of the move.
    E._lastfp = E._fp + 2 > E._maxfp

    E._taskaltitude = E.altitude()
    E._taskaltitudeband = E.altitudeband()

    try:

        remainingtask = task

        remainingtask = doactions(
            E, remainingtask, actiondispatchlist, "maneuvering departure"
        )
        if remainingtask != task:

            E._maneuveringdeparture = True

            assert aphex.isvalid(E.x(), E.y(), facing=E.facing())
            assert apaltitude.isvalidaltitude(E.altitude())

            E._logposition("end")

            return

        E._horizontal = False
        E._vertical = False

        E._hasunloaded = False
        E._hasdeclaredamaneuver = False
        E._hasmaneuvered = False
        E._hasrolled = False
        E._hasbanked = False

        remainingtask = doactions(E, remainingtask, actiondispatchlist, "prolog")

        fp = E._fp
        remainingtask = doactions(E, remainingtask, actiondispatchlist, "FP")
        if E._fp == fp:
            raise RuntimeError(
                "%r is not a valid task as it does not expend an FP." % task
            )
        elif E._fp > fp + 1:
            raise RuntimeError(
                "%r is not a valid task as it attempts to expend more than one FP."
                % task
            )

        # We save maneuvertype, as E._maneuvertype may be set to None of the
        # maneuver is completed below.

        E._taskmaneuvertype = E._maneuvertype
        E._hasturned = _isturn(E._maneuvertype)
        E._hasrolled = _isroll(E._maneuvertype)
        E._hasslid = _isslide(E._maneuvertype)

        # See rule 8.2.2 and 13.1.
        if not E._hasunloaded:
            if E._hasturned:
                E._maneuverfp += 1
            elif E._maneuvertype == "VR" and E._vertical:
                E._maneuverfp += 1
            elif E._maneuvertype == "DR" or E._maneuvertype == "LR":
                E._maneuverfp += 1
            elif E._horizontal:
                E._maneuverfp += 1

        if E._hasturned and E._maneuversupersonic:
            E._turningsupersonic = True

        if afterFP is not None:
            afterFP(E)

        remainingtask = doactions(E, remainingtask, actiondispatchlist, "epilog")

        if E._hasbanked and E._hasmaneuvered and not E._hasrolled:
            raise RuntimeError(
                "attempt to bank immediately after a maneuver that is not a roll."
            )

        if remainingtask != "":
            raise RuntimeError("%r is not a valid task." % task)

        assert aphex.isvalid(E.x(), E.y(), facing=E.facing())
        assert apaltitude.isvalidaltitude(E.altitude())

    except RuntimeError as e:

        raise e

    finally:
        if E._lastfp:
            E._logpositionandmaneuver("end")
        else:
            E._logpositionandmaneuver("")
        E._extendpath()

    if E._taskaltitudeband != E.altitudeband():
        E._logevent(
            "altitude band changed from %s to %s."
            % (E._taskaltitudeband, E.altitudeband())
        )
        E._logevent("speed of sound is %.1f." % apspeed.m1speed(E.altitudeband()))
        previoussupersonic = E._supersonic
        E._supersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
        if previoussupersonic and not E._supersonic:
            E._logevent("speed is now subsonic.")
        elif not previoussupersonic and E._supersonic:
            E._logevent("speed is now supersonic.")

    if E.killed() or E.removed():
        return

    E._checkforterraincollision()
    E._checkforleavingmap()

    if aftertask is not None:
        aftertask(E)


################################################################################


def doactions(E, task, actiondispatchlist, selectedactiontype):
    """
    Carry out the actions in an task that match the action type.
    """

    while task != "":

        actioncode = task.split("/", maxsplit=1)[0]

        for action in actiondispatchlist:

            actiontype = action[1]
            actionprocedure = action[2]

            if actioncode == action[0]:
                break

        if selectedactiontype == "prolog" and actiontype == "epilog":
            raise RuntimeError("unexpected %s action in task prolog." % actioncode)
        if selectedactiontype == "epilog" and actiontype == "prolog":
            raise RuntimeError("unexpected %s action in task epilog." % actioncode)

        if selectedactiontype != actiontype:
            break

        if actionprocedure is None:
            break

        task = "/".join(task.split("/")[1:])

        actionprocedure(E)

    return task


################################################################################


def _isturn(maneuvertype):
    """
    Return True if the maneuver type is a turn. Otherwise False.
    """

    return maneuvertype in ["EZ", "TT", "HT", "BT", "ET"]


def _isroll(maneuvertype):
    """
    Return True if the maneuver type is a roll. Otherwise False.
    """

    return maneuvertype in ["VR", "DR", "LR", "BR"]


def _isslide(maneuvertype):
    """
    Return True if the maneuver type is a slide. Otherwise False.
    """

    return maneuvertype == "SL"


def _isdivingflight(flighttype, vertical=False):
    """
    Return True if the flight type is SD, UD, or VD. Otherwise return False.
    """

    if vertical:
        return flighttype == "VD"
    else:
        return flighttype == "SD" or flighttype == "UD" or flighttype == "VD"


def _isclimbingflight(flighttype, vertical=False):
    """
    Return True if the flight type is ZC, SC, or VC. Otherwise return False.
    """

    if vertical:
        return flighttype == "VC"
    else:
        return flighttype == "ZC" or flighttype == "SC" or flighttype == "VC"


def _islevelflight(flighttype):
    """
    Return True if the flight type is LVL. Otherwise return False.
    """

    return flighttype == "LVL"


################################################################################


