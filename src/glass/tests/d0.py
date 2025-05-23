from glass.tests.infrastructure import *

startfile(__file__, "turns")

# Turns

# Basic Turns

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "N", 10, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "N", 10, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2215", "N", 10, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2415", "N", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "TTL/H,H/L,TTL/H,H/L")
A1._assert("A1-1711       WNW  10", 4.0)
A2.move("LVL", "M", "TTL/H,H/L,H,H/WL")
A2._assert("A1-1911       NNW  10", 4.0)
A3.move("LVL", "M", "TTR/H,H/R,H,H/WL")
A3._assert("A1-2311       NNE  10", 4.0)
A4.move("LVL", "M", "TTR/H,H/R,TTR/H,H/R")
A4._assert("A1-2511       ENE  10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H/WL,TTR/H,H/R,TTR/H")
A1._assert("A1-1309/1409  NNW  10", 4.0)
A2.move("LVL", "M", "TTR/H,H/R,TTR/H,H/R")
A2._assert("A1-1808       NNE  10", 4.0)
A3.move("LVL", "M", "TTL/H,H/L,TTL/H,H/L")
A3._assert("A1-2408       NNW  10", 4.0)
A4.move("LVL", "M", "H/WL,TTL/H,H/L,TTL/H")
A4._assert("A1-2809/2909  NNE  10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H/R,H/WL,TTL/H,H/L")
A1._assert("A1-1305       NNW  10", 4.0)
A2.move("LVL", "M", "H/WL,TTL/H,H/L,H")
A2._assert("A1-1904       N    10", 4.5)
A3.move("LVL", "M", "H/WL,TTR/H,H/R,H")
A3._assert("A1-2304       N    10", 4.5)
A4.move("LVL", "M", "H/L,H/WL,TTR/H,H/R")
A4._assert("A1-2905       NNE  10", 4.0)
endgameturn()

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1915", "N", 12, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2115", "N", 12, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "TTL/H,H/L,H/WL,HTR/H/R")
A1._assert("A1-1812       N    12", 4.0)
A2.move("LVL", "M", "TTR/H,H/R,H/WL,HTL/H/L")
A2._assert("A1-2212       N    12", 4.0)
endgameturn()

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2014", "W", 12, 2.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "W", 12, 3.0, "CL")
endtestsetup()

for i in range(1, 13):
    startgameturn()
    A1.move("LVL", 0, "EZR/H,H/R")
    A2.move("LVL", 0, "EZR/H,H,H/R")
    endgameturn()
A1._assert("A1-2014       W    12", 2.0)
A2._assert("A1-2015       W    12", 3.0)

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-2014", "E", 12, 2.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "E", 12, 3.0, "CL")
endtestsetup()

for i in range(1, 13):
    startgameturn()
    A1.move("LVL", 0, "EZL/H,H/L")
    A2.move("LVL", 0, "EZL/H,H,H/L")
    endgameturn()

A1._assert("A1-2014       E    12", 2.0)
A2._assert("A1-2015       E    12", 3.0)

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "ENE", 10, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "ENE", 10, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2215", "ENE", 10, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2415", "ENE", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "BTL/H/LL,BTL/H/LL,BTL/H/LL,HTL/H/L")
A1._assert("A1-1713       SSW  10", 2.5)
A2.move("LVL", "M", "HTL/H/L,HTL/H/L,HTL/H/L,HTL/H/L")
A2._assert("A1-2012       WNW  10", 3.5)
A3.move("LVL", "M", "TTL/H,H/L,TTL/H,H/L")
A3._assert("A1-2512       N    10", 4.0)
A4.move("LVL", "M", "EZL/H,H,H/L,EZL/H")
A4._assert("A1-2712/2813  NNE  10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "HTL/H/LLL,HTL/H/LLL")
A1._assert("A1-1815       NNE  10", 1.5)
A2.move("LVL", "M", "HTL/H/L,HTL/H/L,HTL/H/L")
A2._assert("A1-1712       SSW  10", 3.0)
A3.move("LVL", "M", "TTL/H,H/L,TTL/H,H/L")
A3._assert("A1-2409       WNW  10", 4.0)
A4.move("LVL", "M", "H,H/L,EZL/H,H")
A4._assert("A1-2809       N    10", 4.5)
endgameturn()

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "NNE", 10, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "NNE", 10, 4.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2215", "NNE", 10, 4.0, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2415", "NNE", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "BTL/H/LLL,BTL/H/LLL,BTL/H/LLL,BTL/H/LLL")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A2.move("LVL", "M", "HTL/H/LL,HTL/H/L,HTL/H/L,HTL/H/L")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A3.move("LVL", "M", "H/L,H,H,H/L")
asserterror("attempt to maneuver without a declaration.")
startgameturn()
A4.move("LVL", "M", "EZL/H,H,H/R,H")
asserterror("attempt to maneuver against the sense of the declaration.")
startgameturn()
A1.move("LVL", "M", "BTL/H/LL,BTL/H/LL,BTL/H/LL,BTL/H/LL")
A1._assert("A1-1615       SSE  10", 2.5)
A2.move("LVL", "M", "HTL/H/L,HTL/H/L,HTL/H/L,HTL/H/L")
A2._assert("A1-1812       W    10", 3.5)
A3.move("LVL", "M", "HTL/H,H/L,HTL/H,H/L")
A3._assert("A1-2311       NNW  10", 4.0)
A4.move("LVL", "M", "EZR/H,H,H/R,H")
A4._assert("A1-2712       ENE  10", 4.0)
endgameturn()


# Check that we use the correct alitude band when we change altitude. When we
# pop up from MH (25) to HI (26), we use the turn rate in MH (4 FPs for an EZ
# turn rate). When we pop down again, we use the turn rate in HI (6 FPs for an
# EZ turn rate). Check that the turn requirement is recalculated at the start
# of each game turn.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A2-2030", "N", 25, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-2230", "N", 25, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("ZC", "M", "H,EZR/H,H,C")
A1._assert("A2-2027       N    26", 4.0)
A2.move("LVL", "M", "H,H,H,EZR/H")
A2._assert("A2-2226       N    25", 4.0)
endgameturn()

startgameturn()
A1.move("SD", "M", "H/R,EZR/H,H,D")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A1.move("SD", "M", "H,H/R,EZR/H,D")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A1.move("SD", "M", "H,H,H/R,EZR/D")
A1._assert("A2-2024       NNE  25", 4.5)
A2.move("ZC", "M", "H,C,H/R,EZR/H")
A2._assert("A2-2223/2323  NNE  26", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H/R,H,H,H")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A1.move("LVL", "M", "H,H/R,H,H")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A2.move("LVL", "M", "H,H,H,H/R")
asserterror("attempt to turn faster than the declared turn rate.")
startgameturn()
A1.move("LVL", "M", "H,H,H/R,H")
A1._assert("A2-2321       ENE  25", 4.5)
A2.move("LVL", "M", "H,H,H,H")
A2._assert("A2-2420/2520  NNE  26", 4.5)
endgameturn()

startgameturn()
A1.move("LVL", "M", "H,H,H,H")
A2.move("SD", "M", "H/R,D,H,H")
A2._assert("A2-2718       ENE  25", 5.0)
endgameturn()

# Turning and minimum speeds.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1815", "N", 10, 1.5, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2015", "N", 10, 2.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-2215", "N", 10, 2.5, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-2415", "N", 10, 3.0, "CL")
A5 = setupaircraft("A5", "AF", "F-80C", "A1-2615", "N", 10, 3.5, "CL")
endtestsetup()

startgameturn()
A1.move("SD", "N", "TTR/H")
asserterror("speed limits the turn rate to EZ.")
startgameturn()
A2.move("SD", "N", "HTR/H,H")
asserterror("speed limits the turn rate to TT.")
startgameturn()
A3.move("SD", "N", "BTR/H,H")
asserterror("speed limits the turn rate to HT.")
startgameturn()
A4.move("SD", "N", "ETR/H,H,H")
asserterror("speed limits the turn rate to BT.")
startgameturn()
A5.move("SD", "N", "ETR/H,H,H")
asserterror("aircraft does not allow a turn rate of ET.")
startgameturn()
A1.move("SD", "N", "EZR/D")
asserterror("insufficient initial HFPs.")
startgameturn()
A1.move("LVL", "N", "EZR/H")
A1._assert("A1-1814       N    10", 1.5)
A2.move("SD", "N", "TTR/H,D")
A2._assert("A1-2014       N     9", 2.0)
A3.move("SD", "N", "HTR/H,D")
A3._assert("A1-2214       N     9", 2.5)
A4.move("SD", "N", "BTR/H,H,D")
A4._assert("A1-2413       N     9", 3.0)
A5.move("SD", "N", "BTR/H,H,D")
A5._assert("A1-2613       N     9", 3.5)

endgameturn()

# Turning and configuration.

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-104A", "A1-1815", "N", 10, 6.0, "CL")
A2 = setupaircraft("A2", "AF", "F-104A", "A1-2015", "N", 10, 6.0, "1/2")
endtestsetup()

startgameturn()
A2.move("LVL", "AB", "BTR/H,H,H,H,H,H")
asserterror("aircraft does not allow a turn rate of BT.")
startgameturn()
A1.move("LVL", "AB", "BTR/H,H,H,H,H,H")
A1._assert("A1-1809       N    10", 6.0)
A2.move("LVL", "AB", "HTR/H,H,H,H,H,H")
A2._assert("A1-2009       N    10", 6.0)
endgameturn()

# Turning at SS speed

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-100A", "A1-1815", "N", 20, 8.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "ETR/H,H/R,ETR/H,H/R,ETR/H,H/R,ETR/H,H/R")
A1._assert("A1-2310       ESE  20", 7.0)
endgameturn()

# Turning and GSSM/PSSM aircraft

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-104A", "A1-1215", "N", 10, 7.5, "CL")  # GSSM
A2 = setupaircraft("A2", "AF", "F-100A", "A1-1415", "N", 10, 7.5, "CL")
A3 = setupaircraft("A3", "AF", "F-102A", "A1-1615", "N", 10, 7.5, "CL")  # PSSM
A4 = setupaircraft("A4", "AF", "F-102A", "A1-1815", "N", 10, 7.5, "1/2")  # PSSM
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "BTR/H,H,H,H,H,H,H")
A1._assert("A1-1208       N    10", 7.5)
startgameturn()
A1.move("LVL", 2.5, "BTR/H,H/R,BTR/H,H/R,BTR/H,H/R,H")
A1._assert("A1-1610/1611  E    10", 6.5)
startgameturn()
A2.move("LVL", "AB", "BTR/H,H,H,H,H,H,H")
A2._assert("A1-1408       N    10", 7.0)
startgameturn()
A2.move("LVL", 2.0, "BTR/H,H/R,BTR/H,H/R,BTR/H,H/R,H")
A2._assert("A1-1810/1811  E    10", 6.5)
startgameturn()
A3.move("LVL", "AB", "ETR/H,H,H,H,H,H,H")
asserterror("aircraft does not allow a turn rate of ET.")
startgameturn()
A3.move("LVL", "AB", "BTR/H,H,H,H,H,H,H")
A3._assert("A1-1608       N    10", 7.0)
startgameturn()
A3.move("LVL", 1.5, "BTR/H,H/R,BTR/H,H/R,BTR/H,H/R,H")
A3._assert("A1-2010/2011  E    10", 6.0)
startgameturn()
A4.move("LVL", "AB", "BTR/H,H,H,H,H,H,H")
asserterror("aircraft does not allow a turn rate of BT.")
startgameturn()
A4.move("LVL", "AB", "HTR/H,H,H,H,H,H,H")
A4._assert("A1-1808       N    10", 7.0)
endgameturn()

# Check that turn drag applies even if the aircraft doesn't change facing.

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-80C", "A2-1230", "N", 10, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A2-1230", "N", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "N", "H,H,H,H")
A1._assert("A2-1226       N    10", 4.0)
A2.move("LVL", "N", "BTR/H,H,H,H")
A2._assert("A2-1226       N    10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "N", "H,H,H,H")
A1._assert("A2-1222       N    10", 4.0)
A2.move("LVL", "N", "H,H,H,H")
A2._assert("A2-1222       N    10", 3.5)
endgameturn()

startgameturn()
A1.move("LVL", "N", "H,H,H,H")
A1._assert("A2-1218       N    10", 4.0)
A2.move("LVL", "N", "H,H,H")
A2._assert("A2-1219       N    10", 3.5)
endgameturn()

startgameturn()
A1.move("LVL", "N", "H,H,H,H")
A1._assert("A1-1214       N    10", 4.0)
A2.move("LVL", "N", "H,H,H,H")
A2._assert("A1-1215       N    10", 3.0)
endgameturn()

# Continued turns.

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-80C", "A2-1220", "N", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "N", "HTR/H/R+,H/R+,BTR/H/RR+,HTR/H/R+")
A1._assert("A2-1518       SSE  10", 3.0)
endgameturn()

startgameturn()
A1.move("LVL", "N", "H/RR+,BTR/H/RRR+,H/RRR+")
A1._assert("A2-1319       NNE  10", 1.0)
endgameturn()

endfile(__file__)
