from apxo.tests.infrastructure import *
startfile(__file__, "NRM aircraft")

# Rolls and NRM aircraft

starttestsetup()
A1 = aircraft("A1", "AF", "B-26B", "A1-2015", "N", 24, 3.0, "CL")
endtestsetup()

startturn()
A1.move("VD/HRD",  "FT", "H,D2,D2,D2")
asserterror("aircraft cannot perform rolling maneuvers.")
startturn()
A1.move("SD",  "FT", "H,H,D")
A1._assert("A1-2013       N    23",  3.0)
endturn()

startturn()
A1.move("VD",  "FT", "H,D3,D3/VRL/L")
asserterror("aircraft cannot perform rolling maneuvers.")
startturn()
A1.move("VD",  "FT", "H,D3,D3")
A1._assert("A1-2012       N    17",  4.5)
endturn()


endfile(__file__)