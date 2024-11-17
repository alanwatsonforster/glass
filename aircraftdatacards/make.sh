#!/bin/sh

cd "$dirname("$0")"

python3 aircraftdatacards.py

xelatex main.tex
