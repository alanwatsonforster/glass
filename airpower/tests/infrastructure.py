import airpower as ap
import airpower.log as aplog

from airpower import aircraft

def startfile(file):
  print("starting tests in file %s." % file)

def endfile(file):
  print("finished tests in file %s." % file)

aplog._silent = True

def _error(error):
  if aplog._error != error:
    print("expected error: %r" % error)
    print("actual   error: %r" % aplog._error)
    assert aplog._error == error

def startsetup(sheets=[["A1"],["A2"]], compassrose=1113, north="up", variants=[], verbose=False):
  aplog._silent = not verbose
  ap.startsetup(None, sheets=sheets, compassrose=compassrose, north=north, variants=variants)

def endsetup():
  ap.endsetup()

def startturn():
  ap.startturn()

def endturn():
  ap.endturn()