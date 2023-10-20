from apengine.tests.infrastructure import *
startfile(__file__, "special flight")

# Close Formation flying limits

# Climbing and Diving

from apengine.tests.infrastructure import *

startsetup()
A1 = aircraft("A1", "O-1E", 2030, "N", 40, 0, "CL", color="green")

endsetup()

startturn()

A1.move("LVL", 0, "")
asserterror("special-flight aircraft cannot perform normal flight.")
A1.move("ST", 0, "")
asserterror("special-flight aircraft cannot perform stalled flight.")
A1.move("DP", 0, "")
asserterror("special-flight aircraft cannot perform departed flight.")


A1.move("SP", 0, "H,H,H")
A1._assert("2027       N    40", 0)
A1.move("SP", 0, "H,H,HR")
A1._assert("2027       NNE  40", 0)
A1.move("SP", 0, "H,H,HL")
A1._assert("2027       NNW  40", 0)
endturn()

startturn()
A1.move("SP", 0, "H,H,H")
A1._assert("1825/1924  NNW  40", 0)
A1.move("SP", 0, "H,H,HL")
A1._assert("1825       WNW  40", 0)
A1.move("SP", 0, "H,H,HR")
A1._assert("1924       N    40", 0)
endturn()

startturn()
A1.move("SP", 0, "H,H,CR")
endturn()

startturn()
A1.move("SP", 0, "H,H,CR")
endturn()

startturn()
A1.move("SP", 0, "H,H,CR")
endturn()

startturn()
A1.move("SP", 0, "H,H,CR")
endturn()

startturn()
A1.move("SP", 0, "H,H,CR")
A1._assert("2621       SSE  41", 0)
endturn()

startturn()

A1.move("SP", 0, "H,H,HR")
endturn()

startturn()
A1.move("SP", 0, "H,H,HR,H")
A1._assert("2627/2727  SSW  41", 0)
endturn()

startturn()
A1.move("SP", 0, "H,H,DR")
A1._assert("2528       WSW  40", 0)
endturn()


endfile(__file__)