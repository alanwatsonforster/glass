"""
Special flight for aircaft.
"""

import apxo.altitude as apaltitude
import apxo.capabilities as apcapabilities
import apxo.flight as apflight
import apxo.hex as aphex
import apxo.speed as apspeed
import apxo.turnrate as apturnrate
import apxo.variants as apvariants

################################################################################


def checkflight(A):
    return


################################################################################


def doflight(A, tasks, note=False):
    """
    Carry out out special flight.
    """

    ########################################

    def dostationary(A):
        """
        Stay stationary.
        """

        A._fp += 1

    ########################################

    def dohorizontal(A):
        """
        Move horizontally.
        """

        A._moveforward()
        A._fp += 1
        A._hfp += 1

    ########################################

    def doclimb(A, altitudechange):
        """
        Climb.
        """

        if altitudechange == 1:
            altitudechange = apcapabilities.specialclimbcapability(A)

        A._moveclimb(altitudechange)
        A._fp += 1
        A._vfp += 1

    ########################################

    def dodive(A, altitudechange):
        """
        Dive.
        """

        A._setaltitudecarry(0)
        A._movedive(altitudechange)
        A._fp += 1
        A._vfp += 1

    ########################################

    def doturn(A, sense, facingchange):
        """
        Turn in the specified sense and amount.
        """

        A._moveturn(sense, facingchange)

    ########################################

    def doattack(A, weapon):
        """
        Declare an attack with the specified weapon.
        """

        A._logevent("attack using %s." % weapon)

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
        ["AAGN", "epilog", None, lambda A: doattack(A, "guns")],
        ["AARK", "epilog", None, lambda A: doattack(A, "rockets")],
        ["S", "FP", None, lambda A: dostationary(A)],
        ["H", "FP", None, lambda A: dohorizontal(A)],
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

    A._maxfp = len(tasks.split(","))

    A._logposition("start")

    apflight.dotasks(A, tasks, taskdispatchlist, start=True)

    A._lognote(note)

    A._logposition("end")

    if not A._destroyed and not A._leftmap:
        if A._altitudecarry != 0:
            A._logend("is carrying %.2f altitude levels." % A._altitudecarry)

    A._newspeed = A.speed()


################################################################################
