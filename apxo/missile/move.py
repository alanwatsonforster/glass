################################################################################

import apxo.flight

################################################################################


def _move(self, moves):
    apxo.flight._move(self, "MS", None, moves)


def _continuemove(self, moves, note=None):
    apxo.flight._continuemove(self, moves)


################################################################################
