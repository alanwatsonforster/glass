import apxo.altitude as apaltitude
import apxo.gameturn as apgameturn
import apxo.geometry as apgeometry
import apxo.hex as aphex
import apxo.speed as apspeed

################################################################################


def _startmove(M, **kwargs):
    """
    Start a move and possibly carry out some actions.
    """

    M._logposition("start")

    M._fp = 0
    M._hfp = 0
    M._vfp = 0


def _continuemove(M, actions, **kwargs):

    if M.speed() < minspeed(M.altitudeband()):
        M._logevent("has stalled.")
        if actions != "":
            raise RuntimeError("invalid actions %r for stalled missile." % actions)
        M._remove()
        M._logevent("has been removed.")
        M._finishedmoving = True
        return

    startaltitude = M.altitude()
    starthfp = M._hfp

    _doactions(M, actions)

    endaltitude = M.altitude()
    endhfp = M._hfp

    slopenumerator = endaltitude - startaltitude
    slopedenominator = endhfp - starthfp
    M._logevent("flight slope is %+d/%d." % (slopenumerator, slopedenominator))

    horizontalrange = apgeometry.horizontalrange(M, M._target)
    M._logevent("horizontal range is %d." % horizontalrange)

    altitudedifference = M._target.altitude() - M.altitude()
    M._logevent("altitude difference is %+d." % altitudedifference)

    def checknormallimit(minf, maxf):
        minaltitudedifference = int(minf * horizontalrange)
        maxaltitudedifference = int(maxf * horizontalrange)
        M._logevent(
            "the allowed altitude difference range is [%+d,%+d]."
            % (minaltitudedifference, maxaltitudedifference)
        )
        if (
            altitudedifference < minaltitudedifference
            or altitudedifference > maxaltitudedifference
        ):
            M._logevent("the target is not within the seeker vertical limits.")
        else:
            M._logevent("the target is within the seeker vertical limits.")

    if slopenumerator < -3 * slopedenominator:
        pass
    elif slopenumerator < -1 * slopedenominator:
        checknormallimit(-7.0, -0.5)
    elif slopenumerator < 0:
        checknormallimit(-2.0, +0.5)
    elif slopenumerator == 0:
        checknormallimit(-1.0, +1.0)
    elif slopenumerator <= +1 * slopedenominator:
        checknormallimit(-0.5, +2.0)
    elif abs(slopenumerator) <= 3 * slopedenominator:
        checknormallimit(+0.5, +7.0)
    else:
        pass


################################################################################


def _doactions(M, actions):
    if actions != "":
        for action in actions.split(","):
            if not M.removed():
                _doaction(M, action)


################################################################################


def _doaction(M, action):
    """
    Carry out out missile flight.
    """

    ########################################

    def dohorizontal(element):
        """
        Move horizontally.
        """

        M._fp += 1
        M._hfp += 1

        if element == "HD":
            M._movedive(1)

        M._moveforward()

    ########################################

    def doclimb(altitudechange):
        """
        Climb.
        """

        M._fp += 1
        M._vfp += 1

        M._moveclimb(altitudechange)

    ########################################

    def dodive(altitudechange):
        """
        Dive.
        """

        M._fp += 1
        M._vfp += 1

        M._movedive(altitudechange)

    ########################################

    def dodeclaremaneuver(maneuvertype, sense):
        M._maneuvertype = maneuvertype
        M._maneuversense = sense

    ########################################

    def domaneuver(sense, facingchange, shift, continuous):

        if M._maneuvertype == None:
            raise RuntimeError("attempt to maneuver without a declaration.")

        if M._maneuversense != sense:
            raise RuntimeError(
                "attempt to maneuver against the sense of the declaration."
            )

        assert (
            M._maneuvertype == "SL" or M._maneuvertype == "T" or M._maneuvertype == "VR"
        )

        if M._maneuvertype == "SL":

            M._moveslide(sense)

        elif M._maneuvertype == "VR":

            M._moveverticalroll(sense, facingchange, shift)

        else:

            M._moveturn(sense, facingchange)

        if not continuous:
            M._maneuvertype = None
            M._maneuversense = None

    ########################################

    elementdispatchlist = [
        # This table is searched in order, so put longer elements before shorter
        # ones that are prefixes (e.g., put C2 before C).
        ["SLL", lambda: dodeclaremaneuver("SL", "L")],
        ["SLR", lambda: dodeclaremaneuver("SL", "R")],
        ["VRL", lambda: dodeclaremaneuver("VR", "L")],
        ["VRR", lambda: dodeclaremaneuver("VR", "R")],
        ["TL", lambda: dodeclaremaneuver("T", "L")],
        ["TR", lambda: dodeclaremaneuver("T", "R")],
        ["L90+", lambda: domaneuver("L", 90, True, True)],
        ["L60+", lambda: domaneuver("L", 60, True, True)],
        ["L30+", lambda: domaneuver("L", 30, True, True)],
        ["LLL+", lambda: domaneuver("L", 90, True, True)],
        ["LL+", lambda: domaneuver("L", 60, True, True)],
        ["L+", lambda: domaneuver("L", 30, True, True)],
        ["R90+", lambda: domaneuver("R", 90, True, True)],
        ["R60+", lambda: domaneuver("R", 60, True, True)],
        ["R30+", lambda: domaneuver("R", 30, True, True)],
        ["RRR+", lambda: domaneuver("R", 90, True, True)],
        ["RR+", lambda: domaneuver("R", 60, True, True)],
        ["R+", lambda: domaneuver("R", 30, True, True)],
        ["LS180", lambda: domaneuver("L", 180, True, False)],
        ["L180", lambda: domaneuver("L", 180, False, False)],
        ["L150", lambda: domaneuver("L", 150, True, False)],
        ["L120", lambda: domaneuver("L", 120, True, False, False)],
        ["L90", lambda: domaneuver("L", 90, True, False)],
        ["L60", lambda: domaneuver("L", 60, True, False)],
        ["L30", lambda: domaneuver("L", 30, True, False)],
        ["LLL", lambda: domaneuver("L", 90, True, False)],
        ["LL", lambda: domaneuver("L", 60, True, False)],
        ["L", lambda: domaneuver("L", 30, True, False)],
        ["RS180", lambda: domaneuver("R", 180, True, False)],
        ["R180", lambda: domaneuver("R", 180, False, False)],
        ["R150", lambda: domaneuver("R", 150, True, False)],
        ["R120", lambda: domaneuver("R", 120, True, False)],
        ["R90", lambda: domaneuver("R", 90, True, False)],
        ["R60", lambda: domaneuver("R", 60, True, False)],
        ["R30", lambda: domaneuver("R", 30, True, False)],
        ["RRR", lambda: domaneuver("R", 90, True, False)],
        ["RR", lambda: domaneuver("R", 60, True, False)],
        ["R", lambda: domaneuver("R", 30, True, False)],
        ["HD", lambda: dohorizontal("HD")],
        ["H", lambda: dohorizontal("H")],
        ["C1", lambda: doclimb(1)],
        ["C2", lambda: doclimb(2)],
        ["CC", lambda: doclimb(2)],
        ["C", lambda: doclimb(1)],
        ["D1", lambda: dodive(1)],
        ["D2", lambda: dodive(2)],
        ["D3", lambda: dodive(3)],
        ["DDD", lambda: dodive(3)],
        ["DD", lambda: dodive(2)],
        ["D", lambda: dodive(1)],
        ["/", lambda: None],
    ]

    ########################################

    M._logaction("FP %d" % (M._fp + 1), action)

    initialaltitude = M.altitude()
    initialaltitudeband = M.altitudeband()

    fp = M._fp

    remainingaction = action

    while remainingaction != "":

        for element in elementdispatchlist:

            elementcode = element[0]
            elementprocedure = element[1]

            if (
                len(elementcode) <= len(remainingaction)
                and elementcode == remainingaction[: len(elementcode)]
            ):
                elementprocedure()
                remainingaction = remainingaction[len(elementcode) :]
                M._checkforterraincollision()
                M._checkforleavingmap()
                if M.removed():
                    return
                break

        else:

            raise RuntimeError("invalid action %r." % action)

    if M._fp == fp:
        raise RuntimeError(
            "%r is not a valid action as it does not expend an FP." % action
        )
    elif M._fp > fp + 1:
        raise RuntimeError(
            "%r is not a valid action as it attempts to expend more than one FP."
            % action
        )

    M._extendpath()

    if M._fp == M._maxfp:
        M._logpositionandmaneuver("end")
    else:
        M._logpositionandmaneuver("")

    if initialaltitudeband != M.altitudeband():
        M._logevent(
            "altitude band changed from %s to %s."
            % (initialaltitudeband, M.altitudeband())
        )


################################################################################


def _attenuationfactor(altitudeband, flightgameturn):
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


def maxspeed(altitudeband):
    table = {"LO": 24, "ML": 26, "MH": 28, "HI": 30, "VH": 32, "EH": 34, "UH": 36}
    return table[altitudeband]


def minspeed(altitudeband):
    table = {"LO": 2, "ML": 3, "MH": 3, "HI": 4, "VH": 4, "EH": 5, "UH": 7}
    return table[altitudeband]


def maneuverspeed(altitudeband):
    table = {"LO": 4, "ML": 5, "MH": 6, "HI": 7, "VH": 8, "EH": 10, "UH": 14}
    return table[altitudeband]
