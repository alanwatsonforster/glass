from apengine.tests.infrastructure import *
startfile(__file__, "collision with terrain")

from apengine.tests.infrastructure import *

startsetup(sheets=[["C2"]],verbose=False)
A1 = aircraft("A1", "F-80C", 6625, "WSW", 1, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 6624, "WSW", 1, 4.0, "CL")
A3 = aircraft("A3", "F-80C", 6623, "WSW", 2, 4.0, "CL")
A4 = aircraft("A3", "F-80C", "6628/6727", "NNW", 1, 4.0, "CL")
endsetup()

startturn()
A1.move("LVL", "M", "H,H,H,H")
A1._assert("6227       WSW   1",  4.0)
A2.move("LVL", "M", "H,H,H,H")
A2._assert("6425       WSW   1",  4.0)
A3.move("LVL", "M", "H,H,H,H")
A3._assert("6225       WSW   2",  4.0)
A4.move("LVL", "M", "H,H,H,H")
A4._assert("6526/6626  NNW   1",  4.0)
endturn()

startsetup(sheets=[["B2"]],verbose=False)
A1 = aircraft("A1", "F-80C", 4228, "ENE", 2, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 4227, "ENE", 2, 4.0, "CL")
A3 = aircraft("A3", "F-80C", 4226, "ENE", 3, 4.0, "CL")
A4 = aircraft("A4", "F-80C", "4526/4627", "NNE", 2, 4.0, "CL")
endsetup()

startturn()
A1.move("LVL", "M", "H,H,H,H")
A1._assert("4626       ENE   2",  4.0)
A2.move("LVL", "M", "H,H,H,H")
A2._assert("4525       ENE   2",  4.0)
A3.move("LVL", "M", "H,H,H,H")
A3._assert("4624       ENE   3",  4.0)
A4.move("LVL", "M", "H,H,H,H")
A4._assert("4625/4725  NNE   2", 4.0)
endturn()

endfile(__file__)