import apxo.altitude as apaltitude
import apxo.element as apelement
import apxo.log as aplog

##############################################################################


class barragefire(apelement.element):

    ############################################################################

    def __init__(self, x, y, altitude):

        self._name = ""

        self.logwhenwhat("", "creating barrage fire zone.")

        super().__init__(
            None,
            x=x,
            y=y,
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
