################################################################################

import apxo.azimuth
import apxo.hex
import apxo.hexcode

################################################################################


def _move(self, s):
    self.logposition("start")
    self._continuemove(s)


def _continuemove(self, s):
    self._setlastposition()
    self.logwhenwhat("", s)
    if self._facing is not None:
        if s == "R" or s == "R30":
            self._moveturn("R", 30)
        elif s == "RR" or s == "R60":
            self._moveturn("R", 60)
        elif s == "L" or s == "L30":
            self._moveturn("L", 30)
        elif s == "LL" or s == "L60":
            self._moveturn("L", 60)
    elif apxo.hexcode.isvalidhexcodeforcenter(s):
        self._setposition(hexcode=s)
    elif apxo.azimuth.isvalidazimuth(s):
        newx, newy = apxo.hex.forward(self._x, self._y, apxo.azimuth.tofacing(s))
        if not apxo.hex.iscenter(newx, newy):
            raise RuntimeError('invalid azimuth "%s" for move.' % s)
        self._setposition(x=newx, y=newy)
    else:
        raise RuntimeError('invalid move "%s".' % s)
    self.logposition("")


################################################################################
