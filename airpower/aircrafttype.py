import json

class aircrafttype:

  def __init__(self, name):
    self._name = name
    # TODO: Look for the file using a relative path.
    filename = "/content/src/airpower/aircrafttypes/%s.json" % name
    # TODO: Handle errors.
    self._data = json.load(open(filename, "r", encoding="utf-8"))
    assert name == self._data["name"]

  def power(self, configuration, setting):
    if not setting in self._data["powertable"][configuration]:
      return None
    else:
      return self._data["powertable"][configuration][setting]

  def SPBR(self, configuration):
    return self._data["powertable"][configuration]["SPBR"]

  def fuelrate(self, setting):
    if not setting in self._data["powertable"]["FUEL"]:
      return None
    else:
      return self._data["powertable"]["FUEL"][setting]
  
  def turndrag(self, configuration, turnrate):
    if not turnrate in self._data["turndragtable"][configuration]:
      return None
    else:
      return self._data["turndragtable"][configuration][turnrate]

  def minspeed(self, configuration, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if not altitudeband in self._data["minspeedtable"][configuration]:
      return None
    else:
      return self._data["minspeedtable"][configuration][altitudeband]

  def maxspeed(self, configuration, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    return self._data["maxspeedtable"][configuration][altitudeband]
  
  def cruisespeed(self):
    return self._data["cruisespeed"]

  def climbspeed(self):
    return self._data["climbspeed"]

  def maxdivespeed(self, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if not altitudeband in self._data["maxdivespeedtable"]:
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
      rolltype == "LR/DR"
    return self._data["maneuvertable"][rolltype]["DP"]
    
  def hasproperty(self, p):
    return p in self._data["properties"]

  def turnrates(self, configuration):
    return ["EZ"] + list(self._data["turndragtable"][configuration].keys())

  def climbcapability(self, configuration, altitudeband, powersetting):
    if powersetting == "AB":
      climbcapacity = self._data["climbcapabilitytable"][configuration][altitudeband]["AB"]
    else:
      climbcapacity = self._data["climbcapabilitytable"][configuration][altitudeband]["Other"]
    if climbcapacity == 0:
      return None
    else:
      return climbcapacity
