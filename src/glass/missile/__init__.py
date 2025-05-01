import math

import glass.altitude
import glass.azimuth
import glass.element
import glass.flight
import glass.gameturn
import glass.geometry
import glass.hexcode
import glass.log
import glass.map
import glass.missiledata
import glass.speed
import glass.variants

##############################################################################


def aslist():
    elementlist = glass.element.aslist()
    missilelist = filter(lambda self: self.ismissile(), elementlist)
    return list(missilelist)


#############################################################################


class Missile(glass.element.Element):

    def __init__(self, name, missiletype, launcher, target, color="white"):

        self._name = ""

        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating missile %s." % name)

            self._type = missiletype
            self.logwhenwhat("", "type          is %s." % missiletype)

            super().__init__(
                name,
                x=launcher.x(),
                y=launcher.y(),
                facing=launcher.facing(),
                altitude=launcher.altitude(),
                speed=0,
                color=color,
            )

            self.logwhenwhat("", "position      is %s." % self.position())

            self._target = target
            self.logwhenwhat("", "target        is %s." % self._target.name())

            self._missiletype = missiletype

            self._flighttype = "MS"
            self._finishedmoving = True

            self._launchgameturn = glass.gameturn.gameturn()

            self._newspeed = None
            if glass.variants.withvariant("use house rules"):
                self._setspeed(self.basespeed() + launcher.newspeed())
            else:
                self._setspeed(self.basespeed() + launcher.speed())
            maxspeed = glass.speed.missilemaxspeed(self.altitudeband())
            if self.speed() > maxspeed:
                self.logcomment("reducing start speed to maximum for altitude band.")
                self._setspeed(maxspeed)
            self.logwhenwhat("", "start speed   is %.1f." % self._speed)
            self.logwhenwhat("", "turn rate     is %s/%d." % self.turnrate())

        except RuntimeError as e:
            glass.log.logexception(e)
        self.logbreak()

    #############################################################################

    def ismissile(self):
        return True

    #############################################################################

    def _properties(self):
        return []

    #############################################################################

    def _startgameturn(self):
        self._setspeed(self._newspeed)
        self._newspeed = None
        self._finishedmoving = False

    def _endgameturn(self):
        if not self.removed() and not self._finishedmoving:
            pass
            # raise Runtimeselfrror("missile %s has not finished its move." % self._name)

    #############################################################################

    def basespeed(self):
        return glass.missiledata.basespeed(self._missiletype)

    def turnrate(self):
        return glass.missiledata.turnrate(self._missiletype)

    #############################################################################

    def _checktargettracking(self):

        slopenumerator, slopedenominator = glass.flight._endflightslope(self)

        horizontalrange = glass.geometry.horizontalrange(self, self._target)
        self.logcomment("horizontal range is %d." % horizontalrange)

        self.logcomment("missile altitude is %d." % self.altitude())
        self.logcomment("target altitude is %d." % self._target.altitude())
        altitudedifference = self._target.altitude() - self.altitude()
        self.logcomment("altitude difference is %+d." % altitudedifference)

        def checkmixedonly(minf, maxf):
            minaltitudedifference = int(math.ceil(minf * horizontalrange))
            maxaltitudedifference = int(math.floor(maxf * horizontalrange))
            self.logcomment(
                "the allowed target altitude difference range is %+d to %+d."
                % (minaltitudedifference, maxaltitudedifference)
            )
            minaltitude = max(0, self.altitude() + minaltitudedifference)
            maxaltitude = min(100, self.altitude() + maxaltitudedifference)
            self.logcomment(
                "the allowed target altitude range is %d to %d."
                % (minaltitude, maxaltitude)
            )
            if (
                altitudedifference < minaltitudedifference
                or altitudedifference > maxaltitudedifference
            ):
                self.logcomment("the target is not within the seeker vertical limits.")
            else:
                self.logcomment("the target is within the seeker vertical limits.")

        def checkpixedandpure(mixedf, puref):

            mixedaltitudedifference = int(math.floor(mixedf * horizontalrange))
            purealtitudedifference = int(math.floor(puref * horizontalrange))
            if mixedf > 0:
                self.logcomment(
                    "the allowed target altitude difference for the mixed arc is %+d or more."
                    % (mixedaltitudedifference)
                )
                self.logcomment(
                    "the allowed target altitude difference for the pure arc is %+d or more."
                    % (purealtitudedifference)
                )
                mixedaltitude = self.altitude() + mixedaltitudedifference
                npurealtitude = self.altitude() + purealtitudedifference
                if mixedaltitude <= 100:
                    self.logcomment(
                        "the allowed target altitude range for the mixed arc is at or above %d."
                        % (mixedaltitude)
                    )
                else:
                    self.logcomment(
                        "there is no valid allowed target altitude range for the mixed arc."
                    )
                if purealtitude <= 100:
                    self.logcomment(
                        "the allowed target altitude range for the pure arc is at or above %d."
                        % (purealtitude)
                    )
                else:
                    self.logcomment(
                        "there is no valid allowed target altitude range for the pure arc."
                    )
                if altitudedifference >= purealtitudedifference:
                    self.logcomment(
                        "the target is within the seeker vertical limits for the pure arc."
                    )
                elif altitudedifference >= mixedaltitudedifference:
                    self.logcomment(
                        "the target is within the seeker vertical limits for the mixed arc."
                    )
                else:
                    self.logcomment(
                        "the target is not within the seeker vertical limits."
                    )
            else:
                self.logcomment(
                    "the allowed target altitude difference for the mixed arc is %+d or less."
                    % (mixedaltitudedifference)
                )
                self.logcomment(
                    "the allowed target altitude difference for the pure arc is %+d or less."
                    % (purealtitudedifference)
                )
                mixedaltitude = self.altitude() + mixedaltitudedifference
                purealtitude = self.altitude() + purealtitudedifference
                if mixedaltitude >= 0:
                    self.logcomment(
                        "the allowed target altitude range for the mixed arc is at or below %d."
                        % (mixedaltitude)
                    )
                else:
                    self.logcomment(
                        "there is no valid allowed target altitude range for the mixed arc."
                    )
                if purealtitude >= 0:
                    self.logcomment(
                        "the allowed target altitude range for the pure arc is at or below %d."
                        % (purealtitude)
                    )
                else:
                    self.logcomment(
                        "there is no valid allowed target altitude range for the pure arc."
                    )
                if altitudedifference <= purealtitudedifference:
                    self.logcomment(
                        "the target is within the seeker vertical limits for the pure arc."
                    )
                elif altitudedifference <= mixedaltitudedifference:
                    self.logcomment(
                        "the target is within the seeker vertical limits for the mixed arc."
                    )
                else:
                    self.logcomment(
                        "the target is not within the seeker vertical limits."
                    )

        def checkpureonly(puref):

            purealtitudedifference = int(math.floor(puref * horizontalrange))
            if puref > 0:
                self.logcomment(
                    "the allowed target altitude difference for the pure arc is %+d or more."
                    % (purealtitudedifference)
                )
                purealtitude = self.altitude() + purealtitudedifference
                if purealtitude <= 100:
                    self.logcomment(
                        "the allowed target altitude range for the pure arc is at or above %d."
                        % (purealtitude)
                    )
                else:
                    self.logcomment(
                        "there is no valid allowed target altitude range for the pure arc."
                    )
                if altitudedifference >= purealtitudedifference:
                    self.logcomment(
                        "the target is within the seeker vertical limits for the pure arc."
                    )
                else:
                    self.logcomment(
                        "the target is not within the seeker vertical limits."
                    )
            else:
                self.logcomment(
                    "the allowed target altitude difference for the pure arc is %+d or less."
                    % (purealtitudedifference)
                )
                purealtitude = self.altitude() + purealtitudedifference
                if purealtitude >= 0:
                    self.logcomment(
                        "the allowed target altitude range for the pure arc is at or below %d."
                        % (purealtitude)
                    )
                else:
                    self.logcomment(
                        "there is no valid allowed target altitude range for the pure arc."
                    )
                if altitudedifference <= purealtitudedifference:
                    self.logcomment(
                        "the target is within the seeker vertical limits for the pure arc."
                    )
                else:
                    self.logcomment(
                        "the target is not within the seeker vertical limits."
                    )

        if slopedenominator == 0 and slopenumerator < 0:
            checkpureonly(-3.0)
        if slopenumerator < -3 * slopedenominator:
            checkpixedandpure(-2.0, -7.0)
        elif slopenumerator < -1 * slopedenominator:
            checkmixedonly(-7.0, -0.5)
        elif slopenumerator < 0:
            checkmixedonly(-2.0, +0.5)
        elif slopenumerator == 0:
            checkmixedonly(-1.0, +1.0)
        elif slopenumerator <= +1 * slopedenominator:
            checkmixedonly(-0.5, +2.0)
        elif abs(slopenumerator) <= 3 * slopedenominator:
            checkmixedonly(+0.5, +7.0)
        else:
            checkpureonly(+3.0)

    ############################################################################

    from glass.missile.attack import _attackaircraft
    from glass.missile.draw import _draw
    from glass.missile.move import _move, _continuemove

    ############################################################################
