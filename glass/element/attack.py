################################################################################

import glass.hexcode
import glass.log

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
                glass.log.plural(self._unspecifiedattackresult, "result", "results"),
            )
        )


################################################################################


def _attackgroundunit(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


def _attackaircraft(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack aircraft." % self.name())


def _secondaryattackgroundunit(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


################################################################################


def attack(self, target, *args, **kwargs):
    try:
        if target.isaircraft():
            self._attackaircraft(target, *args, **kwargs)
        elif target.isgroundunit():
            self._attackgroundunit(target, *args, **kwargs)
        else:
            raise RuntimeError("invalid target for attack.")
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


def secondaryattack(self, target, *args, **kwargs):
    try:
        if target.isgroundunit():
            self._secondaryattackgroundunit(target, *args, **kwargs)
        else:
            raise RuntimeError("invalid target.")
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################
