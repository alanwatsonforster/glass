import glass.altitude
import glass.element
import glass.log

##############################################################################


class BlastZone(glass.element.Element):

    ############################################################################

    def __init__(self, name, x, y):

        self._name = ""

        if not isinstance(name, str):
            raise RuntimeError("the name argument must be a string.")

        self.logwhenwhat("", "creating blast zone %s." % name)

        super().__init__(
            name,
            x=x,
            y=y,
            azimuth=None,
            altitude=glass.altitude.terrainaltitude(x, y) + 2,
            speed=0,
        )

        self.logwhenwhat(
            "",
            "blast zone in %s extends to altitude %d."
            % (self.hexcode(), self.altitude()),
        )

    #############################################################################

    def isblastzone(self):
        return True

    #############################################################################

    def _endgameturn(self):
        self._remove()

    ############################################################################

    from glass.blastzone.attack import _attackaircraft
    from glass.blastzone.draw import _draw

    ############################################################################
