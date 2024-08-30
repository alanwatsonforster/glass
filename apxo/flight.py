import math
import re

import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.gameturn as apgameturn
import apxo.hex as aphex
import apxo.missiledata as apmissiledata
import apxo.speed as apspeed
import apxo.turnrate as apturnrate
import apxo.variants as apvariants

from apxo.rounding import *
from apxo.log import plural

################################################################################


def _move(E, flighttype, power, moves, **kwargs):

    # We save values of these variables at the end of the previous move.

    E._previousflighttype = E._flighttype
    E._flighttype = flighttype

    _checkflighttype(E)

    E.logstart("flight type      is %s." % E._flighttype)
    E.logstart("altitude band    is %s." % E.altitudeband())
    E.logcomment("speed of sound is %.1f." % apspeed.m1speed(E.altitudeband()))

    if E.isaircraft():
        apspeed._startaircraftspeed(E, power, **kwargs)
    else:
        apspeed._startmissilespeed(E)

    _startmove(E)

    E.logpositionandmaneuver("start")

    _continuemove(E, moves)


################################################################################


def _checkflighttype(E):

    if (
        E._flighttype == "LVL"
        or E._flighttype == "ZC"
        or E._flighttype == "SC"
        or E._flighttype == "VC"
        or E._flighttype == "SD"
        or E._flighttype == "HRD/SD"
        or E._flighttype == "UD"
        or E._flighttype == "VD"
        or E._flighttype == "HRD/VD"
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

    # See rule 13.3.5. A HRD is signalled with a "HRD/" prefix to the flight type.
    if E._flighttype[:4] == "HRD/":

        if apcapabilities.hasproperty(E, "NRM"):
            raise RuntimeError("aircraft cannot perform rolling maneuvers.")

        hrd = True
        E._flighttype = E._flighttype[4:]
        E._flighttype = E._flighttype

        # See rule 7.7.
        if E.altitude() > apcapabilities.ceiling(E):
            E.logcomment(
                "check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll."
            )
        elif E.altitudeband() == "EH" or E.altitudeband() == "UH":
            E.logcomment(
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

    E.logstart("speed is below the minimum of %.1f." % apcapabilities.minspeed(E))
    E.logstart("aircraft is stalled.")


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

    # The number of FPs, HFPs, and VFPs used. They are used to ensure that the
    # right mix of HFPs and VFPs are used and to determine when the turn ends.

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

    # This keeps track of the number of turns, turn facing changes,
    # rolls, and vertical rolls.

    E._turnmaneuvers = 0
    E._turnfacingchanges = 0
    E._rollmaneuvers = 0
    E._verticalrolls = 0

    # The number of slides performed and the FP of the last one performed.

    E._slides = 0
    E._slidefp = 0

    # Whether flight is currently supersonic.
    E._m1speed = apspeed.m1speed(E.altitudeband())
    E._supersonic = E._speed >= E._m1speed

    if E.ismissile():
        _startmovemissile(E)
    else:
        _startmoveaircraft(E)


########################################


def _startmovemissile(M, **kwargs):

    M._maneuveringdeparture = False


########################################


def _startmoveaircraft(A):

    # This flags whether a maneuvering departure has occured.

    A._maneuveringdeparture = False

    startmaneuvertype = A._maneuvertype
    if A._flighttype == "VC" or A._flighttype == "VD":
        if (
            A._maneuvertype == "EZ"
            or A._maneuvertype == "TT"
            or A._maneuvertype == "HT"
            or A._maneuvertype == "BT"
            or A._maneuvertype == "ET"
        ):
            A._maneuvertype = None
    elif A._flighttype == "ZC":
        if A._maneuvertype == "ET":
            A.maneuvertype = None
    elif A._flighttype == "SC":
        if (
            A._maneuvertype == "TT"
            or A._maneuvertype == "HT"
            or A._maneuvertype == "BT"
            or A._maneuvertype == "ET"
        ):
            A._maneuvertype = None

    if startmaneuvertype != A._maneuvertype:
        A.logcomment("%s implicitly aborts %s." % (A._flighttype, startmaneuvertype))

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
    A.logcomment("is carrying %+.2f APs." % A._apcarry)


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
    A.logcomment("has %.1f FPs." % A._maxfp)

    A._effectiveclimbcapability = apcapabilities.specialclimbcapability(A)
    A.logcomment("effective climb capability is %.2f." % A._effectiveclimbcapability)


########################################


def _startmovenormalflight(A):

    ########################################

    def reportapcarry():
        A.logcomment("is carrying %+.2f APs." % A._apcarry)

    ########################################

    def reportaltitudecarry():
        if A._altitudecarry != 0:
            A.logcomment("is carrying %.2f altitude levels." % A._altitudecarry)

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
            A.logcomment("damage limits the turn rate to TT.")
            turnrates = turnrates[:2]
        elif A.damageatleast("2L"):
            A.logcomment("damage limits the turn rate to HT.")
            turnrates = turnrates[:3]
        elif A.damageatleast("L"):
            A.logcomment("damage limits the turn rate to BT.")
            turnrates = turnrates[:4]

        # See rule 7.5.

        minspeed = apcapabilities.minspeed(A)
        if A.speed() == minspeed:
            A.logcomment("speed limits the turn rate to EZ.")
            turnrates = turnrates[:1]
        elif A.speed() == minspeed + 0.5:
            A.logcomment("speed limits the turn rate to TT.")
            turnrates = turnrates[:2]
        elif A.speed() == minspeed + 1.0:
            A.logcomment("speed limits the turn rate to HT.")
            turnrates = turnrates[:3]
        elif A.speed() == minspeed + 1.5:
            A.logcomment("speed limits the turn rate to BT.")
            turnrates = turnrates[:4]
        else:
            A.logcomment("speed does not limit the turn rate.")

        # See rule 8.1.1.

        if A._flighttype == "ZC":
            A.logcomment("ZC limits the turn rate to BT.")
            turnrates = turnrates[:4]

        # See rule 8.1.1.

        if A._flighttype == "SC":
            A.logcomment("SC limits the turn rate to EZ.")
            turnrates = turnrates[:1]

        # See rule 8.1.3.

        if A._flighttype == "VC":
            A.logcomment("VC disallows all turns.")
            turnrates = []

        # See rule 8.2.3.

        if A._flighttype == "VD":
            A.logcomment("VD disallows all turns.")
            turnrates = []

        A._allowedturnrates = turnrates

    ########################################

    def checkcloseformationlimits():

        if A.closeformationsize() == 0:
            return

        # See rule 13.7, interpreted in the same sense as rule 7.8.
        if A._hrd:
            A.logcomment("close formation breaks down upon a HRD.")
            apcloseformation.breakdown(A)

        # See rule 8.6.
        if (
            A._flighttype == "ZC"
            or (A._flighttype == "SC" and A._powersetting == "AB")
            or A._flighttype == "VC"
            or A._flighttype == "UD"
            or A._flighttype == "VD"
        ):
            A.logcomment(
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
        A.logcomment("has %d FPs (including %.1f carry)." % (A._maxfp, A._fpcarry))
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

            A.logcomment("all FPs must be HFPs.")

        else:

            if mininitialhfp == 1:
                A.logcomment("the first FP must be an HFP.")
            elif mininitialhfp > 1:
                A.logcomment("the first %d FPs must be HFPs." % mininitialhfp)

            if minhfp == maxhfp:
                A.logcomment(
                    plural(
                        minhfp,
                        "exactly 1 FP must be an HFP.",
                        "exactly %d FPs must be HFPs." % minhfp,
                    )
                )
            elif minhfp > 0 and maxhfp < A._maxfp:
                A.logcomment("between %d and %d FP must be HFPs." % (minhfp, maxhfp))
            elif minhfp > 0:
                A.logcomment(
                    plural(
                        minhfp,
                        "at least 1 FP must be an HFP.",
                        "at least %d FPs must be HFPs." % minhfp,
                    )
                )
            else:
                A.logcomment(
                    plural(
                        maxhfp,
                        "at most 1 FP may be an HFP.",
                        "at most %d FPs may be HFPs." % maxhfp,
                    )
                )

            if minvfp == maxvfp:
                A.logcomment(
                    plural(
                        minvfp,
                        "exactly 1 FP must be a VFP.",
                        "exactly %d FPs must be VFPs." % minvfp,
                    )
                )
            elif minvfp > 0 and maxvfp < A._maxfp:
                A.logcomment("between %d and %d FP must be VFPs." % (minvfp, maxvfp))
            elif minvfp > 0:
                A.logcomment(
                    plural(
                        minvfp,
                        "at least 1 FP must be a VFP.",
                        "at least %d FPs must be VFPs." % minvfp,
                    )
                )
            else:
                A.logcomment(
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
            A.logcomment(
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
                A.logcomment(
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
                    A.logcomment(
                        "turn requirement changed to %d in 1 FP."
                        % A._maneuverfacingchange
                    )
                else:
                    A.logcomment(
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
                A.logcomment("climb capability reduced in SC below climb speed.")
                A._effectiveclimbcapability *= 0.5

            # See the Aircraft Damage Effects Table in the charts.
            if A.damageatleast("H"):
                A.logcomment("climb capability reduced by damage.")
                A._effectiveclimbcapability *= 0.5

            # See rule 6.6 and rule 8.1.4.
            if A.speed() >= apspeed.m1speed(A.altitudeband()):
                A.logcomment("climb capability reduced at supersonic speed.")
                A._effectiveclimbcapability *= 2 / 3

            A.logcomment(
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
        _continuemissileflight(E, moves)
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


def _continuestalledflight(A, moves):

    A.logwhenwhat("", moves)

    if moves != "ST":
        raise RuntimeError("invalid moves %r for stalled flight." % moves)

    altitudechange = math.ceil(A.speed() + A._turnsstalled)

    initialaltitude = A.altitude()
    initialaltitudeband = A.altitudeband()
    A._movedive(altitudechange)
    altitudechange = initialaltitude - A.altitude()

    if A._turnsstalled == 0:
        A._altitudeap = 0.5 * altitudechange
    else:
        A._altitudeap = 1.0 * altitudechange

    A.logposition("end")
    if initialaltitudeband != A.altitudeband():
        A.logcomment(
            "altitude band changed from %s to %s."
            % (initialaltitudeband, A.altitudeband())
        )
    A._checkforterraincollision()
    if A.killed():
        return

    A._finishedmoving = True


########################################


def _continuedepartedflight(A, moves):

    # See rule 6.4 "Abnormal FLight (Stalls and Departures)" and rule 7.7
    # "Manuevering Departures".

    # The action specifies a possible shift and the facing change. Valid values
    # are:
    #
    # - "R30", "R60", "R90", ..., "R300"
    # - "R", "RR", and "RRR" which as usual mean "R30", "R60", and "R90"
    # - the "L" equivalents.

    A.logwhenwhat("", moves)

    if moves[0:2] == "MD":
        maneuveringdeparture = True
        moves = moves[2:]
    else:
        maneuveringdeparture = False

    if moves == "R":
        moves = "R30"
    elif moves == "RR":
        moves = "R60"
    elif moves == "RRR":
        moves = "R90"
    elif moves == "L":
        moves = "L30"
    elif moves == "LL":
        moves = "L60"
    elif moves == "LLL":
        moves = "L90"

    if (
        len(moves) < 3
        or (moves[0] != "R" and moves[0] != "L")
        or not moves[1:].isdecimal()
    ):
        raise RuntimeError("invalid moves %r for departed flight." % moves)

    sense = moves[0]
    facingchange = int(moves[1:])
    if facingchange % 30 != 0 or facingchange <= 0 or facingchange > 300:
        raise RuntimeError("invalid moves %r for departed flight." % moves)

    if maneuveringdeparture:

        # Do the first facing change.

        A._moveturn(sense, 30)
        A._extendpath()
        facingchange -= 30

        # Shift.

        # See rule 5.4.
        A._maxfp = A.speed() + A._fpcarry
        A._fpcarry = 0

        shift = int((A._maxfp) / 2)
        for i in range(0, shift):
            A._moveforward()
            A._extendpath()
            A._checkforterraincollision()
            A._checkforleavingmap()
            if A.killed() or A.removed():
                return

    # Do the (remaining) facing change.

    A._moveturn(sense, facingchange)
    A._extendpath()

    # Now lose altitude.

    initialaltitudeband = A.altitudeband()
    altitudechange = math.ceil(A.speed() + 2 * A._turnsdeparted)
    A._movedive(altitudechange)

    A.logposition("end")
    if initialaltitudeband != A.altitudeband():
        A.logcomment(
            "altitude band changed from %s to %s."
            % (initialaltitudeband, A.altitudeband())
        )
    A._checkforterraincollision()
    if A.killed():
        return

    A._finishedmoving = True


########################################


def _continuespecialflight(A, moves):

    actiondispatchlist = [
        ["L180", "prolog/epilog", lambda A: _doturn(A, "L", 180, False)],
        ["L150", "prolog/epilog", lambda A: _doturn(A, "L", 150, False)],
        ["L120", "prolog/epilog", lambda A: _doturn(A, "L", 120, False)],
        ["L90", "prolog/epilog", lambda A: _doturn(A, "L", 90, False)],
        ["L60", "prolog/epilog", lambda A: _doturn(A, "L", 60, False)],
        ["L30", "prolog/epilog", lambda A: _doturn(A, "L", 30, False)],
        ["LLL", "prolog/epilog", lambda A: _doturn(A, "L", 90, False)],
        ["LL", "prolog/epilog", lambda A: _doturn(A, "L", 60, False)],
        ["L", "prolog/epilog", lambda A: _doturn(A, "L", 30, False)],
        ["R180", "prolog/epilog", lambda A: _doturn(A, "R", 180, False)],
        ["R150", "prolog/epilog", lambda A: _doturn(A, "R", 150, False)],
        ["R120", "prolog/epilog", lambda A: _doturn(A, "R", 120, False)],
        ["R90", "prolog/epilog", lambda A: _doturn(A, "R", 90, False)],
        ["R60", "prolog/epilog", lambda A: _doturn(A, "R", 60, False)],
        ["R30", "prolog/epilog", lambda A: _doturn(A, "R", 30, False)],
        ["RRR", "prolog/epilog", lambda A: _doturn(A, "R", 90, False)],
        ["RR", "prolog/epilog", lambda A: _doturn(A, "R", 60, False)],
        ["R", "prolog/epilog", lambda A: _doturn(A, "R", 30, False)],
        ["HD1", "FP", lambda A: _dohorizontal(A, "HD")],
        ["HD", "FP", lambda A: _dohorizontal(A, "HD")],
        ["H", "FP", lambda A: _dohorizontal(A, "H")],
        ["C1", "FP", lambda A: _doclimb(A, 1)],
        ["C2", "FP", lambda A: _doclimb(A, 2)],
        ["C3", "FP", lambda A: _doclimb(A, 3)],
        ["CCC", "FP", lambda A: _doclimb(A, 3)],
        ["CC", "FP", lambda A: _doclimb(A, 2)],
        ["C", "FP", lambda A: _doclimb(A, 1)],
        ["D1", "FP", lambda A: _dodive(A, 1)],
        ["D2", "FP", lambda A: _dodive(A, 2)],
        ["D3", "FP", lambda A: _dodive(A, 3)],
        ["DDD", "FP", lambda A: _dodive(A, 3)],
        ["DD", "FP", lambda A: _dodive(A, 2)],
        ["D", "FP", lambda A: _dodive(A, 1)],
        ["S", "FP", lambda A: _dostationary(A)],
        ["", "", None],
    ]

    _domoves(
        A,
        moves,
        actiondispatchlist,
    )


########################################


def _continuenormalflight(A, moves):

    actiondispatchlist = [
        ["SLL", "prolog", lambda A: _dodeclaremaneuver(A, "SL", "L")],
        ["SLR", "prolog", lambda A: _dodeclaremaneuver(A, "SL", "R")],
        ["DRL", "prolog", lambda A: _dodeclaremaneuver(A, "DR", "L")],
        ["DRR", "prolog", lambda A: _dodeclaremaneuver(A, "DR", "R")],
        ["LRL", "prolog", lambda A: _dodeclaremaneuver(A, "LR", "L")],
        ["LRR", "prolog", lambda A: _dodeclaremaneuver(A, "LR", "R")],
        ["VRL", "prolog", lambda A: _dodeclaremaneuver(A, "VR", "L")],
        ["VRR", "prolog", lambda A: _dodeclaremaneuver(A, "VR", "R")],
        ["EZL", "prolog", lambda A: _dodeclaremaneuver(A, "EZ", "L")],
        ["TTL", "prolog", lambda A: _dodeclaremaneuver(A, "TT", "L")],
        ["HTL", "prolog", lambda A: _dodeclaremaneuver(A, "HT", "L")],
        ["BTL", "prolog", lambda A: _dodeclaremaneuver(A, "BT", "L")],
        ["ETL", "prolog", lambda A: _dodeclaremaneuver(A, "ET", "L")],
        ["EZR", "prolog", lambda A: _dodeclaremaneuver(A, "EZ", "R")],
        ["TTR", "prolog", lambda A: _dodeclaremaneuver(A, "TT", "R")],
        ["HTR", "prolog", lambda A: _dodeclaremaneuver(A, "HT", "R")],
        ["BTR", "prolog", lambda A: _dodeclaremaneuver(A, "BT", "R")],
        ["ETR", "prolog", lambda A: _dodeclaremaneuver(A, "ET", "R")],
        ["BL", "epilog", lambda A: _dobank(A, "L")],
        ["BR", "epilog", lambda A: _dobank(A, "R")],
        ["WL", "epilog", lambda A: _dobank(A, None)],
        ["L90+", "epilog", lambda A: _domaneuver(A, "L", 90, True, True)],
        ["L60+", "epilog", lambda A: _domaneuver(A, "L", 60, True, True)],
        ["L30+", "epilog", lambda A: _domaneuver(A, "L", 30, True, True)],
        ["LLL+", "epilog", lambda A: _domaneuver(A, "L", 90, True, True)],
        ["LL+", "epilog", lambda A: _domaneuver(A, "L", 60, True, True)],
        ["L+", "epilog", lambda A: _domaneuver(A, "L", None, True, True)],
        ["R90+", "epilog", lambda A: _domaneuver(A, "R", 90, True, True)],
        ["R60+", "epilog", lambda A: _domaneuver(A, "R", 60, True, True)],
        ["R30+", "epilog", lambda A: _domaneuver(A, "R", 30, True, True)],
        ["RRR+", "epilog", lambda A: _domaneuver(A, "R", 90, True, True)],
        ["RR+", "epilog", lambda A: _domaneuver(A, "R", 60, True, True)],
        ["R+", "epilog", lambda A: _domaneuver(A, "R", None, True, True)],
        ["LS180", "epilog", lambda A: _domaneuver(A, "L", 180, True, False)],
        ["L180", "epilog", lambda A: _domaneuver(A, "L", 180, False, False)],
        ["L150", "epilog", lambda A: _domaneuver(A, "L", 150, True, False)],
        ["L120", "epilog", lambda A: _domaneuver(A, "L", 120, True, False)],
        ["L90", "epilog", lambda A: _domaneuver(A, "L", 90, True, False)],
        ["L60", "epilog", lambda A: _domaneuver(A, "L", 60, True, False)],
        ["L30", "epilog", lambda A: _domaneuver(A, "L", 30, True, False)],
        ["LLL", "epilog", lambda A: _domaneuver(A, "L", 90, True, False)],
        ["LL", "epilog", lambda A: _domaneuver(A, "L", 60, True, False)],
        ["L", "epilog", lambda A: _domaneuver(A, "L", None, True, False)],
        ["RS180", "epilog", lambda A: _domaneuver(A, "R", 180, True, False)],
        ["R180", "epilog", lambda A: _domaneuver(A, "R", 180, False, False)],
        ["R150", "epilog", lambda A: _domaneuver(A, "R", 150, True, False)],
        ["R120", "epilog", lambda A: _domaneuver(A, "R", 120, True, False)],
        ["R90", "epilog", lambda A: _domaneuver(A, "R", 90, True, False)],
        ["R60", "epilog", lambda A: _domaneuver(A, "R", 60, True, False)],
        ["R30", "epilog", lambda A: _domaneuver(A, "R", 30, True, False)],
        ["RRR", "epilog", lambda A: _domaneuver(A, "R", 90, True, False)],
        ["RR", "epilog", lambda A: _domaneuver(A, "R", 60, True, False)],
        ["R", "epilog", lambda A: _domaneuver(A, "R", None, True, False)],
        ["HD1", "FP", lambda A: _dohorizontal(A, "HD")],
        ["HD", "FP", lambda A: _dohorizontal(A, "HD")],
        ["HU", "FP", lambda A: _dohorizontal(A, "HU")],
        ["H", "FP", lambda A: _dohorizontal(A, "H")],
        ["C1", "FP", lambda A: _doclimb(A, 1)],
        ["C2", "FP", lambda A: _doclimb(A, 2)],
        ["C3", "FP", lambda A: _doclimb(A, 3)],
        ["CCC", "FP", lambda A: _doclimb(A, 3)],
        ["CC", "FP", lambda A: _doclimb(A, 2)],
        ["C", "FP", lambda A: _doclimb(A, 1)],
        ["D1", "FP", lambda A: _dodive(A, 1)],
        ["D2", "FP", lambda A: _dodive(A, 2)],
        ["D3", "FP", lambda A: _dodive(A, 3)],
        ["DDD", "FP", lambda A: _dodive(A, 3)],
        ["DD", "FP", lambda A: _dodive(A, 2)],
        ["D", "FP", lambda A: _dodive(A, 1)],
        [
            "MDL300",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 300),
        ],
        [
            "MDL270",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 270),
        ],
        [
            "MDL240",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 240),
        ],
        [
            "MDL210",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 210),
        ],
        [
            "MDL180",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 180),
        ],
        [
            "MDL150",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 150),
        ],
        [
            "MDL120",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 120),
        ],
        [
            "MDL90",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 90),
        ],
        [
            "MDL60",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 60),
        ],
        [
            "MDL30",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "L", 30),
        ],
        [
            "MDR300",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 300),
        ],
        [
            "MDR270",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 270),
        ],
        [
            "MDR240",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 240),
        ],
        [
            "MDR210",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 210),
        ],
        [
            "MDR180",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 180),
        ],
        [
            "MDR150",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 150),
        ],
        [
            "MDR120",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 120),
        ],
        [
            "MDR90",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 90),
        ],
        [
            "MDR60",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 60),
        ],
        [
            "MDR30",
            "maneuvering departure",
            lambda A: _domaneuveringdeparture(A, "R", 30),
        ],
        ["", "", None],
    ]

    _domoves(
        A,
        moves,
        actiondispatchlist,
    )


###############################################################################


def _continuemissileflight(M, moves):

    actiondispatchlist = [
        ["TL", "prolog", lambda A: _dodeclaremaneuver(A, "T", "L")],
        ["TR", "prolog", lambda A: _dodeclaremaneuver(A, "T", "R")],
        ["SLL", "prolog", lambda A: _dodeclaremaneuver(A, "SL", "L")],
        ["SLR", "prolog", lambda A: _dodeclaremaneuver(A, "SL", "R")],
        ["VRL", "prolog", lambda A: _dodeclaremaneuver(A, "VR", "L")],
        ["VRR", "prolog", lambda A: _dodeclaremaneuver(A, "VR", "R")],
        ["H", "FP", lambda A: _dohorizontal(A, "H")],
        ["HD", "FP", lambda A: _dohorizontal(A, "HD")],
        ["HD1", "FP", lambda A: _dohorizontal(A, "HD")],
        ["C", "FP", lambda A: _doclimb(A, 1)],
        ["C1", "FP", lambda A: _doclimb(A, 1)],
        ["CC", "FP", lambda A: _doclimb(A, 2)],
        ["C2", "FP", lambda A: _doclimb(A, 2)],
        ["D", "FP", lambda A: _dodive(A, 1)],
        ["D1", "FP", lambda A: _dodive(A, 1)],
        ["DD", "FP", lambda A: _dodive(A, 2)],
        ["D2", "FP", lambda A: _dodive(A, 2)],
        ["DDD", "FP", lambda A: _dodive(A, 3)],
        ["D3", "FP", lambda A: _dodive(A, 3)],
        ["L90+", "epilog", lambda A: _domaneuver(A, "L", 90, True, True)],
        ["L60+", "epilog", lambda A: _domaneuver(A, "L", 60, True, True)],
        ["L30+", "epilog", lambda A: _domaneuver(A, "L", 30, True, True)],
        ["LLL+", "epilog", lambda A: _domaneuver(A, "L", 90, True, True)],
        ["LL+", "epilog", lambda A: _domaneuver(A, "L", 60, True, True)],
        ["L+", "epilog", lambda A: _domaneuver(A, "L", None, True, True)],
        ["R90+", "epilog", lambda A: _domaneuver(A, "R", 90, True, True)],
        ["R60+", "epilog", lambda A: _domaneuver(A, "R", 60, True, True)],
        ["R30+", "epilog", lambda A: _domaneuver(A, "R", 30, True, True)],
        ["RRR+", "epilog", lambda A: _domaneuver(A, "R", 90, True, True)],
        ["RR+", "epilog", lambda A: _domaneuver(A, "R", 60, True, True)],
        ["R+", "epilog", lambda A: _domaneuver(A, "R", None, True, True)],
        ["LS180", "epilog", lambda A: _domaneuver(A, "L", 180, True, False)],
        ["L180", "epilog", lambda A: _domaneuver(A, "L", 180, False, False)],
        ["L150", "epilog", lambda A: _domaneuver(A, "L", 150, True, False)],
        ["L120", "epilog", lambda A: _domaneuver(A, "L", 120, True, False)],
        ["L90", "epilog", lambda A: _domaneuver(A, "L", 90, True, False)],
        ["L60", "epilog", lambda A: _domaneuver(A, "L", 60, True, False)],
        ["L30", "epilog", lambda A: _domaneuver(A, "L", 30, True, False)],
        ["LLL", "epilog", lambda A: _domaneuver(A, "L", 90, True, False)],
        ["LL", "epilog", lambda A: _domaneuver(A, "L", 60, True, False)],
        ["L", "epilog", lambda A: _domaneuver(A, "L", None, True, False)],
        ["RS180", "epilog", lambda A: _domaneuver(A, "R", 180, True, False)],
        ["R180", "epilog", lambda A: _domaneuver(A, "R", 180, False, False)],
        ["R150", "epilog", lambda A: _domaneuver(A, "R", 150, True, False)],
        ["R120", "epilog", lambda A: _domaneuver(A, "R", 120, True, False)],
        ["R90", "epilog", lambda A: _domaneuver(A, "R", 90, True, False)],
        ["R60", "epilog", lambda A: _domaneuver(A, "R", 60, True, False)],
        ["R30", "epilog", lambda A: _domaneuver(A, "R", 30, True, False)],
        ["RRR", "epilog", lambda A: _domaneuver(A, "R", 90, True, False)],
        ["RR", "epilog", lambda A: _domaneuver(A, "R", 60, True, False)],
        ["R", "epilog", lambda A: _domaneuver(A, "R", None, True, False)],
        ["", "", None],
    ]

    _startslope(M)
    _domoves(
        M,
        moves,
        actiondispatchlist,
    )
    M._checktargettracking()


###############################################################################


def _endmove(E):

    if E.killed():
        E.logend("has been killed.")
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
        E.logend("will carry %.1f FPs." % E._fpcarry)
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
        A.logcomment(
            "used %s and %s."
            % (
                plural(A._hfp, "1 HFP", "%d HFPs" % A._hfp),
                plural(A._vfp, "1 VFP", "%d VFPs" % A._vfp),
            )
        )

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
            altitudechange = A.altitude() - A.startaltitude()
            if altitudechange < -1:
                raise RuntimeError("free descent cannot only be taken once per move.")

    ########################################

    def reportgloccycle():

        # See rule 7.6.
        if A._gloccheck > 0 and A._maxturnrate != "ET" and A._maxturnrate != "BT":
            A.logcomment("GLOC cycle ended.")
            A._gloccheck = 0

    ########################################

    def reportcarry():

        if A._altitudecarry != 0:
            A.logcomment("is carrying %.2f altitude levels." % A._altitudecarry)

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

        altitudechange = A.altitude() - A.startaltitude()

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
                truestartaltitude = A.startaltitude() + A.startaltitudecarry()

                truealtitudechange = truealtitude - truestartaltitude

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

        altitudeloss = A.startaltitude() - A.altitude()
        if A._flighttype == "SD" and altitudeloss > 2:
            A.logcomment(
                "close formation breaks down as the aircraft lost %d levels in an SD."
                % altitudeloss
            )
            apcloseformation.breakdown(A)
        elif A._flighttype == "SC" and A._scwithzccomponent:
            A.logcomment(
                "close formation breaks down as the aircraft climbed faster than the sustained climb rate."
            )
            apcloseformation.breakdown(A)

    ########################################

    def handleunloadeddiveflighttype():

        if A._flighttype == "UD":
            # See rule 8.2.2.
            altitudechange = A.altitude() - A.startaltitude()
            if altitudechange == -2:
                A.logcomment("UD ends as flight type SD.")
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


def _domoves(E, moves, actiondispatchlist):
    """
    Carry out flight moves.
    """

    if moves == "":
        return

    for move in re.split(r" *[, ] *", moves):
        if not E.killed():
            _domove(E, move, actiondispatchlist)


################################################################################


def _domove(E, move, actiondispatchlist):
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

    def checkminspeed():

        # The minimum speed can change during a move if the altitude or
        # configuration changes.

        if E.isaircraft():
            previousminspeed = E._minspeed
            E._minspeed = apcapabilities.minspeed(E)
            if E._minspeed != previousminspeed:
                E.logcomment("minimum speed is now %.1f." % E._minspeed)
                if (
                    E.speed() <= previousminspeed + 2.0
                    or E.speed() <= E._minspeed + 2.0
                ):
                    # See rule 7.5.
                    if E.speed() == E._minspeed:
                        E.logcomment("speed now limits the turn rate to EZ.")
                    elif E.speed() == E._minspeed + 0.5:
                        E.logcomment("speed now limits the turn rate to TT.")
                    elif E.speed() == E._minspeed + 1.0:
                        E.logcomment("speed now limits the turn rate to HT.")
                    elif E.speed() == E._minspeed + 1.5:
                        E.logcomment("speed now limits the turn rate to BT.")
                    else:
                        E.logcomment("speed no longer limits the turn rate.")

    def checkm1speed():

        # The m1 speed can change during a move if the altitude changes.

        previousm1speed = E._m1speed
        E._m1speed = apspeed.m1speed(E.altitudeband())
        if E._m1speed != previousm1speed:
            E.logcomment("speed of sound is now %.1f." % E._m1speed)

        previoussupersonic = E._supersonic
        E._supersonic = E.speed() >= E._m1speed
        if previoussupersonic and not E._supersonic:
            E.logcomment("speed is now subsonic.")
        elif not previoussupersonic and E._supersonic:
            E.logcomment("speed is now supersonic.")

    ####################

    checkminspeed()

    E.logwhenwhat("FP %d" % (E._fp + 1), move)

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
    E._movestartm1speed = apspeed.m1speed(E.altitudeband())

    # Check a missile has not stalled. We do this for each FP, since
    # the stall speed depends on altitude and can change as the missile
    # climbs or dives.

    if E.ismissile() and E.speed() < apspeed.missileminspeed(E.altitudeband()):
        E.logcomment("has stalled.")
        if move != "":
            raise RuntimeError("invalid move %r for stalled missile." % move)
        M._remove()
        M.logcomment("has been removed.")
        M._finishedmoving = True
        return

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

            E.logposition("end")

            return

        E._horizontal = False
        E._vertical = False

        E._hasunloaded = False
        E._hasdeclaredamaneuver = False
        E._hasmaneuvered = False
        E._hasrolled = False
        E._hasbanked = False

        remainingactions = doactions(E, remainingactions, "prolog")
        remainingactions = doactions(E, remainingactions, "prolog/epilog")

        fp = E._fp
        remainingactions = doactions(E, remainingactions, "FP")
        if E._fp == fp or E._fp > fp + 1:
            raise RuntimeError("%r is not a valid move." % move)

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
            if E._flighttype != "SP":
                _checkrecovery(E)
                _checktracking(E)
                _checkmaneuveringdeparture(E)
                _checkgloc(E)
            _checkcloseformation(E)

        remainingactions = doactions(E, remainingactions, "epilog")
        remainingactions = doactions(E, remainingactions, "prolog/epilog")

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
            E.logpositionandmaneuver("end")
        else:
            E.logpositionandmaneuver("")
        E._extendpath()

    if E._movestartaltitudeband != E.altitudeband():
        E.logcomment(
            "altitude band changed from %s to %s."
            % (E._movestartaltitudeband, E.altitudeband())
        )
        if not E._lastfp:
            checkm1speed()
            checkminspeed()

    E._checkforterraincollision()
    E._checkforleavingmap()

    if E.killed() or E._maneuveringdeparture or E._fp >= E._maxfp:
        E._finishedmoving = True


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
        A.logcomment("recovered from ET.")
    if A._BTrecoveryfp == 0:
        A.logcomment("recovered from BT.")
    if A._rollrecoveryfp == 0:
        A.logcomment("recovered from roll.")
    if A._HTrecoveryfp == 0:
        A.logcomment("recovered from HT.")
    if A._TTrecoveryfp == 0:
        A.logcomment("recovered from TT.")


def _checktracking(A):

    # Check tracking. See rule 9.4.
    if A._tracking:
        if useofweaponsforbidden(A):
            A.logcomment("stopped SSGT.")
            A._tracking = None
            A._trackingfp = 0
        elif apairtoair.trackingforbidden(A, A._tracking):
            A.logcomment(
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
            A.logcomment(
                "check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll."
            )
        elif A._movestartaltitudeband == "EH" or A._movestartaltitudeband == "UH":
            A.logcomment(
                "check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll."
                % A._movestartaltitudeband
            )

    # See rules 7.7 and 8.5.
    if A._hasmaneuvered and A._hasturned:
        if (
            A._movestartaltitude > apcapabilities.ceiling(A)
            and A._movemaneuvertype != "EZ"
        ):
            A.logcomment(
                "check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ."
            )


def _checkgloc(A):

    # See rules 7.5.
    if A._hasmaneuvered and A._hasturned:

        if A._movemaneuvertype == "ET" and A._movestartaltitude <= 25:
            A._gloccheck += 1
            A.logcomment(
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
            A.logcomment(
                "close formation breaks down as the turn rate is %s."
                % A._movemaneuvertype
            )
            apcloseformation.breakdown(A)

    # See rule 13.7, interpreted in the same sense as rule 7.8.
    if A._hasrolled and apcloseformation.size(A) != 0:
        A.logcomment("close formation breaks down aircraft is rolling.")
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

    return maneuvertype in ["EZ", "TT", "HT", "BT", "ET", "T"]


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


########################################


def _dohorizontal(E, action):
    """
    Move horizontally.
    """

    if E._maneuvertype == "VR":
        raise RuntimeError("attempt to declare a vertical roll during an HFP.")

    if action == "HD":

        if E._flighttype != "LVL" and E._flighttype != "SP" and E._flighttype != "MS":
            raise RuntimeError(
                "%r is not a valid action when the flight type is %s."
                % (action, E._flighttype)
            )
        altitudechange = 1

    elif action == "HU":

        if E._flighttype != "UD":
            raise RuntimeError(
                "%r is not a valid action when the flight type is %s."
                % (action, E._flighttype)
            )

        E._hasunloaded = True
        E._unloadedhfp += 1
        if E._firstunloadedfp == None:
            E._firstunloadedfp = E._hfp
        E._lastunloadedfp = E._hfp

        if math.floor(E._maxfp) == 1:
            # Both half FPs and all FPs.
            altitudechange = 2
        elif E._unloadedhfp == math.floor(E._maxfp / 2):
            altitudechange = 1
        elif E._unloadedhfp == math.floor(E._maxfp):
            altitudechange = 1
        else:
            altitudechange = 0

    else:

        altitudechange = 0

    E._movedive(altitudechange)
    E._moveforward()

    E._horizontal = True
    E._fp += 1
    E._hfp += 1


########################################


def _doclimb(E, altitudechange):
    """
    Climb.
    """

    if E.isaircraft():

        if (
            E._flighttype == "LVL"
            or E._flighttype == "SD"
            or E._flighttype == "UD"
            or E._flighttype == "VD"
        ):

            raise RuntimeError(
                "attempt to climb while flight type is %s." % E._flighttype
            )

        elif E._flighttype == "SP":

            if altitudechange == 1:
                altitudechange = E._effectiveclimbcapability

        elif E._hfp < E._mininitialhfp:

            raise RuntimeError("insufficient initial HFPs.")

        elif E._flighttype == "ZC":

            # See rule 8.1.1.
            if altitudechange == 2:
                if E._effectiveclimbcapability <= 2.0:
                    raise RuntimeError("invalid altitude change in climb.")
            elif altitudechange == 3:
                if E._effectiveclimbcapability < 6.0:
                    raise RuntimeError("invalid altitude change in climb.")
                if E._usedsuperclimb:
                    raise RuntimeError("invalid altitude change in climb.")
                E._usedsuperclimb = True

        elif E._flighttype == "SC":

            # See rule 8.1.2.
            if E._effectiveclimbcapability < 2.0 and altitudechange == 2:
                raise RuntimeError("invalid altitude change in climb.")
            if E._vfp == 0 and E._effectiveclimbcapability % 1 != 0:
                # First VFP with fractional climb capability.
                altitudechange = E._effectiveclimbcapability % 1

        elif E._flighttype == "VC":

            # See rule 8.1.3.
            if altitudechange != 1 and altitudechange != 2:
                raise RuntimeError("invalid altitude change in climb.")

    E._moveclimb(altitudechange)

    E._vertical = True
    E._fp += 1
    E._vfp += 1

    # See rule 8.5.
    if E._flighttype == "SC" and E.altitude() > apcapabilities.ceiling(E):
        raise RuntimeError("attempt to climb above ceiling in SC.")


########################################


def _dodive(E, altitudechange):
    """
    Dive.
    """

    def checkaltitudechange():

        assert altitudechange == 1 or altitudechange == 2 or altitudechange == 3

        if E._flighttype == "SP":

            pass

        elif E._flighttype == "SD":

            # See rule 8.2.1.
            if altitudechange != 1 and altitudechange != 2:
                raise RuntimeError(
                    "attempt to dive %d levels per VFP while the flight type is SC."
                    % altitudechange
                )

        elif E._flighttype == "UD":

            # See rule 8.2.2.
            if altitudechange != 1:
                raise RuntimeError(
                    "attempt to dive %d levels per unloaded HFP while the flight type is UL."
                    % altitudechange
                )

        elif E._flighttype == "VD":

            # See rule 8.2.3.
            if altitudechange != 2 and altitudechange != 3:
                raise RuntimeError(
                    "attempt to dive %s per VFP while the flight type is VD."
                    % plural(altitudechange, "1 level", "%d levels" % altitudechange)
                )

        elif E._flighttype == "LVL":

            # See rule 8.2.4.
            if altitudechange != 1:
                raise RuntimeError(
                    "attempt to descend %d levels while flight type is LVL."
                    % altitudechange
                )

        else:

            # See rule 8.0.
            raise RuntimeError(
                "attempt to dive while flight type is %s." % E._flighttype
            )

    if E.isaircraft():
        checkaltitudechange()
        if E._flighttype != "SP" and E._hfp < E._mininitialhfp:
            raise RuntimeError("insufficient initial HFPs.")

    E._vertical = True
    E._fp += 1
    E._vfp += 1

    E._movedive(altitudechange)


########################################


def _dostationary(E):

    E._fp += 1


########################################


def _dobank(E, sense):

    if E._hasbanked:
        raise RuntimeError("attempt to bank twice.")

    # See rule 7.4.
    if apcapabilities.hasproperty(E, "LRR"):
        if (E._bank == "L" and sense == "R") or (E._bank == "R" and sense == "L"):
            raise RuntimeError(
                "attempt to bank to %s while banked to %s in a LRR aircraft."
                % (sense, E._bank)
            )

    E._bank = sense
    E._hasbanked = True
    if _isturn(E._maneuvertype):
        E._maneuvertype = None
        E._maneuversense = None
        E._maneuverfacingchange = None
        E._maneuverfp = 0


########################################


def _dodeclareturn(E, turnrate, sense):
    """
    Declare the start of turn in the specified direction and rate.
    """

    if E.isaircraft():

        # See rule 8.1.3 and 8.2.3
        if E._flighttype == "VC" or E._flighttype == "VD":
            raise RuntimeError(
                "attempt to declare turn while flight type is %s." % E._flighttype
            )

        # See rule 7.1.

        # Check the bank. See rule 7.4.
        if apcapabilities.hasproperty(E, "LRR"):
            if E._bank != sense:
                raise RuntimeError(
                    "attempt to declare a turn to %s while not banked to %s in a LRR aircraft."
                    % (sense, sense)
                )
        elif not apcapabilities.hasproperty(E, "HRR"):
            if (E._bank == "L" and sense == "R") or (E._bank == "R" and sense == "L"):
                raise RuntimeError(
                    "attempt to declare a turn to %s while banked to %s."
                    % (sense, E._bank)
                )

        if E._allowedturnrates == []:
            raise RuntimeError("turns are forbidded.")

        if turnrate not in E._allowedturnrates:
            raise RuntimeError(
                "attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type."
            )

        turnrateap = apcapabilities.turndrag(E, turnrate)
        if turnrateap == None:
            raise RuntimeError(
                "attempt to declare a turn rate tighter than allowed by the aircraft."
            )

        # Determine the maximum turn rate.
        if E._maxturnrate == None:
            E._maxturnrate = turnrate
        else:
            turnrates = ["EZ", "TT", "HT", "BT", "ET"]
            E._maxturnrate = turnrates[
                max(turnrates.index(turnrate), turnrates.index(E._maxturnrate))
            ]

        turnrequirement = apturnrate.turnrequirement(
            E.altitudeband(), E.speed(), turnrate
        )

    else:

        if E.speed() < apspeed.missilemaneuverspeed(E.altitudeband()):
            raise RuntimeError(
                "attempt to maneuver when not allowed by the speed and altitude."
            )

        baseturnrate, divisor = E.turnrate()
        turnrequirement = apturnrate.turnrequirement(
            E.altitudeband(), E.speed(), baseturnrate, divisor=divisor
        )

    if turnrequirement == None:
        raise RuntimeError(
            "attempt to declare a turn rate tighter than allowed by the speed and altitude."
        )

    E._bank = sense
    E._maneuvertype = turnrate
    E._maneuversense = sense
    E._maneuverfp = 0
    E._maneuversupersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
    if turnrequirement >= 60:
        E._maneuverrequiredfp = 1
        E._maneuverfacingchange = turnrequirement
    else:
        E._maneuverrequiredfp = turnrequirement
        E._maneuverfacingchange = 30

    if E.isaircraft():
        if apvariants.withvariant("use house rules"):
            E._turnrateap -= turnrateap
            if E._maneuversupersonic:
                if apcapabilities.hasproperty(E, "PSSM"):
                    E._turnrateap -= 1.0
                elif not apcapabilities.hasproperty(E, "GSSM"):
                    E._turnrateap -= 0.5


########################################


def _doturn(E, sense, facingchange, continuous):
    """
    Turn in the specified sense and amount.
    """

    # See rule 8.1.3 and 8.2.3
    if E._flighttype == "VC" or E._flighttype == "VD":
        raise RuntimeError("attempt to turn while flight type is %s." % E._flighttype)

    if E._flighttype != "SP":

        # See rule 7.1.
        if (
            E._maneuverfp < E._maneuverrequiredfp
            or facingchange > E._maneuverfacingchange
        ):
            raise RuntimeError("attempt to turn faster than the declared turn rate.")

    E._moveturn(sense, facingchange)

    if E.isaircraft() and E._flighttype != "SP":

        # See Hack's article in APJ 36
        if E._turnmaneuvers == 0:
            sustainedfacingchanges = facingchange // 30 - 1
        else:
            sustainedfacingchanges = facingchange // 30

        if not apvariants.withvariant("use house rules"):
            if apcapabilities.hasproperty(E, "LBR"):
                E._sustainedturnap -= sustainedfacingchanges * 0.5
            elif apcapabilities.hasproperty(E, "HBR"):
                E._sustainedturnap -= sustainedfacingchanges * 1.5
            else:
                E._sustainedturnap -= sustainedfacingchanges * 1.0

    E._turnmaneuvers += 1
    E._turnfacingchanges += facingchange // 30


########################################


def _dodeclareslide(E, sense):

    # See rule 8.1.3 and 8.2.3
    if E._flighttype == "VC" or E._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare slide while flight type is %s." % E._flighttype
        )

    # See rules 13.1 and 13.2.

    if E.isaircraft():

        if E._slides == 1 and E.speed() <= 9.0:
            raise RuntimeError("only one slide allowed per turn at low speed.")
        if E._slides == 1 and E._fp - E._slidefp < 4:
            raise RuntimeError(
                "attempt to start a second slide without sufficient intermediate FPs."
            )
        elif E._slides == 2:
            raise RuntimeError("at most two slides allowed per turn.")

    E._bank = None
    E._maneuvertype = "SL"
    E._maneuversense = sense
    E._maneuverfacingchange = None
    E._maneuverfp = 0
    E._maneuversupersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
    E._maneuverrequiredfp = 2 + _extrapreparatoryhfp(E) + 1


########################################


def _extrapreparatoryhfp(E):

    # See rule 13.1.

    extrapreparatoryfp = {
        "LO": 0,
        "ML": 0,
        "MH": 0,
        "HI": 1,
        "VH": 2,
        "EH": 3,
        "UH": 4,
    }[E.altitudeband()]

    if E.speed() >= apspeed.m1speed(E.altitudeband()):
        extrapreparatoryfp += 1.0

    # See "Aircraft Damage Effects" in the Play Aids.

    if E.isaircraft() and E.damageatleast("2L"):
        extrapreparatoryfp += 1.0

    return extrapreparatoryfp


########################################


def _doslide(E, sense):

    # See rule 8.1.3 and 8.2.3
    if E._flighttype == "VC" or E._flighttype == "VD":
        raise RuntimeError("attempt to slide while flight type is %s." % E._flighttype)

    # See rules 13.1 and 13.2.

    if E._maneuverfp < E._maneuverrequiredfp:
        raise RuntimeError("attempt to slide without sufficient preparatory HFPs.")

    # Move.
    E._moveslide(sense)

    # See rule 13.2.
    if not apvariants.withvariant("use house rules"):
        if E._slides >= 1:
            E._othermaneuversap -= 1.0

    # Keep track of the number of slides and the FP of the last slide.
    E._slides += 1
    E._slidefp = E._fp

    # Implicitly finish with wings level.
    E._bank = None


########################################


def _dodeclaredisplacementroll(E, sense):

    # See rules 13.1 and 13.3.1.

    if apcapabilities.hasproperty(E, "NRM"):
        raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if apcapabilities.rolldrag(E, "DR") == None:
        raise RuntimeError("aircraft cannot perform displacement rolls.")

    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if E._flighttype == "SC" or E._flighttype == "VC" or E._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare a displacement roll while flight type is %s."
            % E._flighttype
        )

    E._bank = None
    E._maneuvertype = "DR"
    E._maneuversense = sense
    E._maneuverfacingchange = None
    E._maneuverfp = 0
    E._maneuversupersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
    # The requirement includes the FPs used to execute the roll.
    E._maneuverrequiredfp = (
        apcapabilities.rollhfp(E) + _extrapreparatoryhfp(E) + rounddown(E.speed() / 3)
    )

    # See rules 13.3.1 and 6.6.
    if apvariants.withvariant("use house rules"):
        E._othermaneuversap -= apcapabilities.rolldrag(E, "DR")
        if E._maneuversupersonic:
            if apcapabilities.hasproperty(E, "PSSM"):
                E._othermaneuversap -= 2.0
            elif not apcapabilities.hasproperty(E, "GSSM"):
                E._othermaneuversap -= 1.0


########################################


def _dodisplacementroll(E, sense):

    # See rules 13.1 and 13.3.1.

    if E._maneuverfp < E._maneuverrequiredfp:
        raise RuntimeError("attempt to roll without sufficient preparatory FPs.")

    if not E._horizontal:
        raise RuntimeError("attempt to roll on a VFP.")

    # Move.
    E._movedisplacementroll(sense)

    # See rule 13.3.1.
    if not apvariants.withvariant("use house rules"):
        E._othermaneuversap -= apcapabilities.rolldrag(E, "DR")

    # See rule 6.6.
    if E._maneuversupersonic:
        if apcapabilities.hasproperty(E, "PSSM"):
            E._othermaneuversap -= 2.0
        elif not apcapabilities.hasproperty(E, "GSSM"):
            E._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if not apvariants.withvariant("use house rules"):
        if E._rollmaneuvers > 0:
            E._othermaneuversap -= 1.0
        E._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    E._bank = None


########################################


def _dodeclarelagroll(E, sense):

    # See rule 13.3.2.

    if apcapabilities.hasproperty(E, "NRM"):
        raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if apcapabilities.rolldrag(E, "LR") == None:
        raise RuntimeError("aircraft cannot perform lag rolls.")

    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if E._flighttype == "SC" or E._flighttype == "VC" or E._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare a lag roll while flight type is %s." % E._flighttype
        )

    E._bank = None
    E._maneuvertype = "LR"
    E._maneuversense = sense
    E._maneuverfacingchange = None
    E._maneuverfp = 0
    E._maneuversupersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
    # The requirement includes the FPs used to execute the roll.
    E._maneuverrequiredfp = (
        apcapabilities.rollhfp(E) + _extrapreparatoryhfp(E) + rounddown(E.speed() / 3)
    )

    # See rules 13.3.1 and 6.6.
    if apvariants.withvariant("use house rules"):
        E._othermaneuversap -= apcapabilities.rolldrag(E, "LR")
        if E._maneuversupersonic:
            if apcapabilities.hasproperty(E, "PSSM"):
                E._othermaneuversap -= 2.0
            elif not apcapabilities.hasproperty(E, "GSSM"):
                E._othermaneuversap -= 1.0


########################################


def _dolagroll(E, sense):

    # See rules 13.1 and 13.3.2.

    if E._maneuverfp < E._maneuverrequiredfp:
        raise RuntimeError("attempt to roll without sufficient preparatory FPs.")

    if not E._horizontal:
        raise RuntimeError("attempt to roll on a VFP.")

    # Move.
    E._movelagroll(sense)

    # See rule 13.3.1.
    if not apvariants.withvariant("use house rules"):
        E._othermaneuversap -= apcapabilities.rolldrag(E, "LR")

    # See rule 6.6.
    if E._maneuversupersonic:
        if apcapabilities.hasproperty(E, "PSSM"):
            E._othermaneuversap -= 2.0
        elif not apcapabilities.hasproperty(E, "GSSM"):
            E._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if not apvariants.withvariant("use house rules"):
        if E._rollmaneuvers > 0:
            E._othermaneuversap -= 1.0
        E._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    E._bank = None


########################################


def _dodeclareverticalroll(E, sense):

    if E.isaircraft():

        if apcapabilities.hasproperty(E, "NRM"):
            raise RuntimeError("aircraft cannot perform rolling maneuvers.")
        if E._verticalrolls == 1 and apcapabilities.hasproperty(E, "OVR"):
            raise RuntimeError("aircraft can only perform one vertical roll per turn.")

        # See rule 13.3.4.
        if E._flighttype != "VC" and E._flighttype != "VD":
            raise RuntimeError(
                "attempt to declare a vertical roll while flight type is %s."
                % E._flighttype
            )
        if E._previousflighttype == "LVL" and E._flighttype == "VC" and not E._lastfp:
            raise RuntimeError(
                "attempt to declare a vertical roll in VC following LVL flight other than on the last FP."
            )

        # See rule 13.3.5.
        if E._hrd and not E._lastfp:
            raise RuntimeError(
                "attempt to declare a vertical roll after HRD other than on the last FP."
            )

    E._bank = None
    E._maneuvertype = "VR"
    E._maneuversense = sense
    E._maneuverfacingchange = None
    E._maneuverfp = 0
    E._maneuversupersonic = E.speed() >= apspeed.m1speed(E.altitudeband())
    E._maneuverrequiredfp = 1

    if E.isaircraft():

        # See rules 6.6 and 13.3.6
        if apvariants.withvariant("use house rules"):
            E._othermaneuversap -= apcapabilities.rolldrag(E, "VR")
            if E._maneuversupersonic:
                if apcapabilities.hasproperty(E, "PSSM"):
                    E._othermaneuversap -= 2.0
                elif not apcapabilities.hasproperty(E, "GSSM"):
                    E._othermaneuversap -= 1.0


########################################


def _doverticalroll(E, sense, facingchange, shift):

    if E._maneuverfp < E._maneuverrequiredfp:
        raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")

    if E.isaircraft():

        # See rule 13.3.4.
        if apcapabilities.hasproperty(E, "LRR") and facingchange > 90:
            raise RuntimeError(
                "attempt to roll vertically by more than 90 degrees in LRR aircraft."
            )

        if not apvariants.withvariant("use house rules"):
            E._othermaneuversap -= apcapabilities.rolldrag(E, "VR")

        # See rule 13.3.6
        if not apvariants.withvariant("use house rules"):
            if E._rollmaneuvers > 0:
                E._othermaneuversap -= 1

    # Move.
    E._moveverticalroll(sense, facingchange, shift)

    E._rollmaneuvers += 1
    E._verticalrolls += 1

    if E.isaircraft():
        # See rule 6.6.
        if not apvariants.withvariant("use house rules"):
            if E._maneuversupersonic:
                if apcapabilities.hasproperty(E, "PSSM"):
                    E._othermaneuversap -= 2.0
                elif not apcapabilities.hasproperty(E, "GSSM"):
                    E._othermaneuversap -= 1.0


########################################


def _dodeclaremaneuver(E, maneuvertype, sense):

    if E._hasdeclaredamaneuver:
        raise RuntimeError("attempt to declare a second maneuver.")

    if E.isaircraft() and apvariants.withvariant("use house rules"):
        startap = E._turnrateap + E._othermaneuversap

    if maneuvertype == "SL":
        _dodeclareslide(E, sense)
    elif maneuvertype == "DR":
        _dodeclaredisplacementroll(E, sense)
    elif maneuvertype == "LR":
        _dodeclarelagroll(E, sense)
    elif maneuvertype == "VR":
        _dodeclareverticalroll(E, sense)
    else:
        _dodeclareturn(E, maneuvertype, sense)

    if E.isaircraft() and apvariants.withvariant("use house rules"):
        endap = E._turnrateap + E._othermaneuversap
        ap = " (%+.1f AP)" % (endap - startap)
    else:
        ap = ""

    if E._maneuversupersonic:
        E.logcomment("declared supersonic %s%s." % (E.maneuver(), ap))
    else:
        E.logcomment("declared %s%s." % (E.maneuver(), ap))

    E._hasdeclaredamaneuver = True


########################################


def _domaneuver(E, sense, facingchange, shift, continuous):

    if E._maneuvertype == None:
        raise RuntimeError("attempt to maneuver without a declaration.")

    if E._maneuversense != sense:
        raise RuntimeError("attempt to maneuver against the sense of the declaration.")

    if E._maneuvertype == "SL":
        if facingchange != None:
            raise RuntimeError("invalid action for a slide.")
        _doslide(E, sense)
    elif E._maneuvertype == "DR":
        if facingchange != None:
            raise RuntimeError("invalid action for a displacement roll.")
        _dodisplacementroll(E, sense)
    elif E._maneuvertype == "LR":
        if facingchange != None:
            raise RuntimeError("invalid action for a lag roll.")
        _dolagroll(E, sense)
    elif E._maneuvertype == "VR":
        if facingchange == None:
            facingchange = 30
        _doverticalroll(E, sense, facingchange, shift)
    else:
        if facingchange == None:
            facingchange = 30
        _doturn(E, sense, facingchange, continuous)

    E._hasmaneuvered = True
    E._maneuverfp = 0

    if not continuous:
        E._maneuvertype = None
        E._maneuversense = None
        E._maneuverfacingchange = None
        E._maneuverrequiredfp = 0
        E._maneuversupersonic = False
    else:
        E._hasdeclaredamaneuver = False
        _dodeclaremaneuver(E, E._maneuvertype, E._maneuversense)


########################################


def _domaneuveringdeparture(E, sense, facingchange):

    # Do the first facing change.
    E._moveturn(sense, 30)
    E._extendpath()
    facingchange -= 30

    # Shift.

    shift = int((E._maxfp - E._fp) / 2)
    for i in range(0, shift):
        E._moveforward()
        E._extendpath()
        E._checkforterraincollision()
        E._checkforleavingmap()
        if E.killed() or E.removed():
            return

    # Do any remaining facing changes.
    E._moveturn(sense, facingchange)
    E._extendpath()


################################################################################


def _startslope(E):

    E._startslopealtitude = E.altitude()
    E._startslopehp = E._hfp


def _slope(E):

    startaltitude = E._startslopealtitude
    starthfp = E._startslopehp

    endaltitude = E.altitude()
    endhfp = E._hfp

    slopenumerator = endaltitude - startaltitude
    slopedenominator = endhfp - starthfp

    return slopenumerator, slopedenominator


################################################################################
