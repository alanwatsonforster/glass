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
    "headquarters",
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
    setupgroundunit(s, hexcode, s, color="lightgreen")
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
    "infantry",
    "armor/gun",
    "artillery/gun",
    "artillery/armor/gun",
    "artillery/multiplerocket/limitedwheeled",
    "airdefense/gun",
    "airdefense/missile",
    "airdefense/radar",
    "airdefense/gun/armor",
    "airdefense/missile/wheeled",
    "airdefense/missile/armor",
    "airdefense/headquarters",
]:
    hexcode = "A1-%02d%02d" % (x, y)
    setupgroundunit(s, hexcode, s, color="lightgreen")
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
    setupgroundunit(c, hexcode, "infantry", color=c)
    y += 1
    if y == 8:
        x += 1
        y = 3

# Check stacks

x = 7
y = 9
hexcode = "A1-%02d%02d" % (x, y)
setupgroundunit("1/1", hexcode, "infantry", stack="1/1", color="lightgreen")
y += 1
hexcode = "A1-%02d%02d" % (x, y)
setupgroundunit("1/2", hexcode, "infantry", stack="1/2", color="lightgreen")
setupgroundunit("2/2", hexcode, "infantry", stack="2/2", color="lightgreen")
x += 1
y -= 1
hexcode = "A1-%02d%02d" % (x, y)
setupgroundunit("1/3", hexcode, "infantry", stack="1/3", color="lightgreen")
setupgroundunit("2/3", hexcode, "infantry", stack="2/3", color="lightgreen")
setupgroundunit("3/3", hexcode, "infantry", stack="3/3", color="lightgreen")
y += 1
hexcode = "A1-%02d%02d" % (x, y)
setupgroundunit("1/4", hexcode, "infantry", stack="1/4", color="lightgreen")
setupgroundunit("2/4", hexcode, "infantry", stack="2/4", color="lightgreen")
setupgroundunit("3/4", hexcode, "infantry", stack="3/4", color="lightgreen")
setupgroundunit("4/4", hexcode, "infantry", stack="4/4", color="lightgreen")

endtestsetup()

# Check errors

starttestsetup()

setupgroundunit("invalid", "A1-2110", symbols="foo")
asserterror('invalid ground unit symbol "foo".')

setupgroundunit(1, "A1-2110", symbols="infantry")
asserterror("the name argument must be a string.")

setupgroundunit("A", "A1-2110", symbols="infantry")
setupgroundunit("A", "A1-2110", symbols="infantry")
asserterror("the name argument must be unique.")

# Check types

starttestsetup()

G0 = setupgroundunit("G0", "A1-2110", "infantry")
assert G0.isgroundunit()
G1 = setupgroundunit("G1", "A1-2110", "ZPU-1")
assert G1.isgroundunit()

setupgroundunit("missing", "A1-2110", "_MISSING")
asserterror('unable to find ground unit data file for "_MISSING".')

setupgroundunit("invalid", "A1-2110", "_INVALID")
asserterror(
    'unable to read ground unit data file for "_INVALID": line 2: expecting property name enclosed in double quotes.'
)

# Check azimuths

starttestsetup()
G0 = setupgroundunit("G0", "A1-2110", symbols="", aaaclass="H", azimuth="N")
G0._assert("A1-2110 N 0", None)

starttestsetup()
G0 = setupgroundunit("G0", "A1-2110", symbols="", azimuth="N")
asserterror("only heavy AAA ground units may have an azimuth.")

starttestsetup()
G0 = setupgroundunit("G0", "A1-2110", symbols="", aaaclass="H")
asserterror("heavy AAA ground units must have an azimuth.")

# Make sure all of the ground unit data files are readable.

import glob
import os.path

starttestsetup()

pathlist = sorted(list(glob.glob("apxo/groundunitdata/*.json")))
i = 0
for path in pathlist:
    groundunittype = os.path.basename(path)[:-5]
    if groundunittype[0] != "_":
        if groundunittype == "KS-12":
            setupgroundunit("G%d" % i, "A1-2110", groundunittype, azimuth="N")
        else:
            setupgroundunit("G%d" % i, "A1-2110", groundunittype)
        asserterror(None)
        i += 1


endfile(__file__)
