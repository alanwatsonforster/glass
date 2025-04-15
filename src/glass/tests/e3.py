from glass.tests.infrastructure import *

startfile(__file__, "loss of thrust with altitude")


# Loss of Thrust With Altitude

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "N", 10, 3.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "N", 40, 3.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "H,H,H")
A1._assert("A1-1812       N    10", 3.0)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-2012       N    40", 3.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H,H,H")
A1._assert("A1-1809       N    10", 3.5)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-2009       N    40", 3.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H,H,H")
A1._assert("A1-1806       N    10", 3.5)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-2006       N    40", 3.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H,H,H,H")
A1._assert("A1-1802       N    10", 4.0)
A2.move("LVL", "M", "H,H,H")
A2._assert("A1-2003       N    40", 3.5)
endgameturn()

endfile(__file__)
