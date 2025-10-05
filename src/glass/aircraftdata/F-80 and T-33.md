# F-80 and T-33 Shooting Star

## ADCs

- [F-80C](F-80C.json)
- [RF-80C](RF-80C.json)
- [T-33A](T-33A.json)
- [AT-33A](AT-33A.json)
- (RT-33A)(RT-33A.json)

## Notes and Changes

### Original ADCs

TSOH gives ADCs for the F-80C, RF-80C, and AT-33A.

### RF-80C

Drendel (p. 13) states that RF-80Cs had one or two KF-14 cameras.

### T-33A

ADC adapted from AT-33A by removing the underwing weapon stations.

### AT-33A

ADC from TSOH, as a variant of the F-80. The original ADC refers to this as an "AT-33", but it seems to correspond to the AT-33A.

Guns specified as .50 cal M3 in [5d648cf](https://github.com/alanwatsonforster/glass/commit/5d648cfe184e56db52e87879456f3b8b4f05f358), under the assumption that they are the same as in the F-80C.

### RT-33A

Drendel (pp. 88, 92, 102, and 103) shows an RT-33A in service with the Armée de l'Air, the Royal Thai AF, Turkish AF, and the Imperial Iranian AF. Yip states that the rear cockpit was used for equipment relocated from the nose of the T-33A and for fuel.

Added in [b5e763e](https://github.com/alanwatsonforster/glass/commit/b5e763e9e925c6f808ab7000c7ba832a6382bc06).

### Guns

Drendel (p. 12) states that the M2 machine guns of the P-80A were replaced by M3 machine guns in the P-80B.

Guns specified as .50 cal M3 in [5d648cf](https://github.com/alanwatsonforster/glass/commit/5d648cfe184e56db52e87879456f3b8b4f05f358) (Wikipedia).

### Internal Fuel

Drendel (p. 52) states that the T-33A had an internal capacity of 353 gal compared to 425 gal for the P-80C. Scaling from the 135 FPs of the F-80C, this gives 112 FPs. Changed in [db5c52f](https://github.com/alanwatsonforster/glass/commit/db5c52f564f379a3e7268709ee95afe27e91fe05).

Yip (p. 134) states that the RT-33A can carry a maximum of 978 gal is 165 gal more than the T-33A. This would seem to agree since 460 (two 230 gal tanks) + 353 (T-33A internal) + 165 = 978. Thus, the internal fuel of the RF-33A is 518 gal. Scaling from the 135 FPs of the F-80C, this gives 165 FPs.

### FTs

Misawa tanks has 265 gal of fuel (compared to the usual 165 gal), but stressed the wings (Thompson, ch. 2 & 3). According to the ADC for the F-80C, the wing-tip stations 1 and 4 have a capacity of 1100 lb but may be overloaded to 1500 lb at a cost of reducing the maximum turn rate to HT. The loads corresponding to 160 gallon (600 liter), 225 gallon (850 liter), and 265 gallon (1000 liter) tanks are 1100 lb, 1500 lb, and 1800 lb. Thus, the original the ADC does not permit mounting a 265 gallon wing-tip tank. I have modified the ADC to permit this in [2bdac9b](https://github.com/alanwatsonforster/glass/commit/2bdac9bca63a80d6df43ce8388d179c18d7fe8f7).

Many photos in Drendel show that the T-33A's tip-tanks are center-mounted. The AFSC report states these are 230 gal. The nearest standard FT would be the 850L (weight 1500, load 3.5/2.5). Use of these would give a DT configuration when full and 1/2 configuration when empty. Added in [fd68583](https://github.com/alanwatsonforster/glass/commit/fd68583e0eee0a82df7a9fdefb6e2201f3b2c88a).

### Weapon Stations and Loads

The TSOH ADC has:

- Two wing-tip stations with a capacity of 1100 lb (FT or BB)
- Two mid-wing stations with a capacity of 1100 lb (BB only)
- Alternatively, instead of the mid-wing stations, four underwing stations with a capacity of 200 lb (RK only)

However:

Thompson

- mentions in many places the use of 500-lb bombs.
- ch. 3: quotes a Col. Clure Smith as stating that they routinely carried two 265 gal Misawa tanks, two 1000 lb bombs, and four HVARs in the winter of 1951. With this load, it required JATO to take off. The 1000 lb bombs were for attacking the bridges across the Yalu.
- ch. 4: shows a photo of 7th FBS F-80s which appear to have Misawa tanks, napalm bombs on the mid-wing stations, and four HVARs on the inner stations (two on each wing stacked one above the other).
- ch. 4: mentions a "90 gal napalm tank". This would be about 340L.
- ch. 5: quotes a pilot as saying that the napalm tanks were of low quality and restricted the approach speed.
- ch. 5: mentions a load of two 500-lb bombs and four 250-lb fragmentation bombs. I presume the 250-lb bombs were carried in place of HVARs.
- ch. 5: quotes a pilot as saying they carried four 500-lb bombs. Might this have been using the wing-tip stations?
- ch. 5: shows a photo of a 35th FBS F-80 armed with two 250-lb bombs on the mid-wing station and four 100-lb bombs on the inner-wing stations.

Jackson:

- p. 59: F-80C with two 500 lb bombs
- p. 61: F-80C with a display of weapons including 1000? lb bombs, 250? lb bombs, HVARs, and napalm/FTs.
- p. 67: F-80C with a napalm tank (capacity unknown)
- p. 69: F-80C with a pair of 500? lb bombs and possibly four HVARs

Therefore, the stations seem to be:

- Two wing-tip stations with a capacity of 1100 lb (for 600L FTs or 500/1000-lb bombs)
- Two mid-wing stations with a capacity of 1000 lb (2 HVARs or one 500/1000-lb bomb)
- Four inner-wing stations with a capacity of 280 lb (2 HVARs or one 250-lb bomb).

Added in [1aa5b7b](https://github.com/alanwatsonforster/glass/commit/1aa5b7bb74aa86a4094d6d2119758389c36d69a8).

## Bibliography

- Jackson, Robert, “Air War Korea 1950-1953,” Motorbooks
- Thompson, Warren, F-80 Units of the Korean War, Osprey
- [Wikipedia on F-80](https://en.wikipedia.org/wiki/Lockheed_P-80_Shooting_Star)
- [Wikipedia on T-33](https://en.wikipedia.org/wiki/Lockheed_T-33)
- [T-33B SAC](https://www.aahs-online.org/images/Navy_SAC/T-33B.pdf)
- [AFSC T-33A Performance Evaluation](https://apps.dtic.mil/sti/tr/pdf/AD0258317.pdf)
- Yip, W, “[Lockheed's RT-33A](https://www.aahs-online.org/pubs/journals/files/692133.pdf)”, AAHSJ, Summer 2024, pp. 133-146
