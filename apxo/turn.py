"""
Keep track of the game turn.
"""

_activeturn   = None
_turn         = None
_previousturn = None

def turn():
  return _turn

def startsetup():
  global _activeturn, _turn, _previousturn
  _previousturn = None
  _turn         = 0
  _activeturn   = _turn

def endsetup():
  checkinsetup()
  global _activeturn, _turn, _previousturn
  _previousturn = _activeturn
  _activeturn   = None

def startturn():
  global _activeturn, _turn, _previousturn
  _turn       = _previousturn + 1
  _activeturn = _turn

def endturn():
  checkinturn()
  global _activeturn, _turn, _previousturn
  _previousturn = _activeturn
  _activeturn   = None

def checkinsetup():
  if _activeturn is None or _activeturn != 0:
    raise RuntimeError("activity outside of setup.")

def checkinturn():
  if _activeturn is None or _activeturn == 0:
    raise RuntimeError("activity outside of turn.")

def checkinsetuporturn():
  if _activeturn is None:
    raise RuntimeError("activity outside of setup or turn.")
