################################################################################

import glass.barragefire
import glass.gameturn
import glass.geometry
import glass.log
import glass.plottedfire

################################################################################


def _initattack(self):
    self._barragefire = None
    self._plottedfire = None
    self._outofammunition = False


################################################################################


def _endgameturnattack(self):
    self.stopusingbarragefire()


################################################################################


def _aaarangeclass(self, range):
    if self._aaarange is None:
        return None
    if range <= self._aaarange[0]:
        return "short"
    elif range <= self._aaarange[1]:
        return "medium"
    elif range <= self._aaarange[2]:
        return "long"
    else:
        return None


def _aaamaximumrange(self):
    if self._aaarange is None:
        return None
    else:
        return self._aaarange[2]


def _aaamaximumaltitude(self):
    if self._aaamaximumrelativealtitude is None:
        return None
    else:
        return self.altitude() + self._aaamaximumrelativealtitude


################################################################################


def _attackaircraft(self, target, result=None, note=None):

    if self.isusingbarragefire():

        self.logwhenwhat("", "attacks %s with barrage fire." % target.name())
        if glass.geometry.horizontalrange(self, target) > 1:
            raise RuntimeError("target is outside the barrage fire zone.")
        if target.altitude() > self._aaamaximumaltitude():
            raise RuntimeError("target is above the barrage fire.")

    elif self.isusingplottedfire():

        self.logwhenwhat("", "attacks %s with plotted fire." % target.name())
        if glass.geometry.horizontalrange(self._plottedfire, target) > 1:
            raise RuntimeError("target is outside the plotted fire zone.")
        if target.altitude() < self._plottedfire.altitude() - 2:
            raise RuntimeError("target is below the plotted fire.")
        if target.altitude() > self._plottedfire.altitude() + 2:
            raise RuntimeError("target is above the plotted fire.")

    elif self._aaarange is not None:

        self.logwhenwhat("", "attacks %s with aimed fire." % target.name())
        if self._outofammunition:
            raise RuntimeError("%s is out of ammunition." % self.name())
        if self._tracking is not target:
            raise RuntimeError("%s is not tracking %s." % (self.name(), target.name()))

        range = glass.geometry.range(self, target)
        rangeclass = self._aaarangeclass(range)
        if rangeclass is None:
            self.logcomment("range to target is %d." % range)
            raise RuntimeError(
                "%s is beyond the maximum range of %d."
                % (target.name(), self._aaamaximumrange())
            )
        self.logcomment("range to target is %d (%s)." % (range, rangeclass))
        self.logcomment(
            "altitude to target is %d." % (target.altitude() - self.altitude())
        )
        if target.altitude() > self._aaamaximumaltitude():
            raise RuntimeError(
                "%s is above the maximum altitude of %d."
                % (target.name(), self._aaamaximumaltitude())
            )
    else:
        raise RuntimeError("%s cannot attack aircraft." % self.name())

    if self.issuppressed():
        raise RuntimeError("%s is suppressed" % self.name())

    target._takeattackdamage(self, result)

    if not self.isusingbarragefire() and not self.isusingplottedfire():
        self._stoptracking()

    self.lognote(note)


################################################################################


def isusingbarragefire(self):
    "Return true if the ground unit it using barrage fire otherwise return false."
    return self._barragefire is not None


def usebarragefire(self, note=None):
    "Use barrage fire."
    try:
        glass.gameturn.checkingameturn()
        self.logwhenwhat("", "is using barrage fire.")
        self._checknotkilled()
        self._checknotremoved()
        self._checknotsuppressed()
        if self._aaaclass not in ["B", "L", "M"]:
            raise RuntimeError("%s is not capable of barrage fire." % self.name())
        if self._outofammunition:
            raise RuntimeError("%s is out of ammunition." % self.name())
        if self._aaaclass in ["L", "M"]:
            self.logwhenwhat("", "will be out of ammunition.")
            self._outofammunition = True
        self._barragefire = glass.barragefire.BarrageFire(
            self.hexcode(), altitude=self.altitude() + self._aaamaximumrelativealtitude
        )
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


def stopusingbarragefire(self):
    "Stop using barrage fire."
    if self.isusingbarragefire():
        self._barragefire._remove()
        self._barragefire = None


################################################################################


def isusingplottedfire(self):
    "Return true if the ground unit it using plotted fire otherwise return false."
    return self._plottedfire is not None


def useplottedfire(self, hexcode, altitude, note=None):
    "Use plotted fire."
    try:
        glass.gameturn.checkingameturn()
        self.logwhenwhat("", "is using plotted fire.")
        self._checknotkilled()
        self._checknotremoved()
        self._checknotsuppressed()
        if self._aaaclass not in ["M", "H"]:
            raise RuntimeError("%s is not capable of plotted fire." % self.name())
        if self._outofammunition:
            raise RuntimeError("%s is out of ammunition." % self.name())
        self._plottedfire = glass.plottedfire.PlottedFire(hexcode, altitude)
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


def stopusingplottedfire(self):
    "Stop using plotted fire."
    if self.isusingplottedfire():
        self._plottedfire._remove()
        self._plottedfire = None


################################################################################


def resupplyammunition(self, note=None):
    "Resupply ammunition."
    try:
        glass.gameturn.checkingameturn()
        self.logwhenwhat("", "is resupplied with ammunition.")
        self._checknotkilled()
        self._checknotremoved()
        self._checknotsuppressed()
        self._outofammunition = False
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################
