################################################################################

import apxo.geometry
import apxo.log

################################################################################


def _attackaircraft(self, target, result=None, note=None):

    self.logwhenwhat("", "attacks %s." % target.name())

    target._takeattackdamage(self, result)

    self.lognote(note)

    self._remove()


################################################################################
