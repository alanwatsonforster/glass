from apengine._tests.infrastructure import *
startfile(__file__, "turns")

# Turns

# Basic Turns

starttestsetup()
A1 = aircraft("A1", "F-80C", "1815", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", "2015", "N", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C", "2215", "N", 10, 4.0, "CL")
A4 = aircraft("A4", "F-80C", "2415", "N", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "M", "TTL/H,HL,TTL/H,HL"   )
A1._assert("1711       WNW  10",  4.0)
A2.move("LVL",  "M", "TTL/H,HL,H,WL/H")
A2._assert("1911       NNW  10",  4.0)
A3.move("LVL",  "M", "TTR/H,HR,H,WL/H")
A3._assert("2311       NNE  10",  4.0)
A4.move("LVL",  "M", "TTR/H,HR,TTR/H,HR"   )
A4._assert("2511       ENE  10",  4.0)
endturn()

startturn()
A1.move("LVL",  "M", "WL/H,TTR/H,HR,TTR/H")
A1._assert("1309/1409  NNW  10",  4.0)
A2.move("LVL",  "M", "TTR/H,HR,TTR/H,HR"   )
A2._assert("1808       NNE  10",  4.0)
A3.move("LVL",  "M", "TTL/H,HL,TTL/H,HL"   )
A3._assert("2408       NNW  10",  4.0)
A4.move("LVL",  "M", "WL/H,TTL/H,HL,TTL/H")
A4._assert("2809/2909  NNE  10",  4.0)
endturn()

startturn()
A1.move("LVL",  "M", "HR,H/WL,TTL/H,HL")
A1._assert("1305       NNW  10",  4.0)
A2.move("LVL",  "M", "H/WL,TTL/H,HL,H" )
A2._assert("1904       N    10",  4.5)
A3.move("LVL",  "M", "H/WL,TTR/H,HR,H" )
A3._assert("2304       N    10",  4.5)
A4.move("LVL",  "M", "HL,H/WL,TTR/H,HR")
A4._assert("2905       NNE  10",  4.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C", "1915", "N", 12, 4.0, "CL")
A2 = aircraft("A2", "F-80C", "2115", "N", 12, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL", "M", "TTL/H,HL,WL/H,HTR/HR")
A1._assert("1812       N    12", 4.0)
A2.move("LVL", "M", "TTR/H,HR,WL/H,HTL/HL")
A2._assert("2212       N    12", 4.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C", "2014", "W", 12, 2.0, "CL")
A2 = aircraft("A2", "F-80C", "2015", "W", 12, 3.0, "CL")
endtestsetup()

for i in range(1, 13):
  startturn()
  A1.move("LVL", 0, "EZR/H,HR")
  A2.move("LVL", 0, "EZR/H,H,HR")
  endturn()
A1._assert("2014       W    12", 2.0)
A2._assert("2015       W    12", 3.0)

starttestsetup()
A1 = aircraft("A1", "F-80C", "2014", "E", 12, 2.0, "CL")
A2 = aircraft("A2", "F-80C", "2015", "E", 12, 3.0, "CL")
endtestsetup()

for i in range(1, 13):
  startturn()
  A1.move("LVL", 0, "EZL/H,HL")
  A2.move("LVL", 0, "EZL/H,H,HL")
  endturn()
  
A1._assert("2014       E    12", 2.0)
A2._assert("2015       E    12", 3.0)

starttestsetup()
A1 = aircraft("A1", "F-80C", "1815", "ENE", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", "2015", "ENE", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C", "2215", "ENE", 10, 4.0, "CL")
A4 = aircraft("A4", "F-80C", "2415", "ENE", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "M", "BTL/HLL,BTL/HLL,BTL/HLL,HTL/HL")
A1._assert("1713       SSW  10",  3.0)
A2.move("LVL",  "M", "HTL/HL,HTL/HL,HTL/HL,HTL/HL"       )
A2._assert("2012       WNW  10",  3.5)
A3.move("LVL",  "M", "TTL/H,HL,TTL/H,HL"         )
A3._assert("2512       N    10",  4.0)
A4.move("LVL",  "M", "EZL/H,H,HL,EZL/H"          )
A4._assert("2712/2813  NNE  10",  4.0)
endturn()

startturn()
A1.move("LVL",  "M", "BTL/HLLL,BTL/HLLL,TTL/HL")
A1._assert("1814       N    10",  2.0)
A2.move("LVL",  "M", "HTL/HL,HTL/HL,HTL/HL"            )
A2._assert("1712       SSW  10",  3.0)
A3.move("LVL",  "M", "TTL/H,HL,TTL/H,HL"           )
A3._assert("2409       WNW  10",  4.0)
A4.move("LVL",  "M", "H,HL,EZL/H,H"            )
A4._assert("2809       N    10",  4.5)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C", "1815", "NNE", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", "2015", "NNE", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C", "2215", "NNE", 10, 4.0, "CL")
A4 = aircraft("A4", "F-80C", "2415", "NNE", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "M", "BTL/HLLL,BTL/HLLL,BTL/HLLL,BTL/HLLL")
asserterror("attempt to turn faster than the declared turn rate.")
A1.move("LVL",  "M", "BTL/HLL,BTL/HLL,BTL/HLL,BTL/HLL")
A1._assert("1615       SSE  10",  2.5)
A2.move("LVL",  "M", "HTL/HLL,HTL/HL,HTL/HL,HTL/HL"       )
asserterror("attempt to turn faster than the declared turn rate.")
A2.move("LVL",  "M", "HTL/HL,HTL/HL,HTL/HL,HTL/HL"       )
A2._assert("1812       W    10",  3.5)
A3.move("LVL",  "M", "HL,H,H,HL"              )
asserterror("attempt to maneuver without a declaration.")
A3.move("LVL",  "M", "HTL/H,HL,HTL/H,HL"              )
A3._assert("2311       NNW  10",  4.0)
A4.move("LVL",  "M", "EZL/H,H,HR,H"           )
asserterror("attempt to maneuver against the sense of the declaration.")
A4.move("LVL",  "M", "EZR/H,H,HR,H"           )
A4._assert("2712       ENE  10",  4.0)
endturn()


# Check that we use the correct alitude band when we change altitude. When we 
# pop up from MH (25) to HI (26), we use the turn rate in MH (4 FPs for an EZ 
# turn rate). When we pop down again, we use the turn rate in HI (6 FPs for an 
# EZ turn rate). Check that the turn requirement is recalculated at the start
# of each game turn.

starttestsetup()
A1 = aircraft("A1", "F-80C", "2030", "N", 25, 4.0, "CL")
A2 = aircraft("A2", "F-80C", "2230", "N", 25, 4.0, "CL")
endtestsetup()

startturn()
A1.move("ZC" ,  "M", "H,EZR/H,H,C")
A1._assert("2027       N    26",  4.0)
A2.move("LVL",  "M", "H,H,H,EZR/H")
A2._assert("2226       N    25",  4.0)
endturn()

startturn()
A1.move("SD" ,  "M", "H/R,EZR/H,H,D"  )
asserterror("attempt to turn faster than the declared turn rate.")
A1.move("SD" ,  "M", "H,H/R,EZR/H,D"  )
asserterror("attempt to turn faster than the declared turn rate.")
A1.move("SD" ,  "M", "H,H,H/R,EZR/D"  )
A1._assert("2024       NNE  25",  4.0)
A2.move("ZC" , "M", "H,C,H/R,EZR/H"   )
A2._assert("2223/2323  NNE  26",  4.0)
endturn()

startturn()
A1.move("LVL",  "M", "H/R,H,H,H"  )
asserterror("attempt to turn faster than the declared turn rate.")
A1.move("LVL",  "M", "H,H/R,H,H"  )
asserterror("attempt to turn faster than the declared turn rate.")
A1.move("LVL",  "M", "H,H,H/R,H"  )
A1._assert("2321       ENE  25",  4.5)
A2.move("LVL",  "M", "H,H,H,HR"    )
asserterror("attempt to turn faster than the declared turn rate.")
A2.move("LVL",  "M", "H,H,H,H"    )
A2._assert("2420/2520  NNE  26",  4.5)
endturn()

startturn()
A1.move("LVL",  "M", "H,H,H,H"  )
A2.move("SD",  "M", "HR,D,H,H"    )
A2._assert("2718       ENE  25",  4.5)
endturn()

# Turning and minimum speeds.

starttestsetup()
A1 = aircraft("A1", "F-80C", "1815", "N", 10, 1.5, "CL")
A2 = aircraft("A2", "F-80C", "2015", "N", 10, 2.0, "CL")
A3 = aircraft("A3", "F-80C", "2215", "N", 10, 2.5, "CL")
A4 = aircraft("A4", "F-80C", "2415", "N", 10, 3.0, "CL")
A5 = aircraft("A5", "F-80C", "2615", "N", 10, 3.5, "CL")
endtestsetup()

startturn()
A1.move("SD" ,  "N", "TTR/H"    )
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
A2.move("SD" ,  "N", "HTR/H,H"  )
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
A3.move("SD" ,  "N", "BTR/H,H"  )
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
A4.move("SD" ,  "N", "ETR/H,H,H")
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
A5.move("SD" ,  "N", "ETR/H,H,H")
asserterror("attempt to declare a turn rate tighter than allowed by the aircraft.")

A1.move("SD" ,  "N", "EZR/D"    )
asserterror("insufficient initial HFPs.")
A1.move("LVL" , "N", "EZR/H"    )
A1._assert("1814       N    10",  1.5)
A2.move("SD" ,  "N", "TTR/H,D"  )
A2._assert("2014       N     9",  2.0)
A3.move("SD" ,  "N", "HTR/H,D"  )
A3._assert("2214       N     9",  2.5)
A4.move("SD" ,  "N", "BTR/H,H,D")
A4._assert("2413       N     9",  3.0)
A5.move("SD" ,  "N", "BTR/H,H,D")
A5._assert("2613       N     9",  3.5)

endturn()

# Turning and configuration.

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-104A", "1815", "N", 10, 6.0, "CL")
A2 = aircraft("A2", "F-104A", "2015", "N", 10, 6.0, "1/2")
endtestsetup()

startturn()
A1.move("LVL",  "AB", "BTR/H,H,H,H,H,H"    )
A1._assert("1809       N    10",  6.0)
A2.move("LVL",  "AB", "BTR/H,H,H,H,H,H"  )
asserterror("attempt to declare a turn rate tighter than allowed by the aircraft.")
A2.move("LVL",  "AB", "HTR/H,H,H,H,H,H"    )
A2._assert("2009       N    10",  6.0)
endturn()

# Turning at SS speed

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-100A", "1815", "N", 20, 8.5, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "AB", "ETR/H,HR,ETR/H,HR,ETR/H,HR,ETR/H,HR"    )
A1._assert("2310       ESE  20",  7.0)
endturn()

# Turning and GSSM/PSSM aircraft

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-104A", "1215", "N", 10, 7.5, "CL") # GSSM
A2 = aircraft("A2", "F-100A", "1415", "N", 10, 7.5, "CL")
A3 = aircraft("A3", "F-102A", "1615", "N", 10, 7.5, "CL") # PSSM
A4 = aircraft("A4", "F-102A", "1815", "N", 10, 7.5, "1/2") # PSSM
endtestsetup()

startturn()
A1.move("LVL" ,  "AB", "BTR/H,H,H,H,H,H,H"   )
A1._assert("1208       N    10",  7.5)
A1.move("LVL" ,  2.5, "BTR/H,HR,BTR/H,HR,BTR/H,HR,H" )
A1._assert("1610/1611  E    10",  6.5)
A2.move("LVL" ,  "AB", "BTR/H,H,H,H,H,H,H"   )
A2._assert("1408       N    10",  7.0)
A2.move("LVL" ,  2.0, "BTR/H,HR,BTR/H,HR,BTR/H,HR,H" )
A2._assert("1810/1811  E    10",  6.5)
A3.move("LVL" ,  "AB", "ETR/H,H,H,H,H,H,H"   )
asserterror("attempt to declare a turn rate tighter than allowed by the aircraft.")
A3.move("LVL" ,  "AB", "BTR/H,H,H,H,H,H,H"   )
A3._assert("1608       N    10",  7.0)
A3.move("LVL" ,  1.5, "BTR/H,HR,BTR/H,HR,BTR/H,HR,H" )
A3._assert("2010/2011  E    10",  6.0)
A4.move("LVL" ,  "AB", "BTR/H,H,H,H,H,H,H"   )
asserterror("attempt to declare a turn rate tighter than allowed by the aircraft.")
A4.move("LVL" ,  "AB", "HTR/H,H,H,H,H,H,H"   )
A4._assert("1808       N    10",  7.0)
endturn()

# Check that turn drag applies even if the aircraft doesn't change facing.

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-80C", "1230", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", "1230", "N", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "N", "H,H,H,H"    )
A1._assert("1226       N    10", 4.0)
A2.move("LVL",  "N", "BTR/H,H,H,H")
A2._assert("1226       N    10", 4.0)
endturn()

startturn()
A1.move("LVL",  "N", "H,H,H,H")
A1._assert("1222       N    10", 4.0)
A2.move("LVL",  "N", "H,H,H,H")
A2._assert("1222       N    10", 3.5)
endturn()

startturn()
A1.move("LVL",  "N", "H,H,H,H")
A1._assert("1218       N    10", 4.0)
A2.move("LVL",  "N", "H,H,H"  )
A2._assert("1219       N    10", 3.5)
endturn()

startturn()
A1.move("LVL",  "N", "H,H,H,H")
A1._assert("1214       N    10", 4.0)
A2.move("LVL",  "N", "H,H,H,H")
A2._assert("1215       N    10", 3.0)
endturn()

# Continued turns.

starttestsetup(verbose=False)
A1 = aircraft("A1", "F-80C", "1220", "N", 10, 4.0, "CL")
endtestsetup()

startturn()
A1.move("LVL",  "N", "HTR/HR+,HR+,BTR/HRR+,HTR/HR+"    )
A1._assert("1518       SSE  10", 3.0)
endturn()

startturn()
A1.move("LVL",  "N", "HRR+,BTR/HRRR+,HRRR+"    )
A1._assert("1319       NNE  10", 1.0)
endturn()

endfile(__file__)