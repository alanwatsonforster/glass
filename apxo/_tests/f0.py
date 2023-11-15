from apxo._tests.infrastructure import *
startfile(__file__, "departed flight")

# Maneuvering Departures

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-80C", "2010", "N", 10, 3.0, "CL")
endtestsetup()

startturn()
A1.move("LVL" ,  "M", "MDR60"    )
A1._assert("2109       ENE  10",  3.0)
startturn()
A1.move("LVL" ,  "M", "H,MDR60"  )
A1._assert("2108       ENE  10",  3.0)
startturn()
A1.move("LVL" ,  "M", "H,H,MDR60")
A1._assert("2008       ENE  10",  3.0)
endturn()

# Maneuvering Departures from Carried Turn

starttestsetup()
A1 = aircraft("A1", "F-80C", "2010", "N", 10, 3.0, "CL")
endtestsetup()

startturn()
A1.move("SD" ,  "M", "BTR/H/RRR+,H/RRR+,D/RRR+"    )
A1._assert("2109       W     9",  2.0)
endturn()

startturn()
A1.move("SD" ,  "M", "H")
asserterror("aircraft has entered departed flight while maneuvering.")
startturn()
A1.move("DP" ,  "M", "R30"    )
A1._assert("2109       WNW   7",  2.0)
endturn()

# Maneuvering Departures from Rolls. Run with verbose=True to check that the 
# warnings are issued.

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-80C" , "2030", "N", 46, 3.0, "CL")
A2 = aircraft("A2", "F-104A", "2230", "N", 59, 6.0, "CL")
A3 = aircraft("A3", "F-80C" , "2430", "N", 46, 3.0, "CL")
endtestsetup()

startturn()
A2.move("VD/HRD",  "M", "H,H,D2,D2,D2,D2"  )
A2._assert("2228       N    51",  8.0)
startturn()
A1.move("VD/HRD",  "M", "H,D2,D2"          )
A1._assert("2029       N    42",  4.0)
A2.move("SD",  "M", "H,H,H,H,H,D"          )
A2._assert("2225       N    58",  6.0)
A3.move("LVL",  "M", "TTR/H,H,H"           )
A3._assert("2427       N    46",  3.0)
endturn()

startturn()
A1.move("SD" ,  "M", "H,H,D,D"                 )
A1._assert("2027       N    40",  4.5)
A2.move("VD" ,  "M", "H,H,D2,D2,D2,VRL/D2/L180")
A2._assert("2223       S    50",  8.0)
A3.move("LVL",  "M", "H,H,HR"                  )
A3._assert("2424       NNE  46",  3.0)
endturn()

# Departed Flight

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-80C", "1814", "N", 10, 3.0, "CL")
A2 = aircraft("A2", "F-80C", "2014", "N", 10, 1.0, "CL")
A3 = aircraft("A3", "F-80C", "2214", "N", 10, 5.0, "CL")
endtestsetup()

startturn()
A1.move("DP",  "M", "MDR150")
A1._assert("1913       SSE   7",  3.0)
startturn()
A1.move("DP",  "M", "MDL150")
A1._assert("1713       SSW   7",  3.0)
startturn()
A3.move("DP",  "M", "MDR150")
A3._assert("2312       SSE   5",  5.0)
startturn()
A1.move("DP",  "M", "R150")
A1._assert("1814       SSE   7",  3.0)
A2.move("DP",  "M", "L300")
A2._assert("2014       ENE   9",  1.0)
A3.move("DP",  "M", "MDL150")
A3._assert("2112       SSW   5",  5.0)
endturn()

startturn()
A1.move("DP",  "M", "R150")
A1._assert("1814       WNW   2",  3.0)
A2.move("DP",  "M", "L300")
A2._assert("2014       ESE   6",  1.0)
A3.move("DP", "M", "R180")
A3._assert("2112       NNE   0",  5.0)
endturn()

endfile(__file__)