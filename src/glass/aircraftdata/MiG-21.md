# MiG-21

## Variants

### MiG-21F (Fishbed-B)

- [ADC](MiG-21F.json)
- Year: 1959
- Description: First production version. Day fighter with two NR-30 guns, but without search radar or missiles.

### MiG-21F-13 (Fishbed-C)

- [ADC](MiG-21F-13.json)
- Year: 1960
- Description: Upgraded F with provision for AA-2 IRMs, but only one NR-30 gun and still without search radar.

### MiG-21PF (Fishbed-D)

- [ADC](MiG-21PF.json)
- Year: 1961
- Description: First all-weather intercepter with RP-21 radar, more powerful engine, and the ability to use AA-1 BRMs and AA-2 IRMs.

### MiG-21PFM (Fishbed-F)

- [ADC](MiG-21PFM.json)
- Year: 1964
- Description: Updated MiG-21PF with blown flaps, improved RP-21M radar, the capability to carry the GP-9 gun pod, and from 1966 the capability to carry the Kh-66 ASM.

### MiG-21FL (Fishbed-D)

- [ADC](MiG-21FL.json)
- Year: 1965
- Description: Export version of the MiG-21 with less powerful engine (from the MiG-21F/F-13, no AA-1, and a downgraded version of the RP21 designated R1L.

### MiG-21S (Fishbed-J)

- [ADC](MiG-21S.json)
- Year: 1964
- Interceptor with the RP-22 radar, able to use the AA-2 IRMs and RHMs and AA-1 BRMs. No internal guns, but able to mount a GP-9 gun pod. Not exported.

### MiG-21M (Fishbed-J)

- [ADC](MiG-21S.json)
- Year: 1968
- Description: Export version of the MiG-21S with the RP-21MA radar instead of RP-22, an internal GSh-23L gun, and AA-2 IRMs.

### MiG-21SM (Fishbed-J)

- [ADC](MiG-21SM.json)
- Year: 1969
- Description: Upgrade of the MiG-21S with a new engine and internal GSh-21L cannon.

### MiG-21MF (Fishbed-J)

- [ADC](MiG-21MF.json)
- Year: 1970
- Description: Export version of the MiG-21SM with the same RP-22 radar and engine and the ability to use AA-2 and AA-8 IRMs.

### MiG-21bis (Fishbed-L/N)

- [ADC](MiG-21bis.json)
- Year: 1972
- Description: Version with RP-22 radar and improved engine.

## Notes and Changes

### Summary of TSOH and Revised Version

The TSOH ADCs from 1994 give versions which do not seem to correspond precisely to our current (presumably much better) knowledge of MiG-21 version. I have attempted to determine which current version corresponds to which TSOH version:

- TSOH F = F-13 (able to use AA-2 IRMs)
- TSOH PF = PF
- TSOH FL = FL
- TSOH Improved PF = PFM
- TSOH PFMA = S
- TSOH export FPMA = M
- TSOH MF = SM
- TSOH export MF = MF

### MiG-21F

ADC adapted by AWF from that of the F-13.

### MiG-21F-13

ADC from the TSOH. The TSOH ADC describes an "MiG-21F" with only one gun, primitive radar, and the ability to carry AA-2 IRMs; this seems to be a MiG-21F-13.

### MiG-21PF

ADC from TSOH.

### MiG-21PFM

ADC from TSOH. In TSOH it is described as an "improved PFM".

### MiG-21FL

ADC from TSOH.

### MiG-21S

ADC from TSOH. The TSOH ADC for the MiG-21MF describes an "MiG-21PFMA" that is an early version of the "MiG-21MF" but with less AB power that the MF, a RP-22 (Jaybird) radar, no gun but the ability to carry a GP-9 gunpack, and the ability to use AA-2 IRMs and RHMs; since the "MiG-21MF" seems to be a MiG-21SM, this "MiG-21PFMA" seems to be a MiG-21S.

### MiG-21M

ADC from TSOH. The TSOH ADC describes an "MiG-21PFMA export version" as a "MiG-21PFMA" with a Spin Scan-B radar and internal GSh-21 gun; since the "MiG-21PFMA" seems to be an MiG-21S, this "MiG-21PFMA export version" seems to be a MiG-21M.

### MiG-21SM

ADC from the TSOH. The TSOH ADC labels this as an MF.

### MiG-21MF

ADC from TSOH. The TSOH ADC describes an "MiG-21MF export version" with Spin Scan-B radar, but this appears to be simply a MiG-21MF. It is further adapted based on information in the Wikipedia article on MiG-21 variants, which is based on Gordon.

### MiG-21bis

ADCs for the MiG-21bis appear in APJ 39 and APJ 43. We typically adopt values from APJ 43. However, the SPBR values seem to be converted at the rate of 1 FP = 4 DP rather than the accepted rate of 1 FP = 2 DP. Therefore, we use the values from APJ 39 at this rate; instead of 2/2/2 we use 1/1/1. See #282.

### Radars

I have taken the radar names from the Wikipedia article on MiG-21 versions, which is derived from Gordon. Added in [750fd28](https://github.com/alanwatsonforster/glass/commit/750fd2867100ac5945edb520e325bed56558157e) and [baa63c7](https://github.com/alanwatsonforster/glass/commit/baa63c78114b2940d2e13d44342c74bba76f8f48).

### NR-30 Guns

See [#208](https://github.com/alanwatsonforster/glass/issues/208).

### Missiles

The Wikipedia article on variants states that the MF could not use AA-2C RHMs, but could use AA-8 IRMs as a new capability. Added in [999ee10](https://github.com/alanwatsonforster/glass/commit/999ee109bb9c96551b483289f47ac8e0d9959a4b).

### Use of GP-9

Müller states that the GP-9 was only used on the PFM, FL, and S. Removed from PF in [4e62484](https://github.com/alanwatsonforster/glass/commit/4e624841cf6d4b5e1c6cfd8189370378c6a86d6f).

### Speed

Ethell & Price (ch. 1) state that the MiG-21MF was faster than the F-4J (Mach 1.15 = 880 mph) below 5,000 feet, whereas earlier versions were slower (Mach 1.05 = 800 mph). 

According to Wikipedia, Vietnam used:
- MiG-21F-13 from 1965
- MiG-21PFL (modified PF) from 1966
- MiG-21PFM from 1968
- MiG-21MF from 1970

The TSOH ADCs have maximum speeds of 6.5 for the MiG-21F-13/PF/PFM, 8.0 for the MiG-21MF, and 8.5 for the F-4J.

Perhaps the TSOH ADC underestimates the speed of the MF (perhaps it should be 9.0) and earlier MiGs (perhaps they should be 8.0)

## Operational History

Introduced in fall of 1959 (Goebel).

## Bibliography

- [Goebel](http://www.airvectors.net/avmig21.html)
- Gordon, Mikoyan MiG-21 (Famous Russian aircraft).
- Müller, [The MiG-21](https://mig-21.de/english/default.htm)
- [Wikipedia on MiG-21](https://en.wikipedia.org/wiki/Mikoyan-Gurevich_MiG-21)
- [Wikipedia on MiG-21 Variants](https://en.wikipedia.org/wiki/List_of_Mikoyan-Gurevich_MiG-21_variants)
- [Wikipedia on RP-21 radar](https://en.wikipedia.org/wiki/RP-21_Sapfir)
- Ethell & Price, "One Day in a Long War"