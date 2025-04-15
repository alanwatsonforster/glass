################################################################################

import apxo.draw

################################################################################


def _draw(self):

    zorder = self.altitude() + 1
    if self._type == "dot":

        apxo.draw.drawdot(*self.xy(), size=0.1, fillcolor=self.color(), zorder=zorder)

    elif self._type == "circle":

        apxo.draw.drawcircle(*self.xy(), size=0.65, linecolor=self.color(), linewidth=2)
        if self.name() is not None:
            apxo.draw.drawtext(
                *self.xy(),
                self.facing(),
                self.name(),
                color=self.color(),
                zorder=zorder
            )

    elif self._type == "square":

        apxo.draw.drawsquare(
            *self.xy(),
            size=0.65,
            linecolor=self.color(),
            linewidth=2,
            facing=self.facing(),
            zorder=zorder
        )
        if self.name() is not None:
            apxo.draw.drawtext(*self.xy(), self.facing(), self.name(), color=self.color())


################################################################################
