################################################################################

import glass.azimuth
import glass.hex
import glass.hexcode

################################################################################


def _move(self, move, speedchange=0):
    self._newspeed = self._speed + speedchange
    self._continuemove(move)


def _continuemove(self, move):

    self.logstart("speed            is %.1f knots." % (self._speed))

    if self._speed > 0:
        self._movegameturn += 1
        movecadence = int(87 / self._speed + 0.5)
        self.logstart("move game turn   is %d/%d." % (self._movegameturn, movecadence))
        if self._movegameturn >= movecadence:
            self.logcomment("the ship must move forward one hex.")
    else:
        movecadence = None
        self.logcomment("the ship is stationary.")

    self._setlastposition()
    self.logpositionandmaneuver("start")

    self.logwhenwhat("", move)
    action = move.split("/")

    if action[0] == "H":
        if movecadence is not None and self._movegameturn < movecadence:
            raise RuntimeError("the ship cannot move forward one hex this game turn.")
        self._moveforward()
        self._movegameturn = 0
        self._maneuverfp += 1
        action.pop(0)
        if len(action) > 0 and action[0] in ["RR", "R60", "LL", "L60"]:
            sense = action[0][0]
            if self._maneuvertype == None:
                raise RuntimeError("attempt to turn without a declaration.")
            if self._maneuversense != sense:
                raise RuntimeError(
                    "attempt to turn against the sense of the declaration."
                )
            if self._maneuverfp < self._maneuverrequiredfp:
                raise RuntimeError(
                    "attempt to turn faster than the declared turn rate."
                )
            self._moveturn(sense, 60)
            self._maneuvertype = None
            self._maneuversense = None
            self._maneuverfp = 0
            action.pop(0)
    elif movecadence is not None and self._movegameturn >= movecadence:
        raise RuntimeError("the ship must move forward one hex this game turn.")

    if len(action) > 0 and action[0] in ["NTL", "NTR", "HTL", "HTR"]:
        self._maneuvertype = action[0][:2]
        if self._maneuvertype == "HT" and self._classification in [
            "mediummerchantship",
            "largemerchantship",
        ]:
            raise RuntimeError(
                "only warships and small merchant ships can declare HTs."
            )
        if self._maneuvertype == "HT" and self._speed < 10:
            raise RuntimeError("HTs require a speed of at least 10 knots.")
        elif self._maneuvertype == "NT" and self._speed < 5:
            raise RuntimeError("NTs require a speed of at least 5 knots.")
        self._maneuversense = action[0][2]
        self._maneuverfp = 0
        if self._maneuvertype == "NT":
            self._maneuverrequiredfp = 2
        else:
            self._maneuverrequiredfp = 1
        action.pop(0)

    if len(action) > 0 and action[0] != "":
        raise RuntimeError('invalid move "%s".' % move)

    self._extendpath()

    self.logpositionandmaneuver("end")

    self._speed = self._newspeed
    if self._speed > self._maxspeed:
        self.logcomment(
            "acceleration is limited by maximum speed of %.1f knots." % self._maxspeed
        )
        self._speed = self._maxspeed
    if self._speed < 0:
        self.logcomment("deceleration is limited by minimum speed of 0 knots.")
        self._speed = 0
    self.logend("speed will be %.1f knots." % self._speed)


################################################################################
