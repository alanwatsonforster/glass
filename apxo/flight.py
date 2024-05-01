import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.hex as aphex
import apxo.variants as apvariants

from apxo.log import plural

import re

################################################################################


def dotasks(E, tasks, actiondispatchlist):

    if tasks != "":
        for task in tasks.split(","):
            if not E._destroyed and not E._leftmap:
                dotask(E, task, actiondispatchlist)


################################################################################


def dotask(E, task, actiondispatchlist):
    """
    Carry out an task for normal flight.
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
            elif apvariants.withvariant("use version 2.4 rules") and (
                E._maneuvertype == "DR" or E._maneuvertype == "LR"
            ):
                E._maneuverfp += 1
            elif E._horizontal:
                E._maneuverfp += 1

        if E._hasturned and E._maneuversupersonic:
            E._turningsupersonic = True

        _checkrecovery(E)
        _checktracking(E)

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

    _aftertask(E)

    if E._taskaltitudeband != E.altitudeband():
        E._logevent(
            "altitude band changed from %s to %s."
            % (E._taskaltitudeband, E.altitudeband())
        )

    E._checkforterraincollision()
    E._checkforleavingmap()
    if E._destroyed or E._leftmap:
        return


################################################################################


def doactions(E, task, actiondispatchlist, selectedactiontype):
    """
    Carry out the actions in an task that match the action type.
    """

    while task != "":

        if task[0] == "/" or task[0] == " ":
            task = task[1:]
            continue

        for action in actiondispatchlist:

            actioncode = action[0]
            actiontype = action[1]
            actionregex = action[2]
            actionprocedure = action[3]

            if actioncode == task[: len(actioncode)]:
                break

        if selectedactiontype == "prolog" and actiontype == "epilog":
            raise RuntimeError("unexpected %s action in task prolog." % actioncode)
        if selectedactiontype == "epilog" and actiontype == "prolog":
            raise RuntimeError("unexpected %s action in task epilog." % actioncode)

        if selectedactiontype != actiontype:
            break

        if actionprocedure is None:
            break

        task = task[len(actioncode) :]

        if actionregex == None:
            actionprocedure(E)
        else:
            m = re.compile(actionregex).match(task)
            if not m:
                raise RuntimeError("invalid arguments to %s action." % actioncode)
            task = task[len(m.group()) :]
            actionprocedure(E, m)

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


################################################################################


def _aftertask(A):

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


def _checkrecovery(A):

    # See rules 9.1 and 13.3.6. The +1 is because the recovery period is
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


################################################################################


def _checktracking(A):

    # See rule 9.4.
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
