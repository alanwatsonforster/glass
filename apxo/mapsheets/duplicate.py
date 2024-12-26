#!/usr/bin/env python3

import ast
import os

for oldsheet, newsheet in [
    ["A1", "A5"],
    ["A2", "A6"],
    ["B1", "B5"],
    ["B2", "B6"],
    ["C1", "C5"],
    ["C2", "C6"],
]:

    with open(oldsheet + ".py", "r", encoding="utf-8") as f:
        s = f.read(-1)
        oldterrain = ast.literal_eval(s)

    def duplicatehexes(oldhexes):
        return list(duplicatehex(oldhex) for oldhex in oldhexes)

    def duplicatehex(oldhex):
        oldx = oldhex // 100
        oldy = oldhex % 100
        newx = oldx
        newy = oldy + 60
        newhex = newx * 100 + newy
        return int(newhex)

    def duplicatepaths(oldpaths):
        return list(duplicatepath(oldpath) for oldpath in oldpaths)

    def duplicatepath(oldpath):
        return list(duplicatexy(oldxy) for oldxy in oldpath)

    def duplicatexy(oldxy):
        oldx = oldxy[0]
        oldy = oldxy[1]
        newx = oldx
        newy = oldy + 60
        newxy = [newx, newy]
        return newxy

    def duplicateterrain(old):
        new = {}
        for key in old.keys():
            if key[-5:] == "hexes":
                new[key] = duplicatehexes(old[key])
            elif key[-5:] == "paths":
                new[key] = duplicatepaths(old[key])
            else:
                new[key] = old[key]
        return new

    newterrain = duplicateterrain(oldterrain)
    with open(newsheet + ".py", "w", encoding="utf-8") as f:
        print(newterrain, file=f)
