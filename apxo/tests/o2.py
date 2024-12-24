from apxo.tests.infrastructure import *

startfile(__file__, "ground unit barrage fire")

starttestsetup()

G0 = groundunit(
    "G0", "A1-2110", symbols="infantry", aaaclass="B", aaamaximumrelativealtitude=2
)
G1 = groundunit(
    "G1", "A1-2110", symbols="infantry", aaaclass="B", aaamaximumrelativealtitude=2
)
G2 = groundunit(
    "G2", "A1-2110", symbols="armor", aaaclass="B", aaamaximumrelativealtitude=3
)
G3 = groundunit("G3", "A1-2110", symbols="artillery")
G4 = groundunit(
    "G4",
    "A1-2110",
    symbols="airdefense/gun",
    aaaclass="L",
    aaamaximumrelativealtitude=9,
)
G5 = groundunit(
    "G5",
    "A1-2110",
    symbols="airdefense/gun",
    aaaclass="M",
    aaamaximumrelativealtitude=18,
)
G6 = groundunit(
    "G6",
    "A1-2110",
    symbols="airdefense/gun",
    aaaclass="H",
    aaamaximumrelativealtitude=27,
)

A0 = aircraft("A0", "USAF", "F-100A", "A1-2110", "E", 2, 3)
A1 = aircraft("A1", "USAF", "F-100A", "A1-2110", "E", 3, 3)
A2 = aircraft("A2", "USAF", "F-100A", "A1-2110", "E", 4, 3)
A3 = aircraft("A3", "USAF", "F-100A", "A1-2111", "E", 2, 3)
A4 = aircraft("A4", "USAF", "F-100A", "A1-2112", "E", 2, 3)

endtestsetup()

startgameturn()

assert not G0.isusingbarragefire()
assert not G1.isusingbarragefire()
assert not G2.isusingbarragefire()
assert not G3.isusingbarragefire()
assert not G4.isusingbarragefire()
assert not G5.isusingbarragefire()
assert not G6.isusingbarragefire()

G0.takedamage("S")
G0.usebarragefire()
asserterror("G0 is suppressed.")

G1.usebarragefire()
assert G1.isusingbarragefire()

G2.usebarragefire()
assert G2.isusingbarragefire()

G3.usebarragefire()
asserterror("G3 is not capable of barrage fire.")

G4.usebarragefire()
assert G4.isusingbarragefire()

G5.usebarragefire()
assert G5.isusingbarragefire()

G6.usebarragefire()
asserterror("G6 is not capable of barrage fire.")

assert not G0.isusingbarragefire()
assert G1.isusingbarragefire()
assert G2.isusingbarragefire()
assert not G3.isusingbarragefire()
assert G4.isusingbarragefire()
assert G5.isusingbarragefire()
assert not G6.isusingbarragefire()

G1.attack(A0, "L")
assert A0.damage() == "L"
G2.attack(A0, "L")
assert A0.damage() == "2L"
G4.attack(A0, "L")
assert A0.damage() == "H"
G5.attack(A0, "L")
assert A0.damage() == "L+H"

G1.attack(A1, "L")
asserterror("target is above the barrage fire.")
assert A1.damage() == ""
G2.attack(A1, "L")
assert A1.damage() == "L"
G4.attack(A1, "L")
assert A1.damage() == "2L"
G5.attack(A1, "L")
assert A1.damage() == "H"

G1.attack(A2, "L")
asserterror("target is above the barrage fire.")
assert A2.damage() == ""
G2.attack(A2, "L")
asserterror("target is above the barrage fire.")
assert A2.damage() == ""
G4.attack(A2, "L")
assert A2.damage() == "L"
G5.attack(A2, "L")
assert A2.damage() == "2L"

G1.attack(A3, "L")
assert A3.damage() == "L"
G2.attack(A3, "L")
assert A3.damage() == "2L"
G4.attack(A3, "L")
assert A3.damage() == "H"
G5.attack(A3, "L")
assert A3.damage() == "L+H"

G1.attack(A4, "L")
asserterror("target is outside the barrage fire zone.")
assert A4.damage() == ""
G2.attack(A4, "L")
asserterror("target is outside the barrage fire zone.")
assert A4.damage() == ""
G4.attack(A4, "L")
asserterror("target is outside the barrage fire zone.")
assert A4.damage() == ""
G5.attack(A4, "L")
asserterror("target is outside the barrage fire zone.")
assert A4.damage() == ""

startgameturn()

G1.usebarragefire()
assert G1.isusingbarragefire()

G2.usebarragefire()
assert G2.isusingbarragefire()

G4.usebarragefire()
assert G4.isusingbarragefire()

G5.usebarragefire()
assert G5.isusingbarragefire()

# Kill the aircraft to avoid having to move them.
A0.takedamage("K")
A1.takedamage("K")
A2.takedamage("K")
A3.takedamage("K")
A4.takedamage("K")

endgameturn()

assert not G0.isusingbarragefire()
assert not G1.isusingbarragefire()
assert not G2.isusingbarragefire()
assert not G3.isusingbarragefire()
assert not G4.isusingbarragefire()
assert not G5.isusingbarragefire()
assert not G6.isusingbarragefire()

startgameturn()

G2.usebarragefire()
assert G2.isusingbarragefire()

G4.usebarragefire()
asserterror("G4 is out of ammunition.")

G5.usebarragefire()
asserterror("G5 is out of ammunition.")

startgameturn()

G2.usebarragefire()
assert G2.isusingbarragefire()

G4.resupplyammunition()
G5.resupplyammunition()

endgameturn()

startgameturn()

G2.usebarragefire()
assert G2.isusingbarragefire()

G4.usebarragefire()
assert G4.isusingbarragefire()

G5.usebarragefire()
assert G5.isusingbarragefire()

endgameturn()

endfile(__file__)
