################################################################################

import apxo.barragefire as apbarragefire
import apxo.gameturn as apgameturn
import apxo.geometry as apgeometry
import apxo.log as aplog
import apxo.plottedfire as applottedfire

################################################################################


def _attackaircraft(self, target, result=None):

    if self.isusingbarragefire():

        if apgeometry.horizontalrange(self, target) > 1:
            raise RuntimeError("target is out of range of the barrage fire.")
        if target.altitude() > self._barragefiremaximumaltitude():
            raise RuntimeError("target is above the barrage fire.")
        self.logwhenwhat(
            "", "%s attacks %s with barrage fire." % (self.name(), target.name())
        )

    elif self.isusingplottedfire():

        if apgeometry.horizontalrange(self._plottedfire, target) > 1:
            raise RuntimeError("target is out of range of the plotted fire.")
        if target.altitude() < self._plottedfire.altitude() - 2:
            raise RuntimeError("target is below the plotted fire.")
        if target.altitude() > self._plottedfire.altitude() + 2:
            raise RuntimeError("target is above the plotted fire.")
        self.logwhenwhat(
            "", "%s attacks %s with plotted fire." % (self.name(), target.name())
        )

    else:

        self.logwhenwhat(
            "", "%s attacks %s with aimed fire." % (self.name(), target.name())
        )
        if self._tracking is not target:
            raise RuntimeError("%s is not tracking %s." % (self.name(), target.name()))
        self.logwhenwhat("", "range to target is %d." % apgeometry.range(self, target))
        self.logwhenwhat(
            "", "altitude to target is %d." % (target.altitude() - self.altitude())
        )

    target._takeattackdamage(self, result)


################################################################################

def isusingbarragefire(self):
    "Return true if the ground unit it using barrage fire otherwise return false."
    return self._barragefire is not None

def usebarragefire(self, note=None):
    "Use barrage fire."
    aplog.clearerror()
    try:
        apgameturn.checkingameturn()
        self._checknotkilled()
        self._checknotremoved()
        self._checknotsuppressed()
        if self._barragefirealtitude is None:
            raise RuntimeError("%s is not capable of barrage fire." % self.name())
        self.logwhenwhat("", "using barrage fire.")
        self._barragefire = apbarragefire.barragefire(
            self.hexcode(), altitude=self._barragefiremaximumaltitude()
        )
        self.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()

def stopusingbarragefire(self):
    "Stop using barrage fire."
    if self.isusingbarragefire():
        self._barragefire._remove()
        self._barragefire = None

def _barragefiremaximumaltitude(self):
    "Return the maximum altitude of barrage fire."
    return self.altitude() + self._barragefirealtitude

################################################################################

def isusingplottedfire(self):
    "Return true if the ground unit it using plotted fire otherwise return false."
    return self._plottedfire is not None

def useplottedfire(self, hexcode, altitude, note=None):
    "Use plotted fire."
    aplog.clearerror()
    try:
        apgameturn.checkingameturn()
        self._checknotkilled()
        self._checknotremoved()
        self._checknotsuppressed()
        if not self._canuseplottedfire:
            raise RuntimeError("%s is not capable of plotted fire." % self.name())
        self.logwhenwhat("", "using plotted fire.")
        self._plottedfire = applottedfire.plottedfire(
            hexcode, altitude
        )
        self.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()

def stopusingplottedfire(self):
    "Stop using plotted fire."
    if self.isusingplottedfire():
        self._plottedfire._remove()
        self._plottedfire = None

def _plottedfiremaximumaltitude(self):
    "Return the maximum altitude of plotted fire."
    return self.altitude() + self._plottedfirealtitude

################################################################################
