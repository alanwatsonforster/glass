def sheets(scenario):

  sheets = {
    "TSOH:T-1" : [["A1"]],
    "TSOH:T-2" : [["C1"]],
    "TSOH:T-3" : [["C1", "C2"]],
    "TSOH:T-4" : [["A2", "C1", "B1"]],
    "TSOH:T-5" : [["C1"]],
    "TSOH:T-6" : [["B1"],["C1"],["B2"]],
    "TSOH:G-1" : [["B1"],["B2"]],
    "TSOH:G-2" : [["B1"],["C2"]],
    "TSOH:G-3" : [["A2","B2"],["A1","C1"]],
    "TSOH:K-1" : [["C2"],["C1"]],
    "TSOH:K-2" : [["C2"],["C1"]],
    "TSOH:K-3" : [["B1"],["C2"]],
    "TSOH:K-4" : [["A1"],["C1"],["C2"],["B1"]],
    "TSOH:K-5" : [["B1","C1"],["A1","B2"]],
    "TSOH:K-6" : [["A1"],["C1"]],
    "TSOH:K-7" : [["C2","B2","A2"]],
    "TSOH:K-8" : [["B2"]],
    "TSOH:K-9" : [["C1"]],
    "TSOH:K-10": [["B1","C1"],["C2","B2"]],
    "TSOH:CW-1": [["B1","C1"],["A1","B2"]],
    "TSOH:CW-2": [["C2","B2","A1"]],
    "TSOH:CW-3": [["C2","B2","A1"]],
    "TSOH:CW-4": [["A2"],["B1"],["B2"],["C1"]],
    "TSOH:CW-5": [["A1"],["C1"],["B2"]],
    "TSOH:V-1" : [["B1"],["C2"]],
    "TSOH:V-2" : [["B1"],["B2"]],
    "TSOH:V-3" : [["C1"],["C2"]],
    "TSOH:V-4" : [["B1"],["B2"]],
    "TSOH:V-5" : [["B1"],["C2"]],
    "TSOH:V-6" : [["C2"],["B1"],["B2"],["A1"]],
    "TSOH:V-7" : [["C1","B1"],["A1","B2"]],
    "TSOH:V-8" : [["A2"],["A1"],["C1"]],
    "TSOH:V-9" : [["C1","B1"],["B2","A2"]],
    "TSOH:V-10": [["A1"],["C1"],["B2"]],
    # V-11: sheet B2 is inverted.
    "TSOH:V-12": [["C1","C2"],["B1","A1"]],
    "TSOH:V-13": [["C1","--"],["B1","C2"],["A2","B2"],["A1","--"]],
    "TSOH:V-14": [["B1"],["B2"]],
    "TSOH:V-15": [["A1"]],
    "TSOH:V-16": [["A1"],["C2"]],
    "TSOH:V-17": [["C1"],["C2"]],
    "TSOH:V-18": [["B2"],["A1"]],
    "TSOH:V-19": [["A1","C2"],["B1","B2"]],
    "TSOH:V-20": [["C2","B1"],["A1","B2"]],
    "TSOH:V-21": [["B1","A1"],["B2","C2"]],
    # V-22: sheets C1 and C2 are inverted.
    "TSOH:V-23": [["B1"],["A2"],["A1"],["C1"]],
    "TSOH:V-24": [["--","B1"],["C2","A2"],["B2","A1"],["--","C1"]],
    # V-25: sheet C1 is twice.
    "TSOH:V-E" : [["B1","A1"]]
    
  }
  if not scenario in sheets:
    raise RuntimeError("%r is not a recognized scenario." % scenario)
  return sheets[scenario]

def north(scenario):
  left = ["TSOH:V-E"]
  if scenario in left:
    return "left"
  else:
    return "up"