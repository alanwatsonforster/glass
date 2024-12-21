################################################################################

import apxo.log as aplog

################################################################################


def _attackterrain(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


def _attackgroundunit(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack ground targets." % self.name())


def _attackaircraft(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot attack aircraft." % self.name())


################################################################################


def attack(self, target, *args, **kwargs):
    aplog.clearerror()
    try:
        if isinstance(target, str):
            aphexcode.checkisvalidhexcodeforcenter(target)
            self._attackterrain(target, *args, **kwargs)
        elif target.isaircraft():
            self._attackaircraft(target, *args, **kwargs)
        elif target.isgroundunit():
            self._attackgroundunit(target, *args, **kwargs)
        else:
            raise RuntimeError("invalid target.")
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################
