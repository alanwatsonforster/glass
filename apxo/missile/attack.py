################################################################################

import apxo.geometry as apgeometry
import apxo.log as aplog

################################################################################


def _attackaircraft(self, target, result=None, note=None):

    self.logwhenwhat("", "%s attacks %s." % (self.name(), target.name()))

    target._takeattackdamage(self, result)

    aplog.lognote(note)
    
    self._remove()


################################################################################
