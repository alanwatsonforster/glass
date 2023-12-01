"""
Keep track of the game turn.
"""

# Turn is None in outside of setup and turns, 0 in setup, and 1 or more in turns.

_turn = None

# _savedturn holds the value of _turn outside of startsetup/endsetup and
# startturn/endturn.

_savedturn = None

def turn():
  return _turn

def startsetup():
  global _turn, _savedturn
  _turn = 0

def endsetup():
  checkinsetup()
  global _turn, _savedturn
  _turn = None
  _savedturn = 0

def startturn():
  global _turn, _savedturn
  _turn = _savedturn + 1

def endturn():
  checkinturn()
  global _turn, _savedturn
  _savedturn = _turn
  _turn = None

def checkinsetup():
  if _turn is None or _turn != 0:
    raise RuntimeError("activity outside of setup.")

def checkinturn():
  if _turn is None or _turn == 0:
    raise RuntimeError("activity outside of turn.")
