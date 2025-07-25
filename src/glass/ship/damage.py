################################################################################


def _initdamage(self):

    self._damagelevel = 0


################################################################################


def _damage(self):
    if self._damagelevel == 0:
        return ""
    else:
        return "%dD" % self._damagelevel


################################################################################


def _damageatleast(self, damage):
    assert isinstance(damage, int)
    return self._damagelevel >= damage


def _damageatmost(self, damage):
    assert isinstance(damage, int)
    return self._damagelevel <= damage


################################################################################


def _takedamage(self, damage):
    assert isinstance(damage, int) or damage in ["D", "2D", "K"]
    if damage == "D":
        damage = 1
    elif damage == "2D":
        damage = 2
    elif damage == "K":
        damage = 3
    self._damagelevel += damage


################################################################################
