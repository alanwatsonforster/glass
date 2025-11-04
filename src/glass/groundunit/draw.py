################################################################################

import glass.draw

################################################################################


def _draw(self):

    glass.draw.drawgroundunit(
        *self.xy(),
        self._facing,
        self.sighted(),
        self.identified(),
        self._symbols,
        self._uppertext,
        self._lowertext,
        self._sightingrange,
        self._defensestrength,
        self._protectionclass,
        self.name(),
        self.damage(),
        self.color(),
        self._counter,
        self._stack,
    )


################################################################################
