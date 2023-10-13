from airpower.tests.infrastructure import *
startfile(__file__, "aircraft data")

# Checks on airpower.aircraftdata.

from airpower.aircraftdata import aircraftdata

# Make sure all of the aircraft data files are readable.

aircraftdata("A-3")
aircraftdata("AD-4")
aircraftdata("AT-33")
aircraftdata("B-26B")
aircraftdata("B-26C")
aircraftdata("B-66")
aircraftdata("EA-3")
aircraftdata("F-100A")
aircraftdata("F-100C")
aircraftdata("F-100D")
aircraftdata("F-100F")
aircraftdata("F-102A")
aircraftdata("F-104A")
aircraftdata("F-5A")
aircraftdata("F-5C")
aircraftdata("F-80C")
aircraftdata("F-84E")
aircraftdata("F-84G")
aircraftdata("F7U-3")
aircraftdata("F7U-3M")
aircraftdata("Meteor F.8")
aircraftdata("Meteor FR.9")
aircraftdata("MiG-15bis")
aircraftdata("MiG-15ISh")
aircraftdata("MiG-15P")
aircraftdata("RB-66")
aircraftdata("RF-5A")
aircraftdata("RF-80C")
aircraftdata("Sea Fury FB.11")
aircraftdata("Yak-9D")

# Check the basic functionallity using the F-104A as a test case.

d = aircraftdata("F-104A")
assert d.power("CL", "AB") == 3.5
assert d.powerfade(6.0) == None
assert d.spbr("DT") == 1.0
assert d.fuelrate("M") == 2.0
assert d.engines() == 1
assert d.lowspeedturnlimit() == None
assert d.turndrag("CL", "BT") == 4.0
assert d.turndrag("CL", "ET") == None
assert d.turndrag("DT", "BT") == None
assert d.minspeed("1/2", "VH") == 4.5
assert d.maxspeed("1/2", "VH") == 11.0
assert d.minspeed("DT", "EH") == None
assert d.maxspeed("DT", "EH") == None
assert d.maxdivespeed("LO") == 9.0
assert d.ceiling("1/2") == 52
assert d.cruisespeed() == 6.0
assert d.climbspeed() == 4.5
assert d.rollhfp() == 1.0
assert d.rolldrag("LR") == 1.0
assert d.rolldrag("DR") == 1.0
assert d.rolldrag("VR") == 0.0
assert d.climbcapability("CL", "ML", "AB") == 7.0
assert d.climbcapability("DT", "EH", "M") == None
assert d.hasproperty("LTD") == True
assert d.hasproperty("RAA") == True
assert d.hasproperty("GSSM") == True
assert d.hasproperty("RPR") == True
assert d.hasproperty("HPR") == False

# Check slatted wings using the F-100A as a test case.

d = aircraftdata("F-100A")
assert d.turndrag("CL", "BT", lowspeed=True) == 3.0
assert d.turndrag("CL", "BT", highspeed=True) == 2.0
assert d.lowspeedturnlimit() == 4.0

endfile(__file__)
