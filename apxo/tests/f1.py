from apxo.tests.infrastructure import *
startfile(__file__, "stalled flight")

# Stalled flight

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-80C", "1914", "N", 10, 1.0, configuration="DT")
A2 = aircraft("A2", "AF", "F-80C", "2114", "N",  3, 1.0, configuration="DT")
A3 = aircraft("A3", "AF", "F-80C", "2314", "N",  2, 1.0, configuration="DT")
endtestsetup()

startturn()
A1.move("ST", "M", "")
A1._assert("1914       N     9", 1.0)
A2.move("ST", "M", "")
A2._assert("2114       N     2", 1.0)
A3.move("ST", "M", "")
A3._assert("2314       N     1", 1.0)
endturn()

startturn()
A1.move("ST", "M", "")
A1._assert("1914       N     7", 2.0)
A2.move("ST", "M", "")
A2._assert("2114       N     0", 1.0)
A3.move("ST", "M", "")
A3._assert("2314       N     0", 1.0)
endturn()

startturn()
A1.move("LVL", "M", "H,H")
A1._assert("1912       N     7", 2.0)
endturn()

# Check jettisoning.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "2024", "N", 10, 1.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
                "2": "BB/M57",
                "3": "BB/M57"
              })
A1._assert("2024       N    10", 1.0, configuration="DT")
endtestsetup()

startturn()
A1.move("ST", "N", "J(BB)")
A1._assert("2024       N     9", 1.0, configuration="1/2")
endturn()

startturn()
A1.move("ST", "N", "J(1+4)")
A1._assert("2024       N     7", 1.5, configuration="CL")
endturn()


endfile(__file__)