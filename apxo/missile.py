import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.draw as apdraw
import apxo.element as apelement
import apxo.flight as apflight
import apxo.gameturn as apgameturn
import apxo.geometry as apgeometry
import apxo.hexcode as aphexcode
import apxo.log as aplog
import apxo.map as apmap
import apxo.missiledata as apmissiledata
import apxo.speed as apspeed

##############################################################################


def aslist():
    elementlist = apelement.aslist()
    missilelist = filter(lambda self: self.ismissile(), elementlist)
    return list(missilelist)


#############################################################################


class missile(apelement.element):

    def __init__(self, name, missiletype, launcher, target, color="white"):

        self._name = name
        self._logbreak()
        self._logwhenwhat("", "creating missile %s." % name)

        aplog.clearerror()
        try:

            self._type = missiletype
            self._logwhenwhat("", "type          is %s." % missiletype)

            super().__init__(
                name,
                x=launcher.x(),
                y=launcher.y(),
                facing=launcher.facing(),
                altitude=launcher.altitude(),
                speed=0,
                color=color,
            )

            self._logwhenwhat("", "position      is %s." % self.position())

            self._target = target
            self._logwhenwhat("", "target        is %s." % self._target.name())

            self._missiletype = missiletype

            self._flighttype = "MS"
            self._startedmoving = False
            self._finishedmoving = True
            self._maneuvertype = None
            self._maneuversense = None
            self._maneuverfp = 0
            self._maneuverrequiredfp = 0
            self._maneuverfacingchange = None
            self._manueversupersonic = False

            self._launchgameturn = apgameturn.gameturn()

            self._setspeed(self.basespeed() + launcher.newspeed())
            maxspeed = apspeed.missilemaxspeed(self.altitudeband())
            if self.speed() > maxspeed:
                self._logcomment("reducing start speed to maximum for altitude band.")
                self._setspeed(maxspeed)
            self._logwhenwhat("", "start speed   is %.1f." % self._speed)
            self._logwhenwhat("", "turn rate     is %s/%d." % self.turnrate())

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def ismissile(self):
        return True

    #############################################################################

    def _startgameturn(self):
        self._startedmoving = False
        self._finishedmoving = False

    def _endgameturn(self):
        if not self.removed() and not self._finishedmoving:
            pass
            # raise Runtimeselfrror("missile %s has not finished its move." % self._name)

    #############################################################################

    def _move(self, moves):
        apflight._move(self, "MS", None, moves)

    def _continuemove(self, moves, note=None):
        apflight._continuemove(self, moves)

    #############################################################################

    def _draw(self):
        self._drawpath(self._color, annotate=False)
        apdraw.drawmissile(
            self.x(),
            self.y(),
            self.facing(),
            self._color,
            self._name,
            self.altitude(),
            self.speed(),
        )

    ########################################

    def maneuver(self):
        """Return a string describing the current maneuver of the aircraft."""
        if self._maneuverfacingchange == 60 or self._maneuverfacingchange == 90:
            return "%s%s %d/%d %d" % (
                self._maneuvertype,
                self._maneuversense,
                self._maneuverfp,
                self._maneuverrequiredfp,
                self._maneuverfacingchange,
            )
        elif self._maneuvertype != None:
            return "%s%s %d/%d" % (
                self._maneuvertype,
                self._maneuversense,
                self._maneuverfp,
                self._maneuverrequiredfp,
            )
        else:
            return ""

    #############################################################################

    def basespeed(self):
        return apmissiledata.basespeed(self._missiletype)

    def turnrate(self):
        return apmissiledata.turnrate(self._missiletype)

    #############################################################################

    def _checktargettracking(self):

        slopenumerator, slopedenominator = apflight._slope(self)
        self._logcomment("flight slope is %+d/%d." % (slopenumerator, slopedenominator))

        horizontalrange = apgeometry.horizontalrange(self, self._target)
        self._logcomment("horizontal range is %d." % horizontalrange)

        self._logcomment("missile altitude is %d." % self.altitude())
        self._logcomment("target altitude is %d." % self._target.altitude())
        altitudedifference = self._target.altitude() - self.altitude()
        self._logcomment("altitude difference is %+d." % altitudedifference)

        def checknormallimit(minf, maxf):
            minaltitudedifference = int(minf * horizontalrange)
            maxaltitudedifference = int(maxf * horizontalrange)
            self._logcomment(
                "the allowed target altitude difference range is %+d to %+d."
                % (minaltitudedifference, maxaltitudedifference)
            )
            minaltitude = max(0, self.altitude() + minaltitudedifference)
            maxaltitude = min(100, self.altitude() + maxaltitudedifference)
            self._logcomment(
                "the allowed target altitude range is %d to %d."
                % (minaltitude, maxaltitude)
            )
            if (
                altitudedifference < minaltitudedifference
                or altitudedifference > maxaltitudedifference
            ):
                self._logcomment("the target is not within the seeker vertical limits.")
            else:
                self._logcomment("the target is within the seeker vertical limits.")

        if slopenumerator < -3 * slopedenominator:
            pass
        elif slopenumerator < -1 * slopedenominator:
            checknormallimit(-7.0, -0.5)
        elif slopenumerator < 0:
            checknormallimit(-2.0, +0.5)
        elif slopenumerator == 0:
            checknormallimit(-1.0, +1.0)
        elif slopenumerator <= +1 * slopedenominator:
            checknormallimit(-0.5, +2.0)
        elif abs(slopenumerator) <= 3 * slopedenominator:
            checknormallimit(+0.5, +7.0)
        else:
            pass
