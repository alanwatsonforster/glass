_known_variants = [
  "disallow NE/SE/SW/NW",
  "disallow ENE/ESE/WSW/WNW",
  "prefer NE/SE/SW/NW",
  "disallow HT/FT",
  "prefer version 1 bleed rate",
  ""
]

_variants = []

def setvariants(variants):

  """
  Set the variants.
  """

  global _variants
  _variants = variants

def withvariant(variant):

  """
  Return True if the variant has been set. Otherwise return False.
  """

  return variant in _variants
