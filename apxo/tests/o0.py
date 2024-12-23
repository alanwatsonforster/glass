from apxo.tests.infrastructure import *

startfile(__file__, "ground unit creation")

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

groundunit("invalid", "A1-2110", symbols="foo")
asserterror('invalid ground unit symbol "foo".')

groundunit(1, "A1-2110", symbols="infantry")
asserterror("the name argument must be a string.")

groundunit("A", "A1-2110", symbols="infantry")
groundunit("A", "A1-2110", symbols="infantry")
asserterror("the name argument must be unique.")

starttestsetup()

G0 = groundunit("G0", "A1-2110", "infantry")
assert G0.isgroundunit()
G1 = groundunit("G1", "A1-2110", "ZPU-1")
assert G1.isgroundunit()

groundunit("invalid", "A1-2110", "foo")
asserterror('invalid ground unit type "foo".')

endfile(__file__)
