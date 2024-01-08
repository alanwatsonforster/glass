from apxo.tests.infrastructure import *
startfile(__file__, "air-to-air attack elements")

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "Tu-4"   , "A2-2023", "E", 5, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C"  , "A2-2025", "N", 5, 4.0, "CL", gunammunition=3.5)
A4 = aircraft("A4", "AF", "Tu-4"   , "A2-2023", "E", 5, 4.0, "CL", gunammunition=11.0)
A5 = aircraft("A5", "AF", "F-89D"  , "A2-2023", "E", 5, 4.0, "CL")
A6 = aircraft("A6", "AF", "F-102A" , "A2-2023", "E", 5, 4.0, "CL", rocketfactors=0)
A7 = aircraft("A7", "AF", "F-100C" , "A2-2025", "N", 5, 6.0, "CL")
endtestsetup()

startturn()

A1.move("LVL", "M", "TTR/H/AA(GN)(A2)(L)")
A2.react("AA(GN)(A1)()(L)")
A1.continuemove("H/AA(GN/SS)(A2)(M)")
A2.react("AA(GN/SS)(A1)(L)")
A1.continuemove("H,H")
A2.move("LVL", "N", "H,H,H,H")
A1._assert("A2-2021       N     5", 4.0)
A2._assert("A2-2423       E     5", 3.5)
assert A1._gunammunition == 6.5
assert A2._gunammunition == 18.5

assert A3._gunammunition == 3.5
A3.move("LVL", "M", "H/AA(GN)(A4)(A)")
assert A3._gunammunition == 3.5
A3.continuemove("H/AA(GN)(A4)(-)")
assert A3._gunammunition == 2.5

assert A4._gunammunition == 11.0

assert A5._rocketfactors == 9
A5.move("LVL", "M", "H/AA(RK/3)(A2)(A)")
assert A5._rocketfactors == 9
A5.continuemove("H/AA(RK/3)(A2)(-)")
assert A5._rocketfactors == 6

assert A6._rocketfactors == 0

# Check SSGT and RR

startturn()
A7.move("LVL", "M", "H/AA(GN/RR)(A2)(-)")
asserterror("RE radar-ranging requires SSGT.")
startturn()
A7.move("LVL", "M", "SSGT/H/AA(GN/RR)(A2)(-)")
assert A7._gunammunition == 3.0
startturn()
A7.move("LVL", "M", "SSGT/H/AA(GN/SS/RR)(A2)(-)")
assert A7._gunammunition == 3.5
startturn()
A7.move("LVL", "M", "SSGT/H/AA(GN/RR/SS)(A2)(-)")
assert A7._gunammunition == 3.5

# Check recovery after ET.

startturn()
A7.move("LVL", "M", "ETR/H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H,H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H,H,H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H,H,H,H/AA(GN)()()")
A7._assert("A2-2221       NNE   5", 6.0)

# Check error if attack results are not specified at end of turn.
starttestsetup()
A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "Tu-4"   , "A2-2024", "N", 5, 3.0, "CL")
endtestsetup()

startturn()
A2.move("LVL", "FT", "H,H,H")
A1.move("LVL", "M", "H,H,H,H/AA(GN)(A2)()")
endturn()
asserterror("aircraft A1 has 1 unspecified attack result.")

startturn()
A2.move("LVL", "FT", "H,H,H")
A1.move("LVL", "M", "H,H,H/AA(GN)(A2)(),H/AA(GN)(A2)()")
endturn()
asserterror("aircraft A1 has 2 unspecified attack results.")
