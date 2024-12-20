from apxo.tests.infrastructure import *

startfile(__file__, "ground units")

starttestsetup()

x = 13
y = 3
for s in [
    "infantry",
    "armor",
    "artillery",
    "reconnaissance",
    "airdefense",
    "supply",
    "transportation",
    "ammunition",
    "fuel",
    "ordnance",
    "headquarter",
    "light",
    "medium",
    "heavy",
    "missile",
    "gun",
    "multiplerocket",
    "radar",
    "motorized",
    "wheeled",
    "limitedwheeled",
    "locomotive",
    "railcar",
    "barge",
    "truck",
]:
    hexcode = "A1-%02d%02d" % (x, y)
    groundunit(s, hexcode, s)
    y += 1
    if y == 8:
        x += 1
        y = 3

x = 21
y = 3
for s in [
    "infantry/armor",
    "infantry/armor/gun",
    "infantry/armor/wheeled",
    "infantry/light",
    "armor/medium/gun",
    "artillery/gun",
    "artillery/armor/gun",
    "artillery/multiplerocket/limitedwheeled",
    "airdefense/gun/light",
    "airdefense/missile",
    "airdefense/radar",
    "airdefense/gun/armor/medium",
    "airdefense/missile/wheeled",
    "airdefense/missile/armor",
    "airdefense/headquarter",
]:
    hexcode = "A1-%02d%02d" % (x, y)
    groundunit(s, hexcode, s, color="lightgreen")
    y += 1
    if y == 8:
        x += 1
        y = 3


x = 27
y = 3
for c in [
    "white",
    "natoblue",
    "natored",
    "natogreen",
    "natoyellow",
    "green",
    "lightgreen",
    "tan",
    "darktan",
    "sand",
]:
    hexcode = "A1-%02d%02d" % (x, y)
    groundunit(c, hexcode, "infantry", color=c)
    y += 1
    if y == 8:
        x += 1
        y = 3

endtestsetup()

starttestsetup()

groundunit("invalid", "A1-2110", "foo")
asserterror('invalid ground unit symbol "foo".')

groundunit(1, "A1-2110", "infantry")
asserterror('the name argument must be a string.')

groundunit("A", "A1-2110", "infantry")
groundunit("A", "A1-2110", "infantry")
asserterror('the name argument must be unique.')


endtestsetup()

# Damage
starttestsetup()

A0 = groundunit("A0", "A1-2110", "infantry")
A1 = groundunit("A1", "A1-2110", "infantry")
A2 = groundunit("A2", "A1-2110", "infantry")
assert A0.damage() == ""
assert A1.damage() == ""
assert A2.damage() == ""
A0.takedamage("D")
A1.takedamage("2D")
A2.takedamage("K")
assert A0.damage() == "D+S"
assert A1.damage() == "2D+S"
assert A2.damage() == "K"
A0.takedamage("D")
A1.takedamage("D")
A2.takedamage("D")
assert A0.damage() == "2D+S"
assert A1.damage() == "K"
assert A2.damage() == "K"
A0.takedamage("2D")
A1.takedamage("2D")
A2.takedamage("2D")
assert A0.damage() == "K"
assert A1.damage() == "K"
assert A2.damage() == "K"

endtestsetup()

# Barrage Fire

starttestsetup()

A0 = groundunit("A0", "A1-2110", "infantry" , barragefirealtitude=2)
A1 = groundunit("A1", "A1-2110", "infantry" , barragefirealtitude=2)
A2 = groundunit("A2", "A1-2110", "armor"    , barragefirealtitude=3)
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
