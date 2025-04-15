from glass.tests.infrastructure import *

startfile(__file__, "slatted wings")

# Turns with slatted wings.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-100A", "A1-1110", "N", 10, 3.5, "CL")
A2 = setupaircraft("A2", "AF", "F-100A", "A1-1310", "N", 10, 4.0, "CL")
endtestsetup()
startgameturn()
A1.move("LVL", "AB", "BTR/H/RR,BTR/H/RR,BTR/H/RR")
A1._assert("A1-1309       S    10", 2.0)
A2.move("LVL", "AB", "BTR/H/RR,BTR/H/RR,BTR/H/RR,H")
A2._assert("A1-1510       S  10", 3.0)
endgameturn()

# Turns with selectable slats.

starttestsetup()
A1 = setupaircraft("A1", "AF", "MiG-21bis", "A1-1110", "N", 10, 2.5, "CL")
A2 = setupaircraft("A2", "AF", "MiG-21bis", "A1-1310", "N", 10, 2.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "TTR/H/RR,TTR/H/RR", lowspeedliftdeviceselected=True)
A1._assert("A1-1209       ESE  10", 2.0)
A2.move("LVL", "AB", "TTR/H/RR,TTR/H/RR")
asserterror("speed limits the turn rate to EZ.")

# A-7D/E automatic maneuvering flaps, which are automatic but also change min speed.

starttestsetup()
A1 = setupaircraft("A1", "AF", "A-7E (1980 Upgrade)", "A1-1110", "N", 40, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "A-7E (1980 Upgrade)", "A1-1112", "N", 40, 3.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "N", "HTR/H/R,H,H,H")
asserterror("speed limits the turn rate to TT.")
A2.move("LVL", "N", "HTR/H/R,H,H")
asserterror("speed limits the turn rate to TT.")

endfile(__file__)
