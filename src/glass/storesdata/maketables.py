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

            write(
                "|Name|Liters|US Gallons|Imp Gallons|Weight|Load (Full)|Load (Empty)|Fuel Capacity|Notes|"
            )
            write("|--|--|--|--|--|--|--|--|--|")

            for name in storetable:
                data = storetable[name]
                weight = data["weight"]
                load = data["load"]
                emptyload = data["emptyload"]
                fuelcapacity = data["fuelcapacity"]
                liters = int(name.split("/")[-1][:-1])

                if "note" in data:
                    note = data["note"]
                else:
                    note = ""
                write(
                    "|%s|%.0f|%.0f|%.0f|%d|%.1f|%.1f|%d|%s|"
                    % (
                        name,
                        liters,
                        liters / 3.785,
                        liters / 4.546,
                        weight,
                        load,
                        emptyload,
                        fuelcapacity,
                        note,
                    )
                )

        else:

            write("|Name|Weight|Load|")
            write("|--|--|--|")

            for name in storetable:
                data = storetable[name]
                weight = data["weight"]
                load = data["load"]
                write("|%s|%d|%.1f|" % (name, weight, load))
