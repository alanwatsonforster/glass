from apxo.tests.infrastructure import *
startfile(__file__, "ABSF aircraft")

from apxo.tests.infrastructure import *

# The F-89D has a different max speed with AB and M power.

starttestsetup()
A1 = aircraft("A1", "AF", "F-89D", "A2-2030", "N", 30, 6.0, "CL", fuel="60%", bingofuel="40%")
A2 = aircraft("A2", "AF", "F-89D", "A2-2030", "N", 30, 6.0, "CL", fuel="60%", bingofuel="40%")
endtestsetup()

startturn()
A1.move("LVL", "AB", "H,H,H,H,H,H")
A1._assert("A2-2024       N    30", 6.0)
A2.move("LVL", "M" , "H,H,H,H,H,H")
A2._assert("A2-2024       N    30", 5.5)
endturn()

endfile(__file__)