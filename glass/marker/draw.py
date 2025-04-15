################################################################################

import glass.draw

################################################################################


def _draw(self):

    zorder = self.altitude() + 1
    if self._type == "dot":

        glass.draw.drawdot(*self.xy(), size=0.1, fillcolor=self.color(), zorder=zorder)

    elif self._type == "circle":

        glass.draw.drawcircle(*self.xy(), size=0.65, linecolor=self.color(), linewidth=2)
        if self.name() is not None:
            glass.draw.drawtext(
                *self.xy(),
                self.facing(),
                self.name(),
                color=self.color(),
                zorder=zorder
            )

    elif self._type == "square":

        glass.draw.drawsquare(
            *self.xy(),
            size=0.65,
            linecolor=self.color(),
            linewidth=2,
            facing=self.facing(),
            zorder=zorder
        )
        if self.name() is not None:
            glass.draw.drawtext(*self.xy(), self.facing(), self.name(), color=self.color())


################################################################################
