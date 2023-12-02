##############################################################################

import apxo.log as aplog
import apxo.hex as aphex

##############################################################################

def showvisualsighting(alist):

  aplog.logbreak()
  aplog.log("visual sighting.")

  for target in alist:
    aplog.log("target %s:" % target.name())
    maxr = 4 * target.visibility()
    aplog.log("maximum visbible sighting range is %d." % maxr)
    for searcher in alist:
      if target.name() == searcher.name():
        continue
      r = visualsightingrange(searcher, target)
      blindarc      = _blindarc(searcher, target)
      restrictedarc = _restrictedarc(searcher, target)
      if blindarc is not None:
        aplog.log("target %s: searcher %s: blind (%s arc)." % (target.name(), searcher.name(), blindarc))
      elif restrictedarc is not None:
        aplog.log("target %s: searcher %s: range is %d but restricted (%s arc)." % (target.name(), searcher.name(), r, restrictedarc))
      else:
        aplog.log("target %s: searcher %s: range is %d." % (target.name(), searcher.name(), r))

##############################################################################

def visualsightingrange(searcher, target):

  """
  Return the visual sighting range from aircraft a0 to aircraft a1.
  """

  # See rule 11.1.

  horizontalrange = aphex.distance(target.x(), target.y(), searcher.x(), searcher.y())

  if searcher.altitude() >= target.altitude():
    verticalrange = int((searcher.altitude() - target.altitude()) / 2)
  else:
    verticalrange = int((target.altitude() - searcher.altitude()) / 4)

  return horizontalrange + verticalrange

##############################################################################

def _arc(searcher, target, arcs):

  """
  If the target is in the specified arcs of the searcher, return the arc. Otherwise
  return None.
  """
  
  angleoff = target.angleofftail(searcher, arconly=True)

  for arc in arcs:
    if arc == "30-" or arc == "60L":
      angleoffs = [ "30 arc" ]
    elif arc == "60-" or arc == "60L":
      angleoffs = [ "30 arc", "60 arc" ]
    elif arc == "90-" or arc == "90L":
      angleoffs = [ "30 arc", "60 arc", "90 arc" ]
    elif arc == "180L":
      angleoffs = [ "180 arc" ]
    else:
      raise RuntimeError("invalid arc %r." % arc)
    lower = (arc[-1] == "L")
    if lower and searcher.altitude() <= target.altitude():
      continue
    if angleoff in angleoffs:
      return arc

  return None

def _blindarc(searcher, target):

  """
  If the target is in the blind arcs of the searcher, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(searcher, target, searcher.blindarcs())

def _restrictedarc(searcher, target):

  """
  If the target is in the restricted arcs of the searcher, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(searcher, target, searcher.restrictedarcs())

##############################################################################
