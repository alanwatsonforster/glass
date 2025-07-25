################################################################################


def _initdamage(self):

    self._damagelevel = 0
    self._suppressionlevel = 0


################################################################################


def _endgameturndamage(self):
    if self._suppressionlevel > 0:
        self._suppressionlevel -= 1


################################################################################


def _damage(self):
    def suppression():
        if self._suppressionlevel == 2:
            return "2S"
        elif self._suppressionlevel == 1:
            return "S"
        else:
            return ""
    def damage():
        if self._damagelevel == 0:
            return ""
        elif self._damagelevel == 1:
            return "D"
        elif self._damagelevel == 2:
            return "2D"
        else:
            return "K"
    if damage() == "K":
        return "K"
    elif damage() == "":
        return suppression()
    elif suppression() != "":
        return damage() + "+" + suppression()
    else:
        return damage()

################################################################################


def _damageatleast(self, damage):
    assert damage in ["", "D", "2D", "K"]
    if damage == "":
        return True
    elif damage == "D":
        return self._damagelevel >= 1
    elif damage == "2D":
        return self._damagelevel >= 2
    elif damage == "K":
        return self._damagelevel >= 3


def _damageatmost(self, damage):
    assert damage in ["", "D", "2D", "K"]
    if damage == "":
        return self._damagelevel == 0
    elif damage == "D":
        return self._damagelevel <= 1
    elif damage == "2D":
        return self._damagelevel <= 2
    elif damage == "K":
        return True


################################################################################


def _takedamage(self, damage):
    self._suppressionlevel = 2
    if damage == "S":
        pass
    elif damage == "D":
        self._damagelevel += 1
    elif damage == "2D":
        self._damagelevel += 2
    elif damage == "K":
        self._damagelevel += 3
    else:
        raise RuntimeError("invalid damage %r" % damage)


def _takedamageconsequences(self):
    if self.isusingbarragefire():
        self.logwhenwhat("", "ceases barrage fire.")
        self._barragefire._remove()
        self._barragefire = None


################################################################################


def _issuppressed(self):
    return self._suppressionlevel > 0


################################################################################
