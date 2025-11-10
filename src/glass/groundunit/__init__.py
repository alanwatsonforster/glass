import glass.element
import glass.gameturn
import glass.log

################################################################################


def aslist(withkilled=False):
    elementlist = glass.element.aslist()
    groundunitlist = filter(lambda E: E.isgroundunit(), elementlist)
    if not withkilled:
        groundunitlist = filter(lambda x: not x.killed(), groundunitlist)
    return list(groundunitlist)


################################################################################

from glass.groundunit.data import _loaddata

################################################################################


class GroundUnit(glass.element.Element):

    ############################################################################

    def __init__(
        self,
        name,
        hexcode,
        type=None,
        symbols=None,
        uppertext=None,
        lowertext=None,
        aaaclass=None,
        aaarange=None,
        aaadamagerating=None,
        aaamaximumrelativealtitude=None,
        stack=None,
        color="white",
        azimuth=None,
        sightingrange=None,
        defensestrength=None,
        protectionclass=None,
        sighted=False,
        identified=False,
        counter=False,
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
                if uppertext is None and "uppertext" in data:
                    uppertext = data["uppertext"]
                if lowertext is None and "lowertext" in data:
                    lowertext = data["lowertext"]
                if "aaa" in data:
                    aaa = data["aaa"]
                    if aaaclass is None and "class" in aaa:
                        aaaclass = aaa["class"]
                    if aaarange is None and "range" in aaa:
                        aaarange = aaa["range"]
                    if aaadamagerating is None and "damagerating" in aaa:
                        aaadamagerating = aaa["damagerating"]
                    if (
                        aaamaximumrelativealtitude is None
                        and "maximumrelativealtitude" in aaa
                    ):
                        aaamaximumrelativealtitude = aaa["maximumrelativealtitude"]
                if sightingrange is None and "sightingrange" in data:
                    sightingrange = data["sightingrange"]
                if defensestrength is None and "defensestrength" in data:
                    defensestrength = data["defensestrength"]

            if symbols is None:
                raise RuntimeError("invalid symbols argument.")
            if isinstance(symbols, str):
                if symbols == "":
                    symbols = []
                else:
                    symbols = symbols.split("/")
            for symbol in symbols:
                if symbol not in [
                    "unidentified",
                    "infantry",
                    "transport",
                    "armor",
                    "armour",
                    "artillery",
                    "reconnaissance",
                    "air-defense",
                    "air-defence",
                    "antiarmor",
                    "antiarmour",
                    "supply",
                    "transportation",
                    "ammunition",
                    "fuel",
                    "ordnance",
                    "headquarters",
                    "missile",
                    "gun",
                    "rocket",
                    "radar",
                    "locomotive",
                    "railcar",
                    "truck",
                    "barge",
                    "junk",
                    "smallbuilding",
                    "largebuilding",
                    "factory",
                    "bridge",
                    "tower",
                    "hangar",
                    "shelter",
                    "fixedwing",
                    "rotarywing",
                    "hex",
                    "light",
                    "medium",
                    "heavy",
                    "fac",
                    "squad",
                    "section",
                    "platoon",
                    "company",
                    "battery",
                ]:
                    raise RuntimeError('invalid ground unit symbol "%s".' % symbol)

            if aaaclass not in [None, "B", "L", "M", "H"]:
                raise RuntimeError("invalid aaaclass %r." % aaaclass)

            if aaaclass == "H" and azimuth is None:
                raise RuntimeError("heavy AAA ground units must have an azimuth.")
            if aaaclass != "H" and azimuth is not None:
                raise RuntimeError("only heavy AAA ground units may have an azimuth.")

            if sightingrange is None:
                raise RuntimeError("no sighting range specified.")

            if protectionclass not in [None, "entrenched", "bunkered"]:
                raise RuntimeError('invalid protection class "%r".' % protectionclass)

            super().__init__(
                name,
                hexcode=hexcode,
                altitude=None,
                speed=0,
                color=color,
                azimuth=azimuth,
                sighted=sighted,
                identified=identified,
            )

            self._symbols = symbols
            self._uppertext = uppertext
            self._lowertext = lowertext
            self._counter = counter
            self._stack = stack

            self._aaaclass = aaaclass
            self._aaarange = aaarange
            self._aaamaximumrelativealtitude = aaamaximumrelativealtitude
            self._aaadamagerating = aaadamagerating

            self._sightingrange = sightingrange
            self._defensestrength = defensestrength

            self._protectionclass = protectionclass

            self._initattack()
            self._inittracking()

        except RuntimeError as e:
            glass.log.logexception(e)
        self.logbreak()

    ############################################################################

    def isgroundunit(self):
        return True

    ############################################################################

    def _properties(self):
        return []

    ############################################################################

    def _endgameturn(self):
        self._endgameturndamage()
        self._endgameturnattack()

    ############################################################################

    from glass.groundunit.attack import (
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
    from glass.groundunit.damage import (
        _initdamage,
        _endgameturndamage,
        _damage,
        _damageatleast,
        _damageatmost,
        _takedamage,
        _takedamageconsequences,
        _issuppressed,
    )
    from glass.groundunit.draw import _draw
    from glass.groundunit.move import _move, _continuemove
    from glass.groundunit.track import (
        _maximumtrackingrange,
        _trackingrequirement,
        _track,
        _stoptracking,
    )


################################################################################


def HexGroundUnit(hexcode):
    return GroundUnit(hexcode, hexcode, symbols="hex")


################################################################################
