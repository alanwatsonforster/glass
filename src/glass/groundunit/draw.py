################################################################################

import glass.draw

################################################################################


def _draw(self):

    if not self.sighted():
        symbols = []
        uppertext = ""
        lowertext = ""
    elif not self.identified():
        if "infantry" in self._symbols:
            symbols = ["infantry"]
        elif "radar" in self._symbols:
            symbols = ["radar"]
        elif "armor" in self._symbols:
            symbols = ["armor"]
        elif "truck" in self._symbols:
            symbols = ["truck"]
        elif "air-defense" in self._symbols:
            symbols = ["air-defense"]
        elif "artillery" in self._symbols:
            symbols = ["artillery"]
        else:
            symbols = []
        lowertext = "%d" % self._sightingrange
        uppertext = ""
    else:
        symbols = self._symbols
        uppertext = self._uppertext
        if self._defensestrength is not None:
            lowertext = "%s-%d" % (self._defensestrength, self._sightingrange)
        else:
            lowertext = "%d" % self._sightingrange

    glass.draw.drawgroundunit(
        *self.xy(),
        self._facing,
        symbols,
        uppertext,
        lowertext,
        self._protectionclass,
        self.name(),
        self.damage(),
        self.color(),
        self._stack,
    )


################################################################################
