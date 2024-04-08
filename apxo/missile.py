import apxo.altitude as apaltitude
import apxo.azimuth  as apazimuth
import apxo.draw     as apdraw
import apxo.hex      as aphex
import apxo.hexcode  as aphexcode
import apxo.log      as aplog
import apxo.map      as apmap
import apxo.turn     as apturn

_missilelist = []

def _startsetup():
  global _missilelist
  _missilelist = []

def _startturn():
  for M in _missilelist:
    M._restore()
    M._startflightpath()

def _endturn():
  for M in _missilelist:
    M._save()
  
def _drawmap():
  for M in _missilelist:
    M._drawflightpath()
    M._draw()

class missile:

  def __init__(self, name, missiletype, launcher, color="white"):

    aplog.clearerror()
    try:

      self._logbreak()
      self._logline()
      
      self._name     = name
      self._logaction("", "creating missile %s." % name)

      self._type     = missiletype
      self._logaction("", "type          is %s." % missiletype)

      self._x, self._y   = launcher.x(), launcher.y()
      self._facing       = launcher.facing()
      self._altitude     = launcher.altitude()
      self._altitudeband = apaltitude.altitudeband(self._altitude)
      self._logaction("", "position      is %s." % self.position())

      self._color    = color
      self._removed  = False
      self._zorder   = launcher._zorder

      self._startflightpath()

      global _missilelist
      _missilelist.append(self)

      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  ##############################################################################

  # Turn management
  
  def _restore(self):

    """
    Restore the missile properties at the start of the turn.
    """

    self._x, \
    self._y, \
    self._facing, \
    self._altitude, \
    self._removed, \
    = self._saved
    self._altitudeband = apaltitude.altitudeband(self._altitude)

  def _save(self):

    """
    Save the missile properties at the end of the turn.
    """

    self._saved = ( \
      self._x, \
      self._y, \
      self._facing, \
      self._altitude, \
      self._removed, \
    )

  #############################################################################

  def position(self):
    """Return a string describing the current position of the aircraft."""
    if apmap.isonmap(self._x, self._y):
      hexcode = aphexcode.fromxy(self._x, self._y)
    else:
      hexcode = "-------"
    azimuth = apazimuth.fromfacing(self._facing)
    altitude = self._altitude
    return "%-12s  %-3s  %2d" % (hexcode, azimuth, altitude)
    
  #############################################################################
    
  def move(self, actions):

    aplog.clearerror()
    try:

      self._startflightpath()

      self._logbreak()
      self._logline()
      self._logposition("start")
      if actions != "":
        for action in actions.split(","):
          if not self._removed:
            _doaction(self, action)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

  def continuemove(self, actions):

    aplog.clearerror()
    try:
      
      self._logbreak()
      self._logline()
      if actions != "":
        for action in actions.split(","):
          if not self._removed:
            _doaction(self, action)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

  def remove(self):
    self._removed = True
    
  #############################################################################

  def _startflightpath(self):
    self._flightpathx = [self._x]
    self._flightpathy = [self._y]

  def _continueflightpath(self):
    self._flightpathx.append(self._x)
    self._flightpathy.append(self._y)

  def _drawflightpath(self):
    if self._removed:
      return
    apdraw.drawflightpath(self._flightpathx, self._flightpathy, self._color, self._zorder)
    
  def _draw(self):
    if self._removed:
      return
    apdraw.drawmissile(self._x, self._y, self._facing, self._color, self._name, self._altitude, self._zorder)

  ########################################

  def _logbreak(self):
    aplog.logbreak()
    
  def _log(self, s):
    aplog.log("%-4s : %s" % (self._name, s))

  def _logline(self):
    aplog.log("%-4s : %s :" % ("----", "-----"))
      
  def _log1(self, s, t):
    self._log("%-5s : %s" % (s, t))

  def _log2(self, s, t):
    self._log("%-5s : %-32s : %s" % (s, "", t))

  def _logposition(self, s):
    self._log1(s, self.position())

  def _logpositionandmaneuver(self, s):
    self._log1(s, "%s  %s" % (self.position(), self.maneuver()))

  def _logaction(self, s, t):
    self._log1(s, t)

  def _logevent(self, s):
    self._log2("", s)

  def _logstart(self, s):
    self._log1("start", s)

  def _logend(self, s):
    self._log1("end", s)

  def _lognote(self, note):
    aplog.lognote(self, note)
    
  #############################################################################

  def checkforterraincollision(self):

    """
    Check if the missile has collided with terrain.
    """

    altitudeofterrain = apaltitude.terrainaltitude(self._x, self._y)
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._logaction("", "missile has collided with terrain at altitude %d." % altitudeofterrain)
      self._removed = True

  def checkforleavingmap(self):

    """
    Check if the missile has left the map.
    """

    if not apmap.isonmap(self._x, self._y):
      self._logaction("", "missile has left the map.")
      self._removed = True
  
  ################################################################################

def _doaction(M, action, note=False):

  """
  Carry out out special flight.
  """

  ########################################

  def dohorizontal():

    """
    Move horizontally.
    """

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

    ["LS180+", lambda: domaneuver("L", 180, True , True ) ],
    ["L180+" , lambda: domaneuver("L", 180, False, True ) ],
    ["L150+" , lambda: domaneuver("L", 150, True , True ) ],
    ["L120+" , lambda: domaneuver("L", 120, True , True ) ],
    ["L90+"  , lambda: domaneuver("L",  90, True , True ) ],
    ["L60+"  , lambda: domaneuver("L",  60, True , True ) ],
    ["L30+"  , lambda: domaneuver("L",  30, True , True ) ],
    ["LLL+"  , lambda: domaneuver("L",  90, True , True ) ],
    ["LL+"   , lambda: domaneuver("L",  60, True , True ) ],
    ["L+"    , lambda: domaneuver("L",  30, True , True ) ],

    ["RS180+", lambda: domaneuver("R", 180, True , True ) ],
    ["R180+" , lambda: domaneuver("R", 180, False, True ) ],
    ["R150+" , lambda: domaneuver("R", 150, True , True ) ],
    ["R120+" , lambda: domaneuver("R", 120, True , True ) ],
    ["R90+"  , lambda: domaneuver("R",  90, True , True ) ],
    ["R60+"  , lambda: domaneuver("R",  60, True , True ) ],
    ["R30+"  , lambda: domaneuver("R",  30, True , True ) ],
    ["RRR+"  , lambda: domaneuver("R",  90, True , True ) ],
    ["RR+"   , lambda: domaneuver("R",  60, True , True ) ],
    ["R+"    , lambda: domaneuver("R",  30, True , True ) ],

    ["AA"  , lambda: doattack() ],

    ["K"    , lambda: dokilled()],

    ["/"    , lambda: None ],
    [","    , lambda: M._continueflightpath() ],

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

    ["TL"   , lambda: dodeclaremaneuver("T" , "L") ],
    ["TR"   , lambda: dodeclaremaneuver("T" , "R") ],
    ["SLL"  , lambda: dodeclaremaneuver("SL", "L") ],
    ["SLR"  , lambda: dodeclaremaneuver("SL", "R") ],
    ["VRL"  , lambda: dodeclaremaneuver("VR", "L") ],
    ["VRR"  , lambda: dodeclaremaneuver("VR", "R") ],
  ]

  ########################################

  def doaction(action):

    """
    Carry out an action for missile flight.
    """
    
  M._logaction("", action)

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

  M._lognote(note)
  
  M._logposition("end")
  M._continueflightpath()

  if initialaltitudeband != M._altitudeband:
    M._logevent("altitude band changed from %s to %s." % (initialaltitudeband, M._altitudeband))

################################################################################

