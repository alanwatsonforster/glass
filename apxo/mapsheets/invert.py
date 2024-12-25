#!/usr/bin/env python3

import ast
import os

for oldsheet, newsheet in [
    ["A1", "A3"],
    ["A2", "A4"],
    ["B1", "B3"],
    ["B2", "B4"],
    ["C1", "C3"],
    ["C2", "C4"],
]:

    with open(oldsheet + ".py", "r", encoding="utf-8") as f:
        s = f.read(-1)
        oldterrain = ast.literal_eval(s)

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

        return xcenter, ycenter

    oldxcenter, oldycenter = xycenter(oldsheet)
    newxcenter, newycenter = xycenter(newsheet)

    def inverthexes(oldhexes):
        return list(inverthex(oldhex) for oldhex in oldhexes)

    def inverthex(oldhex):
        oldx = oldhex // 100
        oldy = oldhex % 100
        dx = oldx - oldxcenter
        dy = oldy - oldycenter
        newx = newxcenter - dx
        newy = newycenter - dy
        newhex = newx * 100 + newy
        return int(newhex)

    def invertpaths(oldpaths):
        return list(invertpath(oldpath) for oldpath in oldpaths)

    def invertpath(oldpath):
        return list(invertxy(oldxy) for oldxy in oldpath)

    def invertxy(oldxy):
        oldx = oldxy[0]
        oldy = oldxy[1]
        if int(oldx) % 2 == 1:
            oldy += 0.5
        dx = oldx - oldxcenter
        dy = oldy - oldycenter
        newx = newxcenter - dx
        newy = newycenter - dy
        if int(newx) % 2 == 1:
            newy -= 0.5
        newxy = [newx, newy]
        return newxy

    def invertterrain(old):
        new = {}
        for key in old.keys():
            if key[-5:] == "hexes":
                new[key] = inverthexes(old[key])
            elif key[-5:] == "paths":
                new[key] = invertpaths(old[key])
            else:
                new[key] = old[key]
        return new

    newterrain = invertterrain(oldterrain)
    with open(newsheet + ".py", "w", encoding="utf-8") as f:
        print(newterrain, file=f)
