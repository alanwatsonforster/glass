import apxo.draw as apdraw
import apxo.element as apelement
import apxo.log as aplog

##############################################################################


class groundunit(apelement.element):

    ############################################################################

    def __init__(self, name, hexcode, symbols="", color="white", stack=None):

        aplog.clearerror()
        try:

            super().__init__(
                name,
                hexcode=hexcode,
                altitude=None,
                speed=0,
                color=color,
            )

            if isinstance(symbols, str):
                symbols = symbols.split("/")
            self._symbols = symbols
            self._stack = stack

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

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        pass

    ############################################################################

    def _draw(self):
        apdraw.drawgroundunit(
            *self.xy(), self._symbols, self.color(), self.name(), self._stack, self._killed
        )
