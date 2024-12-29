import apxo.geometry as apgeometry
import apxo.log as aplog
from apxo.rounding import onethirdfromtable, twothirdsfromtable, roundup, rounddown

################################################################################


def _maximumtrackingrange(self):
    if self._aaamaximumrange() is None:
        return None
    else:
        return rounddown(self._aaamaximumrange() * 1.5)


def _trackingrequirement(self, target, radar=False):
    if self._aaaclass == "H":
        return max(1, roundup(twothirdsfromtable(target.speed())))
        factor = 2 / 3
    elif not radar:
        return max(1, roundup(self.speed() / 2))
    else:
        return max(1, roundup(onethirdfromtable(target.speed())))


################################################################################


def _track(self, target):

    self.logwhenwhat("", "starts tracking %s." % target.name())

    maximumtrackingrange = self._maximumtrackingrange()
    if maximumtrackingrange is None:
        raise RuntimeError("%s cannot track." % self.name())
    range = apgeometry.range(self, target)
    self.logcomment("range to target is %d." % range)
    if range > maximumtrackingrange:
        raise RuntimeError(
            "%s is beyond the maximum tracking range of %d."
            % (target.name(), maximumtrackingrange)
        )
    trackingrequirement = self._trackingrequirement(target)
    self.logcomment(
        "tracking requirement is %d %s."
        % (trackingrequirement, aplog.plural(trackingrequirement, "FP", "FPs"))
    )
    self._tracking = target


#############################################################################


def _stoptracking(self):

    self.logwhenwhat("", "stops tracking %s." % self._tracking.name())
    self._tracking = None


#############################################################################
