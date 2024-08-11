import apxo as ap
import apxo.aircraftdata as apaircraftdata
import apxo.altitude as apaltitude
import apxo.azimuth as apazimuth
import apxo.closeformation as apcloseformation
import apxo.configuration as apconfiguration
import apxo.damage as apdamage
import apxo.draw as apdraw
import apxo.element as apelement
import apxo.aircraftflight as apaircraftflight
import apxo.gameturn as apgameturn
import apxo.hex as aphex
import apxo.hexcode as aphexcode
import apxo.log as aplog
import apxo.map as apmap
import apxo.speed as apspeed
import apxo.stores as apstores
import apxo.turnrate as apturnrate
import apxo.geometry as apgeometry
import apxo.airtoair as apairtoair
import apxo.visualsighting as apvisualsighting

from apxo.aircraftflight import _isclimbingflight, _isdivingflight, _islevelflight

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
        fuel=None,
        bingofuel=None,
        gunammunition=None,
        rocketfactors=None,
        stores=None,
        paintscheme="unpainted",
        color="unpainted",
        counter=False,
    ):

        global _aircraftlist

        aplog.clearerror()
        try:

            super().__init__(
                name,
                hexcode=hexcode,
                azimuth=azimuth,
                altitude=altitude,
                speed=speed,
                color=color,
            )

            if not isinstance(aircrafttype, str):
                raise RuntimeError("the aircrafttype argument must be a string.")
                raise RuntimeError("the configuration argument is not valid.")
            if not apvisualsighting.isvalidpaintscheme(paintscheme):
                raise RuntimeError("the paintscheme argument is not valid.")

            # In addition to the specified position, azimuth, altitude, speed, and
            # configuration, aircraft initially have level flight, normal power, and
            # no carries.

            self._logbreak()
            self._logline()
            self._logaction("", "creating aircraft %s." % name)

            self._newspeed = None
            self._unspecifiedattackresult = 0
            self._damageL = 0
            self._damageH = 0
            self._damageC = 0
            self._damageK = 0
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
            self._climbslope = 0
            self._lowspeedliftdeviceselected = False
            self._closeformation = []
            self._aircraftdata = apaircraftdata.aircraftdata(aircrafttype)
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
            self._finishedmove = True
            self._counter = counter
            self._force = force
            self._enginesmoking = False

            self._startaltitude = self.altitude()

            self._logaction("", "force         is %s." % force)
            self._logaction("", "type          is %s." % aircrafttype)
            self._logaction("", "position      is %s." % self.position())
            self._logaction("", "speed         is %.1f." % self.speed())

            # Determine the fuel and bingo levels.

            if isinstance(fuel, str) and fuel[-1] == "%" and fuel[:-1].isdecimal():
                fuel = float(fuel[:-1]) / 100
                self._logaction(
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
                self._logaction(
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
                    self._logaction("", "fuel          is %.1f." % self._fuel)
                else:
                    self._logaction(
                        "",
                        "fuel          is %.1f and bingo fuel is %.1f."
                        % (self._fuel, self._bingofuel),
                    )

            # Determine the configuration, either explicitly or from the specified
            # stores.

            if stores is None:

                self._stores = stores
                self._configuration = configuration

            else:

                self._stores = apstores._checkstores(stores)
                if len(self._stores) != 0:
                    apstores._showstores(
                        stores,
                        printer=lambda s: self._logaction("", s),
                        fuel=self.externalfuel(),
                    )

                if (
                    self.fuel() is not None
                    and self.fuel()
                    > self.internalfuelcapacity() + self.externalfuelcapacity()
                ):
                    raise RuntimeError(
                        "total fuel exceeds the internal and external capacity."
                    )

            apconfiguration.update(self)
            self._logaction("", "configuration is %s." % self._configuration)

            self._logline()

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    def isaircraft(self):
        return True

    #############################################################################

    def _startgameturn(self):
        self._setspeed(self._newspeed)
        self._newspeed = None
        self._finishedmove = False
        self._sightedonpreviousturn = self._sighted
        self._enginesmokingonpreviousturn = self._enginesmoking
        self._sighted = False
        self._identifiedonpreviousturn = self._identified
        self._identified = False
        self._unspecifiedattackresult = 0
        apcloseformation.check(self)

    def _endgameturn(self):
        if not self.killed() and not self.removed() and not self._finishedmove:
            raise RuntimeError("aircraft %s has not finished its move." % self._name)
        if self._unspecifiedattackresult > 0:
            raise RuntimeError(
                "aircraft %s has %d unspecified attack %s."
                % (
                    self._name,
                    self._unspecifiedattackresult,
                    aplog.plural(self._unspecifiedattackresult, "result", "results"),
                )
            )
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

    def note(self, s):
        """Write a note to the log."""
        self._lognote(s)
        self._logline()

    #############################################################################

    def react(self, action, note=False):
        """
        Return fire, either with fixed guns or articulated guns.
        """

        aplog.clearerror()
        try:

            apgameturn.checkingameturn()
            self._logaction("react", action)

            m = re.compile("AA" + 3 * r"\(([^)]*)\)").match(action)
            if m is None:
                raise RuntimeError("invalid action %r" % action)

            attacktype = m[1]
            targetname = m[2]
            result = m[3]

            if targetname == "":
                target = None
            else:
                target = apelement.fromname(targetname)
                if target is None:
                    raise RuntimeError("unknown target %s." % targetname)
                if not target.isaircraft():
                    raise RuntimeError("target %s is not an aircraft." % targetname)

            apairtoair.react(self, attacktype, target, result)

            self._lognote(note)
            self._logline()

        except RuntimeError as e:
            aplog.logexception(e)

    ##############################################################################

    # Visual Sighting

    ##############################################################################

    def issighted(self):
        return apvisualsighting.issighted(self)

    ##############################################################################

    def padlock(self, other, note=False):
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

    ##############################################################################

    def attempttosight(self, other, success=None, note=False):
        """
        Attempt to sight another aircraft.
        """

        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            apvisualsighting.attempttosight(self, other, success=None, note=False)
        except RuntimeError as e:
            aplog.logexception(e)

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

    def externalfuel(self):
        """Return the current external fuel points."""
        if self.fuel() is None:
            return None
        else:
            return max(0, self.fuel() - self.internalfuelcapacity())

    def internalfuelcapacity(self):
        """Return the internal fuel capacity."""
        return self._aircraftdata.internalfuelcapacity()

    def externalfuelcapacity(self):
        """Return the external fuel capacity."""
        return apstores.totalfuelcapacity(self._stores)

    #############################################################################

    # Stores

    #############################################################################

    def showstores(self, note=False):
        """
        Show the aircraft's stores to the log.
        """

        aplog.clearerror()
        try:

            apgameturn.checkingamesetuporgameturn()
            self._logbreak()
            self._logline()

            apstores._showstores(
                self._stores, printer=lambda s: self._log(s), fuel=self.externalfuel()
            )

            self._lognote(note)
            self._logline()

        except RuntimeError as e:
            aplog.logexception(e)

    #############################################################################

    # Geometry

    #############################################################################

    def showgeometry(self, other, note=False):
        """
        Show the geometry of the other aircraft with respect to the aircraft.
        """

        aplog.clearerror()
        try:
            apgameturn.checkingameturn()
            showgeometry(self, other, note=False)
        except RuntimeError as e:
            aplog.logexception(e)

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

    def hasbeenkilled(self):
        apgameturn.checkingameturn()
        self.kill()
        self._log("has been killed.")
        self._color = None

    ################################################################################

    def _assert(self, expectedposition, expectedspeed, expectedconfiguration=None):
        """
        Verify the position and new speed of an aircraft.
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

    ################################################################################

    def _draw(self):
        if self.killed():
            color = None
        else:
            color = self._color
        self._drawpath(color)
        apdraw.drawaircraft(
            self.x(),
            self.y(),
            self.facing(),
            color,
            self.name(),
            self.altitude(),
            self.speed(),
            self._flighttype,
        )

    ################################################################################

    def _startmovespeed(
        self, power, flamedoutengines, lowspeedliftdeviceselected, speedbrakes
    ):
        apspeed.startmovespeed(
            self, power, flamedoutengines, lowspeedliftdeviceselected, speedbrakes
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

    def leavecloseformation(self):
        aplog.clearerror()
        try:
            apcloseformation.leave(self)
        except RuntimeError as e:
            aplog.logexception(e)

    def closeformationsize(self):
        return apcloseformation.size(self)

    def closeformationnames(self):
        return apcloseformation.names(self)

    ################################################################################

    def _move(self, *args, **kwargs):
        apaircraftflight.move(self, *args, **kwargs)

    def continuemove(self, *args, **kwargs):
        apaircraftflight.continuemove(self, *args, **kwargs)

    ################################################################################

    def takedamage(self, damage, note=False):
        aplog.clearerror()
        try:
            apdamage.takedamage(self, damage)
            self._lognote(note)
            self._logline()
        except RuntimeError as e:
            aplog.logexception(e)

    def damage(self):
        return apdamage.damage(self)

    def damageatleast(self, damage):
        return apdamage.damageatleast(self, damage)

    def damageatmost(self, damage):
        return apdamageatmost(self, damage)

    ################################################################################
