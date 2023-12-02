from apxo.tests.infrastructure import *
startfile(__file__, "angle-off")

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2025", "N", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "2023", "N", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "0 line"
A2 = aircraft("B2", "AF", "F-80C"  , "2023", "NNW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"
A2 = aircraft("C2", "AF", "F-80C"  , "2023", "WNW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "60 arc"
A2 = aircraft("D2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"
A2 = aircraft("E2", "AF", "F-80C"  , "2023", "WSW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "150 arc"
A2 = aircraft("F2", "AF", "F-80C"  , "2023", "SSW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("G2", "AF", "F-80C"  , "2023", "S", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 line"
A2 = aircraft("H2", "AF", "F-80C"  , "2023", "SSE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("I2", "AF", "F-80C"  , "2023", "ESE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "150 arc"
A2 = aircraft("J2", "AF", "F-80C"  , "2023", "E", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"
A2 = aircraft("K2", "AF", "F-80C"  , "2023", "ENE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "60 arc"
A2 = aircraft("L2", "AF", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2025", "NNE", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "2023", "N", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"
A2 = aircraft("B2", "AF", "F-80C"  , "2023", "NNW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"
A2 = aircraft("C2", "AF", "F-80C"  , "2023", "WNW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "60 arc"
A2 = aircraft("D2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"
A2 = aircraft("E2", "AF", "F-80C"  , "2023", "WSW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "150 arc"
A2 = aircraft("F2", "AF", "F-80C"  , "2023", "SSW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("G2", "AF", "F-80C"  , "2023", "S", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("H2", "AF", "F-80C"  , "2023", "SSE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("I2", "AF", "F-80C"  , "2023", "ESE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "150 arc"
A2 = aircraft("J2", "AF", "F-80C"  , "2023", "E", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"
A2 = aircraft("K2", "AF", "F-80C"  , "2023", "ENE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "60 arc"
A2 = aircraft("L2", "AF", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2025/2124", "NNW", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "2023", "N", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"
A2 = aircraft("B2", "AF", "F-80C"  , "2023", "NNW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "30 arc"
A2 = aircraft("C2", "AF", "F-80C"  , "2023", "WNW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "60 arc"
A2 = aircraft("D2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"
A2 = aircraft("E2", "AF", "F-80C"  , "2023", "WSW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "120 arc"
A2 = aircraft("F2", "AF", "F-80C"  , "2023", "SSW", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "150 arc"
A2 = aircraft("G2", "AF", "F-80C"  , "2023", "S", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("H2", "AF", "F-80C"  , "2023", "SSE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "180 arc"
A2 = aircraft("I2", "AF", "F-80C"  , "2023", "ESE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "150 arc"
A2 = aircraft("J2", "AF", "F-80C"  , "2023", "E", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "120 arc"
A2 = aircraft("K2", "AF", "F-80C"  , "2023", "ENE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"
A2 = aircraft("L2", "AF", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "60 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2024", "NNE", 5, 5.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "2023", "W", 5, 5.0, "CL")
assert A1.angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2024", "NNW", 5, 5.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "120 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2024", "NNW", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleofftail(A2) == "90 arc"

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "2023", "W", 5, 5.0, "CL")
assert A1.angleofftail(A2) == "90 arc"

endtestsetup()

endfile(__file__)