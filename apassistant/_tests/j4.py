from apassistant._tests.infrastructure import *
startfile(__file__, "air-to-air attack elements")

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "Tu-4"   , "2023", "E", 5, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2025", "N", 5, 4.0, "CL", gunammunition=3.5)
A4 = aircraft("A4", "Tu-4"   , "2023", "E", 5, 4.0, "CL", gunammunition=11.0)
A5 = aircraft("A5", "F-89D"  , "2023", "E", 5, 4.0, "CL")
A6 = aircraft("A6", "F-102A" , "2023", "E", 5, 4.0, "CL", rocketfactors=0)
endtestsetup()

startturn()

A1.move("LVL", "M", "TTR/H/AA(GN)(A2)(L)")
A2.react("AA(GN)(A1)(L)")
A1.continuemove("H/AA(GNSS)(A2)(M)")
A2.react("AA(GNSS)(A1)(L)")
A1.continuemove("H,H")
A2.move("LVL", "N", "H,H,H,H")

A1._assert("2021       N     5", 4.0)
A2._assert("2423       E     5", 3.5)
assert A1._gunammunition == 6.5
assert A2._gunammunition == 18.5

assert A3._gunammunition == 3.5
assert A4._gunammunition == 11.0

assert A5._rocketfactors == 9
A5.move("LVL", "M", "H/AA(RK3)(A2)()")
assert A5._rocketfactors == 6

assert A6._rocketfactors == 0

