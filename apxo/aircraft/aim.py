################################################################################

import apxo.hexcode as aphexcode
import apxo.log as aplog
from apxo.rounding import onethirdfromtable, twothirdsfromtable, roundup

################################################################################


def _initaim(self):
    self._aimingtarget = None


################################################################################


def aim(self, target, *args, **kwargs):
    try:
        if not target.isgroundunit():
            raise RuntimeError("invalid target for aiming.")
        self.logwhenwhat("", "starts aiming at %s." % target.name())
        if self.bombsystem() == "manual":
            requirement = max(1, roundup(twothirdsfromtable(self.speed())))
        elif self.bombsystem() == "ballistic":
            requirement = max(1, roundup(self.speed() / 2))
        else:
            requirement = max(1, roundup(onethirdfromtable(self.speed())))
        self.logcomment("aiming requirement is %d %s." % (
            requirement,
            aplog.plural(requirement, "FP", "FPs")
        ))
        modifierrequirement =  max(1, roundup(onethirdfromtable(self.speed())))
        self.logcomment("aiming modifier requirement is %d %s." % (
            modifierrequirement,
            aplog.plural(modifierrequirement, "FP", "FPs")
        ))
        self._aimingtarget = target
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################


def _stopaiming(self):
    if self._aimingtarget is None:
        raise RuntimeError("%s is not aiming." % self.name())
    self.logwhenwhat("", "stops aiming at %s." % self._aimingtarget.name())
    self._aimingtarget = None


################################################################################

def stopaiming(self):
    try:
        self._stopaiming()
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################
