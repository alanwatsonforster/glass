import apxo.aircraft     as apaircraft
import apxo.capabilities as apcapabilities
import apxo.damage       as apdamage
import apxo.geometry     as apgeometry
import apxo.hex          as aphex
import apxo.log          as aplog
import apxo.math         as apmath

##############################################################################

def gunattackrange(attacker, target, arc=False):

  """
  Returns the range of an air-to-air gun attack from the attacker on the target
  or the reason the attack is forbidden.
  """

  # See rule 9.1 and the Air-to-Air Gun Attack diagram in the sheets.

  def horizontalrange(x0, y0, facing0, x1, y1, facing1):
    
    angleofftail, angleoffnose, r, dx, dy = apgeometry.relativepositions(x0, y0, facing0, x1, y1, facing1)

    if dx < 0:
      return False
    elif dx == 0:
      if dy == 0:
        return 0
      else:
        return False
    elif dx <= 1.0:
      if dy == 0:
        return 1
      else:
        return False
    elif dx < 1.5:
      if abs(dy) <= 0.5:
        return 1
      else:
        return False
    elif dx <= 2.2:
      if abs(dy) <= 0.5:
        return 2
      else:
        return False
    else:
      return False

  def verticalrange():
    return int(abs(attacker.altitude() - target.altitude()) / 2)

  if arc:

    rmin = False
    for facing in range(0, 361, 30):
      r = horizontalrange(
        attacker.x(), attacker.y(), facing, 
        target.x(), target.y(), target.facing()
      )
      if rmin is False:
        rmin = r
      elif r is not False:
        rmin = min(r, rmin)
    r = rmin

    if r is False:
      return "the target is not in the weapon range or arc."

    angleoff = apgeometry.angleofftail(target, attacker)
    if arc == "30-":
      allowedangleoff = [ "0 line", "30 arc" ]
    elif arc == "60-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc" ]
    elif arc == "90-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc" ]
    elif arc == "120-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc" ]
    elif arc == "150-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc", "150 arc" ]
    elif arc == "180-":
      allowedangleoff = [ "0 line", "30 arc", "60 arc", "90 arc", "120 arc", "150 arc", "180 arc", "180 line" ]
    else:
      raise RuntimeError("invalid arc %r." % arc)

    if not angleoff in allowedangleoff:
      return "the target is not in the weapon range or arc."
      
    r += verticalrange()
    if r > 2:
      return "the target is not in the weapon range or arc."
    else:
      return r
    
  else:
    
    r = horizontalrange(
      attacker.x(), attacker.y(), attacker.facing(), 
      target.x(), target.y(), target.facing()
    )

    if r is False:
      return "the target is not in the weapon range or arc."

    # Apply the relative altitude restrictions for climbing, diving, and level flight.
    if attacker.climbingflight() and attacker.altitude() > target.altitude():
      return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
    if attacker.divingflight() and attacker.altitude() < target.altitude():
      return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
    if attacker.levelflight():
      if r == 0 and attacker.altitude() != target.altitude():
        return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
      if r > 0 and abs(attacker.altitude() - target.altitude()) > 1:
        return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
        
    r += verticalrange()
    if r > 2:
      return "the target is not in the weapon range or arc."
    else:
      return r

##############################################################################

def rocketattackrange(attacker, target):

  # See rule 9.3.

  def verticalrange():
    return int(abs(attacker.altitude() - target.altitude()) / 2)
    
  if not apgeometry.inlimitedradararc(attacker, target):
    return "the target is not in the weapon range or arc."

  r = apgeometry.horizontalrange(attacker, target)

  # Apply the relative altitude restrictions for climbing, diving, and level flight.
  if attacker.climbingflight() and attacker.altitude() > target.altitude():
    return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
  if attacker.divingflight() and attacker.altitude() < target.altitude():
    return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
  if attacker.levelflight():
    if r == 0 and attacker.altitude() != target.altitude():
      return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
    if r > 0 and abs(attacker.altitude() - target.altitude()) > 1:
      return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
  
  r += verticalrange()
  if r == 0 or r > 4:
    return "the target is not in the weapon range or arc."
  else:
    return r

##############################################################################

def _attack(attacker, weapon, target, result, allowRK=True, allowSSGT=True):

  """
  Attack and aircraft with fixed guns, articulated guns, or rockets.
  """

  if attacker._ETrecoveryfp > 0:
    raise RuntimeError("attempt to use weapons in or while recovering from an ET.")
    
  if target is None:
    targetdescription = ""
  else:
    targetdescription = targetdescription = " on %s" % target.name()
    
  if weapon == "GN":

    attacker._logevent("gun air-to-air attack%s." % targetdescription)
    if attacker._gunammunition < 1.0:
      raise RuntimeError("available gun ammunition is %.1f." % attacker._gunammunition)

  elif weapon == "GNSS":

    attacker._logevent("snap-shot gun air-to-air attack%s." % targetdescription)
    if attacker._gunammunition < 0.5:
      raise RuntimeError("available gun ammunition is %.1f." % attacker._gunammunition)

  elif allowRK and weapon[0:2] == "RK":

    if not weapon[2:].isdigit():
      raise RuntimeError("invalid weapon %r." % weapon)
    rocketfactors = int(weapon[2:])
    attacker._logevent("rocket air-to-air attack with %d factors%s." % (rocketfactors, targetdescription))

    if attacker._rocketfactors < rocketfactors:
      raise RuntimeError("available rocket factors are %d." % attacker._rocketfactors)

  else:

    raise RuntimeError("invalid weapon %r." % weapon)

  if target is not None:

    if weapon == "GN" or weapon == "GNSS":
      if apcapabilities.gunarc(attacker) != None:
        attacker._logevent("gunnery arc is %s." % apcapabilities.gunarc(attacker))
      r = gunattackrange(attacker, target, arc=apcapabilities.gunarc(attacker))
    else:
      r = rocketattackrange(attacker, target)
    if isinstance(r, str):
        raise RuntimeError(r)      
    attacker._logevent("range is %d." % r)      
    attacker._logevent("angle-off-tail is %s." % apgeometry.angleofftail(attacker, target))

  if allowSSGT:
    interval = apmath.onethird(attacker._speed)
    attacker._logevent("SSGT interval is %.1f %s." % (interval, aplog.plural(interval, "FP", "FPs")))

  if attacker._BTrecoveryfp > 0:
    attacker._logevent("applicable turn rate is BT.")
  if attacker._rollrecoveryfp > 0:
    attacker._logevent("applicable turn rate is BT (for a roll).")
  elif attacker._HTrecoveryfp > 0:
    attacker._logevent("applicable turn rate is HT.")
  elif attacker._TTrecoveryfp > 0:
    attacker._logevent("applicable turn rate is TT.")
  else:
    attacker._logevent("no applicable turn rate.")
    
  if result == "":
    attacker._logevent("unspecified result.")
    attacker._unspecifiedattackresult += 1
  elif result == "A":
    attacker._logevent("aborted.")
  elif result == "M":
    attacker._logevent("missed.")
  elif result == "-":
    attacker._logevent("hit but inflicted no damage.")
  else:
    attacker._logevent("hit and inflicted %s damage." % result)
    if target != None:
      apdamage.takedamage(target, result)

  if result != "A":
    if weapon == "GN":
      attacker._gunammunition -= 1.0
    elif weapon == "GNSS":
      attacker._gunammunition -= 0.5
    else:
      attacker._rocketfactors -= rocketfactors

  if weapon == "GN" or weapon == "GNSS":
    attacker._logevent("%.1f gun ammunition remain." % attacker._gunammunition)
  else:
    attacker._logevent("%d rocket %s." % (attacker._rocketfactors, aplog.plural(attacker._rocketfactors, "factor remains", "factors remain")))
      
##############################################################################

def attack(attacker, weapon, target, result):

  """
  Attack an aircraft, with fixed guns, articulated guns, or rockets.
  """

  _attack(attacker, weapon, target, result)
      
##############################################################################

def react(attacker, weapon, target, result):

  """
  Return fire, with fixed guns or articulated guns.
  """

  return _attack(attacker, weapon, target, result, allowSSGT=False, allowRK=False)

##############################################################################

