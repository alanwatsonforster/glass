from glass.tests.infrastructure import *

startfile(__file__, "attacks on ground unit")

starttestsetup()

G0 = setupgroundunit("G0", "A1-2120", "infantry")


A0 = setupaircraft("A0", "USAF", "F-100A", "A1-2212", "S", 1, 6)
A1 = setupaircraft("A1", "USAF", "F-100A", "A1-2212", "SSW", 1, 6)
A2 = setupaircraft("A2", "USAF", "F-100A", "A1-2212", "SSW", 1, 6)
A3 = setupaircraft(
    "A3",
    "USAF",
    "F-100A",
    "A1-2112",
    "S",
    1,
    6,
    stores={
        3: "RK/HVAR",
        4: "RK/HVAR",
        5: "RK/HVAR",
        6: "RK/HVAR",
    },
)
A4 = setupaircraft(
    "A4",
    "USAF",
    "F-100A",
    "A1-2112",
    "S",
    1,
    6,
    stores={
        3: "RK/HVAR",
        4: "RK/HVAR",
        5: "RK/HVAR",
        6: "RK/HVAR",
    },
)

endtestsetup()

startgameturn()

A0.move("LVL", "M", "DRR/H H H/R")
A0.aim(G0)
asserterror("aiming is forbidden immediately after rolling.")

A1.move("LVL", "M", "BTL/H H H/L")
A1.aim(G0)
asserterror("aiming is forbidden while banked.")

A2.move("LVL", "M", "ETL/H H H/L H")
A2.aim(G0)
asserterror("aiming is forbidden while recovering from an ET.")

A3.aim(G0)
assertnoerror()
A3.move("LVL", "M", "H")
A3.attack(G0, "RK")
asserterror("stores must be specified for RK attacks.")
A3.attack(G0, "RK", "-", stores=[3, 4, 5, 6])
assert G0.damage() == ""

A4.aim(G0)
assertnoerror()
A4.move("LVL", "M", "H")
A4.attack(G0, "RK")
asserterror("stores must be specified for RK attacks.")
A4.attack(G0, "RK", "K", stores=[3, 4, 5, 6])
assert G0.damage() == "K"

endfile(__file__)
