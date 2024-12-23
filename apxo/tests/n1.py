from apxo.tests.infrastructure import *

startfile(__file__, "missile speed")

# LO altitude band

starttestsetup()
starttestsetup()
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    3.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A2 = aircraft(
    "A2",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    4.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A3 = aircraft(
    "A3",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    5.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A4 = aircraft(
    "A4",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A5 = aircraft(
    "A5",
    "AF",
    "F-16A-10",
    "A2-2010",
    "N",
    5,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
endtestsetup()

startgameturn()

A1.move("LVL", "N", "H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

A1a = A1.airtoairlaunch("A1a", A5, "9")
A2a = A2.airtoairlaunch("A2a", A5, "9")
A3a = A3.airtoairlaunch("A3a", A5, "9")
A4a = A4.airtoairlaunch("A4a", A5, "9")

assert A1a.ismissile()
assert A2a.ismissile()
assert A3a.ismissile()
assert A4a.ismissile()

assert A1a.speed() == 17.0
assert A2a.speed() == 18.0
assert A3a.speed() == 19.0
assert A4a.speed() == 20.0

endgameturn()

startgameturn()

A1a.move("")
A2a.move("")
A3a.move("")
A4a.move("")

assert A1a.speed() == 10.0
assert A2a.speed() == 11.0
assert A3a.speed() == 11.0
assert A4a.speed() == 12.0

A1a.continuemove("H,H,H,H,H,H,H,H,H,H")
A2a.continuemove("H,H,H,H,H,H,H,H,H,H,H")
A3a.continuemove("H,H,H,H,H,H,H,H,H,H,H")
A4a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H")

A1.move("LVL", "N", "H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

endgameturn()

startgameturn()

A1a.move("")
A2a.move("")
A3a.move("")
A4a.move("")

assert A1a.speed() == 6.0
assert A2a.speed() == 7.0
assert A3a.speed() == 7.0
assert A4a.speed() == 7.0

A1a.continuemove("H,H,H,H,H,H")
A2a.continuemove("H,H,H,H,H,H,H")
A3a.continuemove("H,H,H,H,H,H,H")
A4a.continuemove("H,H,H,H,H,H,H")

A1.move("LVL", "N", "H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

endgameturn()

startgameturn()

A1a.move("")
A2a.move("")
A3a.move("")
A4a.move("")

assert A1a.speed() == 4.0
assert A2a.speed() == 5.0
assert A3a.speed() == 5.0
assert A4a.speed() == 5.0

A1a.continuemove("H,H,H,H")
A2a.continuemove("H,H,H,H,H")
A3a.continuemove("H,H,H,H,H")
A4a.continuemove("H,H,H,H,H")

A1.move("LVL", "N", "H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

endgameturn()

# EH altitude band

starttestsetup(verbose=False)
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    60,
    3.5,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A2 = aircraft(
    "A2",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    60,
    4.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A3 = aircraft(
    "A3",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    60,
    5.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A4 = aircraft(
    "A4",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    60,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A5 = aircraft(
    "A5",
    "AF",
    "F-16A-10",
    "A2-2010",
    "N",
    60,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
endtestsetup()

startgameturn()

A1.move("LVL", "N", "H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

A1a = A1.airtoairlaunch("A1a", A5, "9")
A2a = A2.airtoairlaunch("A2a", A5, "9")
A3a = A3.airtoairlaunch("A3a", A5, "9")
A4a = A4.airtoairlaunch("A4a", A5, "9")

assert A1a.ismissile()
assert A2a.ismissile()
assert A3a.ismissile()
assert A4a.ismissile()

assert A1a.speed() == 17.5
assert A2a.speed() == 18.0
assert A3a.speed() == 19.0
assert A4a.speed() == 20.0

endgameturn()

startgameturn()

A1a.move("")
A2a.move("")
A3a.move("")
A4a.move("")

assert A1a.speed() == 16.0
assert A2a.speed() == 16.0
assert A3a.speed() == 17.0
assert A4a.speed() == 18.0

A1a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A2a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A3a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A4a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H")

A1.move("LVL", "N", "H,H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

endgameturn()

startgameturn()

A1a.move("")
A2a.move("")
A3a.move("")
A4a.move("")

assert A1a.speed() == 14.0
assert A2a.speed() == 14.0
assert A3a.speed() == 15.0
assert A4a.speed() == 16.0

A1a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A2a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A3a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A4a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H,H,H")

A1.move("LVL", "N", "H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

endgameturn()

startgameturn()

A1a.move("")
A2a.move("")
A3a.move("")
A4a.move("")

assert A1a.speed() == 13.0
assert A2a.speed() == 13.0
assert A3a.speed() == 14.0
assert A4a.speed() == 14.0

A1a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H")
A2a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H")
A3a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A4a.continuemove("H,H,H,H,H,H,H,H,H,H,H,H,H,H")

A1.move("LVL", "N", "H,H,H,H")
A2.move("LVL", "N", "H,H,H,H")
A3.move("LVL", "N", "H,H,H,H,H")
A4.move("LVL", "N", "H,H,H,H,H,H")
A5.move("LVL", "N", "H,H,H,H,H,H")

endgameturn()

starttestsetup(verbose=False)
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    8.0,
    stores={"1": "IRM/AIM-9P", "9": "IRM/AIM-9P"},
)
A2 = aircraft("A2", "AF", "F-16A-10", "A2-2010", "N", 5, 8.0)
endtestsetup()

startgameturn()

A1.move("LVL", "AB", "H,H,H,H,H,H,H,H")
A2.move("LVL", "AB", "H,H,H,H,H,H,H,H")

A1a = A1.airtoairlaunch("A1a", A2, "1")
# Speed would be 26, but is limited by the maximum speed.
assert A1a.speed() == 24.0

endgameturn()

starttestsetup(verbose=False)
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    60,
    14.0,
    stores={"1": "IRM/AIM-9P", "9": "IRM/AIM-9P"},
)
A2 = aircraft("A2", "AF", "F-16A-10", "A2-2010", "N", 60, 14.0)
endtestsetup()

startgameturn()

A1.move("LVL", "AB", "H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A2.move("LVL", "AB", "H,H,H,H,H,H,H,H,H,H,H,H,H,H")

A1a = A1.airtoairlaunch("A1a", A2, "1")
assert A1a.speed() == 30.0

endgameturn()

starttestsetup(verbose=False)
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    8.0,
    stores={"1": "IRM/AIM-9P", "9": "IRM/AIM-9P"},
)
A2 = aircraft("A2", "AF", "F-16A-10", "A2-2010", "N", 5, 8.0)
endtestsetup()

startgameturn()

A1.move("LVL", "AB", "H,H,H,H,H,H,H,H")
A2.move("LVL", "AB", "H,H,H,H,H,H,H,H")

A1a = A1.airtoairlaunch("A1a", A2, "1")
# Speed would be 26, but is limited by the maximum speed.
assert A1a.speed() == 24.0

endgameturn()

starttestsetup(verbose=False)
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2015",
    "N",
    5,
    1.0,
    stores={"1": "IRM/AIM-9B", "9": "IRM/AIM-9B"},
)
A2 = aircraft("A2", "AF", "F-16A-10", "A2-2010", "N", 5, 1.0)
endtestsetup()

startgameturn()
A1.move("LVL", "N", "H")
A2.move("LVL", "N", "H")
A1a = A1.airtoairlaunch("A1a", A2, "1")
assert A1a.speed() == 11.0
endgameturn()

startgameturn()
# We have to fudge this.
A1a._setspeed(1.0)
assert A1a.speed() == 1.0
A1a.move("H")
asserterror("invalid move 'H' for stalled missile.")

startgameturn()
# We have to fudge this.
A1a._setspeed(1.0)
assert A1a.speed() == 1.0
A1a.move("")
A1.move("LVL", "N", "H")
A2.move("LVL", "N", "H")
endgameturn()

# Test speed loss from turning and altitude.

starttestsetup()
A1 = aircraft(
    "A1",
    "AF",
    "F-16A-10",
    "A2-2030",
    "N",
    10,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
A2 = aircraft(
    "A2",
    "AF",
    "F-16A-10",
    "A2-2020",
    "N",
    10,
    6.0,
    stores={"1": "IRM/AIM-9L", "9": "IRM/AIM-9L"},
)
endtestsetup()

startgameturn()
A1.move("LVL", "N", "H,H,H,H,H,H")
A2.move("LVL", "N", "H,H,H,H,H,H")
A1a = A1.airtoairlaunch("A1a", A2, "1")
endgameturn()

startgameturn()
A1a.move("H,H,H,H,H,H,H,H,H,H,H,H,H,H")
A1a._assert("A1-2010       N    10", 14.0)

startgameturn()
A1a.move("TR/H,H/R,TR/H,H/R,TR/H,H/R,TR/H,H/R,TR/H,H/R,TR/H,H/R,TR/H,H/R")
A1a._assert("A2-2824       SSW  10", 7.0)


startgameturn()
A1a.move("C,C,C,C,C,C,C,C,C,C,C,C,C,C")
A1a._assert("A2-2024       N    24", 12.0)


endfile(__file__)
