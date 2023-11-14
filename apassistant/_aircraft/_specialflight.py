"""
Normal flight for the aircraft class.
"""

import math
from apengine._math import onethird, twothirds, roundtoquarter

import apengine._altitude as apaltitude
import apengine._hex      as aphex
import apengine._speed    as apspeed
import apengine._turnrate as apturnrate
import apengine._variants as apvariants

################################################################################

def _checkspecialflight(self):
  return

################################################################################

def _dospecialflight(self, action, note=False):

  """
  Carry out out special flight.
  """

  ########################################

  def dohorizontal():

    """
    Move horizontally.
    """

    self._x, self._y = aphex.forward(self._x, self._y, self._facing)

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    if altitudechange == 1:
      altitudechange = self.specialclimbcapability()
    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  ########################################

  def dodive(altitudechange):

    """
    Dive.
    """

    self._altitudecarry = 0
    
    self._altitude, self._altitudecarry = apaltitude.adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  ########################################

  def doturn(sense, facingchange):

    """
    Turn in the specified sense and amount.
    """
    
    # Change facing.
    if aphex.isedge(self._x, self._y):
      self._x, self._y = aphex.edgetocenter(self._x, self._y, self._facing, sense)
    if sense == "L":
      self._facing = (self._facing + facingchange) % 360
    else:
      self._facing = (self._facing - facingchange) % 360

  ########################################

  def doattack(weapon):

    """
    Declare an attack with the specified weapon.
    """

    self._logevent("attack using %s." % weapon)

  ########################################

  def dokilled():

    """
    Declare that the aircraft has been killed.
    """

    self._logaction("aircraft has been killed.")
    self._destroyed = True

  ########################################

  elementdispatchlist = [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C).
  
    ["L180" , lambda: doturn("L", 180) ],
    ["L150" , lambda: doturn("L", 150) ],
    ["L120" , lambda: doturn("L", 120) ],
    ["L90"  , lambda: doturn("L",  90) ],
    ["L60"  , lambda: doturn("L",  60) ],
    ["L30"  , lambda: doturn("L",  30) ],
    ["LLL"  , lambda: doturn("L",  90) ],
    ["LL"   , lambda: doturn("L",  60) ],
    ["L"    , lambda: doturn("L",  30) ],

    ["R180" , lambda: doturn("R", 180) ],
    ["R150" , lambda: doturn("R", 150) ],
    ["R120" , lambda: doturn("R", 120) ],
    ["R90"  , lambda: doturn("R",  90) ],
    ["R60"  , lambda: doturn("R",  60) ],
    ["R30"  , lambda: doturn("R",  30) ],
    ["RRR"  , lambda: doturn("R",  90) ],
    ["RR"   , lambda: doturn("R",  60) ],
    ["R"    , lambda: doturn("R",  30) ],

    ["AAGN"  , lambda: doattack("guns") ],
    ["AARK"  , lambda: doattack("rockets") ],

    ["K"    , lambda: dokilled()],

    ["/"    , lambda: None ],
    [","    , lambda: self._continueflightpath() ],

    ["H"    , lambda: dohorizontal() ],

    ["C1"   , lambda: doclimb(1) ],
    ["C2"   , lambda: doclimb(2) ],
    ["CC"   , lambda: doclimb(2) ],
    ["C"    , lambda: doclimb(1) ],

    ["D1"   , lambda: dodive(1) ],
    ["D2"   , lambda: dodive(2) ],
    ["D3"   , lambda: dodive(3) ],
    ["DDD"  , lambda: dodive(3) ],
    ["DD"   , lambda: dodive(2) ],
    ["D"    , lambda: dodive(1) ],

  ]

  ########################################

  def doaction(action):

    """
    Carry out an action for special flight.
    """
    
  self._logposition("start")
  self._logaction("", action)

  initialaltitude     = self._altitude
  initialaltitudeband = self._altitudeband

  while action != "":

    for element in elementdispatchlist:

      elementcode = element[0]
      elementprocedure = element[1]

      if len(elementcode) <= len(action) and elementcode == action[:len(elementcode)]:
        elementprocedure()
        action = action[len(elementcode):]
        self.checkforterraincollision()
        self.checkforleavingmap()
        if self._destroyed or self._leftmap:
          return
        break

    else:

      raise RuntimeError("invalid action %r." % action)

  self._lognote(note)
  
  self._logposition("end")
  self._continueflightpath()

  if initialaltitudeband != self._altitudeband:
    self._logevent("altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
  
  if not self._destroyed and not self._leftmap:
    if self._altitudecarry != 0:
      self._logend("is carrying %.2f altitude levels." % self._altitudecarry)

  self._newspeed = self._speed

################################################################################
