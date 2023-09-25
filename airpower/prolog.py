import airpower.azimuth as apazimuth
import airpower.log     as aplog
import airpower.map     as apmap
import airpower.turn    as apturn

def startprolog(sheets, compassrose, north="up"):
  aplog.log("--- start prolog ---")
  aplog.logbreak()
  apmap.setmap(sheets, compassrose)
  apazimuth.setnorth(north)
  apmap.drawmap()
  apturn.restart()
  aplog.logbreak()

def endprolog():
  aplog.log("--- end prolog ---")
  aplog.logbreak()