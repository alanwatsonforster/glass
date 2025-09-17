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
        elif "armor" in self._symbols:
            symbols = ["armor"]
        elif "truck" in self._symbols:
            symbols = ["truck"]
        elif "radar" in self._symbols:
            symbols = ["radar"]
        elif "airdefense" in self._symbols:
            symbols = ["airdefense"]
        elif "artillery" in self._symbols:
            symbols = ["artillery"]
        else:
            symbols = []
        uppertext = "%d" % self._sightingrange
        lowertext = ""
    else:
        symbols = self._symbols
        uppertext = self._uppertext
        lowertext = self._lowertext

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
