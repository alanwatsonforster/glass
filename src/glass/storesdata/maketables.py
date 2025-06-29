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

            write("|Name|Weight|Load (Full)|Load (Empty)|Fuel Capacity|Notes|")
            write("|--|--|--|--|--|--|")

            for name in storetable:
                data = storetable[name]
                weight = data[1]
                loadpoints = data[2]
                additionaldata = data[3]
                emptyloadpoints = additionaldata["emptyload"]
                fuelcapacity = additionaldata["fuelcapacity"]
                if "note" in additionaldata:
                    note = additionaldata["note"]
                else:
                    note = ""
                write(
                    "|%s|%d|%.1f|%.1f|%d|%s|"
                    % (name, weight, loadpoints, emptyloadpoints, fuelcapacity, note)
                )

        else:

            write("|Name|Weight|Load|")
            write("|--|--|--|")

            for name in storetable:
                data = storetable[name]
                weight = data[1]
                loadpoints = data[2]
                write("|%s|%d|%.1f|" % (name, weight, loadpoints))
