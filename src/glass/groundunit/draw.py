################################################################################

import glass.draw

################################################################################


def _draw(self):
    glass.draw.drawgroundunit(
        *self.xy(),
        self._facing,
        self._symbols,
        self._uppertext,
        self._lowertext,
        self.name(),
        self.color(),
        self._stack,
        self._killed
    )


################################################################################
