import airpower.map as apmap

_turn = None
_maxturn = 0

def restart():
  global _turn
  _turn = 1

def startturn(turn):
  global _turn
  global _maxturn
  if not isinstance(turn, int) or turn < 1:
    raise ValueError("invalid turn %d." % turn)
  if turn > _maxturn + 1:
    raise ValueError("attempt to start turn %d out of sequence." % turn)
  _turn = turn
  _maxturn = max(_maxturn, _turn)
  print("--- start of turn %d ---" % _turn)
  print("")
  apmap.drawmap()

def endturn():
  global _turn
  print("--- end of turn %d ---" % _turn)
  print("")
  _turn = None

def turn():
  return _turn

def restart():
  global _turn
  global _maxturn
  _turn = None
  _maxturn = 0
