################################################################################

import apxo.flight as apflight

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
    apflight._move(
        self,
        flighttype,
        power,
        moves,
        speedbrakes=speedbrakes,
        flamedoutengines=flamedoutengines,
        lowspeedliftdeviceselected=lowspeedliftdeviceselected,
    )


def _continuemove(self, moves=""):
    apflight._continuemove(self, moves)


################################################################################
