from apxo.tests.infrastructure import *

startfile(__file__, "gun attack range")

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2025", "N", 5, 4.0, "CL")

A2 = setupaircraft("A2", "AF", "F-80C", "A2-1924/1925", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("B2", "AF", "F-80C", "A2-2025", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 0
A2 = setupaircraft("C2", "AF", "F-80C", "A2-2124/2125", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("D2", "AF", "F-80C", "A2-1924/2025", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("E2", "AF", "F-80C", "A2-2124/2025", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("F2", "AF", "F-80C", "A2-1924", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("G2", "AF", "F-80C", "A2-2024/2025", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("H2", "AF", "F-80C", "A2-2124", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("I2", "AF", "F-80C", "A2-1924/2024", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("J2", "AF", "F-80C", "A2-2124/2024", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("K2", "AF", "F-80C", "A2-1923/1924", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("L2", "AF", "F-80C", "A2-2024", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("M2", "AF", "F-80C", "A2-2123/2124", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("N2", "AF", "F-80C", "A2-1923/2024", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("O2", "AF", "F-80C", "A2-2123/2024", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1

A2 = setupaircraft("P2", "AF", "F-80C", "A2-1923", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("Q2", "AF", "F-80C", "A2-2023/2024", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("R2", "AF", "F-80C", "A2-2123", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("S2", "AF", "F-80C", "A2-1923/2023", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("T2", "AF", "F-80C", "A2-2123/2023", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2

A2 = setupaircraft("U2", "AF", "F-80C", "A2-1922/1923", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("V2", "AF", "F-80C", "A2-2023", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("W2", "AF", "F-80C", "A2-2122/2123", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("X2", "AF", "F-80C", "A2-1922/2023", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("Y2", "AF", "F-80C", "A2-2122/2023", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("Z2", "AF", "F-80C", "A2-1922", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AA2", "AF", "F-80C", "A2-2022/2023", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AB2", "AF", "F-80C", "A2-2122", "W", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("AC2", "AF", "F-80C", "A2-1922/2022", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AD2", "AF", "F-80C", "A2-2122/2022", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2025", "NNE", 5, 4.0, "CL")

A2 = setupaircraft("A2", "AF", "F-80C", "A2-1924", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("B2", "AF", "F-80C", "A2-1924/2025", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("C2", "AF", "F-80C", "A2-2025", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 0
A2 = setupaircraft("D2", "AF", "F-80C", "A2-2025/2125", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("E2", "AF", "F-80C", "A2-2125", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("F2", "AF", "F-80C", "A2-1924/2024", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("G2", "AF", "F-80C", "A2-2024/2025", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("H2", "AF", "F-80C", "A2-2025/2124", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("I2", "AF", "F-80C", "A2-2124/2125", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("J2", "AF", "F-80C", "A2-1923/2024", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("K2", "AF", "F-80C", "A2-2024", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("L2", "AF", "F-80C", "A2-2024/2124", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("M2", "AF", "F-80C", "A2-2124", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("N2", "AF", "F-80C", "A2-2124/2225", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("O2", "AF", "F-80C", "A2-2023/2024", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("P2", "AF", "F-80C", "A2-2024/2123", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("Q2", "AF", "F-80C", "A2-2123/2124", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("R2", "AF", "F-80C", "A2-2124/2224", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("S2", "AF", "F-80C", "A2-2023", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("T2", "AF", "F-80C", "A2-2023/2123", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("U2", "AF", "F-80C", "A2-2123", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("V2", "AF", "F-80C", "A2-2123/2224", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("W2", "AF", "F-80C", "A2-2224", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("X2", "AF", "F-80C", "A2-2023/2122", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("Y2", "AF", "F-80C", "A2-2122/2123", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("Z2", "AF", "F-80C", "A2-2123/2223", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("AA2", "AF", "F-80C", "A2-2223/2224", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("AB2", "AF", "F-80C", "A2-2022/2122", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AC2", "AF", "F-80C", "A2-2122", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AD2", "AF", "F-80C", "A2-2122/2223", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AE2", "AF", "F-80C", "A2-2223", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AF2", "AF", "F-80C", "A2-2223/2323", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

endtestsetup()

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2024/2025", "E", 5, 4.0, "CL")

A2 = setupaircraft("A2", "AF", "F-80C", "A2-2023/2024", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("B2", "AF", "F-80C", "A2-2024", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("C2", "AF", "F-80C", "A2-2024/2025", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 0
A2 = setupaircraft("D2", "AF", "F-80C", "A2-2025", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("E2", "AF", "F-80C", "A2-2025/2026", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("F2", "AF", "F-80C", "A2-2024/2123", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("G2", "AF", "F-80C", "A2-2024/2124", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("H2", "AF", "F-80C", "A2-2025/2124", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("I2", "AF", "F-80C", "A2-2025/2125", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("J2", "AF", "F-80C", "A2-2123", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("K2", "AF", "F-80C", "A2-2123/2124", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("L2", "AF", "F-80C", "A2-2124", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("M2", "AF", "F-80C", "A2-2124/2125", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("N2", "AF", "F-80C", "A2-2125", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("O2", "AF", "F-80C", "A2-2123/2224", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("P2", "AF", "F-80C", "A2-2124/2224", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("Q2", "AF", "F-80C", "A2-2124/2225", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 1
A2 = setupaircraft("R2", "AF", "F-80C", "A2-2125/2225", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("S2", "AF", "F-80C", "A2-2223/2224", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("T2", "AF", "F-80C", "A2-2224", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("U2", "AF", "F-80C", "A2-2224/2225", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("V2", "AF", "F-80C", "A2-2225", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("W2", "AF", "F-80C", "A2-2225/2226", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("X2", "AF", "F-80C", "A2-2224/2323", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("Y2", "AF", "F-80C", "A2-2224/2324", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("Z2", "AF", "F-80C", "A2-2225/2324", "NNW", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == 2
A2 = setupaircraft("AA2", "AF", "F-80C", "A2-2225/2325", "NNE", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = setupaircraft("AB2", "AF", "F-80C", "A2-2323", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AC2", "AF", "F-80C", "A2-2323/2324", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AD2", "AF", "F-80C", "A2-2324", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AE2", "AF", "F-80C", "A2-2324/2325", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = setupaircraft("AF2", "AF", "F-80C", "A2-2325", "E", 5, 4.0, "CL")
assert A1._gunattackrange(A2) == "the target is not in the arc or range of the weapon."

endtestsetup()

# Check altitude requirements and the vertical component of range.

starttestsetup()

A1 = setupaircraft("A1", "AF", "F-80C", "A2-2025", "N", 10, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2025", "N", 10, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A2-2025", "N", 10, 4.0, "CL")

endtestsetup()

startgameturn()

A1.move("LVL", "M", "")
A2.move("SD", "M", "")
A3.move("SC", "M", "")

# Horizontal range 0

A0 = setupaircraft("A0", "AF", "F-80C", "A2-2025", "N", 4, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("B0", "AF", "F-80C", "A2-2025", "N", 5, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert A2._gunattackrange(A0) == 2
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("C0", "AF", "F-80C", "A2-2025", "N", 6, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert A2._gunattackrange(A0) == 2
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("D0", "AF", "F-80C", "A2-2025", "N", 7, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert A2._gunattackrange(A0) == 1
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("E0", "AF", "F-80C", "A2-2025", "N", 8, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert A2._gunattackrange(A0) == 1
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("F0", "AF", "F-80C", "A2-2025", "N", 9, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert A2._gunattackrange(A0) == 0
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("G0", "AF", "F-80C", "A2-2025", "N", 10, 4.0, "CL")
assert A1._gunattackrange(A0) == 0
assert A2._gunattackrange(A0) == 0
assert A3._gunattackrange(A0) == 0

A0 = setupaircraft("H0", "AF", "F-80C", "A2-2025", "N", 11, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 0

A0 = setupaircraft("I0", "AF", "F-80C", "A2-2025", "N", 12, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 1

A0 = setupaircraft("J0", "AF", "F-80C", "A2-2025", "N", 13, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 1

A0 = setupaircraft("K0", "AF", "F-80C", "A2-2025", "N", 14, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 2

A0 = setupaircraft("L0", "AF", "F-80C", "A2-2025", "N", 15, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 2

A0 = setupaircraft("M0", "AF", "F-80C", "A2-2025", "N", 16, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

# Horizontal range 1

A0 = setupaircraft("N0", "AF", "F-80C", "A2-2024", "N", 4, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("O0", "AF", "F-80C", "A2-2024", "N", 5, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("P0", "AF", "F-80C", "A2-2024", "N", 6, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("Q0", "AF", "F-80C", "A2-2024", "N", 7, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == 2
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("R0", "AF", "F-80C", "A2-2024", "N", 8, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == 2
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("S0", "AF", "F-80C", "A2-2024", "N", 9, 4.0, "CL")
assert A1._gunattackrange(A0) == 1
assert A2._gunattackrange(A0) == 1
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("T0", "AF", "F-80C", "A2-2024", "N", 10, 4.0, "CL")
assert A1._gunattackrange(A0) == 1
assert A2._gunattackrange(A0) == 1
assert A3._gunattackrange(A0) == 1

A0 = setupaircraft("U0", "AF", "F-80C", "A2-2024", "N", 11, 4.0, "CL")
assert A1._gunattackrange(A0) == 1
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 1

A0 = setupaircraft("V0", "AF", "F-80C", "A2-2024", "N", 12, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 2

A0 = setupaircraft("W0", "AF", "F-80C", "A2-2024", "N", 13, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 2

A0 = setupaircraft("X0", "AF", "F-80C", "A2-2024", "N", 14, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = setupaircraft("Y0", "AF", "F-80C", "A2-2024", "N", 15, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = setupaircraft("Z0", "AF", "F-80C", "A2-2024", "N", 16, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

# Horizontal range 2

A0 = setupaircraft("AA0", "AF", "F-80C", "A2-2023", "N", 4, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("AB0", "AF", "F-80C", "A2-2023", "N", 5, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("AC0", "AF", "F-80C", "A2-2023", "N", 6, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("AD0", "AF", "F-80C", "A2-2023", "N", 7, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("AE0", "AF", "F-80C", "A2-2023", "N", 8, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert A2._gunattackrange(A0) == "the target is not in the arc or range of the weapon."
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("AF0", "AF", "F-80C", "A2-2023", "N", 9, 4.0, "CL")
assert A1._gunattackrange(A0) == 2
assert A2._gunattackrange(A0) == 2
assert (
    A3._gunattackrange(A0)
    == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
)

A0 = setupaircraft("AG0", "AF", "F-80C", "A2-2023", "N", 10, 4.0, "CL")
assert A1._gunattackrange(A0) == 2
assert A2._gunattackrange(A0) == 2
assert A3._gunattackrange(A0) == 2

A0 = setupaircraft("AH0", "AF", "F-80C", "A2-2023", "N", 11, 4.0, "CL")
assert A1._gunattackrange(A0) == 2
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == 2

A0 = setupaircraft("AI0", "AF", "F-80C", "A2-2023", "N", 12, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = setupaircraft("AJ0", "AF", "F-80C", "A2-2023", "N", 13, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = setupaircraft("AK0", "AF", "F-80C", "A2-2023", "N", 14, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = setupaircraft("AL0", "AF", "F-80C", "A2-2023", "N", 15, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = setupaircraft("AM0", "AF", "F-80C", "A2-2023", "N", 16, 4.0, "CL")
assert (
    A1._gunattackrange(A0)
    == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
)
assert (
    A2._gunattackrange(A0)
    == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
)
assert A3._gunattackrange(A0) == "the target is not in the arc or range of the weapon."

endfile(__file__)
