################################################################################

import apxo.element as apelement
import apxo.log as aplog

################################################################################


class marker(apelement.element):

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
            aplog.logexception(e)
        if not silent:
            self.logbreak()

    ############################################################################

    def ismarker(self):
        return True

    ############################################################################

    from apxo.marker.draw import _draw

    ############################################################################
