################################################################################

import glass.draw

################################################################################


def _draw(self, **kwargs):

    zorder = self.altitude() + 1
    if self._type == "dot":

        glass.draw.drawdot(*self.xy(), size=0.1, fillcolor=self.color(), zorder=zorder)

    elif self._type == "circle":

        glass.draw.drawcircle(
            *self.xy(), size=0.65, linecolor=self.color(), linewidth="thick"
        )

    elif self._type == "square":

        glass.draw.drawsquare(
            *self.xy(),
            size=0.65,
            linecolor=self.color(),
            linewidth="thick",
            facing=self.facing(),
            zorder=zorder
        )

    glass.draw.drawtext(
        *self.xy(), self.name(), self.facing(), textcolor=self.color(), zorder=zorder
    )


################################################################################
