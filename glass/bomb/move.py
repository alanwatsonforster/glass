################################################################################

import glass.hex

################################################################################


def _move(self):
    self.logposition("start")
    self._continuemove()


def _continuemove(self):
    self.logwhenwhat("FP", "H")
    x, y = glass.hex.forward(self._x, self._y, self.facing())
    self._setposition(x=x, y=y)
    self.logposition("")


################################################################################
