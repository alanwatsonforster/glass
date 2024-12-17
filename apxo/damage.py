import math
import apxo as ap
import apxo.hex as aphex
import apxo.log as aplog

##############################################################################


def damage(A):

    if A._damageK > 0:
        return "K"

    damage = ""
    if A._damageL == 1:
        damage = "L"
    elif A._damageL == 2:
        damage = "2L"
    if A._damageH == 1:
        damage = "%sH" % ("" if damage == "" else damage + "+",)
    if A._damageC == 1:
        damage = "%sC" % ("" if damage == "" else damage + "+")

    return damage


##############################################################################


def takedamage(A, damage):

    if damage == "L":
        A._damageL += 1
    elif damage == "2L":
        A._damageL += 2
    elif damage == "H":
        A._damageH += 1
    elif damage == "C":
        A._damageC += 1
    elif damage == "K":
        A._damageK += 1
    else:
        raise RuntimeError("invalid damage %r" % damage)

    if A._damageL >= 3:
        A._damageL -= 3
        A._damageH += 1

    if A._damageH >= 2:
        A._damageH -= 2
        A._damageC += 1

    if A._damageC >= 2:
        A._damageK = 1

    if A._damageH > 0 and A._damageC > 0:
        A._damageK = 1

    if A._damageK > 0:
        A._damageK = 1
        A._damageL = 0
        A._damageH = 0
        A._damageC = 0
        A._kill()

def takedamageconsequences(A):

    def gain(p):
        if not A.hasproperty(p):
            A.logwhenwhat("", "gains %s property." % p)
            A.gainproperty(p)

    def lose(p):
        if A.hasproperty(p):
            A.logwhenwhat("", "loses %s property." % p)
            A.loseproperty(p)

    if damageatleast(A, "L"):
        lose("HPR")
        lose("HRR")
        gain("LRR")
    if damageatleast(A, "H"):
        gain("NRM")


##############################################################################


def damageatleast(A, damage):
    assert damage in ["none", "L", "2L", "H", "C", "K"]
    if damage == "none":
        return True
    elif damage == "L":
        return A._damageL >= 1 or A.damageatleast("2L")
    elif damage == "2L":
        return A._damageL >= 2 or A.damageatleast("H")
    elif damage == "H":
        return A._damageH >= 1 or A.damageatleast("C")
    elif damage == "C":
        return A._damageC >= 1 or A.damageatleast("K")
    elif damage == "K":
        return A._damageK >= 1


##############################################################################


def damageatmost(A, damage):
    assert damage in ["none", "L", "2L", "H", "C", "K"]
    if damage == "none":
        return not A.damageatleast("L")
    elif damage == "L":
        return not A.damageatleast("2L")
    elif damage == "2L":
        return not A.damageatleast("H")
    elif damage == "H":
        return not A.damageatleast("C")
    elif damage == "C":
        return not A.damageatleast("K")
    elif damage == "K":
        return True


##############################################################################
