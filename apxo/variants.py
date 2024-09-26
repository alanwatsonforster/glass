_knownvariants = [
    "disallow NE/SE/SW/NW",
    "disallow ENE/ESE/WSW/WNW",
    "prefer NE/SE/SW/NW",
    "disallow HT/FT",
    "use first-edition ADCs",
    "use version 2.4 rules",
    "draw counters",
    "require limited radar arc for SSGT",
    "use house rules",
]

variants = []


def setvariants(_variants):
    """
    Set the variants.
    """

    for variant in _variants:
        if variant not in _knownvariants:
            raise RuntimeError("unknown variant %r." % variant)

    global variants
    variants = _variants


def withvariant(variant):
    """
    Return True if the variant has been set. Otherwise return False.
    """

    assert variant in _knownvariants

    return variant in variants
