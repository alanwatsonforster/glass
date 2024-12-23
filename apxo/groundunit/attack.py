import apxo.geometry as apgeometry

#############################################################################


def _attackaircraft(self, target, result=None):

    if self.isusingbarragefire():

        if apgeometry.horizontalrange(self, target) > 1:
            raise RuntimeError("target is out of range of the barrage fire.")
        if target.altitude() > self._barragefiremaximumaltitude():
            raise RuntimeError("target is above the barrage fire.")
        self.logwhenwhat(
            "", "%s attacks %s with barrage fire." % (self.name(), target.name())
        )

    elif self.isusingplottedfire():

        if apgeometry.horizontalrange(self._plottedfire, target) > 1:
            raise RuntimeError("target is out of range of the plotted fire.")
        if target.altitude() < self._plottedfire.altitude() - 2:
            raise RuntimeError("target is below the plotted fire.")
        if target.altitude() > self._plottedfire.altitude() + 2:
            raise RuntimeError("target is above the plotted fire.")
        self.logwhenwhat(
            "", "%s attacks %s with plotted fire." % (self.name(), target.name())
        )

    else:

        self.logwhenwhat(
            "", "%s attacks %s with aimed fire." % (self.name(), target.name())
        )
        if self._tracking is not target:
            raise RuntimeError("%s is not tracking %s." % (self.name(), target.name()))
        self.logwhenwhat("", "range to target is %d." % apgeometry.range(self, target))
        self.logwhenwhat(
            "", "altitude to target is %d." % (target.altitude() - self.altitude())
        )

    target._takeattackdamage(self, result)


#############################################################################
