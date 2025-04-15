import apxo.altitude
import apxo.element
import apxo.log

##############################################################################


class BarrageFire(apxo.element.Element):

    ############################################################################

    def __init__(self, hexcode, altitude):

        self._name = ""

        self.logwhenwhat("", "creating barrage fire zone.")

        super().__init__(
            None,
            hexcode=hexcode,
            azimuth=None,
            altitude=altitude,
            speed=0,
        )

        self.logwhenwhat(
            "",
            "barrage fire zone centered on %s extends to altitude %d."
            % (self.hexcode(), self.altitude()),
        )

    #############################################################################

    def isbarragefire(self):
        return True

    #############################################################################

    def _endgameturn(self):
        self._remove()

    ############################################################################

    from apxo.barragefire.draw import _draw

    ############################################################################
