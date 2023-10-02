import airpower.aircraft as apaircraft
import airpower.azimuth  as apazimuth
import airpower.log      as aplog
import airpower.map      as apmap
import airpower.variants as apvariants

_turn = None

def startprolog(sheets, compassrose, north="up", variants=[]):
  global _turn
  _turn = None
  aplog.log("--- start prolog ---")
  aplog.logbreak()
  apvariants.setvariants(variants)
  aplog.logbreak()
  apmap.setmap(sheets, compassrose)
  aplog.logbreak()
  apazimuth.setnorth(north)
  aplog.logbreak()

  apaircraft._restart()

def endprolog():
  global _turn
  _turn = 0
  aplog.log("--- end prolog ---")
  aplog.logbreak()

def startturn():

  global _turn
  if turn == None:
    aplog.error("startturn() called before endprolog().")
  _turn += 1

  aplog.log("--- start of turn %d ---" % _turn)
  aplog.logbreak()

  apaircraft._allstartturn()

def endturn():

  apaircraft._allendturn()

  aplog.log("--- end of turn %d ---" % _turn)
  aplog.logbreak()

def turn():
  return _turn

def drawmap():
  apmap.drawmap()
  apaircraft._alldraw()

from airpower.aircraft import aircraft