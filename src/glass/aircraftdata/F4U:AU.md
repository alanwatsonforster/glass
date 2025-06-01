# F4U and AU Corsair

## ADCs

- [F4U-4](F4U-4.json)
- [F4U-4B](F4U-4B.json)
- [F4U-4P](F4U-4P.json)
- [F4U-5](F4U-5.json)
- [F4U-5P](F4U-5P.json)
- [F4U-5N](F4U-5N.json)
- [F4U-5NL](F4U-5NL.json)
- [AU-1](AU-1.json)

## Notes and Changes

### Original ADCs

APJ 32 contains ADCs for the F4U-5 and AU-1.

### Versions Serving in Korea

Cleaver mentions the following versions:

- F4U-4: USN & USMC.
- F4U-4B: USN & USMC.
- F4U-4P: USN.
- F4U-5N: USMC & USN.
- F4U-5NL: Winterized F4U-5N. USMC & USN?
- F4U-5P: USMC & USN.
- AU-1. USMC.

He makes no mention of the plain F4U-5 serving. Tilman (Warbird, ch. 5) confirms that the -5 did not serve in Korea.

Cleaver (ch. 16) notes that the -4 was preferred to the -4B on carriers: “The reason for this lay in the fact that the cannon were difficult to service and arm when the wings were folded, while the machine guns were not. Aboard the carriers, it was not possible due to space limitations to service the Corsairs on the cramped hangar decks without their wings being folded.”

### Versions Serving in Suez and Indo-China

F4U-7 and AU-1 according to Wikipedia.

### F4U-4 and -4B

The SAC of the F4U-4 and F4U-5 show quite similar performance. It looks like the additional power of the -5 is balanced by its heavier weight.

ADCs based on the above were created in [18c8bcb](https://github.com/alanwatsonforster/glass/commit/18c8bcbcba1c6b2a2de8be5b6dea1b2ea28ff5d6).

### F4U-4P and F4U-5P

These seems to be essentially a -4 or -5 (complete with guns and weapon stations) with an overhead or oblique cameras (SAC).

Overhead: 5000 ft AGL and 220 kt (Tilman, Warbirds, p. 54)

Oblique: 400 ft AGL and 280 kk (Tillman, Warbirds, p. 57)

Added in [cd0ec03](https://github.com/alanwatsonforster/glass/commit/cd0ec039f32a7bff25ab7fd357ca7af10f9a981f).

### AU-1

Attack variant for USMC, with armor, oil coolers relocated to reduce vulnerability, simplified superchargers, and two additional weapon racks.

### Guns

The -4 has six .50 cals with 390 rounds per gun, or more precisely 400 each for the inner two guns and 375 for the outer guns (Goebel; Tilman, ch. 1). However the SAC says it has 2400 rounds which would be 400 for each gun. The Mustang had about 300 rounds per gun and its ADC gives it 10.0 ammunition. Scaling, the F4U-4 should have 13.0. 

F4U-2s has only five .50 cals and reduced the ammunition load to 250 rounds per gun (Tilman, ch. 1).

Gun effectiveness of those armed with .50 cal M2s reduced for lower rate of fire of the M2 in 
[e615570](https://github.com/alanwatsonforster/glass/commit/e61557086cfc61119e920453d1bded66bac57bd3).

The -4B, -5, and AU-1 have four 20 mm M3 with 231 rounds per gun (SACs). I have increased the hit rolls of these from 6/3/2 to 6/4/3, to match similar-armed fighters. See [#157](https://github.com/alanwatsonforster/glass/issues/157).

ADCs based on the above were created in [18c8bcb](https://github.com/alanwatsonforster/glass/commit/18c8bcbcba1c6b2a2de8be5b6dea1b2ea28ff5d6).

### Stores

The -4 and -4P have eight Mk5 rocket launchers and two wing pylons (SAC). The rocket launchers are for HVARs. The wing pylons can carry two 150 gal FTs, two 1000/500/250 lb BBs or two "A.R. 11.5" Tiny Tim rockets (SAC). The -4B is the same, but with Mk 9 rocket launchers in place of the Mk 5 rocker launchers (SAC). Some used the Mk8 shackle to carry 110 lb and 220 lb frag bombs (White) on the outer wings, but at least initially some has only rocket rails (Lantham). Starting in 1951, some F4U-4s used the AERO 14A in Korea (Brehm Daniels).

The -4 and -4B do not have a centerline stations (SAC), which is surprising since it existed on the F4U-1, but I can find no photographic evidence to contract this. I've seen several photos of -4/-4B with a FT on one wing (or napalm?) and a 500 lb BB on the other (e.g., Tillman, Warbirds, p. 76).

The -5 has eight Mk 9 rocket launchers, two wing pylons, and one centerline pylon (SAC). The rocket launchers are for HVARs. The wing pylons can carry “A.R. 11.75"” Tiny Tim rockets, two 500/100/1000 lb BBs, or two 150 gal FTs. The centerline pylon can carry a 500/100/1600/2000 lb BB or another Tiny Tim (SAC). The total bomb capacity is 5200 lb (SAC).

The AU-1 has ten AERO 14A bomb and rocket launchers (presumably similar to the AD's Aero 14 racks) in place of the rocket launchers and each has a capacity of 500 lb (SAC). Loads include ten HVAR, ten 260 lb BB, and six 500 lb BB (SAC). It has three Mk 51 racks, two on the wing and one centerline, each with a capacity of 2000 lb (SAC). The total bomb capacity is 8,200 lb (SAC). Only the wing pylons are capable of carrying FTs (SAC). Loads include 1000 lb BB, 150 gal FT (SAC).

At least some F4U-5Ns in Kora used Mk 55 bomb racks and could carry 260 lb frag BB, 250 lb GP, and 100 lb GP (Daniels). 

I will simply note that early war F4Us were limited to HVARs and in some cases 100/200 lb BBs, but from 1951 they could also used 250/500 lb BBs.

Stores updated in [606b10b](https://github.com/alanwatsonforster/glass/commit/606b10b401b1a90c493f17d3fea7f058634c8ef8).

### FTs

Early tanks were 174 gal on the centerline pylon and 154 or 178 gal tanks on the two wing pylons (Dial). The F4U-4, -4B, and -5 used 150 gal tanks (SAC).

Fuel tanks updated in [606b10b](https://github.com/alanwatsonforster/glass/commit/606b10b401b1a90c493f17d3fea7f058634c8ef8).

### F4U-2

AIA radar in pod on starboard wing and only five .50 cal and ammunition reduced to 250 rounds per gun. Effective range 2 miles. Quoted range 3 miles.

### F4U-5N

AN/APS-19 radar in pod on starboard wing.

> “Pilots of VMF(N)-513 and VMF(AW)-542 could use their AN/APS-19 radars to map the terrain below for nearly 80 miles ahead.” (Cleaver)

> “The APS-19 radar carried by the Corsairs and Skyraiders was useless when it came to detecting landmarks on the ground or small troop units, while the mountainous terrain of North Korea blocked the radar from seeing what might otherwise have been seen. The APS-6 was better for ground mapping. The result was that the night fliers relied on visual spotting of targets.” (Cleaver)

Range given as 100 miles (nm?) for surface targets and 20 nm for aircraft (70 hexes), with a scan range of 130 deg (Manual).

- F-86L Sabre Dog APG-36 has 70-10 and 180+
- F-89D Starfire E-6 has 100-20 and 180+
- F-94A Scorpion APG-33 has 60-10 and 180+

Perhaps give is 70-10 and 180+ like the APG-36. I'm deliberately ignoring the statement that is has a scan angle of 130 deg, since no other early radar has a 150+ arc. It does not seem to have any automatic tracking capability, although perhaps we can consider it to have to 8 nm (20 hexes) the 30 deg cone (limited arc).

When used as a ground nav radar, the 80 nm range would be 280 hexes. This makes is much more powerful than other ground mapping radars. I'll leave this for the time being.

Added in [8622611](https://github.com/alanwatsonforster/glass/commit/8622611a1603e29ffe88f50dfdbceb001c6ce439).

### Dive Brakes

The undercarriage could be lowered or trailed to act as a dive break. They could be selected up to 380 kn = 440 mph, but once selected (and locked in place) could be used at higher speeds. I have added this as a 0.5 FP drag. Added in [227c0eb](https://github.com/alanwatsonforster/glass/commit/227c0eb0a607e956d59c478a7613d46fffab34c2).

## Bibliography

- Brehm, “[Action Report of CVG-101](https://www.history.navy.mil/content/dam/nhhc/research/archives/action-reports/Korean%20War%20Carrier%20Air%20Group%20Combat/PDF%27s/cvg101-30apr-4jun51.pdf)”, 30 April to 4 June 1951
- Daniels, “[Action Report of ATG2](https://www.history.navy.mil/content/dam/nhhc/research/archives/action-reports/Korean%20War%20Carrier%20Air%20Group%20Combat/PDF%27s/atg2a-52.pdf)”, 18 July to 4 September 1952.
- Dial, “The Chance Vought F4U Corsair,” Profile Publications, 1965
- [Goebel](https://www.airvectors.net/avf4u.html)
- Lantham, “[Action Report of CVG-5](https://www.history.navy.mil/content/dam/nhhc/research/archives/action-reports/Korean%20War%20Carrier%20Air%20Group%20Combat/PDF%27s/cvg5-16-31jul50.pdf)”, 16 to 31 July 1950.
- [Manual for F4U-5N](https://stephentaylorhistorian.com/wp-content/uploads/2020/04/f4u-5n-corsair.pdf)
- [SAC for F4U-4](https://www.aahs-online.org/images/Navy_SAC/F4U-4.pdf)
- [SAC for F4U-4B](https://www.aahs-online.org/images/Navy_SAC/F4U-4B.pdf)
- [SAC for F4U-4P](https://www.aahs-online.org/images/Navy_SAC/F4U-4P.pdf)
- [SAC for F4U-5](https://www.aahs-online.org/images/Navy_SAC/F4U-5.pdf)
- [SAC for F4U-5P](https://www.aahs-online.org/images/Navy_SAC/F4U-5P.pdf)
- [SAC for F4U-5N](https://www.aahs-online.org/images/Navy_SAC/F4U-5N.pdf)
- [SAC for AU-1](https://www.aahs-online.org/images/Navy_SAC/AU-1.pdf)
- Tilman, Barrett, “Corsair: The F4U in World War II and Korea”
- Tilman, Barrett, "Warbird Tech: The F4U Corsair", ????
- [Wikipedia](https://en.wikipedia.org/wiki/Vought_F4U_Corsair)
- White, “[Action Report of CAG2](https://www.history.navy.mil/content/dam/nhhc/research/archives/action-reports/Korean%20War%20Carrier%20Air%20Group%20Combat/PDF%27s/cvg2-50-1.pdf)”, 15 September to 2 October 1950.



