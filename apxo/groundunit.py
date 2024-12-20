import apxo.draw as apdraw
import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.log as aplog
import apxo.marker as apmarker

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

    def __init__(self, name, hexcode, symbols="", color="white", barragefirealtitude=None, stack=None):

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

            self._barragefiremarker = None
            self._barragefirealtitude = barragefirealtitude

        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    #############################################################################

    def isgroundunit(self):
        return True

    #############################################################################
    
    def _damage(self):
        if self._damagelevel == 0:
            if self.issuppressed():
                return "S"
            else:
                return "" 
        elif self._damagelevel == 1:
            if self.issuppressed():
                return "D+S"
            else:
                return "D"
        elif self._damagelevel == 2:
            if self.issuppressed():
                return "2D+S"
            else:
                return "2D"
        else:
            return "K"
            
    def _takedamage(self, damage):
        self._suppressionlevel = 2
        if damage == "S":
            pass
        elif damage == "D":
            self._damagelevel += 1
        elif damage == "2D":
            self._damagelevel += 2
        elif damage == "K":
            self._damagelevel += 3
        else:
            raise RuntimeError("invalid damage %r" % damage)

    def _takedamageconsequences(self):
        if self._barragefiremarker is not None:
            self.logwhenwhat("", "%s ceases barrage fire." % self.name())
            self._barragefiremarker._remove()
            self._barragefiremarker = None
    
    #############################################################################

    def _properties(self):
        return []

    #############################################################################

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        self._suppressionlevel -= 1
        if self._barragefiremarker is not None:
            self._barragefiremarker._remove()
            self._barragefiremarker = None

    ############################################################################

    def _draw(self):
        apdraw.drawgroundunit(
            *self.xy(),
            self._symbols,
            self.color(),
            self.name(),
            self._stack,
            self._killed
        )

    ############################################################################

    def usebarragefire(self, note=None):
        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            self._checknotkilled()
            self._checknotremoved()
            self._checknotsuppressed()
            if self._barragefirealtitude is None:
                raise RuntimeError("%s is not capable of barrage fire." % self.name())
            maximumaltitude = self.altitude() + self._barragefirealtitude
            self.logwhenwhat("", "using barrage fire to altitude %d." % maximumaltitude)
            self._barragefiremarker = apmarker.marker("barragefire", self.hexcode(), altitude=maximumaltitude, silent=True)
            self.lognote(note)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()
    
