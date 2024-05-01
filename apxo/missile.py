import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.draw as apdraw
import apxo.hexcode as aphexcode
import apxo.log as aplog
import apxo.map as apmap
import apxo.missileflight as apmissileflight

from apxo.element import element

_missilelist = []


def _startsetup():
    global _missilelist
    _missilelist = []


def _startturn():
    for M in _missilelist:
        M._restore()


def _endturn():
    for M in _missilelist:
        M._save()


##############################################################################


def aslist(withremoved=False):
    missilelist = _missilelist
    if not withremoved:
        missilelist = filter(lambda x: not x._removed, missilelist)
    return list(missilelist)


##############################################################################


class missile(element):

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

            self._zorder = launcher._zorder

            global _missilelist
            _missilelist.append(self)

            self._logline()

        except RuntimeError as e:
            aplog.logexception(e)

    ##############################################################################

    # Turn management

    def _restore(self):
        """
        Restore the missile properties at the start of the turn.
        """

        (
            x,
            y,
            facing,
            altitude,
            self._maneuvertype,
            self._maneuversense,
            self._removed,
        ) = self._saved
        self._setposition(x=x, y=y, facing=facing, altitude=altitude)

    def _save(self):
        """
        Save the missile properties at the end of the turn.
        """

        self._saved = (
            self.x(),
            self.y(),
            self.facing(),
            self.altitude(),
            self._maneuvertype,
            self._maneuversense,
            self._removed,
        )

    #############################################################################

    def move(self, speed, actions, note=False):

        aplog.clearerror()
        try:

            apmissileflight.move(self, speed, actions, note=note)

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def continuemove(self, actions, note=False):

        aplog.clearerror()
        try:

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
        self._drawpath(self._color, self._zorder, annotate=False)
        apdraw.drawmissile(
            self.x(),
            self.y(),
            self.facing(),
            self._color,
            self._name,
            self.altitude(),
            self.speed(),
            self._zorder,
        )

    ########################################

    def _logbreak(self):
        aplog.logbreak()

    def _log(self, s):
        aplog.log("%-4s : %s" % (self.name(), s))

    def _logline(self):
        aplog.log("%-4s : %s :" % ("----", "-----"))

    def _log1(self, s, t):
        self._log("%-5s : %s" % (s, t))

    def _log2(self, s, t):
        self._log("%-5s : %-32s : %s" % (s, "", t))

    def _logposition(self, s):
        self._log1(s, self.position())

    def _logpositionandmaneuver(self, s):
        self._log1(s, "%s  %s" % (self.position(), self.maneuver()))

    def _logaction(self, s, t):
        self._log1(s, t)

    def _logevent(self, s):
        self._log2("", s)

    def _logstart(self, s):
        self._log1("start", s)

    def _logend(self, s):
        self._log1("end", s)

    def _lognote(self, note):
        aplog.lognote(self, note)

    #############################################################################

    def checkforterraincollision(self):
        """
        Check if the missile has collided with terrain.
        """

        altitudeofterrain = apaltitude.terrainaltitude(*self.xy())
        if self.altitude() <= altitudeofterrain:
            self._setaltitude(altitudeofterrain)
            self._altitudecarry = 0
            self._logaction(
                "",
                "missile has collided with terrain at altitude %d." % altitudeofterrain,
            )
            self._removed = True

    def checkforleavingmap(self):
        """
        Check if the missile has left the map.
        """

        if not apmap.isonmap(*self.xy()):
            self._logaction("", "missile has left the map.")
            self._removed = True

    ################################################################################
