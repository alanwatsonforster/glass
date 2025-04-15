################################################################################

import glass.element
import glass.log

################################################################################


class Marker(glass.element.Element):

    ############################################################################

    def __init__(
        self,
        type,
        hexcode,
        azimuth=0,
        speed=0,
        altitude=0,
        name=None,
        color="black",
        silent=False,
    ):

        self._name = ""

        try:

            if not isinstance(name, str) and name is not None:
                raise RuntimeError("the name argument must be a string or None.")

            if not type in ["dot", "circle", "square"]:
                raise RuntimeError("invalid marker type.")

            if not silent:
                if name is None:
                    self.logwhenwhat("", "creating %s marker." % type)
                else:
                    self.logwhenwhat("", "creating %s marker %s." % (type, name))

            super().__init__(
                name,
                hexcode=hexcode,
                azimuth=azimuth,
                altitude=altitude,
                speed=speed,
                color=color,
            )

            self._type = type

        except RuntimeError as e:
            glass.log.logexception(e)
        if not silent:
            self.logbreak()

    ############################################################################

    def ismarker(self):
        return True

    ############################################################################

    from glass.marker.draw import _draw

    ############################################################################
