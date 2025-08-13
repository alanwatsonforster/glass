# CAC Sabre

## ADCs

- [CAC Sabre Mk.30](Avon%20Sabre%20Mk.30.json)
- [CAC Sabre Mk.31](Avon%20Sabre%20Mk.31.json)
- [CAC Sabre Mk.31 (1960 Upgrade)](Avon%20Sabre%20Mk.31%20(1960%20Upgrade).json)
- [CAC Sabre Mk.32](Avon%20Sabre%20Mk.32.json)

## Notes and Changes

### Original ADCs

ADCs for the Mk.31/32 appear in APJ 25.

### Mk.30

The Mk.31 has the unslatted 6-3 wing. The Mk.30 is essentially a Mk.31 with the earlier slatted wing (Wikipedia). The minimum speeds and turn drags of the Mk.31 match those of the F-86F-25, which also has the unslatted 6-3 wing. This suggests that we can create an ADC for the Mk.30 by modifying that of the Mk-31 with the minimum speeds and turn drag of the F-86F. Added in [30c23b1](https://github.com/alanwatsonforster/glass/commit/30c23b11cc4ed029e767ed874b547de33682565e).

The F-86A/E/F with the early slatted wing are HTD, so the Mk.30 should be too.

### Fuel Tanks

- Curtis (p. 114) states that the Mk.32 could carry 100 gal (450L) and 167 gal (760L) FTs (perhaps on the inner pylons).
- Farquhar states that the Mk.32 could carry 100 gal FTs on the inner pylons and 167 gal FTs on the outer ones.
- Wikipedia states they could carry 200 gal (900L) FTs on the outer pylons. This may be a confusion between US gal and imperial gal, since 167 imperial gal is about 200 US gal.

### Weight Limits

The weight limits are given uniformly as 1000 per station. Both could carry a 200 US gal (167 gal) FT on the outer pylons. This weights about 1400. Wikipedia gives the load limits of the F-86F and Mk.32 as 5300 and states they can both carry two 1000 lb bombs and two 200 US gal FTs, which would be a total of about 4800. I have increased the outer pylon loads to 1500 and the total loads to 3000 for the Mk.30/31 and 5000 for the Mk.32. Changed in [4e671f5](https://github.com/alanwatsonforster/glass/commit/4e671f5974b0aa8a0f535c2bb0911aee836a6f86).

### Guns

Two 30 mm ADENs with 162 rounds per gun (Wikipedia).

## Bibliography

- Curtis, “North American F-86 Sabre”, 2000, Crowood
- [Farquhar](http://www.adf-serials.com.au/research/avon-sabre.pdf)
- [Wikipedia](https://en.wikipedia.org/wiki/CAC_Sabre)