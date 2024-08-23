"""
Logging.
"""

import apxo.gameturn as apgameturn

_silent = False
_writefiles = True

def _filename(nameforfile):
   return "log-%s.txt" % nameforfile


def log(s, name=None, nameforfile=None):
    if _silent:
        return
    if apgameturn.gameturn() is None:
        line = s
    elif apgameturn.gameturn() == 0:
        line = "set-up      : %s" % s
    else:
        line = "game turn %2d: %s" % (apgameturn.gameturn(), s)
    print(line)
    if _writefiles:
        if nameforfile is not None:
            with open(_filename(nameforfile), "a") as file:
                print(line, file=file)

def logbreak(name=None, nameforfile=None):
    if _silent:
        return
    print()
    if name is not None:
        with open(_filename(name), "a") as file:
            print(file=file)

def logmain(s, name=None, nameforfile=None):
    log("%-4s : %s" % (name if name is not None else "", s), name=name, nameforfile=nameforfile)


def logcomment(s, name=None, nameforfile=None):
    log(
        "%-4s : %-5s : %-32s : %s" % (name if name is not None else "", "", "", s),
        name=name,
    )

def logaction(s, name=None, nameforfile=None):
    log("%-4s : %-5s : %s" % (name if name is not None else "", "", s), name=name, nameforfile=nameforfile)

def lognote(note, name=None, nameforfile=None):

    # This is adapted from the public-domain code in PEP 257.
    def splitandtrim(s):
        # Convert tabs to spaces (following the normal Python rules)
        # and split into a list of lines:
        lines = s.expandtabs().splitlines()
        # Determine minimum indentation (first line doesn't count):
        indent = None
        for line in lines[1:]:
            stripped = line.lstrip()
            if stripped:
                if indent is None:
                    indent = len(line) - len(stripped)
                else:
                    indent = min(indent, len(line) - len(stripped))
        # Remove indentation (first line is special):
        trimmed = [lines[0].strip()]
        if indent is not None:
            for line in lines[1:]:
                trimmed.append(line[indent:].rstrip())
        # Strip off trailing and leading blank lines:
        while trimmed and not trimmed[-1]:
            trimmed.pop()
        while trimmed and not trimmed[0]:
            trimmed.pop(0)
        # Return the lines.
        return trimmed

    if note is not None:
        for line in splitandtrim(note):
            logcomment("- %s" % line, name=name, nameforfile=nameforfile)


_error = None


def clearerror():
    global _error
    _error = None


def logexception(e):
    global _error
    _error = str(e.args[0])
    if _silent:
        return
    logbreak()
    log("=== ERROR: %s ===" % _error)
    logbreak()


def plural(i, singular, plural):
    if i == 1:
        return singular
    else:
        return plural
