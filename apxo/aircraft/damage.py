################################################################################

def _damage(self):

    if self._damageK > 0:
        return "K"

    damage = ""
    if self._damageL == 1:
        damage = "L"
    elif self._damageL == 2:
        damage = "2L"
    if self._damageH == 1:
        damage = "%sH" % ("" if damage == "" else damage + "+",)
    if self._damageC == 1:
        damage = "%sC" % ("" if damage == "" else damage + "+")

    return damage

################################################################################

def _damageatleast(self, damage):
    assert damage in ["none", "L", "2L", "H", "C", "K"]
    if damage == "none":
        return True
    elif damage == "L":
        return self._damageL >= 1 or self.damageatleast("2L")
    elif damage == "2L":
        return self._damageL >= 2 or self.damageatleast("H")
    elif damage == "H":
        return self._damageH >= 1 or self.damageatleast("C")
    elif damage == "C":
        return self._damageC >= 1 or self.damageatleast("K")
    elif damage == "K":
        return self._damageK >= 1


def _damageatmost(self, damage):
    assert damage in ["none", "L", "2L", "H", "C", "K"]
    if damage == "none":
        return not self.damageatleast("L")
    elif damage == "L":
        return not self.damageatleast("2L")
    elif damage == "2L":
        return not self.damageatleast("H")
    elif damage == "H":
        return not self.damageatleast("C")
    elif damage == "C":
        return not self.damageatleast("K")
    elif damage == "K":
        return True


################################################################################

def _takedamage(self, damage):

    if damage == "L":
        self._damageL += 1
    elif damage == "2L":
        self._damageL += 2
    elif damage == "H":
        self._damageH += 1
    elif damage == "C":
        self._damageC += 1
    elif damage == "K":
        self._damageK += 1
    else:
        raise RuntimeError("invalid damage %r" % damage)

    if self._damageL >= 3:
        self._damageL -= 3
        self._damageH += 1

    if self._damageH >= 2:
        self._damageH -= 2
        self._damageC += 1

    if self._damageC >= 2:
        self._damageK = 1

    if self._damageH > 0 and self._damageC > 0:
        self._damageK = 1

    if self._damageK > 0:
        self._damageK = 1
        self._damageL = 0
        self._damageH = 0
        self._damageC = 0
        self._kill()


def _takedamageconsequences(self):

    def gain(p):
        if not self.hasproperty(p):
            self.logwhenwhat("", "gains %s property." % p)
            self.gainproperty(p)

    def lose(p):
        if self.hasproperty(p):
            self.logwhenwhat("", "loses %s property." % p)
            self.loseproperty(p)

    if self.damageatleast("L"):
        lose("HPR")
        lose("HRR")
        gain("LRR")
    if self.damageatleast("H"):
        gain("NRM")

################################################################################
