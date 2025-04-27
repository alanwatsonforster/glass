################################################################################

import glass.draw
import glass.gameturn

################################################################################


def _draw(self):
    self._drawpath(
        self._color, annotate=glass.gameturn.gameturn() > self._launchgameturn + 1
    )
    glass.draw.drawmissile(
        self.x(),
        self.y(),
        self.facing(),
        self.altitude(),
        self.speed(),
        self._name,
        self._color,
        annotate=self._startedmoving,
    )


################################################################################
