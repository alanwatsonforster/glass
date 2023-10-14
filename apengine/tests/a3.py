from apengine.tests.infrastructure import *
startfile(__file__, "azimuths")

# Checks on apengine.azimuth.

# Conversion of numeric azimuths to symbolic directions.

startsetup()
A1 = aircraft("A1", "F-80C", 1115,   0, 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 1315,  90, 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C", 1515, 180, 10, 4.0, "CL")
A4 = aircraft("A4", "F-80C", 1715, 270, 10, 4.0, "CL")
endsetup()

A1._assert("1115       N    10", 4.0)
A2._assert("1315       E    10", 4.0)
A3._assert("1515       S    10", 4.0)
A4._assert("1715       W    10", 4.0)

# Check that ENE/ESE/WSW/WNW are accepted.

startsetup()
A1 = aircraft("A1", "F-80C", 1115, "ENE", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 1315, "ESE", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C", 1515, "WSW", 10, 4.0, "CL")
A4 = aircraft("A4", "F-80C", 1715, "WNW", 10, 4.0, "CL")
endsetup()

A1._assert("1115       ENE  10", 4.0)
A2._assert("1315       ESE  10", 4.0)
A3._assert("1515       WSW  10", 4.0)
A4._assert("1715       WNW  10", 4.0)

# Check that NE/SE/SW/NW are not accepted.

startsetup()
A1 = aircraft("A1", "F-80C", 1115, "NE", 10, 4.0, "CL")
asserterror("invalid azimuth 'NE'.")
A2 = aircraft("A2", "F-80C", 1315, "SE", 10, 4.0, "CL")
asserterror("invalid azimuth 'SE'.")
A3 = aircraft("A3", "F-80C", 1515, "SW", 10, 4.0, "CL")
asserterror("invalid azimuth 'SW'.")
A4 = aircraft("A4", "F-80C", 1715, "NW", 10, 4.0, "CL")
asserterror("invalid azimuth 'NW'.")
endsetup()

# Check that NE/SE/SW/NW are accepted but converted to ENE/ESE/WSW/WNW.

startsetup(variants=["allow NE/SE/SW/NW"])
A1 = aircraft("A1", "F-80C", 1115, "NE", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 1315, "SE", 10, 4.0, "CL")
A3 = aircraft("A3", "F-80C", 1515, "SW", 10, 4.0, "CL")
A4 = aircraft("A4", "F-80C", 1715, "NW", 10, 4.0, "CL")
endsetup()

A1._assert("1115       ENE  10", 4.0)
A2._assert("1315       ESE  10", 4.0)
A3._assert("1515       WSW  10", 4.0)
A4._assert("1715       WNW  10", 4.0)

# Check that NE/SE/SW/NW are accepted but not converted to ENE/ESE/WSW/WNW.

startsetup(variants=["allow NE/SE/SW/NW", "prefer NE/SE/SW/NW"])
A1 = aircraft("A1", "F-80C", 1115, "NE", 10, 4.0, "CL")
A2 = aircraft("A2", "F-80C", 1315, "SE", 10, 4.0, "CL")
A3 = aircraft("A2", "F-80C", 1515, "SW", 10, 4.0, "CL")
A4 = aircraft("A2", "F-80C", 1715, "NW", 10, 4.0, "CL")
endsetup()

A1._assert("1115       NE   10", 4.0)
A2._assert("1315       SE   10", 4.0)
A3._assert("1515       SW   10", 4.0)
A4._assert("1715       NW   10", 4.0)

# Check that only NE/SE/SW/NW are accepted.

startsetup(variants=["allow NE/SE/SW/NW", "disallow ENE/ESE/WSW/WNW"])
A1 = aircraft("A1", "F-80C", 1115, "ENE", 10, 4.0, "CL")
asserterror("invalid azimuth 'ENE'.")
A2 = aircraft("A2", "F-80C", 1315, "ESE", 10, 4.0, "CL")
asserterror("invalid azimuth 'ESE'.")
A3 = aircraft("A3", "F-80C", 1515, "WSW", 10, 4.0, "CL")
asserterror("invalid azimuth 'WSW'.")
A4 = aircraft("A4", "F-80C", 1715, "WNW", 10, 4.0, "CL")
asserterror("invalid azimuth 'WNW'.")
endsetup()

endfile(__file__)
