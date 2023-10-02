import airpower.aircraft as apaircraft
import airpower.log as aplog

_turn = None

def restart():
  global _turn
  _turn = 0

def startturn():
  global _turn
  _turn += 1
  aplog.log("--- start of turn %d ---" % _turn)
  aplog.logbreak()
  apaircraft._allstartturn()

def endturn():
  apaircraft._allendturn()
  global _turn
  aplog.log("--- end of turn %d ---" % _turn)
  aplog.logbreak()

def turn():
  return _turn
