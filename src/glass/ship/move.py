################################################################################

import glass.azimuth
import glass.gameturn
import glass.hex
import glass.hexcode

################################################################################

_maxspeeddecrease = {
    "smallwarship": 3 / 2,
    "mediumwarship": 3 / 2,
    "largewarship": 1,
    "smallmerchantship": 1 / 2,
    "mediummerchantship": 1 / 2,
    "largemerchantship": 1 / 2,
}

_maxspeedincrease = {
    "smallwarship": 1,
    "mediumwarship": 2 / 3,
    "largewarship": 1 / 2,
    "smallmerchantship": 1 / 2,
    "mediummerchantship": 1 / 2,
    "largemerchantship": 1 / 2,
}


def _move(self, move, speedchange=0):

    self.logstart("speed            is %.1f knots." % (self._speed))
    speed = self._speed
    if speedchange < 0:
        maxspeeddecrease = _maxspeeddecrease[self._classification]
        if speedchange < -maxspeeddecrease:
            raise RuntimeError(
                "the speed decrease cannot be more than %.2f knots." % maxspeeddecrease
            )
    elif speedchange > 0:
        maxspeedincrease = _maxspeedincrease[self._classification]
        if speed >= self._maxspeed / 2:
            maxspeedincrease /= 2
        if speedchange > maxspeedincrease:
            raise RuntimeError(
                "the speed increase cannot be more than %.2f knots." % maxspeedincrease
            )
    self._newspeed = speed + speedchange
    self._continuemove(move)


def _continuemove(self, move):

    if self._speed > 0:
        self._movegameturn += 1
        movecadence = int(87 / self._speed + 0.5)
        self.logstart("move game turn   is %d/%d." % (self._movegameturn, movecadence))
        if self._movegameturn >= movecadence:
            self.logcomment("the ship must move forward one hex.")
    else:
        movecadence = None
        self.logcomment("the ship is stationary.")

    if self._maneuvertype == "HT":
        self._HTrecoverygameturn = glass.gameturn.gameturn() + 1
        
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
    
    if len(action) > 0 and action[0] == "AT":
        self._maneuvertype = None
        self._maneuversense = None
        self._maneuverfp = 0
        action.pop(0)
    elif len(action) > 0 and action[0] in ["NTL", "NTR", "HTL", "HTR"]:
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
        if self._maneuvertype == "HT":
            self._HTrecoverygameturn = glass.gameturn.gameturn() + 1
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

    if self._HTrecoverygameturn == glass.gameturn.gameturn():
        self.logcomment("recovered from HT.")

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
