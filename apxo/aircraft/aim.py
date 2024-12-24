################################################################################

import apxo.hexcode as aphexcode
import apxo.log as aplog

################################################################################

def _initaim(self):
    self._aiming = None

################################################################################


def aim(self, target, *args, **kwargs):
    try:
        if isinstance(target, str):
            self.logwhenwhat("", "starts aiming at hex %s" % target)
            aphexcode.checkisvalidhexcodeforcenter(target)
        elif not target.isgroundunit():
            raise RuntimeError("invalid target for aiming.")
        else:
            self.logwhenwhat("", "starts aiming at %s" % target.name())
        self._aiming = target
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################


def stopaiming(self):
    try:
        if self._aiming is None:
            raise RuntimeError("%s is not aiming" % self.name())
        if isinstance(target, str):
            self.logwhenwhat("", "stops aiming at hex %s" % target)
        else:
            self.logwhenwhat("", "stops aiming at %s" % target.name())
        self._aiming = None
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################
