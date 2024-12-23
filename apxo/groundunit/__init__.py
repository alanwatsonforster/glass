import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.log as aplog
import apxo.barragefire as apbarragefire
import apxo.plottedfire as applottedfire

##############################################################################


def aslist(withkilled=False):
    elementlist = apelement.aslist()
    groundunitlist = filter(lambda E: E.isgroundunit(), elementlist)
    if not withkilled:
        groundunitlist = filter(lambda x: not x.killed(), groundunitlist)
    return list(groundunitlist)


##############################################################################


class groundunit(apelement.element):

    ############################################################################

    def __init__(
        self,
        name,
        hexcode,
        symbols="",
        color="white",
        barragefirealtitude=None,
        canuseplottedfire=False,
        stack=None,
    ):

        self._name = ""

        aplog.clearerror()
        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating ground unit %s." % name)

            super().__init__(
                name,
                hexcode=hexcode,
                altitude=None,
                speed=0,
                color=color,
            )

            if isinstance(symbols, str):
                symbols = symbols.split("/")
            for symbol in symbols:
                if symbol not in [
                    "infantry",
                    "armor",
                    "artillery",
                    "reconnaissance",
                    "airdefense",
                    "supply",
                    "transportation",
                    "ammunition",
                    "fuel",
                    "ordnance",
                    "headquarter",
                    "light",
                    "medium",
                    "heavy",
                    "missile",
                    "gun",
                    "multiplerocket",
                    "radar",
                    "motorized",
                    "wheeled",
                    "limitedwheeled",
                    "locomotive",
                    "railcar",
                    "barge",
                    "truck",
                ]:
                    raise RuntimeError('invalid ground unit symbol "%s".' % symbol)
            self._symbols = symbols
            self._stack = stack

            self._damagelevel = 0

            self._barragefire = None
            self._barragefirealtitude = barragefirealtitude
            self._plottedfire = None
            self._canuseplottedfire = canuseplottedfire

        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    #############################################################################

    def isgroundunit(self):
        return True

    #############################################################################

    def _properties(self):
        return []

    #############################################################################

    def _endgameturn(self):
        self._suppressionlevel -= 1
        self.stopusingbarragefire()

    ############################################################################

    def isusingbarragefire(self):
        "Return true if the ground unit it using barrage fire otherwise return false."
        return self._barragefire is not None

    def stopusingbarragefire(self):
        "Stop using barrage fire."
        if self.isusingbarragefire():
            self._barragefire._remove()
            self._barragefire = None

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

    def _barragefiremaximumaltitude(self):
        "Return the maximum altitude of barrage fire."
        return self.altitude() + self._barragefirealtitude

    ############################################################################

    def isusingplottedfire(self):
        "Return true if the ground unit it using plotted fire otherwise return false."
        return self._plottedfire is not None

    def stopusingplottedfire(self):
        "Stop using plotted fire."
        if self.isusingplottedfire():
            self._plottedfire._remove()
            self._plottedfire = None

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

    def _plottedfiremaximumaltitude(self):
        "Return the maximum altitude of plotted fire."
        return self.altitude() + self._plottedfirealtitude

    ############################################################################

    from apxo.groundunit.attack import _attackaircraft

    from apxo.groundunit.damage import (
        _initdamage,
        _damage,
        _damageatleast,
        _damageatmost,
        _takedamage,
        _takedamageconsequences,
        _issuppressed,
    )

    from apxo.groundunit.draw import _draw

    ############################################################################
