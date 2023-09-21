print("airpower")

from airpower.draw import *

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
matplotlib.rcParams['figure.figsize'] = [7.5, 10]
plt.rcParams.update({'font.size': 10})

northfacing = 90

def tofacing(azimuth):
  named = {
    "N":   0, "NNE":  30, "ENE":  60,
    "E":  90, "ESE": 120, "SSE": 150, 
    "S": 180, "SSW": 210, "WSW": 240, 
    "W": 270, "WNW": 300, "NNW": 330, 
  }
  superseded = {
    "NE": "ENE", "SE": "ESE", "SW": "WSW", "NW": "WNW"
  }
  if azimuth in named:
    azimuth = named[azimuth]
  elif azimuth in superseded:
    raise ValueError("use azimuth \"%s\" instead of \"%s\"" % (superseded[azimuth], azimuth))
  return (northfacing - azimuth) % 360

def toazimuth(facing):
  print(facing)
  print(northfacing)
  azimuth = (northfacing - facing) % 360
  print(azimuth)
  print(azimuth // 30)
  if azimuth % 30 == 0:
    named = ["N", "NNE", "ENE", "E", "ESE", "SSE", "S", "SSW", "WSW", "W", "WNW", "NNW"]
    return named[azimuth // 30]
  else:
    return azimuth

def altitudeband(altitude):
  if altitude <= 7:
    return "LO"
  elif altitude <= 16:
    return "ML"
  elif altitude <= 25:
    return "MH"
  elif altitude <= 35:
    return "HI"
  elif altitude <= 45:
    return "VH"
  elif altitude <= 60:
    return "EH"
  else:
    return "UH"

class Aircraft:

  def __init__(self, name, x, y, azimuth, altitude):
    self.turn     = 0
    self.name     = name
    self.x        = x
    self.y        = y
    self.facing   = tofacing(azimuth)
    self.altitude = altitude
    self.saved = []
    self._save(0)
    self.drawatend()

  def __str__(self):
    return "%s: (%.2f,%.2f) %03d %s %02d" % (self.name, self.x, self.y, self.facing, fromfacing(self.facing), self.altitude)

  def _restore(self, i):
    self.x, self.y, self.facing, self.altitude = self.saved[i]

  def _save(self, i):
    if len(self.saved) == i:
      self.saved.append(None)
    self.saved[i] = (self.x, self.y, self.facing, self.altitude)

  def _maxprevturn(self):
    return len(self.saved) - 1

  def drawflightpath(self, lastx, lasty):
    drawlineinhex(lastx, lasty, self.x, self.y, color="lightgrey", linestyle="dashed", zorder=0.5)

  def drawbeforeend(self):
    drawdartinhex(self.x, self.y, self.facing, dy=-0.02, size=0.5, color="grey")
    drawtextinhex(self.x, self.y, self.facing, self.name, dx=-0.3, dy=0.0, size=7, color="grey")
    drawtextinhex(self.x, self.y, self.facing, "%2d" % self.altitude, dx=+0.3, dy=0.0, size=7, color="grey")

  def drawatend(self):
    drawdartinhex(self.x, self.y, self.facing, dy=-0.02, size=0.5)
    drawtextinhex(self.x, self.y, self.facing, self.name, dx=-0.3, dy=0.0, size=7)
    drawtextinhex(self.x, self.y, self.facing, "%2d" % self.altitude, dx=+0.3, dy=0.0, size=7)

  def _H(self):
    dx = {
          0: +1.00,
         30: +1.00,
         60: +0.50,
         90: +0.00,
        120: -0.50,
        150: -1.00,
        180: -1.00,
        210: -1.00,
        240: -0.50,
        270: -0.00,
        300: +0.50,
        330: +1.00
    }
    dy = {
          0: +0.00,
         30: +0.50,
         60: +0.75,
         90: +1.00,
        120: +0.75,
        150: +0.50,
        180: +0.00,
        210: -0.50,
        240: -0.75,
        270: -1.00,
        300: -0.75,
        330: -0.50
    }
    self.x += dx[self.facing]
    self.y += dy[self.facing]

  def onedge(self):
    if self.x % 1 != 0:
      return True
    elif self.x % 2 == 0 and self.y % 1 == 0.5:
      return True
    elif self.x % 2 == 1 and self.y % 1 == 0.0:
      return True
    else:
      return False

  def _R(self, pointingchange):
    if self.onedge():
      if self.facing == 0:
        self.y -= 0.5
      elif self.facing == 60:
        self.x += 0.50
        self.y -= 0.25
      elif self.facing == 120:
        self.x += 0.50
        self.y += 0.25
      elif self.facing == 180:
        self.y += 0.5
      elif self.facing == 240:
        self.x -= 0.50
        self.y += 0.25
      elif self.facing == 300:
        self.x -= 0.50
        self.y -= 0.25
    self.facing = (self.facing + 360 - pointingchange) % 360

  def _L(self, pointingchange):
    if self.onedge():
      if self.facing == 0:
        self.y += 0.5
      elif self.facing == 60:
        self.x -= 0.50
        self.y += 0.25
      elif self.facing == 120:
        self.x -= 0.50
        self.y -= 0.25
      elif self.facing == 180:
        self.y -= 0.5
      elif self.facing == 240:
        self.x += 0.50
        self.y -= 0.25
      elif self.facing == 300:
        self.x += 0.50
        self.y += 0.25
    self.facing = (self.facing + pointingchange) % 360

  def _D(self, altitudechange):
    self.altitude -= altitudechange

  def _C(self, altitudechange):
    self.altitude += altitudechange

  def _report(self, s):
    print("%s: turn %d: %s" % (self.name, self.turn, s))

  def _reportfp(self, s):
    print("%s: turn %d: FP %d: %s" % (self.name, self.turn, self.ifp, s))

  def start(self, turn, nfp, s):

    if turn > self._maxprevturn() + 1:
      raise ValueError("turn %d is out of sequence." % turn)

    self.turn = turn
    self.nfp = nfp
    self.ifp = 0
    self.ihfp = 0
    self.ivfp = 0
    self._restore(turn - 1)

    self.initialaltitude = self.altitude

    self._report("--- start of turn ---")
    self._report("%d FPs available." % self.nfp)
    self._report("initial azimuth  = %s." % toazimuth(self.facing))
    self._report("initial altitude = %5.2f (%s)" % (self.altitude, altitudeband(self.altitude)))

    if s != "":
      self.next(s)

  def next(self, s):

    lastx = self.x
    lasty = self.y
    altitudechange = 1

    for t in s.split(","):

      self.ifp = self.ifp + 1

      self._reportfp("movement code is %s." % t)

      if t[0] == 'H':
        self.ihfp = self.ihfp + 1
      elif t[0] == 'D' or t[0] == 'C':
        self.ivfp = self.ivfp + 1
      else:
        raise ValueError("movement code must begin with H, D, or C.")

      for c in t:
        if c == 'H':
          self._H()
        elif c == 'C':
          self._C(altitudechange)
          altitudechange = 1
        elif c == 'D':
          self._D(altitudechange)
          altitudechange = 1
        elif c == '¼':
          altitudechange = 1/4
        elif c == '½':
          altitudechange = 1/2
        elif c == '¾':
          altitudechange = 3/4
        elif c == 'L':
          self._L(30)
        elif c == 'R':
          self._R(30)
        else:
          raise ValueError("unknown movement code %s" % c)

      self.drawflightpath(lastx, lasty)
      lastx = self.x
      lasty = self.y

    self._reportfp("%d HFPs and %d VFPs used." % (self.ihfp, self.ivfp))
      
    if self.ifp < self.nfp:

      self._reportfp("%d FPs remaining." % (self.nfp - self.ifp))

      self.drawbeforeend()

    elif self.ifp == self.nfp:

      self._report("all %d FPs used." % (self.nfp))

      self._report("final azimuth    = %s." % toazimuth(self.facing))
      self._report("final altitude   = %5.2f (%s)" % (self.altitude, altitudeband(self.altitude)))
      if altitudeband(self.initialaltitude) != altitudeband(self.altitude):
        self._report("altitude band changed from %s to %s." % (altitudeband(self.initialaltitude), altitudeband(self.altitude)))
      self._report("--- end of turn ---")

      self._save(self.turn)

      self.drawatend()

    else:

      raise ValueError("only %d FPs are available." % self.nfp)
