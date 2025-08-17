################################################################################

import glass.hexcode
import glass.log
import glass.flight
from glass.rounding import onethirdfromtable, twothirdsfromtable, roundup, rounddown

################################################################################


def _initaim(self):
    self._aimingtarget = None


################################################################################


def aim(self, target, *args, **kwargs):
    try:        
        if not target.isgroundunit():
            raise RuntimeError("invalid target for aiming.")
        if glass.flight.aimingforbidden(self):
            raise RuntimeError("aiming is forbidden %s." % glass.flight.aimingforbidden(self))
        self.logwhenwhat("", "starts aiming at %s." % target.name())
        if self.bombsystem() == "manual":
            requirement = max(1, rounddown(twothirdsfromtable(self.speed())))
        elif self.bombsystem() == "ballistic":
            requirement = max(1, roundup(self.speed() / 2))
        else:
            requirement = max(1, roundup(onethirdfromtable(self.speed())))
        self.logcomment(
            "aiming requirement is %d %s."
            % (requirement, glass.log.plural(requirement, "FP", "FPs"))
        )
        modifierrequirement = max(1, onethirdfromtable(self.speed())) + requirement
        self.logcomment(
            "aiming modifier requirement is %d %s in total for -1 modifier."
            % (modifierrequirement, glass.log.plural(modifierrequirement, "FP", "FPs"))
        )
        modifierrequirement = max(1, twothirdsfromtable(self.speed())) + requirement
        self.logcomment(
            "aiming modifier requirement is %d %s in total for -2 modifier."
            % (modifierrequirement, glass.log.plural(requirement + modifierrequirement, "FP", "FPs"))
        )
        self._aimingtarget = target
    except RuntimeError as e:
        glass.log.logexception(e)
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
        glass.log.logexception(e)
    self.logbreak()


################################################################################
