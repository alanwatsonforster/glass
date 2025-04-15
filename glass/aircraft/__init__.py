import apxo.aircraftdata
import apxo.altitude
import apxo.azimuth
import apxo.capabilities
import apxo.closeformation
import apxo.element
import apxo.flight
import apxo.gameturn
import apxo.hex
import apxo.hexcode
import apxo.log
import apxo.map
import apxo.missile
import apxo.speed
import apxo.aircraft.stores
import apxo.turnrate
import apxo.geometry
import apxo.airtoair
import apxo.visualsighting

from apxo.flight import _isclimbingflight, _isdivingflight, _islevelflight

import re

##############################################################################


def aslist(withkilled=False):
    elementlist = apxo.element.aslist()
    aircraftlist = filter(lambda E: E.isaircraft(), elementlist)
    if not withkilled:
        aircraftlist = filter(lambda x: not x.killed(), aircraftlist)
    return list(aircraftlist)


#############################################################################


class Aircraft(apxo.element.Element):

    #############################################################################

    def __init__(
        self,
        name,
        force,
        aircrafttype,
        hexcode,
        azimuth,
        altitude,
        speed,
        configuration="CL",
        geometry=None,
        fuel=None,
        bingofuel=None,
        gunammunition=None,
        rocketfactors=None,
        stores=None,
        paintscheme="unpainted",
        color="unpainted",
        counter=False,
        delay=0,
    ):

        global _aircraftlist

        self._name = ""

        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating aircraft %s." % name)

            if not isinstance(aircrafttype, str):
                raise RuntimeError("the aircrafttype argument must be a string.")
            aircraftdata = apxo.aircraftdata.aircraftdata(aircrafttype)

            if not apxo.visualsighting.isvalidpaintscheme(paintscheme):
                raise RuntimeError("the paintscheme argument is not valid.")

            super().__init__(
                name,
                hexcode=hexcode,
                azimuth=azimuth,
                altitude=altitude,
                speed=speed,
                color=color,
                delay=delay,
            )

            # In addition to the specified position, azimuth, altitude, speed, and
            # configuration, aircraft initially have level flight, normal power, and
            # no carries.

            self._finishedmoving = False

            self._newspeed = None
            self._unspecifiedattackresult = 0
            self._flighttype = "LVL"
            self._powersetting = "N"
            self._bank = None
            self._maneuvertype = None
            self._maneuversense = None
            self._maneuverfp = 0
            self._maneuverrequiredfp = 0
            self._maneuverfacingchange = None
            self._manueversupersonic = False
            self._fpcarry = 0
            self._apcarry = 0
            self._gloccheck = 0
            self._unloadedrecoveryfp = -1
            self._ETrecoveryfp = -1
            self._BTrecoveryfp = -1
            self._HTrecoveryfp = -1
            self._TTrecoveryfp = -1
            self._rollrecoveryfp = -1
            self._trackingfp = 0
            self._lowspeedliftdeviceselected = False
            self._closeformation = []
            self._aircraftdata = aircraftdata
            if gunammunition is None:
                self._gunammunition = self._aircraftdata.gunammunition()
            else:
                self._gunammunition = gunammunition
            if rocketfactors is None:
                self._rocketfactors = self._aircraftdata.rocketfactors()
            else:
                self._rocketfactors = rocketfactors
            self._crew = self._aircraftdata.crew()
            self._sighted = False
            self._identified = False
            self._paintscheme = paintscheme
            self._turnsstalled = 0
            self._turnsdeparted = 0
            self._finishedmoving = True
            self._counter = counter
            self._force = force
            self._enginesmoking = False

            self._startaltitude = self.altitude()

            self.logwhenwhat("", "force         is %s." % force)
            self.logwhenwhat("", "type          is %s." % aircrafttype)
            self.logwhenwhat("", "position      is %s." % self.position())
            self.logwhenwhat("", "speed         is %.1f." % self.speed())

            self._setgeometry(geometry)
            if self.geometry() is not None:
                self.logwhenwhat("", "geometry      is %s." % self.geometry())

            # Determine the fuel and bingo levels.

            if isinstance(fuel, str) and fuel[-1] == "%" and fuel[:-1].isdecimal():
                fuel = float(fuel[:-1]) / 100
                self.logwhenwhat(
                    "", "fuel          is %3.0f%% of internal capacity." % (fuel * 100)
                )
                fuel *= self.internalfuelcapacity()
            elif fuel is not None and not isinstance(fuel, int | float):
                raise RuntimeError("invalid fuel value %r" % fuel)
            self._fuel = fuel

            if (
                isinstance(bingofuel, str)
                and bingofuel[-1] == "%"
                and bingofuel[:-1].isdecimal()
            ):
                bingofuel = float(bingofuel[:-1]) / 100
                self.logwhenwhat(
                    "",
                    "bingo fuel    is %3.0f%% of internal capacity."
                    % (bingofuel * 100),
                )
                bingofuel *= self.internalfuelcapacity()
            elif bingofuel is not None and not isinstance(bingofuel, int | float):
                raise RuntimeError("invalid bingo fuel value %r" % bingofuel)
            self._bingofuel = bingofuel

            if not self._fuel is None:
                if self._bingofuel is None:
                    self.logwhenwhat("", "fuel          is %.1f." % self._fuel)
                else:
                    self.logwhenwhat(
                        "",
                        "fuel          is %.1f and bingo fuel is %.1f."
                        % (self._fuel, self._bingofuel),
                    )

            # Determine the configuration, either explicitly or from the specified
            # stores.

            if stores is None:

                if configuration not in ["CL", "1/2", "DT"]:
                    raise RuntimeError("the configuration argument is not valid.")

                self._stores = stores
                self._configuration = configuration

            else:

                self._initstores(stores)

                if (
                    self.fuel() is not None
                    and self.fuel()
                    > self.internalfuelcapacity() + self.storesfuelcapacity()
                ):
                    raise RuntimeError(
                        "total fuel exceeds the internal and stores capacity."
                    )

            self.logwhenwhat("", "configuration is %s." % self._configuration)

            self._lowspeedliftdeviceextended = False
            self._minspeed = apxo.capabilities.minspeed(self)

            self._initaim()

        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    #############################################################################

    def isaircraft(self):
        return True

    #############################################################################

    def _startgameturn(self):
        self._setspeed(self._newspeed)
        self._newspeed = None
        self._finishedmoving = False
        self._sightedonpreviousturn = self._sighted
        self._enginesmokingonpreviousturn = self._enginesmoking
        self._sighted = False
        self._identifiedonpreviousturn = self._identified
        self._identified = False
        self._startx = self.x()
        self._starty = self.y()
        self._startfacing = self.facing()
        self._startaltitude = self.altitude()
        apxo.closeformation.check(self)

    def _endgameturn(self):
        if not self.killed() and not self.removed() and not self._finishedmoving:
            raise RuntimeError("aircraft %s has not finished its move." % self._name)
        if self.killed() or self.removed():
            apxo.closeformation.leaveany(self)
        else:
            apxo.closeformation.check(self)

    #############################################################################

    def force(self):
        """Return the force of the aircraft."""
        return self._force

    #############################################################################

    def paintscheme(self):
        """Return the paint scheme of the aircraft."""
        return self._paintscheme

    #############################################################################

    def crew(self):
        """Return the crew of the aircraft."""
        return self._crew

    #############################################################################

    def enginesmoking(self):
        """Return whether the engine is smoking."""
        return self._enginesmokingonpreviousturn

    #############################################################################

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
        elif self._bank != None:
            return "B%s" % self._bank
        else:
            return "WL"

    #############################################################################

    def flighttype(self):
        """Return the flight type of the aircraft."""
        return self._flighttype

    #############################################################################

    def _setgeometry(self, geometry):
        """Set the geometry of the aircraft."""
        if geometry not in apxo.capabilities.geometries(self):
            raise RuntimeError("the geometry argument %r is not valid." % geometry)
        self._geometry = geometry

    def geometry(self):
        """Return the geometry of the aircraft."""
        return self._geometry

    #############################################################################

    def react(self, attacktype, target, result, note=None):
        """
        Return fire, either with fixed guns or articulated guns.
        """

        try:

            apxo.gameturn.checkingameturn()
            self.logwhenwhat("react", action)

            apxo.airtoair.react(self, attacktype, target, result)

            self.lognote(note)

        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    ##############################################################################

    def hasproperty(self, p):

        if p == "LTD" and super().hasproperty("LTDCL"):
            return self._configuration == "CL"
        if p == "HRR" and super().hasproperty("HRRCL"):
            return self._configuration == "CL"
        if p == "RA" and super().hasproperty("RACL"):
            return self._configuration == "CL"
        if p == "LRR" and super().hasproperty("LRRHS"):
            return self.speed() >= self._aircraftdata["LRRHSlimit"]

        return super().hasproperty(p)

    def _properties(self):
        return apxo.capabilities.properties(self)

    ##############################################################################

    # Terrain-following Flight

    ##############################################################################

    def enterterrainfollowingflight(self, note=None):
        """
        Enter terrain-following flight.
        """

        try:

            if self._maneuvertype == "ET":
                raise RuntimeError(
                    "attempt to enter terrain-following flight while using a turn rate of ET."
                )
            if self.isinterrainfollowingflight():
                raise RuntimeError(
                    "attempt to enter terrain-following flight while already in terrain-following flight."
                )
            if self.altitude() != self.terrainaltitude() + 1:
                raise RuntimeError(
                    "attempt to enter terrain-following flight while not exactly one altitude level above terrain."
                )
            if not self.isinlevelflight():
                raise RuntimeError(
                    "attempt to enter terrain-following flight while not in level flight."
                )
            if self._leftterrainfollowingflightthisgameturn:
                raise RuntimeError(
                    "attempt to enter terrain-following flight after leaving it."
                )
            self._isinterrainfollowingflight = True
            self._setaltitude(self.terrainaltitude())
            self.logwhenwhat("", "enters terrain-following flight.")
            self.lognote(note)

        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    def leaveterrainfollowingflight(self, note=None):
        """
        Leave terrain-following flight.
        """

        try:

            if not self.isinterrainfollowingflight():
                raise RuntimeError(
                    "attempt to leave terrain-following flight while not in terrain-following flight."
                )
            self._isinterrainfollowingflight = False
            self._setaltitude(self.terrainaltitude() + 1)
            self._leftterrainfollowingflightthisgameturn = True
            self.logwhenwhat("", "leaves terrain-following flight.")
            self.lognote(note)

        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    ##############################################################################

    # Visual Sighting

    ##############################################################################

    def issighted(self):
        return apxo.visualsighting.issighted(self)

    ##############################################################################

    def padlock(self, other, note=None):
        """
        Padlock another aircraft.
        """

        # TODO: Check we are in the visual sighting phase.

        try:
            apxo.gameturn.checkingameturn()
            apxo.visualsighting.padlock(self, other, note=note)
        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    ##############################################################################

    def attempttosight(self, other, success=None, note=None):
        """
        Attempt to sight another aircraft.
        """

        try:
            apxo.gameturn.checkingameturn()
            apxo.visualsighting.attempttosight(self, other, success=None, note=None)
        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    #############################################################################

    def setsighted(self):
        """Set the aircraft to be sighted regardless."""
        apxo.visualsighting.setsighted(self)

    #############################################################################

    def setunsighted(self):
        """Set the aircraft to be unsighted regardless."""
        apxo.visualsighting.unsetsighted(self)

    #############################################################################

    def _maxvisualsightingrange(self):
        """
        Return the maximum visual sighting range of the aircraft.
        """

        return apxo.visualsighting.maxvisualsightingrange(self)

    #############################################################################

    def _visualsightingrange(self, target):
        """
        Return the visual sighting range for a visual sighting attempt from the
        aircraft on the target.
        """

        return apxo.visualsighting.visualsightingrange(self, target)

    #############################################################################

    def _visualsightingcondition(self, target):
        """
        Return a tuple describing the visual sighting condition for a visual
        sighting attempt from the aircraft on the target: a descriptive string,
        a boolean indicating if sighting is possible, and a boolean indicating if
        padlocking is possible.
        """

        return apxo.visualsighting.visualsightingcondition(self, target)

    #############################################################################

    # Fuel

    #############################################################################

    def fuel(self):
        """Return the current fuel points."""
        return self._fuel

    def internalfuel(self):
        """Return the current internal fuel points."""
        if self.fuel() is None:
            return None
        else:
            return min(self.fuel(), self.internalfuelcapacity())

    def storesfuel(self):
        """Return the current stores fuel points."""
        if self.fuel() is None:
            return None
        else:
            return max(0, self.fuel() - self.internalfuelcapacity())

    def internalfuelcapacity(self):
        """Return the internal fuel capacity."""
        return self._aircraftdata.internalfuelcapacity()

    def storesfuelcapacity(self):
        """Return the stores fuel capacity."""
        return self._storestotalfuelcapacity()

    ############################################################################

    # Bomb System

    ############################################################################

    def bombsystem(self):
        """Return the bomb system."""
        return self._aircraftdata.bombsystem()

    ############################################################################

    # Geometry

    #############################################################################

    def showgeometry(self, other, note=None):
        """
        Show the geometry of the other aircraft with respect to the aircraft.
        """

        try:
            apxo.gameturn.checkingameturn()
            showgeometry(self, other, note=None)
        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    #############################################################################

    def _angleofftail(self, other, **kwargs):
        """
        Return the angle of the aircraft off the tail of the other aircraft.
        """

        return apxo.geometry.angleofftail(self, other, **kwargs)

    #############################################################################

    def _inarc(self, other, arc):
        """
        Return True if the other aircraft is in the specified arc of the aircraft.
        Otherwise, return False.
        """

        return apxo.geometry.inarc(self, other, arc)

    #############################################################################

    def _inradararc(self, other, arc):
        """
        Return True if the other aircraft is in the specified radar arc of the
        aircraft. Otherwise, return False.
        """

        return apxo.geometry.inradararc(self, other, arc)

    #############################################################################

    def _gunattackrange(self, other, arc=False):
        """
        Return the gun attack range of the other aircraft from the aircraft
        or a string explaining why it cannot be attacked.
        """

        return apxo.airtoair.gunattackrange(self, other, arc=arc)

    #############################################################################

    def _rocketattackrange(self, other):
        """
        Return the rocket attack range of the other aircraft from the aircraft
        or a string explaining why it cannot be attacked.
        """

        return apxo.airtoair.rocketattackrange(self, other)

    #############################################################################

    def _inlimitedradararc(self, other):
        """
        Return True if the other aircraft is in the limited radar arc of the aircraft.
        """

        return apxo.geometry.inradararc(self, other, "limited")

    #############################################################################

    def isinclimbingflight(self, vertical=False):
        """
        Return true if the aircraft is climbing.
        """

        return _isclimbingflight(self._flighttype, vertical=vertical)

    #############################################################################

    def isindivingflight(self, vertical=False):
        """
        Return true if the aircraft is diving.
        """

        return _isdivingflight(self._flighttype, vertical=vertical)

    #############################################################################

    def isinlevelflight(self):
        """
        Return true if the aircraft is in level flight.
        """

        return _islevelflight(self._flighttype)

    ##############################################################################

    def hasbeenkilled(self, note=None):
        try:
            apxo.gameturn.checkingameturn()
            self._log("has been killed.")
            self.lognote(note)
            self._kill()
            self._color = None
        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    ################################################################################

    def _startmovespeed(
        self, power, flamedoutengines, lowspeedliftdeviceselected, speedbrakes, geometry
    ):
        apxo.speed.startmovespeed(
            self,
            power,
            flamedoutengines,
            lowspeedliftdeviceselected,
            speedbrakes,
            geometry,
        )

    def _endmovespeed(self):
        apxo.speed.endmovespeed(self)

    ################################################################################

    def joincloseformation(self, other):
        try:
            apxo.closeformation.join(self, other)
        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    def leavecloseformation(self):
        try:
            apxo.closeformation.leave(self)
        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    def closeformationsize(self):
        return apxo.closeformation.size(self)

    def closeformationnames(self):
        return apxo.closeformation.names(self)

    ########################################

    def ssgt(self, target=None):
        """
        Start SSGT.
        """

        # See rule 9.4.

        # The rules only explicitly prohibit SSGT during recovery from an
        # ET. However, we assume that SSGT has the same restrictions as
        # attacks.

        try:

            if apxo.flight.useofweaponsforbidden(self):
                raise RuntimeError(
                    "attempt to start SSGT while %s"
                    % apxo.flight.useofweaponsforbidden(self)
                )

            # TODO: Check we can start SSGT on a specific target.

            if target is None:
                raise RuntimeError("unknown target %s." % target.name())
            if not target.isaircraft():
                raise RuntimeError("target %s is not an aircraft." % target.name())

            if apxo.airtoair.trackingforbidden(self, target):
                raise RuntimeError(
                    "attempt to start SSGT while %s"
                    % apxo.airtoair.trackingforbidden(self, target)
                )

            self.logcomment("started SSGT on %s." % target.name())
            self._tracking = target

        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

    ################################################################################

    def airtoairlaunch(
        self,
        name,
        target,
        loadstation,
        failed=False,
        failedbeforelaunch=False,
        note=None,
    ):

        M = None

        try:

            if not self._finishedmoving:
                raise RuntimeError("launcher has not finished moving.")

            if not target._finishedmoving:
                raise RuntimeError("target has not finished moving.")

            previousconfiguration = self._configuration

            missiletype, newstores = apxo.aircraft.stores._airtoairlaunch(
                self._stores, loadstation, printer=lambda s: self.logcomment(s)
            )

            self._updateconfiguration()

            self.lognote(note)
            if failedbeforelaunch:
                self.logcomment("launch failed but missile not lost.")
            elif failed:
                self.logcomment("launch failed and missile lost.")
                self._stores = newstores
            else:
                self.logcomment("launch succeeded.")
                self._stores = newstores
                M = apxo.missile.Missile(name, missiletype, self, target)

            if self._configuration != previousconfiguration:
                self.logcomment(
                    "configuration changed from %s to %s."
                    % (previousconfiguration, self._configuration)
                )


        except RuntimeError as e:
            apxo.log.logexception(e)
        self.logbreak()

        return M

    ############################################################################

    from apxo.aircraft.aim import _initaim, aim, _stopaiming, stopaiming

    from apxo.aircraft.attack import (
        _attackaircraft,
        _attackgroundunit,
        _secondaryattackgroundunit,
        bomb,
    )

    from apxo.aircraft.damage import (
        _initdamage,
        _damage,
        _damageatleast,
        _damageatmost,
        _takedamage,
        _takedamageconsequences,
    )

    from apxo.aircraft.draw import _draw

    from apxo.aircraft.move import _move, _continuemove

    from apxo.aircraft.stores import (
        _initstores,
        _updateconfiguration,
        _storestotalweight,
        _storestotalload,
        _storestotalfuelcapacity,
        _showstores,
        showstores,
        _release,
        release,
    )

    ############################################################################
