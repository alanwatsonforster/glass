"""
Stalled flight for aircraft.
"""

import math

import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities


def doflight(A, action):
    """
    Carry out stalled flight.
    """

    if action != "ST":
        raise RuntimeError("invalid action %r for stalled flight." % action)

    altitudechange = math.ceil(A.speed() + A._turnsstalled)

    initialaltitude = A.altitude()
    initialaltitudeband = A.altitudeband()
    A._movedive(altitudechange)
    altitudechange = initialaltitude - A.altitude()

    if A._turnsstalled == 0:
        A._altitudeap = 0.5 * altitudechange
    else:
        A._altitudeap = 1.0 * altitudechange

    A._logposition("end")

    if initialaltitudeband != A.altitudeband():
        A._logevent(
            "altitude band changed from %s to %s."
            % (initialaltitudeband, A.altitudeband())
        )

    A._checkforterraincollision()
    if A.killed():
        return

    A._turnsstalled += 1
    A._finishedmoving = True
