from apxo._tests.infrastructure import *
startfile(__file__, "rocket attack range")

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "1924/1925", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("B2", "F-80C"  , "2025", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("C2", "F-80C"  , "2124/2125", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("D2", "F-80C"  , "1924/2025", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("E2", "F-80C"  , "2124/2025", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("F2", "F-80C"  , "1924", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("G2", "F-80C"  , "2024/2025", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("H2", "F-80C"  , "2124", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("I2", "F-80C"  , "1924/2024", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("J2", "F-80C"  , "2124/2024", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("K2", "F-80C"  , "1923/1924", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("L2", "F-80C"  , "2024", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("M2", "F-80C"  , "2123/2124", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("N2", "F-80C"  , "1923/2024", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("O2", "F-80C"  , "2123/2024", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1

A2 = aircraft("P2", "F-80C"  , "1923", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("Q2", "F-80C"  , "2023/2024", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("R2", "F-80C"  , "2123", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("S2", "F-80C"  , "1923/2023", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("T2", "F-80C"  , "2123/2023", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2

A2 = aircraft("U2", "F-80C"  , "1922/1923", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("V2", "F-80C"  , "2023", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("W2", "F-80C"  , "2122/2123", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("X2", "F-80C"  , "1922/2023", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("Y2", "F-80C"  , "2122/2023", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2

A2 = aircraft("Z2", "F-80C"  , "1922", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AA2", "F-80C"  , "2022/2023", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("AB2", "F-80C"  , "2122", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AC2", "F-80C"  , "1922/2022", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AD2", "F-80C"  , "2122/2022", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3

A2 = aircraft("AE2", "F-80C"  , "1921/1922", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AF2", "F-80C"  , "2022", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AG2", "F-80C"  , "2121/2122", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AH2", "F-80C"  , "1921/2022", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AI2", "F-80C"  , "2121/2022", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3

A2 = aircraft("AJ2", "F-80C"  , "1921", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AK2", "F-80C"  , "2021/2022", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AL2", "F-80C"  , "2121", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AM2", "F-80C"  , "1921/2021", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AN2", "F-80C"  , "2121/2021", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4

A2 = aircraft("AO2", "F-80C"  , "1920/1921", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AP2", "F-80C"  , "2021", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AQ2", "F-80C"  , "2120/2121", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AR2", "F-80C"  , "1920/2021", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AS2", "F-80C"  , "2120/2021", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4

A2 = aircraft("AT2", "F-80C"  , "1920", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AU2", "F-80C"  , "2020/2021", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AV2", "F-80C"  , "2120", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AW2", "F-80C"  , "1920/2020", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AX2", "F-80C"  , "2120/2020", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AY2", "F-80C"  , "1919/1920", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AZ2", "F-80C"  , "2020", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("BA2", "F-80C"  , "2119/2120", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("BB2", "F-80C"  , "1919/2020", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("BC2", "F-80C"  , "2119/2020", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("BD2", "F-80C"  , "1919", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("BE2", "F-80C"  , "2019/2020", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("BF2", "F-80C"  , "2119", "W", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "NNE", 5, 4.0, "CL")

A2 = aircraft("A2", "F-80C"  , "1924", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("B2", "F-80C"  , "1924/2025", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("C2", "F-80C"  , "2025", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("D2", "F-80C"  , "2025/2125", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("E2", "F-80C"  , "2125", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("F2", "F-80C"  , "1924/2024", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("G2", "F-80C"  , "2024/2025", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("H2", "F-80C"  , "2025/2124", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("I2", "F-80C"  , "2124/2125", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("J2", "F-80C"  , "1923/2024", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("K2", "F-80C"  , "2024", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("L2", "F-80C"  , "2024/2124", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("M2", "F-80C"  , "2124", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("N2", "F-80C"  , "2124/2225", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("O2", "F-80C"  , "2023/2024", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("P2", "F-80C"  , "2024/2123", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("Q2", "F-80C"  , "2123/2124", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("R2", "F-80C"  , "2124/2224", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("S2", "F-80C"  , "2023", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("T2", "F-80C"  , "2023/2123", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("U2", "F-80C"  , "2123", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("V2", "F-80C"  , "2123/2224", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("W2", "F-80C"  , "2224", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("X2", "F-80C"  , "2023/2122", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("Y2", "F-80C"  , "2122/2123", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("Z2", "F-80C"  , "2123/2223", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("AA2", "F-80C" , "2223/2224", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AB2", "F-80C"  , "2022/2122", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AC2", "F-80C"  , "2122", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AD2", "F-80C"  , "2122/2223", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AE2", "F-80C"  , "2223", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AF2", "F-80C"  , "2223/2323", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AG2", "F-80C"  , "2121/2122", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AH2", "F-80C"  , "2222/2122", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AI2", "F-80C"  , "2222/2223", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AJ2", "F-80C"  , "2223/2322", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AK2", "F-80C"  , "2121", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AL2", "F-80C"  , "2121/2222", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AM2", "F-80C"  , "2222", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AN2", "F-80C"  , "2222/2322", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AO2", "F-80C"  , "2322", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AP2", "F-80C" , "2121/2221", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AQ", "F-80C"  , "2222/2221", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AR", "F-80C"  , "2222/2321", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AS2", "F-80C" , "2322/2321", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
  
A2 = aircraft("AT2", "F-80C"  , "2120/2221", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AU2", "F-80C"  , "2221", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AV2", "F-80C"  , "2221/2321", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AW2", "F-80C"  , "2321", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AX2", "F-80C"  , "2321/2422", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

endtestsetup()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2024/2025", "E", 5, 4.0, "CL")
    
A2 = aircraft("A2", "F-80C"  , "2023/2024", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("B2", "F-80C"  , "2024", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("C2", "F-80C"  , "2024/2025", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("D2", "F-80C"  , "2025", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("E2", "F-80C"  , "2025/2026", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("F2", "F-80C"  , "2024/2123", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("G2", "F-80C"  , "2024/2124", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("H2", "F-80C"  , "2025/2124", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("I2", "F-80C"  , "2025/2125", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("J2", "F-80C"  , "2123", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("K2", "F-80C"  , "2123/2124", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("L2", "F-80C"  , "2124", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("M2", "F-80C"  , "2124/2125", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("N2", "F-80C"  , "2125", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("O2", "F-80C"  , "2123/2224", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("P2", "F-80C"  , "2124/2224", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("Q2", "F-80C"  , "2124/2225", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 1
A2 = aircraft("R2", "F-80C"  , "2125/2225", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("S2", "F-80C"  , "2223/2224", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("T2", "F-80C"  , "2224", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("U2", "F-80C"  , "2224/2225", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("V2", "F-80C"  , "2225", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("W2", "F-80C"  , "2225/2226", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("X2", "F-80C"  , "2224/2323", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("Y2", "F-80C"  , "2224/2324", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("Z2", "F-80C"  , "2225/2324", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 2
A2 = aircraft("AA2", "F-80C"  , "2225/2325", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AB2", "F-80C"  , "2323", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AC2", "F-80C"  , "2323/2324", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AD2", "F-80C"  , "2324", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AE2", "F-80C"  , "2324/2325", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AF2", "F-80C"  , "2325", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AG2", "F-80C"  , "2323/2424", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AH2", "F-80C"  , "2324/2424", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AI2", "F-80C"  , "2324/2425", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 3
A2 = aircraft("AJ2", "F-80C"  , "2325/2425", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AK2", "F-80C"  , "2423/2424", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AL2", "F-80C"  , "2424", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AM2", "F-80C"  , "2424/2425", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AN2", "F-80C"  , "2425", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AO2", "F-80C"  , "2425/2426", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AP2", "F-80C"  , "2424/2523", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AQ2", "F-80C"  , "2424/2524", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AR2", "F-80C"  , "2425/2524", "NNW", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == 4
A2 = aircraft("AS2", "F-80C"  , "2425/2525", "NNE", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

A2 = aircraft("AT2", "F-80C"  , "2523", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AU2", "F-80C"  , "2523/2524", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AV2", "F-80C"  , "2524", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AW2", "F-80C"  , "2524/2525", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."
A2 = aircraft("AX2", "F-80C"  , "2525", "E", 5, 4.0, "CL")
assert A1.rocketattackrange(A2) == "the target is not in the weapon range or arc."

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

A0 = aircraft("A0", "F-80C"  , "2025", "N",  0, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("B0", "F-80C"  , "2025", "N",  1, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("C0", "F-80C"  , "2025", "N",  2, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("D0", "F-80C"  , "2025", "N",  3, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("E0", "F-80C"  , "2025", "N",  4, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("F0", "F-80C"  , "2025", "N",  5, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("G0", "F-80C"  , "2025", "N",  6, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("H0", "F-80C"  , "2025", "N",  7, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("I0", "F-80C"  , "2025", "N",  8, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("J0", "F-80C"  , "2025", "N",  9, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("K0", "F-80C"  , "2025", "N", 10, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("L0", "F-80C"  , "2025", "N", 11, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("M0", "F-80C"  , "2025", "N", 12, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("N0", "F-80C"  , "2025", "N", 13, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("O0", "F-80C"  , "2025", "N", 14, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("P0", "F-80C"  , "2025", "N", 15, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("Q0", "F-80C"  , "2025", "N", 16, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("R0", "F-80C"  , "2025", "N", 17, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("S0", "F-80C"  , "2025", "N", 18, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("T0", "F-80C"  , "2025", "N", 19, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("U0", "F-80C"  , "2025", "N", 20, 4.0, "CL")
assert A1.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

endturn()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2025", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2025", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 1

A0 = aircraft("A0", "F-80C"  , "2024", "N",  0, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "F-80C"  , "2024", "N",  1, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "F-80C"  , "2024", "N",  2, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "F-80C"  , "2024", "N",  3, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "F-80C"  , "2024", "N",  4, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "F-80C"  , "2024", "N",  5, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 3
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "F-80C"  , "2024", "N",  6, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 3
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("H0", "F-80C"  , "2024", "N",  7, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 2
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("I0", "F-80C"  , "2024", "N",  8, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 2
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("J0", "F-80C"  , "2024", "N",  9, 4.0, "CL")
assert A1.rocketattackrange(A0) == 1
assert A2.rocketattackrange(A0) == 1
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("K0", "F-80C"  , "2024", "N", 10, 4.0, "CL")
assert A1.rocketattackrange(A0) == 1
assert A2.rocketattackrange(A0) == 1
assert A3.rocketattackrange(A0) == 1

A0 = aircraft("L0", "F-80C"  , "2024", "N", 11, 4.0, "CL")
assert A1.rocketattackrange(A0) == 1
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 1

A0 = aircraft("M0", "F-80C"  , "2024", "N", 12, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 2

A0 = aircraft("N0", "F-80C"  , "2024", "N", 13, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 2

A0 = aircraft("O0", "F-80C"  , "2024", "N", 14, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 3

A0 = aircraft("P0", "F-80C"  , "2024", "N", 15, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 3

A0 = aircraft("Q0", "F-80C"  , "2024", "N", 16, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("R0", "F-80C"  , "2024", "N", 17, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("S0", "F-80C"  , "2024", "N", 18, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("T0", "F-80C"  , "2024", "N", 19, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("U0", "F-80C"  , "2024", "N", 20, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

endturn()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2025", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2025", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2025", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 2

A0 = aircraft("A0", "F-80C"  , "2023", "N",  4, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "F-80C"  , "2023", "N",  5, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "F-80C"  , "2023", "N",  6, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "F-80C"  , "2023", "N",  7, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 3
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "F-80C"  , "2023", "N",  8, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 3
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "F-80C"  , "2023", "N",  9, 4.0, "CL")
assert A1.rocketattackrange(A0) == 2
assert A2.rocketattackrange(A0) == 2
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "F-80C"  , "2023", "N", 10, 4.0, "CL")
assert A1.rocketattackrange(A0) == 2
assert A2.rocketattackrange(A0) == 2
assert A3.rocketattackrange(A0) == 2

A0 = aircraft("H0", "F-80C"  , "2023", "N", 11, 4.0, "CL")
assert A1.rocketattackrange(A0) == 2
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 2

A0 = aircraft("I0", "F-80C"  , "2023", "N", 12, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 3

A0 = aircraft("J0", "F-80C"  , "2023", "N", 13, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 3

A0 = aircraft("K0", "F-80C"  , "2023", "N", 14, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("L0", "F-80C"  , "2023", "N", 15, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("M0", "F-80C"  , "2023", "N", 16, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

endturn()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2026", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2026", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2026", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 3

A0 = aircraft("A0", "F-80C"  , "2023", "N",  4, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "F-80C"  , "2023", "N",  5, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "F-80C"  , "2023", "N",  6, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "F-80C"  , "2023", "N",  7, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "F-80C"  , "2023", "N",  8, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "F-80C"  , "2023", "N",  9, 4.0, "CL")
assert A1.rocketattackrange(A0) == 3
assert A2.rocketattackrange(A0) == 3
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "F-80C"  , "2023", "N", 10, 4.0, "CL")
assert A1.rocketattackrange(A0) == 3
assert A2.rocketattackrange(A0) == 3
assert A3.rocketattackrange(A0) == 3

A0 = aircraft("H0", "F-80C"  , "2023", "N", 11, 4.0, "CL")
assert A1.rocketattackrange(A0) == 3
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 3

A0 = aircraft("I0", "F-80C"  , "2023", "N", 12, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("J0", "F-80C"  , "2023", "N", 13, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("K0", "F-80C"  , "2023", "N", 14, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("L0", "F-80C"  , "2023", "N", 15, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("M0", "F-80C"  , "2023", "N", 16, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

endturn()

starttestsetup()

A1 = aircraft("A1", "F-80C"  , "2027", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C"  , "2027", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2027", "N", 10, 4.0, "CL")

endtestsetup()

startturn()

A1.move("LVL", "M", "")
A2.move("SD" , "M", "")
A3.move("SC" , "M", "")

# Horizontal range 3

A0 = aircraft("A0", "F-80C"  , "2023", "N",  4, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("B0", "F-80C"  , "2023", "N",  5, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("C0", "F-80C"  , "2023", "N",  6, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("D0", "F-80C"  , "2023", "N",  7, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("E0", "F-80C"  , "2023", "N",  8, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "the target is not in the weapon range or arc."
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("F0", "F-80C"  , "2023", "N",  9, 4.0, "CL")
assert A1.rocketattackrange(A0) == 4
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == "aircraft in climbing flight cannot fire on aircraft at lower altitudes."

A0 = aircraft("G0", "F-80C"  , "2023", "N", 10, 4.0, "CL")
assert A1.rocketattackrange(A0) == 4
assert A2.rocketattackrange(A0) == 4
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("H0", "F-80C"  , "2023", "N", 11, 4.0, "CL")
assert A1.rocketattackrange(A0) == 4
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == 4

A0 = aircraft("I0", "F-80C"  , "2023", "N", 12, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("J0", "F-80C"  , "2023", "N", 13, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("K0", "F-80C"  , "2023", "N", 14, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("L0", "F-80C"  , "2023", "N", 15, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

A0 = aircraft("M0", "F-80C"  , "2023", "N", 16, 4.0, "CL")
assert A1.rocketattackrange(A0) == "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
assert A2.rocketattackrange(A0) == "aircraft in diving flight cannot fire on aircraft at higher altitudes."
assert A3.rocketattackrange(A0) == "the target is not in the weapon range or arc."

endturn()

endfile(__file__)