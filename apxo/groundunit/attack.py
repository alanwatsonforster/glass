import apxo.geometry as apgeometry

#############################################################################


def _attackaircraft(self, target, result=None):

    if self.isusingbarragefire():

        if apgeometry.horizontalrange(self, target) > 1:
            raise RuntimeError("target is out of range of barrage fire.")
        if target.altitude() > self._barragefiremaximumaltitude():
            raise RuntimeError("target is above barrage fire.")
        self.logwhenwhat(
            "", "%s attacks %s with barrage fire." % (self.name(), target.name())
        )

    else:

        self.logwhenwhat(
            "", "%s attacks %s with aimed fire." % (self.name(), target.name())
        )
        self.logwhenwhat("", "range to target is %d." % apgeometry.range(self, target))
        self.logwhenwhat(
            "", "altitude to target is %d." % (target.altitude() - self.altitude())
        )

    target._takeattackdamage(self, result)

#############################################################################
