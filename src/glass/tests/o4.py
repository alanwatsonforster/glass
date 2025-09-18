from glass.tests.infrastructure import *

startfile(__file__, "ground unit aimed fire")

starttestsetup()

G0 = setupgroundunit(
    "G0", "A1-2120", symbols="infantry", aaaclass="B", aaamaximumrelativealtitude=2
)
G1 = setupgroundunit(
    "G1", "A1-2120", symbols="infantry", aaaclass="B", aaamaximumrelativealtitude=2
)
G2 = setupgroundunit(
    "G2", "A1-2120", symbols="armor", aaaclass="B", aaamaximumrelativealtitude=3
)
G3 = setupgroundunit("G3", "A1-2120", symbols="artillery")
G4 = setupgroundunit(
    "G4",
    "A1-2120",
    symbols="air-defense/gun",
    aaaclass="L",
    aaamaximumrelativealtitude=6,
    aaarange=[2, 3, 5],
)
G5 = setupgroundunit(
    "G5",
    "A1-2120",
    symbols="air-defense/gun",
    aaaclass="L",
    aaamaximumrelativealtitude=6,
    aaarange=[2, 3, 5],
)

A0 = setupaircraft("A0", "USAF", "F-100A", "A1-2112", "S", 1, 6)
A1 = setupaircraft("A1", "USAF", "F-100A", "A1-2120", "S", 16, 6)
A2 = setupaircraft("A2", "USAF", "F-100A", "A1-2113", "S", 1, 6)
A3 = setupaircraft("A3", "USAF", "F-100A", "A1-2118", "S", 8, 6)

endtestsetup()

startgameturn()

G0.track(A0)
asserterror("G0 cannot track.")
G1.track(A0)
asserterror("G1 cannot track.")
G2.track(A0)
asserterror("G2 cannot track.")
G3.track(A0)
asserterror("G3 cannot track.")
G4.track(A0)
asserterror("A0 is beyond the maximum tracking range of 7.")
G4.track(A1)
asserterror("A1 is beyond the maximum tracking range of 7.")

A0.move("LVL", "M", "H")
G4.attack(A0)
asserterror("G4 is not tracking A0.")
G4.track(A0)
A0.continuemove("H")
G4.attack(A0)
asserterror("A0 is beyond the maximum range of 5.")
A0.continuemove("H")
G4.attack(A0, "L")
assert A0.damage() == "L"

G5.track(A3)
A3.move("LVL", "M", "H H")
G5.attack(A3)
asserterror("A3 is above the maximum altitude of 6.")

assertnoerror()

endfile(__file__)
