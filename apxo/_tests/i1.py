from apxo._tests.infrastructure import *
startfile(__file__, "close formation flying limits")

# Close Formation flying limits

# Climbing and Diving

from apxo._tests.infrastructure import *

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("LVL", "AB", "H,H,H,H,H")
A2.move("LVL", "AB", "H,H,H,H,H")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("ZC", "AB", "H,H,H,H,C")
A2.move("ZC", "AB", "H,H,H,H,C")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SC", "AB", "H,H,H,H,C")
A2.move("SC", "AB", "H,H,H,H,C")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SC", "M", "H,H,H,H,C")
A2.move("SC", "M", "H,H,H,H,C")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SC", "M", "H,H,H,C,C")
A2.move("SC", "M", "H,H,H,C,C")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SC", "M", "H,H,C,C,C")
A2.move("SC", "M", "H,H,C,C,C")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SC", "M", "H,H,H,C,C")
A2.move("SC", "M", "H,H,H,C,C")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
startturn()
A1.move("VC", "M", "H,H,C2,C2,C2")
A2.move("VC", "M", "H,H,C2,C2,C2")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SD", "M", "H,H,H,D,D")
A2.move("SD", "M", "H,H,H,D,D")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SD", "M", "H,H,D,D,D")
A2.move("SD", "M", "H,H,D,D,D")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("UD", "M", "H,H,H,H,HD")
A2.move("UD", "M", "H,H,H,H,HD")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()
startturn()
A1.move("SD", "M", "H,H,H,D,D")
A2.move("SD", "M", "H,H,H,D,D")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
startturn()
A1.move("VD", "M", "H,H,D2,D2,D2")
A2.move("VD", "M", "H,H,D2,D2,D2")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

from apxo._tests.infrastructure import *

# Turns with 4 aircraft formations

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A3 = aircraft("A3", "F-104A", "1530", "N", 10, 5.0, "CL")
A4 = aircraft("A4", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
A1.joincloseformation(A3)
A1.joincloseformation(A4)
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]
endtestsetup()

startturn()
A1.move("LVL", "N", "TTR/H,H,H,H,H")
A2.move("LVL", "N", "TTR/H,H,H,H,H")
A3.move("LVL", "N", "TTR/H,H,H,H,H")
A4.move("LVL", "N", "TTR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A2.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A3.closeformationnames() == ["A1", "A2", "A3", "A4"]
assert A4.closeformationnames() == ["A1", "A2", "A3", "A4"]

startturn()
A1.move("LVL", "N", "HTR/H,H,H,H,H")
A2.move("LVL", "N", "HTR/H,H,H,H,H")
A3.move("LVL", "N", "HTR/H,H,H,H,H")
A4.move("LVL", "N", "HTR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []
assert A3.closeformationnames() == []
assert A4.closeformationnames() == []

# Turns with 3 aircraft formations

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A3 = aircraft("A3", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
A1.joincloseformation(A3)
assert A1.closeformationnames() == ["A1", "A2", "A3"]
assert A2.closeformationnames() == ["A1", "A2", "A3"]
assert A3.closeformationnames() == ["A1", "A2", "A3"]
endtestsetup()

startturn()
A1.move("LVL", "N", "TTR/H,H,H,H,H")
A2.move("LVL", "N", "TTR/H,H,H,H,H")
A3.move("LVL", "N", "TTR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == ["A1", "A2", "A3"]
assert A2.closeformationnames() == ["A1", "A2", "A3"]
assert A3.closeformationnames() == ["A1", "A2", "A3"]

startturn()
A1.move("LVL", "N", "HTR/H,H,H,H,H")
A2.move("LVL", "N", "HTR/H,H,H,H,H")
A3.move("LVL", "N", "HTR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []
assert A3.closeformationnames() == []

# Turns with 2 aircraft formations

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startturn()
A1.move("LVL", "N", "HTR/H,H,H,H,H")
A2.move("LVL", "N", "HTR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

startturn()
A1.move("LVL", "N", "BTR/H,H,H,H,H")
A2.move("LVL", "N", "BTR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

# Slides

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startturn()
A1.move("LVL", "N", "SLR/H,H,H,H,H")
A2.move("LVL", "N", "SLR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]

# Rolls

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startturn()
A1.move("LVL", "N", "DRR/H,H,H,H,H")
A2.move("LVL", "N", "DRR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

starttestsetup()
A1 = aircraft("A1", "F-104A", "1530", "N", 10, 5.0, "CL")
A2 = aircraft("A2", "F-104A", "1530", "N", 10, 5.0, "CL")
A1.joincloseformation(A2)
assert A1.closeformationnames() == ["A1", "A2"]
assert A2.closeformationnames() == ["A1", "A2"]
endtestsetup()

startturn()
A1.move("LVL", "N", "LRR/H,H,H,H,H")
A2.move("LVL", "N", "LRR/H,H,H,H,H")
endturn()
assert A1.closeformationnames() == []
assert A2.closeformationnames() == []

endfile(__file__)