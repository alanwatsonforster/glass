#!/usr/bin/env python3

import sys
sys.path.append("../..")
import glass.jsonc

storetable = glass.jsonc.load(sys.stdin)

if sys.argv[1] == "FT":

    print("|Name|Weight|Load (Full)|Load (Empty)|Fuel Points|Notes|")
    print("|--|--|--|--|--|--|")

    for name in storetable:
        data = storetable[name]
        if len(data) == 5:
            note = ""
        else:
            note = data[5]["note"]
        print("|%s|%d|%.1f|%.1f|%d|%s|" % (
            name, data[1], data[2], data[3], data[4], note
        ))

else:

    print("|Name|Weight|Load|")
    print("|--|--|--|")

    for name in storetable:
        data = storetable[name]
        print("|%s|%d|%.1f|" % (
            name, data[1], data[2]
        ))
