import glass as ap
import glass.log

from glass import setupaircraft, setupgroundunit, drawmap

import os.path


def startfile(file, description):
    print("running tests in file %s: %s." % (os.path.basename(file), description))
    glass.log.setprint(False)
    glass.log.setwritefiles(False)


def endfile(file):
    glass.log.setprint(True)
    glass.log.setwritefiles(True)


def asserterror(error):
    if glass.log._error != error:
        print("expected error: %r" % error)
        print("actual   error: %r" % glass.log._error)
        assert glass.log._error == error


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
