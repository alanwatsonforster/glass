from apxo.tests.infrastructure import *

startfile(__file__, "variable-geometry aircraft")

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-111A", "A1-2010", "N", 5, 3.5, "CL", geometry="forward")
A2 = setupaircraft("A2", "AF", "F-111A", "A1-2210", "N", 5, 3.5, "CL", geometry="mid")
A3 = setupaircraft("A3", "AF", "F-111A", "A1-2410", "N", 5, 3.5, "CL", geometry="aft")
endtestsetup()

# Check geometry() works.
assert A1.geometry() == "forward"
assert A2.geometry() == "mid"
assert A3.geometry() == "aft"

# Check dependence of properties on geometry.
assert not A1.hasproperty("HBR")
assert not A2.hasproperty("HBR")
assert A3.hasproperty("HBR")

# Check geometry argument is required.
startgameturn()
A1.move("LVL", "N", "TTR/H/R H H")
asserterror("the geometry argument None is not valid.")

# Check dependence of allowed turn rate on geometry.
starttestsetup()
A1 = setupaircraft("A1", "AF", "F-111A", "A1-2010", "N", 5, 3.5, "CL", geometry="forward")
A2 = setupaircraft("A2", "AF", "F-111A", "A1-2210", "N", 5, 3.5, "CL", geometry="mid")
A3 = setupaircraft("A3", "AF", "F-111A", "A1-2410", "N", 5, 3.5, "CL", geometry="aft")
endtestsetup()
startgameturn()
A1.move("LVL", "N", "BTR/H/R H H", geometry="forward")
asserterror("aircraft does not allow a turn rate of BT.")
A2.move("LVL", "N", "BTR/H/R H H", geometry="mid")
A3.move("LVL", "N", "BTR/H/R H H", geometry="aft")

# Check dependence of turn drag on geomatry
starttestsetup()
A1 = setupaircraft("A1", "AF", "F-111A", "A1-2010", "N", 5, 3.5, "CL", geometry="forward")
A2 = setupaircraft("A2", "AF", "F-111A", "A1-2210", "N", 5, 3.5, "CL", geometry="mid")
A3 = setupaircraft("A3", "AF", "F-111A", "A1-2410", "N", 5, 3.5, "CL", geometry="aft")
endtestsetup()
startgameturn()
A1.move("LVL", "M", "HTR/H/R H H", geometry="forward")
A1._assert("A1-2107       NNE   5", 3.0)
A2.move("LVL", "M", "HTR/H/R H H", geometry="mid")
A2._assert("A1-2307       NNE   5", 3.0)
A3.move("LVL", "M", "HTR/H/R H H", geometry="aft")
A3._assert("A1-2507       NNE   5", 2.5)
endgameturn()

# Check dependence of minimum speed on geomatry
starttestsetup()
A1 = setupaircraft("A1", "AF", "F-111A", "A1-2010", "N", 5, 2.0, "CL", geometry="forward")
A2 = setupaircraft("A2", "AF", "F-111A", "A1-2210", "N", 5, 2.0, "CL", geometry="mid")
A3 = setupaircraft("A3", "AF", "F-111A", "A1-2410", "N", 5, 2.0, "CL", geometry="aft")
endtestsetup()
startgameturn()
A1.move("LVL", "M", "TTR/H/R H", geometry="forward")
A1._assert("A1-2008/2108 NNE 5", 2.0)
A2.move("LVL", "M", "TTR/H/R H", geometry="mid")
asserterror("speed limits the turn rate to EZ.")
A3.move("LVL", "M", "TTR/H/R H", geometry="aft")
asserterror("speed limits the turn rate to EZ.")

endfile(__file__)
