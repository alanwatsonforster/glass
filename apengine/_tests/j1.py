from apengine._tests.infrastructure import *
startfile(__file__, "gun attack range")

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "1924/1925", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2025", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 0
A2 = aircraft("A2", "F-80C"  , "2124/2125", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1924/2025", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2124/2025", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1924", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024/2025", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2124", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1924/2024", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2124/2024", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1923/1924", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2123/2124", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1923/2024", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2123/2024", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1

A2 = aircraft("A2", "F-80C"  , "1923", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2023/2024", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2123", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1923/2023", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2123/2023", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2

A2 = aircraft("A2", "F-80C"  , "1922/1923", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2122/2123", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1922/2023", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2122/2023", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1922", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2022/2023", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2122", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1922/2022", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2122/2022", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A1 = aircraft("A1", "F-80C"  , "2025", "NNE", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "1924", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "1924/2025", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2025", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 0
A2 = aircraft("A2", "F-80C"  , "2025/2125", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2125", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1924/2024", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024/2025", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2025/2124", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2124/2125", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "1923/2024", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024/2124", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2124", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2124/2225", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2023/2024", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024/2123", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2123/2124", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2124/2224", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2023/2123", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2123", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2123/2224", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2224", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2023/2122", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2122/2123", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2123/2223", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2223/2223", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2022/2122", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2122", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2122/2223", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2223", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2223/2323", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A1 = aircraft("A1", "F-80C"  , "2024/2025", "E", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "2023/2024", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024/2025", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 0
A2 = aircraft("A2", "F-80C"  , "2025", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2025/2026", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2024/2123", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2024/2124", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2025/2124", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2025/2125", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2123", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2123/2124", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2124", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2124/2125", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2125", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2123/2224", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2124/2224", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2124/2225", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 1
A2 = aircraft("A2", "F-80C"  , "2125/2225", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2223/2224", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2224", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2224/2225", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2225", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2225/2226", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2224/2323", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2224/2324", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2225/2324", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is not False and A1.gunattackrange(A2) == 2
A2 = aircraft("A2", "F-80C"  , "2225/2325", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

A2 = aircraft("A2", "F-80C"  , "2323", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2323/2324", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2324", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2324/2325", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False
A2 = aircraft("A2", "F-80C"  , "2325", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2) is False

endtestsetup()

# Check altitude requirements and the vertical component of range.

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2025", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2025", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 0

A0 = aircraft("A0", "F-80C"  , "2025", "N",  4, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2025", "N",  5, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 2
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2025", "N",  6, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 2
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2025", "N",  7, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 1
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2025", "N",  8, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 1
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2025", "N",  9, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 0
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2025", "N", 10, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 0
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 0
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 0

A0 = aircraft("A0", "F-80C"  , "2025", "N", 11, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 0

A0 = aircraft("A0", "F-80C"  , "2025", "N", 12, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 1

A0 = aircraft("A0", "F-80C"  , "2025", "N", 13, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 1

A0 = aircraft("A0", "F-80C"  , "2025", "N", 14, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 2

A0 = aircraft("A0", "F-80C"  , "2025", "N", 15, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 2

A0 = aircraft("A0", "F-80C"  , "2025", "N", 16, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

# Horizontal range 1

A0 = aircraft("A0", "F-80C"  , "2024", "N",  4, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N",  5, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N",  6, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N",  7, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 2
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N",  8, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 2
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N",  9, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 1
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 1
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N", 10, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 1
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 1
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 1

A0 = aircraft("A0", "F-80C"  , "2024", "N", 11, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 1
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 1

A0 = aircraft("A0", "F-80C"  , "2024", "N", 12, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 2

A0 = aircraft("A0", "F-80C"  , "2024", "N", 13, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 2

A0 = aircraft("A0", "F-80C"  , "2024", "N", 14, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N", 15, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2024", "N", 16, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

# Horizontal range 2

A0 = aircraft("A0", "F-80C"  , "2023", "N",  4, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N",  5, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N",  6, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N",  7, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N",  8, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N",  9, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 2
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 2
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N", 10, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 2
assert A2.gunattackrange(A0) is not False and A2.gunattackrange(A0) == 2
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 2

A0 = aircraft("A0", "F-80C"  , "2023", "N", 11, 4.0, "CL")
assert A1.gunattackrange(A0) is not False and A1.gunattackrange(A0) == 2
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is not False and A3.gunattackrange(A0) == 2

A0 = aircraft("A0", "F-80C"  , "2023", "N", 12, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N", 13, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N", 14, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N", 15, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

A0 = aircraft("A0", "F-80C"  , "2023", "N", 16, 4.0, "CL")
assert A1.gunattackrange(A0) is False
assert A2.gunattackrange(A0) is False
assert A3.gunattackrange(A0) is False

endfile(__file__)