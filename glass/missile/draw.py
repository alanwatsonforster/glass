################################################################################

import apxo.draw
import apxo.gameturn

################################################################################


def _draw(self):
    self._drawpath(
        self._color, annotate=apxo.gameturn.gameturn() > self._launchgameturn + 1
    )
    apxo.draw.drawmissile(
        self.x(),
        self.y(),
        self.facing(),
        self._color,
        self._name,
        self.altitude(),
        self.speed(),
        annotate=self._startedmoving,
    )


################################################################################
