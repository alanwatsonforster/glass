"""
Aircraft flight.
"""

##############################################################################

import math
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

################################################################################


########################################


def continuespecialflight(A, moves):
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

    movedispatchlist = [
        # This table is searched in order, so put longer elements before shorter
        # ones that are prefixes (e.g., put C2 before C).
        ["L180", "epilog", lambda A: doturn(A, "L", 180)],
        ["L150", "epilog", lambda A: doturn(A, "L", 150)],
        ["L120", "epilog", lambda A: doturn(A, "L", 120)],
        ["L90", "epilog", lambda A: doturn(A, "L", 90)],
        ["L60", "epilog", lambda A: doturn(A, "L", 60)],
        ["L30", "epilog", lambda A: doturn(A, "L", 30)],
        ["LLL", "epilog", lambda A: doturn(A, "L", 90)],
        ["LL", "epilog", lambda A: doturn(A, "L", 60)],
        ["L", "epilog", lambda A: doturn(A, "L", 30)],
        ["R180", "epilog", lambda A: doturn(A, "R", 180)],
        ["R150", "epilog", lambda A: doturn(A, "R", 150)],
        ["R120", "epilog", lambda A: doturn(A, "R", 120)],
        ["R90", "epilog", lambda A: doturn(A, "R", 90)],
        ["R60", "epilog", lambda A: doturn(A, "R", 60)],
        ["R30", "epilog", lambda A: doturn(A, "R", 30)],
        ["RRR", "epilog", lambda A: doturn(A, "R", 90)],
        ["RR", "epilog", lambda A: doturn(A, "R", 60)],
        ["R", "epilog", lambda A: doturn(A, "R", 30)],
        ["S", "FP", lambda A: dostationary(A)],
        ["H", "FP", lambda A: dohorizontal(A, "H")],
        ["HD", "FP", lambda A: dohorizontal(A, "HD")],
        ["C1", "FP", lambda A: doclimb(A, 1)],
        ["C2", "FP", lambda A: doclimb(A, 2)],
        ["CC", "FP", lambda A: doclimb(A, 2)],
        ["C", "FP", lambda A: doclimb(A, 1)],
        ["D1", "FP", lambda A: dodive(A, 1)],
        ["D2", "FP", lambda A: dodive(A, 2)],
        ["D3", "FP", lambda A: dodive(A, 3)],
        ["DDD", "FP", lambda A: dodive(A, 3)],
        ["DD", "FP", lambda A: dodive(A, 2)],
        ["D", "FP", lambda A: dodive(A, 1)],
    ]

    ########################################

    apflight.domoves(A, moves, movedispatchlist)

    if not A.killed() and not A.removed():
        if A._altitudecarry != 0:
            A._logend("is carrying %.2f altitude levels." % A._altitudecarry)

    A._newspeed = A.speed()

    if A.killed() or A.removed() or A._fp + 1 > A._maxfp:

        A._finishedmoving = True


################################################################################
