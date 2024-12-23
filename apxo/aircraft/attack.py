################################################################################

import apxo.airtoair as apairtoair
import apxo.bomb as apbomb
import apxo.flight as apflight
import apxo.geometry as apgeometry
import apxo.log as aplog

################################################################################


def _attackaircraft(self, target, attacktype, result=None, returnfire=False, note=None):

    if not returnfire and apflight.useofweaponsforbidden(self):
        raise RuntimeError(
            "attempt to use weapons %s." % apflight.useofweaponsforbidden(self)
        )

    apairtoair.attack(self, attacktype, target, result, returnfire=returnfire)

    aplog.lognote(note)


################################################################################


def _attackgroundunit(self, target, attacktype, result=None, stores=None, note=None):

    attacktype = attacktype.split("/")

    weapon = attacktype[0]
    if weapon not in ["GN", "RK", "RP"]:
        raise RuntimeError("invalid weapon.")

    if weapon == "GN":
        if stores is not None:
            raise RuntimeError("stores cannot be specified for GN attacks.")
        for s in attacktype[1:]:
            if s not in ["SS"]:
                raise RuntimeError("invalid attack type.")
        if "SS" in attacktype:
            if self._gunammunition < 0.5:
                raise RuntimeError("insuffient gun ammunition.")
            self._gunammunition -= 0.5
        else:
            if self._gunammunition < 1.0:
                raise RuntimeError("insuffient gun ammunition.")
            self._gunammunition -= 1.0
    else:
        if stores is None:
            raise RuntimeError("stores must be specified for %s attacks." % weapon)

    self.logwhenwhat(
        "", "%s attacks %s with %s." % (self.name(), target.name(), weapon)
    )
    self.logwhenwhat("", "range to target is %d." % apgeometry.range(self, target))
    self.logwhenwhat(
        "", "altitude to target is %d." % (target.altitude() - self.altitude())
    )

    if weapon == "GN":
        self.logwhenwhat("", "gun ammunition is now %.1f." % self._gunammunition)
    else:
        self._release(stores)

    target._takeattackdamage(self, result)

    aplog.lognote(note)


################################################################################


def _secondaryattackgroundunit(self, target, attacktype, result=None, note=None):

    attacktype = attacktype.split("/")

    weapon = attacktype[0]
    if weapon not in ["GN", "RK", "RP"]:
        raise RuntimeError("invalid weapon.")

    self.logwhenwhat(
        "", "%s attacks %s with %s (secondary)." % (self.name(), target.name(), weapon)
    )

    target._takeattackdamage(self, result)

    aplog.lognote(note)

################################################################################


def bomb(self, name, target, stores=None, note=None):

    try:
        if isinstance(target, str):
            aphexcode.checkisvalidhexcodeforcenter(target)
            self.logwhenwhat("", "%s bombs hex %s." % (self.name(), target))
        elif target.isgroundunit():
            self.logwhenwhat("", "%s bombs %s." % (self.name(), target.name()))
        else:
            raise RuntimeError("invalid target.")
        self._release(stores)
        bomb = apbomb.bomb(name, self.hexcode(), self.facing(), self.altitude())
        aplog.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()
    return bomb


################################################################################
