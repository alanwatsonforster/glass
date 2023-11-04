"""
Logging for the aircraft class.
"""

import apengine      as ap
import apengine._log as aplog

def _log(self, s):
  aplog.log("%s: turn %-2d : %s" % (self._name, ap.turn(), s))

def _logbreak(self):
  aplog.logbreak()

def _logaction(self, s, t, u):
  self._log("%-5s : %-16s : %s" % (s, t, u))

def _logevent(self, s):
  self._log("%-5s : %s" % ("", s))

def _logstart(self, s):
  self._log("%-5s : %s" % ("start", s))

def _logend(self, s):
  self._log("%-5s : %s" % ("end", s))

def _logline(self):
  self._log("%-5s :" % "-----")  

def _lognote(self, note):

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
      self._log("note  : -- %s" % line)
