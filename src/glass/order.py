import glass.aircraft
import glass.gameturn
import glass.geometry
import glass.log

#############################################################################


def advantaged(A, B):
    """
    Return True if A is advantaged over B.
    """

    # See rule 12.2.

    # TODO: tailing.

    # Sighted.
    if not B.issighted():
        return False

    # Not same hex or hexside.
    if glass.geometry.samehorizontalposition(A, B):
        return False

    # In 150+ arc.
    if not glass.geometry.inarc(A, B, "150+"):
        return False

    # Within 9 hexes horizontally.
    if glass.geometry.horizontalrange(A, B) > 9:
        return False

    # No more than 6 altitude levels above.
    if B.altitude() > A.altitude() + 6:
        return False

    # No more than 9 altitude levels below.
    if B.altitude() < A.altitude() - 9:
        return False

    # Not below if in VC.
    if A.isinclimbingflight(vertical=True) and B.altitude() < A.altitude():
        return False

    # Not above if in VD.
    if A.isindivingflight(vertical=True) and B.altitude() > A.altitude():
        return False

    return True


#############################################################################


def disadvantaged(A, B):
    """
    Return True if A is disadvantaged by B.
    """

    # See rule 12.2.

    # This is equivalent to B being advantaged over A.

    return advantaged(B, A)


#############################################################################

_training = {}

_trainingmodifier = {
    "excellent": +2,
    "good": +1,
    "average": +0,
    "limited": -1,
    "poor": -2,
}


def settraining(training):

    global _training
    _training = training

    glass.log.logwhat("training.")
    for k, v in training.items():
        glass.log.logcomment(
            "training modifier is %+d (%s) for %s." % (_trainingmodifier[v], v, k)
        )


#############################################################################


def orderofflightdeterminationphase(rolls, firstkill=None, mostkills=None):

    def score(A):
        i = rolls[A.force()]
        if A.force() in _training:
            i += _trainingmodifier[_training[A.force()]]
        if A.force() == firstkill:
            i += 1
        if A.force() == mostkills:
            i += 1
        return i

    glass.log.logwhat("start of order of flight determination phase.")

    for k, v in rolls.items():
        glass.log.logcomment("roll is %2d for %s." % (v, k))
    for k, v in _training.items():
        glass.log.logcomment(
            "training   modifier is %+d (%s) for %s." % (_trainingmodifier[v], v, k),
        )
    if firstkill is not None:
        glass.log.logcomment("first kill modifier is +1 for %s." % firstkill)
    if mostkills is not None:
        glass.log.logcomment("most kills modifier is +1 for %s." % mostkills)

    for A in glass.aircraft.aslist():
        glass.log.logwhat("%s has a score of %d." % (A.name(), score(A)), name=A.name())

    unsightedlist = []
    advantagedlist = []
    disadvantagedlist = []
    nonadvantagedlist = []

    for A in glass.aircraft.aslist():

        # TODO: departed, stalled, and engaged.

        if not A.issighted():

            unsightedlist.append(A)
            category = "unsighted"

        else:

            isadvantaged = False
            isdisadvantaged = False
            for B in glass.aircraft.aslist():
                if A.force() != B.force():
                    if advantaged(A, B):
                        A.logcomment("is advantaged over %s." % B.name())
                        isadvantaged = True
                    elif disadvantaged(A, B):
                        A.logcomment("is disadvantaged by %s." % B.name())
                        isdisadvantaged = True

            if isadvantaged and not isdisadvantaged:
                advantagedlist.append(A)
                category = "advantaged"
            elif isdisadvantaged and not isadvantaged:
                disadvantagedlist.append(A)
                category = "disadvantaged"
            else:
                nonadvantagedlist.append(A)
                category = "nonadvantaged"

        glass.log.logwhat("%s is %s." % (A.name(), category), name=A.name())

    def showcategory(category, alist):
        adict = {}
        for A in alist:
            adict[score(A)] = []
        for A in alist:
            adict[score(A)].append(A.name())
        for k, v in sorted(adict.items()):
            glass.log.logwhat("  %s" % " ".join(v))

    glass.log.logwhat("")
    glass.log.logwhat("order of flight is:")
    glass.log.logwhat("")
    showcategory("disadvantaged", disadvantagedlist)
    showcategory("nonadvantaged", nonadvantagedlist)
    showcategory("advantaged", advantagedlist)
    showcategory("unsighted", unsightedlist)
    glass.log.logwhat(None, "")

    glass.log.logwhat("end of order of flight determination phase.")


#############################################################################
