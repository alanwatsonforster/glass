from apxo.tests.infrastructure import *
startfile(__file__, "rocket attack range")

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "N", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "A2-1924/1925", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("B2", "AF", "F-80C"  , "A2-2025", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("C2", "AF", "F-80C"  , "A2-2124/2125", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("D2", "AF", "F-80C"  , "A2-1924/2025", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("E2", "AF", "F-80C"  , "A2-2124/2025", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("F2", "AF", "F-80C"  , "A2-1924", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("G2", "AF", "F-80C"  , "A2-2024/2025", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("H2", "AF", "F-80C"  , "A2-2124", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("I2", "AF", "F-80C"  , "A2-1924/2024", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("J2", "AF", "F-80C"  , "A2-2124/2024", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("K2", "AF", "F-80C"  , "A2-1923/1924", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("L2", "AF", "F-80C"  , "A2-2024", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("M2", "AF", "F-80C"  , "A2-2123/2124", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("N2", "AF", "F-80C"  , "A2-1923/2024", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("O2", "AF", "F-80C"  , "A2-2123/2024", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1

A2 = aircraft("P2", "AF", "F-80C"  , "A2-1923", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("Q2", "AF", "F-80C"  , "A2-2023/2024", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("R2", "AF", "F-80C"  , "A2-2123", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("S2", "AF", "F-80C"  , "A2-1923/2023", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("T2", "AF", "F-80C"  , "A2-2123/2023", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1

A2 = aircraft("U2", "AF", "F-80C"  , "A2-1922/1923", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("V2", "AF", "F-80C"  , "A2-2023", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("W2", "AF", "F-80C"  , "A2-2122/2123", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("X2", "AF", "F-80C"  , "A2-1922/2023", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("Y2", "AF", "F-80C"  , "A2-2122/2023", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2

A2 = aircraft("Z2", "AF", "F-80C"  , "A2-1922", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AA2", "AF", "F-80C"  , "A2-2022/2023", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("AB2", "AF", "F-80C"  , "A2-2122", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AC2", "AF", "F-80C"  , "A2-1922/2022", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("AD2", "AF", "F-80C"  , "A2-2122/2022", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2

A2 = aircraft("AE2", "AF", "F-80C"  , "A2-1921/1922", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AF2", "AF", "F-80C"  , "A2-2022", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AG2", "AF", "F-80C"  , "A2-2121/2122", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AH2", "AF", "F-80C"  , "A2-1921/2022", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AI2", "AF", "F-80C"  , "A2-2121/2022", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3

A2 = aircraft("AJ2", "AF", "F-80C"  , "A2-1921", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AK2", "AF", "F-80C"  , "A2-2021/2022", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AL2", "AF", "F-80C"  , "A2-2121", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AM2", "AF", "F-80C"  , "A2-1921/2021", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AN2", "AF", "F-80C"  , "A2-2121/2021", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3

A2 = aircraft("AO2", "AF", "F-80C"  , "A2-1920/1921", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AP2", "AF", "F-80C"  , "A2-2021", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AQ2", "AF", "F-80C"  , "A2-2120/2121", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AR2", "AF", "F-80C"  , "A2-1920/2021", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AS2", "AF", "F-80C"  , "A2-2120/2021", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4

A2 = aircraft("AT2", "AF", "F-80C"  , "A2-1920", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AU2", "AF", "F-80C"  , "A2-2020/2021", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AV2", "AF", "F-80C"  , "A2-2120", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AW2", "AF", "F-80C"  , "A2-1920/2020", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AX2", "AF", "F-80C"  , "A2-2120/2020", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4

A2 = aircraft("AY2", "AF", "F-80C"  , "A2-1919/1920", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AZ2", "AF", "F-80C"  , "A2-2020", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("BA2", "AF", "F-80C"  , "A2-2119/2120", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("BB2", "AF", "F-80C"  , "A2-1919/2020", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("BC2", "AF", "F-80C"  , "A2-2119/2020", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("BD2", "AF", "F-80C"  , "A2-1919", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("BE2", "AF", "F-80C"  , "A2-2019/2020", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("BF2", "AF", "F-80C"  , "A2-2119", "W", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "NNE", 5, 4.0, "CL")

A2 = aircraft("A2", "AF", "F-80C"  , "A2-1924", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("B2", "AF", "F-80C"  , "A2-1924/2025", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("C2", "AF", "F-80C"  , "A2-2025", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("D2", "AF", "F-80C"  , "A2-2025/2125", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("E2", "AF", "F-80C"  , "A2-2125", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("F2", "AF", "F-80C"  , "A2-1924/2024", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("G2", "AF", "F-80C"  , "A2-2024/2025", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("H2", "AF", "F-80C"  , "A2-2025/2124", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("I2", "AF", "F-80C"  , "A2-2124/2125", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("J2", "AF", "F-80C"  , "A2-1923/2024", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("K2", "AF", "F-80C"  , "A2-2024", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("L2", "AF", "F-80C"  , "A2-2024/2124", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("M2", "AF", "F-80C"  , "A2-2124", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("N2", "AF", "F-80C"  , "A2-2124/2225", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("O2", "AF", "F-80C"  , "A2-2023/2024", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("P2", "AF", "F-80C"  , "A2-2024/2123", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("Q2", "AF", "F-80C"  , "A2-2123/2124", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("R2", "AF", "F-80C"  , "A2-2124/2224", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("S2", "AF", "F-80C"  , "A2-2023", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("T2", "AF", "F-80C"  , "A2-2023/2123", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("U2", "AF", "F-80C"  , "A2-2123", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("V2", "AF", "F-80C"  , "A2-2123/2224", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("W2", "AF", "F-80C"  , "A2-2224", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("X2", "AF", "F-80C"  , "A2-2023/2122", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("Y2", "AF", "F-80C"  , "A2-2122/2123", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("Z2", "AF", "F-80C"  , "A2-2123/2223", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("AA2", "AF", "F-80C" , "A2-2223/2224", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AB2", "AF", "F-80C"  , "A2-2022/2122", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AC2", "AF", "F-80C"  , "A2-2122", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AD2", "AF", "F-80C"  , "A2-2122/2223", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("AE2", "AF", "F-80C"  , "A2-2223", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AF2", "AF", "F-80C"  , "A2-2223/2323", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AG2", "AF", "F-80C"  , "A2-2121/2122", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AH2", "AF", "F-80C"  , "A2-2222/2122", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AI2", "AF", "F-80C"  , "A2-2222/2223", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AJ2", "AF", "F-80C"  , "A2-2223/2322", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AK2", "AF", "F-80C"  , "A2-2121", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AL2", "AF", "F-80C"  , "A2-2121/2222", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AM2", "AF", "F-80C"  , "A2-2222", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AN2", "AF", "F-80C"  , "A2-2222/2322", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AO2", "AF", "F-80C"  , "A2-2322", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AP2", "AF", "F-80C" , "A2-2121/2221", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AQ", "AF", "F-80C"  , "A2-2222/2221", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AR", "AF", "F-80C"  , "A2-2222/2321", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AS2", "AF", "F-80C" , "A2-2322/2321", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
  
A2 = aircraft("AT2", "AF", "F-80C"  , "A2-2120/2221", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AU2", "AF", "F-80C"  , "A2-2221", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AV2", "AF", "F-80C"  , "A2-2221/2321", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AW2", "AF", "F-80C"  , "A2-2321", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AX2", "AF", "F-80C"  , "A2-2321/2422", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2024/2025", "E", 5, 4.0, "CL")
    
A2 = aircraft("A2", "AF", "F-80C"  , "A2-2023/2024", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("B2", "AF", "F-80C"  , "A2-2024", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("C2", "AF", "F-80C"  , "A2-2024/2025", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("D2", "AF", "F-80C"  , "A2-2025", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("E2", "AF", "F-80C"  , "A2-2025/2026", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("F2", "AF", "F-80C"  , "A2-2024/2123", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("G2", "AF", "F-80C"  , "A2-2024/2124", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("H2", "AF", "F-80C"  , "A2-2025/2124", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("I2", "AF", "F-80C"  , "A2-2025/2125", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("J2", "AF", "F-80C"  , "A2-2123", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("K2", "AF", "F-80C"  , "A2-2123/2124", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("L2", "AF", "F-80C"  , "A2-2124", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("M2", "AF", "F-80C"  , "A2-2124/2125", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("N2", "AF", "F-80C"  , "A2-2125", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("O2", "AF", "F-80C"  , "A2-2123/2224", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("P2", "AF", "F-80C"  , "A2-2124/2224", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("Q2", "AF", "F-80C"  , "A2-2124/2225", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 1
A2 = aircraft("R2", "AF", "F-80C"  , "A2-2125/2225", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("S2", "AF", "F-80C"  , "A2-2223/2224", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("T2", "AF", "F-80C"  , "A2-2224", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("U2", "AF", "F-80C"  , "A2-2224/2225", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("V2", "AF", "F-80C"  , "A2-2225", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("W2", "AF", "F-80C"  , "A2-2225/2226", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("X2", "AF", "F-80C"  , "A2-2224/2323", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("Y2", "AF", "F-80C"  , "A2-2224/2324", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("Z2", "AF", "F-80C"  , "A2-2225/2324", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 2
A2 = aircraft("AA2", "AF", "F-80C"  , "A2-2225/2325", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AB2", "AF", "F-80C"  , "A2-2323", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AC2", "AF", "F-80C"  , "A2-2323/2324", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AD2", "AF", "F-80C"  , "A2-2324", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AE2", "AF", "F-80C"  , "A2-2324/2325", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AF2", "AF", "F-80C"  , "A2-2325", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AG2", "AF", "F-80C"  , "A2-2323/2424", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AH2", "AF", "F-80C"  , "A2-2324/2424", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AI2", "AF", "F-80C"  , "A2-2324/2425", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 3
A2 = aircraft("AJ2", "AF", "F-80C"  , "A2-2325/2425", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AK2", "AF", "F-80C"  , "A2-2423/2424", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AL2", "AF", "F-80C"  , "A2-2424", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AM2", "AF", "F-80C"  , "A2-2424/2425", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AN2", "AF", "F-80C"  , "A2-2425", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AO2", "AF", "F-80C"  , "A2-2425/2426", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AP2", "AF", "F-80C"  , "A2-2424/2523", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AQ2", "AF", "F-80C"  , "A2-2424/2524", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AR2", "AF", "F-80C"  , "A2-2425/2524", "NNW", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == 4
A2 = aircraft("AS2", "AF", "F-80C"  , "A2-2425/2525", "NNE", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

A2 = aircraft("AT2", "AF", "F-80C"  , "A2-2523", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AU2", "AF", "F-80C"  , "A2-2523/2524", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AV2", "AF", "F-80C"  , "A2-2524", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AW2", "AF", "F-80C"  , "A2-2524/2525", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."
A2 = aircraft("AX2", "AF", "F-80C"  , "A2-2525", "E", 5, 4.0, "CL")
assert A1._rocketattackrange(A2) == "the target is not in the arc or range of the weapon."

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

A0 = aircraft("A0", "AF", "F-80C"  , "A2-2025", "N",  0, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "AF", "F-80C"  , "A2-2025", "N",  1, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "AF", "F-80C"  , "A2-2025", "N",  2, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "AF", "F-80C"  , "A2-2025", "N",  3, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "AF", "F-80C"  , "A2-2025", "N",  4, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "AF", "F-80C"  , "A2-2025", "N",  5, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "AF", "F-80C"  , "A2-2025", "N",  6, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("H0", "AF", "F-80C"  , "A2-2025", "N",  7, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("I0", "AF", "F-80C"  , "A2-2025", "N",  8, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("J0", "AF", "F-80C"  , "A2-2025", "N",  9, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("K0", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
assert A1._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("L0", "AF", "F-80C"  , "A2-2025", "N", 11, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("M0", "AF", "F-80C"  , "A2-2025", "N", 12, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("N0", "AF", "F-80C"  , "A2-2025", "N", 13, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("O0", "AF", "F-80C"  , "A2-2025", "N", 14, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("P0", "AF", "F-80C"  , "A2-2025", "N", 15, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("Q0", "AF", "F-80C"  , "A2-2025", "N", 16, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("R0", "AF", "F-80C"  , "A2-2025", "N", 17, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("S0", "AF", "F-80C"  , "A2-2025", "N", 18, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("T0", "AF", "F-80C"  , "A2-2025", "N", 19, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("U0", "AF", "F-80C"  , "A2-2025", "N", 20, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

endturn()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 1

A0 = aircraft("A0", "AF", "F-80C"  , "A2-2024", "N",  0, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "AF", "F-80C"  , "A2-2024", "N",  1, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "AF", "F-80C"  , "A2-2024", "N",  2, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "AF", "F-80C"  , "A2-2024", "N",  3, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "AF", "F-80C"  , "A2-2024", "N",  4, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "AF", "F-80C"  , "A2-2024", "N",  5, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "AF", "F-80C"  , "A2-2024", "N",  6, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("H0", "AF", "F-80C"  , "A2-2024", "N",  7, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 2
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("I0", "AF", "F-80C"  , "A2-2024", "N",  8, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 2
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("J0", "AF", "F-80C"  , "A2-2024", "N",  9, 4.0, "CL")
assert A1._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A2._rocketattackrange(A0) == 1
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("K0", "AF", "F-80C"  , "A2-2024", "N", 10, 4.0, "CL")
assert A1._rocketattackrange(A0) == 1
assert A2._rocketattackrange(A0) == 1
assert A3._rocketattackrange(A0) == 1

A0 = aircraft("L0", "AF", "F-80C"  , "A2-2024", "N", 11, 4.0, "CL")
assert A1._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 1

A0 = aircraft("M0", "AF", "F-80C"  , "A2-2024", "N", 12, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 2

A0 = aircraft("N0", "AF", "F-80C"  , "A2-2024", "N", 13, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("O0", "AF", "F-80C"  , "A2-2024", "N", 14, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("P0", "AF", "F-80C"  , "A2-2024", "N", 15, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("Q0", "AF", "F-80C"  , "A2-2024", "N", 16, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("R0", "AF", "F-80C"  , "A2-2024", "N", 17, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("S0", "AF", "F-80C"  , "A2-2024", "N", 18, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("T0", "AF", "F-80C"  , "A2-2024", "N", 19, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("U0", "AF", "F-80C"  , "A2-2024", "N", 20, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

endturn()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C"  , "A2-2025", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 2

A0 = aircraft("A0", "AF", "F-80C"  , "A2-2023", "N",  4, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "AF", "F-80C"  , "A2-2023", "N",  5, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 4
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "AF", "F-80C"  , "A2-2023", "N",  6, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 4
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "AF", "F-80C"  , "A2-2023", "N",  7, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 3
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "AF", "F-80C"  , "A2-2023", "N",  8, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 3
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "AF", "F-80C"  , "A2-2023", "N",  9, 4.0, "CL")
assert A1._rocketattackrange(A0) == 2
assert A2._rocketattackrange(A0) == 2
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "AF", "F-80C"  , "A2-2023", "N", 10, 4.0, "CL")
assert A1._rocketattackrange(A0) == 2
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == 2

A0 = aircraft("H0", "AF", "F-80C"  , "A2-2023", "N", 11, 4.0, "CL")
assert A1._rocketattackrange(A0) == 2
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 2

A0 = aircraft("I0", "AF", "F-80C"  , "A2-2023", "N", 12, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 3

A0 = aircraft("J0", "AF", "F-80C"  , "A2-2023", "N", 13, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 3

A0 = aircraft("K0", "AF", "F-80C"  , "A2-2023", "N", 14, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 4

A0 = aircraft("L0", "AF", "F-80C"  , "A2-2023", "N", 15, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("M0", "AF", "F-80C"  , "A2-2023", "N", 16, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

endturn()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2026", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "A2-2026", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C"  , "A2-2026", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 3

A0 = aircraft("A0", "AF", "F-80C"  , "A2-2023", "N",  4, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "AF", "F-80C"  , "A2-2023", "N",  5, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "AF", "F-80C"  , "A2-2023", "N",  6, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "AF", "F-80C"  , "A2-2023", "N",  7, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 4
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "AF", "F-80C"  , "A2-2023", "N",  8, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == 4
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "AF", "F-80C"  , "A2-2023", "N",  9, 4.0, "CL")
assert A1._rocketattackrange(A0) == 3
assert A2._rocketattackrange(A0) == 3
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "AF", "F-80C"  , "A2-2023", "N", 10, 4.0, "CL")
assert A1._rocketattackrange(A0) == 3
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == 3

A0 = aircraft("H0", "AF", "F-80C"  , "A2-2023", "N", 11, 4.0, "CL")
assert A1._rocketattackrange(A0) == 3
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 3

A0 = aircraft("I0", "AF", "F-80C"  , "A2-2023", "N", 12, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 4

A0 = aircraft("J0", "AF", "F-80C"  , "A2-2023", "N", 13, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 4

A0 = aircraft("K0", "AF", "F-80C"  , "A2-2023", "N", 14, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("L0", "AF", "F-80C"  , "A2-2023", "N", 15, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("M0", "AF", "F-80C"  , "A2-2023", "N", 16, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

endturn()

starttestsetup()

A1 = aircraft("A1", "AF", "F-80C"  , "A2-2027", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C"  , "A2-2027", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C"  , "A2-2027", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 3

A0 = aircraft("A0", "AF", "F-80C"  , "A2-2023", "N",  4, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "AF", "F-80C"  , "A2-2023", "N",  5, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "AF", "F-80C"  , "A2-2023", "N",  6, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "AF", "F-80C"  , "A2-2023", "N",  7, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "AF", "F-80C"  , "A2-2023", "N",  8, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "AF", "F-80C"  , "A2-2023", "N",  9, 4.0, "CL")
assert A1._rocketattackrange(A0) == 4
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "AF", "F-80C"  , "A2-2023", "N", 10, 4.0, "CL")
assert A1._rocketattackrange(A0) == 4
assert A2._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."
assert A3._rocketattackrange(A0) == 4

A0 = aircraft("H0", "AF", "F-80C"  , "A2-2023", "N", 11, 4.0, "CL")
assert A1._rocketattackrange(A0) == 4
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == 4

A0 = aircraft("I0", "AF", "F-80C"  , "A2-2023", "N", 12, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("J0", "AF", "F-80C"  , "A2-2023", "N", 13, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("K0", "AF", "F-80C"  , "A2-2023", "N", 14, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("L0", "AF", "F-80C"  , "A2-2023", "N", 15, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

A0 = aircraft("M0", "AF", "F-80C"  , "A2-2023", "N", 16, 4.0, "CL")
assert A1._rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2._rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3._rocketattackrange(A0) == "the target is not in the arc or range of the weapon."

endturn()

endfile(__file__)