from glass.tests.infrastructure import *

startfile(__file__, "order of actions")

# Check basic movement.

# H movements.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 2.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "WL/H")
asserterror("unexpected WL action in prolog of 'WL/H'.")

startgameturn()
A1.move("LVL", "M", "H/TTR")
asserterror("unexpected TTR action in epilog of 'H/TTR'.")
