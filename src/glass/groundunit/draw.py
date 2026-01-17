################################################################################

import glass.draw

################################################################################


def _draw(self, allsighted=False, allidentified=False, **kwargs):

    if self.istransported():
        return

    if self.isidentified() and self.istowing():
        name = self.name() + "+" + self.transporting().name()
    else:
        name = self.name()

    glass.draw.drawgroundunit(
        *self.xy(),
        self._facing,
        self.issighted() or allsighted,
        self.isidentified() or allidentified,
        self._symbols,
        self._text,
        self._sightingrange,
        self._defensestrength,
        self._protectionclass,
        name,
        self.damage(),
        self.color(),
        self._counter,
        self._stack,
    )


################################################################################
