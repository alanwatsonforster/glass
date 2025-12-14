# Mikoyan-Gurevich MiG-15

## ADCs

- [MiG-15bis](MiG-15bis.json)
- [MiG-15P](MiG-15P.json)
- [MiG-15ISh](MiG-15ISh.json)

## Notes and Changes

### Original ADCs

The ADCs for the -15bis, -15P, and -15ISh are originally from TSOH.

### Guns

I have removed "*" from the AtG rating; see [#206](https://github.com/alanwatsonforster/glass/issues/206).

### FTs

Goebel states it could use 250L, 300L, 400L, or 600L FTs. These are 550, 650, 700, and 1100 lb each, but the standard pylon is only for 550 lb. I have added a restriction that the heavier tanks can be carried but turns are limited to HT with the 300/400L and TT with the 600L. Added in [07c3bd0](https://github.com/alanwatsonforster/glass/commit/07c3bd00f04050fffff80aca8ff9cbdee6edf7ce).

### MiG-15UTI

Wikipedia and Goebel state that it has a single 12.7 mm. I've adapted the gun characteristics from the T-33A.

Internal fuel is reduced. I'm guessing from 125 to 100.

## Bibliography

- [Goebel](https://www.airvectors.net/avmig15_1.html)
- [Wikipedia](https://en.wikipedia.org/wiki/Mikoyan-Gurevich_MiG-15)
