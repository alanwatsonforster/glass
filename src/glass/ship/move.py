################################################################################

import glass.azimuth
import glass.hex
import glass.hexcode

################################################################################


def _move(self, move):
    self._continuemove(move)


def _continuemove(self, move):

    self.logstart("speed            is %.f knots." % (self._speed))

    self._movegameturn += 1
    movecadence = int(87 / self._speed + 0.5)
    self.logstart("move game turn   is %d/%d." % (self._movegameturn, movecadence))
    if self._movegameturn >= movecadence:
        self.logcomment("the ship must move forward one hex.")

    self._setlastposition()
    self.logpositionandmaneuver("start")

    self.logwhenwhat("", move)
    action = move.split("/")
    
    if action[0] == "H":
        if self._movegameturn < movecadence:
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
    elif self._movegameturn >= movecadence:
        raise RuntimeError("the ship must move forward one hex this game turn.")

    if len(action) > 0 and action[0] in ["NTL", "NTR", "HTL", "HTR"]:
        self._maneuvertype = action[0][:2]
        if self._maneuvertype == "HT" and self._classification in [
            "mediummerchantship",
            "largemerchantship",
        ]:
            raise RuntimeError("only warships and small merchant ships can declare HTs.")
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


################################################################################
