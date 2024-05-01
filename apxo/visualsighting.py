################################################################################

import apxo.capabilities as apcapabilities
import apxo.hex as aphex
import apxo.geometry as apgeometry
import apxo.log as aplog

################################################################################


def startvisualsighting():
    """
    Report sighting status at the start of the visual sighting phase.
    """

    for target in apaircraft.aslist():
        aplog.logbreak()
        if target._sightedonpreviousturn:
            aplog.log("%-4s : was sighted on previous turn." % target.name())
        else:
            aplog.log("%-4s : was unsighted on previous turn." % target.name())
        aplog.log(
            "%-4s : maximum visual range is %d."
            % (target.name(), target.maxvisualsightingrange())
        )
        for searcher in aslist():
            if target.name() != searcher.name() and target.force() != searcher.force():
                aplog.log(
                    "%-4s : searcher %s: range is %2d: %s."
                    % (
                        target.name(),
                        searcher.name(),
                        visualsightingrange(searcher, target),
                        visualsightingcondition(searcher, target)[0],
                    )
                )


################################################################################


def endvisualsighting():
    """
    Report sighting status at the end of the visual sighting phase.
    """

    aplog.logbreak()
    for target in apaircraft.aslist():
        if target._sighted and target._identified:
            aplog.log("%-4s : is sighted and identified." % target.name())
        elif target._sighted:
            aplog.log("%-4s : is sighted." % target.name())
        else:
            aplog.log("%-4s : is unsighted." % target.name())


################################################################################


def padlock(A, B, note=False):
    """
    Carry out a padlock on aircraft B by aircraft A
    """

    A._logbreak()
    A._logline()

    A._log("padlocks %s." % B.name())

    if not B._sightedonpreviousturn:
        raise RuntimeError("%s was not sighted on previous turn." % (B.name()))

    A._logevent("range is %d." % visualsightingrange(A, B))
    A._logevent("%s." % visualsightingcondition(A, B)[0])

    condition, cansight, canpadlock, restricted = visualsightingcondition(A, B)
    if not canpadlock:
        raise RuntimeError("%s cannot padlock %s." % (A.name(), B.name()))

    B._sighted = True
    B._identified = B._identifiedonpreviousturn or canidentify(A, B)
    if B._identified:
        A._log("%s is sighted and identified." % B.name())
    else:
        A._log("%s is sighted but not identified." % B.name())

    A._lognote(note)
    A._logline()


################################################################################


def attempttosight(A, B, success=None, note=False):
    """
    Carry out an attempt to sight on aircraft B by aircraft A.
    """

    A._logbreak()
    A._logline()

    A._log("attempts to sight %s." % B.name())
    A._logevent("range is %d." % visualsightingrange(A, B))
    A._logevent("%s." % visualsightingcondition(A, B)[0])

    condition, cansight, canpadlock, restricted = visualsightingcondition(A, B)
    if not cansight:
        raise RuntimeError("%s cannot sight %s." % (A.name(), B.name()))

    allrestricted = restricted

    additionalsearchers = 0
    for searcher in aslist():
        if searcher.name() != A.name() and searcher.force() == A.force():
            condition, cansight, canpadlock, restricted = visualsightingcondition(
                searcher, B
            )
            A._logevent("additional searcher %s: %s." % (searcher.name(), condition))
            if cansight:
                additionalsearchers += 1
                allrestricted = allrestricted and restricted
    if additionalsearchers == 0:
        A._logevent("no additional searchers.")
    else:
        A._logevent(
            "%d additional %s."
            % (
                additionalsearchers,
                aplog.plural(additionalsearchers, "searcher", "searchers"),
            )
        )

    modifier = 0

    dmodifier = visualsightingrangemodifier(A, B)
    A._logevent("range modifier        is %+d." % dmodifier)
    modifier += dmodifier

    dmodifier = visualsightingallrestrictedmodifier(allrestricted)
    A._logevent("restricted modifier   is %+d." % dmodifier)
    modifier += dmodifier

    dmodifier = visualsightingsearchersmodifier(additionalsearchers + 1)
    A._logevent("searchers modifier    is %+d." % dmodifier)
    modifier += dmodifier

    dmodifier = visualsightingpaintschememodifier(A, B)
    A._logevent("paint-scheme modifier is %+d." % dmodifier)
    modifier += dmodifier

    dmodifier = visualsightingcrewmodifier(A)
    if dmodifier != 0:
        A._logevent("crew modifier         is %+d." % dmodifier)

    dmodifier = visualsightingsmokingmodifier(A, B)
    if dmodifier != 0:
        A._logevent("smoking modifier      is %+d." % dmodifier)
    modifier += dmodifier

    A._logevent("total modifier        is %+d." % modifier)
    A._logevent("target visibility is %d." % apcapabilities.visibility(B))

    A._lognote(note)

    if success is False:
        A._log("%s is unsighted." % B.name())
    elif success is True:
        B._sighted = True
        B._identified = B._identifiedonpreviousturn or canidentify(A, B)
        if B._identified:
            A._log("%s is sighted and identified." % B.name())
        else:
            A._log("%s is sighted but not identified." % B.name())

    A._logline()


################################################################################


def issighted(A):
    """
    Return True is the aircraft A is sighted, otherwise return False.
    """
    return A._sighted


################################################################################


def setsighted(A):
    """
    Set the aircraft A to be sighted.
    """
    A._sighted = True


################################################################################


def setunsighted(A):
    """
    Set the aircraft A to be unsighted.
    """
    A._sighted = False


################################################################################


def maxvisualsightingrange(A):
    """
    Return the maximum visual sighting range of the target A.
    """

    # See rule 11.1.

    return 4 * apcapabilities.visibility(A)


################################################################################


def maxvisualidentificationrange(A):
    """
    Return the maximum visual identification range of the target A.
    """

    # See rule 11.5.

    return 2 * apcapabilities.visibility(A)


################################################################################


def visualsightingrange(A, B):
    """
    Return the visual sighting range for a search by searcher A for target B.
    """

    # See rule 11.1.

    horizontalrange = apgeometry.horizontalrange(A, B)

    if A.altitude() >= B.altitude():
        verticalrange = int((A.altitude() - B.altitude()) / 2)
    else:
        verticalrange = int((B.altitude() - A.altitude()) / 4)

    return horizontalrange + verticalrange


################################################################################


def visualsightingrangemodifier(A, B):
    """
    Return the visual sighting range modifier for a search by searcher A
    for target B.
    """

    # See rule 11.1 and the sheets.

    r = visualsightingrange(A, B)

    if r <= 3:
        return -2
    elif r <= 6:
        return -1
    elif r <= 9:
        return 0
    elif r <= 12:
        return +1
    elif r <= 15:
        return +2
    elif r <= 20:
        return +3
    elif r <= 30:
        return +5
    else:
        return +8


################################################################################


def visualsightingsearchersmodifier(searchers):
    """
    Return the visual sighting modifier for searchers beyond the first.
    """

    # See the sheets.

    if searchers <= 2:
        return 0
    elif searchers <= 4:
        return -1
    elif searchers <= 8:
        return -2
    else:
        return -3


################################################################################


def isvalidpaintscheme(paintscheme):

    return paintscheme in [
        "silver",
        "aluminum",
        "aluminium",
        "unpainted",
        "uncamouflaged",
        "camouflaged",
        "lowvisibilitygray",
        "lowvisibilitygrey",
    ]


################################################################################


def visualsightingpaintschememodifier(A, B):
    """
    Return the visual sighting paint scheme modifier for a search by
    seacher A for target B.
    """

    paintscheme = B.paintscheme()

    # Map alternate names to standard names.
    paintscheme = {
        "unpainted": "unpainted",
        "silver": "unpainted",
        "aluminum": "unpainted",
        "aluminium": "unpainted",
        "uncamouflaged": "uncamouflaged",
        "camouflaged": "camouflaged",
        "lowvisibilitygray": "lowvisibilitygray",
        "lowvisibilitygrey": "lowvisibilitygray",
    }[paintscheme]

    if A.altitude() > B.altitude():
        # Target lower than searcher
        return {
            "unpainted": -2,
            "uncamouflaged": -1,
            "camouflaged": +1,
            "lowvisibilitygray": +0,
        }[paintscheme]
    elif A.altitude() == B.altitude():
        # Target level with searcher
        return {
            "unpainted": -1,
            "uncamouflaged": +0,
            "camouflaged": +0,
            "lowvisibilitygray": +1,
        }[paintscheme]
    else:
        # Target higher than searcher
        return {
            "unpainted": -1,
            "uncamouflaged": +0,
            "camouflaged": -1,
            "lowvisibilitygray": +1,
        }[paintscheme]


################################################################################


def visualsightingcrewmodifier(A):
    """
    Return the visual sighting crew modifier for a search by searcher A.
    """

    # See rule 11.1 and the sheets.

    if len(A.crew()) > 1:
        return -1
    else:
        return +0


################################################################################


def visualsightingsmokingmodifier(A, B):
    """
    Return the visual sighting smoking modifier for a search by searcher A
    for target B.
    """

    # See rule 11.1 and the sheets.

    smoking = B.enginesmoking()

    if not smoking:
        return 0
    elif A.altitude() > B.altitude():
        # Target lower than searcher
        return -1
    elif A.altitude() == B.altitude():
        # Target level with searcher
        return -2
    else:
        # Target higher than searcher
        return -2


################################################################################


def visualsightingallrestrictedmodifier(allrestricted):
    """
    Return the visual sighting crew modifier for a search by searchers that are
    all restricted.
    """

    # See rule 11.1 and the sheets.

    if allrestricted:
        return +2
    else:
        return +0


################################################################################


def visualsightingcondition(A, B):
    """
    Return a tuple describing the visual sighting condition for a visual
    sighting attempt from searcher A on the target B: a descriptive string,
    a boolean indicating if sighting is possible, a boolean indicating if
    padlocking is possible, and a boolean indicating if the target is within
    range but in the searcher's restricted arc.
    """

    # See rule 11.1.

    blindarc = _blindarc(A, B)
    restrictedarc = _restrictedarc(A, B)

    if visualsightingrange(A, B) > maxvisualsightingrange(B):
        return "beyond visual range", False, False, False
    elif apgeometry.samehorizontalposition(A, B) and A.altitude() > B.altitude():
        return (
            "within visual range and can padlock, but blind (immediately below)",
            False,
            True,
            False,
        )
    elif apgeometry.samehorizontalposition(A, B) and A.altitude() < B.altitude():
        return "within visual range (immediately above)", True, True, False
    elif blindarc is not None:
        return "within visual range but blind (%s arc)" % blindarc, False, False, False
    elif restrictedarc is not None:
        return (
            "within visual range but restricted (%s arc)" % restrictedarc,
            True,
            True,
            True,
        )
    else:
        return "within visual range", True, True, False


################################################################################


def _arc(A, B, arcs):
    """
    If the target B is in the specified arcs of the searcher A, return the arc.
    Otherwise return None.
    """

    angleoff = apgeometry.angleofftail(B, A, arconly=True)

    for arc in arcs:
        if arc == "30-" or arc == "60L":
            angleoffs = ["30 arc"]
        elif arc == "60-" or arc == "60L":
            angleoffs = ["30 arc", "60 arc"]
        elif arc == "90-" or arc == "90L":
            angleoffs = ["30 arc", "60 arc", "90 arc"]
        elif arc == "180L":
            angleoffs = ["180 arc"]
        else:
            raise RuntimeError("invalid arc %r." % arc)
        lower = arc[-1] == "L"
        if lower and A.altitude() <= B.altitude():
            continue
        if angleoff in angleoffs:
            return arc

    return None


################################################################################


def _blindarc(A, B):
    """
    If the target B is in the blind arcs of the searcher A, return the arc.
    Otherwisereturn None.
    """

    # See rules 9.2 and 11.1.

    return _arc(A, B, apcapabilities.blindarcs(A))


################################################################################


def _restrictedarc(A, B):
    """
    If the target B is in the restricted arcs of the searcher A, return the arc.
    Otherwise return None.
    """

    # See rules 9.2 and 11.1.

    return _arc(A, B, apcapabilities.restrictedarcs(A))


################################################################################


def canidentify(A, B):
    """
    Return true if the searcher A can visually identify the target B, assuming
    target is sighted or padlocked.
    """

    # See rule 11.5.

    return visualsightingrange(A, B) <= maxvisualidentificationrange(B)


################################################################################
