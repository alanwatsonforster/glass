from apengine.tests.infrastructure import *
startfile(__file__, "angle-off")

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "2023", "N", 5, 4.0, "CL")
assert A1.angleoff(A2) == "0 line"
A2 = aircraft("A2", "F-80C"  , "2023", "NNW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "WNW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "60 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "WSW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "120 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "SSW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "S", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 line"
A2 = aircraft("A2", "F-80C"  , "2023", "SSE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "ESE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "120 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "E", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "ENE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "60 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"

A1 = aircraft("A1", "F-80C"  , "2025", "NNE", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "2023", "N", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "NNW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "WNW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "60 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "WSW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "120 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "SSW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "S", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "SSE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "ESE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "120 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "E", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "ENE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "60 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"

A1 = aircraft("A1", "F-80C"  , "2025/2124", "NNW", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "2023", "N", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "NNW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "WNW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "60 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "WSW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "120 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "SSW", 5, 4.0, "CL")
assert A1.angleoff(A2) == "150 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "S", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "SSE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "ESE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "150 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "E", 5, 4.0, "CL")
assert A1.angleoff(A2) == "120 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "ENE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"
A2 = aircraft("A2", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.angleoff(A2) == "60 arc"

A1 = aircraft("A1", "F-80C"  , "2024", "NNE", 5, 5.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "30 arc"

A1 = aircraft("A1", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"

A1 = aircraft("A1", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 5.0, "CL")
assert A1.angleoff(A2) == "60 arc"

A1 = aircraft("A1", "F-80C"  , "2024", "NNW", 5, 5.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "180 arc"

A1 = aircraft("A1", "F-80C"  , "2024", "NNW", 5, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.angleoff(A2) == "90 arc"

A1 = aircraft("A1", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 5.0, "CL")
assert A1.angleoff(A2) == "60 arc"


endfile(__file__)