import apxo as ap
import apxo.aircraftdata as apaircraftdata
import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.capabilities as apcapabilities
import apxo.closeformation as apcloseformation
import apxo.element as apelement
import apxo.flight as apflight
import apxo.gameturn as apgameturn
import apxo.hex as aphex
import apxo.hexcode as aphexcode
import apxo.log as aplog
import apxo.map as apmap
import apxo.missile as apmissile
import apxo.speed as apspeed
import apxo.aircraft.stores as apstores
import apxo.turnrate as apturnrate
import apxo.geometry as apgeometry
import apxo.airtoair as apairtoair
import apxo.visualsighting as apvisualsighting

from apxo.flight import _isclimbingflight, _isdivingflight, _islevelflight

import re

##############################################################################


def aslist(withkilled=False):
    elementlist = apelement.aslist()
    aircraftlist = filter(lambda E: E.isaircraft(), elementlist)
    if not withkilled:
        aircraftlist = filter(lambda x: not x.killed(), aircraftlist)
    return list(aircraftlist)


#############################################################################


class aircraft(apelement.element):

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

        aplog.clearerror()
        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating aircraft %s." % name)

            if not isinstance(aircrafttype, str):
                raise RuntimeError("the aircrafttype argument must be a string.")
            aircraftdata = apaircraftdata.aircraftdata(aircrafttype)

            if not apvisualsighting.isvalidpaintscheme(paintscheme):
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
            self._minspeed = apcapabilities.minspeed(self)

        except RuntimeError as e:
            aplog.logexception(e)
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
        apcloseformation.check(self)

    def _endgameturn(self):
        if not self.killed() and not self.removed() and not self._finishedmoving:
            raise RuntimeError("aircraft %s has not finished its move." % self._name)
        if self.killed() or self.removed():
            apcloseformation.leaveany(self)
        else:
            apcloseformation.check(self)

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
        if geometry not in apcapabilities.geometries(self):
            raise RuntimeError("the geometry argument %r is not valid." % geometry)
        self._geometry = geometry

    def geometry(self):
        """Return the geometry of the aircraft."""
        return self._geometry

    #############################################################################

    def note(self, s):
        """Write a note to the log."""
        self.lognote(s)
        self.logbreak()

    #############################################################################

    def react(self, attacktype, target, result, note=None):
        """
        Return fire, either with fixed guns or articulated guns.
        """

        aplog.clearerror()
        try:

            apgameturn.checkingameturn()
            self.logwhenwhat("react", action)

            apairtoair.react(self, attacktype, target, result)

            self.lognote(note)

        except RuntimeError as e:
            aplog.logexception(e)
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
        return apcapabilities.properties(self)

    ##############################################################################

    # Visual Sighting

    ##############################################################################

    def issighted(self):
        return apvisualsighting.issighted(self)

    ##############################################################################

    def padlock(self, other, note=None):
        """
        Padlock another aircraft.
        """

        # TODO: Check we are in the visual sighting phase.

        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            apvisualsighting.padlock(self, other, note=note)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    ##############################################################################

    def attempttosight(self, other, success=None, note=None):
        """
        Attempt to sight another aircraft.
        """

        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            apvisualsighting.attempttosight(self, other, success=None, note=None)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    #############################################################################

    def setsighted(self):
        """Set the aircraft to be sighted regardless."""
        apvisualsighting.setsighted(self)

    #############################################################################

    def setunsighted(self):
        """Set the aircraft to be unsighted regardless."""
        apvisualsighting.unsetsighted(self)

    #############################################################################

    def _maxvisualsightingrange(self):
        """
        Return the maximum visual sighting range of the aircraft.
        """

        return apvisualsighting.maxvisualsightingrange(self)

    #############################################################################

    def _visualsightingrange(self, target):
        """
        Return the visual sighting range for a visual sighting attempt from the
        aircraft on the target.
        """

        return apvisualsighting.visualsightingrange(self, target)

    #############################################################################

    def _visualsightingcondition(self, target):
        """
        Return a tuple describing the visual sighting condition for a visual
        sighting attempt from the aircraft on the target: a descriptive string,
        a boolean indicating if sighting is possible, and a boolean indicating if
        padlocking is possible.
        """

        return apvisualsighting.visualsightingcondition(self, target)

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

    #############################################################################

    # Geometry

    #############################################################################

    def showgeometry(self, other, note=None):
        """
        Show the geometry of the other aircraft with respect to the aircraft.
        """

        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            showgeometry(self, other, note=None)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    #############################################################################

    def _angleofftail(self, other, **kwargs):
        """
        Return the angle of the aircraft off the tail of the other aircraft.
        """

        return apgeometry.angleofftail(self, other, **kwargs)

    #############################################################################

    def _inarc(self, other, arc):
        """
        Return True if the other aircraft is in the specified arc of the aircraft.
        Otherwise, return False.
        """

        return apgeometry.inarc(self, other, arc)

    #############################################################################

    def _inradararc(self, other, arc):
        """
        Return True if the other aircraft is in the specified radar arc of the
        aircraft. Otherwise, return False.
        """

        return apgeometry.inradararc(self, other, arc)

    #############################################################################

    def _gunattackrange(self, other, arc=False):
        """
        Return the gun attack range of the other aircraft from the aircraft
        or a string explaining why it cannot be attacked.
        """

        return apairtoair.gunattackrange(self, other, arc=arc)

    #############################################################################

    def _rocketattackrange(self, other):
        """
        Return the rocket attack range of the other aircraft from the aircraft
        or a string explaining why it cannot be attacked.
        """

        return apairtoair.rocketattackrange(self, other)

    #############################################################################

    def _inlimitedradararc(self, other):
        """
        Return True if the other aircraft is in the limited radar arc of the aircraft.
        """

        return apgeometry.inradararc(self, other, "limited")

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
        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            self._log("has been killed.")
            self.lognote(note)
            self._kill()
            self._color = None
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    ################################################################################

    def _startmovespeed(
        self, power, flamedoutengines, lowspeedliftdeviceselected, speedbrakes, geometry
    ):
        apspeed.startmovespeed(
            self,
            power,
            flamedoutengines,
            lowspeedliftdeviceselected,
            speedbrakes,
            geometry,
        )

    def _endmovespeed(self):
        apspeed.endmovespeed(self)

    ################################################################################

    def joincloseformation(self, other):
        aplog.clearerror()
        try:
            apcloseformation.join(self, other)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    def leavecloseformation(self):
        aplog.clearerror()
        try:
            apcloseformation.leave(self)
        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    def closeformationsize(self):
        return apcloseformation.size(self)

    def closeformationnames(self):
        return apcloseformation.names(self)

    ########################################

    def ssgt(self, target=None):
        """
        Start SSGT.
        """

        # See rule 9.4.

        # The rules only explicitly prohibit SSGT during recovery from an
        # ET. However, we assume that SSGT has the same restrictions as
        # attacks.

        aplog.clearerror()
        try:

            if apflight.useofweaponsforbidden(self):
                raise RuntimeError(
                    "attempt to start SSGT while %s"
                    % apflight.useofweaponsforbidden(self)
                )

            # TODO: Check we can start SSGT on a specific target.

            if target is None:
                raise RuntimeError("unknown target %s." % target.name())
            if not target.isaircraft():
                raise RuntimeError("target %s is not an aircraft." % target.name())

            if apairtoair.trackingforbidden(self, target):
                raise RuntimeError(
                    "attempt to start SSGT while %s"
                    % apairtoair.trackingforbidden(self, target)
                )

            self.logcomment("started SSGT on %s." % target.name())
            self._tracking = target

        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

    ################################################################################

    def airtoairlaunch(
        self,
        name,
        target,
        loadstation,
        failed=False,
        failedbeforelaunch=False,
    ):

        M = None

        aplog.clearerror()
        try:

            if not self._finishedmoving:
                raise RuntimeError("launcher has not finished moving.")

            if not target._finishedmoving:
                raise RuntimeError("target has not finished moving.")

            previousconfiguration = self._configuration

            missiletype, newstores = apstores._airtoairlaunch(
                self._stores, loadstation, printer=lambda s: self.logcomment(s)
            )

            self._updateconfiguration()

            if failedbeforelaunch:
                self.logcomment("launch failed but missile not lost.")
            elif failed:
                self.logcomment("launch failed and missile lost.")
                self._stores = newstores
            else:
                self.logcomment("launch succeeded.")
                self._stores = newstores
                M = apmissile.missile(name, missiletype, self, target)

            if self._configuration != previousconfiguration:
                self.logcomment(
                    "configuration changed from %s to %s."
                    % (previousconfiguration, self._configuration)
                )

        except RuntimeError as e:
            aplog.logexception(e)
        self.logbreak()

        return M

    ############################################################################

    from apxo.aircraft.attack import (
        _attackaircraft,
        _attackgroundunit,
        _secondaryattackgroundunit,
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

    from apxo.aircraft.stores import _initstores, _updateconfiguration, _storestotalweight, _storestotalload, _storestotalfuelcapacity, _showstores, showstores, _release, release

    ############################################################################
