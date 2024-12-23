import apxo.geometry as apgeometry

#############################################################################


def _attackaircraft(self, target, result=None):

    self.logwhenwhat(
        "", "%s attacks %s." % (self.name(), target.name())
    )

    target._takeattackdamage(self, result)
    
    self._remove()


#############################################################################
