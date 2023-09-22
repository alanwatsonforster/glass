import airpower.altitude as apaltitude
import airpower.azimuth  as apazimuth
import airpower.draw     as apdraw
import airpower.hex      as aphex
import airpower.hexcode  as aphexcode

import math

class Aircraft:

  def __init__(self, name, hexcode, azimuth, altitude):

    x, y = aphexcode.toxy(hexcode)
    facing = apazimuth.tofacing(azimuth)

    apaltitude._checkaltitude(altitude)
    aphex.checkisvalidfacing(x, y, facing)

    self._turn          = 0
    self._name          = name
    self._x             = x
    self._y             = y
    self._facing        = facing
    self._altitude      = altitude
    self._altitudecarry = 0
    self._destroyed     = False

    self._saved = []
    self._save(0)
  
    self._drawaircraft("end")

  def __str__(self):
    return "%s: %s %02d %s (%+.03f)" % (
      self._name, 
      aphexcode.fromxy(self._x, self._y), 
      self._altitude, 
      apazimuth.toazimuth(self._facing), 
      self._altitudecarry
    )

  def _restore(self, i):
    self._x, self._y, self._facing, self._altitude, self._altitudecarry, self._destroyed = self._saved[i]

  def _save(self, i):
    if len(self._saved) == i:
      self._saved.append(None)
    self._saved[i] = (self._x, self._y, self._facing, self._altitude, self._altitudecarry, self._destroyed)

  def _maxprevturn(self):
    return len(self._saved) - 1

  def _drawflightpath(self, lastx, lasty):
    apdraw.drawflightpath(lastx, lasty, self._x, self._y)

  def _drawaircraft(self, when):
    apdraw.drawaircraft(self._x, self._y, self._facing, self._name, self._altitude, when)
        
  def _position(self):
    return "%s %d %s" % (
        aphexcode.fromxy(self._x, self._y),
        self._altitude,
        apazimuth.toazimuth(self._facing)
      )

  def _report(self, s):
    print("%s: turn %d: %s" % (self._name, self._turn, s))

  def _reportfp(self, s):
    print("%s: turn %d: FP %d of %d: %s" % (self._name, self._turn, self._ifp, self._nfp, s))

  def _reportposition(self, s):
      self._reportfp("%-16s : %s" % (s, self._position()))

  def _reportactionandposition(self, action):
    self._reportposition(action)

  def _reportstatus(self, when):

    if when != "start":
       self._report("%d HFPs and %d VFPs used." % (self._ihfp, self._ivfp))

    altitudeband = apaltitude._altitudeband(self._altitude)

    if when == "start":
      self._reportposition("")

    if when != "start":
      self._report("altitude carry is %s." % apaltitude._formataltitudecarry(self._altitudecarry))

    if when == "start":
      self._initialaltitudeband = altitudeband
    elif when == "end":
      if altitudeband!= self._initialaltitudeband:
        self._report("altitude band changed from %s to %s." % (self._initialaltitudeband, altitudeband))

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
    self._altitude, self._altitudecarry = apaltitude._adjustaltitude(self._altitude, self._altitudecarry, -altitudechange)

  def _C(self, altitudechange):
    self._altitude, self._altitudecarry = apaltitude._adjustaltitude(self._altitude, self._altitudecarry, +altitudechange)

  def _K(self):
    self._reportfp("killed.")
    self._destroyed = True

  def _A(self, what):
    self._reportfp("attack with %s." % what)

  def checkforterraincollision(self):
    altitudeofterrain = apaltitude._altitudeofterrain()
    if self._altitude <= altitudeofterrain:
      self._altitude = altitudeofterrain
      self._altitudecarry = 0
      self._reportfp("collided with terrain at altitude %d." % altitudeofterrain)
      self._destroyed = True
  
  def start(self, turn, nfp, actions):

    if turn > self._maxprevturn() + 1:
      raise ValueError("turn %d is out of sequence." % turn)

    self._turn = turn
    self._nfp = nfp
    self._ifp = 0
    self._ihfp = 0
    self._ivfp = 0
    self._restore(turn - 1)

    self._report("--- start of turn ---")

    if self._destroyed:
        self._report("aircraft has been destroyed.")
        self._report("--- end of turn ---")
        self._save(self._turn)
        return
 
    self._reportstatus("start")

    if actions != "":
      self.next(actions)

  def next(self, actions):

    elements = [

      # This table is searched in order, so put longer elements before shorter 
      # ones that are prefixes (e.g., put C2 before C and D3/4 before D3).

      # [0] is the element code.
      # [1] is the procedure for movement elements.
      # [2] is the procedure for other (non-movement) elements.

      ["H"   , lambda : self._H()   , lambda : None],

      ["C⅛"  , lambda : self._C(1/8), lambda : None],
      ["C1/8", lambda : self._C(1/8), lambda : None],
      ["C¼"  , lambda : self._C(1/4), lambda : None],
      ["C1/4", lambda : self._C(1/4), lambda : None],
      ["C⅜"  , lambda : self._C(3/8), lambda : None],
      ["C3/8", lambda : self._C(3/8), lambda : None],
      ["C½"  , lambda : self._C(1/2), lambda : None],
      ["C1/2", lambda : self._C(1/2), lambda : None],
      ["C⅝"  , lambda : self._C(5/8), lambda : None],
      ["C5/8", lambda : self._C(5/8), lambda : None],
      ["C¾"  , lambda : self._C(3/4), lambda : None],
      ["C3/4", lambda : self._C(3/4), lambda : None],
      ["C⅞"  , lambda : self._C(7/8), lambda : None],
      ["C7/8", lambda : self._C(7/8), lambda : None],
      ["CC"  , lambda : self._C(2)  , lambda : None],
      ["C2"  , lambda : self._C(2)  , lambda : None],
      ["C"   , lambda : self._C(1)  , lambda : None],
      ["C1"  , lambda : self._C(1)  , lambda : None],

      ["D⅛"  , lambda : self._D(1/8), lambda : None],
      ["D1/8", lambda : self._D(1/8), lambda : None],
      ["D¼"  , lambda : self._D(1/4), lambda : None],
      ["D1/4", lambda : self._D(1/4), lambda : None],
      ["D⅜"  , lambda : self._D(3/8), lambda : None],
      ["D3/8", lambda : self._D(3/8), lambda : None],
      ["D½"  , lambda : self._D(1/2), lambda : None],
      ["D1/2", lambda : self._D(1/2), lambda : None],
      ["D⅝"  , lambda : self._D(5/8), lambda : None],
      ["D5/8", lambda : self._D(5/8), lambda : None],
      ["D¾"  , lambda : self._D(3/4), lambda : None],
      ["D3/4", lambda : self._D(3/4), lambda : None],
      ["D⅞"  , lambda : self._D(7/8), lambda : None],
      ["D7/8", lambda : self._D(7/8), lambda : None],
      ["DDD" , lambda : self._D(3)  , lambda : None],
      ["D3"  , lambda : self._D(3)  , lambda : None],
      ["DD"  , lambda : self._D(2)  , lambda : None],
      ["D2"  , lambda : self._D(2)  , lambda : None],
      ["D"   , lambda : self._D(1)  , lambda : None],
      ["D1"  , lambda : self._D(1)  , lambda : None],

      ["LLL" , lambda : self._L(90) , lambda : None],
      ["L90" , lambda : self._L(90) , lambda : None],
      ["LL"  , lambda : self._L(60) , lambda : None],
      ["L60" , lambda : self._L(60) , lambda : None],
      ["L"   , lambda : self._L(30) , lambda : None],
      ["L30" , lambda : self._L(30) , lambda : None],

      ["RRR" , lambda : self._R(90) , lambda : None],
      ["R90" , lambda : self._R(90) , lambda : None],
      ["RR"  , lambda : self._R(60) , lambda : None],
      ["R60" , lambda : self._R(60) , lambda : None],
      ["R"   , lambda : self._R(30) , lambda : None],
      ["R30" , lambda : self._R(30) , lambda : None],

      ["K"   , lambda : None        , lambda : self._K()],

      ["AGN" , lambda : None        , lambda : self._A("guns")],
      ["AGP" , lambda : None        , lambda : self._A("gun pod")],
      ["ARK" , lambda : None        , lambda : self._A("rockets")],
      ["ARP" , lambda : None        , lambda : self._A("rocket pods")],

      ["/"   , lambda : None        , lambda : None]

    ]

    if self._destroyed:
      return

    for action in actions.split(","):

      self._ifp = self._ifp + 1

      if self._ifp > self._nfp:
        raise ValueError("only %d FPs are available." % self._nfp)

      if action[0] == 'H':
        self._ihfp = self._ihfp + 1
      elif action[0] == 'D' or action[0] == 'C':
        self._ivfp = self._ivfp + 1
      else:
        raise ValueError("action %s does not begin with H, D, or C." % action)

      lastx = self._x
      lasty = self._y

      # Execute movement elements.
      a = action
      while a != "":
        for element in elements:
          if element[0] == a[:len(element[0])]:
            element[1]()
            a = a[len(element[0]):]
            break
        else:
          raise ValueError("unknown element %s in action %s." % (a, action))

      self._reportactionandposition(action)
      self._drawflightpath(lastx, lasty)

      self.checkforterraincollision()
      if self._destroyed:
        self._report("aircraft has been destroyed.")
        break

      # Execute other elements.
      a = action
      while a != "":
        for element in elements:
          if element[0] == a[:len(element[0])]:
            element[2]()
            a = a[len(element[0]):]
            break
        else:
          raise ValueError("unknown element %s in action %s." % (a, action))

      if self._destroyed:
        self._report("aircraft has been destroyed.")
        break

    assert self._ifp <= self._nfp
    aphex.checkiscenteroredge(self._x, self._y)
    aphex.checkisvalidfacing(self._x, self._y, self._facing)
    apaltitude._checkaltitude(self._altitude)

    if self._ifp == self._nfp:

      self._reportstatus("end")
      self._drawaircraft("end")
      self._save(self._turn)
      self._report("--- end of turn ---")
      
    else:
      
      self._reportstatus("next")
      self._drawaircraft("next")
