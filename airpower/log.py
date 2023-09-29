_donotlog = False

def log(s):
  if _donotlog:
    return
  print(s)

def logbreak():
  if _donotlog:
    return
  print()

_error = None

def clearerror():
  global _error
  _error = None

def logerror(e):
  global _error
  _error = str(e.args[0])
  if _donotlog:
    return
  logbreak()
  log("=== ERROR: %s ===" % _error)
  logbreak()
