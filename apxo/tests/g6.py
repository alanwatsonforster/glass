from apxo.tests.infrastructure import *

startfile(__file__, "attacks after rolls")

# Attacks after Rolls

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "A1-2015", "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "DRR/H,HR,H,H")
A1._assert("A1-2111       N    20", 4.0)
startgameturn()
A1.move("LVL", "M", "DRR/H,HR/AA(GN)()(),H,H")
asserterror("attempt to use weapons immediately after rolling.")
startgameturn()
A1.move("VD/HRD", "M", "H,D2,D2,D2/AA(GN)()()")
asserterror("attempt to use weapons after HRD.")
startgameturn()
A1.move("VD/HRD", "M", "H,D2,D2,D2")
A1._assert("A1-2014       N    14", 5.5)
endgameturn()

startgameturn()
A1.move("VD", "M", "D2,D2,VRR/D2/RAA(GN)()(),D2,D2")
asserterror("attempt to use weapons immediately after rolling.")
startgameturn()
A1.move("VD", "M", "D2,D2,VRR/D2/R,D2,D2")
A1._assert("A1-2014       NNE   4", 6.5)
endgameturn()

endfile(__file__)
