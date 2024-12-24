import apxo.geometry as apgeometry

################################################################################




def _maximumtrackingrange(self):
    if self._aaamaximumrange() is None:
        return None
    else:
        return int(self._aaamaximumrange() * 1.5)

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
    self._tracking = target


#############################################################################


def _stoptracking(self):

    self.logwhenwhat("", "%s stops tracking %s." % (self.name(), self._tracking.name()))
    self._tracking = None


#############################################################################
