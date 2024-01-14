"""
Logging.
"""


import apxo.turn as apturn

_silent = False

def log(s):
  if _silent:
    return
  if apturn.turn() is None:
    print(s)
  elif apturn.turn() == 0:
    print("set-up: %s" % s)
  else:
    print("turn %d: %s" % (apturn.turn(), s))

def logmain(a, s):
  log("%-4s : %s" % (
    a.name() if a is not None else "",
    s
    ))


def logcomment(a, s):
  log("%-4s : %-5s : %-32s : %s" % (
    a.name() if a is not None else "",
    "",
    "",
    s
    ))

def logaction(a, s):
  log("%-4s : %-5s : %s" % (
    a.name() if a is not None else "",
    "",
    s
    ))

def logbreak():
  if _silent:
    return
  print()

def lognote(a, note):

  # This is adapted from the public-domain code in PEP 257.
  def splitandtrim(s):
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = s.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = None
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
          if indent is None:
            indent = len(line) - len(stripped)
          else:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent is not None:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return the lines.
    return trimmed

  if note is not False:
    for line in splitandtrim(note):
      logcomment(a, "- %s" % line)

_error = None

def clearerror():
  global _error
  _error = None

def logexception(e):
  global _error
  _error = str(e.args[0])
  if _silent:
    return
  logbreak()
  log("=== ERROR: %s ===" % _error)
  logbreak()

def plural(i, singular, plural):
  if i == 1:
    return singular
  else:
    return plural