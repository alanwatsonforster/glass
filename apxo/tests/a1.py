from apxo.tests.infrastructure import *

startfile(__file__, "aircraft creation")

# Checks on aircraft creation.

starttestsetup()
A1 = aircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 4.0, "CL")
A2 = aircraft("A2", "AF", "F-84E", "A1-1315", "NNE", 20, 4.5, "CL")
A3 = aircraft("A3", "AF", "F-84G", "A1-1515", "ENE", 30, 5.0, "1/2")
A4 = aircraft("A4", "AF", "F-100A", "A1-1715", "NNW", 40, 5.5, "CL")
A5 = aircraft("A5", "AF", "F-104A", "A1-1915", "WNW", 50, 6.0, "DT")
endtestsetup()

A1._assert("A1-1115           N    10", 4.0, expectedconfiguration="CL")
A2._assert("A1-1315       NNE  20", 4.5, expectedconfiguration="CL")
A3._assert("A1-1515       ENE  30", 5.0, expectedconfiguration="1/2")
A4._assert("A1-1715       NNW  40", 5.5, expectedconfiguration="CL")
A5._assert("A1-1915       WNW  50", 6.0, expectedconfiguration="DT")

starttestsetup()
A1 = aircraft(1, "AF", "F-80C", "A1-1115", "N", 10, 4.0, "CL")
asserterror("the name argument must be a string.")
A2 = aircraft("A2", "AF", "F-84E", "A1-1315", "NNE", 20, 4.5, "CL")
A3 = aircraft("A2", "AF", "F-84G", "A1-1515", "ENE", 30, 5.0, "1/2")
asserterror("the name argument must be unique.")

endtestsetup()

endfile(__file__)
