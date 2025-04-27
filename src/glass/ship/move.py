################################################################################

import glass.azimuth
import glass.hex
import glass.hexcode

################################################################################


def _move(self, s):
    self.logposition("start")
    self._continuemove(s)


def _continuemove(self, s):
    self._setlastposition()
    self.logwhenwhat("", s)
    if s == "RR/H" or s == "R60/H":
       self._moveturn("R", 60)
    elif s == "LL/H" or s == "L60/H":
       self._moveturn("L", 60)
    elif s != "H":
        raise RuntimeError('invalid move "%s".' % s)
    newx, newy = glass.hex.forward(self._x, self._y, self._facing)
    self._setposition(x=newx, y=newy)
    self._extendpath()
    self.logposition("")

################################################################################
