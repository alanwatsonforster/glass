##############################################################################

import apxo.log as aplog
import apxo.hex as aphex

##############################################################################

def showvisualsighting(alist):

  aplog.log("visual sighting.")

  for a0 in alist:
    rlist = [visualsightingrange(a0, a1) for a1 in alist]
    zipped = sorted(list(zip(rlist, alist)), key=lambda x: x[0])
    for r, a1 in zipped:
      if a0._name != a1._name:
        aplog.log("range from %s to %s is %d." % (a1._name, a0._name, r))

##############################################################################

def visualsightingrange(a0, a1):

  """
  Return the visual sighting range from aircraft a0 to aircraft a1.
  """

  # See rule 11.1.

  x0 = a0._x
  y0 = a1._y
  x1 = a1._x
  y1 = a1._y

  horizontalrange = aphex.distance(x0, y0, x1, y1)

  altitude0 = a0._altitude
  altitude1 = a1._altitude

  if a0._altitude >= a1._altitude:
    verticalrange = int((a0._altitude - a1._altitude) / 2)
  else:
    verticalrange = int((a1._altitude - a0._altitude) / 4)

  return horizontalrange + verticalrange

##############################################################################

def inblindarc(a0, a1):

  """
  Return True if a1 is in the blind arc of a0.
  """

  # See rules 9.2 and 11.1.

  blindarcs = a0.blindarcs()

  if blindarcs == None:
    return True

  angleoff = target.angleofftail(attacker)
  if blindarcs == "30-":
    blindangloff = [ "0 line", "30 arc" ]
  elif arc == "60-":
    blindangloff = [ "0 line", "30 arc", "60 arc" ]
  elif blindarcs == "90-":
    blindangloff = [ "0 line", "30 arc", "60 arc", "90 arc" ]
  elif blindarcs == "120-":
    blindangloff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc" ]
  elif blindarcs == "150-":
    blindangloff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc", "150 arc" ]
  elif blindarcs == "180-":
    blindangloff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc", "150 arc", "180 arc", "180 line" ]
  else:
    raise RuntimeError("invalid arc %r." % arc)

  return angleoff in blindarcs

##############################################################################
