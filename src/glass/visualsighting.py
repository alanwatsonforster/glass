################################################################################

import glass.capabilities
import glass.hex
import glass.geometry
import glass.log

################################################################################


def startvisualsighting():
    """
    Report sighting status at the start of the visual sighting phase.
    """

    for target in glass.aircraft.aslist():
        if target._sightedonpreviousturn:
            glass.log.logwhat(
                "%-4s : was sighted on previous game turn." % target.name()
            )
        else:
            glass.log.logwhat(
                "%-4s : was unsighted on previous game turn." % target.name()
            )
        glass.log.logwhat(
            "%-4s : maximum visual range is %d."
            % (target.name(), target._maxvisualsightingrange())
        )
        for searcher in glass.aircraft.aslist():
            if target.name() != searcher.name() and target.force() != searcher.force():
                glass.log.logwhat(
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

    for target in glass.aircraft.aslist():
        if target._sighted and target._identified:
            glass.log.logwhat("%-4s : is sighted and identified." % target.name())
        elif target._sighted:
            glass.log.logwhat("%-4s : is sighted." % target.name())
        else:
            glass.log.logwhat("%-4s : is unsighted." % target.name())

    for target in glass.missile.aslist():
        if target._sighted and target._identified:
            glass.log.logwhat("%-4s : is sighted and identified." % target.name())
        elif target._sighted:
            glass.log.logwhat("%-4s : is sighted." % target.name())
        else:
            glass.log.logwhat("%-4s : is unsighted." % target.name())

    for target in glass.groundunit.aslist():
        if target._sighted and target._identified:
            glass.log.logwhat("%-4s : is sighted and identified." % target.name())
        elif target._sighted:
            glass.log.logwhat("%-4s : is sighted." % target.name())
        else:
            glass.log.logwhat("%-4s : is unsighted." % target.name())

    for target in glass.ship.aslist():
        if target._sighted and target._identified:
            glass.log.logwhat("%-4s : is sighted and identified." % target.name())
        elif target._sighted:
            glass.log.logwhat("%-4s : is sighted." % target.name())
        else:
            glass.log.logwhat("%-4s : is unsighted." % target.name())

    for searcher in glass.aircraft.aslist():
        searcher._sightinggroundunits = False


################################################################################


def sightgroundunits(A, note=None):
    A.logbreak()
    A.logwhat("sights ground units.")
    A._sightinggroundunits = True
    A.lognote(note)


################################################################################


def padlock(A, B, note=None):
    """
    Carry out a padlock on aircraft B by aircraft A
    """

    A.logbreak()

    A.logwhat("padlocks %s." % B.name())

    if not B._sightedonpreviousturn:
        raise RuntimeError("%s was not sighted on previous game turn." % (B.name()))

    A.logcomment("range is %d." % visualsightingrange(A, B))
    A.logcomment("%s." % visualsightingcondition(A, B)[0])

    condition, cansight, canpadlock, restricted = visualsightingcondition(A, B)
    if not canpadlock:
        raise RuntimeError("%s cannot padlock %s." % (A.name(), B.name()))

    B._sighted = True
    B._identified = B._identifiedonpreviousturn or canidentify(A, B)
    if B._identified:
        A.logwhat("%s is sighted and identified." % B.name())
    else:
        A.logwhat("%s is sighted but not identified." % B.name())

    A.lognote(note)


################################################################################


def sightaircraftormissile(
    A,
    B,
    sightingroll=None,
    sightingrollmodifier=None,
    identifyingroll=None,
    identifyingrollmodifier=None,
    incidentally=False,
    note=None,
):
    """
    Attempt to sight target aircraft B by searching aircraft A.

    If roll is None, simply report the sighting situation.

    If roll is not None, report the sighting situation, determine whether the
    sighting attempt has succeeded, and set the other aircraft as sighted or not
    sighted as appropriate.

    If the sighting attempt succeeds, determine whether the other aircraft is
    also identified. If so, set is as identified.

    :param A: The searching aircraft.
    :param B: The target aircraft or missile.
    :param sightingroll: If None, then simply report sighting situation. If
        True, affirm that the sighting attempt was successful. If False, affirm
        that the sighting attempt was not successful. If an integer, determine
        whether the sighting attempt was successful by comparing the modified
        value to the visibility of the aircraft being sighted. Defaults to None.
    :param sightingrollmodifier: If None, use the calculated modifier. If an
        integer, use the value as the modifier. Defaults to None.
    :param identifyingroll: This is purely for compatibility with sighting
        ground units. It must be None.
    :param identifyingrollmodifier: This is purely for compatibility with
        sighting ground units. It must be None.
    :param incidentally: Whether the sighting is incidental. Affects visual
        sighting condition evaluation. Defaults to ``False``.
    :param note: If a string, an additional note to be logged. If None, do
        nothing. Defaults to None.

    :return: None
    """

    A.logbreak()

    if identifyingroll is not None:
        raise RuntimeError(
            "the identifying roll should not be given when sighting aircraft or missiles."
        )
    if identifyingrollmodifier is not None:
        raise RuntimeError(
            "the identifying roll modifier should not be given when sighting aircraft or missiles."
        )

    if incidentally:
        A.logwhat("attempts to sight %s incidentally." % B.name())
    else:
        A.logwhat("attempts to sight %s." % B.name())
    A.logcomment("range is %d." % visualsightingrange(A, B))
    A.logcomment("%s." % visualsightingcondition(A, B)[0])

    condition, cansight, canpadlock, restricted = visualsightingcondition(
        A, B, incidentally=incidentally
    )
    if not cansight and sightingroll is not True:
        raise RuntimeError("%s cannot sight %s." % (A.name(), B.name()))

    if sightingrollmodifier is None:

        allrestricted = restricted

        additionalsearchers = 0
        for searcher in glass.aircraft.aslist():
            if searcher.name() != A.name() and searcher.force() == A.force():
                condition, cansight, canpadlock, restricted = visualsightingcondition(
                    searcher, B
                )
                A.logcomment(
                    "additional searcher %s: %s." % (searcher.name(), condition)
                )
                if cansight:
                    additionalsearchers += 1
                    allrestricted = allrestricted and restricted

        sightingrollmodifier = 0

        dmodifier = visualsightingrangemodifier(A, B)
        A.logcomment("range modifier         is %+d." % dmodifier)
        sightingrollmodifier += dmodifier

        dmodifier = visualsightingallrestrictedmodifier(allrestricted)
        A.logcomment("restricted modifier    is %+d." % dmodifier)
        sightingrollmodifier += dmodifier

        dmodifier = visualsightingsearchersmodifier(additionalsearchers + 1)
        A.logcomment(
            "searchers modifier     is %+d (%d)." % (dmodifier, additionalsearchers + 1)
        )
        sightingrollmodifier += dmodifier

        dmodifier = visualsightingpaintschememodifier(A, B)
        A.logcomment("paint-scheme modifier  is %+d." % dmodifier)
        sightingrollmodifier += dmodifier

        dmodifier = visualsightingcrewmodifier(A)
        if dmodifier != 0:
            A.logcomment("crew modifier          is %+d." % dmodifier)

        dmodifier = visualsightingsmokingmodifier(A, B)
        if dmodifier != 0:
            A.logcomment("smoking modifier       is %+d." % dmodifier)
        sightingrollmodifier += dmodifier

        A.logcomment("total modifier         is %+d." % sightingrollmodifier)

    elif isinstance(sightingrollmodifier, int):

        A.logcomment("sighting modifier is %+d." % sightingrollmodifier)

    else:

        raise RuntimeError('invalid sighting modifier "%r"' % sightingrollmodifier)

    visibility = glass.capabilities.visibility(B)

    if sightingroll is None:
        success = None
    elif sightingroll is False:
        A.logcomment("forcing failure.")
        success = False
    elif sightingroll is True:
        A.logcomment("forcing success.")
        success = True
    elif isinstance(sightingroll, int):
        A.logcomment("sighting roll          is %d." % sightingroll)
        A.logcomment(
            "modified sighting roll is %d." % (sightingroll + sightingrollmodifier)
        )
        success = (sightingroll + sightingrollmodifier) <= visibility
        if success:
            A.logcomment("attempt succeeds.")
        else:
            A.logcomment("attempt fails.")

    A.logcomment("target visibility      is %d." % visibility)

    if success is False:
        A.logwhat("%s is unsighted." % B.name())
    elif success is True:
        B._sighted = True
        B._identified = B._identifiedonpreviousturn or canidentify(A, B)
        if B._identified:
            A.logwhat("%s is sighted and identified." % B.name())
        else:
            A.logwhat("%s is sighted but not identified." % B.name())

    A.lognote(note)


################################################################################


def sightgroundunit(
    A,
    B,
    sightingroll=None,
    sightingrollmodifier=None,
    identifyingroll=None,
    identifyingrollmodifier=None,
    note=None,
):
    """
    Attempt to sight and identify target ground unit B by searching aircraft A.

    If roll is None, simply report the sighting situation.

    If roll is not None, report the sighting situation, determine whether the
    sighting attempt has succeeded, and set the target as sighted or not sighted
    as appropriate.

    :param A: The searching aircraft.
    :param B: The target ground unit.
    :param sightingroll: Defaults to None. This is the sighting roll for
        camouflaged units. Sighting is automatic for uncamouflaged units within
        range. If set to True or False, sighting is assumed to automatically
        succeed or fail, respectively. If set to None, carry out automatic
        sighting for uncamouflaged units but simply report the sighting
        situation for camouflaged units.
    :param identifyingroll: Defaults to None. This is the identifying roll. If
        set to True or False, identifying is assumed to automatically succeed or
        fail, respectively. If set to None ,simply report the identifying
        situation
    :param sightingrollmodifier: Defaults to None. The modifier applied to the
        sighting roll for camouflaged units. If None, the calculated modifier is
        used. Defaults to None.
    :param identifyingrollmodifier: Defaults to None. The modifier applied to
        the identifying roll. If None, the calculated modifier is used. Defaults
        to None.
    :param note: If a string, an additional note to be logged. If None, do
        nothing. Defaults to None.

    :return: None
    """

    def iscamouflaged():
        # This is just a placeholder.
        return False

    A.logbreak()

    if not A._sightinggroundunits:
        raise RuntimeError("%s is not sighting ground units." % A.name())
    if not B.isgroundunit():
        raise RuntimeError("%s is not a ground unit." % B.name())

    range = visualsightingrange(A, B)
    A.logcomment("range is %d." % range)

    A.logcomment("target sighting range is %d." % B.sightingrange())

    if sightingroll is True or sightingroll is False:

        A.logcomment("forcing sighting result.")
        sighted = sightingroll

    elif not iscamouflaged():

        sighted = range <= B.sightingrange()

    elif range > B.sightingrange():

        sighted = False

    else:

        if sightingrollmodifier is None:
            sightingrollmodifier = 0
        elif isinstance(sightingrollmodifier, int):
            A.logcomment("sighting roll modifier is %+d." % sightingrollmodifier)
        else:
            raise RuntimeError(
                'invalid sighting roll modifier "%r"' % sightingrollmodifier
            )

        if sightingroll is None:
            A.logcomment("sighting roll succeeds on %d-." % 5)
            sighted = False
        elif isinstance(sightingroll, int):
            A.logcomment(
                "sighting roll is %d against %d-."
                % (sightingroll + sightingrollmodifier, 5)
            )
            sighted = (sightingroll + sightingrollmodifier) <= 5
        else:
            raise RuntimeError('invalid sighting roll "%r"' % sightingroll)

    if B.isidentified():

        identified = True

    elif not sighted:

        identified = False

    elif identifyingroll is True or identifyingroll is False:

        A.logcomment("forcing identifying result.")
        identified = identifyingroll

    elif range >= 10:

        A.logcomment("target identifying range is %d." % 9)
        identified = False

    else:

        if identifyingrollmodifier is None:
            identifyingrollmodifier = 0
        elif isinstance(identifyingrollmodifier, int):
            A.logcomment("identifying roll modifier is %+d." % identifyingrollmodifier)
        else:
            raise RuntimeError(
                'invalid identifying roll modifier "%r"' % identifyingrollmodifier
            )

        A.logcomment("identifying roll succeeds on %d-." % (10 - range))
        if identifyingroll is None and range < 10:
            identified = False
        elif isinstance(identifyingroll, int):
            A.logcomment("identifying roll is %d." % (identifyingroll))
            A.logcomment(
                "modified identifying roll is %d."
                % (identifyingroll + identifyingrollmodifier)
            )
            identified = (identifyingroll + identifyingrollmodifier) <= 10 - range
        else:
            raise RuntimeError('invalid identifying roll "%r"' % identifyingroll)

    if not sighted:
        A.logwhat("%s is unsighted." % B.name())
    elif not identified:
        B.becomesighted()
        A.logwhat("%s is sighted but not identified." % B.name())
    else:
        B.becomesighted()
        B.becomeidentified()
        A.logwhat("%s is sighted and identified." % B.name())

    A.lognote(note)


################################################################################


def issighted(A):
    """
    Return True is the aircraft A is sighted, otherwise return False.
    """
    return A._sighted


################################################################################


def maxvisualsightingrange(A):
    """
    Return the maximum visual sighting range of the target A.
    """

    # See rule 11.1.

    return 4 * glass.capabilities.visibility(A)


################################################################################


def maxvisualidentificationrange(A):
    """
    Return the maximum visual identification range of the target A.
    """

    # See rule 11.5.

    return 2 * glass.capabilities.visibility(A)


################################################################################


def visualsightingrange(A, B):
    """
    Return the visual sighting range for a search by searcher A for target B.
    """

    # See rule 11.1.

    horizontalrange = glass.geometry.horizontalrange(A, B)

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


def visualsightingcondition(A, B, incidentally=False):
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

    if A._sightinggroundunits and not incidentally:
        return "sighting ground units", False, False, False
    elif incidentally and A.altitude() < B.altitude():
        return "lower", False, False, False
    elif visualsightingrange(A, B) > maxvisualsightingrange(B):
        return "beyond visual range", False, False, False
    elif glass.geometry.samehorizontalposition(A, B) and A.altitude() > B.altitude():
        return (
            "within visual range and can padlock, but blind (immediately below)",
            False,
            True,
            False,
        )
    elif glass.geometry.samehorizontalposition(A, B) and A.altitude() < B.altitude():
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

    angleoff = glass.geometry.angleofftail(B, A, arconly=True)

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

    return _arc(A, B, glass.capabilities.blindarcs(A))


################################################################################


def _restrictedarc(A, B):
    """
    If the target B is in the restricted arcs of the searcher A, return the arc.
    Otherwise return None.
    """

    # See rules 9.2 and 11.1.

    return _arc(A, B, glass.capabilities.restrictedarcs(A))


################################################################################


def canidentify(A, B):
    """
    Return true if the searcher A can visually identify the target B, assuming
    target is sighted or padlocked.
    """

    # See rule 11.5.

    return visualsightingrange(A, B) <= maxvisualidentificationrange(B)


################################################################################
