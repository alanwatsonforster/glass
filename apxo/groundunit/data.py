################################################################################

import os.path
import json
import re

################################################################################

def _loaddata(name):

    def filename(name):
        return os.path.join(
            os.path.dirname(__file__), "..", "groundunitdata", name + ".json"
        )

    def loadfile(name):
        try:
            with open(filename(name), "r", encoding="utf-8") as f:
                s = f.read(-1)
                # Strip whole-line // comments.
                r = re.compile("^[ \t]*//.*$", re.MULTILINE)
                s = re.sub(r, "", s)
                return json.loads(s)
        except FileNotFoundError:
            raise RuntimeError(
                'unable to find ground unit data file for "%s".' % name
            )
        except json.JSONDecodeError as e:
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
