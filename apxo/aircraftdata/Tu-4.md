# Tupolev Tu-4

## ADCs

- [Tu-4](Tu-4.json)
- [Tu-4A](Tu-4A.json)

## Notes and Changes

### Original ADC

The ADC is based on that for the [B-29](B-29.md).

### Guns

The twin .50 cal machine guns in the B-29 were replaced with twin 23 mm NS-23 (Nudelman-Suranov) cannons. We can compare them to the twin AM-23 (Afanasev-Makarov) cannons in the Tu-16 and the twin NR-23 mm (Nudelman-Rikhter) cannons in the Il-28. The rates of fire per barrel are:

- .50 cal M2	800 RPM
- NS-23		550 RPM
- AM-23		1250 RPM
- NR-23		650 RPM

In Air Power, these are:

- B-26		0=2	1=1	2=1	Ammo = ?		AtA = 2	360 degrees
- B-29		0=2	1=1	2=1	Ammo = ?		AtA = 2	90+ arc
- B-29		0=3	1=2	2=2	Ammo = ?		AtA = 2	60− arc
- Il-28		0=3	1=2	2=1	Ammo = 6.0		AtA = 4	60− arc
- Tu-16		0=2	1=1	2=1	Ammo = 12.0		AtA = 4	360 degrees

The B-29 has a −1 modifier when firing into its 60− arc, which I show above, and are otherwise modified only for size. The Il-28 tail guns can fire into the 60− arc with no modifiers except target size. The Tu-16 guns are only modified by target size and possibly tail radar ranging in the 30− arc.

All can fire defensively twice against aircraft carrying out gun attacks. The B-26 can only fire at one target, since there is only one gunner, but it can fire twice. The B-26 and B-29 can fire offensively once if they do not fire defensively, and I presume the Tu-16 could do the same.

I’m surprised the rolls to hit of the Tu-16 are so low, given the higher rate of fire of the AM-23 compared to the NR-23 and, presumably, its longer range compared to the .50 cal in the B-29. That said, the Tu-16 has a tail radar that gives a −1 RE modifier against targets in its 30− arc on a roll of 7−. Successful ranging gives an effective rating of 3/2/2. The Il-28 does not have an equivalent capability.
The −1 modifier for the B-29 is rather generous, as it gives a better roll-to-hit than that Il-28 at a range of 2.

I’d suggest that the AtA rating of the Tu-4 be 4, matching the other similar twin 23 mm mounts.

Given the similarity between their fire-control systems and rates of fire, the rolls-to-hit of the Tu-4 should be no worse than the B-29. They should also be no better than the similar Il-28, but as noted above the Il-28 is not completely consistent with the B-29 tail gun. I adopt the B-29 rolls-to-hit.

- Tu-4		0=2	1=1	2=1	Ammo = 20		AtA = 4	60+ arc
- Tu-4		0=3	1=2	2=2	Ammo = 20		AtA = 4	60− arc

The ammunition of the B-29 is given as 500 rounds or about 150 lb per gun. The weight of the NS-23 round is about 12 oz ([Arsenal](https://arsenal-defense.com/wp-content/uploads/spec-sheets/TP_23x115_AIR.pdf)). Assuming the same weight of ammunition, the Tu-4 would carry 200 rounds per gun. With a rate of 550 RPM, this gives 11 two-second bursts.

### Radar

I doubt the Tu-4 had radar. Removed in [faab60](https://github.com/alanwatsonforster/apxo/commit/2faab6011d7566f6ca941e21c1f7b522ff94bf32).

The Tu-4 may have been equipped with a navigation radar (Guerrero):

> The Radar RPB RPB Kobal’t or Kobal’t-M was used for navigation over the ground and target recognition. This was a copy of the US AN/APQ-13 re-engineered by NII-17.

### Bomb Load

Wikipedia (quoting Gordon) states that the bomb load was six 1,000 kg (2,200 lb) bombs = 13,200 lb total. I don't think the M46 series had a 1,000 kg variant, but the M54 series does. 

I am assuming the M46 series was carried. Comparing it to the B-29A, a reasonable guess is two 1500 kg, six 500 kg, or twelve 250 kg bombs per bay. Added in [e55d0dd](https://github.com/alanwatsonforster/apxo/commit/e55d0dd8a505ec074af6063614089593241af6fa).

### FTs

I presume the Soviets deployed internal FTs like those in the B-29. Added in [2d81218](https://github.com/alanwatsonforster/apxo/commit/2d81218ee0aaa166e1c80f16eeb6519176d520df) and [a253f9d](https://github.com/alanwatsonforster/apxo/commit/a253f9d40113dbfbc4b4e4eb193fd6e4c28d14c6).

### Nuclear Weapons

Added to Tu-4A in [624b2d5](https://github.com/alanwatsonforster/apxo/commit/624b2d578a4ff93d2fd2c8f36ee3104ac4641200).

- [RDS-3](https://en.wikipedia.org/wiki/RDS-3) [Three times](https://en.wikipedia.org/wiki/RDS-2_Linage) weight of RDS-4, so 3600 kg = 8000 lb
- [RDS-4](https://en.wikipedia.org/wiki/RDS-4) 1200 kg = 2600 lb (tested, but this is a tactical weapon so probably not deployed on the Tu4).

### Tu-4A

I presume the Tu-4A was stripped, like the Silverplate/Saddletree B-29s. Added in [cfd5e7b](https://github.com/alanwatsonforster/apxo/commit/cfd5e7b42f714086cc7ff712895a3fdbaba31d4b) and [c4f6ef1](https://github.com/alanwatsonforster/apxo/commit/c4f6ef185207aa902909689a25cbad6d601c028a).

## Other Possible Versions

- Tu-4K with two AS-1 Kennel ASMs.

## Bibliography

- Guerrero, Javier, “[A Look into the Tupolev Tu-4](https://nuclearcompanion.com/data/tupolev-tu-4-standard-specification-performance/)”
- Tokarev Maksim Y., “[Kamikazes: The Soviet Legacy](https://digital-commons.usnwc.edu/nwc-review/vol67/iss1/7/)” (Tu-4k)
- [Wikipedia](https://en.wikipedia.org/wiki/Tupolev_Tu-4)