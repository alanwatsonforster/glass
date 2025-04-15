from apxo.tests.infrastructure import *

startfile(__file__, "NRM aircraft")

# Rolls and NRM aircraft

starttestsetup()
A1 = setupaircraft("A1", "AF", "B-26B (Two Turrets)", "A1-2015", "N", 24, 3.0, "CL")
endtestsetup()

startgameturn()
A1.move("HRD/VD", "FT", "H,D2,D2,D2")
asserterror("aircraft cannot perform rolling maneuvers.")
startgameturn()
A1.move("SD", "FT", "H,H,D")
A1._assert("A1-2013       N    23", 3.0)
endgameturn()

startgameturn()
A1.move("VD", "FT", "H,D3,VRL/D3/L")
asserterror("aircraft cannot perform rolling maneuvers.")
startgameturn()
A1.move("VD", "FT", "H,D3,D3")
A1._assert("A1-2012       N    17", 4.5)
endgameturn()


endfile(__file__)
