print("airpower.aircraft")

import airpower.draw     as apdraw
import airpower.altitude as apaltitude
import airpower.azimuth  as apazimuth

class Aircraft:

  def __init__(self, name, x, y, azimuth, altitude):

    self._turn     = 0
    self._name     = name
    self._x        = x
    self._y        = y
    self._facing   = apazimuth.tofacing(azimuth)
    self._altitude = altitude
    self._saved = []

    self._save(0)
    self._drawatend()

  def __str__(self):
    return "%s: (%.2f,%.2f) %s %02d" % (self._name, self._x, self._y, apazimuth.toazimuth(self._facing), self._altitude)

  def _restore(self, i):
    self._x, self._y, self._facing, self._altitude = self._saved[i]

  def _save(self, i):
    if len(self._saved) == i:
      self._saved.append(None)
    self._saved[i] = (self._x, self._y, self._facing, self._altitude)

  def _maxprevturn(self):
    return len(self._saved) - 1

  def _drawflightpath(self, lastx, lasty):
    apdraw.drawflightpath(lastx, lasty, self._x, self._y)

  def _drawbeforeend(self):
    apdraw.drawaircraftbeforeend(self._x, self._y, self._facing, self._name, self._altitude)

  def _drawatend(self):
    apdraw.drawaircraftatend(self._x, self._y, self._facing, self._name, self._altitude)

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
    self._x += dx[self._facing]
    self._y += dy[self._facing]

  def _onedge(self):
    if self._x % 1 != 0:
      return True
    elif self._x % 2 == 0 and self._y % 1 == 0.5:
      return True
    elif self._x % 2 == 1 and self._y % 1 == 0.0:
      return True
    else:
      return False

  def _R(self, facingchange):
    if self._onedge():
      if self._facing == 0:
        self._y -= 0.5
      elif self._facing == 60:
        self._x += 0.50
        self._y -= 0.25
      elif self._facing == 120:
        self._x += 0.50
        self._y += 0.25
      elif self._facing == 180:
        self._y += 0.5
      elif self._facing == 240:
        self._x -= 0.50
        self._y += 0.25
      elif self._facing == 300:
        self._x -= 0.50
        self._y -= 0.25
    self._facing = (self._facing - facingchange) % 360

  def _L(self, facingchange):
    if self._onedge():
      if self._facing == 0:
        self._y += 0.5
      elif self._facing == 60:
        self._x -= 0.50
        self._y += 0.25
      elif self._facing == 120:
        self._x -= 0.50
        self._y -= 0.25
      elif self._facing == 180:
        self._y -= 0.5
      elif self._facing == 240:
        self._x += 0.50
        self._y -= 0.25
      elif self._facing == 300:
        self._x += 0.50
        self._y += 0.25
    self._facing = (self._facing + facingchange) % 360

  def _D(self, altitudechange):
    self._altitude -= altitudechange

  def _C(self, altitudechange):
    self._altitude += altitudechange

  def _report(self, s):
    print("%s: turn %d: %s" % (self._name, self._turn, s))

  def _reportfp(self, s):
    print("%s: turn %d: FP %d: %s" % (self._name, self._turn, self._ifp, s))

  def start(self, turn, nfp, s):

    if turn > self._maxprevturn() + 1:
      raise ValueError("turn %d is out of sequence." % turn)

    self._turn = turn
    self._nfp = nfp
    self._ifp = 0
    self._ihfp = 0
    self._ivfp = 0
    self._restore(turn - 1)

    self._initialaltitude = self._altitude

    self._report("--- start of turn ---")
    self._report("%d FPs available." % self._nfp)
    self._report("initial azimuth  = %s." % apazimuth.toazimuth(self._facing))
    self._report("initial altitude = %5.2f (%s)" % (self._altitude, apaltitude.altitudeband(self._altitude)))

    if s != "":
      self.next(s)

  def next(self, s):

    lastx = self._x
    lasty = self._y

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

      self._ifp = self._ifp + 1

      self._reportfp("movement code is %s." % t)

      if t[0] == 'H':
        self._ihfp = self._ihfp + 1
      elif t[0] == 'D' or t[0] == 'C':
        self._ivfp = self._ivfp + 1
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

      self._drawflightpath(lastx, lasty)
      lastx = self._x
      lasty = self._y

    self._report("%d HFPs and %d VFPs used." % (self._ihfp, self._ivfp))
      
    if self._ifp < self._nfp:

      self._report("%d FPs remaining." % (self._nfp - self._ifp))

      self._drawbeforeend()

    elif self._ifp == self._nfp:

      self._report("all %d FPs used." % (self._nfp))

      self._report("final azimuth    = %s." % apazimuth.toazimuth(self._facing))
      self._report("final altitude   = %5.2f (%s)" % (self._altitude, apaltitude.altitudeband(self._altitude)))
      if apaltitude.altitudeband(self._initialaltitude) != apaltitude.altitudeband(self._altitude):
        self._report("altitude band changed from %s to %s." % (apaltitude.altitudeband(self._initialaltitude), apaltitude.altitudeband(self._altitude)))
      self._report("--- end of turn ---")

      self._save(self._turn)

      self._drawatend()

    else:

      raise ValueError("only %d FPs are available." % self._nfp)
