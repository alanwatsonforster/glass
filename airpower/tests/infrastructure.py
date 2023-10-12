import airpower as ap
import airpower.log as aplog

from airpower import aircraft

import os.path

aplog._silent = True

def startfile(file, description):
  print("running tests in file %s: %s." % (os.path.basename(file), description))

def endfile(file):
  pass

def asserterror(error):
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