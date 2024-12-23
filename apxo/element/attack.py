################################################################################

import apxo.hexcode as aphexcode
import apxo.log as aplog

################################################################################


def _attackstartgameturn(self):
    self._unspecifiedattackresult = 0


def _attackendgameturn(self):
    if self._unspecifiedattackresult > 0:
        raise RuntimeError(
            "%s has %d unspecified attack %s."
            % (
                self._name,
                self._unspecifiedattackresult,
                aplog.plural(self._unspecifiedattackresult, "result", "results"),
            )
        )


################################################################################


def _attackterrain(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


def _attackgroundunit(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


def _attackaircraft(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack aircraft." % self.name())


def _secondaryattackterrain(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


def _secondaryattackgroundunit(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


################################################################################


def attack(self, target, *args, **kwargs):
    try:
        if isinstance(target, str):
            aphexcode.checkisvalidhexcodeforcenter(target)
            self._attackterrain(target, *args, **kwargs)
        elif target.isaircraft():
            self._attackaircraft(target, *args, **kwargs)
        elif target.isgroundunit():
            self._attackgroundunit(target, *args, **kwargs)
        else:
            raise RuntimeError("invalid target for attack.")
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


def secondaryattack(self, target, *args, **kwargs):
    try:
        if isinstance(target, str):
            aphexcode.checkisvalidhexcodeforcenter(target)
            self._secondaryattackterrain(target, *args, **kwargs)
        elif target.isgroundunit():
            self._secondaryattackgroundunit(target, *args, **kwargs)
        else:
            raise RuntimeError("invalid target.")
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################
