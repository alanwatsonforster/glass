from apxo.tests.infrastructure import *
startfile(__file__, "attacks after rolls")

# Attacks after Rolls

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "2015", "N", 20, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL"   ,  "M", "DRR/H,HR,H,H"    )
A1._assert("2111       N    20",  4.0)
startturn()
A1.move("LVL"   ,  "M", "DRR/H,HR,H/AA(GN)()(),H")
asserterror("attempt to use weapons on the FP immediately after rolling.")
startturn()
A1.move("VD/HRD",  "M", "H,D2,D2,D2/AA(GN)()()"  )
asserterror("attempt to use weapons during the turn after an HRD.")
startturn()
A1.move("VD/HRD",  "M", "H,D2,D2,D2"      )
A1._assert("2014       N    14",  5.5)
endturn()

startturn()
A1.move("VD"    ,  "M", "D2,D2,VRR/D2/R,D2/AA(GN)()(),D2")
asserterror("attempt to use weapons on the FP immediately after rolling.")
startturn()
A1.move("VD"    ,  "M", "D2,D2,VRR/D2/R,D2,D2"    )
A1._assert("2014       NNE   4",  6.5)
endturn()

endfile(__file__)