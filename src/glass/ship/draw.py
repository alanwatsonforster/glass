################################################################################

import glass.draw

################################################################################


def _draw(self):
    self._drawpath(
        self._color, annotate=False
    )
    glass.draw.drawship(
        *self.xy(),
        self._facing,
        self._large,
        self.name(),
        self.color(),
        self._stack,
        self._killed
    )


################################################################################
