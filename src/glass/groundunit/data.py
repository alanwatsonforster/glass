################################################################################

import glass.jsonc

import os.path

################################################################################


def _loaddata(name):

    def filename(name):
        return os.path.join(
            os.path.dirname(__file__), "..", "groundunitdata", name + ".json"
        )

    def loadfile(name):
        try:
            with open(filename(name), "r", encoding="utf-8") as f:
                return glass.jsonc.load(f)
        except FileNotFoundError:
            raise RuntimeError('unable to find ground unit data file for "%s".' % name)
        except glass.jsonc.JSONDecodeError as e:
            raise RuntimeError(
                'unable to read ground unit data file for "%s": line %d: %s.'
                % (name, e.lineno, e.msg.lower())
            )

    data = loadfile(name)
    while "base" in data:
        base = data["base"]
        del data["base"]
        basedata = loadfile(base)
        basedata.update(data)
        data = basedata
    return data


################################################################################
