from airpower.tests.infrastructure import *
startfile(__file__, "forward movement")

# Check basic movement.


# H movements.

startsetup()
A1 = aircraft("A1", "F-80C", 1115, "N", 10, 2.5, "CL")
A2 = aircraft("A2", "F-80C", 1315, "N", 10, 3.0, "CL")
A3 = aircraft("A3", "F-80C", 1515, "N", 10, 3.5, "CL")
A4 = aircraft("A4", "F-80C", 1715, "N", 10, 4.0, "CL")
endsetup()

A1._assert("1115       N    10", 2.5)
A2._assert("1315       N    10", 3.0)
A3._assert("1515       N    10", 3.5)
A4._assert("1715       N    10", 4.0)

startturn()
A1.move("LVL",  "N", "H,H"    )
A1._assert("1113       N    10",  2.5)
A2.move("LVL",  "N", "H,H,H"  )
A2._assert("1312       N    10",  3.0)
A3.move("LVL",  "N", "H,H,H"  )
A3._assert("1512       N    10",  3.5)
A4.move("LVL",  "N", "H,H,H,H")
A4._assert("1711       N    10",  4.0)
endturn()

startturn()
A1.move("LVL",  "N", "H,H,H"  )
A1._assert("1110       N    10",  2.5)
A2.move("LVL",  "N", "H,H,H"  )
A2._assert("1309       N    10",  3.0)
A3.move("LVL",  "N", "H,H,H,H")
A3._assert("1508       N    10",  3.5)
A4.move("LVL",  "N", "H,H,H,H")
A4._assert("1707       N    10",  4.0)
endturn()

startturn()
A1.move("LVL",  "N", "H,H"    )
A1._assert("1108       N    10",  2.5)
A2.move("LVL",  "N", "H,H,H"  )
A2._assert("1306       N    10",  3.0)
A3.move("LVL",  "N", "H,H,H"  )
A3._assert("1505       N    10",  3.5)
A4.move("LVL",  "N", "H,H,H,H")
A4._assert("1703       N    10",  4.0)
endturn()

startsetup()
A1 = aircraft("A1", "F-80C", 1830, "N", 12, 1.5, "CL")
A2 = aircraft("A2", "F-80C", 2030, "N", 12, 2.0, "CL")
endsetup()

for i in range(1, 10, 2):
  startturn()
  A1.move("LVL", 0.0, "H")
  A2.move("LVL", 0.0, "H,H")
  endturn()
  startturn()
  A1.move("LVL", 0.0, "H,H")
  A2.move("LVL", 0.0, "H,H")
  endturn()

A1._assert("1815       N    12", 1.5)
A2._assert("2010       N    12", 2.0)

# HC and HD combinations.

startsetup()
A1 = aircraft("A1", "F-80C" , 1115, "N"  , 10, 4.0, "CL")
A2 = aircraft("A1", "F-80C" , 1315, "N"  , 10, 4.0, "CL")
endsetup()

startturn()
A1.move("SD",  "N", "H,H,H,HD")
asserterror("'HD' is not a valid action when the flight type is SD.")
A1.move("UD",  "N", "H,H,H,HD")
A1._assert("1111       N     9",  4.0)
A1.move("LVL",  "N", "H,H,H,HD")
A1._assert("1111       N     9",  4.0)
A1.move("LVL",  "N", "H,H,H,HC")
asserterror("attempt to climb while flight type is LVL.")
A1.move("ZC",  "N", "H,H,H,HC")
asserterror("'HC' is not a valid action when the flight type is ZC.")
A1.move("SC",  "N", "H,H,H,HC")
asserterror("'HC' is not a valid action when the flight type is SC.")
A1.move("SC",  "N", "H,H,H,H")
A1._assert("1111       N    10",  4.0)
A2.move("SD",  "N", "H,H,H,H")
A2._assert("1311       N    10",  4.0)
endturn()

startturn()
A1.move("VC",  "N", "H,H,H,HC")
asserterror("'HC' is not a valid action when the flight type is VC.")
A1.move("VC",  "N", "H,C,C,C")
A1._assert("1110       N    13",  2.5)
A2.move("VD",  "N", "H,H,H,HD2")
asserterror("'HD2' is not a valid action when the flight type is VD.")
A2.move("VD",  "N", "H,D2,D2,D2")
A2._assert("1310       N     4",  5.5)
endturn()

endfile(__file__)