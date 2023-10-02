import airpower.aircraft as apaircraft
import airpower.map      as apmap

def drawmap():
  apmap.drawmap()
  apaircraft._alldraw()

from airpower.prolog   import startprolog, endprolog
from airpower.turn     import startturn, endturn
from airpower.aircraft import aircraft