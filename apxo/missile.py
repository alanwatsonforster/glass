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

    def move(self, speed, actions, note=False):

        self._drawontop()
        aplog.clearerror()
        try:

            apgameturn.checkingameturn()
            apmissileflight.move(self, speed, actions, note=note)

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def continuemove(self, actions, note=False):

        self._drawontop()
        aplog.clearerror()
        try:

            apgameturn.checkingameturn()
            apmissileflight.continuemove(self, actions, note=note)

            # self._logbreak()
            # self._logline()
            # if actions != "":
            #  for action in actions.split(","):
            #    if not self._removed:
            #      apmissileflight._doaction(self, action)
            # self._logline()

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def _draw(self):
        self._drawpath(self._color, self.zorder(), annotate=False)
        apdraw.drawmissile(
            self.x(),
            self.y(),
            self.facing(),
            self._color,
            self._name,
            self.altitude(),
            self.speed(),
            self.zorder(),
        )

    ########################################

    def maneuver(self):
        """Return a string describing the current maneuver of the missile."""
        if self._maneuvertype != None:
            return "%s%s" % (self._maneuvertype, self._maneuversense)
        else:
            return ""

    #############################################################################
