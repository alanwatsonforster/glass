import apxo.azimuth        as apazimuth
import apxo.aircraft       as apaircraft
import apxo.log            as aplog
import apxo.map            as apmap
import apxo.marker         as apmarker
import apxo.order          as aporder
import apxo.variants       as apvariants
import apxo.scenarios      as apscenarios
import apxo.turn           as apturn

__all__ = [
  "startsetup",
  "endsetup",
  "startturn",
  "endturn",
  "startvisualsighting",
  "endvisualsighting",
  "settraining",
  "orderofflightdeterminationphase",
  "drawmap",
  "aircraft",
  "marker"
]
 
################################################################################

def startsetup(scenario, sheets=None, north="up", variants=[], **kwargs):

  """
  Start the set-up for the specified scenario (or for the specified map layout).
  """

  aplog.clearerror()
  try:
    
    apturn.startsetup()

    aplog.log("start of set-up.")
    aplog.logbreak()

    apvariants.setvariants(variants)

    if scenario != None:
      aplog.log("scenario is %s." % scenario)
      sheets    = apscenarios.sheets(scenario)
      north     = apscenarios.north(scenario)
      allforest = apscenarios.allforest(scenario)
    else:
      aplog.log("no scenario specified.")
      aplog.log("sheets are %r." % sheets)
      aplog.log("north is %s." % north)

    for key in kwargs.keys():
      aplog.log("map option %s is %r." % (key, kwargs[key]))

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
          
    apaircraft._endsetup()

    aplog.logbreak()
    aplog.log("end of set-up.")

    apturn.endsetup()

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

def startturn():

  """
  Start the next turn.
  """

  aplog.clearerror()
  try:
    
    apturn.startturn()
  
    aplog.log("start of turn.")

    apaircraft._startturn()

    aplog.logbreak()
    aplog.log("initial positions, maneuvers, flight types, and speeds are:")
    for a in apaircraft.aslist():
      aplog.logaction(a, "%s  %-9s  %-3s  %4.1f" % (a.position(), a.maneuver(), a.flighttype(), a.speed()))

  except RuntimeError as e:
    aplog.logexception(e)

def endturn():

  """
  End the current turn.
  """

  aplog.clearerror()
  try:
    
    apaircraft._endturn()

    aplog.logbreak()
    aplog.log("end of turn.")

    apturn.endturn()
      
  except RuntimeError as e:
    aplog.logexception(e)


################################################################################

def startvisualsighting():
  apaircraft.startvisualsighting()

def endvisualsighting():
  apaircraft.endvisualsighting()

################################################################################

def settraining(training):
  aplog.clearerror()
  try:
    apturn.checkinsetup()
    aporder.settraining(training)
  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

def orderofflightdeterminationphase(
  rolls,
  firstkill=None,
  mostkills=None
  ):
  aplog.clearerror()
  try:
    apturn.checkinturn()
    aporder.orderofflightdeterminationphase(
      rolls,
      firstkill=firstkill,
      mostkills=mostkills
      )
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
    apmap.enddrawmap(apturn.turn())

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

from apxo.aircraft import aircraft
from apxo.marker   import marker
