# A3J and A-5 Vigilante

## Versions and Variants

### A3J-1/A-5A

- [ADC for A3J-1](A3J-1.json)
- [ADC for A-5A](A-5A.json

ADC from TSOH.

### A3J-2/A-5B

- [ADC for A3J-2](A3J-2.json)
- [ADC for A-5B](A-5B.json

ADC from TSOH.

### A3J-3P/RA-5C

- [ADC for A3J-3P](A3J-3P.json)
- [ADC for RA-5C](RA-5C.json)
- [ADC for RA-5C (1967 Upgrade)](RA-5C%20(1967%20Upgrade).json)
- [ADC for RA-5C (1971 Upgrade)](RA-5C%20(1971%20Upgrade).json)

ADC from TSOH.

## Notes and Changes

### Initial ECM

I'd guess that the RA-5C didn't have ECM before 1965.

### Fuel

- A-5A SAC: 2215 gal internal, two or three 295 gal FT, and up to two 400 gal FT on external pylons
- A5-B SAC: 2715 gal internal, two or three 295 gal FT, and  up to four 400 gal FT on external pylons.
- RA-5 SAC: 2715 gal internal, three 295 gal FT, and up to four 400 gal FT on external pylons

This means:

- 295 FT = 1100L, weight 2000, fuel 95
- A-5A internal fuel = 2215 * 6.5 / 20 = 720
- A-5A fuel points = (2215 + 2 * 295) * 6.5 / 20 = 911
- A-5B/RA-5C internal fuel = 2715 * 6.5 / 20 = 882
- A-5B fuel points = (2715 + 2 * 295) * 6.5 / 20 = 1074
- A-5B/RA-5C fuel points = (2715 + 3 * 295) * 6.5 / 20 = 1170

These are in good agreement with the value of 1170 given in the TSOH ADC for A-5B/RA-5C with three tanks, but in disagreement with the value of 1025 given for the A-5A with two tanks.

Changed to these values (A-5A = 720, A-5B/RA-5C = 880, 295 FT = 95) in [b48ba52](https://github.com/alanwatsonforster/glass/commit/b48ba521502ba64d9b6507f202606e89d27de2aa).

### Nuclear Bombs

According to the SAC/CS documents:

- A-5A: one [Mark 28](https://en.wikipedia.org/wiki/B28_nuclear_bomb), [Mark 27](https://en.wikipedia.org/wiki/Mark_27_nuclear_bomb), and [Mark 43](https://en.wikipedia.org/wiki/B43_nuclear_bomb) internally and two Mark 43 externally.
- A-5B: one [Mark 28](https://en.wikipedia.org/wiki/B28_nuclear_bomb), [Mark 27](https://en.wikipedia.org/wiki/Mark_27_nuclear_bomb), and [Mark 43](https://en.wikipedia.org/wiki/B43_nuclear_bomb) internally and (presumably up to four) Mark 28 and 43 externally.
- RA-5C: Same as A-5A.

## Operational History

Introduced in June 1961.

## Bibliography

- [Goebel](https://airvectors.net/ava5.html)
- SAC for A3J-1
- SAC for A-5A
- CS for A-5B
- SAC for RA-5C
- [Wikipedia](https://en.wikipedia.org/wiki/North_American_A-5_Vigilante)