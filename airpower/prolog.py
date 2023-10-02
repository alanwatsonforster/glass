import airpower.aircraft as apaircraft
import airpower.azimuth  as apazimuth
import airpower.log      as aplog
import airpower.map      as apmap
import airpower.turn     as apturn
import airpower.variants as apvariants

def startprolog(sheets, compassrose, north="up", variants=[]):
  aplog.log("--- start prolog ---")
  aplog.logbreak()
  apvariants.setvariants(variants)
  aplog.logbreak()
  apmap.setmap(sheets, compassrose)
  aplog.logbreak()
  apazimuth.setnorth(north)
  aplog.logbreak()

  apmap.drawmap()
  apturn.restart()
  apaircraft._restart()

def endprolog():
  aplog.log("--- end prolog ---")
  aplog.logbreak()