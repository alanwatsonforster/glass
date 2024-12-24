from apxo.tests.infrastructure import *

startfile(__file__, "ground unit creation")

starttestsetup()

# Check symbols

x = 3
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
    groundunit(s, hexcode, s, color="lightgreen")
    y += 1
    if y == 12:
        x += 1
        y = 3

# Check combinations

x = 10
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
    if y == 12:
        x += 1
        y = 3


# Check colors

x = 7
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

# Check stacks

x = 7
y = 9
hexcode = "A1-%02d%02d" % (x, y)
groundunit("1/1", hexcode, "infantry", stack="1/1", color="lightgreen")
y += 1
hexcode = "A1-%02d%02d" % (x, y)
groundunit("1/2", hexcode, "infantry", stack="1/2", color="lightgreen")
groundunit("2/2", hexcode, "infantry", stack="2/2", color="lightgreen")
x += 1
y -= 1
hexcode = "A1-%02d%02d" % (x, y)
groundunit("1/3", hexcode, "infantry", stack="1/3", color="lightgreen")
groundunit("2/3", hexcode, "infantry", stack="2/3", color="lightgreen")
groundunit("3/3", hexcode, "infantry", stack="3/3", color="lightgreen")
y += 1
hexcode = "A1-%02d%02d" % (x, y)
groundunit("1/4", hexcode, "infantry", stack="1/4", color="lightgreen")
groundunit("2/4", hexcode, "infantry", stack="2/4", color="lightgreen")
groundunit("3/4", hexcode, "infantry", stack="3/4", color="lightgreen")
groundunit("4/4", hexcode, "infantry", stack="4/4", color="lightgreen")

endtestsetup()

# Check errors

starttestsetup()

groundunit("invalid", "A1-2110", symbols="foo")
asserterror('invalid ground unit symbol "foo".')

groundunit(1, "A1-2110", symbols="infantry")
asserterror("the name argument must be a string.")

groundunit("A", "A1-2110", symbols="infantry")
groundunit("A", "A1-2110", symbols="infantry")
asserterror("the name argument must be unique.")

# Check types

starttestsetup()

G0 = groundunit("G0", "A1-2110", "infantry")
assert G0.isgroundunit()
G1 = groundunit("G1", "A1-2110", "ZPU-1")
assert G1.isgroundunit()

groundunit("missing", "A1-2110", "_MISSING")
asserterror('unable to find ground unit data file for "_MISSING".')

groundunit("invalid", "A1-2110", "_INVALID")
asserterror(
    'unable to read ground unit data file for "_INVALID": line 2: expecting property name enclosed in double quotes.'
)

# Make sure all of the ground unit data files are readable.

import glob
import os.path

starttestsetup()

pathlist = sorted(list(glob.glob("apxo/groundunitdata/*.json")))
i = 0
for path in pathlist:
    groundunittype = os.path.basename(path)[:-5]
    if groundunittype[0] != "_":
        groundunit("G%d" % i, "A1-2110", groundunittype)
        asserterror(None)
        i += 1


endfile(__file__)
