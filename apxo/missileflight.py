import apxo.altitude   as apaltitude
import apxo.flightpath as apflightpath
import apxo.hex        as aphex
import apxo.speed      as apspeed
import apxo.turn       as apturn

################################################################################

def move(M, speed, actions, note=False):

  """
  Start a move and possibly carry out some actions.
  """

  apturn.checkinturn()

  M._logbreak()
  M._logline()

  M._flightpath.start(M._x, M._y)

  if M._removed:
    M._endmove()
    return

  M._speed = speed
  if speed < apspeed.m1speed(M._altitudeband):
    M._logstart("speed         is %.1f." % speed)
  else:
    M._logstart("speed         is %.1f (SS)." % speed)  
  M._logstart("altitude band is %s." % M._altitudeband)
  M._logposition("start")

  M._fp = 0

  continuemove(M, actions, note)

def continuemove(M, actions, note=False):
  _doactions(M, actions)
  M._lognote(note)

################################################################################

def _doactions(M, actions):
  if actions != "":
    for action in actions.split(","):
      if not M._removed:
        _doaction(M, action)

################################################################################

def _doaction(M, action):

  """
  Carry out out missile flight.
  """

  ########################################

  def dohorizontal(element):

    """
    Move horizontally.
    """

    if element == "HD":
      M._altitude -= 1

    M._x, M._y = aphex.forward(M._x, M._y, M._facing)

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    M._altitude += altitudechange
    M._altitudeband = apaltitude.altitudeband(M._altitude)

  ########################################

  def dodive(altitudechange):

    """
    Dive.
    """

    M._altitude -= altitudechange
    M._altitudeband = apaltitude.altitudeband(M._altitude)

  ########################################

  def dodeclaremaneuver(maneuvertype, sense):
    M._maneuvertype  = maneuvertype
    M._maneuversense = sense
    
  ########################################

  def domaneuver(sense, facingchange, shift, continuous):

    if M._maneuvertype == None:
      raise RuntimeError("attempt to maneuver without a declaration.")
      
    if M._maneuversense != sense:
      raise RuntimeError("attempt to maneuver against the sense of the declaration.")

    if M._maneuvertype == "SL":

      M._x, M._y = aphex.slide(M._x, M._y, M._facing, sense)

    else:
    
      if aphex.isside(M._x, M._y) and shift:
        M._x, M._y = aphex.sidetocenter(M._x, M._y, M._facing, sense)
      if sense == "L":
        M._facing = (M._facing + facingchange) % 360
      else:
        M._facing = (M._facing - facingchange) % 360

    if not continuous:
      M._maneuvertype  = None
      M._maneuversense = None

  ########################################

  def doattack():

    """
    Declare an attack with the specified weapon.
    """

    M._logevent("attack.")

  ########################################

  def dokilled():

    """
    Declare that the missile has been killed.
    """

    M._logaction("missile has been killed.")
    M._destroyed = True

  ########################################

  elementdispatchlist = [

    # This table is searched in order, so put longer elements before shorter 
    # ones that are prefixes (e.g., put C2 before C).
  
    ["SLL"  , lambda: dodeclaremaneuver("SL", "L") ],
    ["SLR"  , lambda: dodeclaremaneuver("SL", "R") ],

    ["VRL"  , lambda: dodeclaremaneuver("VR", "L") ],
    ["VRR"  , lambda: dodeclaremaneuver("VR", "R") ],
    
    ["TL"   , lambda: dodeclaremaneuver("T" , "L") ],
    ["TR"   , lambda: dodeclaremaneuver("T" , "R") ],
    
    ["L90+"  , lambda: domaneuver("L",  90, True , True ) ],
    ["L60+"  , lambda: domaneuver("L",  60, True , True ) ],
    ["L30+"  , lambda: domaneuver("L",  30, True , True ) ],
    ["LLL+"  , lambda: domaneuver("L",  90, True , True ) ],
    ["LL+"   , lambda: domaneuver("L",  60, True , True ) ],
    ["L+"    , lambda: domaneuver("L",  30, True , True ) ],

    ["R90+"  , lambda: domaneuver("R",  90, True , True ) ],
    ["R60+"  , lambda: domaneuver("R",  60, True , True ) ],
    ["R30+"  , lambda: domaneuver("R",  30, True , True ) ],
    ["RRR+"  , lambda: domaneuver("R",  90, True , True ) ],
    ["RR+"   , lambda: domaneuver("R",  60, True , True ) ],
    ["R+"    , lambda: domaneuver("R",  30, True , True ) ],
    
    ["LS180" , lambda: domaneuver("L", 180, True , False) ],
    ["L180"  , lambda: domaneuver("L", 180, False, False) ],
    ["L150"  , lambda: domaneuver("L", 150, True , False) ],
    ["L120"  , lambda: domaneuver("L", 120, True , False, False) ],
    ["L90"   , lambda: domaneuver("L",  90, True , False) ],
    ["L60"   , lambda: domaneuver("L",  60, True , False) ],
    ["L30"   , lambda: domaneuver("L",  30, True , False) ],
    ["LLL"   , lambda: domaneuver("L",  90, True , False) ],
    ["LL"    , lambda: domaneuver("L",  60, True , False) ],
    ["L"     , lambda: domaneuver("L",  30, True , False) ],
 
    ["RS180" , lambda: domaneuver("R", 180, True , False) ],
    ["R180"  , lambda: domaneuver("R", 180, False, False) ],
    ["R150"  , lambda: domaneuver("R", 150, True , False) ],
    ["R120"  , lambda: domaneuver("R", 120, True , False) ],
    ["R90"   , lambda: domaneuver("R",  90, True , False) ],
    ["R60"   , lambda: domaneuver("R",  60, True , False) ],
    ["R30"   , lambda: domaneuver("R",  30, True , False) ],
    ["RRR"   , lambda: domaneuver("R",  90, True , False) ],
    ["RR"    , lambda: domaneuver("R",  60, True , False) ],
    ["R"     , lambda: domaneuver("R",  30, True , False) ],

    ["HD"   , lambda: dohorizontal("HD") ],
    ["H"    , lambda: dohorizontal("H")  ],
    
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

    ["AA"  , lambda: doattack() ],

    ["K"    , lambda: dokilled()],

    ["/"    , lambda: None ],

  ]

  ########################################
    
  M._logaction("FP %d" % (M._fp + 1), action)

  initialaltitude     = M._altitude
  initialaltitudeband = M._altitudeband

  while action != "":

    for element in elementdispatchlist:

      elementcode = element[0]
      elementprocedure = element[1]

      if len(elementcode) <= len(action) and elementcode == action[:len(elementcode)]:
        elementprocedure()
        action = action[len(elementcode):]
        M.checkforterraincollision()
        M.checkforleavingmap()
        if M._removed:
          return
        break

    else:

      raise RuntimeError("invalid action %r." % action)

  M._fp += 1
  M._flightpath.next(M._x, M._y)

  if M._fp == M._speed:
    M._logposition("end")
    M._logline()
  else:
    M._logposition("")

  if initialaltitudeband != M._altitudeband:
    M._logevent("altitude band changed from %s to %s." % (initialaltitudeband, M._altitudeband))
