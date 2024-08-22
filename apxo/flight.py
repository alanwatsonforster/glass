import math
import re

import apxo.aircraftflight as apaircraftflight
import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.departedflight as apdepartedflight
import apxo.gameturn as apgameturn
import apxo.hex as aphex
import apxo.missileflight as apmissileflight
import apxo.speed as apspeed
import apxo.stalledflight as apstalledflight
import apxo.turnrate as apturnrate
import apxo.variants as apvariants

from apxo.math import *
from apxo.log import plural

################################################################################


def _move(E, flighttype, power, moves, **kwargs):

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

    if E.isaircraft():
        apspeed._startaircraftspeed(E, power, **kwargs)
    else:
        apspeed._startmissilespeed(E)

    _startmove(E)

    E._logposition("start")

    _continuemove(E, moves)


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


def _startmove(E, **kwargs):

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

    if E.ismissile():
        _startmovemissile(E)
    else:
        _startmoveaircraft(E)


########################################


def _startmovemissile(M, **kwargs):

    pass


########################################


def _startmoveaircraft(A):

    # This flags whether a maneuvering departure has occured.

    A._maneuveringdeparture = False

    A._logstart("configuration is %s." % A._configuration)
    A._logstart("damage        is %s." % A.damage())

    if A._flighttype == "ST":
        _startmovestalledflight(A)
    elif A._flighttype == "DP":
        _startmovedepartedflight(A)
    elif A._flighttype == "SP":
        _startmovespecialflight(A)
    else:
        _startmovenormalflight(A)


########################################


def _startmovestalledflight(A):

    A._fpcarry = 0
    A._setaltitudecarry(0)

    # See rule 6.4.
    A._logevent("is carrying %+.2f APs." % A._apcarry)


########################################


def _startmovedepartedflight(A):

    A._fpcarry = 0
    A._apcarry = 0
    A._setaltitudecarry(0)


########################################


def _startmovespecialflight(A):

    A._fpcarry = 0
    A._apcarry = 0
    A._turnsstalled = 0
    A._turnsdeparted = 0

    A._maxfp = A.speed()
    A._logevent("has %.1f FPs." % A._maxfp)

    A._effectiveclimbcapability = apcapabilities.specialclimbcapability(A)
    A._logevent("effective climb capability is %.2f." % A._effectiveclimbcapability)


########################################


def _startmovenormalflight(A):

    ########################################

    def reportapcarry():
        A._logevent("is carrying %+.2f APs." % A._apcarry)

    ########################################

    def reportaltitudecarry():
        if A._altitudecarry != 0:
            A._logevent("is carrying %.2f altitude levels." % A._altitudecarry)

    ########################################

    def determineallowedturnrates():
        """
        Determine the allowed turn rates according to the flight type and
        speed. The aircraft type and configuration may impose additional
        restrictions.
        """

        turnrates = ["EZ", "TT", "HT", "BT", "ET"]

        # See "Aircraft Damage Effects" in Play Aids.

        if A.damageatleast("C"):
            A._logevent("damage limits the turn rate to TT.")
            turnrates = turnrates[:2]
        elif A.damageatleast("2L"):
            A._logevent("damage limits the turn rate to HT.")
            turnrates = turnrates[:3]
        elif A.damageatleast("L"):
            A._logevent("damage limits the turn rate to BT.")
            turnrates = turnrates[:4]

        # See rule 7.5.

        minspeed = apcapabilities.minspeed(A)
        if A.speed() == minspeed:
            A._logevent("speed limits the turn rate to EZ.")
            turnrates = turnrates[:1]
        elif A.speed() == minspeed + 0.5:
            A._logevent("speed limits the turn rate to TT.")
            turnrates = turnrates[:2]
        elif A.speed() == minspeed + 1.0:
            A._logevent("speed limits the turn rate to HT.")
            turnrates = turnrates[:3]
        elif A.speed() == minspeed + 1.5:
            A._logevent("speed limits the turn rate to BT.")
            turnrates = turnrates[:4]
        else:
            A._logevent("speed does not limit the turn rate.")

        # See rule 8.1.1.

        if A._flighttype == "ZC":
            A._logevent("ZC limits the turn rate to BT.")
            turnrates = turnrates[:4]

        # See rule 8.1.1.

        if A._flighttype == "SC":
            A._logevent("SC limits the turn rate to EZ.")
            turnrates = turnrates[:1]

        # See rule 8.1.3.

        if A._flighttype == "VC":
            A._logevent("VC disallows all turns.")
            turnrates = []

        A._allowedturnrates = turnrates

    ########################################

    def checkcloseformationlimits():

        if A.closeformationsize() == 0:
            return

        # See rule 13.7, interpreted in the same sense as rule 7.8.
        if A._hrd:
            A._logevent("close formation breaks down upon a HRD.")
            apcloseformation.breakdown(A)

        # See rule 8.6.
        if (
            A._flighttype == "ZC"
            or (A._flighttype == "SC" and A._powersetting == "AB")
            or A._flighttype == "VC"
            or A._flighttype == "UD"
            or A._flighttype == "VD"
        ):
            A._logevent(
                "close formation breaks down as the flight type is %s." % A._flighttype
            )
            apcloseformation.breakdown(A)

        return

    ########################################

    def determinemaxfp():
        """
        Determine the number of FPs available, according to the speed and any
        carried FPs.
        """

        # See rule 5.4.

        A._maxfp = int(A.speed() + A._fpcarry)
        A._logevent("has %d FPs (including %.1f carry)." % (A._maxfp, A._fpcarry))
        A._fpcarry = (A.speed() + A._fpcarry) - A._maxfp

    ########################################

    def determinefprequirements():
        """
        Determine the requirements on the use of FPs.
        """

        # See rule 5.5.
        # See rule 13.3.5 (with errata) on HRD restrictions.

        if (
            A._previousflighttype == "ZC" or A._previousflighttype == "SC"
        ) and A._flighttype == "VD":
            assert A._hrd
            mininitialhfp = A.speed() // 3
        elif A._previousflighttype == "LVL" and (
            _isclimbingflight(A._flighttype) or _isdivingflight(A._flighttype)
        ):
            mininitialhfp = 1
        elif (
            _isclimbingflight(A._previousflighttype) and _isdivingflight(A._flighttype)
        ) or (
            _isdivingflight(A._previousflighttype) and _isclimbingflight(A._flighttype)
        ):
            if apcapabilities.hasproperty(A, "HPR"):
                mininitialhfp = A.speed() // 3
            else:
                mininitialhfp = A.speed() // 2
        else:
            mininitialhfp = 0

        minhfp = 0
        maxhfp = A._maxfp
        minvfp = 0
        maxvfp = A._maxfp
        minunloadedhfp = 0
        maxunloadedhfp = 0

        # The comments below about "see the blue sheet" refer to the VFP
        # requirements for SD, SC, and ZC, which do not appear in the rules
        # but which do appear on the blue "Flight Rules Summary" sheet.
        # Actually, there is no requirement for SCs even here, but we assume
        # that at least one VFP must be used in this case too.

        if A._flighttype == "LVL":

            # See rule 5.3.
            maxvfp = 0

        elif A._flighttype == "ZC":

            # See blue sheet.
            minvfp = 1

            # See rules 8.1.1.
            minhfp = rounddown(onethirdfromtable(A._maxfp))

        elif A._flighttype == "SC":

            # See blue sheet.
            minvfp = 1

            # See rule 8.1.2.
            if A.speed() < apcapabilities.minspeed(A) + 1.0:
                raise RuntimeError("insufficient speed for SC.")
            climbcapability = apcapabilities.climbcapability(A)
            if A.speed() < apcapabilities.climbspeed(A):
                climbcapability /= 2
            if climbcapability < 1:
                maxvfp = 1
            else:
                maxvfp = rounddown(twothirdsfromtable(A._maxfp))

        elif A._flighttype == "VC" or A._flighttype == "VD":

            # See blue sheet.
            minvfp = 1

            # See rules 8.1.3 and 8.2.3.
            if A._previousflighttype != A._flighttype:
                minhfp = rounddown(onethirdfromtable(A._maxfp))
                maxhfp = minhfp
            else:
                maxhfp = rounddown(onethirdfromtable(A._maxfp))

        elif A._flighttype == "SD":

            # See blue sheet.
            minvfp = 1

            # See rules 8.2.1 and 8.2.3.
            if A._previousflighttype == "VD":
                if apcapabilities.hasproperty(A, "HPR"):
                    minvfp = rounddown(onethirdfromtable(A._maxfp))
                else:
                    minvfp = rounddown(A._maxfp / 2)
            minhfp = rounddown(onethirdfromtable(A._maxfp))

        elif A._flighttype == "UD":

            # See rules 8.2.2.
            maxvfp = 0
            minunloadedhfp = 1
            maxunloadedhfp = A._maxfp

        minhfp = max(minhfp, mininitialhfp)

        if maxvfp == 0:

            A._logevent("all FPs must be HFPs.")

        else:

            if mininitialhfp == 1:
                A._logevent("the first FP must be an HFP.")
            elif mininitialhfp > 1:
                A._logevent("the first %d FPs must be HFPs." % mininitialhfp)

            if minhfp == maxhfp:
                A._logevent(
                    plural(
                        minhfp,
                        "exactly 1 FP must be an HFP.",
                        "exactly %d FPs must be HFPs." % minhfp,
                    )
                )
            elif minhfp > 0 and maxhfp < A._maxfp:
                A._logevent("between %d and %d FP must be HFPs." % (minhfp, maxhfp))
            elif minhfp > 0:
                A._logevent(
                    plural(
                        minhfp,
                        "at least 1 FP must be an HFP.",
                        "at least %d FPs must be HFPs." % minhfp,
                    )
                )
            else:
                A._logevent(
                    plural(
                        maxhfp,
                        "at most 1 FP may be an HFP.",
                        "at most %d FPs may be HFPs." % maxhfp,
                    )
                )

            if minvfp == maxvfp:
                A._logevent(
                    plural(
                        minvfp,
                        "exactly 1 FP must be a VFP.",
                        "exactly %d FPs must be VFPs." % minvfp,
                    )
                )
            elif minvfp > 0 and maxvfp < A._maxfp:
                A._logevent("between %d and %d FP must be VFPs." % (minvfp, maxvfp))
            elif minvfp > 0:
                A._logevent(
                    plural(
                        minvfp,
                        "at least 1 FP must be a VFP.",
                        "at least %d FPs must be VFPs." % minvfp,
                    )
                )
            else:
                A._logevent(
                    plural(
                        maxvfp,
                        "at most 1 FP may be a VFP.",
                        "at most %d FPs may be VFPs." % maxvfp,
                    )
                )

        if minhfp > maxhfp:
            raise RuntimeError("flight type not permitted by HFP requirements.")
        if minvfp > maxvfp:
            raise RuntimeError("flight type not permitted by VFP requirements.")

        if minunloadedhfp > 0:
            A._logevent(
                plural(
                    minunloadedhfp,
                    "at least 1 FP must be an unloaded HFP.",
                    "at least %d FPs must be unloaded HFPs." % minunloadedhfp,
                )
            )

        A._mininitialhfp = mininitialhfp
        A._minhfp = minhfp
        A._maxhfp = maxhfp
        A._minvfp = minvfp
        A._maxvfp = maxvfp
        A._minunloadedhfp = minunloadedhfp
        A._maxunloadedhfp = maxunloadedhfp

    ########################################

    def handlecarriedturn():
        """
        Handle any carried turn.
        """

        if _isturn(A._maneuvertype):

            # See rule 7.7.

            # Issue: The consequences of carried turn violating the turn
            # requirements of ZC, SC, and VC flight are not clear, but for the
            # moment we assume they result in a maneuvering departure.

            turnrequirement = apturnrate.turnrequirement(
                A.altitudeband(), A.speed(), A._maneuvertype
            )
            if not A._maneuvertype in A._allowedturnrates or turnrequirement == None:
                A._logevent(
                    "carried turn rate is tighter than the maximum allowed turn rate."
                )
                raise RuntimeError(
                    "aircraft has entered departed flight while maneuvering."
                )

            # See rule 7.1.

            previousmaneuverrequiredfp = A._maneuverrequiredfp
            previous_maneuverfacingchange = A._maneuverfacingchange

            A._maneuversupersonic = A.speed() >= apspeed.m1speed(A.altitudeband())
            turnrequirement = apturnrate.turnrequirement(
                A.altitudeband(), A.speed(), A._maneuvertype
            )
            if turnrequirement >= 60:
                A._maneuverrequiredfp = 1
                A._maneuverfacingchange = turnrequirement
            else:
                A._maneuverrequiredfp = turnrequirement
                A._maneuverfacingchange = 30

            if (
                A._maneuverrequiredfp != previousmaneuverrequiredfp
                or A._maneuverfacingchange != previous_maneuverfacingchange
            ):
                if A._maneuverfacingchange > 30:
                    A._logevent(
                        "turn requirement changed to %d in 1 FP."
                        % A._maneuverfacingchange
                    )
                else:
                    A._logevent(
                        "turn requirement changed to %s."
                        % plural(
                            A._maneuverrequiredfp,
                            "1 FP",
                            "%d FPs" % A._maneuverrequiredfp,
                        )
                    )

            A._maxturnrate = A._maneuvertype
            A._turningsupersonic = A._maneuversupersonic

        else:

            A._maxturnrate = None
            A._turningsupersonic = False

    ########################################

    def determineeffectiveclimbcapability():

        if _isclimbingflight(A._flighttype):

            A._effectiveclimbcapability = apcapabilities.climbcapability(A)

            # See rule 4.3 and 8.1.2.
            if A._flighttype == "SC" and A.speed() < apcapabilities.climbspeed(A):
                A._logevent("climb capability reduced in SC below climb speed.")
                A._effectiveclimbcapability *= 0.5

            # See the Aircraft Damage Effects Table in the charts.
            if A.damageatleast("H"):
                A._logevent("climb capability reduced by damage.")
                A._effectiveclimbcapability *= 0.5

            # See rule 6.6 and rule 8.1.4.
            if A.speed() >= apspeed.m1speed(A.altitudeband()):
                A._logevent("climb capability reduced at supersonic speed.")
                A._effectiveclimbcapability *= 2 / 3

            A._logevent(
                "effective climb capability is %.2f." % A._effectiveclimbcapability
            )

        else:

            A._effectiveclimbcapability = None

    ########################################

    # See rule 8.1.4 on altitude carry.
    if not A.isinclimbingflight():
        A._setaltitudecarry(0)

    A._turnsstalled = 0
    A._turnsdeparted = 0

    reportapcarry()
    reportaltitudecarry()
    determineallowedturnrates()
    handlecarriedturn()
    checkcloseformationlimits()
    determinemaxfp()
    determinefprequirements()
    determineeffectiveclimbcapability()


###############################################################################


def _continuemove(E, moves):

    if E._flighttype == "MS":
        _continuemissilemove(E, moves)
    elif E._flighttype == "ST":
        _continuestalledflight(E, moves)
    elif E._flighttype == "DP":
        _continuedepartedflight(E, moves)
    elif E._flighttype == "SP":
        _continuespecialflight(E, moves)
    else:
        _continuenormalflight(E, moves)

    if E._finishedmoving:
        _endmove(E)


########################################


def _continuemissilemove(M, moves):
    apmissileflight._continuemove(M, moves)


########################################


def _continuestalledflight(A, moves):
    apstalledflight.doflight(A, moves)


########################################


def _continuedepartedflight(A, moves):
    apdepartedflight.doflight(A, moves)


########################################


def _continuespecialflight(A, moves):
    apaircraftflight.continuespecialflight(A, moves)


########################################


def _continuenormalflight(A, moves):
    apaircraftflight.continuenormalflight(A, moves)


###############################################################################


def _endmove(E):

    if E.killed():
        E._logend("has been killed.")
        return

    if E._flighttype == "MS":
        _endmissileflight(E)
    else:
        if E._flighttype == "ST":
            _endstalledflight(E)
        elif E._flighttype == "DP":
            _enddepartedflight(E)
        elif E._flighttype == "SP":
            _endspecialflight(E)
        else:
            _endnormalflight(E)
        apspeed._endaircraftspeed(E)


########################################


def _endmissileflight(M):
    apspeed._endmissilespeed(M)


########################################


def _endstalledflight(A):
    A._turnsstalled += 1


########################################


def _enddepartedflight(A):
    A._turnsdeparted += 1


########################################


def _endspecialflight(A):
    pass


########################################


def _endnormalflight(A):

    ########################################

    def reportfp():
        A._logevent(
            "used %s and %s."
            % (
                plural(A._hfp, "1 HFP", "%d HFPs" % A._hfp),
                plural(A._vfp, "1 VFP", "%d VFPs" % A._vfp),
            )
        )
        A._logevent("will carry %.1f FPs." % A._fpcarry)

    ########################################

    def checkfp():

        if A._hfp < A._minhfp:
            raise RuntimeError("too few HFPs.")

        if A._hfp > A._maxhfp:
            raise RuntimeError("too many HFPs.")

        if A._vfp < A._minvfp:
            raise RuntimeError("too few VFPs.")

        if A._vfp > A._maxvfp:
            raise RuntimeError("too many VFPs.")

        if A._flighttype == "UD":
            # See rule 8.2.2.
            if A._firstunloadedfp == None:
                n = 0
            else:
                n = A._lastunloadedfp - A._firstunloadedfp + 1
            if A._unloadedhfp != n:
                raise RuntimeError("unloaded HFPs must be continuous.")
            if A._unloadedhfp < A._minunloadedhfp:
                raise RuntimeError("too few unloaded HFPs.")
            if A._unloadedhfp > A._maxunloadedhfp:
                raise RuntimeError("too many unloaded HFPs.")

    ########################################

    def checkfreedescent():

        # See rule 8.2.4.

        if A._flighttype == "LVL":
            altitudechange = A.altitude() - A._previousaltitude
            if altitudechange < -1:
                raise RuntimeError("free descent cannot only be taken once per move.")

    ########################################

    def reportgloccycle():

        # See rule 7.6.
        if A._gloccheck > 0 and A._maxturnrate != "ET" and A._maxturnrate != "BT":
            A._logevent("GLOC cycle ended.")
            A._gloccheck = 0

    ########################################

    def reportcarry():

        if A._altitudecarry != 0:
            A._logevent("is carrying %.2f altitude levels." % A._altitudecarry)

    ########################################

    def determinemaxturnrateap():
        """
        Determine the APs from the maximum turn rate used.
        """

        if apvariants.withvariant("use house rules"):
            pass
        else:

            if A._maxturnrate != None:
                A._turnrateap = -apcapabilities.turndrag(A, A._maxturnrate)
            else:
                A._turnrateap = 0

            if A._turningsupersonic:
                if apcapabilities.hasproperty(A, "PSSM"):
                    A._turnrateap -= 2.0
                elif not apcapabilities.hasproperty(A, "GSSM"):
                    A._turnrateap -= 1.0

    ########################################

    def determinealtitudeap():

        altitudechange = A.altitude() - A._previousaltitude

        if A._flighttype == "ZC":

            # See rule 8.1.1.
            altitudeap = -1.0 * altitudechange

        elif A._flighttype == "SC":

            if altitudechange == 0:

                altitudeap = 0.0
                A._scwithzccomponent = False

            else:

                # See rule 8.1.2 and 8.1.4.

                climbcapability = A._effectiveclimbcapability

                # We need to figure out how much was climbed at the SC rate and
                # how much was climbed at the ZC rate. This is complicated since
                # altitudechange can be more than the climbcapability because of
                # altitudecarry. Therefore, we calculate how much was at the ZC
                # rate from the true altitude change, including carry, and then
                # assume that any difference was at the SC rate.
                #
                # We also use that the altitude change at the ZC rate must be an
                # integral number of levels.

                truealtitude = A.altitude() + A._altitudecarry
                lasttruealtitude = A._previousaltitude + A._previousaltitudecarry

                truealtitudechange = truealtitude - lasttruealtitude

                scaltitudechange = min(truealtitudechange, climbcapability)
                zcaltitudechange = int(truealtitudechange - scaltitudechange + 0.5)
                scaltitudechange = altitudechange - zcaltitudechange

                altitudeap = -0.5 * scaltitudechange + -1.0 * zcaltitudechange

                A._scwithzccomponent = zcaltitudechange != 0

        elif A._flighttype == "VC":

            # See rule 8.1.3.
            altitudeap = -1.5 * altitudechange

        elif A._flighttype == "SD":

            # See rule 8.2.1.
            altitudeap = -1.0 * altitudechange

        elif A._flighttype == "UD":

            # See rule 8.2.2.
            altitudeap = -1.0 * altitudechange

        elif A._flighttype == "VD":

            # See rule 8.2.3
            altitudeap = -1.0 * altitudechange

        elif A._flighttype == "LVL":

            # See rule 8.2.4.
            altitudeap = 0

        # Round to nearest quarter. See rule 6.2.
        altitudeap = roundtoquarter(altitudeap)

        A._altitudeap = altitudeap

    ########################################

    def checkcloseformationlimits():

        if A.closeformationsize() == 0:
            return

        # See rule 8.6. The other climbing and diving cases are handled at
        # the start of the move.

        altitudeloss = A._previousaltitude - A.altitude()
        if A._flighttype == "SD" and altitudeloss > 2:
            A._logevent(
                "close formation breaks down as the aircraft lost %d levels in an SD."
                % altitudeloss
            )
            apcloseformation.breakdown(A)
        elif A._flighttype == "SC" and A._scwithzccomponent:
            A._logevent(
                "close formation breaks down as the aircraft climbed faster than the sustained climb rate."
            )
            apcloseformation.breakdown(A)

    ########################################

    def handleunloadeddiveflighttype():

        if A._flighttype == "UD":
            # See rule 8.2.2.
            altitudechange = A.altitude() - A._previousaltitude
            if altitudechange == -2:
                A._logevent("UD ends as flight type SD.")
                A._flighttype = "SD"

    ########################################

    if not A._maneuveringdeparture:
        reportfp()
        checkfp()
        checkfreedescent()
        reportcarry()
        reportgloccycle()
        determinemaxturnrateap()
        determinealtitudeap()
        checkcloseformationlimits()
        handleunloadeddiveflighttype()

    A._finishedmoving = True


###############################################################################


def domoves(E, moves, actiondispatchlist):
    """
    Carry out flight moves.
    """

    if moves == "":
        return

    for move in re.split(r"[, ]", moves):
        if not E.killed():
            domove(E, move, actiondispatchlist)


################################################################################


def domove(E, move, actiondispatchlist):
    """
    Carry out a flight move.
    """

    ####################

    def doactions(E, actions, selectedactiontype):
        """
        Carry out the actions in an move that match the action type.
        """

        while actions != []:

            actioncode = actions[0]

            for action in actiondispatchlist:

                actiontype = action[1]
                actionprocedure = action[2]

                if actioncode == action[0]:
                    break

            if selectedactiontype == "prolog" and actiontype == "epilog":
                raise RuntimeError(
                    "unexpected %s action in prolog of %r." % (actioncode, move)
                )
            if selectedactiontype == "epilog" and actiontype == "prolog":
                raise RuntimeError(
                    "unexpected %s action in epilog of %r." % (actioncode, move)
                )

            if selectedactiontype != actiontype:
                break

            if actionprocedure is None:
                break

            actions = actions[1:]

            actionprocedure(E)

        return actions

    ####################

    E._log1("FP %d" % (E._fp + 1), move)

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

    E._movestartaltitude = E.altitude()
    E._movestartaltitudeband = E.altitudeband()

    try:

        actions = move.split("/")
        remainingactions = actions

        remainingactions = doactions(E, remainingactions, "maneuvering departure")
        if remainingactions != actions:

            if remainingactions != []:
                raise RuntimeError("%r is not a valid move." % move)

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

        remainingactions = doactions(E, remainingactions, "prolog")

        fp = E._fp
        remainingactions = doactions(E, remainingactions, "FP")
        if E._fp == fp:
            raise RuntimeError(
                "%r is not a valid move as it does not expend an FP." % move
            )
        elif E._fp > fp + 1:
            raise RuntimeError(
                "%r is not a valid move as it attempts to expend more than one FP."
                % move
            )

        # We save maneuvertype, as E._maneuvertype may be set to None of the
        # maneuver is completed below.

        E._movemaneuvertype = E._maneuvertype
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

        if E.isaircraft():
            _checkrecovery(E)
            _checktracking(E)
            _checkmaneuveringdeparture(E)
            _checkgloc(E)
            _checkcloseformation(E)

        remainingactions = doactions(E, remainingactions, "epilog")

        if E._hasbanked and E._hasmaneuvered and not E._hasrolled:
            raise RuntimeError(
                "attempt to bank immediately after a maneuver that is not a roll."
            )

        if remainingactions != []:
            raise RuntimeError("%r is not a valid move." % move)

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

    if E._movestartaltitudeband != E.altitudeband():
        E._logevent(
            "altitude band changed from %s to %s."
            % (E._movestartaltitudeband, E.altitudeband())
        )
        E._logevent("speed of sound is %.1f." % apspeed.m1speed(E.altitudeband()))
        previoussupersonic = E._supersonic
        E._supersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
        if previoussupersonic and not E._supersonic:
            E._logevent("speed is now subsonic.")
        elif not previoussupersonic and E._supersonic:
            E._logevent("speed is now supersonic.")

    E._checkforterraincollision()
    if E.killed():
        return

    E._checkforleavingmap()

################################################################################


def _checkrecovery(A):

    # Check recovery. See rules 9.1 and 13.3.6. The +1 is because the recovery period is
    # this turn plus half of the speed, rounding down.

    if A._hasunloaded:
        A._unloadedrecoveryfp = int(A.speed() / 2) + 1
        A._ETrecoveryfp -= 1
        A._BTrecoveryfp = -1
        A._rollrecoveryfp = -1
        A._HTrecoveryfp = -1
        A._TTrecoveryfp = -1
    elif A._maneuvertype == "ET":
        A._unloadedrecoveryfp = -1
        A._ETrecoveryfp = int(A.speed() / 2) + 1
        A._BTrecoveryfp = -1
        A._rollrecoveryfp = -1
        A._HTrecoveryfp = -1
        A._TTrecoveryfp = -1
    elif A._maneuvertype == "BT":
        A._unloadedrecoveryfp -= 1
        A._ETrecoveryfp -= 1
        A._BTrecoveryfp = int(A.speed() / 2) + 1
        A._rollrecoveryfp = -1
        A._HTrecoveryfp = -1
        A._TTrecoveryfp = -1
    elif A._maneuvertype in ["VR", "LR", "DR"] or (A._hrd and A._fp == 1):
        A._unloadedrecoveryfp -= 1
        A._ETrecoveryfp -= 1
        A._BTrecoveryfp = -1
        A._rollrecoveryfp = int(A.speed() / 2) + 1
        A._HTrecoveryfp = -1
        A._TTrecoveryfp = -1
    elif A._maneuvertype == "HT":
        A._unloadedrecoveryfp -= 1
        A._ETrecoveryfp -= 1
        A._BTrecoveryfp -= 1
        A._rollrecoveryfp -= 1
        A._HTrecoveryfp = int(A.speed() / 2) + 1
        A._TTrecoveryfp = -1
    elif A._maneuvertype == "TT":
        A._unloadedrecoveryfp -= 1
        A._ETrecoveryfp -= 1
        A._BTrecoveryfp -= 1
        A._rollrecoveryfp -= 1
        A._HTrecoveryfp -= 1
        A._TTrecoveryfp = int(A.speed() / 2) + 1
        A._unloadedrecoveryfp -= 1
    else:
        A._unloadedrecoveryfp -= 1
        A._ETrecoveryfp -= 1
        A._BTrecoveryfp -= 1
        A._rollrecoveryfp -= 1
        A._HTrecoveryfp -= 1
        A._TTrecoveryfp -= 1

    if A._ETrecoveryfp == 0:
        A._logevent("recovered from ET.")
    if A._BTrecoveryfp == 0:
        A._logevent("recovered from BT.")
    if A._rollrecoveryfp == 0:
        A._logevent("recovered from roll.")
    if A._HTrecoveryfp == 0:
        A._logevent("recovered from HT.")
    if A._TTrecoveryfp == 0:
        A._logevent("recovered from TT.")


def _checktracking(A):

    # Check tracking. See rule 9.4.
    if A._tracking:
        if useofweaponsforbidden(A):
            A._logevent("stopped SSGT.")
            A._tracking = None
            A._trackingfp = 0
        elif apairtoair.trackingforbidden(A, A._tracking):
            A._logevent(
                "stopped SSGT as %s" % apairtoair.trackingforbidden(A, A._tracking)
            )
            A._tracking = None
            A._trackingfp = 0
        else:
            A._trackingfp += 1

def _checkmaneuveringdeparture(A):

        # See rules 7.7 and 8.5.
        if A._hasmaneuvered and A._hasrolled:
            if A._movestartaltitude > apcapabilities.ceiling(A):
                A._logevent(
                    "check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll."
                )
            elif A._movestartaltitudeband == "EH" or A._movestartaltitudeband == "UH":
                A._logevent(
                    "check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll."
                    % A._movestartaltitudeband
                )

        # See rules 7.7 and 8.5.
        if A._hasmaneuvered and A._hasturned:
            if (
                A._movestartaltitude > apcapabilities.ceiling(A)
                and A._movemaneuvertype != "EZ"
            ):
                A._logevent(
                    "check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ."
                )

def _checkgloc(A):

        # See rules 7.5.
        if A._hasmaneuvered and A._hasturned:

            if A._movemaneuvertype == "ET" and A._movestartaltitude <= 25:
                A._gloccheck += 1
                A._logevent(
                    "check for GLOC as turn rate is ET and altitude band is %s (check %d in cycle)."
                    % (A._movestartaltitudeband, A._gloccheck)
                )

def _checkcloseformation(A):
        # See rule 7.8.
        if A._hasturned and apcloseformation.size(A) != 0:
            if (
                (apcloseformation.size(A) > 2 and A._movemaneuvertype == "HT")
                or A._movemaneuvertype == "BT"
                or A._movemaneuvertype == "ET"
            ):
                A._logevent(
                    "close formation breaks down as the turn rate is %s."
                    % A._movemaneuvertype
                )
                apcloseformation.breakdown(A)

        # See rule 13.7, interpreted in the same sense as rule 7.8.
        if A._hasrolled and apcloseformation.size(A) != 0:
            A._logevent("close formation breaks down aircraft is rolling.")
            apcloseformation.breakdown(A)

################################################################################


def useofweaponsforbidden(A):

    # See rule 8.2.2.
    if A._unloadedhfp:
        return "while unloaded"
    if A._unloadedrecoveryfp > 0:
        return "while recovering from being unloaded"

    # See rule 10.1.
    if A._maneuvertype == "ET":
        return "while in an ET"

    if A._ETrecoveryfp > 0:
        return "while recovering from an ET"

    # See rule 13.3.5.
    if A._hrd:
        return "after HRD"

    # See rule 13.3.6.
    if A._hasrolled and A._hasmaneuvered:
        return "immediately after rolling"

    # See rule 13.3.6.
    if A._hasrolled:
        return "while rolling"

    return False



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
