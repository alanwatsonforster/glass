import airpower.log as aplog

_known_variants = [
  "allow NE/SE/SW/NW",
  "disallow ENE/ESE/WSW/WNW",
  "prefer NE/SE/SW/NW",
  "implicit turn and bank declarations",
  "disallow HT/FT"
]

_variants = []

def setvariants(variants):

  """
  Set the variants.
  """

  if variants == []:
    aplog.log("using default variants.")

  for variant in variants:
    if not variant in _known_variants:
      raise RuntimeError("invalid variant %r." % variant)
    aplog.log("using variant %r." % variant)

  global _variants
  _variants = variants

def withvariant(variant):

  """
  Return True if the variant has been set. Otherwise return False.
  """

  return variant in _variants
