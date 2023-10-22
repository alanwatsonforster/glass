from apengine.tests.infrastructure import *
startfile(__file__, "aircraft creation")

# Checks on aircraft creation.

starttestsetup()
A1 = aircraft("A1", "F-80C" , "1115", "N"  , 10, 4.0, "CL")
A2 = aircraft("A2", "F-84E" , "1315", "NNE", 20, 4.5, "CL")
A3 = aircraft("A3", "F-84G" , "1515", "ENE", 30, 5.0, "1/2")
A4 = aircraft("A4", "F-100A", "1715", "NNW", 40, 5.5, "CL")
A5 = aircraft("A5", "F-104A", "1915", "WNW", 50, 6.0, "DT")
endtestsetup()

A1._assert("1115       N    10", 4.0, configuration="CL")
A2._assert("1315       NNE  20", 4.5, configuration="CL")
A3._assert("1515       ENE  30", 5.0, configuration="1/2")
A4._assert("1715       NNW  40", 5.5, configuration="CL")
A5._assert("1915       WNW  50", 6.0, configuration="DT")

endfile(__file__)
