import json

class aircraftdata:

  def __init__(self, name):
    self._name = name
    # TODO: Look for the file using a relative path.
    filename = "/content/src/airpower/aircraftdata/%s.json" % name
    # TODO: Handle errors.
    self._name = name
    self._data = json.load(open(filename, "r", encoding="utf-8"))
    assert name == self._data["name"]

  def power(self, configuration, setting):
    if not setting in self._data["powertable"][configuration]:
      return None
    else:
      return self._data["powertable"][configuration][setting]

  def spbr(self, configuration):
    return self._data["powertable"][configuration]["SPBR"]

  def fuelrate(self, setting):
    if not setting in self._data["powertable"]["FUEL"]:
      return None
    else:
      return self._data["powertable"]["FUEL"][setting]
  
  def turnrates(self, configuration):
    return ["EZ"] + list(self._data["turndragtable"][configuration].keys())

  def turndrag(self, configuration, turnrate):
    if not turnrate in self._data["turndragtable"][configuration]:
      return None
    else:
      return self._data["turndragtable"][configuration][turnrate]

  def minspeed(self, configuration, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if self._data["minspeedtable"][configuration][altitudeband] == 0.0:
      return None
    else:
      return self._data["minspeedtable"][configuration][altitudeband]

  def maxspeed(self, configuration, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if self._data["maxspeedtable"][configuration][altitudeband] == 0.0:
      return None
    else:
      return self._data["maxspeedtable"][configuration][altitudeband]
  
  def cruisespeed(self):
    return self._data["cruisespeed"]

  def climbspeed(self):
    return self._data["climbspeed"]

  def maxdivespeed(self, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if self._data["maxdivespeedtable"][altitudeband] == 0.0:
      return None
    else:
      return self._data["maxdivespeedtable"][altitudeband]

  def ceiling(self, configuration):
    return self._data["ceilingtable"][configuration]

  def rollhfp(self):
    return self._data["maneuvertable"]["LR/DR"]["HFP"]

  def rolldrag(self, rolltype):
    assert rolltype in [ "VR", "LR", "DR" ]
    if rolltype != "VR":
      rolltype = "LR/DR"
    return self._data["maneuvertable"][rolltype]["DP"]
    
  def hasproperty(self, p):
    return p in self._data["properties"]

  def climbcapability(self, configuration, altitudeband, powersetting):
    if powersetting == "AB":
      climbcapacity = self._data["climbcapabilitytable"][configuration][altitudeband]["AB"]
    else:
      climbcapacity = self._data["climbcapabilitytable"][configuration][altitudeband]["Other"]
    if climbcapacity == 0:
      return None
    else:
      return climbcapacity


  def print(self):

    def f1(x):
      if x == None:
        return "---"
      else:
        return "%.1f" % x

    def f1z(x):
      if x == 0:
        return "---"
      else:
        return "%.1f" % x
        
    def f0(x):
      if x == None:
        return "--"
      else:
        return "%2.0f" % x

    print("%s" % self._name)
    print()

    print("Power:")
    print()
    print("       CL   1/2  DT  Fuel")
    print("AB     %s  %s  %s  %s" % (
      f1(self.power("CL", "AB")), 
      f1(self.power("1/2", "AB")), 
      f1(self.power("DT", "AB")), 
      f1(self.fuelrate("AB"))
    ))
    print("M      %s  %s  %s  %s" % (
      f1(self.power("CL", "M" )), 
      f1(self.power("1/2", "M" )), 
      f1(self.power("DT", "M" )), 
      f1(self.fuelrate("M"))
    ))
    print("N      %s  %s  %s  %s" % (
      f1(self.power("CL", "N" )), 
      f1(self.power("1/2", "N" )), 
      f1(self.power("DT", "N" )), 
      f1(self.fuelrate("N"))
    ))
    print("I      %s  %s  %s  %s" % (
      f1(self.power("CL", "I")), 
      f1(self.power("1/2", "I")), 
      f1(self.power("DT", "I")), 
      f1(self.fuelrate("I"))
    ))
    print("SPBR   %s  %s  %s" % (
      f1(self.spbr("CL")), 
      f1(self.spbr("1/2")), 
      f1(self.spbr("DT"))
    ))
    print()

    print("Maneuver:")
    print()
    print("LR/DR  %s  %s" % (
      f1(self.rollhfp()), f1(self.rolldrag("LR"))
    ))
    print("VR     %s  %s" % (
      f1(0.0), f1(self.rolldrag("VR"))
    ))
    print()

    print("Turn:")
    print()
    print("       CL   1/2  DT")
    for turnrate in ["TT", "HT", "BT", "ET"]:
      print("%s     %s  %s  %s" % (
        turnrate,
        f1(self.turndrag("CL" , turnrate)),
        f1(self.turndrag("1/2", turnrate)),
        f1(self.turndrag("DT" , turnrate)),
      ))
    print()

    print("Speed and Ceiling:")
    print()
    print("      CL       1/2      DT")
    print("      %s       %s       %s" % (
      f0(self.ceiling("CL")),
      f0(self.ceiling("1/2")),
      f0(self.ceiling("DT")),
    ))
    for band in ["EH", "VH", "HI", "MH", "ML", "LO"]:
      print("%s    %s-%s  %s-%s  %s-%s  %s" % (
        band,
        f1(self.minspeed("CL" , band)), f1(self.maxspeed("CL" , band)),
        f1(self.minspeed("1/2", band)), f1(self.maxspeed("1/2", band)),
        f1(self.minspeed("DT" , band)), f1(self.maxspeed("DT" , band)),
        f1(self.maxdivespeed(band))
      ))
    print()
    print("Cruise: %.1f" % self.cruisespeed())
    print("Climb : %.1f" % self.climbspeed())
    print()

    print("Climb Capability:")
    print()
    print("      CL       1/2      DT")
    for band in ["EH", "VH", "HI", "MH", "ML", "LO"]:
      print("%s    %s %s  %s %s  %s %s" % (
        band,
        f1(self.climbcapability("CL" , band, "AB")), f1(self.climbcapability("CL" , band, "M")),
        f1(self.climbcapability("1/2", band, "AB")), f1(self.climbcapability("1/2", band, "M")),
        f1(self.climbcapability("DT" , band, "AB")), f1(self.climbcapability("DT" , band, "M")),
      ))
    print()

    s = ""
    for p in self._data["properties"]:
      s += " %s" % p
    print("Properties:%s" %s)
    print()


