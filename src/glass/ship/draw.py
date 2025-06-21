################################################################################

import glass.draw

################################################################################


def _draw(self):
    self._drawpath(
        self._color, annotate=False
    )
    if self._classification.startswith("large"):
        size = "large"
    elif self._classification.startswith("medium"):
        size = "medium"
    else:
        size = "small"
    glass.draw.drawship(
        *self.xy(),
        self._facing,
        size,
        self.name(),
        self.color(),
        self._stack,
        self._killed
    )


################################################################################
