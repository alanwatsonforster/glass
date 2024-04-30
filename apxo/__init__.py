import apxo.azimuth        as apazimuth
import apxo.aircraft       as apaircraft
import apxo.draw           as apdraw
import apxo.element        as apelement
import apxo.log            as aplog
import apxo.map            as apmap
import apxo.marker         as apmarker
import apxo.missile        as apmissile
import apxo.order          as aporder
import apxo.variants       as apvariants
import apxo.scenarios      as apscenarios
import apxo.turn           as apturn
import apxo.visualsighting as apvisualsighting

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
  "marker",
  "missile"
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
    apmissile._startsetup()
    apelement._startsetup()

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

def startturn(note=False):

  """
  Start the next turn.
  """

  aplog.clearerror()
  try:
    
    apturn.startturn()
  
    aplog.log("start of turn.")

    apaircraft._startturn()
    apmissile._startturn()

    aplog.logbreak()
    aplog.log("initial positions, maneuvers, flight types, and speeds are:")
    for a in apaircraft.aslist():
      aplog.logaction(a, "%s  %-9s  %-3s  %4.1f" % (a.position(), a.maneuver(), a.flighttype(), a.speed()))
    aplog.lognote(None, note)

  except RuntimeError as e:
    aplog.logexception(e)

def endturn(note=False):

  """
  End the current turn.
  """

  aplog.clearerror()
  try:
    
    apaircraft._endturn()
    apmissile._endturn()

    aplog.logbreak()
    aplog.log("end of turn.")
    aplog.lognote(None, note)

    apturn.endturn()
      
  except RuntimeError as e:
    aplog.logexception(e)


################################################################################

def startvisualsighting():
  aplog.clearerror()
  try:
    apturn.checkinturn()
    apvisualsighting.startvisualsighting(), 
  except RuntimeError as e:
    aplog.logexception(e)

def endvisualsighting():
  aplog.clearerror()
  try:
    apturn.checkinturn()
    apvisualsighting.endvisualsighting(), 
  except RuntimeError as e:
    aplog.logexception(e)

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

def drawmap(
  zoom=True, 
  zoomincludesdestroyed=False,
  zoomborder=2,
  xmin=None, ymin=None, xmax=None, ymax=None,
  drawlimitedarc=[],
  draw180arc=[],
  draw150arc=[],
  draw120arc=[],
  draw90arc=[],
  draw60arc=[],
  draw30arc=[],
  drawL180arc=[],
  drawR180arc=[],
  ):

  """
  Draw the map, with aircraft and markers at their current positions.

  If zoom is True, zoom the map to include region including the
  aircraft, missiles, and markers with a border of zoomborder hexes. If
  zoomincludesdestroyed is True, include destroyed aircraft in the zoom.

  If zoom is False, use xmin, xmax, ymin, and ymax to defined the area
  drawn. If these are None, use the natural border of the map. Otherwise
  use their value.
  """

  aplog.clearerror()
  try:

    if zoom:

      xmin = apaircraft._xminforzoom(withdestroyed=zoomincludesdestroyed)
      xmax = apaircraft._xmaxforzoom(withdestroyed=zoomincludesdestroyed)
      ymin = apaircraft._yminforzoom(withdestroyed=zoomincludesdestroyed)
      ymax = apaircraft._ymaxforzoom(withdestroyed=zoomincludesdestroyed)

      if len(apmissile.aslist()) > 0:
        xmin = min(xmin, apmissile._xminforzoom())
        xmax = max(xmax, apmissile._xmaxforzoom())
        ymin = min(ymin, apmissile._yminforzoom())
        ymax = max(ymax, apmissile._ymaxforzoom())

      xmin -= zoomborder
      ymin -= zoomborder
      xmax += zoomborder
      ymax += zoomborder

    apmap.startdrawmap(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax)

    for A in drawlimitedarc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "limited")
    for A in draw30arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "30-")
    for A in draw60arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "60-")
    for A in draw90arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "90-")
    for A in draw120arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "120+")
    for A in draw150arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "150+")
    for A in draw180arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "180+")
    for A in drawL180arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "L180+")
    for A in drawR180arc:
      apdraw.drawarc(A.x(), A.y(), A.facing(), "R180+")
          
    apelement._drawmap()

    apmap.enddrawmap(apturn.turn())

  except RuntimeError as e:
    aplog.logexception(e)

################################################################################

from apxo.aircraft import aircraft
from apxo.marker   import marker
from apxo.missile  import missile
