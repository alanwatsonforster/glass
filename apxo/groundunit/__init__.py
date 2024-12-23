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

keywordsdict = {
    "infantry": { 
        "symbols": "infantry", 
        "aaaclass": "B", 
        "maximumaltitude": 2 
    },
    "ZPU-1": {
        "symbols": "airdefense/gun/light", 
        "aaaclass": "L", 
        "maximumaltitude": 6
    },
    "ZPU-4": {
        "symbols": "airdefense/gun/light", 
        "aaaclass": "L", 
        "maximumaltitude": 6
    },
    "ZU-23": {
        "symbols": "airdefense/gun/light", 
        "aaaclass": "L", 
        "maximumaltitude": 9
    },
    "S-60": {
        "symbols": "airdefense/gun/medium", 
        "aaaclass": "M", 
        "maximumaltitude": 18
    },
}
    
################################################################################


class groundunit(apelement.element):

    ############################################################################

    def __init__(
        self,
        name,
        hexcode,
        typename=None,
        symbols=None,
        maximumaltitude=None,
        aaaclass=None,
        stack=None,
        color="white",
    ):

        self._name = ""

        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating ground unit %s." % name)
            
            if typename is not None:
                self.logwhenwhat("", "type is %s." % typename)
                if typename not in keywordsdict:
                    raise RuntimeError("invalid ground unit type \"%s\"." % typename)
                keywords = keywordsdict[typename]
                if symbols is None and "symbols" in keywords:
                    symbols = keywords["symbols"]
                if aaaclass is None and "aaaclass" in keywords:
                    aaaclass = keywords["aaaclass"]
                if maximumaltitude is None and "maximumaltitude" in keywords:
                    maximumaltitude = keywords["maximumaltitude"]

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
                raise RuntimeError("invalid aaaclass %r." % aaaclass)
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
        self._endgameturndamage()
        self._endgameturnattack()

    ############################################################################

    from apxo.groundunit.attack import (
        _initattack,
        _endgameturnattack,
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
    from apxo.groundunit.track import _track, _stoptracking

    ############################################################################
