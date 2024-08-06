from apxo.tests.infrastructure import *

startfile(__file__, "speed brakes")

# Speed Brakes

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A2-1125", "N", 10, 2.5, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A2-1325", "N", 10, 3.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A2-1525", "N", 10, 3.5, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A2-1725", "N", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "N", "SH,H")
A1._assert("A2-1123       N    10", 2.5)
A2.move("LVL", "N", "SH,H,H")
A2._assert("A2-1322       N    10", 3.0)
A3.move("LVL", "N", "SH,H,H")
A3._assert("A2-1522       N    10", 3.5)
A4.move("LVL", "N", "SH,H,H,H")
A4._assert("A2-1721       N    10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "N", "SH,H,H")
A1._assert("A2-1120       N    10", 2.0)
A2.move("LVL", "N", "SH,H,H")
A2._assert("A2-1319       N    10", 2.5)
A3.move("LVL", "N", "SH,H,H,H")
A3._assert("A2-1518       N    10", 3.0)
A4.move("LVL", "N", "SH,H,H,H")
A4._assert("A2-1717       N    10", 3.5)
endgameturn()

startgameturn()
A1.move("LVL", "N", "SH,H")
A1._assert("A2-1118       N    10", 2.0)
A2.move("LVL", "N", "SH,H")
A2._assert("A2-1317       N    10", 2.5)
A3.move("LVL", "N", "SH,H,H")
A3._assert("A1-1515       N    10", 3.0)
A4.move("LVL", "N", "SH,H,H")
A4._assert("A1-1714       N    10", 3.5)
endgameturn()

startgameturn()
A1.move("LVL", "N", "SH,H")
A1._assert("A2-1116       N    10", 1.5)
A2.move("LVL", "N", "SH,H,H")
A2._assert("A1-1314       N    10", 2.0)
A3.move("LVL", "N", "SH,H,H")
A3._assert("A1-1512       N    10", 2.5)
A4.move("LVL", "N", "SH,H,H,H")
A4._assert("A1-1710       N    10", 3.0)
endgameturn()

# Check at supersonic speeds.

starttestsetup(variants=["use version 2.4 rules"])
A1 = aircraft("A1", "AF", "F-104A", "A2-2025", "N", 10, 10.0, "CL")
A2 = aircraft("A2", "AF", "F-104A", "A2-2025", "N", 10, 7.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "I", "S4H")
asserterror("speedbrake capability is only 3.0 DPs.")
A2.move("LVL", "I", "S2H")
asserterror("speedbrake capability is only 1 DP.")

startgameturn()
A1.move("LVL", "I", "S3H,H,H,H,H,H,H,H,H,H")
A1._assert("A1-2015       N    10", 5.5)

A2.move("LVL", 0.5, "S1H,H,H,H,H,H,H")
A2._assert("A2-2018       N    10", 7.0)
endgameturn()

startgameturn()
A1.move("LVL", "I", "S1H,H,H,H,H")
A1._assert("A1-2010       N    10", 5.0)
A2.move("LVL", 0.5, "S1H,H,H,H,H,H,H")
A2._assert("A1-2011       N    10", 6.5)
endgameturn()

endfile(__file__)
