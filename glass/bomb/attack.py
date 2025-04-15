################################################################################

import glass.blastzone
import glass.geometry
import glass.log

################################################################################


def _attackgroundunit(self, target, result=None, blastzone=True, note=None):

    self.logwhenwhat("", "attacks %s." % target.name())

    if not target.isgroundunit():
        raise RuntimeError("invalid target.")

    if not glass.geometry.samehorizontalposition(self, target):
        raise RuntimeError("bombs is not at the position of the target.")

    target._takeattackdamage(self, result)
    self.lognote(note)
    self._remove()


################################################################################


def _secondaryattackgroundunit(self, target, result=None, note=None):

    self.logwhenwhat("", "attacks %s (secondary)." % target.name())

    if not target.isgroundunit():
        raise RuntimeError("invalid target.")

    if not glass.geometry.samehorizontalposition(self, target):
        raise RuntimeError("the bombs are not at the position of the target.")

    target._takeattackdamage(self, result)
    self.lognote(note)


################################################################################


def blastzone(self, name, note=None):

    try:
        blastzone = glass.blastzone.BlastZone(name, *self.xy())
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()
    return blastzone


################################################################################
