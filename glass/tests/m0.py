from glass.tests.infrastructure import *

startfile(__file__, "visual sighting")

starttestsetup(sheets=[["A1", "B1"]])
A1 = setupaircraft("A1", "AF", "MiG-17F", "A1-2015", "N", 6, 4.0)
A2 = setupaircraft("A2", "AF", "F-86A", "A1-2215", "N", 9, 4.0)
A3 = setupaircraft("A3", "AF", "F-84E", "A1-2013", "N", 5, 3.5)
A4 = setupaircraft("A4", "AF", "F-84E", "A1-2012", "NNE", 6, 3.5)
A5 = setupaircraft("A5", "AF", "F-84E", "A1-2012", "NNE", 5, 3.5)
A6 = setupaircraft("A6", "AF", "F-84E", "A1-2012", "NNE", 6, 3.5)
A7 = setupaircraft("A7", "AF", "F-84E", "A1-2012", "NNE", 7, 3.5)
A8 = setupaircraft("A8", "AF", "F-84E", "B1-4012", "NNE", 7, 3.5)
A9 = setupaircraft("A9", "AF", "MiG-15bis", "B1-4012", "NNE", 7, 3.5)
endtestsetup()

startgameturn()

assert A1._maxvisualsightingrange() == 16
assert A2._visualsightingrange(A1) == 3
assert A2._visualsightingcondition(A1) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A1) == 2
assert A3._visualsightingcondition(A1) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A4._visualsightingrange(A1) == 3
assert A4._visualsightingcondition(A1) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A5._visualsightingrange(A1) == 3
assert A5._visualsightingcondition(A1) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A6._visualsightingrange(A1) == 3
assert A6._visualsightingcondition(A1) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A7._visualsightingrange(A1) == 3
assert A7._visualsightingcondition(A1) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A8._visualsightingrange(A1) == 20
assert A8._visualsightingcondition(A1) == ("beyond visual range", False, False, False)
assert A9._visualsightingrange(A1) == 20
assert A9._visualsightingcondition(A1) == ("beyond visual range", False, False, False)

assert A2._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A2) == 2
assert A1._visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A2) == 4
assert A3._visualsightingcondition(A2) == (
    "within visual range but restricted (60- arc)",
    True,
    True,
    True,
)
assert A4._visualsightingrange(A2) == 4
assert A4._visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A5._visualsightingrange(A2) == 5
assert A5._visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A6._visualsightingrange(A2) == 4
assert A6._visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A7._visualsightingrange(A2) == 4
assert A7._visualsightingcondition(A2) == ("within visual range", True, True, False)
assert A8._visualsightingrange(A2) == 18
assert A8._visualsightingcondition(A2) == (
    "within visual range but restricted (60- arc)",
    True,
    True,
    True,
)
assert A9._visualsightingrange(A2) == 18
assert A9._visualsightingcondition(A2) == ("within visual range", True, True, False)

assert A3._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A3) == 2
assert A1._visualsightingcondition(A3) == (
    "within visual range but restricted (180L arc)",
    True,
    True,
    True,
)
assert A2._visualsightingrange(A3) == 5
assert A2._visualsightingcondition(A3) == ("within visual range", True, True, False)
assert A4._visualsightingrange(A3) == 1
assert A4._visualsightingcondition(A3) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A5._visualsightingrange(A3) == 1
assert A5._visualsightingcondition(A3) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A6._visualsightingrange(A3) == 1
assert A6._visualsightingcondition(A3) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A7._visualsightingrange(A3) == 2
assert A7._visualsightingcondition(A3) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A8._visualsightingrange(A3) == 21
assert A8._visualsightingcondition(A3) == ("beyond visual range", False, False, False)
assert A9._visualsightingrange(A3) == 21
assert A9._visualsightingcondition(A3) == ("beyond visual range", False, False, False)

assert A4._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A4) == 3
assert A1._visualsightingcondition(A4) == ("within visual range", True, True, False)
assert A2._visualsightingrange(A4) == 5
assert A2._visualsightingcondition(A4) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A4) == 1
assert A3._visualsightingcondition(A4) == ("within visual range", True, True, False)
assert A5._visualsightingrange(A4) == 0
assert A5._visualsightingcondition(A4) == (
    "within visual range (immediately above)",
    True,
    True,
    False,
)
assert A6._visualsightingrange(A4) == 0
assert A6._visualsightingcondition(A4) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A7._visualsightingrange(A4) == 0
assert A7._visualsightingcondition(A4) == (
    "within visual range and can padlock, but blind (immediately below)",
    False,
    True,
    False,
)
assert A8._visualsightingrange(A4) == 20
assert A8._visualsightingcondition(A4) == (
    "within visual range but restricted (60- arc)",
    True,
    True,
    True,
)
assert A9._visualsightingrange(A4) == 20
assert A9._visualsightingcondition(A4) == ("within visual range", True, True, False)

assert A5._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A5) == 3
assert A1._visualsightingcondition(A5) == (
    "within visual range but restricted (180L arc)",
    True,
    True,
    True,
)
assert A2._visualsightingrange(A5) == 6
assert A2._visualsightingcondition(A5) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A5) == 1
assert A3._visualsightingcondition(A5) == ("within visual range", True, True, False)
assert A4._visualsightingrange(A5) == 0
assert A4._visualsightingcondition(A5) == (
    "within visual range and can padlock, but blind (immediately below)",
    False,
    True,
    False,
)
assert A6._visualsightingrange(A5) == 0
assert A6._visualsightingcondition(A5) == (
    "within visual range and can padlock, but blind (immediately below)",
    False,
    True,
    False,
)
assert A7._visualsightingrange(A5) == 1
assert A7._visualsightingcondition(A5) == (
    "within visual range and can padlock, but blind (immediately below)",
    False,
    True,
    False,
)
assert A8._visualsightingrange(A5) == 21
assert A8._visualsightingcondition(A5) == ("beyond visual range", False, False, False)
assert A9._visualsightingrange(A5) == 21
assert A9._visualsightingcondition(A5) == ("beyond visual range", False, False, False)

assert A6._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A6) == 3
assert A1._visualsightingcondition(A6) == ("within visual range", True, True, False)
assert A2._visualsightingrange(A6) == 5
assert A2._visualsightingcondition(A6) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A6) == 1
assert A3._visualsightingcondition(A6) == ("within visual range", True, True, False)
assert A4._visualsightingrange(A6) == 0
assert A4._visualsightingcondition(A6) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)
assert A5._visualsightingrange(A6) == 0
assert A5._visualsightingcondition(A6) == (
    "within visual range (immediately above)",
    True,
    True,
    False,
)
assert A7._visualsightingrange(A6) == 0
assert A7._visualsightingcondition(A6) == (
    "within visual range and can padlock, but blind (immediately below)",
    False,
    True,
    False,
)
assert A8._visualsightingrange(A6) == 20
assert A8._visualsightingcondition(A6) == (
    "within visual range but restricted (60- arc)",
    True,
    True,
    True,
)
assert A9._visualsightingrange(A6) == 20
assert A9._visualsightingcondition(A6) == ("within visual range", True, True, False)

assert A7._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A7) == 3
assert A1._visualsightingcondition(A7) == ("within visual range", True, True, False)
assert A2._visualsightingrange(A7) == 5
assert A2._visualsightingcondition(A7) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A7) == 1
assert A3._visualsightingcondition(A7) == ("within visual range", True, True, False)
assert A4._visualsightingrange(A7) == 0
assert A4._visualsightingcondition(A7) == (
    "within visual range (immediately above)",
    True,
    True,
    False,
)
assert A5._visualsightingrange(A7) == 0
assert A5._visualsightingcondition(A7) == (
    "within visual range (immediately above)",
    True,
    True,
    False,
)
assert A6._visualsightingrange(A7) == 0
assert A6._visualsightingcondition(A7) == (
    "within visual range (immediately above)",
    True,
    True,
    False,
)
assert A8._visualsightingrange(A7) == 20
assert A8._visualsightingcondition(A7) == (
    "within visual range but restricted (60- arc)",
    True,
    True,
    True,
)
assert A9._visualsightingrange(A7) == 20
assert A9._visualsightingcondition(A7) == ("within visual range", True, True, False)

assert A8._maxvisualsightingrange() == 20
assert A1._visualsightingrange(A8) == 20
assert A1._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A2._visualsightingrange(A8) == 19
assert A2._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A3._visualsightingrange(A8) == 20
assert A3._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A4._visualsightingrange(A8) == 20
assert A4._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A5._visualsightingrange(A8) == 20
assert A5._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A6._visualsightingrange(A8) == 20
assert A6._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A7._visualsightingrange(A8) == 20
assert A7._visualsightingcondition(A8) == ("within visual range", True, True, False)
assert A9._visualsightingrange(A8) == 0
assert A9._visualsightingcondition(A8) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)

assert A9._maxvisualsightingrange() == 16
assert A1._visualsightingrange(A9) == 20
assert A1._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A2._visualsightingrange(A9) == 19
assert A2._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A3._visualsightingrange(A9) == 20
assert A3._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A4._visualsightingrange(A9) == 20
assert A4._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A5._visualsightingrange(A9) == 20
assert A5._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A6._visualsightingrange(A9) == 20
assert A6._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A7._visualsightingrange(A9) == 20
assert A7._visualsightingcondition(A9) == ("beyond visual range", False, False, False)
assert A8._visualsightingrange(A9) == 0
assert A8._visualsightingcondition(A9) == (
    "within visual range but blind (30- arc)",
    False,
    False,
    False,
)

endfile(__file__)
