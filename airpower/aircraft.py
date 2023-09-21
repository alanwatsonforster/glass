print("airpower.aircraft")

import airpower.draw     as apdraw
import airpower.altitude as apaltitude
import airpower.azimuth  as apazimuth

class Aircraft:

  def __init__(self, name, x, y, azimuth, altitude):
    self.turn     = 0
    self.name     = name
    self.x        = x
    self.y        = y
    self.facing   = apazimuth.tofacing(azimuth)
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
    apdraw.drawflightpath(lastx, lasty, self.x, self.y)

  def drawbeforeend(self):
    apdraw.drawaircraftbeforeend(self.x, self.y, self.facing, self.name, self.altitude)

  def drawatend(self):
    apdraw.drawaircraftatend(self.x, self.y, self.facing, self.name, self.altitude)

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
    self._report("initial azimuth  = %s." % apazimuth.toazimuth(self.facing))
    self._report("initial altitude = %5.2f (%s)" % (self.altitude, apaltitude.altitudeband(self.altitude)))

    if s != "":
      self.next(s)

  def next(self, s):

    lastx = self.x
    lasty = self.y

    actions = [

      ["H"   , lambda : self._H()],

      ["C¼"  , lambda : self._C(1/4)],
      ["C1/4", lambda : self._C(1/4)],
      ["C½"  , lambda : self._C(1/2)],
      ["C1/2", lambda : self._C(1/2)],
      ["C¾"  , lambda : self._C(3/4)],
      ["C3/4", lambda : self._C(3/4)],
      ["C2"  , lambda : self._C(2)],
      ["C"   , lambda : self._C(1)],

      ["D¼"  , lambda : self._D(1/4)],
      ["D1/4", lambda : self._D(1/4)],
      ["D½"  , lambda : self._D(1/2)],
      ["D1/2", lambda : self._D(1/2)],
      ["D¾"  , lambda : self._D(3/4)],
      ["D3/4", lambda : self._D(3/4)],
      ["D2"  , lambda : self._D(2)],
      ["D"   , lambda : self._D(1)],

      ["L60" , lambda : self._L(60)],
      ["L90" , lambda : self._L(90)],
      ["L"   , lambda : self._L(30)],

      ["R60" , lambda : self._R(60)],
      ["R90" , lambda : self._R(90)],
      ["R"   , lambda : self._R(30)],

    ]
      
    for t in s.split(","):

      self.ifp = self.ifp + 1

      self._reportfp("movement code is %s." % t)

      if t[0] == 'H':
        self.ihfp = self.ihfp + 1
      elif t[0] == 'D' or t[0] == 'C':
        self.ivfp = self.ivfp + 1
      else:
        raise ValueError("movement code must begin with H, D, or C.")

      while t != "":
        for action in actions:
          if action[0] == t[:len(action[0])]:
            action[1]()
            t = t[len(action[0]):]
            break
        else:
          raise ValueError("unknown movement code %s" % t)

      self.drawflightpath(lastx, lasty)
      lastx = self.x
      lasty = self.y

    self._report("%d HFPs and %d VFPs used." % (self.ihfp, self.ivfp))
      
    if self.ifp < self.nfp:

      self._report("%d FPs remaining." % (self.nfp - self.ifp))

      self.drawbeforeend()

    elif self.ifp == self.nfp:

      self._report("all %d FPs used." % (self.nfp))

      self._report("final azimuth    = %s." % apazimuth.toazimuth(self.facing))
      self._report("final altitude   = %5.2f (%s)" % (self.altitude, apaltitude.altitudeband(self.altitude)))
      if apaltitude.altitudeband(self.initialaltitude) != apaltitude.altitudeband(self.altitude):
        self._report("altitude band changed from %s to %s." % (apaltitude.altitudeband(self.initialaltitude), apaltitude.altitudeband(self.altitude)))
      self._report("--- end of turn ---")

      self._save(self.turn)

      self.drawatend()

    else:

      raise ValueError("only %d FPs are available." % self.nfp)
