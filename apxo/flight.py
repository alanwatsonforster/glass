import re

import apxo.airtoair as apairtoair
import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.hex as aphex
import apxo.variants as apvariants

from apxo.log import plural

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


################################################################################
