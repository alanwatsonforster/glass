################################################################################

import apxo.log as aplog

################################################################################

# These procedures can be implemented in subclasses that take damage.


def _initdamage(self):
    pass


def _damage(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _damageatleast(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _damageatmost(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _takedamage(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _takedamageconsequences(self):
    pass


def _isssupressed(self):
    raise RuntimeError("%s cannot be suppresed." % self.name())


################################################################################


def damage(self):
    return self._damage()


def damageatleast(self, damage):
    return self._damageatleast(damage)


def damageatmost(self, damage):
    return self._damageatmost(damage)


def takedamage(self, damage, note=None):
    try:
        self.logwhenwhat("", "%s takes %s damage." % (self.name(), damage))
        if self.killed():
            self.logwhenwhat("", "%s is already killed." % self.name())
            return
        previousdamage = self.damage()
        if previousdamage == "":
            previousdamage = "none"
        self._takedamage(damage)
        if previousdamage == self.damage():
            self.logwhenwhat(
                "", "%s damage is unchanged at %s." % (self.name(), previousdamage)
            )
        else:
            self.logwhenwhat(
                "",
                "%s damage changes from %s to %s."
                % (self.name(), previousdamage, self.damage()),
            )
            if self.damage() == "K":
                self._kill()
                self.logwhenwhat("", "%s is killed." % self.name())
            else:
                self._takedamageconsequences()
        self.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


def issuppressed(self):
    return self._issuppressed()


################################################################################


def _takeattackdamage(self, attacker, result):
    """
    Take damage from an attack.
    """
    if result is None:
        attacker.logcomment("unspecified result.")
        attacker._unspecifiedattackresult += 1
    elif result == "A":
        attacker.logcomment("aborts.")
    elif result == "M":
        attacker.logcomment("misses.")
    elif result == "-":
        attacker.logcomment("hits but inflicts no damage.")
    else:
        attacker.logcomment("hits and inflicts %s damage." % result)
        self.logwhenwhat("", "%s takes %s damage." % (self.name(), result))
        if self.killed():
            self.logwhenwhat("", "%s is already killed." % self.name())
            return
        previousdamage = self.damage()
        if previousdamage == "":
            previousdamage = "none"
        self._takedamage(result)
        if previousdamage == self.damage():
            self.logwhenwhat(
                "", "%s damage is unchanged at %s." % (self.name(), previousdamage)
            )
        else:
            self.logwhenwhat(
                "",
                "%s damage changes from %s to %s."
                % (self.name(), previousdamage, self.damage()),
            )
            if self.damage() == "K":
                self._kill()
                self.logwhenwhat("", "%s is killed." % self.name())
            else:
                self._takedamageconsequences()


################################################################################
