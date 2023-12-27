from apxo.tests.infrastructure import *
startfile(__file__, "articulated gun attack range")

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "W", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "A2-1924/1925", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("B2", "AF", "F-80C"  , "A2-2025", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 0
A2 = aircraft("C2", "AF", "F-80C"  , "A2-2124/2125", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("D2", "AF", "F-80C"  , "A2-1924/2025", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("E2", "AF", "F-80C"  , "A2-2124/2025", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("F2", "AF", "F-80C"  , "A2-1924", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("G2", "AF", "F-80C"  , "A2-2024/2025", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("H2", "AF", "F-80C"  , "A2-2124", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("I2", "AF", "F-80C"  , "A2-1924/2024", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("J2", "AF", "F-80C"  , "A2-2124/2024", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("K2", "AF", "F-80C"  , "A2-1923/1924", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("L2", "AF", "F-80C"  , "A2-2024", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("M2", "AF", "F-80C"  , "A2-2123/2124", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("N2", "AF", "F-80C"  , "A2-1923/2024", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("O2", "AF", "F-80C"  , "A2-2123/2024", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("P2", "AF", "F-80C"  , "A2-1923", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("Q2", "AF", "F-80C"  , "A2-2023/2024", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("R2", "AF", "F-80C"  , "A2-2123", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("S2", "AF", "F-80C"  , "A2-1923/2023", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("T2", "AF", "F-80C"  , "A2-2123/2023", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("U2", "AF", "F-80C"  , "A2-1922/1923", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("V2", "AF", "F-80C"  , "A2-2023", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("W2", "AF", "F-80C"  , "A2-2122/2123", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("X2", "AF", "F-80C"  , "A2-1922/2023", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("Y2", "AF", "F-80C"  , "A2-2122/2023", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

A2 = aircraft("Z2", "AF", "F-80C"  , "A2-1922", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AA2", "AF", "F-80C"  , "A2-2022/2023", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AB2", "AF", "F-80C"  , "A2-2122", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

A2 = aircraft("AC2", "AF", "F-80C"  , "A2-1922/2022", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AD2", "AF", "F-80C"  , "A2-2122/2022", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "WNW", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "A2-1924", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("B2", "AF", "F-80C"  , "A2-1924/2025", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("C2", "AF", "F-80C"  , "A2-2025", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 0
A2 = aircraft("D2", "AF", "F-80C"  , "A2-2025/2125", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("E2", "AF", "F-80C"  , "A2-2125", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("F2", "AF", "F-80C"  , "A2-1924/2024", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("G2", "AF", "F-80C"  , "A2-2024/2025", "E", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("H2", "AF", "F-80C"  , "A2-2025/2124", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("I2", "AF", "F-80C"  , "A2-2124/2125", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("J2", "AF", "F-80C"  , "A2-1923/2024", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("K2", "AF", "F-80C"  , "A2-2024", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("L2", "AF", "F-80C"  , "A2-2024/2124", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("M2", "AF", "F-80C"  , "A2-2124", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("N2", "AF", "F-80C"  , "A2-2124/2225", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("O2", "AF", "F-80C"  , "A2-2023/2024", "E", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("P2", "AF", "F-80C"  , "A2-2024/2123", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("Q2", "AF", "F-80C"  , "A2-2123/2124", "E", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("R2", "AF", "F-80C"  , "A2-2124/2224", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("S2", "AF", "F-80C"  , "A2-2023", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("T2", "AF", "F-80C"  , "A2-2023/2123", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("U2", "AF", "F-80C"  , "A2-2123", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("V2", "AF", "F-80C"  , "A2-2123/2224", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("W2", "AF", "F-80C"  , "A2-2224", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("X2", "AF", "F-80C"  , "A2-2023/2122", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("Y2", "AF", "F-80C"  , "A2-2122/2123", "E", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") ==  "the target is not in the weapon range or arc."
A2 = aircraft("Z2", "AF", "F-80C"  , "A2-2123/2223", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("AA2", "AF", "F-80C" , "A2-2223/2224", "E", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

A2 = aircraft("AB2", "AF", "F-80C"  , "A2-2022/2122", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AC2", "AF", "F-80C"  , "A2-2122", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AD2", "AF", "F-80C"  , "A2-2122/2223", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AE2", "AF", "F-80C"  , "A2-2223", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AF2", "AF", "F-80C"  , "A2-2223/2323", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2024/2025", "W", 5, 4.0, "CL")

A2 = aircraft("F2", "AF", "F-80C"  , "A2-1924", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("G2", "AF", "F-80C"  , "A2-2024/2025", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 0
A2 = aircraft("H2", "AF", "F-80C"  , "A2-2124", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("I2", "AF", "F-80C"  , "A2-1924/2024", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("J2", "AF", "F-80C"  , "A2-2124/2024", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("K2", "AF", "F-80C"  , "A2-1923/1924", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("L2", "AF", "F-80C"  , "A2-2024", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("M2", "AF", "F-80C"  , "A2-2123/2124", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("N2", "AF", "F-80C"  , "A2-1923/2024", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("O2", "AF", "F-80C"  , "A2-2123/2024", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("P2", "AF", "F-80C"  , "A2-1923", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("Q2", "AF", "F-80C"  , "A2-2023/2024", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1
A2 = aircraft("R2", "AF", "F-80C"  , "A2-2123", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("S2", "AF", "F-80C"  , "A2-1923/2023", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("T2", "AF", "F-80C"  , "A2-2123/2023", "NNE", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 1

A2 = aircraft("U2", "AF", "F-80C"  , "A2-1922/1923", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("V2", "AF", "F-80C"  , "A2-2023", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("W2", "AF", "F-80C"  , "A2-2122/2123", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("X2", "AF", "F-80C"  , "A2-1922/2023", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("Y2", "AF", "F-80C"  , "A2-2122/2023", "NNW", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("Z2", "AF", "F-80C"  , "A2-1922", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AA2", "AF", "F-80C"  , "A2-2022/2023", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2
A2 = aircraft("AB2", "AF", "F-80C"  , "A2-2122", "W", 5, 4.0, "CL")
assert A1.gunattackrange(A2, arc="90-") == 2

A2 = aircraft("AC2", "AF", "F-80C"  , "A2-1922/2022", "NNW", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AD2", "AF", "F-80C"  , "A2-2122/2022", "NNE", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

A2 = aircraft("AE2", "AF", "F-80C"  , "A2-1921/1921", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AF2", "AF", "F-80C"  , "A2-2022", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."
A2 = aircraft("AG2", "AF", "F-80C"  , "A2-2121/2122", "W", 5, 4.0, "CL", color="red")
assert A1.gunattackrange(A2, arc="90-") == "the target is not in the weapon range or arc."

endtestsetup()

# Check altitude requirements and the vertical component of range.

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 0

A0 = aircraft("A0", "AF", "F-80C"  , "A2-2025", "N",  4, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("B0", "AF", "F-80C"  , "A2-2025", "N",  5, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("C0", "AF", "F-80C"  , "A2-2025", "N",  6, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("D0", "AF", "F-80C"  , "A2-2025", "N",  7, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("E0", "AF", "F-80C"  , "A2-2025", "N",  8, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("F0", "AF", "F-80C"  , "A2-2025", "N",  9, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 0
assert A2.gunattackrange(A0, arc="90-") == 0
assert A3.gunattackrange(A0, arc="90-") == 0

A0 = aircraft("G0", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 0
assert A2.gunattackrange(A0, arc="90-") == 0
assert A3.gunattackrange(A0, arc="90-") == 0

A0 = aircraft("H0", "AF", "F-80C"  , "A2-2025", "N", 11, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 0
assert A2.gunattackrange(A0, arc="90-") == 0
assert A3.gunattackrange(A0, arc="90-") == 0

A0 = aircraft("I0", "AF", "F-80C"  , "A2-2025", "N", 12, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("J0", "AF", "F-80C"  , "A2-2025", "N", 13, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("K0", "AF", "F-80C"  , "A2-2025", "N", 14, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("L0", "AF", "F-80C"  , "A2-2025", "N", 15, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("M0", "AF", "F-80C"  , "A2-2025", "N", 16, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

# Horizontal range 1

A0 = aircraft("N0", "AF", "F-80C"  , "A2-2026", "N",  4, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("O0", "AF", "F-80C"  , "A2-2026", "N",  5, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("P0", "AF", "F-80C"  , "A2-2026", "N",  6, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("Q0", "AF", "F-80C"  , "A2-2026", "N",  7, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("R0", "AF", "F-80C"  , "A2-2026", "N",  8, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("S0", "AF", "F-80C"  , "A2-2026", "N",  9, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("T0", "AF", "F-80C"  , "A2-2026", "N", 10, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("U0", "AF", "F-80C"  , "A2-2026", "N", 11, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 1
assert A2.gunattackrange(A0, arc="90-") == 1
assert A3.gunattackrange(A0, arc="90-") == 1

A0 = aircraft("V0", "AF", "F-80C"  , "A2-2026", "N", 12, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("W0", "AF", "F-80C"  , "A2-2026", "N", 13, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("X0", "AF", "F-80C"  , "A2-2026", "N", 14, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("Y0", "AF", "F-80C"  , "A2-2026", "N", 15, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("Z0", "AF", "F-80C"  , "A2-2026", "N", 16, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

# Horizontal range 2

A0 = aircraft("AA0", "AF", "F-80C"  , "A2-2027", "N",  4, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AB0", "AF", "F-80C"  , "A2-2027", "N",  5, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AC0", "AF", "F-80C"  , "A2-2027", "N",  6, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AD0", "AF", "F-80C"  , "A2-2027", "N",  7, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AE0", "AF", "F-80C"  , "A2-2027", "N",  8, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AF0", "AF", "F-80C"  , "A2-2027", "N",  9, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("AG0", "AF", "F-80C"  , "A2-2027", "N", 10, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("AH0", "AF", "F-80C"  , "A2-2027", "N", 11, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == 2
assert A2.gunattackrange(A0, arc="90-") == 2
assert A3.gunattackrange(A0, arc="90-") == 2

A0 = aircraft("AI0", "AF", "F-80C"  , "A2-2027", "N", 12, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AJ0", "AF", "F-80C"  , "A2-2027", "N", 13, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AK0", "AF", "F-80C"  , "A2-2027", "N", 14, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AL0", "AF", "F-80C"  , "A2-2027", "N", 15, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

A0 = aircraft("AM0", "AF", "F-80C"  , "A2-2027", "N", 16, 4.0, "CL")
assert A1.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A2.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."
assert A3.gunattackrange(A0, arc="90-") == "the target is not in the weapon range or arc."

endfile(__file__)