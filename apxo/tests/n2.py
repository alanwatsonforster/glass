from apxo.tests.infrastructure import *

startfile(__file__, "missile flight")

# LO altitude band

starttestsetup(verbose=False)
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2030",
    "N",
    5,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A2 = aircraft(
    "A2",
    "AF",
    "F-16A-10",
    "A2-2020",
    "N",
    5,
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
A1a.move("TR/H,C2,C/R,TL/H,H,H/L,D,D2,H,HD")
A1a._assert("A2-2118       N     4", None)

startgameturn()
A1a.move("SLL/H,C2,C,H,H/L,H,D,D2,H,HD")
A1a._assert("A2-1918       N     4", None)

endfile(__file__)
