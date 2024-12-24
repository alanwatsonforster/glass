import apxo.geometry as apgeometry
import apxo.log as aplog
import apxo.rounding as aprounding

################################################################################

def _maximumtrackingrange(self):
    if self._aaamaximumrange() is None:
        return None
    else:
        return aprounding.rounddown(self._aaamaximumrange() * 1.5)
        
def _trackingrequirement(self, target, radar=False):
    if self._aaaclass == "H":
        factor = 2/3
    elif not radar:
        factor = 1/2
    else:
        factor = 1/3
    return aprounding.roundup(target.speed() * factor)

################################################################################

def _track(self, target):

    self.logwhenwhat("", "%s starts tracking %s." % (self.name(), target.name()))

    maximumtrackingrange = self._maximumtrackingrange()
    if maximumtrackingrange is None:
        raise RuntimeError("%s cannot track." % self.name())
    range = apgeometry.range(self, target)
    self.logcomment("range to target is %d." % range)
    if range > maximumtrackingrange:
        raise RuntimeError("%s is beyond the maximum tracking range of %d." % (target.name(), maximumtrackingrange))
    trackingrequirement = self._trackingrequirement(target)
    self.logcomment("tracking requirement is %d %s." % (
        trackingrequirement,
        aplog.plural(trackingrequirement, "FP", "FPs")
    ))
    self._tracking = target


#############################################################################


def _stoptracking(self):

    self.logwhenwhat("", "%s stops tracking %s." % (self.name(), self._tracking.name()))
    self._tracking = None


#############################################################################
