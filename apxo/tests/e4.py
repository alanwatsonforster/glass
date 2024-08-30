from apxo.tests.infrastructure import *

startfile(__file__, "HPR aircraft")

# Rolls and HPR Aircraft

starttestsetup()
A1 = aircraft("A1", "AF", "F7U-3", "A1-2015", "N", 10, 3.5, "CL")
A2 = aircraft("A2", "AF", "F7U-3", "A1-2215", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F7U-3", "A1-2415", "N", 10, 2.0, "CL")
endtestsetup()

startgameturn()
A1.move("VC", "AB", "H,VRL/C2/L30,C2")
asserterror(
    "attempt to declare a vertical roll in VC following LVL flight other than on the last FP."
)
startgameturn()
A1.move("VC", "AB", "H,C2,VRL/C2/L30")
A1._assert("A1-2014       NNW  14", 2.5)
startgameturn()
A2.move("VC", "AB", "H,C2,C2,C2")
asserterror(
    "flight type immediately after LVL cannot be VC (for HPR aircraft at high speed)."
)
startgameturn()
A1.move("VC", "AB", "H,C2,C2")
A1._assert("A1-2014       N    14", 2.5)
A2.move("HRD/VD", "AB", "H,D2,D2,D2")
A2._assert("A1-2214       N     4", 5.5)
A3.move("HRD/VD", "N", "H,D2")
A3._assert("A1-2414       N     8", 2.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H,H")
A1._assert("A1-2012       N    14", 2.5)
startgameturn()
A1.move("UD", "AB", "HU,HU")
A1._assert("A1-2012       N    13", 2.5)
startgameturn()
A2.move("LVL", "AB", "H,C2,C2,C2")
asserterror(
    "flight type immediately after VD cannot be LVL (for HPR aircraft at high speed)."
)
startgameturn()
A1.move("SD", "AB", "H,D2,D2")
A1._assert("A1-2013       N    10", 3.5)
A2.move("SD", "AB", "H,H,H,D,D")
A2._assert("A1-2211       N     2", 6.5)
A3.move("LVL", "N", "H,H")
A3._assert("A1-2412       N     8", 2.5)
endgameturn()

startgameturn()
A2.move("ZC", "AB", "H,H,C,C,C,C,C")
A2._assert("A1-2209       N     7", 6.0)
startgameturn()
A1.move("LVL", "AB", "H,H,H")
A1._assert("A1-2010       N    10", 4.0)
A2.move("SC", "AB", "H,H,C,C,C,C,C")
A2._assert("A1-2209       N     7", 6.0)
A3.move("LVL", "N", "H,H,H")
A3._assert("A1-2409       N     8", 2.5)
endgameturn()

endfile(__file__)
