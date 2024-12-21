################################################################################

import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.hex as aphex
import apxo.gameturn as apgameturn
import apxo.log as aplog

################################################################################


def move(self, *args, note=None, **kwargs):
    aplog.clearerror()
    try:
        apgameturn.checkingameturn()
        self._checknotkilled()
        self._checknotremoved()
        if self._startedmoving:
            raise RuntimeError("%s has already started moving." % self.name())
        self._startedmoving = True
        self._move(*args, **kwargs)
        self.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


def continuemove(self, *args, note=None, **kwargs):
    aplog.clearerror()
    try:
        apgameturn.checkingameturn()
        self._checknotkilled()
        self._checknotremoved()
        if not self._startedmoving:
            raise RuntimeError("%s has not started moving." % self.name())
        self._continuemove(*args, **kwargs)
        self.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()


################################################################################


def _move(self, s):
    self._continuemove(s)


def _continuemove(self, s):
    if apazimuth.isvalidazimuth(s):
        x, y = aphex.forward(self._x, self._y, apazimuth.tofacing(s))
        self._setposition(x=x, y=y)
    else:
        self._setposition(hexcode=s)


################################################################################


def _moveforward(self):
    self._setxy(*aphex.forward(self.x(), self.y(), self.facing()))


def _moveclimb(self, altitudechange):
    altitude, altitudecarry = apaltitude.adjustaltitude(
        self.altitude(), self.altitudecarry(), +altitudechange
    )
    self._setposition(altitude=altitude, altitudecarry=altitudecarry)


def _movedive(self, altitudechange):
    altitude, altitudecarry = apaltitude.adjustaltitude(
        self.altitude(), self.altitudecarry(), -altitudechange
    )
    self._setposition(altitude=altitude, altitudecarry=altitudecarry)


def _moveturn(self, sense, facingchange):
    if aphex.isside(self.x(), self.y()):
        self._setxy(*aphex.sidetocenter(self.x(), self.y(), self.facing(), sense))
    if sense == "L":
        self._setfacing((self.facing() + facingchange) % 360)
    else:
        self._setfacing((self.facing() - facingchange) % 360)


def _moveslide(self, sense):
    self._setxy(*aphex.slide(self.x(), self.y(), self.facing(), sense))


def _movedisplacementroll(self, sense):
    self._setxy(*aphex.displacementroll(self.x(), self.y(), self.facing(), sense))


def _movelagroll(self, sense):
    self._setxy(*aphex.lagroll(self.x(), self.y(), self.facing(), sense))
    if sense == "R":
        self._setfacing((self.facing() + 30) % 360)
    else:
        self._setfacing((self.facing() - 30) % 360)


def _moveverticalroll(self, sense, facingchange, shift):
    if aphex.isside(self.x(), self.y()) and shift:
        self._setxy(*aphex.sidetocenter(self.x(), self.y(), self.facing(), sense))
    if sense == "L":
        self._setfacing((self.facing() + facingchange) % 360)
    else:
        self._setfacing((self.facing() - facingchange) % 360)


################################################################################
