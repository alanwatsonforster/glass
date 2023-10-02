"""
Logging for the aircraft class.
"""

import airpower.azimuth as apazimuth
import airpower.hexcode as aphexcode
import airpower.log     as aplog
import airpower.map     as apmap
import airpower         as ap

def _log(self, s):
  aplog.log("%s: turn %-2d : %s" % (self._name, ap.turn(), s))

def _logbreak(self):
  aplog.logbreak()

def _logposition(self, s, t):

  self._log("%-5s : %-16s : %s" % (s, t, self.position()))

def _logevent(self, s):
  self._log("%-5s : %s" % ("", s))
