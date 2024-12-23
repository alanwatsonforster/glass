################################################################################

import apxo.flight as apflight

################################################################################


def _move(self, moves):
    apflight._move(self, "MS", None, moves)


def _continuemove(self, moves, note=None):
    apflight._continuemove(self, moves)


################################################################################
