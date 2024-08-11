from apxo.tests.infrastructure import *

startfile(__file__, "slatted wings")

# Turns with slatted wings.

starttestsetup()
A1 = aircraft("A1", "AF", "F-100A", "A1-1110", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-100A", "A1-1310", "N", 10, 4.5, "CL")
endtestsetup()
startgameturn()
A1.move("LVL", "AB", "BTR/HRR,BTR/HRR,BTR/HRR,BTR/HR")
A1._assert("A1-1310       SSW  10", 2.5)
A2.move("LVL", "AB", "BTR/HRR,BTR/HRR,BTR/HRR,BTR/HR")
A2._assert("A1-1510       SSW  10", 3.0)
endgameturn()

# Turns with selectable slats.

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-5A", "A1-1110", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-5A", "A1-1310", "N", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "BTR/HRR,BTR/HRR,BTR/HRR,BTR/HR", lowspeedliftdeviceselected=True)
A1._assert("A1-1310       SSW  10", 2.5)
A2.move("LVL", "AB", "BTR/HRR,BTR/HRR,BTR/HRR,BTR/HR")
A2._assert("A1-1510       SSW  10", 3.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "HTR/HRRR,HTR/HRRR")
A1._assert("A1-1110       NNE  10", 1.5)
A2.move("LVL", "AB", "HTR/HRR,HTR/HRR,HTR/HRR")
A2._assert("A1-1309       NNE  10", 2.0)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H,H")
A1._assert("A1-1209       NNE  10", 1.5)
A2.move("LVL", "AB", "H,H")
A2._assert("A1-1408       NNE  10", 2.0)
endgameturn()

endfile(__file__)
