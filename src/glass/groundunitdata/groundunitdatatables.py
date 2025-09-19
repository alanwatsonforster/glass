import json
import os

os.chdir("src/glass/groundunitdata/")

with open("groundunitdatatables-generic.tex", "w") as latexfile:

    def writelatex(s=""):
        print(s, file=latexfile, end="")

    def writelatexline(s=""):
        print(s, file=latexfile, end="\n")        

    writelatexline(r"\begin{tabularx}{0.5\linewidth}{Lccc}")
    writelatexline(r"\toprule")
    writelatexline(r"Name    &Defense    &Sighting   &Barrage\\")
    writelatexline(r"        &Strength   &Range      &Fire\\")
    writelatexline(r"\midrule")

    for name in [
        "infantry",
        "infantry HQ",
        "infantry FAC",
        "heavy tank",
        "heavy tank HQ",
        "medium tank",
        "medium tank HQ",
        "light tank",
        "light tank HQ",
        "medium IFV",
        "light IFV",
        "heavy APC",
        "medium APC",
        "light APC",
        "truck",
        "light truck",
        "towed artillery",
        "armored artillery",
        "mobile artillery",
        "armored rocket artillery",
        "mobile rocket artillery",
        "mobile missile artillery",
        "mobile CCU",
        "armored CCU",
        "towed EWR-A",
        "mobile EWR-A",
        "towed FCR-A",
        "mobile FCR-A",
        "towed FCR-B",
        "mobile FCR-B",
        "towed FCR-C",
        "mobile FCR-C",
        "towed FCR-D",
        "mobile FCR-D",
    ]:
        print(name)
        data = json.load(open(name + ".json"))

        defensestrength = data["defensestrength"]
        sightingrange = data["sightingrange"]
        if "uppertext" not in data:
            uppertext = ""
        else:
            uppertext = data["uppertext"]

        writelatex(r"%s" % name)
        writelatex(r"&\wbox[l]{0H}{%s}" % defensestrength)
        writelatex(r"&\wbox{00}{%d}" % sightingrange)
        if uppertext == "" and "infantry" in data["symbols"]:
            barragefire = "Yes (+2)"
        elif uppertext == "" and "armor" in data["symbols"]:
            barragefire = "Yes (+3)"
        else:
            barragefire = "No"
        writelatex(r"&%s" % barragefire)
        writelatex(r"\\")
        writelatexline()

    writelatexline(r"\bottomrule")
    writelatexline(r"\end{tabularx}")
    