from apxo.tests.infrastructure import *
startfile(__file__, "distances")

starttestsetup()

from apxo.hex import distance
from apxo.hexcode import toxy

# Distances from 2329.

assert 0 == distance(*toxy("A2-2329"), *toxy("A2-2329"))
assert 0 == distance(*toxy("A2-2329"), *toxy("A2-2329/2229"))
assert 0 == distance(*toxy("A2-2329"), *toxy("A2-2329/2429"))
assert 0 == distance(*toxy("A2-2329"), *toxy("A2-2328/2329"))
assert 0 == distance(*toxy("A2-2329"), *toxy("A2-2328/2229"))
assert 0 == distance(*toxy("A2-2329"), *toxy("A2-2328/2429"))

assert 1 == distance(*toxy("A2-2329"), *toxy("A2-2328"))
assert 1 == distance(*toxy("A2-2329"), *toxy("A2-2328/2228"))
assert 1 == distance(*toxy("A2-2329"), *toxy("A2-2328/2428"))
assert 1 == distance(*toxy("A2-2329"), *toxy("A2-2327/2328"))
assert 1 == distance(*toxy("A2-2329"), *toxy("A2-2327/2228"))
assert 1 == distance(*toxy("A2-2329"), *toxy("A2-2327/2428"))

assert 2 == distance(*toxy("A2-2329"), *toxy("A2-2327"))
assert 2 == distance(*toxy("A2-2329"), *toxy("A2-2327/2227"))
assert 2 == distance(*toxy("A2-2329"), *toxy("A2-2327/2427"))
assert 2 == distance(*toxy("A2-2329"), *toxy("A2-2326/2327"))
assert 2 == distance(*toxy("A2-2329"), *toxy("A2-2326/2227"))
assert 2 == distance(*toxy("A2-2329"), *toxy("A2-2326/2427"))

# Distances from 2329/2330.

assert 0 == distance(*toxy("A2-2329/2330"), *toxy("A2-2329/2330"))
assert 0 == distance(*toxy("A2-2329/2330"), *toxy("A2-2329/2230"))
assert 0 == distance(*toxy("A2-2329/2330"), *toxy("A2-2329/2430"))
assert 0 == distance(*toxy("A2-2329/2330"), *toxy("A2-2329"))
assert 0 == distance(*toxy("A2-2329/2330"), *toxy("A2-2329/2229"))
assert 0 == distance(*toxy("A2-2329/2330"), *toxy("A2-2329/2429"))

assert 1 == distance(*toxy("A2-2329/2330"), *toxy("A2-2328/2329"))
assert 1 == distance(*toxy("A2-2329/2330"), *toxy("A2-2328/2229"))
assert 1 == distance(*toxy("A2-2329/2330"), *toxy("A2-2328/2429"))
assert 1 == distance(*toxy("A2-2329/2330"), *toxy("A2-2328"))
assert 1 == distance(*toxy("A2-2329/2330"), *toxy("A2-2328/2228"))
assert 1 == distance(*toxy("A2-2329/2330"), *toxy("A2-2328/2428"))

assert 2 == distance(*toxy("A2-2329/2330"), *toxy("A2-2327/2328"))
assert 2 == distance(*toxy("A2-2329/2330"), *toxy("A2-2327/2228"))
assert 2 == distance(*toxy("A2-2329/2330"), *toxy("A2-2327/2428"))
assert 2 == distance(*toxy("A2-2329/2330"), *toxy("A2-2327"))
assert 2 == distance(*toxy("A2-2329/2330"), *toxy("A2-2327/2227"))
assert 2 == distance(*toxy("A2-2329/2330"), *toxy("A2-2327/2427"))

# Distances from 2329/2230.

assert 0 == distance(*toxy("A2-2329/2230"), *toxy("A2-2329/2230"))
assert 0 == distance(*toxy("A2-2329/2230"), *toxy("A2-2329"))
assert 0 == distance(*toxy("A2-2329/2230"), *toxy("A2-2229/2230"))
assert 0 == distance(*toxy("A2-2329/2230"), *toxy("A2-2229/2329"))
assert 0 == distance(*toxy("A2-2329/2230"), *toxy("A2-2229"))
assert 0 == distance(*toxy("A2-2329/2230"), *toxy("A2-2328/2329"))

assert 1 == distance(*toxy("A2-2329/2230"), *toxy("A2-2328/2229"))
assert 1 == distance(*toxy("A2-2329/2230"), *toxy("A2-2328"))
assert 1 == distance(*toxy("A2-2329/2230"), *toxy("A2-2228/2229"))
assert 1 == distance(*toxy("A2-2329/2230"), *toxy("A2-2228/2328"))
assert 1 == distance(*toxy("A2-2329/2230"), *toxy("A2-2228"))
assert 1 == distance(*toxy("A2-2329/2230"), *toxy("A2-2327/2328"))

assert 2 == distance(*toxy("A2-2329/2230"), *toxy("A2-2327/2228"))
assert 2 == distance(*toxy("A2-2329/2230"), *toxy("A2-2327"))
assert 2 == distance(*toxy("A2-2329/2230"), *toxy("A2-2227/2228"))
assert 2 == distance(*toxy("A2-2329/2230"), *toxy("A2-2227/2327"))
assert 2 == distance(*toxy("A2-2329/2230"), *toxy("A2-2227"))
assert 2 == distance(*toxy("A2-2329/2230"), *toxy("A2-2326/2327"))

endfile(__file__)
