import math
import apxo      as ap
import apxo.hex as aphex
import apxo.log as aplog

##############################################################################

def damage(self):

  if self.damageK > 0:
    return "K"

  damage = ""
  if self.damageL == 1:
    damage = "L"
  elif self.damageL == 2:
    damage = "2L"  
  if self.damageH == 1:
    damage = "%sH" % (
      "" if damage == "" else damage + "+",
    )
  if self.damageC == 1:
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
    self.damageL += 1
  elif damage == "2L":
    self.damageL += 2
  elif damage == "H":
    self.damageH += 1
  elif damage == "C":
    self.damageC += 1
  elif damage == "K":
    self.damageK += 1
  else:
    raise RuntimeError("invalid damage %r" % damage)
    
  self._logaction("", "%s takes %s damage." % (self._name, damage))

  if self._destroyed:
    self._logaction("", "%s is already destroyed." % self._name)
    return

  if self.damageL >= 3:
    self.damageL -= 3
    self.damageH += 1

  if self.damageH >= 2:
    self.damageH -= 2
    self.damageC += 1

  if self.damageC >= 2:
    self.damageK = 1

  if self.damageH > 0 and self.damageC > 0:
    self.damageK = 1

  if self.damageK > 0:
    self.damageK = 1
    self.damageL = 0
    self.damageH = 0
    self.damageC = 0
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
    return self.damageL >= 1 or self.damageatleast("2L")
  elif damage == "2L":
    return self.damageL >= 2 or self.damageatleast("H")
  elif damage == "H":
    return self.damageH >= 1 or self.damageatleast("C")
  elif damage == "C":
    return self.damageC >= 1 or self.damageatleast("K")
  elif damage == "K":
    return self.damageK >= 1

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
