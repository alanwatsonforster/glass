from airpower.tests.infrastructure import *
startfile(__file__, "stalled flight")

# Stalled flight

startsetup()
A1 = aircraft("A1", "F-80C", 1914, "N", 10, 1.0, configuration="DT")
A2 = aircraft("A2", "F-80C", 2114, "N",  3, 1.0, configuration="DT")
A3 = aircraft("A3", "F-80C", 2314, "N",  2, 1.0, configuration="DT")
endsetup()

startturn()
A1.move("ST", "M", "")
A1._assert("1914       N     8", 1.5)
A2.move("ST", "M", "JCL")
A2._assert("2114       N     1", 1.5)
A3.move("ST", "M", "JCL")
A3._assert("2314       N     0", 1.0)
endturn()

startturn()
A1.move("ST", "M", "")
A1._assert("1914       N     4", 2.5)
A2.move("LVL", "M", "H")
A2._assert("2113       N     1", 1.5)
endturn()

startturn()
A1.move("LVL", "M", "H,H")
A1._assert("1912       N     4", 3.0)
A2.move("LVL", "M", "H,H")
A2._assert("2111       N     1", 2.0)
endturn()

endfile(__file__)