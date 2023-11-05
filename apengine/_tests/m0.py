from apengine._tests.infrastructure import *
startfile(__file__, "stores")

starttestsetup()
A1 = aircraft("A1", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
                "2": "BB/M65",
                "3": "BB/M65"
              })
A1._assert("2024       N    10", 4.0, configuration="DT")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "1": "FT/600L",
                "4": "FT/600L",
              })
A1._assert("2024       N    10", 4.0, configuration="1/2")
endtestsetup()


starttestsetup()
A1 = aircraft("A1", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "5": "RK/HVAR",
                "8": "RK/HVAR",
              })
A1._assert("2024       N    10", 4.0, configuration="CL")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C", "2024", "N", 10, 4.0,
              stores={
                "3": "BB/M57",
                "4": "BB/M57"
              })
A1._assert("2024       N    10", 4.0, configuration="CL")
endtestsetup()

endfile(__file__)