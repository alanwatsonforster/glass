import apxo.aircraft as apaircraft
import apxo.geometry as apgeometry
import apxo.hex      as aphex

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
    return int(abs(attacker._altitude - target._altitude) / 2)

  if arc:

    rmin = False
    for facing in range(0, 361, 30):
      r = horizontalrange(
        attacker._x, attacker._y, facing, 
        target._x, target._y, target._facing
      )
      if rmin is False:
        rmin = r
      elif r is not False:
        rmin = min(r, rmin)
    r = rmin

    if r is False:
      return "the target is not in the weapon range or arc."

    angleoff = target.angleofftail(attacker)
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
      attacker._x, attacker._y, attacker._facing, 
      target._x, target._y, target._facing
    )

    if r is False:
      return "the target is not in the weapon range or arc."

    # Apply the relative altitude restrictions for climbing, diving, and level flight.
    if attacker.climbingflight() and attacker._altitude > target._altitude:
      return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
    if attacker.divingflight() and attacker._altitude < target._altitude:
      return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
    if attacker.levelflight():
      if r == 0 and attacker._altitude != target._altitude:
        return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
      if r > 0 and abs(attacker._altitude - target._altitude) > 1:
        return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
        
    r += verticalrange()
    if r > 2:
      return "the target is not in the weapon range or arc."
    else:
      return r

##############################################################################

def rocketattackrange(attacker, target):

  # See rule 9.3.

  def horizontalrange():
    return aphex.distance(attacker._x, attacker._y, target._x, target._y)

  def verticalrange():
    return int(abs(attacker._altitude - target._altitude) / 2)
    
  if not attacker.inlimitedradararc(target):
    return "the target is not in the weapon range or arc."

  r = horizontalrange()

  # Apply the relative altitude restrictions for climbing, diving, and level flight.
  if attacker.climbingflight() and attacker._altitude > target._altitude:
    return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
  if attacker.divingflight() and attacker._altitude < target._altitude:
    return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
  if attacker.levelflight():
    if r == 0 and attacker._altitude != target._altitude:
      return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
    if r > 0 and abs(attacker._altitude - target._altitude) > 1:
      return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
  
  r += verticalrange()
  if r == 0 or r > 4:
    return "the target is not in the weapon range or arc."
  else:
    return r

##############################################################################

def react(attacker, weapon, targetname, result):

  """
  Return fire, either with fixed guns or articulated guns.
  """

  if targetname == "":
    targetdescription = ""
  else:
    targetdescription = " on %s" % targetname
    
  if weapon == "GN":

    attacker._logevent("gun air-to-air attack%s." % targetdescription)
    if attacker._gunammunition < 1.0:
      raise RuntimeError("available gun ammunition is %.1f." % attacker._gunammunition)
    attacker._gunammunition -= 1.0

  elif weapon == "GNSS":

    attacker._logevent("snap-shot gun air-to-air attack%s." % targetdescription)
    if attacker._gunammunition < 0.5:
      raise RuntimeError("available gun ammunition is %.1f." % attacker._gunammunition)
    attacker._gunammunition -= 0.5

  else:

    raise RuntimeError("invalid weapon %r." % weapon)

  if attacker.gunarc() != None:
    attacker._logevent("gunnery arc is %s." % attacker.gunarc())

  if targetname != "":
    target = apaircraft._fromname(targetname)
    if target == None:
      raise RuntimeError("unknown target aircraft %s." % targetname)
    r = attacker.gunattackrange(target, arc=attacker.gunarc())
    if isinstance(r, str):
        raise RuntimeError(r)      
    attacker._logevent("range is %d." % r)     
    if attacker.gunarc != None: 
      attacker._logevent("angle-off-tail is %s." % target.angleofftail(attacker))
    else:
      attacker._logevent("angle-off-tail is %s." % attacker.angleofftail(target))

  if result == "":
    attacker._logevent("result of attack not specified.")
    attacker._unspecifiedattackresult += 1
  elif result == "M":
    attacker._logevent("missed.")
  elif result == "-":
    attacker._logevent("hit but inflicted no damage.")
  else:
    attacker._logevent("hit and inflicted %s damage." % result)
    if target != None:
      target._takedamage(result)

  attacker._logevent("%.1f gun ammunition remain" % attacker._gunammunition)

##############################################################################

