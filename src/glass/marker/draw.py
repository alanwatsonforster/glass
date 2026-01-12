################################################################################

import glass.draw

################################################################################


def _draw(self, **kwargs):

    zorder = self.altitude() + 1
    if self._type == "dot":

        glass.draw.drawdot(*self.xy(), size=0.1, fillcolor=self.color(), zorder=zorder)
        textdy = 0.15

    elif self._type == "circle":

        glass.draw.drawcircle(
            *self.xy(), size=0.65, linecolor=self.color(), linewidth="thick"
        )
        textdy = 0

    elif self._type == "square":

        glass.draw.drawsquare(
            *self.xy(),
            size=0.65,
            linecolor=self.color(),
            linewidth="thick",
            zorder=zorder
        )
        textdy = 0

    if self.name() is not None:
        if self.facing() is None:
            facing = 90
        else:
            facing = self.facing()
        glass.draw.drawtext(
            *self.xy(),
            self.name(),
            facing,
            dy=textdy,
            textcolor=self.color(),
            zorder=zorder
        )


################################################################################
