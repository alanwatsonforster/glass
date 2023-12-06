from apxo.tests.infrastructure import *
startfile(__file__, "visual sighting")

starttestsetup(sheets=[["A1","B1"]])
A1 = aircraft("A1", "AF", "MiG-17F"  , "2015", "N", 6, 4.0)
A2 = aircraft("A2", "AF", "F-86A"  , "2215", "N", 9, 4.0)
A3 = aircraft("A3", "AF", "F-84E"  , "2013", "N", 5, 3.5)
A4 = aircraft("A4", "AF", "F-84E"  , "2012", "NNE", 6, 3.5)
A5 = aircraft("A5", "AF", "F-84E"  , "2012", "NNE", 5, 3.5)
A6 = aircraft("A6", "AF", "F-84E"  , "2012", "NNE", 6, 3.5)
A7 = aircraft("A7", "AF", "F-84E"  , "2012", "NNE", 7, 3.5)
A8 = aircraft("A8", "AF", "F-84E"  , "4012", "NNE", 7, 3.5)
A9 = aircraft("A9", "AF", "MiG-15bis"  , "4012", "NNE", 7, 3.5)
endtestsetup()

startturn()

assert A1.maxvisualsightingrange() == 16
assert A2.visualsightingrange    (A1) == 3
assert A2.visualsightingcondition(A1) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A1) == 2
assert A3.visualsightingcondition(A1) == ("within visual range but blind (30- arc)", False, False, False)
assert A4.visualsightingrange    (A1) == 3
assert A4.visualsightingcondition(A1) == ("within visual range but blind (30- arc)", False, False, False)
assert A5.visualsightingrange    (A1) == 3
assert A5.visualsightingcondition(A1) == ("within visual range but blind (30- arc)", False, False, False)
assert A6.visualsightingrange    (A1) == 3
assert A6.visualsightingcondition(A1) == ("within visual range but blind (30- arc)", False, False, False)
assert A7.visualsightingrange    (A1) == 3
assert A7.visualsightingcondition(A1) == ("within visual range but blind (30- arc)", False, False, False)
assert A8.visualsightingrange    (A1) == 20
assert A8.visualsightingcondition(A1) == ("beyond visual range", False, False, False)
assert A9.visualsightingrange    (A1) == 20
assert A9.visualsightingcondition(A1) == ("beyond visual range", False, False, False)

assert A2.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A2) == 2
assert A1.visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A2) == 4
assert A3.visualsightingcondition(A2) == ("within visual range but restricted (60- arc)", True, True, True)
assert A4.visualsightingrange    (A2) == 4
assert A4.visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A5.visualsightingrange    (A2) == 5
assert A5.visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A6.visualsightingrange    (A2) == 4
assert A6.visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A7.visualsightingrange    (A2) == 4
assert A7.visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A8.visualsightingrange    (A2) == 18
assert A8.visualsightingcondition(A2) == ("within visual range but restricted (60- arc)", True, True, True)
assert A9.visualsightingrange    (A2) == 18
assert A9.visualsightingcondition(A2) == ("within visual range", True, True, False)

assert A3.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A3) == 2
assert A1.visualsightingcondition(A3) == ("within visual range but restricted (180L arc)", True, True, True)
assert A2.visualsightingrange    (A3) == 5
assert A2.visualsightingcondition(A3) == ("within visual range", True, True, False)
assert A4.visualsightingrange    (A3) == 1
assert A4.visualsightingcondition(A3) == ("within visual range but blind (30- arc)", False, False, False)
assert A5.visualsightingrange    (A3) == 1
assert A5.visualsightingcondition(A3) == ("within visual range but blind (30- arc)", False, False, False)
assert A6.visualsightingrange    (A3) == 1
assert A6.visualsightingcondition(A3) == ("within visual range but blind (30- arc)", False, False, False)
assert A7.visualsightingrange    (A3) == 2
assert A7.visualsightingcondition(A3) == ("within visual range but blind (30- arc)", False, False, False)
assert A8.visualsightingrange    (A3) == 21
assert A8.visualsightingcondition(A3) == ("beyond visual range", False, False, False)
assert A9.visualsightingrange    (A3) == 21
assert A9.visualsightingcondition(A3) == ("beyond visual range", False, False, False)

assert A4.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A4) == 3
assert A1.visualsightingcondition(A4) == ("within visual range", True, True, False)
assert A2.visualsightingrange    (A4) == 5
assert A2.visualsightingcondition(A4) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A4) == 1
assert A3.visualsightingcondition(A4) == ("within visual range", True, True, False)
assert A5.visualsightingrange    (A4) == 0
assert A5.visualsightingcondition(A4) == ("within visual range (immediately above)", True, True, False)
assert A6.visualsightingrange    (A4) == 0
assert A6.visualsightingcondition(A4) == ("within visual range but blind (30- arc)", False, False, False)
assert A7.visualsightingrange    (A4) == 0
assert A7.visualsightingcondition(A4) == ("within visual range and can padlock, but blind (immediately below)", False, True, False)
assert A8.visualsightingrange    (A4) == 20
assert A8.visualsightingcondition(A4) == ("within visual range but restricted (60- arc)", True, True, True)
assert A9.visualsightingrange    (A4) == 20
assert A9.visualsightingcondition(A4) == ("within visual range", True, True, False)

assert A5.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A5) == 3
assert A1.visualsightingcondition(A5) == ("within visual range but restricted (180L arc)", True, True, True)
assert A2.visualsightingrange    (A5) == 6
assert A2.visualsightingcondition(A5) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A5) == 1
assert A3.visualsightingcondition(A5) == ("within visual range", True, True, False)
assert A4.visualsightingrange    (A5) == 0
assert A4.visualsightingcondition(A5) == ("within visual range and can padlock, but blind (immediately below)", False, True, False)
assert A6.visualsightingrange    (A5) == 0
assert A6.visualsightingcondition(A5) == ("within visual range and can padlock, but blind (immediately below)", False, True, False)
assert A7.visualsightingrange    (A5) == 1
assert A7.visualsightingcondition(A5) == ("within visual range and can padlock, but blind (immediately below)", False, True, False)
assert A8.visualsightingrange    (A5) == 21
assert A8.visualsightingcondition(A5) == ("beyond visual range", False, False, False)
assert A9.visualsightingrange    (A5) == 21
assert A9.visualsightingcondition(A5) == ("beyond visual range", False, False, False)

assert A6.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A6) == 3
assert A1.visualsightingcondition(A6) == ("within visual range", True, True, False)
assert A2.visualsightingrange    (A6) == 5
assert A2.visualsightingcondition(A6) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A6) == 1
assert A3.visualsightingcondition(A6) == ("within visual range", True, True, False)
assert A4.visualsightingrange    (A6) == 0
assert A4.visualsightingcondition(A6) == ("within visual range but blind (30- arc)", False, False, False)
assert A5.visualsightingrange    (A6) == 0
assert A5.visualsightingcondition(A6) == ("within visual range (immediately above)", True, True, False)
assert A7.visualsightingrange    (A6) == 0
assert A7.visualsightingcondition(A6) == ("within visual range and can padlock, but blind (immediately below)", False, True, False)
assert A8.visualsightingrange    (A6) == 20
assert A8.visualsightingcondition(A6) == ("within visual range but restricted (60- arc)", True, True, True)
assert A9.visualsightingrange    (A6) == 20
assert A9.visualsightingcondition(A6) == ("within visual range", True, True, False)

assert A7.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A7) == 3
assert A1.visualsightingcondition(A7) == ("within visual range", True, True, False)
assert A2.visualsightingrange    (A7) == 5
assert A2.visualsightingcondition(A7) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A7) == 1
assert A3.visualsightingcondition(A7) == ("within visual range", True, True, False)
assert A4.visualsightingrange    (A7) == 0
assert A4.visualsightingcondition(A7) == ("within visual range (immediately above)", True, True, False)
assert A5.visualsightingrange    (A7) == 0
assert A5.visualsightingcondition(A7) == ("within visual range (immediately above)", True, True, False)
assert A6.visualsightingrange    (A7) == 0
assert A6.visualsightingcondition(A7) == ("within visual range (immediately above)", True, True, False)
assert A8.visualsightingrange    (A7) == 20
assert A8.visualsightingcondition(A7) == ("within visual range but restricted (60- arc)", True, True, True)
assert A9.visualsightingrange    (A7) == 20
assert A9.visualsightingcondition(A7) == ("within visual range", True, True, False)

assert A8.maxvisualsightingrange() == 20
assert A1.visualsightingrange    (A8) == 20
assert A1.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A2.visualsightingrange    (A8) == 19
assert A2.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A3.visualsightingrange    (A8) == 20
assert A3.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A4.visualsightingrange    (A8) == 20
assert A4.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A5.visualsightingrange    (A8) == 20
assert A5.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A6.visualsightingrange    (A8) == 20
assert A6.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A7.visualsightingrange    (A8) == 20
assert A7.visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A9.visualsightingrange    (A8) == 0
assert A9.visualsightingcondition(A8) == ("within visual range but blind (30- arc)", False, False, False)

assert A9.maxvisualsightingrange() == 16
assert A1.visualsightingrange    (A9) == 20
assert A1.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A2.visualsightingrange    (A9) == 19
assert A2.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A3.visualsightingrange    (A9) == 20
assert A3.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A4.visualsightingrange    (A9) == 20
assert A4.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A5.visualsightingrange    (A9) == 20
assert A5.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A6.visualsightingrange    (A9) == 20
assert A6.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A7.visualsightingrange    (A9) == 20
assert A7.visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A8.visualsightingrange    (A9) == 0
assert A8.visualsightingcondition(A9) == ("within visual range but blind (30- arc)", False, False, False)

endfile(__file__)
