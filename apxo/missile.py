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
      self.continuemove(actions)

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

  def continuemove(self, actions):

    aplog.clearerror()
    try:
      
      if actions != "":
        for action in actions.split(","):
          if not self._removed:
            _doaction(self, action)

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

  def doturn(sense, facingchange):

    """
    Turn in the specified sense and amount.
    """
    
    # Change facing.
    if aphex.isside(M._x, M._y):
      M._x, M._y = aphex.sidetocenter(M._x, M._y, M._facing, sense)
    if sense == "L":
      M._facing = (M._facing + facingchange) % 360
    else:
      M._facing = (M._facing - facingchange) % 360

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

