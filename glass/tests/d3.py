from glass.tests.infrastructure import *

startfile(__file__, "LBR/HBR aircraft")

# Sustained turns with LBR aircraft.

starttestsetup()
A1 = setupaircraft("A1", "AF", "Sea Fury FB.11", "A1-2010", "N", 10, 4.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "FT", "BTR/H/RR,BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("A1-2210       WSW  10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "FT", "BTR/H/RR,BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("A1-2108       ESE  10", 3.0)
endgameturn()

startgameturn()
A1.move("LVL", "FT", "BTR/H/RRR,BTR/H/RRR,BTR/H/RRR")
A1._assert("A1-2009       NNE  10", 2.5)
endgameturn()

startgameturn()
A1.move("LVL", "FT", "HTR/H/RRR,HTR/H/RRR,HTR/H/RRR")
A1._assert("A1-2109       WNW  10", 2.0)
endgameturn()

startgameturn()
A1.move("LVL", "FT", "HTR/H/RRR,HTR/H/RRR")
A1._assert("A1-2108       ESE  10", 1.5)
endgameturn()

# Sustained turns with HBR aircraft

starttestsetup()
A1 = setupaircraft("A1", "AF", "F7U-3", "A1-2010", "N", 10, 6.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "ETR/H/R,ETR/H/R,ETR/H/R,ETR/H/R,ETR/H/R,ETR/H/R")
A1._assert("A1-2410       S    10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "BTR/H/RR,BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("A1-2210       ENE  10", 1.0)
endgameturn()

endfile(__file__)
