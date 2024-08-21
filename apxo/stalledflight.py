"""
Stalled flight for aircraft.
"""

import math

import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities


def doflight(A, action, jettison=None):
    """
    Carry out stalled flight.
    """

    # See rule 6.4.

    A._logevent("is carrying %+.2f APs." % A._apcarry)

    A._logposition("start")

    if jettison is not None:
        A._jettison(*jettison)

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
