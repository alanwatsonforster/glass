from apengine.tests.infrastructure import *
startfile(__file__, "HRD")

# Half Roll and Dive

startsetup()
A1 = aircraft("A1", "F-80C", 2015, "N", 20, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 2215, "N", 20, 4.0, "CL")
A3 = aircraft("A3", "F-80C", 2415, "N", 20, 5.0, "CL")
A4 = aircraft("A4", "F-80C", 2615, "N", 20, 5.0, "CL")
A5 = aircraft("A5", "F-104A", 2815, "N", 20, 7.0, "CL") # SS
endsetup()

startturn()
A1.move("LVL/HRD",  "N", "")
asserterror("flight type immediately after LVL cannot be LVL with a HRD.")
A1.move("SD/HRD",  "N", "")
asserterror("flight type immediately after LVL cannot be SD with a HRD.")
A1.move("UD/HRD",  "N", "")
asserterror("flight type immediately after LVL cannot be UD with a HRD.")
A1.move("ZC/HRD",  "N", "")
asserterror("flight type immediately after LVL cannot be ZC with a HRD.")
A1.move("SC/HRD",  "N", "")
asserterror("flight type immediately after LVL cannot be SC with a HRD.")
A1.move("VC/HRD",  "N", "")
asserterror("flight type immediately after LVL cannot be VC with a HRD.")
A1.move("VD/HRD",  "N", "H,D2,D2,D2")
A1._assert("2014       N    14",  5.5)

A1.move("ZC",  "M", "H,H,H,H")
A1._assert("2011       N    20",  4.0)
A2.move("SC",  "M", "H,H,H,H")
A2._assert("2211       N    20",  4.0)
A3.move("ZC",  "M", "H,H,H,H,H")
A3._assert("2410       N    20",  5.0)
A4.move("SC",  "M", "H,H,H,H,H")
A4._assert("2610       N    20",  5.0)

A5.move("VD/HRD",  "AB", "H,H,D2,D2,D2,D2,D2")
A5._assert("2813       N    10",  10.0)

endturn()

startturn()
A1.move("LVL/HRD",  "N", "")
asserterror("flight type immediately after ZC cannot be LVL with a HRD.")
A1.move("SD/HRD",  "N", "")
asserterror("flight type immediately after ZC cannot be SD with a HRD.")
A1.move("UD/HRD",  "N", "")
asserterror("flight type immediately after ZC cannot be UD with a HRD.")
A1.move("ZC/HRD",  "N", "")
asserterror("flight type immediately after ZC cannot be ZC with a HRD.")
A1.move("SC/HRD",  "N", "")
asserterror("flight type immediately after ZC cannot be SC with a HRD.")
A1.move("VC/HRD",  "N", "")
asserterror("flight type immediately after ZC cannot be VC with a HRD.")

A1.move("VD/HRD",  "M", "H,D3,D3,D3")
A1._assert("2010       N    11",  6.5)
A2.move("VD/HRD",  "M", "H,D3,D3,D3")
A2._assert("2210       N    11",  6.5)

A3.move("VD/HRD",  "M", "")
asserterror("flight type immediately after ZC cannot be VD (without a low-speed HRD).")
A3.move("VC",  "M", "H,H,C,C,C")
A3._assert("2408       N    23",  4.0)

A4.move("VD/HRD",  "M", "")
asserterror("flight type immediately after SC cannot be VD (without a low-speed HRD).")
A4.move("VC",  "M", "H,H,C,C,C")
A4._assert("2608       N    23",  4.0)

A5.move("SD",  "AB", "H,H,H,H,H,D,D,D,D,D")
A5._assert("2808       N     5",  9.0)

endturn()

startturn()
A1.move("SD",  "N", "H,H,H,D,D,D")
A1._assert("2007       N     8",  6.5)
A2.move("SD",  "N", "H,H,H,D,D,D")
A2._assert("2207       N     8",  6.5)
A3.move("SD/HRD",  "M", "H,H,D,D")
A3._assert("2406       N    21",  4.5)
A4.move("SD/HRD",  "M", "H,H,D,D")
A4._assert("2606       N    21",  4.5)
A5.move("ZC",  "AB", "H,H,H,H,C2,C2,C2,C2,C2")
A5._assert("2804       N    15",  8.0)

endturn()

endfile(__file__)