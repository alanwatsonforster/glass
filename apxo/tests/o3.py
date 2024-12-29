from apxo.tests.infrastructure import *

startfile(__file__, "ground unit plotted fire")

starttestsetup()

G0 = groundunit(
    "G0", "A1-2120", symbols="infantry", aaaclass="B", aaamaximumrelativealtitude=2
)
G1 = groundunit(
    "G1", "A1-2120", symbols="infantry", aaaclass="B", aaamaximumrelativealtitude=2
)
G2 = groundunit(
    "G2", "A1-2120", symbols="armor", aaaclass="B", aaamaximumrelativealtitude=3
)
G3 = groundunit("G3", "A1-2120", symbols="artillery")
G4 = groundunit(
    "G4",
    "A1-2120",
    symbols="airdefense/gun",
    aaaclass="L",
    aaamaximumrelativealtitude=9,
)
G5 = groundunit(
    "G5",
    "A1-2120",
    symbols="airdefense/gun",
    aaaclass="M",
    aaamaximumrelativealtitude=18,
)
G6 = groundunit(
    "G6",
    "A1-2120",
    symbols="airdefense/gun",
    aaaclass="H",
    aaamaximumrelativealtitude=27,
    azimuth="N",
)

A0 = aircraft("A0", "USAF", "F-100A", "A1-2110", "E", 2, 3)
A1 = aircraft("A1", "USAF", "F-100A", "A1-2110", "E", 6, 3)
A2 = aircraft("A2", "USAF", "F-100A", "A1-2111", "E", 2, 3)
A3 = aircraft("A3", "USAF", "F-100A", "A1-2112", "E", 2, 3)

endtestsetup()

startgameturn()

assert not G0.isusingplottedfire()
assert not G1.isusingplottedfire()
assert not G2.isusingplottedfire()
assert not G3.isusingplottedfire()
assert not G4.isusingplottedfire()
assert not G5.isusingplottedfire()
assert not G6.isusingplottedfire()

G0.takedamage("S")
G0.useplottedfire("A1-2110", 3)
asserterror("G0 is suppressed.")

G1.useplottedfire("A1-2110", 3)
asserterror("G1 is not capable of plotted fire.")

G2.useplottedfire("A1-2110", 3)
asserterror("G2 is not capable of plotted fire.")

G3.useplottedfire("A1-2110", 3)
asserterror("G3 is not capable of plotted fire.")

G4.useplottedfire("A1-2110", 3)
asserterror("G4 is not capable of plotted fire.")

G5.useplottedfire("A1-2110", 3)
assert G5.isusingplottedfire()

G6.useplottedfire("A1-2110", 3)
assert G6.isusingplottedfire()

assert not G0.isusingplottedfire()
assert not G1.isusingplottedfire()
assert not G2.isusingplottedfire()
assert not G3.isusingplottedfire()
assert not G4.isusingplottedfire()
assert G5.isusingplottedfire()
assert G6.isusingplottedfire()

G5.attack(A0, "L")
assert A0.damage() == "L"
G6.attack(A0, "L")
assert A0.damage() == "2L"

G5.attack(A1, "L")
asserterror("target is above the plotted fire.")
assert A1.damage() == ""
G6.attack(A1, "L")
asserterror("target is above the plotted fire.")
assert A1.damage() == ""

G5.attack(A2, "L")
assert A2.damage() == "L"
G6.attack(A2, "L")
assert A2.damage() == "2L"

G5.attack(A3, "L")
asserterror("target is outside the plotted fire zone.")
assert A3.damage() == ""
G6.attack(A3, "L")
asserterror("target is outside the plotted fire zone.")
assert A3.damage() == ""

# Kill the aircraft to avoid having to move them.
A0.takedamage("K")
A1.takedamage("K")
A2.takedamage("K")
A3.takedamage("K")

endgameturn()

assert not G0.isusingplottedfire()
assert not G1.isusingplottedfire()
assert not G2.isusingplottedfire()
assert not G3.isusingplottedfire()
assert not G4.isusingplottedfire()
assert G5.isusingplottedfire()
assert G6.isusingplottedfire()

endfile(__file__)
