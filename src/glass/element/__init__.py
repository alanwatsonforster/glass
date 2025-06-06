import copy
import re

import glass.altitude
import glass.azimuth
import glass.path
import glass.hex
import glass.hexcode
import glass.gameturn
import glass.log
import glass.map
import glass.speed

# Elements are anything that can be placed on a map: aircraft, missiles,
# ground units, markers, and bombs. This class gathers together their common
# properties.


##############################################################################

_elementlist = []
_savedelementlist = []


def _startgamesetup():
    global _elementlist, _savedelementlist
    _elementlist = []
    _savedelementlist = _elementlist.copy()


def _endgamesetup():
    global _savedelementlist
    for E in _elementlist:
        E._save()
    _savedelementlist = _elementlist.copy()


def _startgameturn():
    global _elementlist
    _elementlist = _savedelementlist.copy()
    for E in _elementlist:
        E._restore()
    for E in _elementlist:
        E._startspeed = E.speed()
        E._startaltitude = E.altitude()
        E._startaltitudeband = E.altitudeband()
        E._startaltitudecarry = E.altitudecarry()
        E._startedmoving = False
        E._attackstartgameturn()
        E._startgameturn()
    for E in _elementlist:
        E._startpath()


def _endgameturn():
    global _savedelementlist
    for E in _elementlist:
        E._attackendgameturn()
        E._endgameturn()
    for E in _elementlist:
        E._save()
    _savedelementlist = _elementlist.copy()


def _drawmap():
    for E in _elementlist:
        if not E.removed():
            E._draw()


##############################################################################


def fromname(name):
    """
    Look for the element with the given name. Return the element or None if
    no matching element is found.
    """

    if not isinstance(name, str):
        raise RuntimeError("name must be a string.")

    for E in _elementlist:
        if E.name() == name:
            return E
    return None


def aslist(withkilled=False):
    elementlist = _elementlist
    elementlist = filter(lambda E: not E.removed(), elementlist)
    if not withkilled:
        elementlist = filter(lambda E: not E.killed(), elementlist)
    return list(elementlist)


##############################################################################


def _xminforzoom(withkilled=False):
    if len(aslist(withkilled=withkilled)) == 0:
        return None
    else:
        return min([min(E.x(), E._path.xmin()) for E in aslist(withkilled=withkilled)])


def _xmaxforzoom(withkilled=False):
    if len(aslist(withkilled=withkilled)) == 0:
        return None
    else:
        return max([max(E.x(), E._path.xmax()) for E in aslist(withkilled=withkilled)])


def _yminforzoom(withkilled=False):
    if len(aslist(withkilled=withkilled)) == 0:
        return None
    else:
        return min([min(E._y, E._path.ymin()) for E in aslist(withkilled=withkilled)])


def _ymaxforzoom(withkilled=False):
    if len(aslist(withkilled=withkilled)) == 0:
        return None
    else:
        return max([max(E._y, E._path.ymax()) for E in aslist(withkilled=withkilled)])


##############################################################################


class Element:

    ############################################################################

    def __init__(
        self,
        name,
        x=None,
        y=None,
        facing=None,
        hexcode=None,
        azimuth=None,
        altitude=None,
        speed=None,
        color=None,
        delay=0,
    ):

        global _elementlist

        if isinstance(name, str):
            for E in _elementlist:
                if name == E._name:
                    raise RuntimeError("the name argument must be unique.")
        elif name is None:
            name = ""
        else:
            raise RuntimeError("the name argument must be a string or None.")

        self._name = name

        if azimuth is not None:
            if not glass.azimuth.isvalidazimuth(azimuth):
                raise RuntimeError("the azimuth argument is not valid.")
            facing = glass.azimuth.tofacing(azimuth)

        if hexcode is not None:
            if not glass.hexcode.isvalidhexcode(hexcode):
                raise RuntimeError("the hexcode argument is not valid.")
            x, y = glass.hexcode.toxy(hexcode)

        if not glass.hex.isvalid(x, y, facing):
            raise RuntimeError("the combination of hexcode and facing are not valid.")

        if altitude is not None and not glass.altitude.isvalidaltitude(altitude):
            raise RuntimeError("the altitude argument is not valid.")

        if delay < 0:
            raise RuntimeError("the delay argument is not valid.")
        while delay != 0:
            x, y = glass.hex.backward(x, y, facing)
            delay -= 1

        self._x = x
        self._y = y
        self._facing = facing
        self._altitude = altitude
        self._altitudeband = glass.altitude.altitudeband(self.altitude())
        self._altitudecarry = 0
        self._flightslope = None
        self._startedmoving = False
        self._isinterrainfollowingflight = False

        self._maneuvertype = None
        self._maneuversense = None
        self._maneuverfacingchange = 0
        self._maneuverfp = 0
        self._maneuverrequiredfp = 0
        self._bank = None
        self._manueversupersonic = False

        self._killed = False
        self._removed = False
        self._unspecifiedattackresult = 0

        if not glass.speed.isvalidspeed(speed):
            raise RuntimeError("the speed argument is not valid.")

        self._speed = speed

        self._path = glass.path.path(x, y, facing, altitude, speed)

        self._color = color

        self._gainedproperties = set([])
        self._lostproperties = set([])

        self._initdamage()
        self._inittracking()

        _elementlist.append(self)

    ############################################################################

    def _setposition(
        self,
        x=None,
        y=None,
        facing=None,
        hexcode=None,
        azimuth=None,
        altitude=None,
        altitudecarry=None,
    ):

        if hexcode is not None:
            if not glass.hexcode.isvalidhexcode(hexcode):
                raise RuntimeError("the hexcode argument is not valid.")
            x, y = glass.hexcode.toxy(hexcode)

        if x is None:
            x = self._x
        if y is None:
            y = self._y

        if azimuth is not None:
            if not glass.azimuth.isvalidazimuth(azimuth):
                raise RuntimeError("the azimuth argument is not valid.")
            facing = glass.azimuth.tofacing(azimuth)

        if facing is None:
            facing = self._facing

        if not glass.hex.isvalid(x, y, facing):
            raise RuntimeError("the combination of hexcode and facing are not valid.")

        if altitude is None:
            altitude = self._altitude
        elif not glass.altitude.isvalidaltitude(altitude):
            raise RuntimeError("the altitude argument is not valid.")

        if altitudecarry is None:
            altitudecarry = self._altitudecarry

        self._x = x
        self._y = y
        self._facing = facing
        self._altitude = altitude
        self._altitudeband = glass.altitude.altitudeband(self.altitude())
        self._altitudecarry = altitudecarry

    ############################################################################

    def _startgameturn(self):
        pass

    def _endgameturn(self):
        pass

    ############################################################################

    def _setxy(self, x=None, y=None):
        self._setposition(x=x, y=y)

    def _setfacing(self, facing):
        self._setposition(facing=facing)

    def _setaltitude(self, altitude=None):
        self._setposition(altitude=altitude)

    def _setaltitudecarry(self, altitudecarry=None):
        self._setposition(altitudecarry=altitudecarry)

    def _setspeed(self, speed=None):
        if speed is None:
            speed = self.speed()
        if not glass.speed.isvalidspeed(speed):
            raise RuntimeError("the speed argument is not valid.")
        self._speed = speed

    def _setflightslope(self, flightslope):
        self._flightslope = flightslope

    def _setlastposition(self):
        self._lastx = self.x()
        self._lasty = self.y()

    ############################################################################

    def _kill(self):
        self._killed = True

    def kill(self, note=None):
        try:
            glass.gameturn.checkingameturn()
            self.logcomment("has been killed.")
            self.lognote(note)
            self._kill()
        except RuntimeError as e:
            glass.log.logexception(e)
        self.logbreak()

    def _remove(self):
        self._removed = True

    def remove(self, note=None):
        try:
            glass.gameturn.checkingameturn()
            self.logcomment("has been removed.")
            self.lognote(note)
            self._removed = True
        except RuntimeError as e:
            glass.log.logexception(e)
        self.logbreak()

    ############################################################################

    def name(self):
        return self._name

    def x(self):
        return self._x

    def y(self):
        return self._y

    def xy(self):
        return self._x, self._y

    def hexcode(self):
        if glass.map.isonmap(self.x(), self.y()):
            return glass.hexcode.fromxy(self.x(), self.y())
        else:
            return None

    def facing(self):
        return self._facing

    def azimuth(self):
        if self.facing() is None:
            return None
        else:
            return glass.azimuth.fromfacing(self.facing())

    def altitude(self):
        if self._altitude is None:
            return self.terrainaltitude()
        else:
            return self._altitude

    def terrainaltitude(self):
        return glass.altitude.terrainaltitude(self.x(), self.y())

    def startaltitude(self):
        return self._startaltitude

    def altitudeband(self):
        return self._altitudeband

    def startaltitudeband(self):
        return self._startaltitudeband

    def altitudecarry(self):
        return self._altitudecarry

    def startaltitudecarry(self):
        return self._startaltitudecarry

    def position(self):
        hexcode = self.hexcode()
        if hexcode is None:
            hexcode = "-------"
        azimuth = self.azimuth()
        if azimuth is None:
            azimuth = "---"
        return "%-12s  %-3s  %2d" % (hexcode, azimuth, self.altitude())

    def speed(self):
        return self._speed

    def startspeed(self):
        return self._startspeed

    def newspeed(self):
        return self._newspeed


    def maneuver(self):
        """Return a string describing the current maneuver of the element."""
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
        elif self._bank != None:
            return "B%s" % self._bank
        else:
            return ""

    def flightslope(self):
        return self._flightslope

    def color(self):
        return self._color

    def killed(self):
        return self._killed

    def removed(self):
        return self._removed

    def isinterrainfollowingflight(self):
        return self._isinterrainfollowingflight

    def lastx(self):
        return self._lastx

    def lasty(self):
        return self._lasty

    def lastxy(self):
        return self._lastx, self._lasty

    ############################################################################

    def isaircraft(self):
        return False

    def ismissile(self):
        return False

    def isgroundunit(self):
        return False

    def ismarker(self):
        return False

    def isbomb(self):
        return False

    def isblastzone(self):
        return False

    def isbarragefire(self):
        return False

    def isship(self):
        return False
    
    def issurfaceelement(self):
        return self.isgroundunit() or self.isship()
    
    #############################################################################

    def note(self, s):
        """Write a note to the log."""
        self.lognote(s)
        self.logbreak()

    ############################################################################

    def _checknotkilled(self):
        if self.killed():
            raise RuntimeError("%s has been killed." % self.name())

    def _checknotremoved(self):
        if self.removed():
            raise RuntimeError("%s has been removed." % self.name())

    def _checknotsuppressed(self):
        if self.issuppressed():
            raise RuntimeError("%s is suppressed." % self.name())

    ############################################################################

    def _startpath(self):
        self._path.start(
            self.x(), self.y(), self.facing(), self.altitude(), self.speed()
        )

    def _extendpath(self):
        self._path.extend(self.x(), self.y(), self.facing(), self.altitude())

    def _drawpath(self, color, annotate=True, killed=False):
        self._path.draw(color, annotate=annotate, killed=killed, surfaceelement=self.issurfaceelement())

    ############################################################################

    def _save(self):
        self._saveddict = None
        self._saveddict = copy.copy(self.__dict__)

    def _restore(self):
        saveddict = self._saveddict
        self.__dict__.update(saveddict)
        self._saveddict = saveddict

    #############################################################################

    def _checkaltitude(self):
        """
        Check if the element has collided with terrain.
        """

        killed = False

        terrainaltitude = self.terrainaltitude()

        if self.isinterrainfollowingflight():
            if glass.map.iscity(*self.xy()):
                killed = "entered city while in terrain-following flight"
            elif glass.map.crossesridgeline(*self.lastxy(), *self.xy()):
                killed = "crossed ridge line while in terrain-following flight"
            elif self.altitude() < self.terrainaltitude():
                killed = "collided with terrain"
        elif self.altitude() <= self.terrainaltitude():
            killed = "collided with terrain"

        if killed is not False:
            self._setaltitude(terrainaltitude)
            self._altitudecarry = 0
            self.logwhenwhat(
                "",
                "%s at altitude %d." % (killed, terrainaltitude),
            )
            self._kill()

        if self.isinterrainfollowingflight() and (self.altitude() != terrainaltitude):
            raise RuntimeError(
                "did not maintain correct altitude for terrain-following flight."
            )

    def _checkforleavingmap(self):
        """
        Check if the element has left the map.
        """

        if not glass.map.isonmap(self.x(), self.y()):
            self.logwhenwhat("", "has left the map.")

    ############################################################################

    def hasproperty(self, p):
        return p not in self._lostproperties and (
            p in self._gainedproperties or p in self._properties()
        )

    def gainproperty(self, p):
        self._gainedproperties.add(p)

    def loseproperty(self, p):
        self._lostproperties.add(p)

    ############################################################################

    def logwhat(self, what, writefile=True):
        glass.log.logwhat(what, who=self.name(), writefile=writefile)

    def logwhenwhat(self, when, what, writefile=True):
        glass.log.logwhenwhat(when, what, who=self.name(), writefile=writefile)

    def logcomment(self, comment, writefile=True):
        glass.log.logcomment(
            comment,
            who=self.name(),
            writefile=writefile,
        )

    def lognote(self, note, writefile=True):
        glass.log.lognote(note, who=self.name(), writefile=writefile)

    def logbreak(self, writefile=True):
        glass.log.logbreak(who=self.name(), writefile=writefile)

    def logposition(self, when, writefile=True):
        self.logwhenwhat(when, self.position(), writefile=writefile)

    def logpositionandmaneuver(self, when, writefile=True):
        self.logwhenwhat(
            when, "%s  %s" % (self.position(), self.maneuver()), writefile=writefile
        )

    def logstart(self, what, writefile=True):
        self.logwhenwhat("start", what, writefile=writefile)

    def logend(self, what, writefile=True):
        self.logwhenwhat("end", what, writefile=writefile)

    ################################################################################

    def _assert(self, expectedposition, expectedspeed, expectedconfiguration=None):
        """
        Verify the position and new speed of an element.
        """

        if glass.log._error != None:
            print("== assertion failed ===")
            print("== unexpected error: %r" % glass.log._error)
            assert glass.log._error == None

        expectedposition = re.sub(" +", " ", expectedposition)
        actualposition = re.sub(" +", " ", self.position())

        if expectedposition != None and expectedposition != actualposition:
            print("== assertion failed ===")
            print("== actual   position: %s" % actualposition)
            print("== expected position: %s" % expectedposition)
            assert expectedposition == actualposition
        if expectedspeed is not None:
            if self._newspeed is None:
                if expectedspeed != self.speed():
                    print("== assertion failed ===")
                    print("== actual   speed: %.1f" % self.speed())
                    print("== expected speed: %.1f" % expectedspeed)
                    assert expectedspeed == self.speed()
            else:
                if expectedspeed != self._newspeed:
                    print("== assertion failed ===")
                    print("== actual   new speed: %.1f" % self._newspeed)
                    print("== expected new speed: %.1f" % expectedspeed)
                    assert expectedspeed == self._newspeed
        if (
            expectedconfiguration != None
            and expectedconfiguration != self._configuration
        ):
            print("== assertion failed ===")
            print("== actual   configuration: %s" % self._configuration)
            print("== expected configuration: %s" % expectedconfiguration)
            assert expectedconfiguration == self._configuration

    ############################################################################

    from glass.element.attack import (
        _attackstartgameturn,
        _attackendgameturn,
        _attackgroundunit,
        _attackaircraft,
        _secondaryattackgroundunit,
        attack,
        secondaryattack,
    )

    from glass.element.damage import (
        _initdamage,
        _damage,
        _damageatleast,
        _damageatmost,
        _takedamage,
        _takedamageconsequences,
        damage,
        damageatleast,
        damageatmost,
        takedamage,
        _takeattackdamage,
        issuppressed,
    )

    from glass.element.move import (
        move,
        continuemove,
        _move,
        _continuemove,
        _moveforward,
        _moveclimb,
        _movedive,
        _moveturn,
        _moveslide,
        _movedisplacementroll,
        _movelagroll,
        _moveverticalroll,
    )

    from glass.element.track import _inittracking, track, stoptracking
