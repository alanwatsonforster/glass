import apxo.draw as apdraw
import apxo.element as apelement
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

    def __init__(self, name, hexcode, symbols="", color="white", stack=None):

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
                return "none" 
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
        pass
    
    #############################################################################

    def _properties(self):
        return []

    #############################################################################

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        self._suppressionlevel -= 1

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
