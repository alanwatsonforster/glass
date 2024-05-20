import apxo.draw as apdraw
import apxo.element as apelement
import apxo.log as aplog

##############################################################################


class groundunit(apelement.element):

    ############################################################################

    def __init__(self, name, type, hexcode, color="black"):

        aplog.clearerror()
        try:

            super().__init__(
                name,
                hexcode=hexcode,
                altitude=None,
                speed=0,
                color=color,
            )

            self._type = type
            self._removed = False

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def isgroundunit(self):
        return True

    #############################################################################

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        pass

    ############################################################################

    def _draw(self):

        if self._removed:
            return

        apdraw.drawgroundunit(*self.xy(), self._type, self.color(), self.name())
