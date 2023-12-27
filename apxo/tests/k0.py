from apxo.tests.infrastructure import *
startfile(__file__, "damage")

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "W", 5, 4.0, "CL")

assert A1.damage() == "none"
assert not A1.damageatleast("L")
assert not A1.damageatleast("2L")
assert not A1.damageatleast("H")
assert not A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "L"
assert A1.damageatleast("L")
assert not A1.damageatleast("2L")
assert not A1.damageatleast("H")
assert not A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "2L"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert not A1.damageatleast("H")
assert not A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "H"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert not A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "L+H"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert not A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "2L+H"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert not A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "C"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "L+C"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "2L+C"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert A1.damageatleast("C")
assert not A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "K"
assert A1.damageatleast("L")
assert A1.damageatleast("2L")
assert A1.damageatleast("H")
assert A1.damageatleast("C")
assert A1.damageatleast("K")

A1.takedamage("L")
assert A1.damage() == "K"

A1.takedamage("2L")
assert A1.damage() == "K"

A1.takedamage("H")
assert A1.damage() == "K"

A1.takedamage("C")
assert A1.damage() == "K"

A1.takedamage("K")
assert A1.damage() == "K"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "W", 5, 4.0, "CL")

assert A1.damage() == "none"
A1.takedamage("L")
assert A1.damage() == "L"
A1.takedamage("H")
assert A1.damage() == "L+H"
A1.takedamage("C")
assert A1.damage() == "K"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "W", 5, 4.0, "CL")

assert A1.damage() == "none"
A1.takedamage("H")
assert A1.damage() == "H"
A1.takedamage("H")
assert A1.damage() == "C"
A1.takedamage("C")
assert A1.damage() == "K"

endtestsetup()

endfile(__file__)