import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.draw as apdraw
import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.hexcode as aphexcode
import apxo.log as aplog
import apxo.map as apmap
import apxo.missiledata as apmissiledata
import apxo.missileflight as apmissileflight

##############################################################################

def aslist():
    elementlist = apelement.aslist()
    missilelist = filter(lambda E: E.ismissile(), elementlist)
    return list(missilelist)


#############################################################################

class missile(apelement.element):

    def __init__(self, name, missiletype, launcher, target, color="white"):

        self._logbreak()
        aplog.clearerror()
        try:

            self._name = name
            self._logaction("", "creating missile %s." % name)

            self._type = missiletype
            self._logaction("", "type          is %s." % missiletype)

            super().__init__(
                name,
                x=launcher.x(),
                y=launcher.y(),
                facing=launcher.facing(),
                altitude=launcher.altitude(),
                speed=0,
                color=color,
            )

            self._logaction("", "position      is %s." % self.position())

            self._target = target
            self._logaction("", "target        is %s." % self._target.name())

            self._missiletype = missiletype

            self._startedmoving = False
            self._finishedmoving = True
            self._maneuvertype = None
            self._maneuversense = None
            self._launchgameturn = apgameturn.gameturn()

            self._setspeed(self._basespeed() + launcher.newspeed())
            if self.speed() > apmissileflight.maxspeed(self.altitudeband()):
                self._logevent("reducing start speed to maximum for altitude band.")
                self._setspeed(apmissileflight.maxspeed(self.altitudeband()))
            self._logaction("", "start speed   is %.1f." % self._speed)

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
            # raise RuntimeError("missile %s has not finished its move." % self._name)

    #############################################################################

    def _move(self, actions, note=False):
        apmissileflight.move(self, actions, note=note)

    #############################################################################

    def _continuemove(self, actions, note=False):
        apmissileflight.continuemove(self, actions, note=note)

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
        """Return a string describing the current maneuver of the missile."""
        if self._maneuvertype != None:
            return "%s%s" % (self._maneuvertype, self._maneuversense)
        else:
            return ""

    #############################################################################

    def _basespeed(self):
        return apmissiledata.basespeed(self._missiletype)
