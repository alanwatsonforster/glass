_knownvariants = [
  "disallow NE/SE/SW/NW",
  "disallow ENE/ESE/WSW/WNW",
  "prefer NE/SE/SW/NW",
  "disallow HT/FT",
  "prefer version 1 bleed rate",
  "use version 2.4 rules"
]

variants = []

def setvariants(_variants):

  """
  Set the variants.
  """

  global variants
  variants = _variants

def withvariant(variant):

  """
  Return True if the variant has been set. Otherwise return False.
  """

  return variant in variants
