"""
Keep track of the game turn.
"""

_activegameturn = None
_gameturn = None
_previousgameturn = None


def gameturn():
    return _gameturn


def startgamesetup():
    global _activegameturn, _gameturn, _previousgameturn
    _previousgameturn = None
    _gameturn = 0
    _activegameturn = _gameturn


def endgamesetup():
    checkingamesetup()
    global _activegameturn, _gameturn, _previousgameturn
    _previousgameturn = _activegameturn
    _activegameturn = None


def startgameturn():
    global _activegameturn, _gameturn, _previousgameturn
    _gameturn = _previousgameturn + 1
    _activegameturn = _gameturn


def endgameturn():
    checkingameturn()
    global _activegameturn, _gameturn, _previousgameturn
    _previousgameturn = _activegameturn
    _activegameturn = None


def checkingamesetup():
    if _activegameturn is None or _activegameturn != 0:
        raise RuntimeError("activity outside of game setup.")


def checkingameturn():
    if _activegameturn is None or _activegameturn == 0:
        raise RuntimeError("activity outside of game turn.")


def checkingamesetuporgameturn():
    if _activegameturn is None:
        raise RuntimeError("activity outside of game setup or turn.")
