import apxo.log as aplog

################################################################################


def names(A):
    """
    Return a list containing the names of the aircraft in close formation with the
    aircraft or an empty list if the aircraft is not in close formation.
    """

    return sorted(map(lambda a: a._name, A._closeformation))


################################################################################


def size(A):
    """
    Returns the total number of aircraft in the close formation with the
    aircraft or zero if the aircraft is not in close formation.
    """

    return len(A._closeformation)


################################################################################


def leave(A):
    """
    The aircraft leaves its close formation.
    """

    if size(A) == 0:
        raise RuntimeError("%s: is not in a close formation." % A._name)

    leaveany(A)


################################################################################


def join(A, B):
    """
    The aircraft A joins a close formation with B. Any aircraft previously in
    a close formation either with A or B are also part of the
    resulting close formation.
    """

    # TODO: check we're called only during setup or after everyone has moved.

    if A.x() != B.x() or A.y() != B.y():
        raise RuntimeError(
            "attempt to form a close formation from aircraft with different positions."
        )
    if A.altitude() != B.altitude():
        raise RuntimeError(
            "attempt to form a close formation from aircraft with different altitudes."
        )
    if A.facing() != B.facing():
        raise RuntimeError(
            "attempt to form a close formation from aircraft with different facings."
        )
    if A.speed() != B.speed():
        raise RuntimeError(
            "attempt to form a close formation from aircraft with different speeds."
        )

    nA = max(1, size(A))
    nB = max(1, size(B))
    if nA + nB > 4:
        raise RuntimeError(
            "attempt to form a close formation with more than four aircraft."
        )

    if A._closeformation == []:
        A._closeformation = [A]

    if B._closeformation == []:
        B._closeformation = [B]

    A._closeformation += B._closeformation
    for a in A._closeformation:
        a._closeformation = A._closeformation

    check(A)


################################################################################


def check(A):
    """
    Raise an exception if any of the aircraft in close formation with the
    aircraft A do not have the same position, altitude, facing, and speed.
    """

    for a in A._closeformation:
        if A.x() != a.x() or A.y() != a.y():
            raise RuntimeError(
                "aircraft %s and %s cannot be in close formation as they do not have the same positions."
                % (A._name, a._name)
            )
        if A.altitude() != a.altitude():
            raise RuntimeError(
                "aircraft %s and %s cannot be in close formation as they do not have the same altitudes."
                % (A._name, a._name)
            )
        if A.facing() != a.facing():
            raise RuntimeError(
                "aircraft %s and %s cannot be in close formation as they do not have the same facings."
                % (A._name, a._name)
            )
        if A.speed() != a.speed():
            raise RuntimeError(
                "aircraft %s and %s cannot be in close formation as they do not have the same speeds."
                % (A._name, a._name)
            )


################################################################################


def leaveany(A):
    """
    The aircraft A leaves its close formation, if it is in one.
    """

    if A._closeformation != []:
        A._closeformation.remove(A)
        A._closeformation = []


################################################################################


def breakdown(A):
    """
    Break down the close formation containing the aircraft A.
    """

    for a in A._closeformation.copy():
        leaveany(a)


################################################################################
