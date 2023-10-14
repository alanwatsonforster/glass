"""
Logging for the aircraft class.
"""

import apengine.log     as aplog
import apengine         as ap

def _log(self, s):
  aplog.log("%s: turn %-2d : %s" % (self._name, ap.turn(), s))

def _logbreak(self):
  aplog.logbreak()

def _logaction(self, s, t, u):
  self._log("%-5s : %-16s : %s" % (s, t, u))

def _logevent(self, s):
  self._log("%-5s : %s" % ("", s))
