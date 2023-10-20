from apengine.tests.infrastructure import *
startfile(__file__, "loss of thrust with altitude")


# Loss of Thrust With Altitude

starttestsetup()
A1 = aircraft("A1", "F-80C", 1815, "N"  , 10, 3.0, "CL")
A2 = aircraft("A2", "F-80C", 2015, "N"  , 40, 3.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "M", "H,H,H")
A1._assert("1812       N    10",  3.0)
A2.move("LVL",  "M", "H,H,H")
A2._assert("2012       N    40",  3.0)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H")
A1._assert("1809       N    10",  3.5)
A2.move("LVL",  "M", "H,H,H")
A2._assert("2009       N    40",  3.0)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H")
A1._assert("1806       N    10",  3.5)
A2.move("LVL",  "M", "H,H,H")
A2._assert("2006       N    40",  3.0)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H,H")
A1._assert("1802       N    10",  4.0)
A2.move("LVL",  "M", "H,H,H")
A2._assert("2003       N    40",  3.5)
endturn()

endfile(__file__)