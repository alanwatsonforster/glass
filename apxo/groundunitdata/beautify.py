#!/usr/bin/env python3

import glob
import json
import os.path
import re

pathlist = sorted(list(glob.glob("*.json")))

for path in pathlist:
    if path == "_INVALID.json":
        continue
    try:
        with open(path, "r", encoding="utf-8") as inputfile:
            text = inputfile.read(-1)

            linelist = text.split("\n")

            # Get whole-line // comments.
            commentlist = filter(
                lambda line: re.match("^[ \t]*//", line) is not None, linelist
            )
            commenttext = "\n".join(commentlist)

            r = re.compile("^[ \t]*//.*$", re.MULTILINE)
            jsontext = re.sub(r, "", text)
            jsontext = json.dumps(json.loads(jsontext), indent=4)

    except json.JSONDecodeError as e:
        raise RuntimeError(
            'unable to read "%s": line %d: %s.' % (path, e.lineno, e.msg.lower())
        )

    with open(path, "w", encoding="utf-8") as outputfile:
        if commenttext != "":
            print(commenttext, file=outputfile)
        print(jsontext, file=outputfile)
