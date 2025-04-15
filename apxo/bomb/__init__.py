################################################################################

import apxo.azimuth
import apxo.element
import apxo.log

################################################################################


class Bomb(apxo.element.Element):

    ############################################################################

    def __init__(self, name, hexcode, facing, altitude, stores=None):

        self._name = ""

        if not isinstance(name, str):
            raise RuntimeError("the name argument must be a string.")

        self.logwhenwhat("", "creating bomb %s." % name)

        super().__init__(
            name,
            hexcode=hexcode,
            azimuth=apxo.azimuth.fromfacing(facing),
            altitude=altitude,
            speed=0,
        )

        self.logposition("")

    ############################################################################

    def isbomb(self):
        return True

    ############################################################################

    def position(self):
        hexcode = self.hexcode()
        if hexcode is None:
            hexcode = "-------"
        azimuth = self.azimuth()
        if azimuth is None:
            azimuth = "---"
        return "%-12s  %-3s" % (hexcode, azimuth)

    ############################################################################

    from apxo.bomb.attack import (
        _attackgroundunit,
        _secondaryattackgroundunit,
        blastzone,
    )
    from apxo.bomb.draw import _draw
    from apxo.bomb.move import _move, _continuemove

    ############################################################################
