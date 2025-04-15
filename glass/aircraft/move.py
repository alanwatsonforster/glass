################################################################################

import glass.flight

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
    glass.flight._move(
        self,
        flighttype,
        power,
        moves,
        speedbrakes=speedbrakes,
        flamedoutengines=flamedoutengines,
        lowspeedliftdeviceselected=lowspeedliftdeviceselected,
    )


def _continuemove(self, moves=""):
    glass.flight._continuemove(self, moves)


################################################################################
