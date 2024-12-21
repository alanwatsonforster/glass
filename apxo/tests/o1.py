from apxo.tests.infrastructure import *

startfile(__file__, "ground unit damage")

# Damage
starttestsetup()

A0 = groundunit("A0", "A1-2110", "infantry")
A1 = groundunit("A1", "A1-2110", "infantry")
A2 = groundunit("A2", "A1-2110", "infantry")

assert A0.damage() == ""
assert A1.damage() == ""
assert A2.damage() == ""

A0.takedamage("D")
A1.takedamage("2D")
A2.takedamage("K")

assert A0.damage() == "D+S"
assert A1.damage() == "2D+S"
assert A2.damage() == "K"

assert A0.damageatleast("")
assert A0.damageatleast("D")
assert not A0.damageatleast("2D")
assert not A0.damageatleast("K")

assert not A0.damageatmost("")
assert A0.damageatmost("D")
assert A0.damageatmost("2D")
assert A0.damageatmost("K")

A0.takedamage("D")
A1.takedamage("D")
A2.takedamage("D")

assert A0.damage() == "2D+S"
assert A1.damage() == "K"
assert A2.damage() == "K"

assert A0.damageatleast("")
assert A0.damageatleast("D")
assert A0.damageatleast("2D")
assert not A0.damageatleast("K")

assert not A0.damageatmost("")
assert not A0.damageatmost("D")
assert A0.damageatmost("2D")
assert A0.damageatmost("K")

A0.takedamage("2D")
A1.takedamage("2D")
A2.takedamage("2D")

assert A0.damage() == "K"
assert A1.damage() == "K"
assert A2.damage() == "K"

assert A0.damageatleast("")
assert A0.damageatleast("D")
assert A0.damageatleast("2D")
assert A0.damageatleast("K")

assert not A0.damageatmost("")
assert not A0.damageatmost("D")
assert not A0.damageatmost("2D")
assert A0.damageatmost("K")

endtestsetup()

endfile(__file__)
