from glass.tests.infrastructure import *

startfile(__file__, "transported ground unit")

starttestsetup()

T0 = setupgroundunit(
    "T0",
    "A1-2120",
    "truck platoon",
    transporting=setupgroundunit("I0", "A1-2120", "infantry platoon"),
)

T1 = setupgroundunit(
    "T1",
    "A1-2120",
    "truck platoon",
    transporting="truck platoon",
)
asserterror("invalid transported unit \"'truck platoon'\".")

T2 = setupgroundunit(
    "T2",
    "A1-2120",
    "truck platoon",
    transporting=setupgroundunit("T3", "A1-2120", "truck platoon"),
)
asserterror("T3 cannot be transported.")

T4 = setupgroundunit(
    "T4",
    "A1-2120",
    "truck platoon",
    transporting=setupgroundunit("B0", "A1-2120", "Bofors L60 battery"),
)

A0 = setupaircraft("A0", "USAF", "F-100A", "A1-2115", "S", 1, 6)

endtestsetup()

startgameturn()

T0.transporting().usebarragefire()
asserterror("I0 is being transported.")

startgameturn()

T4.transporting().useplottedfire("A1-2125", 3)
asserterror("B0 is being transported.")

startgameturn()

T4.transporting().track(A0)
asserterror("B0 is being transported.")

startgameturn()

A0.move("LVL", "M")
A0.aim(T0)
A0.continuemove("H H H H")
A0.attack(T0, "GN", "D")
assert T0.damage() == "D+2S"
assert T0.transporting().damage() == "D+2S"

endfile(__file__)
