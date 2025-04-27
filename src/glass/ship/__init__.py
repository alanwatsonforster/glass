import glass.element
import glass.gameturn
import glass.log

################################################################################


def aslist(withkilled=False):
    elementlist = glass.element.aslist()
    shiplist = filter(lambda E: E.isship(), elementlist)
    if not withkilled:
        shiplist = filter(lambda x: not x.killed(), shiplist)
    return list(shiplist)


################################################################################

class Ship(glass.element.Element):

    ############################################################################

    def __init__(
        self,
        name,
        hexcode,
        azimuth,
        large=False,
        stack=None,
        color="white",
    ):

        self._name = ""

        try:

            if not isinstance(name, str):
                raise RuntimeError("the name argument must be a string.")
            self.logwhenwhat("", "creating ship %s." % name)

            super().__init__(
                name,
                hexcode=hexcode,
                altitude=None,
                speed=0,
                color=color,
                azimuth=azimuth,
            )

            self._large = large
            self._stack = stack

            self._initattack()
            self._inittracking()

        except RuntimeError as e:
            glass.log.logexception(e)
        self.logbreak()

    ############################################################################

    def isship(self):
        return True

    ############################################################################

    def _properties(self):
        return []

    ############################################################################

    def _endgameturn(self):
        return

    ############################################################################

    from glass.ship.draw import _draw
    from glass.ship.move import _move, _continuemove

    def _initattack(self):
        pass

################################################################################
