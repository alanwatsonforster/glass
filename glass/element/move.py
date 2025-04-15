################################################################################

import apxo.altitude
import apxo.azimuth
import apxo.hex
import apxo.gameturn
import apxo.log

################################################################################


def move(self, *args, note=None, **kwargs):
    try:
        apxo.gameturn.checkingameturn()
        self._checknotkilled()
        self._checknotremoved()
        if self._startedmoving:
            raise RuntimeError("%s has already started moving." % self.name())
        self._startedmoving = True
        self._move(*args, **kwargs)
        self.lognote(note)
    except RuntimeError as e:
        apxo.log.logexception(e)
    self.logbreak()


def continuemove(self, *args, note=None, **kwargs):
    try:
        apxo.gameturn.checkingameturn()
        self._checknotkilled()
        self._checknotremoved()
        if not self._startedmoving:
            raise RuntimeError("%s has not started moving." % self.name())
        self._continuemove(*args, **kwargs)
        self.lognote(note)
    except RuntimeError as e:
        apxo.log.logexception(e)
    self.logbreak()


################################################################################


def _move(self, *args):
    self._continuemove(*args)


def _continuemove(self, s):
    if apxo.azimuth.isvalidazimuth(s):
        x, y = apxo.hex.forward(self._x, self._y, apxo.azimuth.tofacing(s))
        self._setposition(x=x, y=y)
    else:
        self._setposition(hexcode=s)


################################################################################


def _moveforward(self):
    self._setxy(*apxo.hex.forward(self.x(), self.y(), self.facing()))


def _moveclimb(self, altitudechange):
    altitude, altitudecarry = apxo.altitude.adjustaltitude(
        self.altitude(), self.altitudecarry(), +altitudechange
    )
    self._setposition(altitude=altitude, altitudecarry=altitudecarry)


def _movedive(self, altitudechange):
    altitude, altitudecarry = apxo.altitude.adjustaltitude(
        self.altitude(), self.altitudecarry(), -altitudechange
    )
    self._setposition(altitude=altitude, altitudecarry=altitudecarry)


def _moveturn(self, sense, facingchange):
    if apxo.hex.isside(self.x(), self.y()):
        self._setxy(*apxo.hex.sidetocenter(self.x(), self.y(), self.facing(), sense))
    if sense == "L":
        self._setfacing((self.facing() + facingchange) % 360)
    else:
        self._setfacing((self.facing() - facingchange) % 360)


def _moveslide(self, sense):
    self._setxy(*apxo.hex.slide(self.x(), self.y(), self.facing(), sense))


def _movedisplacementroll(self, sense):
    self._setxy(*apxo.hex.displacementroll(self.x(), self.y(), self.facing(), sense))


def _movelagroll(self, sense):
    self._setxy(*apxo.hex.lagroll(self.x(), self.y(), self.facing(), sense))
    if sense == "R":
        self._setfacing((self.facing() + 30) % 360)
    else:
        self._setfacing((self.facing() - 30) % 360)


def _moveverticalroll(self, sense, facingchange, shift):
    if apxo.hex.isside(self.x(), self.y()) and shift:
        self._setxy(*apxo.hex.sidetocenter(self.x(), self.y(), self.facing(), sense))
    if sense == "L":
        self._setfacing((self.facing() + facingchange) % 360)
    else:
        self._setfacing((self.facing() - facingchange) % 360)


################################################################################
