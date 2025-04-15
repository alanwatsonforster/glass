from glass.tests.infrastructure import *

startfile(__file__, "close formation flying limits")

# Close Formation flying limits

# Climbing and Diving

from glass.tests.infrastructure import *

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("LVL", "AB", "H,H,H,H,H")
A2.move("LVL", "AB", "H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("ZC", "AB", "H,H,H,H,C")
A2.move("ZC", "AB", "H,H,H,H,C")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SC", "AB", "H,H,H,H,C")
A2.move("SC", "AB", "H,H,H,H,C")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SC", "M", "H,H,H,H,C")
A2.move("SC", "M", "H,H,H,H,C")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SC", "M", "H,H,H,C,C")
A2.move("SC", "M", "H,H,H,C,C")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SC", "M", "H,H,C,C,C")
A2.move("SC", "M", "H,H,C,C,C")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SC", "M", "H,H,H,C,C")
A2.move("SC", "M", "H,H,H,C,C")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
startgameturn()
A1.move("VC", "M", "H,H,C2,C2,C2")
A2.move("VC", "M", "H,H,C2,C2,C2")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SD", "M", "H,H,H,D,D")
A2.move("SD", "M", "H,H,H,D,D")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SD", "M", "H,H,D,D,D")
A2.move("SD", "M", "H,H,D,D,D")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("UD", "M", "H,H,H,H,HD")
A2.move("UD", "M", "H,H,H,H,HD")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startgameturn()
A1.move("SD", "M", "H,H,H,D,D")
A2.move("SD", "M", "H,H,H,D,D")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
startgameturn()
A1.move("VD", "M", "H,H,D2,D2,D2")
A2.move("VD", "M", "H,H,D2,D2,D2")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

from glass.tests.infrastructure import *

# Turns with 4 aircraft formations

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A3 = setupaircraft("A3", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A4 = setupaircraft("A4", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
A1.joincloseformation(A3)
A1.joincloseformation(A4)
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]
endtestsetup()

startgameturn()
A1.move("LVL", "N", "TTR/H,H,H,H,H")
A2.move("LVL", "N", "TTR/H,H,H,H,H")
A3.move("LVL", "N", "TTR/H,H,H,H,H")
A4.move("LVL", "N", "TTR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

startgameturn()
A1.move("LVL", "N", "HTR/H,H,H,H,H")
A2.move("LVL", "N", "HTR/H,H,H,H,H")
A3.move("LVL", "N", "HTR/H,H,H,H,H")
A4.move("LVL", "N", "HTR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []
assert A3.closeformationnames() == []
assert A4.closeformationnames() == []

# Turns with 3 aircraft formations

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A3 = setupaircraft("A3", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
A1.joincloseformation(A3)
assert A1.closeformationnames() == ["A1", "A2", "A3"]
assert A2.closeformationnames() == ["A1", "A2", "A3"]
assert A3.closeformationnames() == ["A1", "A2", "A3"]
endtestsetup()

startgameturn()
A1.move("LVL", "N", "TTR/H,H,H,H,H")
A2.move("LVL", "N", "TTR/H,H,H,H,H")
A3.move("LVL", "N", "TTR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2", "A3"]
assert A2.closeformationnames() == ["A1", "A2", "A3"]
assert A3.closeformationnames() == ["A1", "A2", "A3"]

startgameturn()
A1.move("LVL", "N", "HTR/H,H,H,H,H")
A2.move("LVL", "N", "HTR/H,H,H,H,H")
A3.move("LVL", "N", "HTR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []
assert A3.closeformationnames() == []

# Turns with 2 aircraft formations

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startgameturn()
A1.move("LVL", "N", "HTR/H,H,H,H,H")
A2.move("LVL", "N", "HTR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

startgameturn()
A1.move("LVL", "N", "BTR/H,H,H,H,H")
A2.move("LVL", "N", "BTR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

# Slides

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startgameturn()
A1.move("LVL", "N", "SLR/H,H,H,H,H")
A2.move("LVL", "N", "SLR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

# Rolls

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startgameturn()
A1.move("LVL", "N", "DRR/H,H,H,H,H")
A2.move("LVL", "N", "DRR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A2-1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startgameturn()
A1.move("LVL", "N", "LRR/H,H,H,H,H")
A2.move("LVL", "N", "LRR/H,H,H,H,H")
endgameturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

endfile(__file__)
