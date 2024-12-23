import copy
import re

import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.path as appath
import apxo.hex as aphex
import apxo.hexcode as aphexcode
import apxo.gameturn as apgameturn
import apxo.log as aplog
import apxo.map as apmap
import apxo.speed as apspeed

# Elements are anything that can be placed on a map: aircraft, missiles,
# ground units, markers, and bombs. This class gathers together their common
# properties.


##############################################################################

_elementlist = []


def _startgamesetup():
    global _elementlist
    _elementlist = []


def _endgamesetup():
    for E in _elementlist:
        E._save()


def _startgameturn():
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
    for E in _elementlist:
        E._attackendgameturn()
        E._endgameturn()
    for E in _elementlist:
        E._save()


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
    return min([min(E.x(), E._path.xmin()) for E in aslist(withkilled=withkilled)])


def _xmaxforzoom(withkilled=False):
    return max([max(E.x(), E._path.xmax()) for E in aslist(withkilled=withkilled)])


def _yminforzoom(withkilled=False):
    return min([min(E._y, E._path.ymin()) for E in aslist(withkilled=withkilled)])


def _ymaxforzoom(withkilled=False):
    return max([max(E._y, E._path.ymax()) for E in aslist(withkilled=withkilled)])


##############################################################################


class element:

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

        if not isinstance(name, str) and name is not None:
            raise RuntimeError("the name argument must be a string or None.")
        if name is not None:
            for E in _elementlist:
                if name == E._name:
                    raise RuntimeError("the name argument must be unique.")

        self._name = name

        if azimuth is not None:
            if not apazimuth.isvalidazimuth(azimuth):
                raise RuntimeError("the azimuth argument is not valid.")
            facing = apazimuth.tofacing(azimuth)

        if hexcode is not None:
            if not aphexcode.isvalidhexcode(hexcode):
                raise RuntimeError("the hexcode argument is not valid.")
            x, y = aphexcode.toxy(hexcode)

        if not aphex.isvalid(x, y, facing):
            raise RuntimeError("the combination of hexcode and facing are not valid.")

        if altitude is not None and not apaltitude.isvalidaltitude(altitude):
            raise RuntimeError("the altitude argument is not valid.")

        if delay < 0:
            raise RuntimeError("the delay argument is not valid.")
        while delay != 0:
            x, y = aphex.backward(x, y, facing)
            delay -= 1

        self._x = x
        self._y = y
        self._facing = facing
        self._altitude = altitude
        self._altitudeband = apaltitude.altitudeband(self.altitude())
        self._altitudecarry = 0
        self._flightslope = None
        self._startedmoving = False

        self._killed = False
        self._removed = False
        self._unspecifiedattackresult = 0

        if not apspeed.isvalidspeed(speed):
            raise RuntimeError("the speed argument is not valid.")

        self._speed = speed

        self._path = appath.path(x, y, facing, altitude, speed)

        self._color = color

        self._gainedproperties = set([])
        self._lostproperties = set([])

        self._initdamage()

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
            if not aphexcode.isvalidhexcode(hexcode):
                raise RuntimeError("the hexcode argument is not valid.")
            x, y = aphexcode.toxy(hexcode)

        if x is None:
            x = self._x
        if y is None:
            y = self._y

        if azimuth is not None:
            if not apazimuth.isvalidazimuth(azimuth):
                raise RuntimeError("the azimuth argument is not valid.")
            facing = apazimuth.tofacing(azimuth)

        if facing is None:
            facing = self._facing

        if not aphex.isvalid(x, y, facing):
            raise RuntimeError("the combination of hexcode and facing are not valid.")

        if altitude is None:
            altitude = self._altitude
        if not apaltitude.isvalidaltitude(altitude):
            raise RuntimeError("the altitude argument is not valid.")

        if altitudecarry is None:
            altitudecarry = self._altitudecarry

        self._x = x
        self._y = y
        self._facing = facing
        self._altitude = altitude
        self._altitudeband = apaltitude.altitudeband(self._altitude)
        self._altitudecarry = altitudecarry

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
        if not apspeed.isvalidspeed(speed):
            raise RuntimeError("the speed argument is not valid.")
        self._speed = speed

    def _setflightslope(self, flightslope):
        self._flightslope = flightslope

    ############################################################################

    def _kill(self):
        self._killed = True

    def kill(self, note=None):
        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            self.logcomment("has been killed.")
            self.lognote(note)
            self._kill()
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    def _remove(self):
        self._removed = True

    def remove(self, note=None):
        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            self.logcomment("has been removed.")
            self.lognote(note)
            self._removed = True
        except RuntimeError as e:
            aplog.logexception(e)
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
        if apmap.isonmap(self.x(), self.y()):
            return aphexcode.fromxy(self.x(), self.y())
        else:
            return None

    def facing(self):
        return self._facing

    def azimuth(self):
        if self.facing() is None:
            return None
        else:
            return apazimuth.fromfacing(self.facing())

    def altitude(self):
        if self._altitude is None:
            return apaltitude.terrainaltitude(self.x(), self.y())
        else:
            return self._altitude

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
        return ""

    def flightslope(self):
        return self._flightslope

    def color(self):
        return self._color

    def killed(self):
        return self._killed

    def removed(self):
        return self._removed

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
        self._path.draw(color, annotate=annotate, killed=killed)

    ############################################################################

    def _save(self):
        self._saveddict = None
        self._saveddict = copy.copy(self.__dict__)

    def _restore(self):
        saveddict = self._saveddict
        self.__dict__.update(saveddict)
        self._saveddict = saveddict

    #############################################################################

    def _checkforterraincollision(self):
        """
        Check if the element has collided with terrain.
        """

        altitudeofterrain = apaltitude.terrainaltitude(self.x(), self.y())
        if self.altitude() <= altitudeofterrain:
            self._setaltitude(altitudeofterrain)
            self._altitudecarry = 0
            self.logwhenwhat(
                "",
                "%s has collided with terrain at altitude %d."
                % (self.name(), altitudeofterrain),
            )
            self._kill()

    def _checkforleavingmap(self):
        """
        Check if the element has left the map.
        """

        if not apmap.isonmap(self.x(), self.y()):
            self.logwhenwhat("", "%s has left the map." % self.name())

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
        aplog.logwhat(what, who=self.name(), writefile=writefile)

    def logwhenwhat(self, when, what, writefile=True):
        aplog.logwhenwhat(when, what, who=self.name(), writefile=writefile)

    def logcomment(self, comment, writefile=True):
        aplog.logcomment(
            comment,
            who=self.name(),
            writefile=writefile,
        )

    def lognote(self, note, writefile=True):
        aplog.lognote(note, who=self.name(), writefile=writefile)

    def logbreak(self, writefile=True):
        aplog.logbreak(who=self.name(), writefile=writefile)

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

        if aplog._error != None:
            print("== assertion failed ===")
            print("== unexpected error: %r" % aplog._error)
            assert aplog._error == None

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

    from apxo.element.attack import (
        _attackstartgameturn,
        _attackendgameturn,
        _attackterrain,
        _attackgroundunit,
        _attackaircraft,
        _secondaryattackterrain,
        _secondaryattackgroundunit,
        attack,
        secondaryattack,
    )

    from apxo.element.damage import (
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

    from apxo.element.move import (
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
