"""
Special flight for aircaft.
"""

from apxo.math import onethird, twothirds, roundtoquarter

import apxo.altitude     as apaltitude
import apxo.capabilities as apcapabilities
import apxo.hex          as aphex
import apxo.speed        as apspeed
import apxo.turnrate     as apturnrate
import apxo.variants     as apvariants

################################################################################

def checkflight(a):
  return

################################################################################

def doflight(a, action, note=False):

  """
  Carry out out special flight.
  """

  ########################################

  def dohorizontal():

    """
    Move horizontally.
    """

    a._x, a._y = aphex.forward(a._x, a._y, a._facing)

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    if altitudechange == 1:
      altitudechange = apcapabilities.specialclimbcapability(a)
    
    a._altitude, a._altitudecarry = apaltitude.adjustaltitude(a._altitude, a._altitudecarry, +altitudechange)
    a._altitudeband = apaltitude.altitudeband(a._altitude)

  ########################################

  def dodive(altitudechange):

    """
    Dive.
    """

    a._altitudecarry = 0
    
    a._altitude, a._altitudecarry = apaltitude.adjustaltitude(a._altitude, a._altitudecarry, -altitudechange)
    a._altitudeband = apaltitude.altitudeband(a._altitude)

  ########################################

  def doturn(sense, facingchange):

    """
    Turn in the specified sense and amount.
    """
    
    # Change facing.
    if aphex.isside(a._x, a._y):
      a._x, a._y = aphex.sidetocenter(a._x, a._y, a._facing, sense)
    if sense == "L":
      a._facing = (a._facing + facingchange) % 360
    else:
      a._facing = (a._facing - facingchange) % 360

  ########################################

  def doattack(weapon):

    """
    Declare an attack with the specified weapon.
    """

    a._logevent("attack using %s." % weapon)

  ########################################

  def dokilled():

    """
    Declare that the aircraft has been killed.
    """

    a._logaction("aircraft has been killed.")
    a._destroyed = True

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
    [","    , lambda: a._continueflightpath() ],

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
    
  a._logposition("start")
  a._logaction("", action)

  initialaltitude     = a._altitude
  initialaltitudeband = a._altitudeband

  while action != "":

    for element in elementdispatchlist:

      elementcode = element[0]
      elementprocedure = element[1]

      if len(elementcode) <= len(action) and elementcode == action[:len(elementcode)]:
        elementprocedure()
        action = action[len(elementcode):]
        a.checkforterraincollision()
        a.checkforleavingmap()
        if a._destroyed or a._leftmap:
          return
        break

    else:

      raise RuntimeError("invalid action %r." % action)

  a._lognote(note)
  
  a._logposition("end")
  a._continueflightpath()

  if initialaltitudeband != a._altitudeband:
    a._logevent("altitude band changed from %s to %s." % (initialaltitudeband, a._altitudeband))
  
  if not a._destroyed and not a._leftmap:
    if a._altitudecarry != 0:
      a._logend("is carrying %.2f altitude levels." % a._altitudecarry)

  a._newspeed = a._speed

################################################################################
