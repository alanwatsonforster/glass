import apengine.aircraft   as apaircraft
import apengine._azimuth   as apazimuth
import apengine._log       as aplog
import apengine.map        as apmap
import apengine.marker     as apmarker
import apengine.variants   as apvariants
import apengine.scenarios  as apscenarios
 
################################################################################

# Turn is 0 between startsetup/endsetup, an integer greater than zero between
# startturn/endturn, and Null otherwise. It is incremented by endsetup/endturn.

_turn = None

# _savedturn holds the value of _turn outside of startsetup/endsetup and
# startturn/endturn.

_savedturn = None

def turn():
  return _turn

def _checkinstartuporturn():
  if _turn == None:
    raise RuntimeError("activity outside of setup or turn.")

def _checkinturn():
  if _turn == None or _turn == 0:
    raise RuntimeError("activity outside of turn.")

################################################################################

def startsetup(scenario, sheets=None, north="up", allforest=False, variants=[]):

  """
  Start the set-up for the specified scenario (or for the specified map layout).
  """

  aplog.clearerror()
  try:
    
    global _turn, _savedturn

    _turn = 0
    _savedturn = _turn

    aplog.log("--- start setup ---")
    aplog.logbreak()

    apvariants.setvariants(variants)

    if scenario != None:
      sheets    = apscenarios.sheets(scenario)
      north     = apscenarios.north(scenario)
      allforest = apscenarios.allforest(scenario)

    apmap.setmap(sheets, allforest=allforest)

    apazimuth.setnorth(north)

    apaircraft._startsetup()
    apmarker._startsetup()

  except RuntimeError as e:
    aplog.logexception(e)
    
def endsetup():

  """
  End the setup.
  """

  aplog.clearerror()
  try:
    
    global _turn, _savedturn

    apaircraft._endsetup()

    aplog.log("--- end setup ---")
    aplog.logbreak()

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

    if turn == None or turn == 0:
      raise RuntimeError("startturn() called out of sequence.")
  
    aplog.log("--- start of turn %d ---" % _turn)
    aplog.logbreak()

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

    if turn == None or turn == 0:
      raise RuntimeError("endturn() called out of sequence.")    

    apaircraft._endturn()

    aplog.log("--- end of turn %d ---" % _turn)
    aplog.logbreak()

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
    apmap.enddrawmap()

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

from apengine.aircraft import aircraft
from apengine.marker   import marker
