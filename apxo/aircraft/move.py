################################################################################

import apxo.flight

################################################################################


def _move(
    self,
    flighttype,
    power,
    moves="",
    speedbrakes=None,
    flamedoutengines=0,
    lowspeedliftdeviceselected=None,
    geometry=None,
):
    self._setgeometry(geometry)
    apxo.flight._move(
        self,
        flighttype,
        power,
        moves,
        speedbrakes=speedbrakes,
        flamedoutengines=flamedoutengines,
        lowspeedliftdeviceselected=lowspeedliftdeviceselected,
    )


def _continuemove(self, moves=""):
    apxo.flight._continuemove(self, moves)


################################################################################
