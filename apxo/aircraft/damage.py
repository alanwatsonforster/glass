import apxo.damage as apdamage

################################################################################

def _takedamage(self, damage):
    apdamage.takedamage(self, damage)

def _takedamageconsequences(self):
    apdamage.takedamageconsequences(self)

def damage(self):
    return apdamage.damage(self)

def damageatleast(self, damage):
    return apdamage.damageatleast(self, damage)

def damageatmost(self, damage):
    return apdamageatmost(self, damage)

################################################################################
