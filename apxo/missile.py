import apxo.altitude      as apaltitude
import apxo.azimuth       as apazimuth
import apxo.draw          as apdraw
import apxo.flightpath    as apflightpath
import apxo.hexcode       as aphexcode
import apxo.log           as aplog
import apxo.map           as apmap
import apxo.missileflight as apmissileflight

_missilelist = []

def _startsetup():
  global _missilelist
  _missilelist = []

def _startturn():
  for M in _missilelist:
    M._restore()
    M._flightpath.start(M._x, M._y)

def _endturn():
  for M in _missilelist:
    M._save()
  
def _drawmap():
  for M in aslist():
    if not M._removed:
      M._flightpath.draw(M._color, M._zorder)
      M._draw()

##############################################################################

def aslist(withremoved=False):
  missilelist = _missilelist
  if not withremoved:
    missilelist = filter(lambda x: not x._removed, missilelist)
  return list(missilelist)
  
##############################################################################

def _xminforzoom():
  return min([min(M._x, M._flightpath.xmin()) for M in aslist()])

def _xmaxforzoom():
  return max([max(M._x, M._flightpath.xmax()) for M in aslist()])

def _yminforzoom():
  return min([min(M._y, M._flightpath.ymin()) for M in aslist()])

def _ymaxforzoom():
  return max([max(M._y, M._flightpath.ymax()) for M in aslist()])

##############################################################################

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

      self._maneuvertype  = None
      self._maneuversense = None

      self._color    = color
      self._removed  = False
      self._zorder   = launcher._zorder

      self._flightpath = apflightpath.flightpath(self._x, self._y)

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
    self._maneuvertype, \
    self._maneuversense, \
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
      self._maneuvertype, \
      self._maneuversense, \
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

      self._flightpath.start(self._x, self._y)

      self._logbreak()
      self._logline()
      self._logposition("start")
      if actions != "":
        for action in actions.split(","):
          if not self._removed:
            apmissileflight._doaction(self, action)
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
            apmissileflight._doaction(self, action)
      self._logline()

    except RuntimeError as e:
      aplog.logexception(e)

  #############################################################################

  def remove(self):
    self._removed = True
    
  #############################################################################
    
  def _draw(self):
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
