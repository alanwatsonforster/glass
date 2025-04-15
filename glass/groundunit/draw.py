################################################################################

import glass.draw

################################################################################


def _draw(self):
    glass.draw.drawgroundunit(
        *self.xy(),
        self._symbols,
        self._uppertext,
        self._lowertext,
        self._facing,
        self.color(),
        self.name(),
        self._stack,
        self._killed
    )


################################################################################
