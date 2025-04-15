from apxo.tests.infrastructure import *

startfile(__file__, "terrain-following flight")

from apxo.tests.infrastructure import *

starttestsetup(sheets=[["C2"]])
A1 = setupaircraft("A1", "AF", "F-80C", "C2-6625", "WSW", 1, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "C2-6624", "WSW", 1, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "C2-6623", "WSW", 2, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "C2-6628/6727", "NNW", 1, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("SD", "M")
A1.enterterrainfollowingflight()
asserterror("attempt to enter terrain-following flight while not in level flight.")

startgameturn()
A1.move("LVL", "M")
A1.leaveterrainfollowingflight()
asserterror(
    "attempt to leave terrain-following flight while not in terrain-following flight."
)

startgameturn()
A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.enterterrainfollowingflight()
asserterror(
    "attempt to enter terrain-following flight while already in terrain-following flight."
)

startgameturn()
A4.move("LVL", "M")
A4.enterterrainfollowingflight()
A4.leaveterrainfollowingflight()
A4.enterterrainfollowingflight()
asserterror("attempt to enter terrain-following flight after leaving it.")

startgameturn()
A3.move("LVL", "M")
A3.enterterrainfollowingflight()
asserterror(
    "attempt to enter terrain-following flight while not exactly one altitude level above terrain."
)

startgameturn()
A4.move("LVL", "M")
A4.enterterrainfollowingflight()
A4.continuemove("H,HC,HD,H")
asserterror("aircraft cannot both climb and dive while in terrain-following flight.")

startgameturn()
A4.move("LVL", "M")
A4.enterterrainfollowingflight()
A4.continuemove("H,HC,H,H")
asserterror("did not maintain correct altitude for terrain-following flight.")

startgameturn()
A4.move("LVL", "M")
A4.enterterrainfollowingflight()
A4.continuemove("H,H,H,H")
A4._assert("C2-6526/6626 NNW 1", 4.0)

startgameturn()

A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.continuemove("H,H,H,H")
A1._assert("C2-6227       WSW   0", 4.0)

A2.move("LVL", "M")
A2.enterterrainfollowingflight()
A2.continuemove("H,HC,H,H")
A2._assert("C2-6226       WSW   1", 4.0)

A3.move("LVL", "M", "H")
A3.enterterrainfollowingflight()
A3.continuemove("BTL/H/L,H,H")
A3._assert("C2-6325 SSW 1", 4.0)

A4.move("LVL", "M")
A4.enterterrainfollowingflight()
A4.continuemove("H,HC")
A4.leaveterrainfollowingflight()
A4.continuemove("H,H")
A4._assert("C2-6425/6524 NNW 2", 4.0)

endgameturn()

startgameturn()

A1.move("LVL", "M", "H,H,H,H")
A1._assert("C2-5829       WSW   0", 4.5)

A2.move("LVL", "M", "H,H,HD,H")
A2._assert("C2-5828       WSW   0", 4.0)

A3.move("ZC", "M", "H,HD")
A3.leaveterrainfollowingflight()
A3.continuemove("C,H")
A3._assert("C2-6127/6228 SSW 2", 4.0)

A4.move("LVL", "M")
A4.enterterrainfollowingflight()
A4.continuemove("BTR/H/RR,H,HD,H")
A4._assert("C2-6521/6622 NNE 0", 4.0)

endgameturn()

# Check limits on ETs.

starttestsetup(sheets=[["C2"]])
A1 = setupaircraft("A1", "AF", "F-100C", "C2-6625", "WSW", 1, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "ETR/H")
A1.enterterrainfollowingflight()
asserterror("attempt to enter terrain-following flight while using a turn rate of ET.")

startgameturn()
A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.continuemove("ETR/H/R,H,H,H")
asserterror("terrain-following flight limits the turn rate to BT.")

# Check TFF across ridge line

starttestsetup(sheets=[["C2"]])
A1 = setupaircraft("A1", "AF", "F-100C", "C2-6625", "WNW", 1, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.continuemove("H,HC,H,H")
A1._assert("C2-6323 WNW 1", 4.0)

# Check TTF in city hexes.

starttestsetup(sheets=[["A2"]])
A1 = setupaircraft("A1", "AF", "F-100C", "A2-2224", "N", 1, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.continuemove("H,H,H,H")
A1._assert("A2-2222 N 0", 4.0)

startgameturn()
A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.continuemove("BTR/H/R,H,H,H")
A1._assert("A2-2222/2322 NNE 0", 4.0)

startgameturn()
A1.move("LVL", "M")
A1.enterterrainfollowingflight()
A1.continuemove("H")
A1.leaveterrainfollowingflight()
A1.continuemove("H,H,H")
A1._assert("A2-2220 N 1", 4.0)

endfile(__file__)
