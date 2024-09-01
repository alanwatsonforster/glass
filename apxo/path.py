import apxo.draw as apdraw


class path:

    def __init__(self, x, y, facing, altitude, speed):
        self.start(x, y, facing, altitude, speed)

    def start(self, x, y, facing, altitude, speed):
        self._x = [x]
        self._y = [y]
        self._facing = [facing]
        self._altitude = [altitude]
        self._speed = speed

    def extend(self, x, y, facing, altitude):
        self._x.append(x)
        self._y.append(y)
        self._facing.append(facing)
        self._altitude.append(altitude)

    def draw(self, color, annotate=True):
        apdraw.drawpath(
            self._x,
            self._y,
            self._facing,
            self._altitude,
            self._speed,
            color,
            annotate=annotate,
        )

    def xmin(self):
        return min(self._x)

    def xmax(self):
        return max(self._x)

    def ymin(self):
        return min(self._y)

    def ymax(self):
        return max(self._y)
