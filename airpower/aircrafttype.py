class aircrafttype:

  def __init__(self, name):
    self._name = name

  def powerchart(self, configuration):
    if self._name == "F-80C":
      return {
        "CL" : { "MIL": 1.0, },
        "1/2": { "MIL": 1.0, },
        "DT" : { "MIL": 1.0, },
      }[configuration]
    elif self._name == "F-84E":
      return {
        "CL" : { "MIL": 1.0, },
        "1/2": { "MIL": 0.5, },
        "DT" : { "MIL": 0.5, },
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
