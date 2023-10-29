from apengine._tests.infrastructure import *
startfile(__file__, "stalled flight")

# Stalled flight

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-80C", "1914", "N", 10, 1.0, configuration="DT")
A2 = aircraft("A2", "F-80C", "2114", "N",  3, 1.0, configuration="DT")
A3 = aircraft("A3", "F-80C", "2314", "N",  2, 1.0, configuration="DT")
endtestsetup()

startturn()
A1.move("ST", "M", "")
A1._assert("1914       N     9", 1.0)
A2.move("ST", "M", "JCL")
A2._assert("2114       N     2", 1.0)
A3.move("ST", "M", "JCL")
A3._assert("2314       N     1", 1.0)
endturn()

startturn()
A1.move("ST", "M", "")
A1._assert("1914       N     7", 2.0)
A2.move("ST", "M", "")
A2._assert("2114       N     0", 1.0)
A3.move("ST", "M", "")
A3._assert("2314       N     0", 1.0)
endturn()

startturn()
A1.move("LVL", "M", "H,H")
A1._assert("1912       N     7", 2.0)
endturn()

endfile(__file__)