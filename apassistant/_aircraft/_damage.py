import math
import apengine      as ap
import apengine._hex as aphex
import apengine._log as aplog

##############################################################################

def damage(self):

  if self._damageK > 0:
    return "K"

  damage = ""
  if self._damageL == 1:
    damage = "L"
  elif self._damageL == 2:
    damage = "2L"  
  if self._damageH == 1:
    damage = "%sH" % (
      "" if damage == "" else damage + "+",
    )
  if self._damageC == 1:
    damage = "%sC" % (
      "" if damage == "" else damage + "+"
    )

  if damage == "":
    return "none"
  else:
    return damage

def takedamage(self, damage, note=False):


  aplog.clearerror()
  try:

    self._takedamage(damage)

    self._lognote(note)
    self._logline()

  except RuntimeError as e:
    aplog.logexception(e)

def _takedamage(self, damage):

  previousdamage = self.damage()

  if damage == "L":
    self._damageL += 1
  elif damage == "2L":
    self._damageL += 2
  elif damage == "H":
    self._damageH += 1
  elif damage == "C":
    self._damageC += 1
  elif damage == "K":
    self._damageK += 1
  else:
    raise RuntimeError("invalid damage %r" % damage)
    
  self._logaction("", "%s takes %s damage." % (self._name, damage))

  if self._destroyed:
    self._logaction("", "%s is already destroyed." % self._name)
    return

  if self._damageL >= 3:
    self._damageL -= 3
    self._damageH += 1

  if self._damageH >= 2:
    self._damageH -= 2
    self._damageC += 1

  if self._damageC >= 2:
    self._damageK = 1

  if self._damageH > 0 and self._damageC > 0:
    self._damageK = 1

  if self._damageK > 0:
    self._damageK = 1
    self._damageL = 0
    self._damageH = 0
    self._damageC = 0
    self._destroyed = True

  self._logaction("", "%s damage changed from %s to %s." % (self._name, previousdamage, self.damage()
  ))
  if self._destroyed:
    self._logaction("", "%s is destroyed." % self._name)

def damageatleast(self, damage):
  assert damage in ["none", "L", "2L", "H", "C", "K"]
  if damage == "none":
    return True
  elif damage == "L":
    return self._damageL >= 1 or self.damageatleast("2L")
  elif damage == "2L":
    return self._damageL >= 2 or self.damageatleast("H")
  elif damage == "H":
    return self._damageH >= 1 or self.damageatleast("C")
  elif damage == "C":
    return self._damageC >= 1 or self.damageatleast("K")
  elif damage == "K":
    return self._damageK >= 1

def damageatmost(self, damage):
  assert damage in ["none", "L", "2L", "H", "C", "K"]
  if damage == "none":
    return not self.damageatleast("L")
  elif damage == "L":
    return not self.damageatleast("2L")
  elif damage == "2L":
    return not self.damageatleast("H")
  elif damage == "H":
    return not self.damageatleast("C")
  elif damage == "C":
    return not self.damageatleast("K")
  elif damage == "K":
    return True
