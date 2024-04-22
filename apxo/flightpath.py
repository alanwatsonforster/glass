import apxo.draw as apdraw

class flightpath:

  def __init__(self, x, y):
    self.start(x, y)

  def start(self, x, y):
    self._x = [x]
    self._y = [y]

  def next(self, x, y):
    self._x.append(x)
    self._y.append(y)

  def draw(self, color, zorder):
    apdraw.drawflightpath(self._x, self._y, color, zorder)

  def xmin(self):
    return min(self._x)

  def xmax(self):
    return max(self._x)

  def ymin(self):
    return min(self._y)

  def ymax(self):
    return max(self._y)
