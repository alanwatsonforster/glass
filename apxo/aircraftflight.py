"""
Aircraft flight.
"""

##############################################################################

import math
import re
from apxo.math import *

import apxo as ap
import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.aircraft as apxoaircraft
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.configuration as apconfiguration
import apxo.departedflight as apdepartedflight
import apxo.element as apelement
import apxo.flight as apflight
import apxo.hex as aphex
import apxo.log as aplog
import apxo.speed as apspeed
import apxo.stalledflight as apstalledflight
import apxo.stores as apstores
import apxo.turnrate as apturnrate
import apxo.variants as apvariants

from apxo.log import plural

##############################################################################


def move(
    A,
    flighttype,
    power,
    tasks="",
    speedbrakes=None,
    flamedoutengines=0,
    lowspeedliftdeviceselected=None,
    jettison=None,
    note=None,
):
    """
    Start a move, declaring the flight type and power, and possible carrying
    out some tasks.
    """

    if A.killed() or A.removed():
        endmove(A)
        return

    # We save values of these variables at the end of the previous move.

    A._previouspowersetting = A._powersetting
    A._previousflighttype = A._flighttype
    A._previousaltitude = A.altitude()
    A._previousaltitudecarry = A.altitudecarry()
    A._previousspeed = A.speed()

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

    # This flags whether a maneuvering departure has occured.

    A._maneuveringdeparture = False

    A._flighttype = flighttype
    A._logstart("flight type   is %s." % A._flighttype)

    if flighttype == "SP":
        checkspecialflight(A)
    elif flighttype == "ST":
        apstalledflight.checkflight(A)
    elif flighttype == "DP":
        apdepartedflight.checkflight(A)
    else:
        checknormalflight(A)

    if flighttype == "SP":
        A._setspeed(power)
    else:
        A._startmovespeed(
            power, flamedoutengines, lowspeedliftdeviceselected, speedbrakes
        )
        A._logstart("configuration is %s." % A._configuration)
    A._logstart("altitude band is %s." % A.altitudeband())
    A._logstart("damage        is %s." % A.damage())

    if A._flighttype == "SP":

        if jettison is not None:
            raise RuntimeError("invalid jettison argument.")

        A._fpcarry = 0
        A._apcarry = 0
        A._turnsstalled = 0
        A._turnsdeparted = 0
        startspecialflight(A, tasks, note=note)

    elif A._flighttype == "ST":

        if tasks != "":
            raise RuntimeError("invalid tasks argument.")

        A._fpcarry = 0
        A._setaltitudecarry(0)
        apstalledflight.doflight(A, tasks, jettison=jettison, note=note)
        A._turnsstalled += 1
        endmove(A)

    elif A._flighttype == "DP":

        if jettison is not None:
            raise RuntimeError("invalid jettison argument.")

        A._fpcarry = 0
        A._apcarry = 0
        A._setaltitudecarry(0)
        apdepartedflight.doflight(A, tasks, note=note)
        A._turnsdeparted += 1
        endmove(A)

    else:

        if jettison is not None:
            raise RuntimeError("invalid jettison argument.")

        # See rule 8.1.4 on altitude carry.
        if not A.isinclimbingflight():
            A._setaltitudecarry(0)

        A._turnsstalled = 0
        A._turnsdeparted = 0
        startnormalflight(A, tasks, note=note)


################################################################################


def continuemove(A, tasks="", note=None):
    """
    Continue a move that has been started, possible carrying out some tasks.
    """

    if A.killed() or A.removed() or A._flighttype == "ST" or A._flighttype == "DP":
        A._lognote(note)
    elif A._flighttype == "SP":
        continuespecialflight(A, tasks, note=note)
    else:
        continuenormalflight(A, tasks, note=note)


################################################################################


def endmove(A):
    """
    Process the end of a move.
    """

    if A.killed():

        A._logend("aircraft has been killed.")

    else:

        if A._flighttype == "SP":

            A._newspeed = A.speed()

        else:

            A._endmovespeed()

        A._finishedmoving = True


################################################################################


def checknormalflight(A):

    if apcapabilities.hasproperty(A, "SPFL"):
        raise RuntimeError("special-flight aircraft cannot perform normal flight.")

    # See rule 13.3.5. A HRD is signalled by appending "/HRD" to the flight type.
    if A._flighttype[-4:] == "/HRD":

        if apcapabilities.hasproperty(A, "NRM"):
            raise RuntimeError("aircraft cannot perform rolling maneuvers.")

        hrd = True
        A._flighttype = A._flighttype[:-4]
        A._flighttype = A._flighttype

        # See rule 7.7.
        if A.altitude() > apcapabilities.ceiling(A):
            A._logevent(
                "check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll."
            )
        elif A.altitudeband() == "EH" or A.altitudeband() == "UH":
            A._logevent(
                "check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll."
                % A.altitudeband()
            )

    else:

        hrd = False

    A._hrd = hrd

    if A._flighttype not in ["LVL", "SC", "ZC", "VC", "SD", "UD", "VD"]:
        raise RuntimeError("invalid flight type %r." % A._flighttype)

    # See rule 13.3.5 for restrictions on HRDs.

    if hrd:
        if A._previousflighttype == "LVL" and A._flighttype == "VD":
            pass
        elif (
            A._previousflighttype == "ZC" or A._previousflighttype == "SC"
        ) and A._flighttype == "VD":
            pass
        elif A._previousflighttype == "VC" and A._flighttype == "SD":
            pass
        else:
            raise RuntimeError(
                "flight type immediately after %s cannot be %s with a HRD."
                % (A._previousflighttype, A._flighttype)
            )

    if A._previousflighttype == "DP":

        # See rule 6.4 on recovering from departed flight.

        if _isclimbingflight(A._flighttype):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )
        elif A._flighttype == "LVL" and not apcapabilities.hasproperty(A, "HPR"):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )

    if A._previousflighttype == "ST":

        # See rule 6.4 on recovering from stalled flight.

        if _isclimbingflight(A._flighttype):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )

    if A._flighttype == "LVL":

        # See rule 8.2.3 on VD recovery.

        if A._previousflighttype == "VD":
            if A.speed() <= 2.0:
                pass
            elif not apcapabilities.hasproperty(A, "HPR"):
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (A._previousflighttype, A._flighttype)
                )
            elif A.speed() >= 3.5:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (for HPR aircraft at high speed)."
                    % (A._previousflighttype, A._flighttype)
                )

    elif A._flighttype == "ZC":

        # See rule 8.2.3 on VD recovery.

        if A._previousflighttype == "VD":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )

    elif A._flighttype == "SC":

        # See rule 8.1.2 on SC prerequsistes.

        if A.speed() < apcapabilities.minspeed(A) + 1:
            raise RuntimeError("insufficient speed for SC.")

        # See rule 8.2.3 on VD recovery.

        if A._previousflighttype == "VD":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )

    elif A._flighttype == "VC":

        # See rule 8.1.3 on VC prerequisites.

        if _isdivingflight(A._previousflighttype):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )
        if A._previousflighttype == "LVL":
            if not apcapabilities.hasproperty(A, "HPR"):
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (A._previousflighttype, A._flighttype)
                )
            elif A.speed() >= 4.0:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (for HPR aircraft at high speed)."
                    % (A._previousflighttype, A._flighttype)
                )

        # See rule 8.2.3 on VD recovery.

        if A._previousflighttype == "VD":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )

    elif A._flighttype == "SD":

        # See rule 8.1.3 on VC restrictions.
        # See rule 13.3.5 on HRD restrictions.

        if A._previousflighttype == "VC" and not (
            apcapabilities.hasproperty(A, "HPR") or hrd
        ):
            raise RuntimeError(
                "flight type immediately after %s cannot be %s (without a HRD)."
                % (A._previousflighttype, A._flighttype)
            )

    elif A._flighttype == "UD":

        # See rule 8.2.2 on VC restrictions.

        if apvariants.withvariant("use version 2.4 rules"):

            # I interpret the text "start from level flight" to mean that the aircraft
            # must have been in level flight on the previous turn.

            if A._previousflighttype != "LVL":
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (A._previousflighttype, A._flighttype)
                )

        else:

            # See rule 8.1.3 on VC restrictions.

            if A._previousflighttype == "VC" and not apcapabilities.hasproperty(
                A, "HPR"
            ):
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s."
                    % (A._previousflighttype, A._flighttype)
                )

    elif A._flighttype == "VD":

        # See rule 8.2.3 (with errata) on VD restrictions.
        # See rule 13.3.5 on HRD restrictions.

        if A._previousflighttype == "LVL":
            if not hrd:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (without a HRD)."
                    % (A._previousflighttype, A._flighttype)
                )
        elif A._previousflighttype == "ZC" or A._previousflighttype == "SC":
            if hrd and A.speed() > 4.0:
                raise RuntimeError(
                    "flight type immediately after %s cannot be %s (without a low-speed HRD)."
                    % (A._previousflighttype, A._flighttype)
                )
        elif A._previousflighttype == "VC":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )

        # See rule 8.1.3 on VC restrictions. This duplicates the restriction above.

        if A._previousflighttype == "VC":
            raise RuntimeError(
                "flight type immediately after %s cannot be %s."
                % (A._previousflighttype, A._flighttype)
            )


def checkspecialflight(A):
    return


################################################################################


def startnormalflight(A, tasks, note=None):
    """
    Start to carry out normal flight.
    """

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

        if apflight._isturn(A._maneuvertype):

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

    reportapcarry()
    reportaltitudecarry()
    determineallowedturnrates()
    handlecarriedturn()
    checkcloseformationlimits()
    determinemaxfp()
    determinefprequirements()
    determineeffectiveclimbcapability()

    A._logpositionandmaneuver("start")

    continuenormalflight(A, tasks, start=True, note=note)


########################################


def startspecialflight(A, tasks, note=None):

    A._maxfp = A.speed()
    A._logevent("has %.1f FPs." % A._maxfp)

    A._effectiveclimbcapability = apcapabilities.specialclimbcapability(A)
    A._logevent("effective climb capability is %.2f." % A._effectiveclimbcapability)

    A._logpositionandmaneuver("start")

    continuespecialflight(A, tasks, start=True, note=note)


################################################################################


def continuenormalflight(A, tasks, start=False, note=None):
    """
    Continue to carry out out normal flight.
    """

    ########################################

    actiondispatchlist = [
        # This table is searched in order, so put longer actions before shorter
        # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).
        # [0] is the action code.
        # [1] is the action type.
        # [2] is a possible regex to apply
        # [3] is the action procedure.
        ["SLL", "prolog", None, lambda A: dodeclaremaneuver(A, "SL", "L")],
        ["SLR", "prolog", None, lambda A: dodeclaremaneuver(A, "SL", "R")],
        ["DRL", "prolog", None, lambda A: dodeclaremaneuver(A, "DR", "L")],
        ["DRR", "prolog", None, lambda A: dodeclaremaneuver(A, "DR", "R")],
        ["LRL", "prolog", None, lambda A: dodeclaremaneuver(A, "LR", "L")],
        ["LRR", "prolog", None, lambda A: dodeclaremaneuver(A, "LR", "R")],
        ["VRL", "prolog", None, lambda A: dodeclaremaneuver(A, "VR", "L")],
        ["VRR", "prolog", None, lambda A: dodeclaremaneuver(A, "VR", "R")],
        ["EZL", "prolog", None, lambda A: dodeclaremaneuver(A, "EZ", "L")],
        ["TTL", "prolog", None, lambda A: dodeclaremaneuver(A, "TT", "L")],
        ["HTL", "prolog", None, lambda A: dodeclaremaneuver(A, "HT", "L")],
        ["BTL", "prolog", None, lambda A: dodeclaremaneuver(A, "BT", "L")],
        ["ETL", "prolog", None, lambda A: dodeclaremaneuver(A, "ET", "L")],
        ["EZR", "prolog", None, lambda A: dodeclaremaneuver(A, "EZ", "R")],
        ["TTR", "prolog", None, lambda A: dodeclaremaneuver(A, "TT", "R")],
        ["HTR", "prolog", None, lambda A: dodeclaremaneuver(A, "HT", "R")],
        ["BTR", "prolog", None, lambda A: dodeclaremaneuver(A, "BT", "R")],
        ["ETR", "prolog", None, lambda A: dodeclaremaneuver(A, "ET", "R")],
        ["BL", "epilog", None, lambda A: dobank(A, "L")],
        ["BR", "epilog", None, lambda A: dobank(A, "R")],
        ["WL", "epilog", None, lambda A: dobank(A, None)],
        ["L90+", "epilog", None, lambda A: domaneuver(A, "L", 90, True, True)],
        ["L60+", "epilog", None, lambda A: domaneuver(A, "L", 60, True, True)],
        ["L30+", "epilog", None, lambda A: domaneuver(A, "L", 30, True, True)],
        ["LLL+", "epilog", None, lambda A: domaneuver(A, "L", 90, True, True)],
        ["LL+", "epilog", None, lambda A: domaneuver(A, "L", 60, True, True)],
        ["L+", "epilog", None, lambda A: domaneuver(A, "L", None, True, True)],
        ["R90+", "epilog", None, lambda A: domaneuver(A, "R", 90, True, True)],
        ["R60+", "epilog", None, lambda A: domaneuver(A, "R", 60, True, True)],
        ["R30+", "epilog", None, lambda A: domaneuver(A, "R", 30, True, True)],
        ["RRR+", "epilog", None, lambda A: domaneuver(A, "R", 90, True, True)],
        ["RR+", "epilog", None, lambda A: domaneuver(A, "R", 60, True, True)],
        ["R+", "epilog", None, lambda A: domaneuver(A, "R", None, True, True)],
        ["LS180", "epilog", None, lambda A: domaneuver(A, "L", 180, True, False)],
        ["L180", "epilog", None, lambda A: domaneuver(A, "L", 180, False, False)],
        ["L150", "epilog", None, lambda A: domaneuver(A, "L", 150, True, False)],
        ["L120", "epilog", None, lambda A: domaneuver(A, "L", 120, True, False)],
        ["L90", "epilog", None, lambda A: domaneuver(A, "L", 90, True, False)],
        ["L60", "epilog", None, lambda A: domaneuver(A, "L", 60, True, False)],
        ["L30", "epilog", None, lambda A: domaneuver(A, "L", 30, True, False)],
        ["LLL", "epilog", None, lambda A: domaneuver(A, "L", 90, True, False)],
        ["LL", "epilog", None, lambda A: domaneuver(A, "L", 60, True, False)],
        ["L", "epilog", None, lambda A: domaneuver(A, "L", None, True, False)],
        ["RS180", "epilog", None, lambda A: domaneuver(A, "R", 180, True, False)],
        ["R180", "epilog", None, lambda A: domaneuver(A, "R", 180, False, False)],
        ["R150", "epilog", None, lambda A: domaneuver(A, "R", 150, True, False)],
        ["R120", "epilog", None, lambda A: domaneuver(A, "R", 120, True, False)],
        ["R90", "epilog", None, lambda A: domaneuver(A, "R", 90, True, False)],
        ["R60", "epilog", None, lambda A: domaneuver(A, "R", 60, True, False)],
        ["R30", "epilog", None, lambda A: domaneuver(A, "R", 30, True, False)],
        ["RRR", "epilog", None, lambda A: domaneuver(A, "R", 90, True, False)],
        ["RR", "epilog", None, lambda A: domaneuver(A, "R", 60, True, False)],
        ["R", "epilog", None, lambda A: domaneuver(A, "R", None, True, False)],
        ["HC1", "FP", None, lambda A: invalidaction(A, "HC1")],
        ["HC2", "FP", None, lambda A: invalidaction(A, "HC2")],
        ["HCC", "FP", None, lambda A: invalidaction(A, "HCC")],
        ["HC", "FP", None, lambda A: invalidaction(A, "HC")],
        ["HD1", "FP", None, lambda A: dohorizontal(A, "HD")],
        ["HD2", "FP", None, lambda A: invalidaction(A, "HD2")],
        ["HD3", "FP", None, lambda A: invalidaction(A, "HD3")],
        ["HDDD", "FP", None, lambda A: invalidaction(A, "HDDD")],
        ["HDD", "FP", None, lambda A: invalidaction(A, "HDD")],
        ["HD", "FP", None, lambda A: dohorizontal(A, "HD")],
        ["HU", "FP", None, lambda A: dohorizontal(A, "HU")],
        ["H", "FP", None, lambda A: dohorizontal(A, "H")],
        ["C1", "FP", None, lambda A: doclimb(A, 1)],
        ["C2", "FP", None, lambda A: doclimb(A, 2)],
        ["C3", "FP", None, lambda A: doclimb(A, 3)],
        ["CCC", "FP", None, lambda A: doclimb(A, 3)],
        ["CC", "FP", None, lambda A: doclimb(A, 2)],
        ["C", "FP", None, lambda A: doclimb(A, 1)],
        ["D1", "FP", None, lambda A: dodive(A, 1)],
        ["D2", "FP", None, lambda A: dodive(A, 2)],
        ["D3", "FP", None, lambda A: dodive(A, 3)],
        ["DDD", "FP", None, lambda A: dodive(A, 3)],
        ["DD", "FP", None, lambda A: dodive(A, 2)],
        ["D", "FP", None, lambda A: dodive(A, 1)],
        [
            "MDL300",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 300),
        ],
        [
            "MDL270",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 270),
        ],
        [
            "MDL240",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 240),
        ],
        [
            "MDL210",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 210),
        ],
        [
            "MDL180",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 180),
        ],
        [
            "MDL150",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 150),
        ],
        [
            "MDL120",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 120),
        ],
        [
            "MDL90",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 90),
        ],
        [
            "MDL60",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 60),
        ],
        [
            "MDL30",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "L", 30),
        ],
        [
            "MDR300",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 300),
        ],
        [
            "MDR270",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 270),
        ],
        [
            "MDR240",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 240),
        ],
        [
            "MDR210",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 210),
        ],
        [
            "MDR180",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 180),
        ],
        [
            "MDR150",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 150),
        ],
        [
            "MDR120",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 120),
        ],
        [
            "MDR90",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 90),
        ],
        [
            "MDR60",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 60),
        ],
        [
            "MDR30",
            "maneuvering departure",
            None,
            lambda A: domaneuveringdeparture(A, "R", 30),
        ],
        ["", "", None, None],
    ]

    ################################################################################

    def afterFP(E):

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

    ################################################################################

    def aftertask(A):

        # See rules 7.7 and 8.5.
        if A._hasmaneuvered and A._hasrolled:
            if A._taskaltitude > apcapabilities.ceiling(A):
                A._logevent(
                    "check for a maneuvering departure as the aircraft is above its ceiling and attempted to roll."
                )
            elif A._taskaltitudeband == "EH" or A._taskaltitudeband == "UH":
                A._logevent(
                    "check for a maneuvering departure as the aircraft is in the %s altitude band and attempted to roll."
                    % A._taskaltitudeband
                )

        # See rules 7.7 and 8.5.
        if A._hasmaneuvered and A._hasturned:
            if (
                A._taskaltitude > apcapabilities.ceiling(A)
                and A._taskmaneuvertype != "EZ"
            ):
                A._logevent(
                    "check for a maneuvering departure as the aircraft is above its ceiling and attempted to turn harder than EZ."
                )
            if A._taskmaneuvertype == "ET" and A._taskaltitude <= 25:
                A._gloccheck += 1
                A._logevent(
                    "check for GLOC as turn rate is ET and altitude band is %s (check %d in cycle)."
                    % (A._taskaltitudeband, A._gloccheck)
                )

        # See rule 7.8.
        if A._hasturned and apcloseformation.size(A) != 0:
            if (
                (apcloseformation.size(A) > 2 and A._taskmaneuvertype == "HT")
                or A._taskmaneuvertype == "BT"
                or A._taskmaneuvertype == "ET"
            ):
                A._logevent(
                    "close formation breaks down as the turn rate is %s."
                    % A._taskmaneuvertype
                )
                apcloseformation.breakdown(A)

        # See rule 13.7, interpreted in the same sense as rule 7.8.
        if A._hasrolled and apcloseformation.size(A) != 0:
            A._logevent("close formation breaks down aircraft is rolling.")
            apcloseformation.breakdown(A)

    apflight.dotasks(
        A,
        tasks,
        actiondispatchlist,
        start=start,
        afterFP=afterFP,
        aftertask=aftertask,
    )

    A._lognote(note)

    assert A._maneuveringdeparture or (A._fp == A._hfp + A._vfp)
    assert A._maneuveringdeparture or (A._fp <= A._maxfp)

    if A.killed() or A.removed() or A._maneuveringdeparture:

        endmove(A)

    elif A._fp >= A._maxfp:

        endnormalflight(A)


########################################


def continuespecialflight(A, tasks, start=False, note=None):
    """
    Continue to carry out out special flight.
    """

    ########################################

    def dostationary(A):
        """
        Stay stationary.
        """

        A._fp += 1

    ########################################

    def doturn(A, sense, facingchange):
        """
        Turn in the specified sense and amount.
        """

        A._moveturn(sense, facingchange)

    ########################################

    taskdispatchlist = [
        # This table is searched in order, so put longer elements before shorter
        # ones that are prefixes (e.g., put C2 before C).
        ["L180", "epilog", None, lambda A: doturn(A, "L", 180)],
        ["L150", "epilog", None, lambda A: doturn(A, "L", 150)],
        ["L120", "epilog", None, lambda A: doturn(A, "L", 120)],
        ["L90", "epilog", None, lambda A: doturn(A, "L", 90)],
        ["L60", "epilog", None, lambda A: doturn(A, "L", 60)],
        ["L30", "epilog", None, lambda A: doturn(A, "L", 30)],
        ["LLL", "epilog", None, lambda A: doturn(A, "L", 90)],
        ["LL", "epilog", None, lambda A: doturn(A, "L", 60)],
        ["L", "epilog", None, lambda A: doturn(A, "L", 30)],
        ["R180", "epilog", None, lambda A: doturn(A, "R", 180)],
        ["R150", "epilog", None, lambda A: doturn(A, "R", 150)],
        ["R120", "epilog", None, lambda A: doturn(A, "R", 120)],
        ["R90", "epilog", None, lambda A: doturn(A, "R", 90)],
        ["R60", "epilog", None, lambda A: doturn(A, "R", 60)],
        ["R30", "epilog", None, lambda A: doturn(A, "R", 30)],
        ["RRR", "epilog", None, lambda A: doturn(A, "R", 90)],
        ["RR", "epilog", None, lambda A: doturn(A, "R", 60)],
        ["R", "epilog", None, lambda A: doturn(A, "R", 30)],
        ["S", "FP", None, lambda A: dostationary(A)],
        ["H", "FP", None, lambda A: dohorizontal(A, "H")],
        ["HD", "FP", None, lambda A: dohorizontal(A, "HD")],
        ["C1", "FP", None, lambda A: doclimb(A, 1)],
        ["C2", "FP", None, lambda A: doclimb(A, 2)],
        ["CC", "FP", None, lambda A: doclimb(A, 2)],
        ["C", "FP", None, lambda A: doclimb(A, 1)],
        ["D1", "FP", None, lambda A: dodive(A, 1)],
        ["D2", "FP", None, lambda A: dodive(A, 2)],
        ["D3", "FP", None, lambda A: dodive(A, 3)],
        ["DDD", "FP", None, lambda A: dodive(A, 3)],
        ["DD", "FP", None, lambda A: dodive(A, 2)],
        ["D", "FP", None, lambda A: dodive(A, 1)],
    ]

    ########################################

    apflight.dotasks(A, tasks, taskdispatchlist, start=start)

    A._lognote(note)

    if not A.killed() and not A.removed():
        if A._altitudecarry != 0:
            A._logend("is carrying %.2f altitude levels." % A._altitudecarry)

    A._newspeed = A.speed()

    if A.killed() or A.removed() or A._fp + 1 > A._maxfp:

        endmove(A)


################################################################################


def endnormalflight(A):

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

    endmove(A)


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


def invalidaction(A, action):
    raise RuntimeError("%r is not a valid action." % action)


########################################


def dohorizontal(A, action):
    """
    Move horizontally.
    """

    altitudechange = 0

    if A._maneuvertype == "VR":
        raise RuntimeError("attempt to declare a vertical roll during an HFP.")

    if action == "HD":

        if A._flighttype == "LVL" or A._flighttype == "SP":
            altitudechange = 1
        else:
            raise RuntimeError(
                "%r is not a valid action when the flight type is %s."
                % (action, A._flighttype)
            )

    elif action == "HU":

        if A._flighttype != "UD":
            raise RuntimeError(
                "%r is not a valid action when the flight type is %s."
                % (action, A._flighttype)
            )

        A._hasunloaded = True
        A._unloadedhfp += 1
        if A._firstunloadedfp == None:
            A._firstunloadedfp = A._hfp
        A._lastunloadedfp = A._hfp

        if math.floor(A._maxfp) == 1:
            # Both half FPs and all FPs.
            altitudechange = 2
        elif A._unloadedhfp == math.floor(A._maxfp / 2):
            altitudechange = 1
        elif A._unloadedhfp == math.floor(A._maxfp):
            altitudechange = 1

    A._horizontal = True
    A._fp += 1
    A._hfp += 1

    A._movedive(altitudechange)
    A._moveforward()


########################################


def doclimb(A, altitudechange):
    """
    Climb.
    """

    def determinealtitudechange(altitudechange):

        assert altitudechange == 1 or altitudechange == 2 or altitudechange == 3

        climbcapability = A._effectiveclimbcapability

        if A._flighttype == "SP":

            if altitudechange == 1:
                altitudechange = climbcapability

        elif A._flighttype == "ZC":

            # See rule 8.1.1.
            if altitudechange == 2:
                if climbcapability <= 2.0:
                    raise RuntimeError("invalid altitude change in climb.")
            elif altitudechange == 3:
                if climbcapability < 6.0:
                    raise RuntimeError("invalid altitude change in climb.")
                if A._usedsuperclimb:
                    raise RuntimeError("invalid altitude change in climb.")
                A._usedsuperclimb = True

        elif A._flighttype == "SC":

            # See rule 8.1.2.
            if climbcapability < 2.0 and altitudechange == 2:
                raise RuntimeError("invalid altitude change in climb.")
            if A._vfp == 0 and climbcapability % 1 != 0:
                # First VFP with fractional climb capability.
                altitudechange = climbcapability % 1

        elif A._flighttype == "VC":

            # See rule 8.1.3.
            if altitudechange != 1 and altitudechange != 2:
                raise RuntimeError("invalid altitude change in climb.")

        else:

            # See rule 8.0.
            raise RuntimeError(
                "attempt to climb while flight type is %s." % A._flighttype
            )

        return altitudechange

    if A._flighttype != "SP" and A._hfp < A._mininitialhfp:
        raise RuntimeError("insufficient initial HFPs.")

    altitudechange = determinealtitudechange(altitudechange)

    A._vertical = True
    A._fp += 1
    A._vfp += 1

    A._moveclimb(altitudechange)

    # See rule 8.5.
    if A._flighttype == "SC" and A.altitude() > apcapabilities.ceiling(A):
        raise RuntimeError("attempt to climb above ceiling in SC.")


########################################


def dodive(A, altitudechange):
    """
    Dive.
    """

    def checkaltitudechange():

        assert altitudechange == 1 or altitudechange == 2 or altitudechange == 3

        if A._flighttype == "SP":

            pass

        elif A._flighttype == "SD":

            # See rule 8.2.1.
            if altitudechange != 1 and altitudechange != 2:
                raise RuntimeError(
                    "attempt to dive %d levels per VFP while the flight type is SC."
                    % altitudechange
                )

        elif A._flighttype == "UD":

            # See rule 8.2.2.
            if altitudechange != 1:
                raise RuntimeError(
                    "attempt to dive %d levels per unloaded HFP while the flight type is UL."
                    % altitudechange
                )

        elif A._flighttype == "VD":

            # See rule 8.2.3.
            if altitudechange != 2 and altitudechange != 3:
                raise RuntimeError(
                    "attempt to dive %s per VFP while the flight type is VD."
                    % plural(altitudechange, "1 level", "%d levels" % altitudechange)
                )

        elif A._flighttype == "LVL":

            # See rule 8.2.4.
            if altitudechange != 1:
                raise RuntimeError(
                    "attempt to descend %d levels while flight type is LVL."
                    % altitudechange
                )

        else:

            # See rule 8.0.
            raise RuntimeError(
                "attempt to dive while flight type is %s." % A._flighttype
            )

    checkaltitudechange()

    if A._flighttype != "SP" and A._hfp < A._mininitialhfp:
        raise RuntimeError("insufficient initial HFPs.")

    A._vertical = True
    A._fp += 1
    A._vfp += 1

    A._movedive(altitudechange)


########################################


def dobank(A, sense):

    if A._hasbanked:
        raise RuntimeError("attempt to bank twice.")

    # See rule 7.4.
    if apcapabilities.hasproperty(A, "LRR"):
        if (A._bank == "L" and sense == "R") or (A._bank == "R" and sense == "L"):
            raise RuntimeError(
                "attempt to bank to %s while banked to %s in a LRR aircraft."
                % (sense, A._bank)
            )

    A._bank = sense
    if apflight._isturn(A._maneuvertype):
        A._maneuvertype = None
        A._maneuversense = None
        A._maneuverfacingchange = None
        A._maneuverfp = 0

    A._hasbanked = True


########################################


def dodeclareturn(A, turnrate, sense):
    """
    Declare the start of turn in the specified direction and rate.
    """

    # See rule 8.1.3 and 8.2.3
    if A._flighttype == "VC" or A._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare turn while flight type is %s." % A._flighttype
        )

    # See rule 7.1.

    # Check the bank. See rule 7.4.
    if apcapabilities.hasproperty(A, "LRR"):
        if A._bank != sense:
            raise RuntimeError(
                "attempt to declare a turn to %s while not banked to %s in a LRR aircraft."
                % (sense, sense)
            )
    elif not apcapabilities.hasproperty(A, "HRR"):
        if (A._bank == "L" and sense == "R") or (A._bank == "R" and sense == "L"):
            raise RuntimeError(
                "attempt to declare a turn to %s while banked to %s." % (sense, A._bank)
            )

    if A._allowedturnrates == []:
        raise RuntimeError("turns are forbidded.")

    if turnrate not in A._allowedturnrates:
        raise RuntimeError(
            "attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type."
        )

    turnrateap = apcapabilities.turndrag(A, turnrate)
    if turnrateap == None:
        raise RuntimeError(
            "attempt to declare a turn rate tighter than allowed by the aircraft."
        )

    # Determine the maximum turn rate.
    if A._maxturnrate == None:
        A._maxturnrate = turnrate
    else:
        turnrates = ["EZ", "TT", "HT", "BT", "ET"]
        A._maxturnrate = turnrates[
            max(turnrates.index(turnrate), turnrates.index(A._maxturnrate))
        ]

    A._bank = sense
    A._maneuvertype = turnrate
    A._maneuversense = sense
    A._maneuverfp = 0
    A._maneuversupersonic = A.speed() >= apspeed.m1speed(A.altitudeband())
    turnrequirement = apturnrate.turnrequirement(
        A.altitudeband(), A.speed(), A._maneuvertype
    )
    if turnrequirement == None:
        raise RuntimeError(
            "attempt to declare a turn rate tighter than allowed by the speed and altitude."
        )
    if turnrequirement >= 60:
        A._maneuverrequiredfp = 1
        A._maneuverfacingchange = turnrequirement
    else:
        A._maneuverrequiredfp = turnrequirement
        A._maneuverfacingchange = 30

    if apvariants.withvariant("use house rules"):
        A._turnrateap -= turnrateap
        if A._maneuversupersonic:
            if apcapabilities.hasproperty(A, "PSSM"):
                A._turnrateap -= 1.0
            elif not apcapabilities.hasproperty(A, "GSSM"):
                A._turnrateap -= 0.5


########################################


def doturn(A, sense, facingchange, continuous):
    """
    Turn in the specified sense and amount.
    """

    # See rule 8.1.3 and 8.2.3
    if A._flighttype == "VC" or A._flighttype == "VD":
        raise RuntimeError("attempt to turn while flight type is %s." % A._flighttype)

    # See rule 7.1.
    if A._maneuverfp < A._maneuverrequiredfp or facingchange > A._maneuverfacingchange:
        raise RuntimeError("attempt to turn faster than the declared turn rate.")

    # See Hack's article in APJ 36
    if A._turnmaneuvers == 0:
        sustainedfacingchanges = facingchange // 30 - 1
    else:
        sustainedfacingchanges = facingchange // 30

    if apvariants.withvariant("use house rules"):
        pass
    else:
        if apcapabilities.hasproperty(A, "LBR"):
            A._sustainedturnap -= sustainedfacingchanges * 0.5
        elif apcapabilities.hasproperty(A, "HBR"):
            A._sustainedturnap -= sustainedfacingchanges * 1.5
        else:
            A._sustainedturnap -= sustainedfacingchanges * 1.0

    A._turnmaneuvers += 1

    A._moveturn(sense, facingchange)


########################################


def dodeclareslide(A, sense):

    # See rule 8.1.3 and 8.2.3
    if A._flighttype == "VC" or A._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare slide while flight type is %s." % A._flighttype
        )

    # See rules 13.1 and 13.2.

    if A._slides == 1 and A.speed() <= 9.0:
        raise RuntimeError("only one slide allowed per turn at low speed.")
    if A._slides == 1 and A._fp - A._slidefp < 4:
        raise RuntimeError(
            "attempt to start a second slide without sufficient intermediate FPs."
        )
    elif A._slides == 2:
        raise RuntimeError("at most two slides allowed per turn.")

    A._bank = None
    A._maneuvertype = "SL"
    A._maneuversense = sense
    A._maneuverfacingchange = None
    A._maneuverfp = 0
    A._maneuversupersonic = A.speed() >= apspeed.m1speed(A.altitudeband())
    # The requirement has +1 FP to account for the final H.
    A._maneuverrequiredfp = 2 + extrapreparatoryhfp(A) + 1


########################################


def extrapreparatoryhfp(A):

    # See rule 13.1.

    extrapreparatoryfp = {
        "LO": 0,
        "ML": 0,
        "MH": 0,
        "HI": 1,
        "VH": 2,
        "EH": 3,
        "UH": 4,
    }[A.altitudeband()]

    if A.speed() >= apspeed.m1speed(A.altitudeband()):
        extrapreparatoryfp += 1.0

    # See "Aircraft Damage Effects" in the Play Aids.

    if A.damageatleast("2L"):
        extrapreparatoryfp += 1.0

    return extrapreparatoryfp


########################################


def doslide(A, sense):

    # See rule 8.1.3 and 8.2.3
    if A._flighttype == "VC" or A._flighttype == "VD":
        raise RuntimeError("attempt to slide while flight type is %s." % A._flighttype)

    # See rules 13.1 and 13.2.

    if A._maneuverfp < A._maneuverrequiredfp:
        raise RuntimeError("attempt to slide without sufficient preparatory HFPs.")

    # Move.
    A._moveslide(sense)

    # See rule 13.2.
    if not apvariants.withvariant("use house rules"):
        if A._slides >= 1:
            A._othermaneuversap -= 1.0

    # Keep track of the number of slides and the FP of the last slide.
    A._slides += 1
    A._slidefp = A._fp

    # Implicitly finish with wings level.
    A._bank = None


########################################


def dodeclaredisplacementroll(A, sense):

    # See rules 13.1 and 13.3.1.

    if apcapabilities.hasproperty(A, "NRM"):
        raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if apcapabilities.rolldrag(A, "DR") == None:
        raise RuntimeError("aircraft cannot perform displacement rolls.")

    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if A._flighttype == "SC" or A._flighttype == "VC" or A._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare a displacement roll while flight type is %s."
            % A._flighttype
        )

    A._bank = None
    A._maneuvertype = "DR"
    A._maneuversense = sense
    A._maneuverfacingchange = None
    A._maneuverfp = 0
    A._maneuversupersonic = A.speed() >= apspeed.m1speed(A.altitudeband())
    # The requirement includes the FPs used to execute the roll.
    A._maneuverrequiredfp = (
        apcapabilities.rollhfp(A) + extrapreparatoryhfp(A) + rounddown(A.speed() / 3)
    )

    # See rules 13.3.1 and 6.6.
    if apvariants.withvariant("use house rules"):
        A._othermaneuversap -= apcapabilities.rolldrag(A, "DR")
        if A._maneuversupersonic:
            if apcapabilities.hasproperty(A, "PSSM"):
                A._othermaneuversap -= 2.0
            elif not apcapabilities.hasproperty(A, "GSSM"):
                A._othermaneuversap -= 1.0


########################################


def dodisplacementroll(A, sense):

    # See rules 13.1 and 13.3.1.

    if A._maneuverfp < A._maneuverrequiredfp:
        raise RuntimeError("attempt to roll without sufficient preparatory FPs.")

    if not A._horizontal:
        raise RuntimeError("attempt to roll on a VFP.")

    # Move.
    A._movedisplacementroll(sense)

    # See rule 13.3.1.
    if not apvariants.withvariant("use house rules"):
        A._othermaneuversap -= apcapabilities.rolldrag(A, "DR")

    # See rule 6.6.
    if A._maneuversupersonic:
        if apcapabilities.hasproperty(A, "PSSM"):
            A._othermaneuversap -= 2.0
        elif not apcapabilities.hasproperty(A, "GSSM"):
            A._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if not apvariants.withvariant("use house rules"):
        if A._rollmaneuvers > 0:
            A._othermaneuversap -= 1.0
        A._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    A._bank = None


########################################


def dodeclarelagroll(A, sense):

    # See rule 13.3.2.

    if apcapabilities.hasproperty(A, "NRM"):
        raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if apcapabilities.rolldrag(A, "LR") == None:
        raise RuntimeError("aircraft cannot perform lag rolls.")

    # See rules 8.1.2, 8.1.3, and 8.2.3.
    if A._flighttype == "SC" or A._flighttype == "VC" or A._flighttype == "VD":
        raise RuntimeError(
            "attempt to declare a lag roll while flight type is %s." % A._flighttype
        )

    A._bank = None
    A._maneuvertype = "LR"
    A._maneuversense = sense
    A._maneuverfacingchange = None
    A._maneuverfp = 0
    A._maneuversupersonic = A.speed() >= apspeed.m1speed(A.altitudeband())
    # The requirement includes the FPs used to execute the roll.
    A._maneuverrequiredfp = (
        apcapabilities.rollhfp(A) + extrapreparatoryhfp(A) + rounddown(A.speed() / 3)
    )

    # See rules 13.3.1 and 6.6.
    if apvariants.withvariant("use house rules"):
        A._othermaneuversap -= apcapabilities.rolldrag(A, "LR")
        if A._maneuversupersonic:
            if apcapabilities.hasproperty(A, "PSSM"):
                A._othermaneuversap -= 2.0
            elif not apcapabilities.hasproperty(A, "GSSM"):
                A._othermaneuversap -= 1.0


########################################


def dolagroll(A, sense):

    # See rules 13.1 and 13.3.2.

    if A._maneuverfp < A._maneuverrequiredfp:
        raise RuntimeError("attempt to roll without sufficient preparatory FPs.")

    if not A._horizontal:
        raise RuntimeError("attempt to roll on a VFP.")

    # Move.
    A._movelagroll(sense)

    # See rule 13.3.1.
    if not apvariants.withvariant("use house rules"):
        A._othermaneuversap -= apcapabilities.rolldrag(A, "LR")

    # See rule 6.6.
    if A._maneuversupersonic:
        if apcapabilities.hasproperty(A, "PSSM"):
            A._othermaneuversap -= 2.0
        elif not apcapabilities.hasproperty(A, "GSSM"):
            A._othermaneuversap -= 1.0

    # See rule 13.3.6.
    if not apvariants.withvariant("use house rules"):
        if A._rollmaneuvers > 0:
            A._othermaneuversap -= 1.0
        A._rollmaneuvers += 1

    # Implicitly finish with wings level. This can be changed immediately by a bank.
    A._bank = None


########################################


def dodeclareverticalroll(A, sense):

    if apcapabilities.hasproperty(A, "NRM"):
        raise RuntimeError("aircraft cannot perform rolling maneuvers.")
    if A._verticalrolls == 1 and apcapabilities.hasproperty(A, "OVR"):
        raise RuntimeError("aircraft can only perform one vertical roll per turn.")

    # See rule 13.3.4.
    if A._flighttype != "VC" and A._flighttype != "VD":
        raise RuntimeError(
            "attempt to declare a vertical roll while flight type is %s."
            % A._flighttype
        )
    if A._previousflighttype == "LVL" and A._flighttype == "VC" and not A._lastfp:
        raise RuntimeError(
            "attempt to declare a vertical roll in VC following LVL flight other than on the last FP."
        )

    # See rule 13.3.5.
    if A._hrd and not A._lastfp:
        raise RuntimeError(
            "attempt to declare a vertical roll after HRD other than on the last FP."
        )

    A._bank = None
    A._maneuvertype = "VR"
    A._maneuversense = sense
    A._maneuverfacingchange = None
    A._maneuverfp = 0
    A._maneuversupersonic = A.speed() >= apspeed.m1speed(A.altitudeband())
    A._maneuverrequiredfp = 1

    # See rules 6.6 and 13.3.6
    if apvariants.withvariant("use house rules"):
        A._othermaneuversap -= apcapabilities.rolldrag(A, "VR")
        if A._maneuversupersonic:
            if apcapabilities.hasproperty(A, "PSSM"):
                A._othermaneuversap -= 2.0
            elif not apcapabilities.hasproperty(A, "GSSM"):
                A._othermaneuversap -= 1.0


########################################


def doverticalroll(A, sense, facingchange, shift):

    if A._maneuverfp < A._maneuverrequiredfp:
        raise RuntimeError("attempt to roll without sufficient preparatory HFPs.")

    # See rule 13.3.4.
    if apcapabilities.hasproperty(A, "LRR") and facingchange > 90:
        raise RuntimeError(
            "attempt to roll vertically by more than 90 degrees in LRR aircraft."
        )

    if not apvariants.withvariant("use house rules"):
        A._othermaneuversap -= apcapabilities.rolldrag(A, "VR")

    # See rule 13.3.6
    if not apvariants.withvariant("use house rules"):
        if A._rollmaneuvers > 0:
            A._othermaneuversap -= 1
    A._rollmaneuvers += 1
    A._verticalrolls += 1

    # See rule 6.6.
    if not apvariants.withvariant("use house rules"):
        if A._maneuversupersonic:
            if apcapabilities.hasproperty(A, "PSSM"):
                A._othermaneuversap -= 2.0
            elif not apcapabilities.hasproperty(A, "GSSM"):
                A._othermaneuversap -= 1.0

    # Move.
    A._moveverticalroll(sense, facingchange, shift)


########################################


def dodeclaremaneuver(A, maneuvertype, sense):

    if A._hasdeclaredamaneuver:
        raise RuntimeError("attempt to declare a second maneuver.")

    if maneuvertype == "SL":
        dodeclareslide(A, sense)
    elif maneuvertype == "DR":
        dodeclaredisplacementroll(A, sense)
    elif maneuvertype == "LR":
        dodeclarelagroll(A, sense)
    elif maneuvertype == "VR":
        dodeclareverticalroll(A, sense)
    else:
        dodeclareturn(A, maneuvertype, sense)

    A._logevent("declared %s." % A.maneuver())
    A._hasdeclaredamaneuver = True


########################################


def domaneuver(A, sense, facingchange, shift, continuous):

    if A._maneuvertype == None:
        raise RuntimeError("attempt to maneuver without a declaration.")

    if A._maneuversense != sense:
        raise RuntimeError("attempt to maneuver against the sense of the declaration.")

    if A._maneuvertype == "SL":
        if facingchange != None:
            raise RuntimeError("invalid action for a slide.")
        doslide(A, sense)
    elif A._maneuvertype == "DR":
        if facingchange != None:
            raise RuntimeError("invalid action for a displacement roll.")
        dodisplacementroll(A, sense)
    elif A._maneuvertype == "LR":
        if facingchange != None:
            raise RuntimeError("invalid action for a lag roll.")
        dolagroll(A, sense)
    elif A._maneuvertype == "VR":
        if facingchange == None:
            facingchange = 30
        doverticalroll(A, sense, facingchange, shift)
    else:
        if facingchange == None:
            facingchange = 30
        doturn(A, sense, facingchange, continuous)

    A._hasmaneuvered = True
    A._maneuverfp = 0

    if not continuous:
        A._maneuvertype = None
        A._maneuversense = None
        A._maneuverfacingchange = None
        A._maneuverrequiredfp = 0
        A._maneuversupersonic = False
    else:
        A._hasdeclaredamaneuver = False
        dodeclaremaneuver(A, A._maneuvertype, A._maneuversense)


########################################


def domaneuveringdeparture(A, sense, facingchange):

    # Do the first facing change.
    A._moveturn(sense, 30)
    A._extendpath()
    facingchange -= 30

    # Shift.

    shift = int((A._maxfp - A._fp) / 2)
    for i in range(0, shift):
        A._moveforward()
        A._extendpath()
        A._checkforterraincollision()
        A._checkforleavingmap()
        if A.killed() or A.removed():
            return

    # Do any remaining facing changes.
    A._moveturn(sense, facingchange)
    A._extendpath()


########################################
