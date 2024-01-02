################################################################################

import apxo.capabilities as apcapabilities
import apxo.hex          as aphex
import apxo.geometry     as apgeometry
import apxo.log          as aplog

################################################################################

def maxvisualsightingrange(A):

  """
  Return the maximum visual sighting range of the target A.
  """

  # See rule 11.1.
    
  return 4 * apcapabilities.visibility(A)

################################################################################

def maxvisualidentificationrange(A):

  """
  Return the maximum visual identification range of the target A.
  """

  # See rule 11.5.
    
  return 2 * apcapabilities.visibility(A)

################################################################################

def visualsightingrange(A, B):

  """
  Return the visual sighting range for a search by searcher A for target B.
  """

  # See rule 11.1.

  horizontalrange = apgeometry.horizontalrange(A, B)

  if A.altitude() >= B.altitude():
    verticalrange = int((A.altitude() - B.altitude()) / 2)
  else:
    verticalrange = int((B.altitude() - A.altitude()) / 4)

  return horizontalrange + verticalrange

################################################################################

def visualsightingrangemodifier(A, B):

  """
  Return the visual sighting range modifier for a search by searcher A for target B.
  """

  # See rule 11.1 and the sheets.

  r = visualsightingrange(A, B)

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

def visualsightingpaintschememodifier(A, B):

  """
  Return the visual sighting paint scheme modifier for a search by seacher A for target B.
  """

  paintscheme = B.paintscheme()

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

  if A.altitude() > B.altitude():
    # Target lower than searcher
    return {
      "unpainted"        : -2, 
      "uncamouflaged"    : -1, 
      "camouflaged"      : +1, 
      "lowvisibilitygray": +0
    }[paintscheme]
  elif A.altitude() == B.altitude():
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

def visualsightingcrewmodifier(A):

  """
  Return the visual sighting crew modifier for a search by searcher A.
  """

  # See rule 11.1 and the sheets.

  if len(A.crew()) > 1:
    return -1
  else:
    return +0
    
################################################################################

def visualsightingsmokingmodifier(A, B):

  """
  Return the visual sighting smoking modifier for a search by searcher A for target B.
  """

  # See rule 11.1 and the sheets.

  smoking = B.enginesmoking()

  if not smoking:
    return 0
  elif A.altitude() > B.altitude():
    # Target lower than searcher
    return -1
  elif A.altitude() == B.altitude():
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

def visualsightingcondition(A, B):

  """
  Return a tuple describing the visual sighting condition for a visual
  sighting attempt from searcher A on the target B: a descriptive string,
  a boolean indicating if sighting is possible, a boolean indicating if
  padlocking is possible, and a boolean indicating if the target is within
  range but in the searcher's restricted arc.
  """

  # See rule 11.1.

  blindarc      = _blindarc(A, B)
  restrictedarc = _restrictedarc(A, B)

  if visualsightingrange(A, B) > B.maxvisualsightingrange():
    return "beyond visual range", False, False, False
  elif apgeometry.samehorizontalposition(A, B) and A.altitude() > B.altitude():
    return "within visual range and can padlock, but blind (immediately below)", False, True, False
  elif apgeometry.samehorizontalposition(A, B) and A.altitude() < B.altitude():
    return "within visual range (immediately above)", True, True, False
  elif blindarc is not None:
    return "within visual range but blind (%s arc)" % blindarc, False, False, False
  elif restrictedarc is not None:
    return "within visual range but restricted (%s arc)" % restrictedarc, True, True, True
  else:
    return "within visual range", True, True, False
  
################################################################################

def _arc(A, B, arcs):

  """
  If the target B is in the specified arcs of the searcher A, return the arc. Otherwise
  return None.
  """
  
  angleoff = B.angleofftail(A, arconly=True)

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
    if lower and A.altitude() <= B.altitude():
      continue
    if angleoff in angleoffs:
      return arc

  return None

################################################################################

def _blindarc(A, B):

  """
  If the target B is in the blind arcs of the searcher A, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(A, B, apcapabilities.blindarcs(A))

################################################################################

def _restrictedarc(A, B):

  """
  If the target B is in the restricted arcs of the searcher A, return the arc. Otherwise
  return None.
  """

  # See rules 9.2 and 11.1.

  return _arc(A, B, apcapabilities.restrictedarcs(A))

################################################################################

def canidentify(A, B):

  """
  Return true if the searcher A can visually identify the target B, assuming target is
  sighted or padlocked.
  """

  # See rule 11.5.

  return visualsightingrange(A, B) <= maxvisualidentificationrange(B)
  
################################################################################

