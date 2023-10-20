import apengine as ap
import apengine.log as aplog

from apengine import aircraft

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

def starttestsetup(sheets=[["A1"],["A2"]], north="up", variants=[], verbose=False):
  aplog._silent = not verbose
  ap.starttestsetup(None, sheets=sheets, north=north, variants=variants)

def endtestsetup():
  ap.endsetup()

def startturn():
  ap.startturn()

def endturn():
  ap.endturn()