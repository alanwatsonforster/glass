from apxo.tests.infrastructure import *
startfile(__file__, "slatted wings")

# Turns with slatted wings.

starttestsetup()
A1 = aircraft("A1", "AF", "F-100A" , "1110", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-100A" , "1310", "N", 10, 4.5, "CL")
endtestsetup()
startturn()
A1.move("LVL",  "AB", "BTR/HRR,BTR/HRR,BTR/HRR,BTR/HR")
A1._assert("1310       SSW  10",  2.5)
A2.move("LVL",  "AB", "BTR/HRR,BTR/HRR,BTR/HRR,BTR/HR")
A2._assert("1510       SSW  10",  3.0)
endturn()


endfile(__file__)