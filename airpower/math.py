def onethird(x):

  """
  Return one third of the argument according to the AP rounding rules: minimum 
  is 0.5, leave half integers as they are, otherwise round to the nearest 
  integer.
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

def twothirds(x):

  """
  Return two thirds of the argument, obtained by subtracting one third 
  according to the AP rounding rules.
  """

  return x - onethird(x)
