from apengine.tests.infrastructure import *
startfile(__file__, "LBR/HBR aircraft")

# Sustained turns with LBR aircraft.

startsetup()
A1 = aircraft("A1", "Sea Fury FB.11", 2010, "N", 10, 4.5, "CL")
endsetup()

startturn()
A1.move("LVL",  "FT", "BTR/H/RR,H/RR,H/RR,H/RR")
A1._assert("2210       WSW  10",  4.0)
endturn()

startturn()
A1.move("LVL",  "FT", "H/RR,H/RR,H/RR,H/RR")
A1._assert("2108       ESE  10",  3.5)
endturn()

startturn()
A1.move("LVL",  "FT", "H/RRR,H/RRR,H/RRR,H/RRR")
A1._assert("2108       ESE  10",  2.5)
endturn()

startturn()
A1.move("LVL",  "FT", "HTR/H/RRR,H/RRR")
A1._assert("2109       WNW  10",  2.5)
endturn()

startturn()
A1.move("LVL",  "FT", "HTR/H/RRR,H/RRR,H/RRR")
A1._assert("2209       SSW  10",  2.0)
endturn()

# Sustained turns with HBR aircraft

startsetup()
A1 = aircraft("A1", "F7U-3", 2010, "N", 10, 6.5, "CL")
endsetup()

startturn()
A1.move("LVL",  "AB", "ETR/H/R,H/R,H/R,H/R,H/R,H/R")
A1._assert("2410       S    10",  4.0)
endturn()

startturn()
A1.move("LVL",  "AB", "BTR/H/RR,H/RR,H/RR,H/RR")
A1._assert("2210       ENE  10",  1.5)
endturn()

endfile(__file__)