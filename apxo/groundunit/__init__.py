import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.log as aplog

################################################################################


def aslist(withkilled=False):
    elementlist = apelement.aslist()
    groundunitlist = filter(lambda E: E.isgroundunit(), elementlist)
    if not withkilled:
        groundunitlist = filter(lambda x: not x.killed(), groundunitlist)
    return list(groundunitlist)


################################################################################

from apxo.groundunit.data import _loaddata

################################################################################

class groundunit(apelement.element):

    ############################################################################

    def __init__(
        self,
        name,
        hexcode,
        type=None,
        symbols=None,
        aaaclass=None,
        aaarange=None,
        aaadamagerating=None,
        aaamaximumrelativealtitude=None,
        stack=None,
        color="white",
    ):

        self._name = ""

        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating ground unit %s." % name)

            if type is not None:
                self.logwhenwhat("", "type is %s." % type)
                data = _loaddata(type)
                if symbols is None and "symbols" in data:
                    symbols = data["symbols"]
                if aaaclass is None and "aaaclass" in data:
                    aaaclass = data["aaaclass"]
                if aaarange is None and "aaarange" in data:
                    aaarange = data["aaarange"]
                if aaadamagerating is None and "aaadamagerating" in data:
                    aaadamagerating = data["aaadamagerating"]
                if (
                    aaamaximumrelativealtitude is None
                    and "aaamaximumrelativealtitude" in data
                ):
                    aaamaximumrelativealtitude = data["aaamaximumrelativealtitude"]
                    
            if symbols is None:
                raise RuntimeError("invalid symbols argument.")
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
                    "headquarters",
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
                    "hex",
                ]:
                    raise RuntimeError('invalid ground unit symbol "%s".' % symbol)

            if aaaclass not in [None, "B", "L", "M", "H"]:
                raise RuntimeError("invalid aaaclass %r." % aaaclass)

            super().__init__(
                name,
                hexcode=hexcode,
                altitude=None,
                speed=0,
                color=color,
            )

            self._symbols = symbols
            self._stack = stack

            self._aaaclass = aaaclass
            self._aaarange = aaarange
            self._aaamaximumrelativealtitude = aaamaximumrelativealtitude
            self._aaadamagerating = aaadamagerating

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
        self._endgameturndamage()
        self._endgameturnattack()

    ############################################################################

    from apxo.groundunit.attack import (
        _initattack,
        _endgameturnattack,
        _aaarangeclass,
        _aaamaximumrange,
        _aaamaximumaltitude,
        _attackaircraft,
        usebarragefire,
        stopusingbarragefire,
        isusingbarragefire,
        useplottedfire,
        stopusingplottedfire,
        isusingplottedfire,
        resupplyammunition,
    )

    from apxo.groundunit.damage import (
        _initdamage,
        _endgameturndamage,
        _damage,
        _damageatleast,
        _damageatmost,
        _takedamage,
        _takedamageconsequences,
        _issuppressed,
    )

    from apxo.groundunit.draw import _draw
    from apxo.groundunit.track import (
        _maximumtrackingrange,
        _trackingrequirement,
        _track,
        _stoptracking,
    )

################################################################################

def hexgroundunit(hexcode):
    return groundunit(hexcode, hexcode, symbols="hex")

################################################################################

