from apxo.tests.infrastructure import *

startfile(__file__, "angle-off")

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2025", "N", 5, 4.0, "CL")

A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "N", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "0 line"
A2 = setupaircraft("B2", "AF", "F-80C", "A2-2023", "NNW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"
A2 = setupaircraft("C2", "AF", "F-80C", "A2-2023", "WNW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "60 arc"
A2 = setupaircraft("D2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"
A2 = setupaircraft("E2", "AF", "F-80C", "A2-2023", "WSW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "150 arc"
A2 = setupaircraft("F2", "AF", "F-80C", "A2-2023", "SSW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("G2", "AF", "F-80C", "A2-2023", "S", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 line"
A2 = setupaircraft("H2", "AF", "F-80C", "A2-2023", "SSE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("I2", "AF", "F-80C", "A2-2023", "ESE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "150 arc"
A2 = setupaircraft("J2", "AF", "F-80C", "A2-2023", "E", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"
A2 = setupaircraft("K2", "AF", "F-80C", "A2-2023", "ENE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "60 arc"
A2 = setupaircraft("L2", "AF", "F-80C", "A2-2023", "NNE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2025", "NNE", 5, 4.0, "CL")

A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "N", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"
A2 = setupaircraft("B2", "AF", "F-80C", "A2-2023", "NNW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"
A2 = setupaircraft("C2", "AF", "F-80C", "A2-2023", "WNW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "60 arc"
A2 = setupaircraft("D2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"
A2 = setupaircraft("E2", "AF", "F-80C", "A2-2023", "WSW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "150 arc"
A2 = setupaircraft("F2", "AF", "F-80C", "A2-2023", "SSW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("G2", "AF", "F-80C", "A2-2023", "S", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("H2", "AF", "F-80C", "A2-2023", "SSE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("I2", "AF", "F-80C", "A2-2023", "ESE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "150 arc"
A2 = setupaircraft("J2", "AF", "F-80C", "A2-2023", "E", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"
A2 = setupaircraft("K2", "AF", "F-80C", "A2-2023", "ENE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "60 arc"
A2 = setupaircraft("L2", "AF", "F-80C", "A2-2023", "NNE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2025/2124", "NNW", 5, 4.0, "CL")

A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "N", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"
A2 = setupaircraft("B2", "AF", "F-80C", "A2-2023", "NNW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "30 arc"
A2 = setupaircraft("C2", "AF", "F-80C", "A2-2023", "WNW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "60 arc"
A2 = setupaircraft("D2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"
A2 = setupaircraft("E2", "AF", "F-80C", "A2-2023", "WSW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "120 arc"
A2 = setupaircraft("F2", "AF", "F-80C", "A2-2023", "SSW", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "150 arc"
A2 = setupaircraft("G2", "AF", "F-80C", "A2-2023", "S", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("H2", "AF", "F-80C", "A2-2023", "SSE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "180 arc"
A2 = setupaircraft("I2", "AF", "F-80C", "A2-2023", "ESE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "150 arc"
A2 = setupaircraft("J2", "AF", "F-80C", "A2-2023", "E", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "120 arc"
A2 = setupaircraft("K2", "AF", "F-80C", "A2-2023", "ENE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"
A2 = setupaircraft("L2", "AF", "F-80C", "A2-2023", "NNE", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "60 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024", "NNE", 5, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024", "NNE", 5, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024", "NNE", 5, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "W", 5, 5.0, "CL")
assert A1._angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024", "NNW", 5, 5.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "120 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024", "NNW", 5, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024", "NNE", 5, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023", "W", 5, 5.0, "CL")
assert A1._angleofftail(A2) == "90 arc"

endtestsetup()

endfile(__file__)
