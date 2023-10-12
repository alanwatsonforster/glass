import airpower.log as aplog


def leavecloseformation(self):
  if self._closeformation == None:
    aplog.logerror("%s: is not in a close formation." % self._name)

  self._closeformation.remove(self)
  self._closeformation = None

def joincloseformation(self, other):

  # TODO: check position, altitude, facing, and speed.

  if self._closeformation == None:
    self._closeformation = [self]

  if other._closeformation == None:
    other._closeformation = [other]

  self._closeformation += other._closeformation
  for a in self._closeformation:
    a._closeformation = self._closeformation

def showcloseformation(self):

  if self._closeformation == None:
    aplog.log("%s: is not in a close formation." % self._name)
  else:

    aplog.log("%s: is in a close formation of %d aircraft:" % (self._name, len(self._closeformation)))
    for a in self._closeformation:
      aplog.log("%s: - %s" % (self._name, a._name))

def closeformationsize(self):
  if closeformation == None:
    return 0
  else:
    return len(self._closeformation)