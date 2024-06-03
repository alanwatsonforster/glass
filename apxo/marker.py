import apxo.draw as apdraw
import apxo.element as apelement
import apxo.log as aplog

##############################################################################


class marker(apelement.element):

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

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def ismarker(self):
        return True

    #############################################################################

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        pass

    ############################################################################

    def _draw(self):

        zorder = self.altitude() + 1
        if self._type == "dot":

            apdraw.drawdot(*self.xy(), size=0.1, fillcolor=self.color(), zorder=zorder)

        elif self._type == "circle":

            apdraw.drawcircle(
                *self.xy(), size=0.65, linecolor=self.color(), linewidth=2
            )
            apdraw.drawtext(
                *self.xy(),
                self.facing(),
                self.name(),
                color=self.color(),
                zorder=zorder
            )

        elif self._type == "square":

            apdraw.drawsquare(
                *self.xy(),
                size=0.65,
                linecolor=self.color(),
                linewidth=2,
                facing=self.facing(),
                zorder=zorder
            )
            apdraw.drawtext(*self.xy(), self.facing(), self.name(), color=self.color())
