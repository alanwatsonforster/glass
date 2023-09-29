_donotlog = False

def log(s):
  if _donotlog:
    return
  print(s)

def logbreak():
  if _donotlog:
    return
  print()
