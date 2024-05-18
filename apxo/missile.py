import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.draw as apdraw
import apxo.element as apelement
import apxo.gameturn as apgameturn
import apxo.hexcode as aphexcode
import apxo.log as aplog
import apxo.map as apmap
import apxo.missileflight as apmissileflight

##############################################################################


class missile(apelement.element):

    def __init__(self, name, missiletype, launcher, target, color="white"):

        aplog.clearerror()
        try:

            self._logbreak()
            self._logline()

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

            self._maneuvertype = None
            self._maneuversense = None

            self._logline()

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def ismissile(self):
        return True

    #############################################################################

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        pass

    #############################################################################

    def _move(self, speed, actions, note=False):
        apmissileflight.move(self, speed, actions, note=note)

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
