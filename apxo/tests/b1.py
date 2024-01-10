from apxo.tests.infrastructure import *
startfile(__file__, "order of elements")

# Check basic movement.

# H movements.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 2.5, "CL")
endtestsetup()

startturn()
A1.move("LVL", "M", "WL/H")
asserterror("unexpected WL element in action prolog.")

startturn()
A1.move("LVL", "M", "H/TTR")
asserterror("unexpected TTR element in action epilog.")