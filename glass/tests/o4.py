from glass.tests.infrastructure import *

startfile(__file__, "ground unit movement")

starttestsetup()

G0 = setupgroundunit("G0", "A1-2120", symbols="infantry")
G1 = setupgroundunit("G1", "A1-2120", symbols="airdefense/gun", aaaclass="H", azimuth="N")
endtestsetup()

startgameturn()
G0._assert("A2-2120 --- 0", None)
G0.move("N")
G0._assert("A2-2119 --- 0", None)
G0.continuemove("A1-2118")
G0._assert("A2-2118 --- 0", None)

startgameturn()
G0.continuemove("N")
asserterror("G0 has not started moving.")

startgameturn()
G0.move("N")
G0.move("NNW")
asserterror("G0 has already started moving.")

startgameturn()
G0.move("NNW")
asserterror('invalid azimuth "NNW" for move.')

startgameturn()
G0.move("R")
asserterror('invalid move "R".')

startgameturn()
G1._assert("A2-2120 N   0", None)
G1.move("R")
G1._assert("A2-2120 NNE 0", None)
G1.continuemove("R30")
G1._assert("A2-2120 ENE 0", None)
G1.continuemove("RR")
G1._assert("A2-2120 ESE 0", None)
G1.continuemove("R60")
G1._assert("A2-2120 S   0", None)

startgameturn()
G1._assert("A2-2120 N   0", None)
G1.move("L")
G1._assert("A2-2120 NNW 0", None)
G1.continuemove("L30")
G1._assert("A2-2120 WNW 0", None)
G1.continuemove("LL")
G1._assert("A2-2120 WSW 0", None)
G1.continuemove("L60")
G1._assert("A2-2120 S   0", None)


endfile(__file__)
