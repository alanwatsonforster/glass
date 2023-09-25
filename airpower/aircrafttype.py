class aircrafttype:

  def __init__(self, name):
    self._name = name

  def powerchart(self, configuration):
    if self._name == "F-80C":
      return {
        "CL"  : { "IDLE": 0.5, "NOR": 0.0, "MIL": 1.0, "SPBR": 0.5, },
        "1/2" : { "IDLE": 0.5, "NOR": 0.0, "MIL": 1.0, "SPBR": 0.5, },
        "DT"  : { "IDLE": 0.5, "NOR": 0.0, "MIL": 1.0, "SPBR": 0.5, },
        "FUEL": { "IDLE": 0.0, "NOR": 0.5, "MIL": 1.0, }
      }[configuration]
    elif self._name == "F-84E":
      return {
        "CL"  : { "IDLE": 0.5, "NOR": 0.0, "MIL": 1.0, "SPBR": 0.5, },
        "1/2" : { "IDLE": 0.5, "NOR": 0.0, "MIL": 0.5, "SPBR": 0.5, },
        "DT"  : { "IDLE": 0.5, "NOR": 0.0, "MIL": 0.5, "SPBR": 1.0, },
        "FUEL": { "IDLE": 0.0, "NOR": 0.5, "MIL": 1.0, }
      }[configuration]    

  def turndragchart(self, configuration):
    if self._name == "F-80C":
      return {
        "CL" : { "TT": 0.0, "HT": 1.0, "BT": 1.0, },
        "1/2": { "TT": 0.0, "HT": 1.0, "BT": 1.0, },
        "DT" : { "TT": 0.0, "HT": 1.0, "BT": 2.0, },
      }[configuration]
    elif self._name == "F-84E":
      return {
        "CL" : { "TT": 0.0, "HT": 1.0, "BT": 2.0, },
        "1/2": { "TT": 1.0, "HT": 2.0, "BT": 2.0, },
        "DT" : { "TT": 1.0, "HT": 2.0, "BT": 2.0, },
      }[configuration]

  def minspeed(self, configuration, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if self._name == "F-80C":
      return {
        "CL" : { "LO": 1.5, "ML": 1.5, "MH": 2.0, "HI": 2.0, "VH": 2.5, "EH": 0.0, },
        "1/2": { "LO": 1.5, "ML": 2.0, "MH": 2.0, "HI": 2.5, "VH": 2.5, "EH": 0.0, },
        "DT" : { "LO": 2.0, "ML": 2.0, "MH": 2.5, "HI": 2.5, "VH": 0.0, "EH": 0.0, },
      }[configuration][altitudeband]
    elif self._name == "F-84E":
      return {
        "CL" : { "LO": 1.5, "ML": 1.5, "MH": 2.0, "HI": 2.5, "VH": 2.5, "EH": 0.0, },
        "1/2": { "LO": 1.5, "ML": 2.0, "MH": 2.0, "HI": 2.5, "VH": 2.5, "EH": 0.0, },
        "DT" : { "LO": 2.0, "ML": 2.0, "MH": 2.5, "HI": 0.0, "VH": 0.0, "EH": 0.0, },
      }[configuration][altitudeband]

  def maxspeed(self, configuration, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if self._name == "F-80C":
      return {
        "CL" : { "LO": 5.5, "ML": 5.5, "MH": 5.0, "HI": 4.5, "VH": 4.0, "EH": 0.0, },
        "1/2": { "LO": 5.5, "ML": 5.0, "MH": 4.5, "HI": 4.5, "VH": 4.0, "EH": 0.0, },
        "DT" : { "LO": 5.0, "ML": 4.5, "MH": 4.5, "HI": 4.0, "VH": 0.0, "EH": 0.0, },
      }[configuration][altitudeband]
    elif self._name == "F-84E":
      return {
        "CL" : { "LO": 6.0, "ML": 6.0, "MH": 5.5, "HI": 5.5, "VH": 5.5, "EH": 0.0, },
        "1/2": { "LO": 5.5, "ML": 5.5, "MH": 5.5, "HI": 5.0, "VH": 5.0, "EH": 0.0, },
        "DT" : { "LO": 5.5, "ML": 5.0, "MH": 5.5, "HI": 0.0, "VH": 0.0, "EH": 0.0, },
      }[configuration][altitudeband]
  
  def cruisespeed(self):
    if self._name == "F-80C":
      return 4.0
    elif self._name == "F-84E":
      return 4.5

  def climbspeed(self):
    if self._name == "F-80C":
      return 3.0
    elif self._name == "F-84E":
      return 3.5

  def divespeed(self, altitudeband):
    if altitudeband == "UH":
      altitudeband = "EH"
    if self._name == "F-80C":
      return { "LO": 6.5, "ML": 6.5, "MH": 6.5, "HI": 6.5, "VH": 6.0, "EH": 0.0, }[altitudeband]
    elif self._name == "F-84E":
      return { "LO": 7.0, "ML": 7.0, "MH": 6.5, "HI": 6.5, "VH": 6.0, "EH": 0.0, }[altitudeband]

  def ceiling(self, configuration):
    if self._name == "F-80C":
      return { "CL": 45, "1/2": 40, "DT": 35, }[configuration]
    elif self._name == "F-84E":
      return { "CL": 41, "1/2": 36, "DT": 30, }[configuration]

  def hasproperty(self, p):
    if self._name == "F-80C":
      return p in ["HTD"]
    elif self._name == "F-84E":
      return p in ["HTD"]
