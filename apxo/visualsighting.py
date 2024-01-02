################################################################################

import apxo.capabilities as apcapabilities
import apxo.hex          as aphex
import apxo.geometry     as apgeometry
import apxo.log          as aplog

################################################################################

def maxvisualsightingrange(target):

  """
  Return the maximum visual sighting range of the target.
  """

  # See rule 11.1.
    
  return  4 * apcapabilities.visibility(target)

################################################################################

def maxvisualidentificationrange(target):

  """
  Return the maximum visual identification range of the target.
  """

  # See rule 11.5.
    
  return  2 * apcapabilities.visibility(target)

################################################################################

def visualsightingrange(searcher, target):

  """
  Return the visual sighting range for a search by searcher for target.
  """

  # See rule 11.1.

  horizontalrange = apgeometry.horizontalrange(searcher, target)

  if searcher.altitude() >= target.altitude():
    verticalrange = int((searcher.altitude() - target.altitude()) / 2)
  else:
    verticalrange = int((target.altitude() - searcher.altitude()) / 4)

  return horizontalrange + verticalrange

################################################################################

def visualsightingrangemodifier(searcher, target):

  """
  Return the visual sighting range modifier for a search by searcher for target.
  """

  # See rule 11.1 and the sheets.

  r = visualsightingrange(searcher, target)

  if r <= 3:
    return -2
  elif r <= 6:
    return -1
  elif r <= 9:
    return 0
  elif r <= 12:
    return +1
  elif r <= 15:
    return +2
  elif r <= 20:
    return +3
  elif r <= 30:
    return +5
  else:
    return +8

################################################################################

def visualsightingsearchersmodifier(searchers):

  """
  Return the visual sighting modifier for searchers beyond the first.
  """

  # See the sheets. 
  
  if searchers <= 2:
    return 0
  elif searchers <= 4:
    return -1
  elif searchers <= 8:
    return -2
  else:
    return -3

################################################################################

def isvalidpaintscheme(paintscheme):

  return paintscheme in [
    "silver", "aluminum", "aluminium", "unpainted",
    "uncamouflaged",
    "camouflaged",
    "lowvisibilitygray", "lowvisibilitygrey"
  ]
  
################################################################################

def visualsightingpaintschememodifier(searcher, target):

  """
  Return the visual sighting paint scheme modifier for a search by seacher for target.
  """

  paintscheme = target.paintscheme()

  # Map alternate names to standard names.
  paintscheme = {
    "unpainted"        : "unpainted",
    "silver"           : "unpainted",
    "aluminum"         : "unpainted",
    "aluminium"        : "unpainted",
    "uncamouflaged"    : "uncamouflaged",
    "camouflaged"      : "camouflaged",
    "lowvisibilitygray": "lowvisibilitygray",
    "lowvisibilitygrey": "lowvisibilitygray"

  }[paintscheme]

  if searcher.altitude() > target.altitude():
    # Target lower than searcher
    return {
      "unpainted"        : -2, 
      "uncamouflaged"    : -1, 
      "camouflaged"      : +1, 
      "lowvisibilitygray": +0
    }[paintscheme]
  elif searcher.altitude() == target.altitude():
    # Target level with searcher
    return {
      "unpainted"        : -1, 
      "uncamouflaged"    : +0, 
      "camouflaged"      : +0, 
      "lowvisibilitygray": +1
    }[paintscheme]
  else:
    # Target higher than searcher
    return {
      "unpainted"        : -1, 
      "uncamouflaged"    : +0, 
      "camouflaged"      : -1, 
      "lowvisibilitygray": +1
    }[paintscheme]

################################################################################

def visualsightingcrewmodifier(searcher):

  """
  Return the visual sighting crew modifier for a search by searcher.
  """

  # See rule 11.1 and the sheets.

  if len(searcher.crew()) > 1:
    return -1
  else:
    return +0
    
################################################################################

def visualsightingsmokingmodifier(searcher, target):

  """
  Return the visual sighting smoking modifier for a search by searcher for target.
  """

  # See rule 11.1 and the sheets.

  smoking = target.enginesmoking()

  if not smoking:
    return 0
  elif searcher.altitude() > target.altitude():
    # Target lower than searcher
    return -1
  elif searcher.altitude() == target.altitude():
    # Target level with searcher
    return -2
  else:
    # Target higher than searcher
    return -2
  
################################################################################

def visualsightingallrestrictedmodifier(allrestricted):

  """
  Return the visual sighting crew modifier for a search by searchers that are
  all restricted.
  """

  # See rule 11.1 and the sheets.

  if allrestricted:
    return +2
  else:
    return +0
    
################################################################################

def visualsightingcondition(searcher, target):

  """
  Return a tuple describing the visual sighting condition for a visual
  sighting attempt from searcher on the target: a descriptive string,
  a boolean indicating if sighting is possible, a boolean indicating if
  padlocking is possible, and a boolean indicating if the target is within
  range but in the searcher's restricted arc.
  """

  # See rule 11.1.

  blindarc      = _blindarc(searcher, target)
  restrictedarc = _restrictedarc(searcher, target)

  if visualsightingrange(searcher, target) > target.maxvisualsightingrange():
    return "beyond visual range", False, False, False
  elif apgeometry.samehorizontalposition(searcher, target) and searcher.altitude() > target.altitude():
    return "within visual range and can padlock, but blind (immediately below)", False, True, False
  elif apgeometry.samehorizontalposition(searcher, target) and searcher.altitude() < target.altitude():
    return "within visual range (immediately above)", True, True, False
  elif blindarc is not None:
    return "within visual range but blind (%s arc)" % blindarc, False, False, False
  elif restrictedarc is not None:
    return "within visual range but restricted (%s arc)" % restrictedarc, True, True, True
  else:
    return "within visual range", True, True, False
  
################################################################################

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

################################################################################

def _blindarc(searcher, target):

  """
  If the target is in the blind arcs of the searcher, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(searcher, target, apcapabilities.blindarcs(searcher))

################################################################################

def _restrictedarc(searcher, target):

  """
  If the target is in the restricted arcs of the searcher, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(searcher, target, apcapabilities.restrictedarcs(searcher))

################################################################################

def canidentify(searcher, target):

  """
  Return true if searcher can visually identify target, assuming target is
  sighted or padlocked.
  """

  # See rule 11.5.

  return visualsightingrange(searcher, target) <= maxvisualidentificationrange(target)
  
################################################################################

