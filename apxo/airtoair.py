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
  Return the range of an air-to-air gun attack from the attacker on the target
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
    if attacker.isinclimbingflight() and attacker.altitude() > target.altitude():
      return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
    if attacker.isindivingflight() and attacker.altitude() < target.altitude():
      return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
    if attacker.isinlevelflight():
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

def issamehexattack(attacker, target):

  """
  Return true if the attacker and target are in the same hex.
  """

  return (attacker.x() == target.x()) and (attacker.y() == target.y())

##############################################################################

def rocketattackrange(attacker, target):

  """
  Return the range of an air-to-air rocket attack from the attacker on the target
  or the reason the attack is forbidden.
  """
  
  # See rule 9.3.

  def verticalrange():
    return int(abs(attacker.altitude() - target.altitude()) / 2)
    
  if not apgeometry.inlimitedradararc(attacker, target):
    return "the target is not in the weapon range or arc."

  r = apgeometry.horizontalrange(attacker, target)

  # Apply the relative altitude restrictions for climbing, diving, and level flight.
  if attacker.isinclimbingflight() and attacker.altitude() > target.altitude():
    return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
  if attacker.isindivingflight() and attacker.altitude() < target.altitude():
    return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
  if attacker.isinlevelflight():
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

    angleofftail = apgeometry.angleofftail(attacker, target)
    attacker._logevent("angle-off-tail is %s." % angleofftail)
    if angleofftail == "0 line":
      angleofftailmodifier = -2
    elif angleofftail == "30 arc":
      angleofftailmodifier = +0
    elif angleofftail == "60 arc":
      angleofftailmodifier = +2
    elif angleofftail == "90 arc" or angleofftail == "120 arc" or angleofftail == "150 arc":
      angleofftailmodifier = +4
    elif angleofftail == "180 arc":
      angleofftailmodifier = +3
    elif angleofftail == "180 line":
      angleofftailmodifier = +2
    attacker._logevent("angle-off-tail     modifier is %+d." % angleofftailmodifier)

    if angleofftail != "0 line" and angleofftail != "30 arc" and angleofftail != "60 arc":
      allowSSGT = False
      
    if (weapon == "GN" or weapon == "GNSS") and issamehexattack(attacker, target):
      # See rule 9.2 with errata. Note that the rules do not give a vertical 
      # modifier for an attacker in level flight with a target in climbing or
      # diving flight.
      if attacker.isinclimbingflight():
        if target.isinclimbingflight():
          verticalmodifier = +0
        elif target.isinlevelflight():
          verticalmodifier = +1
        else:
          verticalmodifier = +2
      elif attacker.isinlevelflight():
        verticalmodifier = +0
      else:
        if target.isinclimbingflight():
          verticalmodifier = +2
        elif target.isinlevelflight():
          verticalmodifier = +1
        else:
          verticalmodifier = +0    
      attacker._logevent("same-hex vertical  modifier is %+d." % verticalmodifier)

    attacker._logevent("target size        modifier is %+d." % apcapabilities.sizemodifier(target))

  if apdamage.damageatleast(attacker, "C"):
    damagemodifier = +3
  elif apdamage.damageatleast(attacker, "H"):
    damagemodifier = +2
  elif apdamage.damageatleast(attacker, "L"):
    damagemodifier = +1
  else:
    damagemodifier = +0
  attacker._logevent("attacker damage    modifier is %+d." % damagemodifier)
  
  if allowSSGT:
    interval = apmath.onethird(attacker._speed)
    attacker._logevent("SSGT interval is %.1f %s." % (interval, aplog.plural(interval, "FP", "FPs")))
  else:
    attacker._logevent("SSGT not allowed.")

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

