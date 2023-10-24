from apengine._tests.infrastructure import *
startfile(__file__, "jettisoning stores")

# Jettisoning Stores

starttestsetup()
A1 = aircraft("A1", "F-80C", "1815", "N"  , 10, 3.0, "DT")
endtestsetup()

A1._assert("1815       N    10", 3.0, configuration="DT")

startturn()

A1.move("LVL",  "M", "H/J1/2,H,H")
A1._assert("1812       N    10",  3.0, configuration="1/2")

A1.move("LVL",  "M", "H/JCL,H,H")
A1._assert("1812       N    10",  3.0, configuration="CL")

A1.move("LVL",  "M", "H/J1/2,H/J1/2,H")
asserterror("configuration is already 1/2.")

A1.move("LVL",  "M", "H/JCL,H/JCL,H")
asserterror("configuration is already CL.")

A1.move("LVL",  "M", "H/JCL,H/J1/2,H")
asserterror("attempt to change from configuration CL to 1/2.")

endturn()

endfile(__file__)