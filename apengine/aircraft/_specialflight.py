"""
Normal flight for the aircraft class.
"""

import math
from typing_extensions import LiteralString
from apengine.math import onethird, twothirds, roundtoquarter

import apengine.altitude as apaltitude
import apengine.hex      as aphex
import apengine.speed    as apspeed
import apengine.turnrate as apturnrate
import apengine.variants as apvariants

################################################################################

def _checkspecialflight(self):
  return

################################################################################

def _continuespecialflight(self, actions):

  """
  Continue to carry out out special flight.
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

  def dojettison(configuration):

    """
    Jetison stores to achieve the specified configuration.
    """

    # See rule 4.4. 
  
    # We implement the delay of 1 FP by making this an other element.

    if self._configuration == configuration:
      raise RuntimeError("configuration is already %s." % configuration)
    if self._configuration == "CL" or configuration == "DT":
      raise RuntimeError("attempt to change from configuration %s to %s." % (self._configuration, configuration))
    self._logevent("jettisoned stores.")
    self._logevent("configuration changed from %s to %s." % (self._configuration, configuration))
    self._configuration = configuration
  
  ########################################

  def doattack(weapon):

    """
    Declare an attack with the specified weapon.
    """

    self._logevent("- attack using %s." % weapon)

  ########################################

  def dokilled():

    """
    Declare that the aircraft has been killed.
    """

    self._logevent("- aircraft has been killed.")
    self._destroyed = True

  ########################################

  elementdispatchlist = [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C).

    # [0] is the element code.
    # [1] is the element type.
    # [2] is the element procedure.
  
    ["L90"   , "maneuver"           , lambda: doturn("L", 90) ],
    ["L60"   , "maneuver"           , lambda: doturn("L", 60) ],
    ["L30"   , "maneuver"           , lambda: doturn("L", 30) ],
    ["LLL"   , "maneuver"           , lambda: doturn("L", 90) ],
    ["LL"    , "maneuver"           , lambda: doturn("L", 60) ],
    ["L"     , "maneuver"           , lambda: doturn("L", 30) ],

    ["R90"   , "maneuver"           , lambda: doturn("R", 90) ],
    ["R60"   , "maneuver"           , lambda: doturn("R", 60) ],
    ["R30"   , "maneuver"           , lambda: doturn("R", 30) ],
    ["RRR"   , "maneuver"           , lambda: doturn("R", 90) ],
    ["RR"    , "maneuver"           , lambda: doturn("R", 60) ],
    ["R"     , "maneuver"           , lambda: doturn("R", 30) ],

    ["J1/2"  , "other"              , lambda: dojettison("1/2") ],
    ["JCL"   , "other"              , lambda: dojettison("CL") ],
    
    ["AGN"   , "other"              , lambda: doattack("guns") ],
    ["AGP"   , "other"              , lambda: doattack("gun pod") ],
    ["ARK"   , "other"              , lambda: doattack("rockets") ],
    ["ARP"   , "other"              , lambda: doattack("rocket pods") ],

    ["K"     , "other"              , lambda: dokilled()],

    ["/"     , "other"              , lambda: None ],

    ["H"    , "H"                   , lambda: dohorizontal() ],

    ["C1"   , "C or D"              , lambda: doclimb(1) ],
    ["C2"   , "C or D"              , lambda: doclimb(2) ],
    ["CC"   , "C or D"              , lambda: doclimb(2) ],
    ["C"    , "C or D"              , lambda: doclimb(1) ],

    ["D1"   , "C or D"              , lambda: dodive(1) ],
    ["D2"   , "C or D"              , lambda: dodive(2) ],
    ["D3"   , "C or D"              , lambda: dodive(3) ],
    ["DDD"  , "C or D"              , lambda: dodive(3) ],
    ["DD"   , "C or D"              , lambda: dodive(2) ],
    ["D"    , "C or D"              , lambda: dodive(1) ],

  ]

  ########################################

  def doelements(action, selectedelementtype, allowrepeated):

    """
    Carry out the elements in an action that match the element type.
    """

    fullaction = action

    ielement = 0

    while action != "":

      for element in elementdispatchlist:

        elementcode = element[0]
        elementtype = element[1]
        elementprocedure = element[2]

        if len(elementcode) <= len(action) and elementcode == action[:len(elementcode)]:
          if selectedelementtype == elementtype:
            ielement += 1
            elementprocedure()
          action = action[len(elementcode):]
          break

      else:

        raise RuntimeError("invalid action %r." % action)

    if ielement > 1 and not allowrepeated:
      raise RuntimeError("invalid action %r: repeated %s element." % (fullaction, selectedelementtype))

    return ielement != 0
  
  ########################################

  def doaction(action):

    """
    Carry out an action for normal flight.
    """


    # Check we have at least one FP remaining.
    if self._fp + 1 > self._maxfp:
      raise RuntimeError("only %.1f FPs are available." % self._maxfp)

    # Determine if this FP is the last FP of the move.
    self._lastfp = (self._fp + 2 > self._maxfp) 
    
    initialaltitude     = self._altitude
    initialaltitudeband = self._altitudeband

    try:
      
      if doelements(action, "maneuvering departure", False):
    
        self._maneuveringdeparture = True

        assert aphex.isvalid(self._x, self._y, facing=self._facing)
        assert apaltitude.isvalidaltitude(self._altitude)
  
        self._logaction("end", action, self.position())
        self._continueflightpath()
    
        return

      self._horizontal = doelements(action, "H", False)
      self._vertical   = doelements(action, "C or D", False)

      if not self._horizontal and not self._vertical:
        raise RuntimeError("%r is not a valid action." % action)
      elif self._horizontal and self._vertical:
        raise RuntimeError("%r is not a valid action when the flight type is %s." % (action, flighttype))

      self._fp += 1  

      maneuver = doelements(action, "maneuver" , False)

    except RuntimeError as e:
      self._logaction("FP %d" % self._fp, action, "")
      raise e
  
    self._logaction("FP %d" % self._fp, action, self.position())
    self._continueflightpath()

    if initialaltitudeband != self._altitudeband:
      self._logevent("- altitude band changed from %s to %s." % (initialaltitudeband, self._altitudeband))
      
    self.checkforterraincollision()
    self.checkforleavingmap()
    if self._destroyed or self._leftmap:
      return

    doelements(action, "other", True)

  ########################################
  
  flighttype         = self._flighttype
  previousflighttype = self._previousflighttype  
  
  if actions != "":
    for action in actions.split(","):
      if not self._destroyed and not self._leftmap:
        doaction(action)

  if self._destroyed or self._leftmap:
  
    self._log("---")
    self._endmove()

  elif self._fp + 1 > self._maxfp:

    # See rule 5.4.
    self._fpcarry = self._maxfp - self._fp

    self._endspecialflight()

################################################################################

def _startspecialflight(self, actions):
      
  """
  Start to carry out normal flight.
  """
 
  if self._altitudecarry != 0:
    self._log("- is carrying %.2f altitude levels." % self._altitudecarry)

  self._maxfp = self._speed + self._fpcarry
  self._log("- has %.1f FPs (including %.1f carry)." % (self._maxfp, self._fpcarry))
  self._fpcarry = 0

  self._fp = 0

  self._log("---")
  self._logaction("start", "", self.position())   

  self._continuespecialflight(actions)

################################################################################

def _endspecialflight(self):

  self._log("- is carrying %.1f FPs." % self._fpcarry)
  if self._altitudecarry != 0:
      self._log("- is carrying %.2f altitude levels." % self._altitudecarry)
  self._log("---")
  self._endmove()
