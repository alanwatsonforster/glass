from apxo.tests.infrastructure import *

startfile(__file__, "missile launches")

starttestsetup(verbose=False)
A1 = setupaircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A1-2015",
    "N",
    5,
    3.0,
    stores={
        "1": "IRM/AIM-9L",
        "2": "IRM/AIM-9L",
        "5": "FT/600L",
        "8": "IRM/AIM-9L",
        "9": "IRM/AIM-9L",
    },
)
A2 = setupaircraft("A2", "AF", "F-16A-10", "A1-2010", "N", 5, 6.0)
endtestsetup()

startgameturn()

A1a = A1.airtoairlaunch("A1a", A2, "1")
asserterror("launcher has not finished moving.")

A1.move("LVL", "N", "H,H,H")

A1a = A1.airtoairlaunch("A1a", A2, "1")
asserterror("target has not finished moving.")

A2.move("LVL", "N", "H,H,H,H,H,H")

A1a = A1.airtoairlaunch("A1a", A2, "1", failedbeforelaunch=True)
assert A1a == None

A1a = A1.airtoairlaunch("A1a", A2, "1", failed=True)
assert A1a == None

A1a = A1.airtoairlaunch("A1a", A2, "9")
assert A1a.ismissile()

A1a = A1.airtoairlaunch("A1a", A2, "9")
asserterror("load station 9 is not loaded.")

A1b = A1.airtoairlaunch("A1b", A2, "5")
asserterror("load station 5 is not loaded with an air-to-air missile.")

A1a = A1.airtoairlaunch(1, A2, "8")
asserterror("the name argument must be a string.")

A1a = A1.airtoairlaunch("A1a", A2, "2")
asserterror("the name argument must be unique.")

endfile(__file__)
