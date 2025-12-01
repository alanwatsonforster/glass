from glass.tests.infrastructure import *

startfile(__file__, "unloading")

# Unloading in level flight.

starttestsetup(variants=["use house rules"])
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "N", 20, 3.0, "CL")
endtestsetup()

startgameturn()
A1.move("UD", "N")
asserterror("invalid flight type 'UD'.")

startgameturn()
A1.move("LVL", "M", "HU H HU")
asserterror("unloaded HFPs must be continuous.")

startgameturn()
A1.move("LVL", "N", "H HU H")
A1._assert("A1-1812       N    20", 3.0)

startgameturn()
A1.move("LVL", "N", "HUD H H")
asserterror("FP 1 cannot be HUD.")

startgameturn()
A1.move("LVL", "N", "HU HU H")
asserterror("FP 2 cannot be HU.")

startgameturn()
A1.move("LVL", "N", "HU HUD H")
A1._assert("A1-1812       N    19", 3.0)

startgameturn()
A1.move("LVL", "M", "HU HUD H")
A1._assert("A1-1812       N    19", 3.5)

startgameturn()
A1.move("LVL", "N", "H HU HU")
asserterror("FP 3 cannot be HU.")

startgameturn()
A1.move("LVL", "N", "H HU HUD")
A1._assert("A1-1812       N    19", 3.0)

startgameturn()
A1.move("LVL", "M", "H HU HUD")
A1._assert("A1-1812       N    19", 3.5)

startgameturn()
A1.move("LVL", "N", "HU HUD HU")
asserterror("FP 3 cannot be HU.")

startgameturn()
A1.move("LVL", "N", "HU HUD HUD")
A1._assert("A1-1812       N    18", 3.5)

# Aircraft ends in LVL if not all FPs are unloaded.

starttestsetup(variants=["use house rules"])
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "HU HUD H H")
A1._assert("A1-1811       N    19", 4.5)
endgameturn()
startgameturn()
A1.move("ZC", "M", "C H H H")
asserterror("insufficient initial HFPs.")
startgameturn()
A1.move("ZC", "M", "H C H H")
A1._assert("A1-1808       N    20", 4.5)
startgameturn()
A1.move("ZC", "M", "H H C H")
A1._assert("A1-1808       N    20", 4.5)

# Aircraft ends in SD if all FPs are unloaded.

starttestsetup(variants=["use house rules"])
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "N", "HU HUD HU HUD")
A1._assert("A1-1811       N    18", 4.5)
endgameturn()
startgameturn()
A1.move("ZC", "M", "C H H H")
asserterror("insufficient initial HFPs.")
startgameturn()
A1.move("ZC", "M", "H C H H")
asserterror("insufficient initial HFPs.")
startgameturn()
A1.move("ZC", "M", "H H C H")
A1._assert("A1-1808       N    19", 4.5)

endgameturn()

# Verify that attacks cannot happen on unloaded FPs.

starttestsetup(variants=["use house rules"])
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2015", "N", 20, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A2.move("LVL", "M", "HU HUD HU HUD")
A1.move("LVL", "M", "HU HUD HU HUD")
A1._assert("A1-2011       N    18", 4.5)
startgameturn()
A2.move("LVL", "M", "HU HUD HU HUD")
A1.move("LVL", "M", "HU HUD HU HUD")
A1.attack(A2, "GN")
asserterror("attempt to use weapons while unloaded.")

endfile(__file__)
