import apengine._aircraft  as apaircraft
import apengine._azimuth   as apazimuth
import apengine._log       as aplog
import apengine._map       as apmap
import apengine._marker    as apmarker
import apengine._variants  as apvariants
import apengine._scenarios as apscenarios
 
################################################################################

# Turn is 0 between startsetup/endsetup, an integer greater than zero between
# startturn/endturn, and Null otherwise. It is incremented by endsetup/endturn.

_turn = None

# _savedturn holds the value of _turn outside of startsetup/endsetup and
# startturn/endturn.

_savedturn = None

def turn():
  return _turn

def _checkinsetuporturn():
  if _turn == None:
    raise RuntimeError("activity outside of setup or turn.")

def _checkinturn():
  if _turn == None or _turn == 0:
    raise RuntimeError("activity outside of turn.")

################################################################################

def startsetup(scenario, sheets=None, north="up", variants=[], **kwargs):

  """
  Start the set-up for the specified scenario (or for the specified map layout).
  """

  def log(s):
    aplog.log("set-up  : %s" % s)

  aplog.clearerror()
  try:
    
    global _turn, _savedturn
    _turn = 0
    _savedturn = _turn

    log("start of set-up.")
    aplog.logbreak()

    apvariants.setvariants(variants)

    if scenario != None:
      log("scenario is %s." % scenario)
      sheets    = apscenarios.sheets(scenario)
      north     = apscenarios.north(scenario)
      allforest = apscenarios.allforest(scenario)
    else:
      log("no scenario specified.")
      log("sheets are %r." % sheets)
      log("north is %s." % north)

    for key in kwargs.keys():
      log("map option %s is %r." % (key, kwargs[key]))

    apmap.setmap(sheets, **kwargs)

    apazimuth.setnorth(north)

    apaircraft._startsetup()
    apmarker._startsetup()

  except RuntimeError as e:
    aplog.logexception(e)
    
def endsetup():

  """
  End the set-up.
  """

  aplog.clearerror()
  try:
    
    global _turn, _savedturn
    if _turn != 0:
      raise RuntimeError("endturn() called out of sequence.")    
      
    apaircraft._endsetup()

    aplog.logbreak()
    aplog.log("set-up  : end of set-up.")

    _turn += 1
    _savedturn = _turn
    _turn = None

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

def startturn():

  """
  Start the next turn.
  """

  aplog.clearerror()
  try:
    
    global _turn, _savedturn
    _turn = _savedturn
    if _turn == None or _turn == 0:
      raise RuntimeError("startturn() called out of sequence.")
  
    aplog.log("turn %-2d: start of turn." % _turn)

    apaircraft._startturn()

  except RuntimeError as e:
    aplog.logexception(e)

def endturn():

  """
  End the current turn.
  """

  aplog.clearerror()
  try:
    
    global _turn, _savedturn
    if _turn == None or _turn == 0:
      raise RuntimeError("endturn() called out of sequence.")    

    apaircraft._endturn()

    aplog.logbreak()
    aplog.log("turn %-2d: end of turn." % _turn)

    _turn += 1
    _savedturn = _turn
    _turn = None
      
  except RuntimeError as e:
    aplog.logexception(e)


################################################################################

def drawmap():

  """
  Draw the map, with aircraft and markers at their current positions.
  """

  aplog.clearerror()
  try:

    apmap.startdrawmap()
    apmarker._drawmap()
    apaircraft._drawmap()
    apmap.enddrawmap(_savedturn)

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

from apengine._aircraft import aircraft
from apengine._marker   import marker
