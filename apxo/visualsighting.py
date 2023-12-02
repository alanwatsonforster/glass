##############################################################################

import apxo.log      as aplog
import apxo.hex      as aphex
import apxo.geometry as apgeometry

##############################################################################

def showvisualsighting(alist):

  for target in alist:
    aplog.logbreak()
    aplog.log("%-4s: maximum visual range is %d." % (target.name(), target.maxvisualsightingrange()))
    for searcher in alist:
      if target.name() != searcher.name():
        aplog.log("%-4s: searcher %s: range is %2d: %s." % (
          target.name(), searcher.name(), 
          visualsightingrange(searcher, target), 
          visualsightingcondition(searcher, target)
        ))

##############################################################################

def maxvisualsightingrange(target):

  """
  Return the maximum visual sighting range of the target.
  """

  # See rule 11.1.
    
  return  4 * target.visibility()

##############################################################################

def visualsightingrange(searcher, target):

  """
  Return the visual sighting range for a search by searcher for target.
  """

  # See rule 11.1.

  horizontalrange = aphex.distance(target.x(), target.y(), searcher.x(), searcher.y())

  if searcher.altitude() >= target.altitude():
    verticalrange = int((searcher.altitude() - target.altitude()) / 2)
  else:
    verticalrange = int((target.altitude() - searcher.altitude()) / 4)

  return horizontalrange + verticalrange

##############################################################################

def visualsightingcondition(searcher, target):

  """
  Return a string describing the visual sighting condition for a search by
  searcher for target.
  """

  # See rule 11.1.

  if  apgeometry.samehorizontalposition(searcher, target):
    # I'm confused by the rules for determining arcs if two aircraft are in
    # the same hex, so for the time being I assume blind and restricted arcs
    # do not apply in this case.
    blindarc = None
    restrictedarc = None
  else:
    blindarc      = _blindarc(searcher, target)
    restrictedarc = _restrictedarc(searcher, target)

  if visualsightingrange(searcher, target) > target.maxvisualsightingrange():
    return "beyond visual range"
  elif apgeometry.samehorizontalposition(searcher, target) and searcher.altitude() > target.altitude():
    return "within visual range and can padlock, but blind (immediately below)"
  elif apgeometry.samehorizontalposition(searcher, target) and searcher.altitude() < target.altitude():
    return "within visual range (immediately above)"
  elif blindarc is not None:
    return "within visual range but blind (%s arc)" % blindarc
  elif restrictedarc is not None:
    return "within visual range but restricted (%s arc)" % restrictedarc
  else:
    return "within visual range"

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

##############################################################################

def _blindarc(searcher, target):

  """
  If the target is in the blind arcs of the searcher, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(searcher, target, searcher.blindarcs())

##############################################################################

def _restrictedarc(searcher, target):

  """
  If the target is in the restricted arcs of the searcher, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(searcher, target, searcher.restrictedarcs())

##############################################################################
