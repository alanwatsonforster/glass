from apxo.tests.infrastructure import *

startfile(__file__, "attacks after rolls")

# Attacks after Rolls

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "A1-2015", "N", 20, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-2015", "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A2.move("LVL", "M", "DRR/H,H/R,H,H")
A1.move("LVL", "M", "DRR/H,H/R,H,H")
A1._assert("A1-2111       N    20", 4.0)

startgameturn()
A2.move("LVL", "M", "DRR/H,H/R")
A1.move("LVL", "M", "DRR/H,H/R")
A1.attackaircraft(A2, "GN")
asserterror("attempt to use weapons immediately after rolling.")

startgameturn()
A2.move("HRD/VD", "M", "H,D2,D2,D2")
A1.move("HRD/VD", "M", "H,D2,D2,D2")
A1.attackaircraft(A2, "GN")
asserterror("attempt to use weapons after HRD.")

startgameturn()
A2.move("HRD/VD", "M", "H,D2,D2,D2")
A1.move("HRD/VD", "M", "H,D2,D2,D2")
A1._assert("A1-2014       N    14", 5.5)
endgameturn()

startgameturn()
A2.move("VD", "M", "D2,D2,VRR/D2/R")
A1.move("VD", "M", "D2,D2,VRR/D2/R")
A1.attackaircraft(A2, "GN")
asserterror("attempt to use weapons immediately after rolling.")

startgameturn()
A2.move("VD", "M", "D2,D2,VRR/D2/R,D2,D2")
A1.move("VD", "M", "D2,D2,VRR/D2/R,D2,D2")
A1._assert("A1-2014       NNE   4", 6.5)
endgameturn()

endfile(__file__)
