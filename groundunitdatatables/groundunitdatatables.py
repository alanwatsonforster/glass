import json
import os

latexdir = "groundunitdatatables/"
jsondir = "src/glass/groundunitdata/"

with open(latexdir + "/" + "groundunitdatatables-generic.tex", "w") as latexfile:

    def writelatex(s=""):
        print(s, file=latexfile, end="")

    def writelatexline(s=""):
        print(s, file=latexfile, end="\n")

    writelatexline(r"\begin{tabularx}{0.5\linewidth}{Lccc}")
    writelatexline(r"\toprule")
    writelatexline(r"Name    &Defense    &Sighting   &AAA    \\")
    writelatexline(r"        &Strength   &Range      &\phantom{\tablenotemark{1}}Class\tablenotemark{1}  \\")
    writelatexline(r"\midrule")

    i = 0

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
        "armored rocket artillery",
        "mobile artillery",
        "mobile rocket artillery",
        "mobile missile artillery",
        "mobile CCU",
        "armored CCU",
        "towed EWR-A",
        "towed FCR-A",
        "towed FCR-B",
        "towed FCR-C",
        "towed FCR-D",
        "mobile EWR-A",
        "mobile FCR-A",
        "mobile FCR-B",
        "mobile FCR-C",
        "mobile FCR-D",
    ]:

        if i % 3 == 0:
            writelatexline(r"\addlinespace")
        i += 1

        print(name)
        data = json.load(open(jsondir + "/" + name + ".json"))

        defensestrength = data["defensestrength"]
        sightingrange = data["sightingrange"]

        writelatex(r"%s" % name)
        writelatex(r"&\wbox[l]{0H}{%s}" % defensestrength)
        writelatex(r"&\wbox{00}{%d}" % sightingrange)
        if "aaa" in data:
            aaa = data["aaa"]
            aaaclass = aaa["class"]
            aaaaltitude = aaa["maximumrelativealtitude"]
            aaaclass = aaa["class"] + str(aaa["maximumrelativealtitude"])
        else:
            aaaclass = "---"
        writelatex(r"&%s" % aaaclass)
        writelatex(r"\\")
        writelatexline()

    writelatexline(r"\addlinespace")
    writelatexline(r"\bottomrule")
    writelatexline(r"\end{tabularx}")
    writelatexline(r"\begin{tablenote}{0.5\linewidth}")
    writelatexline(r"\tablenotemark{1} B2 or B3 indicate that the unit is capable of barrage fire to an altitude of 2 or 3 levels, respectively. Otherwise the unit is not capable of AAA fire.")
    writelatexline(r"\end{tablenote}")


with open(latexdir + "/" + "groundunitdatatables-aaa.tex", "w") as latexfile:

    def writelatex(s=""):
        print(s, file=latexfile, end="")

    def writelatexline(s=""):
        print(s, file=latexfile, end="\n")

    writelatexline(r"\begin{tabularx}{\linewidth}{Lcclccc@{~}c@{~}cc@{~}c@{~}cccl}")
    writelatexline(r"\toprule")
    writelatexline(
        r"""
            Name        &
            \multirow{2}*{\begin{tabular}{@{}c@{}}Defense\\Strength\end{tabular}}   &
            \multirow{2}*{\begin{tabular}{@{}c@{}}Sighting\\Range\end{tabular}}     &
            Gun         &
            Class       &
            Altitude    &
            \multicolumn{3}{c}{Range}   &
            \multicolumn{3}{c}{Hit}     &
            \multirow{2}*{\begin{tabular}{@{}c@{}}Damage\\Rating\end{tabular}}     &
            FCR&
            SAM
            \\
        """
    )
    writelatexline(
        r"""
            \cmidrule(lr){7-9}
            \cmidrule(lr){10-12}
        """
    )
    writelatexline(
        r"""
            &
            &
            &
            &
            &
            &
            S&M&L&       
            S&M&L&
            &
            &
            \\
        """
    )
    writelatexline(r"\midrule")

    i = 0

    for name in [

        "DShK-38",
        "M2",
        "M16",
        "M55",
        "mobile M55",

        "ZPU-1",
        "ZPU-2",
        "ZPU-4",
        "mobile ZPU-4",

        "Rh-202",
        "Panhard M3 DCA",
        "M163",
        "M167",

        "ZU-23",
        "mobile ZU-23",
        "ZSU-23-4",

        "AMX-30 DCA",
        "Tunguska",
        "Pantsir S1",
        "Pantsir S1M",
        
        "Oerlikon GDF",
        "Gepard",

        "M-38",
        
        "Bofors L60",
        "Bofors L70",
        "Bofors L70 BOFI-R",
        "M42",
                
        "S-60",
        "ZSU-57-2",
        
        "KS-12",
        
        "KS-19",
        
    ]:

        if i % 3 == 0:
            writelatexline(r"\addlinespace")
        i += 1

        print(name)
        data = json.load(open(jsondir + "/" + name + ".json"))

        defensestrength = data["defensestrength"]
        sightingrange = data["sightingrange"]

        aaa = data["aaa"]

        aaatype = aaa["type"]
        if "×" in aaatype:
            aaatype = r"\binarymultiply{%s mm}{%s}" % tuple(aaatype.split("×"))
        else:
            aaatype = r"%s mm" % aaatype
        
        if "sam" in data:
            samtype = data["sam"]["type"]
        else:
            samtype = "---"

        aaaclass = aaa["class"]
        aaarange = aaa["range"]
        aaahitroll = aaa["hitroll"]
        aaaaltitude = aaa["maximumrelativealtitude"]
        aaadamagerating = aaa["damagerating"]

        if "aaafcrclass" not in data:
            aaafcr = "---"
        else:
            aaafcr = aaa["fcrclass"] + "/" + aaa["fcrfrequency"]

        writelatex(r"%s" % name)

        writelatex(r"&\wbox[l]{0H}{%s}" % defensestrength)
        writelatex(r"&\wbox{00}{%d}" % sightingrange)

        writelatex(r"&%s" % aaatype)

        writelatex(r"&%s" % aaaclass)

        writelatex(r"&\wbox{00}{%s}" % aaaaltitude)

        writelatex(r"&\wbox{00}{%s}" % aaarange[0])
        writelatex(r"&\wbox{00}{%s}" % aaarange[1])
        writelatex(r"&\wbox{00}{%s}" % aaarange[2])

        writelatex(r"&\wbox{00}{%s}" % aaahitroll[0])
        writelatex(r"&\wbox{00}{%s}" % aaahitroll[1])
        writelatex(r"&\wbox{00}{%s}" % aaahitroll[2])

        writelatex(r"&\wbox{0}{%s}" % aaadamagerating)
        writelatex(r"&%s" % aaafcr)
        writelatex(r"&%s" % samtype)

        writelatex(r"\\")
        writelatexline()

    writelatexline(r"\addlinespace")
    writelatexline(r"\bottomrule")
    writelatexline(r"\end{tabularx}")


with open(latexdir + "/" + "groundunitdatatables-sam.tex", "w") as latexfile:

    def writelatex(s=""):
        print(s, file=latexfile, end="")

    def writelatexline(s=""):
        print(s, file=latexfile, end="\n")

    writelatexline(r"\begin{tabularx}{\linewidth}{Lcclcccccccccccl}")
    writelatexline(r"\toprule")
    writelatexline(
        r"""
            &
            &
            &
            &
            \multicolumn{3}{c}{EWR}         &
            \multicolumn{2}{c}{TTR}         &
            &
            \multicolumn{2}{c}{Missiles}    &
            &
            \multicolumn{2}{c}{Lock-On}     &
            \\
        """
    )

    writelatexline(
        r"""
            \cmidrule(lr){5-7}
            \cmidrule(lr){8-9}
            \cmidrule(lr){11-12}
            \cmidrule(lr){14-15}
        """
    )
    writelatexline(
        r"""
            Name&
            \vertical{\begin{tabular}{@{}l@{}}Defense\\Strength\end{tabular}}&
            \vertical{\begin{tabular}{@{}l@{}}Sighting\\Range\end{tabular}}&
            SAM&
            \vertical{Frequency}    &
            \vertical{Range}        &
            \vertical{MTI}          &
            \vertical{Frequency}    &
            \vertical{Range}        &
            \vertical{\begin{tabular}{@{}l@{}}Multi-Target\\Capability\end{tabular}}&
            \vertical{Ready}        &
            \vertical{Volley}       &
            \vertical{\begin{tabular}{@{}l@{}}Quick\\Reaction\end{tabular}}&
            \vertical{Radar}        &
            \vertical{Optical}      &
            AAA\\
            """
    )
    writelatexline(r"\midrule")

    i = 0

    for name in [
        "SA-2B",
        "SA-2C",
        "SA-2E",
        "SA-2F",
        "SA-3A",
        "SA-3B",
        "SA-4",
        "SA-5",
        "SA-6",
        "SA-8A",
        "SA-8B",
        "SA-9",
        "SA-10A",
        "SA-10B",
        "SA-11",
        "SA-12A",
        "SA-12B",
        "SA-13",
        "SA-15",
        "Tunguska",
        "Pantsir S1",
        #THERE ARE TWO SA-19s
        "SA-17",
        "Pantsir S1M",
    ]:

        if i % 3 == 0:
            writelatexline(r"\addlinespace")
        i += 1

        print(name)
        data = json.load(open(jsondir + "/" + name + ".json"))

        defensestrength = data["defensestrength"]
        sightingrange = data["sightingrange"]
        
        sam = data["sam"]

        samtype = sam["type"]
        
        if "aaa" not in data:
            aaatype = "---"
        else:
            aaatype = data["aaa"]["type"]            
            if "×" in aaatype:
                aaatype = r"\binarymultiply{%s mm}{%s}" % tuple(aaatype.split("×"))
            else:
                aaatype = r"%s mm" % aaatype

        if "ewrfrequency" not in sam:
            ewrfrequency = "---"
            ewrrange = "---"
        else:
            ewrfrequency = sam["ewrfrequency"]
            ewrrange = sam["ewrrange"]
        if "ewrmti" not in sam or not sam["ewrmti"]:
            ewrmti = "---"
        else:
            ewrmti = "Y"
        if "ttrfrequency" not in sam:
            ttrfrequency = "---"
            ttrrange = "---"
        else:
            ttrfrequency = sam["ttrfrequency"]
            ttrrange = sam["ttrrange"]

        if "multitargetcapability" not in sam:
            multitargetcapability = "---"
        else:
            multitargetcapability = sam["multitargetcapability"]

        readymissiles = sam["readymissiles"]
        volleymissiles = sam["volleymissiles"]

        if "quickreaction" not in sam or not sam["quickreaction"]:
            quickreaction = "---"
        else:
            quickreaction = "Y"

        if "radarlockon" not in sam:
            radarlockon = "---"
        else:
            radarlockon = sam["radarlockon"]
        if "opticallockon" not in sam:
            opticallockon = "---"
        else:
            opticallockon = sam["opticallockon"]

        writelatex(r"%s" % name)

        writelatex(r"&\wbox[l]{0H}{%s}" % defensestrength)
        writelatex(r"&\wbox{00}{%d}" % sightingrange)

        writelatex(r"&%s" % samtype)
        writelatex(r"&%s" % ewrfrequency)
        writelatex(r"&\wbox{000}{%s}" % ewrrange)
        writelatex(r"&%s" % ewrmti)
        writelatex(r"&%s" % ttrfrequency)
        writelatex(r"&\wbox{00}{%s}" % ttrrange)
        writelatex(r"&%s" % multitargetcapability)
        writelatex(r"&\wbox{00}{%d}" % readymissiles)
        writelatex(r"&\wbox{00}{%d}" % volleymissiles)
        writelatex(r"&%s" % quickreaction)
        writelatex(r"&%s" % radarlockon)
        writelatex(r"&%s" % opticallockon)

        writelatex(r"&%s" % aaatype)

        writelatex(r"\\")
        writelatexline()

    writelatexline(r"\addlinespace")
    writelatexline(r"\bottomrule")
    writelatexline(r"\end{tabularx}")
