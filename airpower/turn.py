import airpower.aircraft as apaircraft
import airpower.log as aplog

_turn = None
_maxturn = 0

def restart():
  global _turn
  _turn = 1

def startturn(turn):
  global _turn
  global _maxturn
  if not isinstance(turn, int) or turn < 1:
    raise RuntimeError("invalid turn %d." % turn)
  if turn > _maxturn + 1:
    raise RuntimeError("attempt to start turn %d out of sequence." % turn)
  _turn = turn
  _maxturn = max(_maxturn, _turn)
  aplog.log("--- start of turn %d ---" % _turn)
  aplog.logbreak()
  apaircraft._allstartturn()

def endturn():
  apaircraft._allendturn()
  global _turn
  aplog.log("--- end of turn %d ---" % _turn)
  aplog.logbreak()
  _turn = None

def turn():
  return _turn

def restart():
  global _turn
  global _maxturn
  _turn = None
  _maxturn = 0
