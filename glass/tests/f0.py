from apxo.tests.infrastructure import *

startfile(__file__, "departed flight")

# Maneuvering Departures

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2010", "N", 10, 3.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "MDR60/H")
asserterror("'MDR60/H' is not a valid move.")

startgameturn()
A1.move("LVL", "M", "MDR60")
A1._assert("A1-2109       ENE  10", 3.0)
startgameturn()
A1.move("LVL", "M", "H,MDR60")
A1._assert("A1-2108       ENE  10", 3.0)
startgameturn()
A1.move("LVL", "M", "H,H,MDR60")
A1._assert("A1-2008       ENE  10", 3.0)
endgameturn()

# Maneuvering Departures from Carried Turn

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2010", "N", 10, 3.0, "CL")
endtestsetup()

startgameturn()
A1.move("SD", "M", "BTR/H/RRR+,H/RRR+,D/RRR+")
A1._assert("A1-2109       W     9", 1.5)
endgameturn()

startgameturn()
A1.move("SD", "M", "H")
asserterror("aircraft has entered departed flight while maneuvering.")
startgameturn()
A1.move("DP", "M", "R30")
A1._assert("A1-2109       WNW   7", 1.5)
endgameturn()

# Maneuvering Departures from Rolls. Run with verbose=True to check that the
# warnings are issued.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A2-2030", "N", 46, 3.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-2230", "N", 59, 6.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A2-2430", "N", 46, 3.0, "CL")
endtestsetup()

startgameturn()
A2.move("HRD/VD", "M", "H,H,D2,D2,D2,D2")
A2._assert("A2-2228       N    51", 8.5)
startgameturn()
A1.move("HRD/VD", "M", "H,D2,D2")
A1._assert("A2-2029       N    42", 4.0)
A2.move("SD", "M", "H,H,H,H,H,D")
A2._assert("A2-2225       N    58", 6.5)
A3.move("LVL", "M", "TTR/H,H,H")
A3._assert("A2-2427       N    46", 3.0)
endgameturn()

startgameturn()
A1.move("SD", "M", "H,H,D,D")
A1._assert("A2-2027       N    40", 4.5)
A2.move("VD", "M", "H,H,D2,D2,D2,VRL/D2/L180")
A2._assert("A2-2223       S    50", 8.0)
A3.move("LVL", "M", "H,H,H/R")
A3._assert("A2-2424       NNE  46", 3.0)
endgameturn()

# Departed Flight

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1814", "N", 10, 3.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2014", "N", 10, 1.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2214", "N", 10, 5.0, "CL")
endtestsetup()

startgameturn()
A1.move("DP", "M", "MDR150")
A1._assert("A1-1913       SSE   7", 3.0)
startgameturn()
A1.move("DP", "M", "MDL150")
A1._assert("A1-1713       SSW   7", 3.0)
startgameturn()
A3.move("DP", "M", "MDR150")
A3._assert("A1-2312       SSE   5", 5.0)
startgameturn()
A1.move("DP", "M", "R150")
A1._assert("A1-1814       SSE   7", 3.0)
A2.move("DP", "M", "L300")
A2._assert("A1-2014       ENE   9", 1.0)
A3.move("DP", "M", "MDL150")
A3._assert("A1-2112       SSW   5", 5.0)
endgameturn()

startgameturn()
A1.move("DP", "M", "R150")
A1._assert("A1-1814       WNW   2", 3.0)
A2.move("DP", "M", "L300")
A2._assert("A1-2014       ESE   6", 1.0)
A3.move("DP", "M", "R180")
A3._assert("A1-2112       NNE   0", 5.0)
endgameturn()

endfile(__file__)
