#!/usr/bin/env python3

import ast
import os

for newsheet, oldsheet in [
    ["A3", "A1"],
    ["A4", "D1"],
    ["A5", "D1"],
    ["A6", "D1"],
    ["B3", "B1"],
    ["B4", "D1"],
    ["B5", "D1"],
    ["B6", "D1"],
    ["C3", "C1"],
    ["C4", "D1"],
    ["C5", "D1"],
    ["C6", "D1"],
    ["D2", "D1"],
    ["D3", "D1"],
    ["D4", "D1"],
    ["D5", "D1"],
    ["D6", "D1"],
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
        newx = newxcenter + (oldx - oldxcenter)
        newy = newycenter + (oldy - oldycenter)
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
        newx = newxcenter + (oldx - oldxcenter)
        newy = newycenter + (oldy - oldycenter)
        if int(newx) % 2 == 1:
            newy -= 0.5
        newxy = [newx, newy]
        return newxy

    def duplicateterrain(old):
        new = {}
        for key in old.keys():
            if key[-5:] == "hexes":
                new[key] = duplicatehexes(old[key])
            elif key[-5:] == "paths":
                new[key] = duplicatepaths(old[key])
            elif key == "center":
                new[key] = [newxcenter, newycenter]
            else:
                new[key] = old[key]
        return new

    newterrain = duplicateterrain(oldterrain)
    with open(newsheet + ".py", "w", encoding="utf-8") as f:
        print(newterrain, file=f)
