import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.log as aplog

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
        maximumaltitude=None,
        aaaclass=None,
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

            self._maximumaltitude = maximumaltitude
            if aaaclass not in [None, "B", "L", "M", "H"]:
                raise RuntimeError('invalid aaaclass %r.' % aaaclass)
            self._aaaclass = aaaclass
            
            self._initattack()
            self._inittracking()

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

    from apxo.groundunit.attack import (
        _initattack,
        _attackaircraft,
        usebarragefire,
        stopusingbarragefire,
        isusingbarragefire,
        useplottedfire,
        stopusingplottedfire,
        isusingplottedfire,
    )

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
    from apxo.groundunit.track import _track, _stoptracking

    ############################################################################
