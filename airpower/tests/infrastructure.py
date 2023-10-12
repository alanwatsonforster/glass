import airpower as ap
import airpower.log as aplog

from airpower import aircraft

def startfile(file):
  print("starting tests in file %s." % file)

def endfile(file):
  print("finished tests in file %s." % file)

def startsetup(sheets=[["A1"],["A2"]], compassrose=1113, north="up", variants=[], verbose=False):
  aplog._donotlog   = not verbose
  ap.startsetup(None, sheets=sheets, compassrose=compassrose, north=north, variants=variants)

def endsetup():
  ap.endsetup()

def startturn(error=None):
  ap.startturn()
  if aplog._error != error:
    print("expected error: %r" % error)
    print("actual   error: %r" % aplog._error)
    assert aplog._error == error

def endturn(error=None):
  ap.endturn()
  if aplog._error != error:
    print("expected error: %r" % error)
    print("actual   error: %r" % aplog._error)
    assert aplog._error == error

def checkaircraft(a, position, speed):
  if aplog._error != None:
    print("unexpected error: %r" % aplog._error)
    assert aplog._error == None
  if a.position() != position:
    print("expected position: %r" % position)
    print("actual   position: %r" % a.position())
    assert a.position() == position
  if a._speed != speed:
    print("expected speed: %r" % speed)
    print("actual   speed: %r" % a._speed)
    assert a._speed == speed

def checkaircrafterror(a, error):
  if aplog._error != error:
    print("expected error: %r" % error)
    print("actual   error: %r" % aplog._error)
    assert aplog._error == error

def moveandcheck(a, flighttype, power, actions, position, speed, flamedoutengines=0):
  a.move(flighttype, power, actions, flamedoutengines=flamedoutengines)
  checkaircraft(a, position, speed)

def moveanderror(a, flighttype, power, actions, error, flamedoutengines=0):
  a.move(flighttype, power, actions, flamedoutengines=flamedoutengines)
  checkaircrafterror(a, error)
