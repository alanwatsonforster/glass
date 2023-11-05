
_storedict = {
    "FT/250L"          : ["FT",  550, 1.5,  25],
    "FT/250L/empty"    : ["FT",  550, 1.0,   0],
    "FT/400L"          : ["FT",  700, 2.0,  30],
    "FT/400L/empty"    : ["FT",  700, 1.0,   0],
    "FT/450L"          : ["FT",  800, 2.5,  40],
    "FT/450L/empty"    : ["FT",  800, 1.5,   0],
    "FT/600L"          : ["FT", 1100, 3.0,  50],
    "FT/600L/empty"    : ["FT", 1100, 2.0,   0],
    "FT/700L"          : ["FT", 1300, 3.0,  60],
    "FT/700L/empty"    : ["FT", 1300, 2.0,   0],
    "FT/850L"          : ["FT", 1500, 3.5,  75],
    "FT/850L/empty"    : ["FT", 1500, 2.5,   0],
    "FT/1000L"         : ["FT", 1800, 3.5,  85],
    "FT/1000L/empty"   : ["FT", 1800, 2.5,   0],
    "FT/1200L"         : ["FT", 2200, 4.0, 100],
    "FT/1200L/empty"   : ["FT", 2200, 2.5,   0],
    "FT/1400L"         : ["FT", 2700, 4.0, 120],
    "FT/1400L/empty"   : ["FT", 2700, 3.0,   0],
    "FT/1700L"         : ["FT", 3000, 5.0, 140],
    "FT/1700L/empty"   : ["FT", 3000, 3.5,   0],
    "FT/1900L"         : ["FT", 3500, 6.0, 175],
    "FT/1900L/empty"   : ["FT", 3500, 4.0,   0],
    "FT/2200L"         : ["FT", 4500, 8.0, 200],
    "FT/2200L/empty"   : ["FT", 4500, 5.0,   0],
    "RK/HVAR"          : ["RK",  140, 1.0],
    "RK/Tiny Tim"      : ["RK", 1200, 2.0],
    "BB/M30"           : ["BB",  100, 0.5],
    "BB/M57"           : ["BB",  250, 1.5],
    "BB/M64"           : ["BB",  500, 2.0],
    "BB/M65"           : ["BB", 1000, 3.0],
    "BB/M66"           : ["BB", 2000, 4.0],
    "BB/M74"           : ["BB",  100, 0.5],
    "BB/M76"           : ["BB",  500, 1.5],
    "BB/BLU-1"         : ["BB",  750, 2.5],
  }

def storeclass(storename):
  if not storename in _storedict:
    raise RuntimeError("unknown store %r." % storename)
  return _storedict[storename][0]

def weight(storename):
  if not storename in _storedict:
    raise RuntimeError("unknown store %r." % storename)
  return _storedict[storename][1]

def load(storename):
  if not storename in _storedict:
    raise RuntimeError("unknown store %r." % storename)
  return _storedict[storename][2]
  
def fuel(storename):
  if not storename in _storedict:
    raise RuntimeError("unknown store %r." % storename)
  if storeclass(storename) == "FT":
    return _storedict[storename][3]
  else:
    return 0
  
def totalweight(stores):
  weight = 0
  for loadpoint, storename in stores.items():
    if not storename in _storedict:
      raise RuntimeError("unknown store %r." % storename)
    weight += _storedict[storename][1]
  return weight

def totalload(stores):
  load = 0
  for loadpoint, storename in stores.items():
    if not storename in _storedict:
      raise RuntimeError("unknown store %r." % storename)
    load += _storedict[storename][2]
  # Round down. See 4.3.
  load = int(load)
  return load

def totalfuel(stores):
  fuel = 0
  for loadpoint, storename in stores.items():
    if not storename in _storedict:
      raise RuntimeError("unknown store %r." % storename)
    if _storedict[storename][0] == "FT":
      fuel += _storedict[storename][3]
  return fuel

def _showstores(stores):
  for loadpoint in sorted(stores):
    storename = load[loadpoint]
    print(loadpoint, storename, store[storename])
  print(totalweight(stores))
  print(totallp(stores))
  print(totalfuel(stores))

def _releasestore(stores, loadpoint):
  if not loadpoint in stores:
    raise RuntimeError("load-point %s is not loaded." % loadpoint)
  newstores = stores.copy()
  del newstores[loadpoint]
  return newstores