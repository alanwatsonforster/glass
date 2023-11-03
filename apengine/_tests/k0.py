from apengine._tests.infrastructure import *
startfile(__file__, "damage")

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "W", 5, 4.0, "CL")

assert A1.damage() == "none"
A1.takedamage("L")
assert A1.damage() == "L"
A1.takedamage("L")
assert A1.damage() == "2L"
A1.takedamage("L")
assert A1.damage() == "H"
A1.takedamage("L")
assert A1.damage() == "L+H"
A1.takedamage("L")
assert A1.damage() == "2L+H"
A1.takedamage("L")
assert A1.damage() == "C"
A1.takedamage("L")
assert A1.damage() == "L+C"
A1.takedamage("L")
assert A1.damage() == "2L+C"
A1.takedamage("L")
assert A1.damage() == "K"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "W", 5, 4.0, "CL")

assert A1.damage() == "none"
A1.takedamage("L")
assert A1.damage() == "L"
A1.takedamage("H")
assert A1.damage() == "L+H"
A1.takedamage("C")
assert A1.damage() == "K"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "W", 5, 4.0, "CL")

assert A1.damage() == "none"
A1.takedamage("H")
assert A1.damage() == "H"
A1.takedamage("H")
assert A1.damage() == "C"
A1.takedamage("C")
assert A1.damage() == "K"

endtestsetup()

endfile(__file__)