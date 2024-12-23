################################################################################

import apxo.geometry as apgeometry
import apxo.log as aplog

################################################################################

def _attackgroundunit(self, target, result=None, blastzone=True):

    self.logwhenwhat(
        "", "%s attacks %s." % (self.name(), target.name())
    )
    if not apgeometry.samehorizontalposition(self, target):
        raise RuntimeError("the bombs are not at the position of the target.")

    target._takeattackdamage(self, result)
    
    self._remove()


################################################################################


def _secondaryattackgroundunit(self, target, result=None):

    self.logwhenwhat(
        "", "%s attacks %s (secondary)." % (self.name(), target.name())
    )

    target._takeattackdamage(self, result)


################################################################################
