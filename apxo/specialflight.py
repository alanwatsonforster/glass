"""
Special flight for aircaft.
"""

import apxo.altitude     as apaltitude
import apxo.capabilities as apcapabilities
import apxo.hex          as aphex
import apxo.speed        as apspeed
import apxo.turnrate     as apturnrate
import apxo.variants     as apvariants

################################################################################

def checkflight(A):
  return

################################################################################

def doflight(A, action, note=False):

  """
  Carry out out special flight.
  """

  ########################################

  def dohorizontal():

    """
    Move horizontally.
    """

    A.setxy(*aphex.forward(A.x(), A.y(), A.facing()))

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    if altitudechange == 1:
      altitudechange = apcapabilities.specialclimbcapability(A)
    
    altitude, altitudecarry = apaltitude.adjustaltitude(A.altitude(), A._altitudecarry, altitudechange)
    A.setaltitude(altitude)
    A._altitudecarry = altitudecarry

  ########################################

  def dodive(altitudechange):

    """
    Dive.
    """

    A._altitudecarry = 0
    
    altitude, altitudecarry = apaltitude.adjustaltitude(A.altitude(), A._altitudecarry, -altitudechange)
    A.setaltitude(altitude)

  ########################################

  def doturn(sense, facingchange):

    """
    Turn in the specified sense and amount.
    """
    
    # Change facing.
    if aphex.isside(A.x(), A.y()):
      A.setxy(*aphex.sidetocenter(A.x(), A.y(), A.facing(), sense))
    if sense == "L":
      A.setfacing((A.facing() + facingchange) % 360)
    else:
      A.setfacing((A.facing() - facingchange) % 360)

  ########################################

  def doattack(weapon):

    """
    Declare an attack with the specified weapon.
    """

    A._logevent("attack using %s." % weapon)

  ########################################

  def dokilled():

    """
    Declare that the aircraft has been killed.
    """

    A._logaction("aircraft has been killed.")
    A._destroyed = True

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
    
  A._logposition("start")
  A._logaction("", action)

  initialaltitude     = A.altitude()
  initialaltitudeband = A.altitudeband()

  while action != "":

    for element in elementdispatchlist:

      elementcode = element[0]
      elementprocedure = element[1]

      if len(elementcode) <= len(action) and elementcode == action[:len(elementcode)]:
        elementprocedure()
        action = action[len(elementcode):]
        A.checkforterraincollision()
        A.checkforleavingmap()
        if A._destroyed or A._leftmap:
          return
        break

    else:

      raise RuntimeError("invalid action %r." % action)

  A._lognote(note)
  
  A._logposition("end")
  A._flightpath.next(A.x(), A.y(), A.facing(), A.altitude())

  if initialaltitudeband != A.altitudeband():
    A._logevent("altitude band changed from %s to %s." % (initialaltitudeband, A.altitudeband()))
  
  if not A._destroyed and not A._leftmap:
    if A._altitudecarry != 0:
      A._logend("is carrying %.2f altitude levels." % A._altitudecarry)

  A._newspeed = A.speed()

################################################################################
