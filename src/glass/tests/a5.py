from glass.tests.infrastructure import *

startfile(__file__, "maps")

# Check we can at least read all of the maps.

for sheet in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    starttestsetup(sheets=[[sheet]])

for letter in "ABCD":
    for number in range(1, 7):
        sheet = "%s%d" % (letter, number)
        starttestsetup(sheets=[[sheet]])

endfile(__file__)
