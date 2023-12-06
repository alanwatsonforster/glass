import apxo.aircraft as apaircraft
import apxo.geometry as apgeometry
import apxo.log      as aplog
import apxo.turn     as apturn

#############################################################################

def advantaged(a, b):

  """
  Return True if a is advantaged over b.
  """

  # See rule 12.2.

  # TODO: tailing.

  # Sighted.
  if not b.sighted():
    return False

  # Not same hex or hexside.
  if apgeometry.samehorizontalposition(a, b):
    return False

  # In 150 or 180 arc.
  arc = apgeometry.angleofftail(a, b, arconly=True)
  if arc != "150 arc" and arc != "180 arc":
    return False

  # Within 9 hexes horizontally.
  if apgeometry.horizontalrange(a, b) > 9:
    return False

  # No more than 6 altitude levels above.
  if b.altitude() > a.altitude() + 6:
    return False

  # No more than 9 altitude levels below.
  if b.altitude() < a.altitude() - 9:
    return False

  # Not below if in VC.
  if a.climbingflight(vertical=True) and b.altitude() < a.altitude():
    return False

  # Not above if in VD.
  if a.divingflight(vertical=True) and b.altitude() > a.altitude():
    return False

  return True

#############################################################################

def disadvantaged(a, b):

  """
  Return True if a is disadvantaged by b.
  """

  # See rule 12.2.

  # This is equivalent to b being advantaged over a.
  
  return advantaged(b, a)

#############################################################################

def orderofflightdeterminationphase(forcerolls):

  def score(a):
    return forcerolls[a.force()]
    
  aplog.logbreak()
  aplog.log("start of order of flight determination phase.")

  for k, v in forcerolls.items():
    aplog.logcomment(None, "roll is %2d for %s." % (v, k))

  unsightedlist     = []
  advantagedlist    = []
  disadvantagedlist = []
  nonadvantagedlist = []

  for a in apaircraft.aslist():

    # TODO: departed, stalled, and engaged.

    if not a.sighted():

      unsightedlist.append(a)
      category = "unsighted"

    else:

      isadvantaged    = False
      isdisadvantaged = False
      for b in apaircraft.aslist():
        if a.force() != b.force():
          if advantaged(a, b):
            a._logevent("is advantaged over %s." % b.name())
            isadvantaged   = True
          elif disadvantaged(a, b):
            a._logevent("is disadvantaged by %s." % b.name())
            isdisadvantaged = True

      if isadvantaged and not isdisadvantaged:
        advantagedlist.append(a)
        category = "advantaged"
      elif isdisadvantaged and not isadvantaged:
        disadvantagedlist.append(a)
        category = "disadvantaged"
      else:
        nonadvantagedlist.append(a)
        category = "nonadvantaged"

    aplog.logcomment(a, "%s and has a score of %d." % (category, score(a)))

  def showcategory(category, alist, forcerolls):
    adict = {}
    for a in alist:
      adict[score(a)] = []
    for a in alist:
      adict[score(a)].append(a.name())
    for k, v in sorted(adict.items()):
      aplog.logmain(None, "  %s" % " ".join(v))

  aplog.logmain(None, "order of flight is:")
  showcategory("disadvantaged", disadvantagedlist, forcerolls)
  showcategory("nonadvantaged", nonadvantagedlist, forcerolls)
  showcategory("advantaged"   , advantagedlist   , forcerolls)
  showcategory("unsighted"    , unsightedlist    , forcerolls)

  aplog.log("end of order of flight determination phase.")

      
#############################################################################
