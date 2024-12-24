################################################################################

import apxo.hexcode as aphexcode
import apxo.log as aplog

################################################################################


def _initaim(self):
    self._aimingtarget = None


################################################################################


def aim(self, target, *args, **kwargs):
    try:
        if isinstance(target, str):
            self.logwhenwhat("", "starts aiming at hex %s." % target)
            aphexcode.checkisvalidhexcodeforcenter(target)
        elif not target.isgroundunit():
            raise RuntimeError("invalid target for aiming.")
        else:
            self.logwhenwhat("", "starts aiming at %s." % target.name())
        self._aimingtarget = target
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################


def stopaiming(self):
    try:
        if self._aimingtarget is None:
            raise RuntimeError("%s is not aiming." % self.name())
        if isinstance(self._aimingtarget, str):
            self.logwhenwhat("", "stops aiming at hex %s." % self._aimingtarget)
        else:
            self.logwhenwhat("", "stops aiming at %s." % self._aimingtarget.name())
        self._aimingtarget = None
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################
