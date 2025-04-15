from glass.tests.infrastructure import *

startfile(__file__, "missile flight")

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
    "A2-2020",
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
A1a.move("H,H,H,H,H,H")
A1a._assert("A2-2018 N 10", None)
startgameturn()
A1a.move("HD,HD,HD,HD,HD,HD")
A1a._assert("A2-2018 N 4", None)

startgameturn()
A1a.move("C,C,C,C,C,C")
A1a._assert("A2-2024 N 16", None)

startgameturn()
A1a.move("C2,C2,C2,C2,C2,C2")
A1a._assert("A2-2024 N 22", None)

startgameturn()
A1a.move("D2,D2,D2")
A1a._assert("A2-2024 N 4", None)

startgameturn()
A1a.move("D2,D2,D2,D")
A1a._assert("A2-2024 N 3", None)

startgameturn()
A1a.move("H/R")
asserterror("attempt to maneuver without a declaration.")
startgameturn()
A1a.move("H/L")
asserterror("attempt to maneuver without a declaration.")

startgameturn()
A1a.move("TR/H/R")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A1a.move("TL/H/L")
asserterror("attempt to turn faster than the declared turn rate.")

startgameturn()
A1a.move("TR/H,H/R,TL/H,H/L")
A1a._assert("A2-2120 N 10", None)
startgameturn()
A1a.move("TL/H,H/L,TR/H,H/R")
A1a._assert("A2-1920 N 10", None)

startgameturn()
A1a.move("TR/H,C2,C/R,TL/H,H/L")
A1a._assert("A2-2121 N 13", None)
startgameturn()
A1a.move("TL/H,C2,C/L,TR/H,H/R")
A1a._assert("A2-1921 N 13", None)

startgameturn()
A1a.move("TR/H,D2,D/R,TL/H,H/L")
A1a._assert("A2-2121 N 7", None)
startgameturn()
A1a.move("TL/H,D2,D/L,TR/H,H/R")
A1a._assert("A2-1921 N 7", None)

startgameturn()
A1a.move("SLL/H,H,H/L")
asserterror("attempt to slide without sufficient preparatory HFPs.")
startgameturn()
A1a.move("SLR/H,H,H/R")
asserterror("attempt to slide without sufficient preparatory HFPs.")

startgameturn()
A1a.move("SLL/H,H,H,H/L")
A1a._assert("A2-1920 N 10", None)
startgameturn()
A1a.move("SLR/H,H,H,H/R")
A1a._assert("A2-2120 N 10", None)

startgameturn()
A1a.move("C2,VRR/C2/R90,H")
A1a._assert("A2-2123/2124 E 14", None)

startgameturn()
A1a.move("C2,VRL/C2/L90,H")
A1a._assert("A2-1923/1924 W 14", None)

startgameturn()
A1a._speed = 6.0
A1a.move("TR/H,H,H/R")
asserterror("attempt to maneuver when not allowed by the speed and altitude.")
startgameturn()
A1a._speed = 7.0
A1a.move("TR/H,H,H/R")
A1a._assert("A2-2021       NNE  10", None)
startgameturn()
A1a._speed = 7.0
A1a.move("TR/H,H,H/RR")
A1a._assert("A2-2021       ENE  10", None)
startgameturn()
A1a._speed = 7.0
A1a.move("TR/H,H,H/RRR")
asserterror("attempt to turn faster than the declared turn rate.")

endfile(__file__)
