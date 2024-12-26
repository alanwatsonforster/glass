#!/usr/bin/env python3

import ast
import os

for newsheet, oldsheet, rotate, simplify in [
    ["A3", "A1", True, True],
    ["A4", "A1", True, True],
    ["A5", "A1", False, True],
    ["A6", "A1", True, True],
    ["B3", "B2", True, True],
    ["B4", "B2", True, False],
    ["B5", "B2", False, True],
    ["B6", "B2", True, True],
    ["C3", "C1", True, False],
    ["C4", "C2", True, False],
    ["C5", "C1", False, True],
    ["C6", "C2", True, True],
]:

    def xycenter(sheet):

        sheetletter = sheet[0]
        if sheetletter == "A":
            xcenter = 20
        elif sheetletter == "B":
            xcenter = 40
        elif sheetletter == "C":
            xcenter = 60
        elif sheetletter == "D":
            xcenter = 80
        else:
            raise RuntimeError("%r is not a valid sheet." % sheet)

        sheetnumber = sheet[1]
        if sheetnumber == "1":
            ycenter = 8.5
        elif sheetnumber == "2":
            ycenter = 23.5
        elif sheetnumber == "3":
            ycenter = 38.5
        elif sheetnumber == "4":
            ycenter = 53.5
        elif sheetnumber == "5":
            ycenter = 68.5
        elif sheetnumber == "6":
            ycenter = 83.5

        return xcenter, ycenter

    oldxcenter, oldycenter = xycenter(oldsheet)
    newxcenter, newycenter = xycenter(newsheet)

    with open(oldsheet + ".py", "r", encoding="utf-8") as f:
        s = f.read(-1)
        oldterrain = ast.literal_eval(s)

    def duplicatehexes(oldhexes):
        return list(duplicatehex(oldhex) for oldhex in oldhexes)

    def duplicatehex(oldhex):
        oldx = oldhex // 100
        oldy = oldhex % 100
        if int(oldx) % 2 == 1:
            oldy += 0.5
        dx = oldx - oldxcenter
        dy = oldy - oldycenter
        if rotate:
            newx = newxcenter - dx
            newy = newycenter - dy
        else:
            newx = newxcenter + dx
            newy = newycenter + dy
        if int(newx) % 2 == 1:
            newy -= 0.5
        newhex = newx * 100 + newy
        return int(newhex)

    def duplicatepaths(oldpaths):
        return list(duplicatepath(oldpath) for oldpath in oldpaths)

    def duplicatepath(oldpath):
        return list(duplicatexy(oldxy) for oldxy in oldpath)

    def duplicatexy(oldxy):
        oldx = oldxy[0]
        oldy = oldxy[1]
        if int(oldx) % 2 == 1:
            oldy += 0.5
        dx = oldx - oldxcenter
        dy = oldy - oldycenter
        if rotate:
            newx = newxcenter - dx
            newy = newycenter - dy
        else:
            newx = newxcenter + dx
            newy = newycenter + dy
        if int(newx) % 2 == 1:
            newy -= 0.5
        newxy = [newx, newy]
        return newxy

    simplifiedkeys = [
        "runwaypaths",
        "taxiwaypaths",
        "dampaths",
        "lakehexes",
        "town5hexes",
        "cityhexes",
    ]

    def duplicateterrain(old):
        new = {}
        for key in old.keys():
            if simplify and key in simplifiedkeys:
                new[key] = []
            elif key[-5:] == "hexes":
                new[key] = duplicatehexes(old[key])
            elif key[-5:] == "paths":
                new[key] = duplicatepaths(old[key])
            else:
                new[key] = old[key]
        return new

    newterrain = duplicateterrain(oldterrain)
    with open(newsheet + ".py", "w", encoding="utf-8") as f:
        print(newterrain, file=f)
