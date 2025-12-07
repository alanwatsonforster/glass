################################################################################

import glass.draw

################################################################################


def _draw(self, allsighted=False, allidentified=False, **kwargs):

    glass.draw.drawgroundunit(
        *self.xy(),
        self._facing,
        self.sighted() or allsighted,
        self.identified() or allidentified,
        self._symbols,
        self._text,
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
