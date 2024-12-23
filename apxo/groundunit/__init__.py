import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.log as aplog
import apxo.barragefire as apbarragefire

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
            self.logwhenwhat(
                "",
                "using barrage fire to altitude %d."
                % self._barragefiremaximumaltitude(),
            )
            self._barragefire = apbarragefire.barragefire(
                *self.xy(),
                altitude=self._barragefiremaximumaltitude()
            )
            self.lognote(note)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    def _barragefiremaximumaltitude(self):
        "Return the maximum altitude of barrage fire."
        return self.altitude() + self._barragefirealtitude

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
