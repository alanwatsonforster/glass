from apxo.tests.infrastructure import *

startfile(__file__, "missile attacks")

# LO altitude band

starttestsetup()
A1 = setupaircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2030",
    "N",
    10,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A2 = setupaircraft(
    "A2",
    "AF",
    "F-16A-10",
    "A2-2025",
    "N",
    10,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
endtestsetup()

startgameturn()
A1.move("LVL", "N", "H,H,H,H,H,H")
A2.move("LVL", "N", "H,H,H,H,H,H")
A1a = A1.airtoairlaunch("A1a", A2, "9")
endgameturn()

startgameturn()
A1a.move("H,H,H")
A1a._assert("A2-2021 N 10", None)
A2.move("LVL", "N", "H")
A2._assert("A2-2018 N 10", None)
A1a.continuemove("H,H")
A1a._assert("A2-2019 N 10", None)
A1a.attack(A2, "K")
A1.move("LVL", "N", "H,H,H,H,H,H")
endgameturn()

endfile(__file__)
