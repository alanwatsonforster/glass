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
  arc = apgeometry.angleofftail(b, a, arconly=True)
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

_training = {}

_trainingmodifier = {
  "excellent": +2,
  "good"     : +1,
  "average"  : +0,
  "limited"  : -1,
  "poor"     : -2
}

def settraining(training):

  global _training
  _training = training

  aplog.logbreak()
  aplog.log("training.")
  for k, v in training.items():
    aplog.logcomment(None, "training modifier is %+d (%s) for %s." % (
      _trainingmodifier[v],
      v,
      k
    ))

#############################################################################

def orderofflightdeterminationphase(
  rolls,
  firstkill=None,
  mostkills=None
  ):

  def score(a):
    i = rolls[a.force()]
    if a.force() in _training:
      i += _trainingmodifier[_training[a.force()]]
    if a.force() == firstkill:
      i += 1
    if a.force() == mostkills:
      i += 1
    return i
    
  aplog.logbreak()
  aplog.log("start of order of flight determination phase.")

  for k, v in rolls.items():
    aplog.logcomment(None, "roll is %2d for %s." % (v, k))
  for k, v in _training.items():
    aplog.logcomment(None, "training   modifier is %+d (%s) for %s." % (
      _trainingmodifier[v],
      v,
      k
    ))
  if firstkill is not None:
    aplog.logcomment(None, "first kill modifier is +1 for %s." % firstkill)
  if mostkills is not None:
    aplog.logcomment(None, "most kills modifier is +1 for %s." % mostkills)

  for a in apaircraft.aslist():
    aplog.logaction(a, "%s has a score of %d." % (a.name(), score(a)))

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

    aplog.logaction(a, "%s is %s." % (a.name(), category))

  def showcategory(category, alist):
    adict = {}
    for a in alist:
      adict[score(a)] = []
    for a in alist:
      adict[score(a)].append(a.name())
    for k, v in sorted(adict.items()):
      aplog.logaction(None, "  %s" % " ".join(v))

  aplog.logaction(None, "")
  aplog.logaction(None, "order of flight is:")
  aplog.logaction(None, "")
  showcategory("disadvantaged", disadvantagedlist)
  showcategory("nonadvantaged", nonadvantagedlist)
  showcategory("advantaged"   , advantagedlist   )
  showcategory("unsighted"    , unsightedlist    )
  aplog.logaction(None, "")

  aplog.log("end of order of flight determination phase.")

      
#############################################################################
