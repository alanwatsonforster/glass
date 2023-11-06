from apengine._tests.infrastructure import *
startfile(__file__, "air-to-air attack elements")

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "Tu-4"   , "2023", "E", 5, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL", "M", "TTR/H/AA(GN)(A2)(L)")
A2.react("AA(GN)(A1)(L)")
A1.continuemove("H/AA(SSGN)(A2)(M)")
A2.react("AA(SSGN)(A1)(L)")
A1.continuemove("H,H")
A2.move("LVL", "N", "H,H,H,H")

A1._assert("2021       N     5", 4.0)
A2._assert("2423       E     5", 3.5)
assert A1._gunammunition == 5
assert A2._gunammunition == 17
endturn()