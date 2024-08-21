import math

import apxo.capabilities as apcapabilities
import apxo.configuration as apconfiguration
import apxo.variants as apvariants

from apxo.math import *
from apxo.log import plural

################################################################################


def isvalidspeed(speed):
    """
    Return True if the argument is a valid speed.
    """

    return isinstance(speed, (int, float)) and speed >= 0


################################################################################

# See the "Transonic/Supersonic Speed Reference Table" chart and the "Speed of
# Sound" and "Transonic Speeds" section of rule 6.6.


def m1speed(altitudeband):
    """
    Return the M1 speed in the specified altitude band.
    """

    if altitudeband == "LO" or altitudeband == "ML":
        return 7.5
    elif altitudeband == "MH" or altitudeband == "HI":
        return 7.0
    else:
        return 6.5


def htspeed(altitudeband):
    """
    Return the high-transonic speed in the specified altitude band.
    """

    return m1speed(altitudeband) - 0.5


def ltspeed(altitudeband):
    """
    Return the low-transonic speed in the specified altitude band.
    """

    return m1speed(altitudeband) - 1.0


################################################################################


def missilemaxspeed(altitudeband):
    table = {"LO": 24, "ML": 26, "MH": 28, "HI": 30, "VH": 32, "EH": 34, "UH": 36}
    return table[altitudeband]


def missileminspeed(altitudeband):
    table = {"LO": 2, "ML": 3, "MH": 3, "HI": 4, "VH": 4, "EH": 5, "UH": 7}
    return table[altitudeband]


def missilemaneuverspeed(altitudeband):
    table = {"LO": 4, "ML": 5, "MH": 6, "HI": 7, "VH": 8, "EH": 10, "UH": 14}
    return table[altitudeband]


################################################################################


################################################################################


def _endmovespeed(A):
    """
    Carry out the rules to do with speed, power, and drag at the end of a move.
    """

    # For aircraft with SP flight type, we skip this.

    if A._flighttype == "SP":
        A.apcarry = 0
        A._newspeed = A.speed()
        A._logevent("speed is unchanged at %.1f." % A.speed())
        return

    # Report fuel.

    if not A._fuel is None:

        previousexternalfuel = A.externalfuel()
        previousinternalfuel = A.internalfuel()

        A._logevent("fuel consumption was %.1f." % A._fuelconsumption)
        A._fuel -= A._fuelconsumption

        if A._bingofuel is None:
            A._logevent("fuel is %.1f." % A._fuel)
        else:
            A._logevent(
                "fuel is %.1f and bingo fuel is %.1f." % (A._fuel, A._bingofuel)
            )
            if A._fuel < A._bingofuel:
                A._logevent("fuel is below bingo fuel.")

        if A.internalfuel() == 0:
            A._logend("fuel is exhausted.")

        if previousexternalfuel > 0 and A.externalfuel() == 0:
            A._logevent("external fuel is exhausted.")
            previousconfiguration = A._configuration
            apconfiguration.update(A)
            if A._configuration != previousconfiguration:
                A._logevent(
                    "changed configuration from %s to %s."
                    % (previousconfiguration, A._configuration)
                )

    # See the "Departed Flight Procedure" section of rule 6.4

    if A._flighttype == "DP" or A._maneuveringdeparture:
        A.apcarry = 0
        A._logevent("speed is unchanged at %.1f." % A.speed())
        return

    # See the "Speed Gain" and "Speed Loss" sections of rule 6.2.

    A._turnsap = A._turnrateap + A._sustainedturnap

    A._logevent("power           APs = %+.2f." % A._powerap)
    A._logevent("speed           APs = %+.2f." % A._speedap)
    A._logevent("altitude        APs = %+.2f." % A._altitudeap)
    A._logevent("turns           APs = %+.2f." % A._turnsap)
    A._logevent("other maneuvers APs = %+.2f." % A._othermaneuversap)
    A._logevent("speedbrakes     APs = %+.2f." % A._speedbrakeap)
    A._logevent("carry           APs = %+.2f." % A._apcarry)
    ap = (
        A._powerap
        + A._speedap
        + A._altitudeap
        + A._turnsap
        + A._othermaneuversap
        + A._speedbrakeap
        + A._apcarry
    )
    A._logevent("total           APs = %+.2f." % ap)

    # See the "Speed Gain", "Speed Loss", and "Rapid Accel Aircraft" sections
    # of rule 6.2 and the "Supersonic Speeds" section of rule 6.6.

    if ap < 0:
        aprate = -2.0
    elif apcapabilities.hasproperty(A, "RA"):
        if A.speed() >= m1speed(A.altitudeband()):
            aprate = +2.0
        else:
            aprate = +1.5
    else:
        if A.speed() >= m1speed(A.altitudeband()):
            aprate = +3.0
        else:
            aprate = +2.0

    # The speed is limited to the maximum dive speed if the aircraft dived at least
    # two levels. See rules 6.3 and 8.2.

    altitudeloss = A._previousaltitude - A.altitude()
    usemaxdivespeed = (altitudeloss >= 2) and not A.damageatleast("H")

    # See rules 6.2, 6.3, and 8.2.

    if usemaxdivespeed:
        maxspeed = apcapabilities.maxdivespeed(A)
        maxspeedname = "maximum dive speed"
    else:
        maxspeed = apcapabilities.maxspeed(A)
        maxspeedname = "maximum speed"

    # See the Aircraft Damage Effects Table. We interpret its prohibition
    # on SS flight as follows: If an aircraft has at least H damage and
    # its speed exceeds HT speed, it performs a fadeback to HT speed. Its
    # maximum level speed and maximum dive speed are limited to HT speed.

    if maxspeed >= m1speed(A.altitudeband()) and A.damageatleast("H"):
        A._logevent("maximum speed limited to HT speed by damage.")
        usedivespeed = False
        maxspeed = htspeed(A.altitudeband())
        maxspeedname = "HT speed"

    A._newspeed = A.speed()

    if ap == 0:

        A._apcarry = 0

    elif ap < 0:

        # See the "Speed Loss" and "Maximum Deceleration" sections of rule 6.2.

        A._newspeed -= 0.5 * (ap // aprate)
        A._apcarry = ap % aprate

        if A._newspeed <= 0:
            A._newspeed = 0
            if A._apcarry < 0:
                A._apcarry = 0

    elif ap > 0:

        if A.speed() >= maxspeed and ap >= aprate:
            A._logevent(
                "acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed)
            )
            A._apcarry = aprate - 0.5
        elif A.speed() >= maxspeed:
            A._apcarry = ap
        elif A.speed() + 0.5 * (ap // aprate) > maxspeed:
            A._logevent(
                "acceleration is limited by %s of %.1f." % (maxspeedname, maxspeed)
            )
            A._newspeed = maxspeed
            A._apcarry = aprate - 0.5
        else:
            A._newspeed += 0.5 * (ap // aprate)
            A._apcarry = ap % aprate

    if usemaxdivespeed:
        if A._newspeed > maxspeed:
            A._logevent(
                "speed will be reduced to maximum dive speed of %.1f." % maxspeed
            )
            A._newspeed = maxspeed
    else:
        if A._newspeed > maxspeed:
            A._logevent("speed will be faded back from %.1f." % A._newspeed)
            A._newspeed = max(A._newspeed - 1, maxspeed)

    if A.speed() != A._newspeed:
        A._logevent("speed will change from %.1f to %.1f." % (A.speed(), A._newspeed))
    else:
        A._logevent("speed will be unchanged at %.1f." % A._newspeed)

    A._logevent("will carry %+.2f APs." % A._apcarry)

    # See rule 6.4.

    minspeed = apcapabilities.minspeed(A)
    if A._newspeed < minspeed:
        A._logevent("speed will be below the minimum of %.1f." % minspeed)
    if A._newspeed >= minspeed and A._flighttype == "ST":
        A._logevent("aircraft will no longer be stalled.")
    elif A._newspeed < minspeed and A._flighttype == "ST":
        A._logevent("aircraft will still stalled.")
    elif A._newspeed < minspeed:
        A._logevent("aircraft will have stalled.")


################################################################################
