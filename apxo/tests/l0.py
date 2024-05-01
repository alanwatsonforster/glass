from apxo.tests.infrastructure import *

startfile(__file__, "fuel")

starttestsetup()
A1 = aircraft("A1", "AF", "F-104A", "A2-2025", "N", 5, 5.0, "CL", fuel=100)
endtestsetup()

startturn()
A1.move("LVL", "AB", "H,H,H,H,H")
assert A1._fuel == 95
startturn()
A1.move("LVL", "M", "H,H,H,H,H")
assert A1._fuel == 98
startturn()
A1.move("LVL", "N", "H,H,H,H,H")
assert A1._fuel == 99
startturn()
A1.move("LVL", "I", "H,H,H,H")
assert A1._fuel == 100

starttestsetup()
A1 = aircraft("A1", "AF", "Meteor F.8", "A2-2025", "N", 5, 5.0, "CL", fuel=100)
endtestsetup()

startturn()
A1.move("LVL", "M", "H,H,H,H,H")
assert A1._fuel == 99
startturn()
A1.move("LVL", "M", "H,H,H,H,H", flamedoutengines=1)
assert A1._fuel == 99.5
startturn()
A1.move("LVL", "M", "H,H,H,H,H", flamedoutengines=2)
assert A1._fuel == 100
startturn()
A1.move("LVL", "N", "H,H,H,H,H", flamedoutengines=1)
assert A1._fuel == 99.75
startturn()
A1.move("LVL", "N", "H,H,H,H,H", flamedoutengines=2)
assert A1._fuel == 100

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A2-2025", "N", 5, 5.0, "CL", fuel="100%")
endtestsetup()
assert A1._fuel == 135

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A2-2025", "N", 5, 5.0, "CL", fuel="50%")
endtestsetup()
assert A1._fuel == 67.5

endfile(__file__)
