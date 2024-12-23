import apxo.geometry as apgeometry

#############################################################################


def _track(self, target):

    self.logwhenwhat("", "%s starts tracking %s." % (self.name(), target.name()))
    self.logwhenwhat("", "range to target is %d." % apgeometry.range(self, target))
    self._tracking = target


#############################################################################


def _stoptracking(self):

    self.logwhenwhat("", "%s stops tracking %s." % (self.name(), self._tracking.name()))
    self._tracking = None


#############################################################################
