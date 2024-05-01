from apxo.tests.infrastructure import *

startfile(__file__, "math")

# Checks on apxo.math.

from apxo.math import onethirdfromtable, twothirdsfromtable

# This table is from the play aids.


def checkthirds(a, b, c):
    assert onethirdfromtable(a) == b
    assert twothirdsfromtable(a) == c


checkthirds(1.0, 0.5, 0.5)
checkthirds(1.5, 0.5, 1.0)
checkthirds(2.0, 1.0, 1.0)
checkthirds(2.5, 1.0, 1.5)
checkthirds(3.0, 1.0, 2.0)
checkthirds(3.5, 1.0, 2.5)
checkthirds(4.0, 1.0, 3.0)
checkthirds(4.5, 1.5, 3.0)
checkthirds(5.0, 2.0, 3.0)
checkthirds(5.5, 2.0, 3.5)
checkthirds(6.0, 2.0, 4.0)
checkthirds(6.5, 2.0, 4.5)
checkthirds(7.0, 2.0, 5.0)
checkthirds(7.5, 2.5, 5.0)
checkthirds(8.0, 3.0, 5.0)
checkthirds(8.5, 3.0, 5.5)
checkthirds(9.0, 3.0, 6.0)
checkthirds(9.5, 3.0, 6.5)
checkthirds(10.0, 3.0, 7.0)
checkthirds(10.5, 3.5, 7.0)
checkthirds(11.0, 4.0, 7.0)
checkthirds(11.5, 4.0, 7.5)
checkthirds(12.0, 4.0, 8.0)
checkthirds(12.5, 4.0, 8.5)
checkthirds(13.0, 4.0, 9.0)
checkthirds(13.5, 4.5, 9.0)
checkthirds(14.0, 5.0, 9.0)
checkthirds(14.5, 5.0, 9.5)
checkthirds(15.0, 5.0, 10.0)

endfile(__file__)
