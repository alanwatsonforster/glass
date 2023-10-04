import airpower.aircraft as apaircraft
import airpower.azimuth  as apazimuth
import airpower.log      as aplog
import airpower.map      as apmap
import airpower.variants as apvariants

_turn = None

def startprolog(sheets, compassrose, north="up", variants=[]):

  global _turn

  aplog.log("--- start prolog ---")
  aplog.logbreak()

  apvariants.setvariants(variants)
  aplog.logbreak()

  apmap.setmap(sheets, compassrose)
  aplog.logbreak()

  apazimuth.setnorth(north)
  aplog.logbreak()

  apaircraft._restart()

  _turn = None


def endprolog():

  global _turn

  aplog.log("--- end prolog ---")
  aplog.logbreak()

  _turn = 1

def startturn():

  if turn == None:
    aplog.error("startturn() called before endprolog().")

  aplog.log("--- start of turn %d ---" % _turn)
  aplog.logbreak()

  apaircraft._allstartturn()

def endturn():

  global _turn

  apaircraft._allendturn()

  aplog.log("--- end of turn %d ---" % _turn)
  aplog.logbreak()

  _turn += 1

def turn():
  return _turn

def drawmap():
  apmap.drawmap()
  apaircraft._alldraw()

from airpower.aircraft import aircraft