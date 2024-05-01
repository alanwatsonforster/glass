import apxo.altitude   as apaltitude
import apxo.path       as appath
import apxo.geometry   as apgeometry
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

  M._path.start(*M.xy(), M.facing(), M.altitude())

  if M.removed():
    M._endmove()
    return

  M._setspeed(speed)
  if speed < apspeed.m1speed(M.altitudeband()):
    M._logstart("speed         is %.1f." % speed)
  else:
    M._logstart("speed         is %.1f (SS)." % speed)  
  M._logstart("altitude band is %s." % M.altitudeband())
  M._logposition("start")

  M._fp  = 0
  M._hfp = 0
  M._vfp = 0

  continuemove(M, actions, note)

def continuemove(M, actions, note=False):

  startaltitude = M.altitude()
  starthfp      = M._hfp

  _doactions(M, actions)

  endaltitude   = M.altitude()
  endhfp        = M._hfp

  slopenumerator   = endaltitude - startaltitude
  slopedenominator = endhfp - starthfp
  M._logevent("flight slope is %+d/%d." % (slopenumerator, slopedenominator))
  
  horizontalrange = apgeometry.horizontalrange(M, M._target)
  M._logevent("horizontal range is %d." % horizontalrange)

  altitudedifference = M._target.altitude() - M.altitude()
  M._logevent("altitude difference is %+d." % altitudedifference)

  def checknormallimit(minf, maxf):
    minaltitudedifference = int(minf * horizontalrange)
    maxaltitudedifference = int(maxf * horizontalrange)
    M._logevent("the allowed altitude difference range is [%+d,%+d]." % (minaltitudedifference, maxaltitudedifference))
    if altitudedifference < minaltitudedifference or altitudedifference > maxaltitudedifference:
      M._logevent("the target is not within the seeker vertical limits.")
    else:
      M._logevent("the target is within the seeker vertical limits.")


  if slopenumerator < - 3 * slopedenominator:
    pass
  elif slopenumerator < -1 * slopedenominator:
    checknormallimit(-7.0, -0.5)
  elif slopenumerator < 0:
    checknormallimit(-2.0, +0.5)
  elif slopenumerator == 0:
    checknormallimit(-1.0, +1.0)
  elif slopenumerator <= +1 * slopedenominator:
    checknormallimit(-0.5, +2.0)
  elif abs(slopenumerator) <= 3 * slopedenominator:
    checknormallimit(+0.5, +7.0)
  else:
    pass

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

    M._fp  += 1
    M._hfp += 1

    if element == "HD":
      M._dodive(1)

    M._doforward()

  ########################################

  def doclimb(altitudechange):

    """
    Climb.
    """

    M._fp  += 1
    M._vfp += 1
    
    M._doclimb(altitudechange)

  ########################################

  def dodive(altitudechange):

    """
    Dive.
    """

    M._fp  += 1
    M._vfp += 1

    M._dodive(altitudechange)

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

    assert(M._maneuvertype == "SL" or M._maneuvertype == "T" or M._maneuvertype == "VR")

    if M._maneuvertype == "SL":

      M._doslide(sense)

    elif M._maneuvertype == "VR":
    
      M._doverticalroll(sense, facingchange, shift)
      
    else:
    
      M._doturn(sense, facingchange)
    
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

  initialaltitude     = M.altitude()
  initialaltitudeband = M.altitudeband()

  fp = M._fp

  remainingaction = action

  while remainingaction != "":

    for element in elementdispatchlist:

      elementcode = element[0]
      elementprocedure = element[1]

      if len(elementcode) <= len(remainingaction) and elementcode == remainingaction[:len(elementcode)]:
        elementprocedure()
        remainingaction = remainingaction[len(elementcode):]
        M.checkforterraincollision()
        M.checkforleavingmap()
        if M._removed:
          return
        break

    else:

      raise RuntimeError("invalid action %r." % action)

  if M._fp == fp:
    raise RuntimeError("%r is not a valid action as it does not expend an FP." % action)
  elif M._fp > fp + 1:
    raise RuntimeError("%r is not a valid action as it attempts to expend more than one FP." % action)

  M._path.next(*M.xy(), M.facing(), M.altitude())

  if M._fp == M.speed():
    M._logposition("end")
    M._logline()
  else:
    M._logposition("")

  if initialaltitudeband != M.altitudeband():
    M._logevent("altitude band changed from %s to %s." % (initialaltitudeband, M.altitudeband()))
