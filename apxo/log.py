"""
Logging.
"""

import apxo.gameturn as apgameturn

################################################################################

_print = True
_writetofiles = True

def setprint(value):
    _print = value
    
def setwritetofiles(value):
    _writetofiles = value

################################################################################

"""

The log messages have one of these forms:

  TURN: WHAT
  TURN:                 : COMMENT
  TURN:                 : - NOTE

  TURN: WHO: WHAT
  TURN: WHO: WHEN: WHAT
  TURN: WHO:     :      : COMMENT
  TURN: WHO:     :      : - NOTE
"""


def _logline(line, who=None, writetofile=True):
    if _print:
        print(line)
    if _writetofiles and writetofile and who is not None:
        with open("log-%s.txt" % who, "a") as file:
            print(line, file=file)


def _logtext(text, who=None, writetofile=True):
    if apgameturn.gameturn() is None:
        line = "            : %s" % text
    elif apgameturn.gameturn() == 0:
        line = "set-up      : %s" % text
    else:
        line = "game turn %2d: %s" % (apgameturn.gameturn(), text)
    _logline(line, who=who, writetofile=writetofile)


def logwhat(what, who=None, writetofile=True):
    if who is None:
        line = what
    else:
        line = "%-5s : %s" % (who, what)
    _logtext(
        line,
        who=who,
        writetofile=writetofile,
    )


def logwhenwhat(when, what, who=None, writetofile=True):
    assert who is not None
    _logtext(
        "%-5s : %-5s : %s" % (who, when, what),
        who=who,
        writetofile=writetofile,
    )


def logcomment(comment, who=None, writetofile=True):
    if who is None:
        line = "%-5s   %-5s   %-32s : %s" % ("", "", "", comment)
    else:
        line = "%-5s : %-5s : %-32s : %s" % (who, "", "", comment)
    _logtext(
        line,
        who=who,
        writetofile=writetofile,
    )


def logbreak(who=None, writetofile=True):
    _logline("", who=who, writetofile=writetofile)


def lognote(note, who=None, writetofile=True):

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
            logcomment("- %s" % line, who=who, writetofile=writetofile)


_error = None


def clearerror():
    global _error
    _error = None


def logexception(e):
    global _error
    _error = str(e.args[0])
    logbreak()
    _logline("=== ERROR: %s ===" % _error)
    logbreak()


def plural(i, singular, plural):
    if i == 1:
        return singular
    else:
        return plural
