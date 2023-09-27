"""
Logging for the aircraft class.
"""

import airpower.azimuth as apazimuth
import airpower.hexcode as aphexcode
import airpower.log     as aplog
import airpower.map     as apmap
import airpower.turn    as apturn

def _log(self, s):
  aplog.log("%s: turn %-2d : %s" % (self._name, apturn.turn(), s))

def _logbreak(self):
  aplog.logbreak()

def _logposition(self, s, t):

  if apmap.isonmap(self._x, self._y):
    sheet = apmap.tosheet(self._x, self._y)
    hexcode = aphexcode.fromxy(self._x, self._y)
  else:
    sheet = "--"
    hexcode = "----"
  azimuth = apazimuth.fromfacing(self._facing)
  altitude = self._altitude
  altitudeband = self._altitudeband
  position = "%2s %-9s  %-3s  %2d  %2s" % (sheet, hexcode, azimuth, altitude, altitudeband)

  self._log("%-5s : %-16s : %s" % (s, t, position))

def _logevent(self, s):
  self._log("%-5s : %s" % ("", s))
