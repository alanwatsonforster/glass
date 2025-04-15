from apxo.tests.infrastructure import *

startfile(__file__, "close formations")

# Close Formations

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")

A1.joincloseformation(A2)

assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

A2.joincloseformation(A3)

assert A1.closeformationnames() == ["A1", "A2", "A3"]
assert A2.closeformationnames() == ["A1", "A2", "A3"]
assert A3.closeformationnames() == ["A1", "A2", "A3"]

A3.joincloseformation(A4)

assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

A2.leavecloseformation()

assert A1.closeformationnames() == ["A1", "A3", "A4"]
assert A2.closeformationnames() == []
assert A3.closeformationnames() == ["A1", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A3", "A4"]

A1.leavecloseformation()

assert A1.closeformationnames() == []
assert A2.closeformationnames() == []
assert A3.closeformationnames() == ["A3", "A4"]
assert A4.closeformationnames() == ["A3", "A4"]

A2.joincloseformation(A1)

assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
assert A3.closeformationnames() == ["A3", "A4"]
assert A4.closeformationnames() == ["A3", "A4"]

A1.joincloseformation(A3)
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]
endtestsetup()

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")

A5 = setupaircraft("A5", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")

A6 = setupaircraft("A6", "AF", "F-80C", "A1-2116", "N", 20, 4.0, "CL")
A7 = setupaircraft("A7", "AF", "F-80C", "A1-2115", "E", 20, 4.0, "CL")
A8 = setupaircraft("A8", "AF", "F-80C", "A1-2115", "N", 21, 4.0, "CL")
A9 = setupaircraft("A9", "AF", "F-80C", "A1-2115", "N", 20, 4.5, "CL")

A1.joincloseformation(A2)
A1.joincloseformation(A3)
A1.joincloseformation(A4)
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

A1.joincloseformation(A5)
asserterror("attempt to form a close formation with more than four aircraft.")

A1.leavecloseformation()

A1.joincloseformation(A6)
asserterror("attempt to form a close formation from aircraft with different positions.")

A1.joincloseformation(A7)
asserterror("attempt to form a close formation from aircraft with different facings.")

A1.joincloseformation(A8)
asserterror("attempt to form a close formation from aircraft with different altitudes.")

A1.joincloseformation(A9)
asserterror("attempt to form a close formation from aircraft with different speeds.")

endtestsetup()

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2115", "N", 20, 4.0, "CL")

A1.joincloseformation(A2)
A1.joincloseformation(A3)
A1.joincloseformation(A4)
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

endtestsetup()

startgameturn()

assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

A1.move("LVL", "M", "H,H,H,H")
A2.move("LVL", "M", "H,H,H,H")
A3.move("LVL", "M", "H,H,H,H")
A4.move("LVL", "M", "H,H,H,H")

assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

endgameturn()

startgameturn()

assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

A1.move("LVL", "M", "H,H,H,H")
A2.move("LVL", "M", "H,H,H,H")
A3.move("LVL", "M", "H,H,H,H")
A4.move("LVL", "M", "EZR/H,H,H,H/R")

assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

endgameturn()
asserterror(
    "aircraft A1 and A4 cannot be in close formation as they do not have the same facings."
)

endfile(__file__)
