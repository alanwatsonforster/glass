from apxo.tests.infrastructure import *

startfile(__file__, "aircraft data")

# Checks on apxo.aircraftdata.

from apxo.aircraftdata import aircraftdata
import apxo.variants

# Make sure all of the aircraft data files are readable.

import glob
import os.path

pathlist = sorted(list(glob.glob("apxo/aircraftdata/*.json")))
for path in pathlist:
    aircrafttype = os.path.basename(path)[:-5]
    if aircrafttype != "_TEMPLATE":
        str(aircraftdata(aircrafttype))

# Check the basic functionallity using the F-104A as a test case.

d = aircraftdata("F-104A")
assert d.power("CL", "AB") == 3.5
assert d.powerfade(6.0, 20) == None
assert d.speedbrake("DT") == 2.0
assert d.fuelrate("M") == 2.0
assert d.engines() == 1
assert d.lowspeedliftdevicelimit() == None
assert d.turndrag("CL", "BT") == 4.0
assert d.turndrag("CL", "ET") == None
assert d.turndrag("DT", "BT") == None
assert d.minspeed("1/2", "VH") == 4.5
assert d.maxspeed("1/2", "VH") == 11.0
assert d.minspeed("DT", "EH") == None
assert d.maxspeed("DT", "EH") == None
assert d.maxdivespeed("LO") == 9.0
assert d.ceiling("1/2") == 52
assert d.cruisespeed("CL") == 6.0
assert d.cruisespeed("1/2") == 5.5
assert d.cruisespeed("DT") == 5.0

assert d.climbspeed() == 4.5
assert d.rollhfp() == 1.0
assert d.rolldrag("LR") == 1.0
assert d.rolldrag("DR") == 1.0
assert d.rolldrag("VR") == 0.0
assert d.climbcapability("CL", "ML", "AB") == 7.0
assert d.climbcapability("DT", "EH", "M") == None
assert d.hasproperty("LTD") == True
assert d.hasproperty("RA") == True
assert d.hasproperty("GSSM") == True
assert d.hasproperty("RPR") == True
assert d.hasproperty("HPR") == False

# Check slatted wings using the F-100A as a test case.

d = aircraftdata("F-100A")
assert d.turndrag("CL", "BT", lowspeedliftdevice=True) == 3.0
assert d.turndrag("CL", "BT") == 2.0
assert d.lowspeedliftdevicelimit() == 3.5

# Check power fade with speed using the Sea Fury as an test case.

d = aircraftdata("Sea Fury FB.11")

assert d.powerfade(3.0, 0) == 0.0
assert d.powerfade(3.5, 0) == 0.5
assert d.powerfade(4.0, 0) == 0.5
assert d.powerfade(4.5, 0) == 1.0

assert d.powerfade(3.0, 30) == 0.0
assert d.powerfade(3.5, 30) == 0.5
assert d.powerfade(4.0, 30) == 0.5
assert d.powerfade(4.5, 30) == 1.0

# Check power fade with altitude using the AU-1 as a test case.

d = aircraftdata("AU-1")

assert d.powerfade(3.0, 16) == 0.0
assert d.powerfade(3.5, 16) == 0.5
assert d.powerfade(4.0, 16) == 0.5
assert d.powerfade(4.5, 16) == 1.0

assert d.powerfade(3.0, 17) == 0.5
assert d.powerfade(3.5, 17) == 1.0
assert d.powerfade(4.0, 17) == 1.0
assert d.powerfade(4.5, 17) == 1.5

endfile(__file__)
