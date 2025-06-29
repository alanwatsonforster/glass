#!/usr/bin/env python3

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import sys
sys.path.append("../..")
import glass.jsonc

import glob

for datafilepath in sorted(glob.glob("*.json")):

    print("reading %s." % datafilepath)

    storetable = glass.jsonc.load(open(datafilepath, "r"))

    tablefilepath = datafilepath[:-5] + ".md"

    print("writing %s." % tablefilepath)

    with open(tablefilepath, "w") as tablefile:

        def write(s):
            print(s, file=tablefile)

        if datafilepath == "FT.json":

            write("|Name|Weight|Load (Full)|Load (Empty)|Fuel Points|Notes|")
            write("|--|--|--|--|--|--|")

            for name in storetable:
                data = storetable[name]
                if len(data) == 5:
                    note = ""
                else:
                    note = data[5]["note"]
                write("|%s|%d|%.1f|%.1f|%d|%s|" % (
                    name, data[1], data[2], data[3], data[4], note
                ))

        else:

            write("|Name|Weight|Load|")
            write("|--|--|--|")

            for name in storetable:
                data = storetable[name]
                write("|%s|%d|%.1f|" % (
                    name, data[1], data[2]
                ))
