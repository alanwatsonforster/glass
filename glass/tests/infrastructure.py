import apxo as ap
import apxo.log

from apxo import setupaircraft, setupgroundunit, drawmap

import os.path


def startfile(file, description):
    print("running tests in file %s: %s." % (os.path.basename(file), description))
    apxo.log.setprint(False)
    apxo.log.setwritefiles(False)


def endfile(file):
    apxo.log.setprint(True)
    apxo.log.setwritefiles(True)


def asserterror(error):
    if apxo.log._error != error:
        print("expected error: %r" % error)
        print("actual   error: %r" % apxo.log._error)
        assert apxo.log._error == error


def starttestsetup(
    sheets=[["A1"], ["A2"]],
    north="up",
    variants=[],
    verbose=False,
    **kwargs
):
    ap.startgamesetup(
        None,
        sheets=sheets,
        north=north,
        variants=variants,
        writelogfiles=False,
        printlog=verbose,
        **kwargs
    )


def endtestsetup():
    ap.endgamesetup()


def startgameturn():
    ap.startgameturn()


def endgameturn():
    ap.endgameturn()
