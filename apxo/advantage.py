import apxo.aircraft as apaircraft
import apxo.geometry as apgeometry

def advantaged(a0, a1):

  """
  Return True if a0 is advantaged over a1.
  """

  # See rule 12.2.

  # TODO: tailing.

  # Sighted.
  if not a1.sighted():
    return False

  # Not same hex.
  if apgeometry.samehorizontalposition(a0, a1):
    return False

  # In 150 or 180 arc.
  arc = apgeometry.angleofftail(a0, a1, arconly=True)
  if arc != "150 arc" and arc != "180 arc":
    return False

  # Within 9 hexes horizontally.
  if apgeometry.horizontalrange(a0, a1) > 9:
    return False

  # No more than 6 altitude levels above.
  if a1.altitude() > a0.altitude() + 6:
    return False

  # No more than 9 altitude levels below.
  if a1.altitude() < a0.altitude() - 9:
    return False

  # Not below if in VC.
  if a0.climbingflight(vertical=True) and a1.altitude() < a0.altitude():
    return False

  # Not above if in VD.
  if a0.divingflight(vertical=True) and a1.altitude() > a0.altitude():
    return False

  return True

def disadvantaged(a0, a1):

  """
  Return True if a0 is disadvantaged by a1.
  """

  # See rule 12.2.

  # This is equivalent to a1 being advantaged over a0.
  
  return advantaged(a1, a0)
