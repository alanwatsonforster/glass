from apxo.tests.infrastructure import *

startfile(__file__, "gloc")

# GLOC Warning The check for a GLOC warning is not automated. However, the
# warnings can be seen by running the code with verbose=True.

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-100A", "A1-1215", "N", 25, 6.5, "CL")
A2 = aircraft("A2", "AF", "F-100A", "A1-1415", "N", 25, 6.5, "CL")
A3 = aircraft("A3", "AF", "F-100A", "A1-1615", "N", 26, 6.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "ETR/H/R,ETR/H/R+,H/R+,H/R+,H/R+,H/R+")
A1._assert("A1-1615       S    25", 4.5)
A2.move("LVL", "AB", "BTR/H,H/R+,H,H/R+,H,H/R+")
A2._assert("A1-1710       E    25", 6.0)
A3.move("LVL", "AB", "ETR/H,H/R+,H,H/R+,H,H/R+")
A3._assert("A1-1910       E    26", 5.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "BTR/H/R+,H/WL,H,H,H")
A1._assert("A2-1419       SSW  25", 4.0)
A2.move("LVL", "AB", "ETR/H/R+,H/R+,H/R+,H/R+,H/R+,BTR/H")
A2._assert("A1-1714       WSW  25", 4.5)
A3.move("LVL", "AB", "BTR/H,H,H/R+,H,H,H/R+")
A3._assert("A1-2512       SSE  26", 4.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "HTL/H,H/L,HTL/H,H")
A1._assert("A2-1322       S    25", 4.0)
A2.move("LVL", "AB", "ETR/H/RR+,H/RR+,H/RR+,H/RR+,H/WL")
A2._assert("A1-1713       ESE  25", 2.0)
A3.move("LVL", "AB", "BTR/H,H,H/R+,H")
A3._assert("A1-2616       S    26", 4.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "H/L+,H,H/L+,H")
A1._assert("A2-1525       ESE  25", 4.0)
A2.move("ST", "AB", "")
A2._assert("A1-1713       ESE  23", 2.5)
A3.move("LVL", "AB", "BTR/H,H,H/R+,H,H")
A3._assert("A2-2520       SSW  26", 4.5)
endgameturn()

endfile(__file__)
