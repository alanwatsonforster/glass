def onethirdfromtable(x):

  """
  Return one third of the argument according to the AP table. This is:
  minimum is 0.5, leave half integers as they are, otherwise round to 
  the nearest integer.
  """

  x = x / 3
  if x < 0.5:
    return 0.5
  elif x % 1 == 0.5:
    return x
  elif x % 1 < 0.5:
    return x // 1
  else:
    return x // 1 + 1

def twothirdsfromtable(x):

  """
  Return two thirds of the argument, obtained by subtracting one third 
  according to the AP rounding rules.
  """

  return x - onethirdfromtable(x)

def rounddown(x):

  """
  Return the argument rounded to the nearest integer towards zero.
  """

  assert x >= 0

  return int(x)

def roundup(x):

  """
  Return the argument rounded to the nearest integer away from zero.
  """

  assert x >= 0

  if int(x) == x:
    return int(x)
  else:
    return int(x) + 1

def round(x):

  """
  Return the argument rounded to the nearest integer, breaking ties by 
  rounding away from zero.
  """

  if x > 0:
    return int(x + 0.5)
  else:
    return int(x - 0.5)

def roundtohalf(x):

  """
  Return the argument rounded to the nearest half-integer, breaking ties by 
  rounding towards zero.
  """

  return round(x * 2) / 2

def roundtoquarter(x):

  """
  Return the argument rounded to the nearest quarter-integer, breaking ties by 
  rounding towards zero.
  """

  return round(x * 4) / 4