################################################################################

import apxo.draw as apdraw
import apxo.gameturn as apgameturn

################################################################################


def _draw(self):
    self._drawpath(
        self._color, annotate=apgameturn.gameturn() > self._launchgameturn + 1
    )
    apdraw.drawmissile(
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
