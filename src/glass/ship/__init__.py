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
        speed=0,
        classification=None,
        maxspeed=None,
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
                speed=speed,
                color=color,
                azimuth=azimuth,
            )

            if classification not in [
                "smallwarship",
                "mediumwarship",
                "largewarship",
                "smallmerchantship",
                "mediummerchantship",
                "largemerchantship",
            ]:
                raise RuntimeError("the classification argument is invalid.")
            self._classification = classification

            if maxspeed is None or not (isinstance(maxspeed, (int, float))) or maxspeed < 0:
                raise RuntimeError("the maxspeed argument is invalid.")
            self._maxspeed = maxspeed
            
            self._stack = stack

            self._maneuvertype = None
            self._maneuversense = None
            self._maneuverfp = 0
            self._maneuverrequiredfp = 0

            self._HTrecoverygameturn = 0
            self._movegameturn = 0

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

    from glass.ship.draw import _draw
    from glass.ship.move import _move, _continuemove

    def _initattack(self):
        pass


################################################################################
