from apxo import aircraftdata


def log(s):
    print("adc: %s" % s)


def writelatex(s):
    print(s, file=latexfile)


def blockA(data):

    def crew():
        if len(data.crew()) == 1:
            return data.crew()[0]
        elif len(data.crew()) == 2:
            return data.crew()[0] + r" \& " + data.crew()[1]
        else:
            return ", ".join(data.crew()[0:-1]) + r", \& " + data.crew()[-1]

    writelatex(
        r"\renewcommand{\Aa}{%s}\renewcommand{\Ab}{%s}\renewcommand{\Ac}{%s}"
        % (data.name(), crew(), data.engines() * r"\circ"),
    )

    def power(configuration, setting):
        if data.power(configuration, setting) is None:
            return "---"
        else:
            return "%.1f" % data.power(configuration, setting)

    def fuelrate(setting):
        if data.fuelrate(setting) is None:
            return "---"
        else:
            return "%.0f" % data.fuelrate(setting)

    def speedbrake(setting):
        if data.speedbrake(setting) is None:
            return "---"
        else:
            return "%.1f" % data.speedbrake(setting)

    if data.power("CL", "M") is None:
        writelatex(
            r"\renewcommand{\Ada}{FT}\renewcommand{\Adb}{%s}\renewcommand{\Adc}{%s}\renewcommand{\Add}{%s}\renewcommand{\Ade}{%s}"
            % (
                power("CL", "FT"),
                power("1/2", "FT"),
                power("DT", "FT"),
                fuelrate("FT"),
            ),
        )
    else:
        writelatex(
            r"\renewcommand{\Ada}{AB}\renewcommand{\Adb}{%s}\renewcommand{\Adc}{%s}\renewcommand{\Add}{%s}\renewcommand{\Ade}{%s}"
            % (
                power("CL", "AB"),
                power("1/2", "AB"),
                power("DT", "AB"),
                fuelrate("AB"),
            ),
        )
    if data.power("CL", "M") is None:
        writelatex(
            r"\renewcommand{\Aea}{HT}\renewcommand{\Aeb}{%s}\renewcommand{\Aec}{%s}\renewcommand{\Aed}{%s}\renewcommand{\Aee}{%s}"
            % (
                power("CL", "HT"),
                power("1/2", "HT"),
                power("DT", "HT"),
                fuelrate("HT"),
            ),
        )
    else:
        writelatex(
            r"\renewcommand{\Aea}{M}\renewcommand{\Aeb}{%s}\renewcommand{\Aec}{%s}\renewcommand{\Aed}{%s}\renewcommand{\Aee}{%s}"
            % (power("CL", "M"), power("1/2", "M"), power("DT", "M"), fuelrate("M")),
        )
    writelatex(
        r"\renewcommand{\Af}{%s}" % (fuelrate("N")),
    )
    writelatex(
        r"\renewcommand{\Aga}{%s}\renewcommand{\Agb}{%s}\renewcommand{\Agc}{%s}"
        % (power("CL", "I"), power("1/2", "I"), power("DT", "I")),
    )
    writelatex(
        r"\renewcommand{\Aha}{%s}\renewcommand{\Ahb}{%s}\renewcommand{\Ahc}{%s}"
        % (speedbrake("CL"), speedbrake("1/2"), speedbrake("DT")),
    )

    s = ""
    if data.hasproperty("SMP"):
        s += "Smoker in military power. "
    if data.powerfade(100, 100) is not None:
        lastpowerfade = 0.0
        speed = 0.0
        while speed < 100:
            powerfade = data.powerfade(speed, 0)
            if powerfade != lastpowerfade:
                s += "Power reduced by %.1f when speed is greater than %.1f. " % (
                    powerfade,
                    speed - 0.5,
                )
            lastpowerfade = powerfade
            speed += 0.5
    writelatex(
        r"\renewcommand{\Ai}{%s}" % s,
    )


def blockB(data):

    def arcs(arcs):
        if len(arcs) == 0:
            return "---"
        elif len(arcs) == 1:
            return r"$\mathrm{%s}$" % arcs[0]
        else:
            return r"${}^\mathrm{%s}_\mathrm{%s}$" % (arcs[0], arcs[1])

    writelatex(r"\renewcommand{\Ba}{}")
    writelatex(r"\renewcommand{\Bb}{%.1f}" % data.cruisespeed("CL"))
    writelatex(r"\renewcommand{\Bc}{%.1f}" % data.climbspeed())
    writelatex(r"\renewcommand{\Bd}{%d}" % data.visibility())
    writelatex(r"\renewcommand{\Be}{%+d}" % data.sizemodifier())
    writelatex(r"\renewcommand{\Bf}{%+d}" % data.vulnerability())
    writelatex(r"\renewcommand{\Bg}{%s}" % arcs(data.restrictedarcs()))
    writelatex(r"\renewcommand{\Bh}{%s}" % arcs(data.blindarcs()))
    writelatex(r"\renewcommand{\Bi}{%d}" % data.internalfuelcapacity())
    if data.atarefuel():
        writelatex(r"\renewcommand{\Bj}{%s}" % "Yes")
    else:
        writelatex(r"\renewcommand{\Bj}{%s}" % "No")
    if data.ejectionseat() == "none":
        writelatex(r"\renewcommand{\Bk}{None}")
    elif data.ejectionseat() == "early":
        writelatex(r"\renewcommand{\Bk}{Early}")
    elif data.ejectionseat() == "standard":
        writelatex(r"\renewcommand{\Bk}{Std}")
    elif data.ejectionseat() == "advanced":
        writelatex(r"\renewcommand{\Bk}{Adv}")
    elif data.ejectionseat() == "rocket extraction device":
        writelatex(r"\renewcommand{\Bk}{Rkt}")
    else:
        raise RuntimeError("unknown ejection seat type %r" % data.ejectionseat())


def blockC(data):

    def drag(drag):
        if drag is None:
            return "---"
        else:
            return "%.1f" % drag

    writelatex(r"\renewcommand{\Ca}{%s}" % drag(data.rolldrag("DR")))
    writelatex(r"\renewcommand{\Cb}{%s}" % drag(data.rolldrag("VR")))

    writelatex(
        r"\renewcommand{\Cca}{%s}\renewcommand{\Ccb}{%s}\renewcommand{\Cca}{%s}"
        % (
            drag(data.turndrag("CL", "TT")),
            drag(data.turndrag("1/2", "TT")),
            drag(data.turndrag("DT", "TT")),
        )
    )
    writelatex(
        r"\renewcommand{\Cda}{%s}\renewcommand{\Cdb}{%s}\renewcommand{\Cda}{%s}"
        % (
            drag(data.turndrag("CL", "HT")),
            drag(data.turndrag("1/2", "HT")),
            drag(data.turndrag("DT", "HT")),
        )
    )
    writelatex(
        r"\renewcommand{\Cea}{%s}\renewcommand{\Ceb}{%s}\renewcommand{\Cea}{%s}"
        % (
            drag(data.turndrag("CL", "BT")),
            drag(data.turndrag("1/2", "BT")),
            drag(data.turndrag("DT", "BT")),
        )
    )
    writelatex(
        r"\renewcommand{\Cfa}{%s}\renewcommand{\Cfb}{%s}\renewcommand{\Cfa}{%s}"
        % (
            drag(data.turndrag("CL", "ET")),
            drag(data.turndrag("1/2", "ET")),
            drag(data.turndrag("DT", "ET")),
        )
    )


def makeadc(name):

    log("making LaTeX ADC for %s." % name)
    data = aircraftdata.aircraftdata(name)

    writelatex("%% %s" % name)

    blockA(data)
    blockB(data)
    blockC(data)

    writelatex(r"\adc")


latexfilename = "aircraftdatacards/generated.tex"
latexfile = open(latexfilename, "w")

makeadc("A-1E")
makeadc("A-1H")
makeadc("A-1J")
makeadc("A-26A")
makeadc("A-37B")
makeadc("A-3B")
makeadc("A3D-2")
makeadc("A3D-2Q")
makeadc("AD-4")
makeadc("AD-5")
makeadc("AD-6")
makeadc("AD-7")
makeadc("AT-33A")
makeadc("AU-1")
makeadc("Avon Sabre Mk.31")
makeadc("Avon Sabre Mk.32")
makeadc("B-26B")
makeadc("B-26C")
makeadc("B-26K")
makeadc("B-29A")
makeadc("B-52D")
makeadc("B-52G")
makeadc("B-57B-early")
makeadc("B-57B")
makeadc("B-57G")
makeadc("B-66B")
makeadc("EA-3B")
makeadc("EB-66C")
makeadc("F-100A")
makeadc("F-100C")
makeadc("F-100D")
makeadc("F-100F")
makeadc("F-102A")
makeadc("F-104A+")
makeadc("F-104A")
makeadc("F-104B")
makeadc("F-104C")
makeadc("F-104D")
makeadc("F-105B")
makeadc("F-105D")
makeadc("F-16A-1")
makeadc("F-16A-10")
makeadc("F-16A-15")
makeadc("F-16A-5")
makeadc("F-4B")
makeadc("F-4C")
makeadc("F-4E")
makeadc("F-4J")
makeadc("F-51D")
makeadc("F-5A")
makeadc("F-5C")
makeadc("F-80C")
makeadc("F-84E")
makeadc("F-84G")
makeadc("F-86A")
makeadc("F-86D")
makeadc("F-86E")
makeadc("F-86F-25")
makeadc("F-86F-35")
makeadc("F-86F-40")
makeadc("F-86F")
makeadc("F-86H Early")
makeadc("F-86H Late")
makeadc("F-86K Early")
makeadc("F-86K Late")
makeadc("F-86L")
makeadc("F-89D")
makeadc("F-89H")
makeadc("F-89J Long-Range")
makeadc("F-89J")
makeadc("F-8E")
makeadc("F-8J")
makeadc("F-94A")
makeadc("F-94B")
makeadc("F2H-2")
makeadc("F2H-2B")
makeadc("F2H-2P")
makeadc("F2H-3")
makeadc("F2H-4")
makeadc("F4U-5")
makeadc("F7U-3")
makeadc("F7U-3M")
makeadc("F9F-2")
makeadc("F9F-2P")
makeadc("F9F-5")
makeadc("F9F-5P")
# makeadc("HH-53C")
makeadc("Il-28")
makeadc("Meteor F.8")
makeadc("Meteor FR.9")
makeadc("MiG-15ISh")
makeadc("MiG-15P")
makeadc("MiG-15bis")
makeadc("MiG-17F")
makeadc("MiG-17PF")
makeadc("MiG-17PFU")
makeadc("MiG-19PF")
makeadc("MiG-19PM")
makeadc("MiG-19SF-CS")
makeadc("MiG-19SF")
makeadc("MiG-21F-13")
makeadc("MiG-21F")
makeadc("MiG-21M")
makeadc("MiG-21MF")
makeadc("MiG-21PFMA")
# makeadc("O-1E")
# makeadc("O-2A")
makeadc("OA-37B")
makeadc("RB-29A")
makeadc("RB-66C")
makeadc("RF-4B")
makeadc("RF-4C")
makeadc("RF-51D")
makeadc("RF-5A")
makeadc("RF-80C")
makeadc("Sabre 5")
makeadc("Sabre 6")
makeadc("Sea Fury FB.11")
makeadc("Su-11")
makeadc("Su-9")
makeadc("T-37C")
makeadc("Tu-16A")
makeadc("Tu-16K")
makeadc("Tu-16KS")
makeadc("Tu-4")
makeadc("Yak-9D")

latexfile.close()
