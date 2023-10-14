from apengine.tests.infrastructure import *
startfile(__file__, "NRM aircraft")

# Rolls and NRM aircraft

startsetup()
A1 = aircraft("A1", "B-26B", 2015, "N", 24, 3.0, "CL")
endsetup()

startturn()
A1.move("VD/HRD",  "FT", "H,D2,D2,D2")
asserterror("aircraft cannot perform rolling maneuvers.")
A1.move("SD",  "FT", "H,H,H")
A1._assert("2012       N    24",  3.0)
endturn()

startturn()
A1.move("VD",  "FT", "H,D3,D3/VRL/L")
asserterror("aircraft cannot perform rolling maneuvers.")
A1.move("VD",  "FT", "H,D3,D3")
A1._assert("2011       N    18",  4.5)
endturn()


endfile(__file__)