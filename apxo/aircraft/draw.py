################################################################################

import apxo.draw as apdraw

################################################################################


def _draw(self):
    if self._startedmoving:
        self._drawpath(self._color, killed=self.killed(), annotate=not self.killed())
    if self._finishedmoving:
        speed = self.newspeed()
    elif self._startedmoving:
        speed = None
    else:
        speed = self.speed()
    apdraw.drawaircraft(
        self.x(),
        self.y(),
        self.facing(),
        self._color,
        self.name(),
        self.altitude(),
        speed,
        self._flighttype,
        killed=self.killed(),
    )


################################################################################
