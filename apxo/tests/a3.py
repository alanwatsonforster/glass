from apxo.tests.infrastructure import *

startfile(__file__, "azimuths")

# Checks on apxo.azimuth.

# Conversion of numeric azimuths to symbolic directions.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", 0, 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", 90, 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", 180, 10, 4.0, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", 270, 10, 4.0, "CL")
endtestsetup()

A1._assert("A1-1115       N    10", 4.0)
A2._assert("A1-1315       E    10", 4.0)
A3._assert("A1-1515       S    10", 4.0)
A4._assert("A1-1715       W    10", 4.0)

# Check that ENE/ESE/WSW/WNW are accepted.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "ENE", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", "ESE", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", "WSW", 10, 4.0, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", "WNW", 10, 4.0, "CL")
endtestsetup()

A1._assert("A1-1115       ENE  10", 4.0)
A2._assert("A1-1315       ESE  10", 4.0)
A3._assert("A1-1515       WSW  10", 4.0)
A4._assert("A1-1715       WNW  10", 4.0)

# Check that NE/SE/SW/NW are accepted but converted to ENE/ESE/WSW/WNW.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "NE", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", "SE", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", "SW", 10, 4.0, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", "NW", 10, 4.0, "CL")
endtestsetup()

A1._assert("A1-1115       ENE  10", 4.0)
A2._assert("A1-1315       ESE  10", 4.0)
A3._assert("A1-1515       WSW  10", 4.0)
A4._assert("A1-1715       WNW  10", 4.0)

# Check that NE/SE/SW/NW are not accepted.

starttestsetup(variants=["disallow NE/SE/SW/NW"])
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "NE", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", "SE", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", "SW", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", "NW", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
endtestsetup()

# Check that NE/SE/SW/NW are accepted but not converted to ENE/ESE/WSW/WNW.

starttestsetup(variants=["prefer NE/SE/SW/NW"])
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "NE", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", "SE", 10, 4.0, "CL")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", "SW", 10, 4.0, "CL")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", "NW", 10, 4.0, "CL")
endtestsetup()

A1._assert("A1-1115       NE   10", 4.0)
A2._assert("A1-1315       SE   10", 4.0)
A3._assert("A1-1515       SW   10", 4.0)
A4._assert("A1-1715       NW   10", 4.0)

# Check that only NE/SE/SW/NW are accepted.

starttestsetup(variants=["disallow ENE/ESE/WSW/WNW"])
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "ENE", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
A2 = aircraft("A2", "AF", "F-80C", "A1-1315", "ESE", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
A3 = aircraft("A3", "AF", "F-80C", "A1-1515", "WSW", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
A4 = aircraft("A4", "AF", "F-80C", "A1-1715", "WNW", 10, 4.0, "CL")
asserterror("the azimuth argument is not valid.")
endtestsetup()

endfile(__file__)
