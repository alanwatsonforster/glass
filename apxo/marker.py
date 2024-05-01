import apxo.draw as apdraw
import apxo.log as aplog

from apxo.element import element

##############################################################################


class marker(element):

    ############################################################################

    def __init__(
        self, type, hexcode, azimuth=0, speed=0, altitude=0, name="", color="black"
    ):

        aplog.clearerror()
        try:

            if not type in ["dot", "circle", "square"]:
                raise RuntimeError("invalid marker type.")

            super().__init__(
                name,
                hexcode=hexcode,
                azimuth=azimuth,
                altitude=altitude,
                speed=speed,
                color=color,
            )

            self._type = type
            self._removed = False

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def ismarker(self):
        return True

    #############################################################################

    def _startturn(self):
        pass

    def _endturn(self):
        pass

    ############################################################################

    def _draw(self):

        if self._removed:
            return

        if self._type == "dot":

            apdraw.drawdot(*self.xy(), size=0.1, fillcolor=self.color())

        elif self._type == "circle":

            apdraw.drawcircle(
                *self.xy(), size=0.65, linecolor=self.color(), linewidth=2
            )
            apdraw.drawtext(*self.xy(), self.facing(), self.name(), color=self.color())

        elif self._type == "square":

            apdraw.drawsquare(
                *self.xy(),
                size=0.65,
                linecolor=self.color(),
                linewidth=2,
                facing=self.facing()
            )
            apdraw.drawtext(*self.xy(), self.facing(), self.name(), color=self.color())
