from apxo.tests.infrastructure import *

startfile(__file__, "ground unit barrage fire")

starttestsetup()

A0 = groundunit("A0", "A1-2110", "infantry", barragefirealtitude=2)
A1 = groundunit("A1", "A1-2110", "infantry", barragefirealtitude=2)
A2 = groundunit("A2", "A1-2110", "armor", barragefirealtitude=3)
A3 = groundunit("A3", "A1-2110", "artillery")

endtestsetup()

startgameturn()

assert A0._barragefiremarker is None
assert A1._barragefiremarker is None
assert A2._barragefiremarker is None
assert A3._barragefiremarker is None

A0.usebarragefire()
assert A0._barragefiremarker is not None

A0.takedamage("S")
assert A0._barragefiremarker is None

A1.takedamage("S")
A1.usebarragefire()
asserterror("A1 is suppressed.")

A2.usebarragefire()
assert A2._barragefiremarker is not None

A3.usebarragefire()
asserterror("A3 is not capable of barrage fire.")

assert A0._barragefiremarker is None
assert A1._barragefiremarker is None
assert A2._barragefiremarker is not None
assert A3._barragefiremarker is None


endgameturn()

assert A0._barragefiremarker is None
assert A1._barragefiremarker is None
assert A2._barragefiremarker is None
assert A3._barragefiremarker is None


endfile(__file__)
