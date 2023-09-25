import airpower.map    as apmap
import airpower.azimuth as apazimuth
import airpower.turn    as apturn

def startprolog(sheets, compassrose, north="up"):
  print("--- start prolog ---")
  apazimuth.setnorth(north)
  apmap.setmap(sheets, compassrose)
  apmap.drawmap()
  apturn.restart()
  print()

def endprolog():
  print("--- end prolog ---")
  print()