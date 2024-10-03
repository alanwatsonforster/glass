#!/bin/env python3

import re
import sys

sys.path.append("..")
from apxo import aircraftdata
import apxo.variants

apxo.variants.setvariants(["use first-edition ADCs"])


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

    name = data.name()
    splitname = re.sub(
        r"\s+(([A-Z][a-z]+([-\s][A-Z][a-z]*)?(\s+II)?(\s\(([A-Z][a-z]+)([\s-][A-Z][a-z]+)*\))?)|([A-Z]+\.[0-9]+))$",
        r"\\\\\1",
        name,
    )
    writelatex(r"\renewcommand{\Aaa}{%s}" % name)
    writelatex(r"\renewcommand{\Aab}{%s}" % splitname)

    if len(data.crew()) > 6:
        writelatex(r"\renewcommand{\Aba}{\tiny}")
    else:
        writelatex(r"\renewcommand{\Aba}{\small}")
    writelatex(r"\renewcommand{\Abb}{%s}" % crew())

    if data.power("CL", "M") is None:
        writelatex(r"\renewcommand{\Ac}{%s}" % (data.engines() * r"\propellerengine"))
    else:
        writelatex(r"\renewcommand{\Ac}{%s}" % (data.engines() * r"\jetengine"))

    def power(configuration, setting):
        if data.power(configuration, setting) is None:
            return "---"
        else:
            return "%.1f" % data.power(configuration, setting)

    def fuelrate(setting):
        if data.fuelrate(setting) is None:
            return "---"
        else:
            return "%.1f" % data.fuelrate(setting)

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
    if data.powerfade(100, 0) is not None:
        lastpowerfade = 0.0
        speed = 0.0
        while speed < 100:
            powerfade = data.powerfade(speed, 0)
            if powerfade != lastpowerfade:
                s += r"If speed $\ge$ %.1f, reduce power by %.1f.\\" % (
                    speed,
                    powerfade,
                )
            lastpowerfade = powerfade
            speed += 0.5
    if data.powerfade(0, 100) is not None:
        lastpowerfade = 0.0
        altitude = 0
        while altitude < 100:
            powerfade = data.powerfade(0, altitude)
            if powerfade != lastpowerfade:
                s += r"If altitude $\ge$ %d, reduce power by %.1f.\\" % (
                    altitude,
                    powerfade,
                )
            lastpowerfade = powerfade
            altitude += 1
    if data.hasproperty("ABSF"):
        s += "If not in AB power, reduce maximum speeds by %.1f." % data.ABSFamount()

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

    def maneuverdrag(maneuvertype):
        drag = data.rolldrag(maneuvertype)
        if drag == None:
            return "---"
        else:
            return "%.1f" % drag

    def turndrag(configuration, turnrate):
        drag = data.turndrag(configuration, turnrate)
        if drag is None:
            return "---"
        if data.lowspeedliftdevicename() is None:
            return "%.1f" % drag
        else:
            lowspeedliftdevicedrag = data.turndrag(
                configuration, turnrate, lowspeedliftdevice=True
            )
            return "%.1f/%.1f" % (drag, lowspeedliftdevicedrag)

    writelatex(r"\renewcommand{\Ca}{%s}" % maneuverdrag("DR"))
    writelatex(r"\renewcommand{\Cb}{%s}" % maneuverdrag("VR"))

    writelatex(
        r"\renewcommand{\Cca}{%s}\renewcommand{\Ccb}{%s}\renewcommand{\Ccc}{%s}"
        % (
            turndrag("CL", "TT"),
            turndrag("1/2", "TT"),
            turndrag("DT", "TT"),
        )
    )
    writelatex(
        r"\renewcommand{\Cda}{%s}\renewcommand{\Cdb}{%s}\renewcommand{\Cdc}{%s}"
        % (
            turndrag("CL", "HT"),
            turndrag("1/2", "HT"),
            turndrag("DT", "HT"),
        )
    )
    writelatex(
        r"\renewcommand{\Cea}{%s}\renewcommand{\Ceb}{%s}\renewcommand{\Cec}{%s}"
        % (
            turndrag("CL", "BT"),
            turndrag("1/2", "BT"),
            turndrag("DT", "BT"),
        )
    )
    writelatex(
        r"\renewcommand{\Cfa}{%s}\renewcommand{\Cfb}{%s}\renewcommand{\Cfc}{%s}"
        % (
            turndrag("CL", "ET"),
            turndrag("1/2", "ET"),
            turndrag("DT", "ET"),
        )
    )

    s = ""
    if data.lowspeedliftdevicename() is not None:
        if data.lowspeedliftdeviceselectable():
            s += (
                r"Selectable %s. If selected and speed $\le$ "
                % data.lowspeedliftdevicename()
            )
        else:
            s += r"Automatic %s. If speed $\le$  " % data.lowspeedliftdevicename()
        if data.lowspeedliftdevicelimittype() == "absolute":
            s += r"%.1f," % data.lowspeedliftdevicelimit()
        else:
            s += r"minimum + %.1f," % data.lowspeedliftdevicelimit()
        if data.lowspeedliftdeviceselectable():
            s += r" use higher drag and reduce minimum speeds by 0.5."
        else:
            s += r" use higher drag."
    if data.hasproperty("NRM"):
        s += r"No rolling maneuvers allowed."
    if data.hasproperty("OVR"):
        s += r"Only one vertical roll allowed per game turn."
    if (
        data.hasproperty("NDRHS")
        and data.hasproperty("NDRHS")
        and data.NDRHSlimit() == data.NDRHSlimit()
    ):
        s += r"No lag or displacement rolls if speed $\ge$ %.1f. " % data.NDRHSlimit()
    else:
        if data.hasproperty("NDRHS"):
            s += r"No displacement rolls if speed $\ge$ %.1f. " % data.NDRHSlimit()
        if data.hasproperty("NLRHS"):
            s += r"No lag rolls if speed $\ge$ %.1f. " % data.NLRHSlimit()

    writelatex(r"\renewcommand{\Cg}{%s}" % s)


def blockD(data):

    def speeds(configuration, altitudeband):
        if data.minspeed(configuration, altitudeband) is None:
            return "---"
        else:
            return r"\blockDminmaxspeed{%.1f}{%.1f}" % (
                data.minspeed(configuration, altitudeband),
                data.maxspeed(configuration, altitudeband),
            )

    def divespeed(altitudeband):
        if data.maxdivespeed(altitudeband) is None:
            return "---"
        else:
            return r"\blockDdivespeed{%.1f}" % data.maxdivespeed(altitudeband)

    writelatex(
        r"\renewcommand{\Daa}{%d}\renewcommand{\Dab}{%d}\renewcommand{\Dac}{%d}"
        % (
            data.ceiling("CL"),
            data.ceiling("1/2"),
            data.ceiling("DT"),
        )
    )
    writelatex(
        r"\renewcommand{\Dca}{%s}\renewcommand{\Dcb}{%s}\renewcommand{\Dcc}{%s}\renewcommand{\Dcd}{%s}"
        % (
            speeds("CL", "EH"),
            speeds("1/2", "EH"),
            speeds("DT", "EH"),
            divespeed("EH"),
        )
    )
    writelatex(
        r"\renewcommand{\Dda}{%s}\renewcommand{\Ddb}{%s}\renewcommand{\Ddc}{%s}\renewcommand{\Ddd}{%s}"
        % (
            speeds("CL", "VH"),
            speeds("1/2", "VH"),
            speeds("DT", "VH"),
            divespeed("VH"),
        )
    )
    writelatex(
        r"\renewcommand{\Dea}{%s}\renewcommand{\Deb}{%s}\renewcommand{\Dec}{%s}\renewcommand{\Ded}{%s}"
        % (
            speeds("CL", "HI"),
            speeds("1/2", "HI"),
            speeds("DT", "HI"),
            divespeed("HI"),
        )
    )
    writelatex(
        r"\renewcommand{\Dfa}{%s}\renewcommand{\Dfb}{%s}\renewcommand{\Dfc}{%s}\renewcommand{\Dfd}{%s}"
        % (
            speeds("CL", "MH"),
            speeds("1/2", "MH"),
            speeds("DT", "MH"),
            divespeed("MH"),
        )
    )
    writelatex(
        r"\renewcommand{\Dga}{%s}\renewcommand{\Dgb}{%s}\renewcommand{\Dgc}{%s}\renewcommand{\Dgd}{%s}"
        % (
            speeds("CL", "ML"),
            speeds("1/2", "ML"),
            speeds("DT", "ML"),
            divespeed("ML"),
        )
    )
    writelatex(
        r"\renewcommand{\Dha}{%s}\renewcommand{\Dhb}{%s}\renewcommand{\Dhc}{%s}\renewcommand{\Dhd}{%s}"
        % (
            speeds("CL", "LO"),
            speeds("1/2", "LO"),
            speeds("DT", "LO"),
            divespeed("LO"),
        )
    )

    if data.maxspeed("CL", "EH") is not None:
        writelatex(r"\renewcommand{\Dba}{%.1f}" % data.maxspeed("CL", "EH"))
    elif data.maxspeed("CL", "VH") is not None:
        writelatex(r"\renewcommand{\Dba}{%.1f}" % data.maxspeed("CL", "VH"))
    elif data.maxspeed("CL", "HI") is not None:
        writelatex(r"\renewcommand{\Dba}{%.1f}" % data.maxspeed("CL", "HI"))
    elif data.maxspeed("CL", "MH") is not None:
        writelatex(r"\renewcommand{\Dba}{%.1f}" % data.maxspeed("CL", "MH"))
    elif data.maxspeed("CL", "ML") is not None:
        writelatex(r"\renewcommand{\Dba}{%.1f}" % data.maxspeed("CL", "ML"))
    else:
        writelatex(r"\renewcommand{\Dba}{%.1f}" % data.maxspeed("CL", "LO"))

    if data.maxdivespeed("EH") is not None:
        writelatex(r"\renewcommand{\Dbb}{%.1f}" % data.maxdivespeed("EH"))
    elif data.maxdivespeed("VH") is not None:
        writelatex(r"\renewcommand{\Dbb}{%.1f}" % data.maxdivespeed("VH"))
    elif data.maxdivespeed("HI") is not None:
        writelatex(r"\renewcommand{\Dbb}{%.1f}" % data.maxdivespeed("HI"))
    elif data.maxdivespeed("MH") is not None:
        writelatex(r"\renewcommand{\Dbb}{%.1f}" % data.maxdivespeed("MH"))
    elif data.maxdivespeed("ML") is not None:
        writelatex(r"\renewcommand{\Dbb}{%.1f}" % data.maxdivespeed("ML"))
    else:
        writelatex(r"\renewcommand{\Dbb}{%.1f}" % data.maxdivespeed("LO"))


def blockE(data):

    def climbcapability(configuration, altitudeband, powersetting):
        value = data.climbcapability(configuration, altitudeband, powersetting)
        if value is None:
            return "---"
        else:
            return r"%.1f" % value

    writelatex(
        r"\renewcommand{\Eaa}{%s}\renewcommand{\Eab}{%s}\renewcommand{\Eac}{%s}\renewcommand{\Ead}{%s}\renewcommand{\Eae}{%s}\renewcommand{\Eaf}{%s}"
        % (
            climbcapability("CL", "EH", "AB"),
            climbcapability("CL", "EH", "M"),
            climbcapability("1/2", "EH", "AB"),
            climbcapability("1/2", "EH", "M"),
            climbcapability("DT", "EH", "AB"),
            climbcapability("DT", "EH", "M"),
        )
    )
    writelatex(
        r"\renewcommand{\Eba}{%s}\renewcommand{\Ebb}{%s}\renewcommand{\Ebc}{%s}\renewcommand{\Ebd}{%s}\renewcommand{\Ebe}{%s}\renewcommand{\Ebf}{%s}"
        % (
            climbcapability("CL", "VH", "AB"),
            climbcapability("CL", "VH", "M"),
            climbcapability("1/2", "VH", "AB"),
            climbcapability("1/2", "VH", "M"),
            climbcapability("DT", "VH", "AB"),
            climbcapability("DT", "VH", "M"),
        )
    )
    writelatex(
        r"\renewcommand{\Eca}{%s}\renewcommand{\Ecb}{%s}\renewcommand{\Ecc}{%s}\renewcommand{\Ecd}{%s}\renewcommand{\Ece}{%s}\renewcommand{\Ecf}{%s}"
        % (
            climbcapability("CL", "HI", "AB"),
            climbcapability("CL", "HI", "M"),
            climbcapability("1/2", "HI", "AB"),
            climbcapability("1/2", "HI", "M"),
            climbcapability("DT", "HI", "AB"),
            climbcapability("DT", "HI", "M"),
        )
    )
    writelatex(
        r"\renewcommand{\Eda}{%s}\renewcommand{\Edb}{%s}\renewcommand{\Edc}{%s}\renewcommand{\Edd}{%s}\renewcommand{\Ede}{%s}\renewcommand{\Edf}{%s}"
        % (
            climbcapability("CL", "MH", "AB"),
            climbcapability("CL", "MH", "M"),
            climbcapability("1/2", "MH", "AB"),
            climbcapability("1/2", "MH", "M"),
            climbcapability("DT", "MH", "AB"),
            climbcapability("DT", "MH", "M"),
        )
    )
    writelatex(
        r"\renewcommand{\Eea}{%s}\renewcommand{\Eeb}{%s}\renewcommand{\Eec}{%s}\renewcommand{\Eed}{%s}\renewcommand{\Eee}{%s}\renewcommand{\Eef}{%s}"
        % (
            climbcapability("CL", "ML", "AB"),
            climbcapability("CL", "ML", "M"),
            climbcapability("1/2", "ML", "AB"),
            climbcapability("1/2", "ML", "M"),
            climbcapability("DT", "ML", "AB"),
            climbcapability("DT", "ML", "M"),
        )
    )
    writelatex(
        r"\renewcommand{\Efa}{%s}\renewcommand{\Efb}{%s}\renewcommand{\Efc}{%s}\renewcommand{\Efd}{%s}\renewcommand{\Efe}{%s}\renewcommand{\Eff}{%s}"
        % (
            climbcapability("CL", "LO", "AB"),
            climbcapability("CL", "LO", "M"),
            climbcapability("1/2", "LO", "AB"),
            climbcapability("1/2", "LO", "M"),
            climbcapability("DT", "LO", "AB"),
            climbcapability("DT", "LO", "M"),
        )
    )


def blockF(data):

    if data.gun() is None:
        writelatex(r"\renewcommand{\Fg}{---}")
        writelatex(r"\renewcommand{\Fh}{---}")
        writelatex(r"\renewcommand{\Fi}{---}")
        writelatex(r"\renewcommand{\Fl}{---}")
    else:
        s = data.gun()
        s = re.sub(r" and ", r" \& ", s)
        s = re.sub(r"\. ", r".~", s)
        if len(s) > 25:
            s = r"\scriptsize " + s
        elif len(s) > 20:
            s = r"\footnotesize " + s
        writelatex(r"\renewcommand{\Fg}{%s}" % s)
        if data.gunatatohitroll(2) is None:
            writelatex(
                r"\renewcommand{\Fh}{%d/%d/--}"
                % (data.gunatatohitroll(0), data.gunatatohitroll(1))
            )
        else:
            writelatex(
                r"\renewcommand{\Fh}{%d/%d/%d}"
                % (
                    data.gunatatohitroll(0),
                    data.gunatatohitroll(1),
                    data.gunatatohitroll(2),
                )
            )
        writelatex(r"\renewcommand{\Fi}{%.1f}" % (data.gunammunition()))
        writelatex(r"\renewcommand{\Fl}{%d/\wbox{0}{}}" % data.gunatadamagerating())

    s = ""
    for turnrate in ["TT", "HT", "BT"]:
        if data.gunsightmodifier(turnrate) is not None:
            s += "/%s%+d" % (turnrate, data.gunsightmodifier(turnrate))
    s = s[1:]
    if s == "":
        s = "---"
    writelatex(r"\renewcommand{\Fj}{%s}" % s)

    if data.ataradarrangingtype() is None:
        writelatex(r"\renewcommand{\Fk}{---}")
    else:
        writelatex(r"\renewcommand{\Fk}{%s}" % data.ataradarrangingtype())

    s = ""
    n = 1
    if len(data.properties()) != 0:
        for property in sorted(data.properties()):
            if property == "ABSF" or property == "SMP":
                # Noted in power section.
                pass
            elif (
                property == "OVR"
                or property == "NRM"
                or property == "NDRHS"
                or property == "NLRHS"
            ):
                # Noted in maneuver section.
                pass
            else:
                s += "%d. " % n
                n += 1
                if property == "GSSM":
                    s += r"Good supersonic maneuverability (GSSM). "
                elif property == "HAE":
                    s += r"High altitude engines (HAE). "
                elif property == "HBR":
                    s += r"High bleed rate (HBR). "
                elif property == "HPR":
                    s += r"High pitch rate (HPR). "
                elif property == "HRR":
                    s += r"High roll rate (HRR). "
                elif property == "HRRCL":
                    s += r"High roll rate (HRR) if CL. "
                elif property == "HTD":
                    s += r"High transonic drag (HTD). "
                elif property == "LBR":
                    s += r"Low bleed rate (LBR). "
                elif property == "LRR":
                    s += r"Low roll rate (LRR). "
                elif property == "LRRHS":
                    s += (
                        r"Low roll rate (LRR) if speed $\ge$ %.1f. "
                        % data._data["LRRHSlimit"]
                    )
                elif property == "LTD":
                    s += r"Low transonic drag (LTD). "
                elif property == "LTDCL":
                    s += r"Low transonic drag (LTD) if CL. "
                elif property == "PSSM":
                    s += r"Poor supersonic maneuverability (PSSM). "
                elif property == "RA":
                    s += r"Rapid acceleration (RA). "
                elif property == "RACL":
                    s += r"Rapid acceleration (RA) if CL. "
                elif property == "RPR":
                    s += r"Rapid power response (RPR). "
                else:
                    log("unknown property: %s" % property)
                    s += "%s. " % property
                s += "\n\n"

    for note in data.notes():
        s += "%d. %s\n\n" % (n, note)
        n += 1

    writelatex(r"\renewcommand{\Ft}{%s}" % s)


def writeadc(name):

    log("making LaTeX ADC for %s." % name)
    data = aircraftdata.aircraftdata(name)

    writelatex("%% %s" % name)

    blockA(data)
    blockB(data)
    blockC(data)
    blockD(data)
    blockE(data)
    blockF(data)

    writelatex(r"\adc")


latexfilename = "generated.tex"
latexfile = open(latexfilename, "w")

def writetype(name):
    writelatex(r"\addtoctype{%s}" % name)

writetype("AD/A-1 Skyraider")
writeadc("AD-4")
writeadc("AD-5")
writeadc("AD-6")
writeadc("AD-7")
writeadc("A-1E")
writeadc("A-1H")
writeadc("A-1J")

writetype("B-26/A-26 Invader")
writeadc("B-26B")
writeadc("B-26C")
writeadc("B-26K")
writeadc("A-26A")

writetype("A-27 Dragonfly")
writeadc("A-37B")

writetype("A3D/A-3 Skywarrior")
writeadc("A3D-2")
writeadc("A-3B")
writeadc("A3D-2Q")
writeadc("EA-3B")

writetype("T-33 Shooting Star")
writeadc("AT-33A")

writetype("F4U/AU Corsair")
writeadc("AU-1")

writetype("F-86 Sabre")
writeadc("Avon Sabre Mk.31")
writeadc("Avon Sabre Mk.32")

writeadc("B-29A")
writeadc("B-52D")
writeadc("B-52G")
writeadc("B-57B-early")
writeadc("B-57B")
writeadc("B-57G")
writeadc("B-66B")
writeadc("EB-66C")
writeadc("F-100A")
writeadc("F-100C")
writeadc("F-100D")
writeadc("F-100F")
writeadc("F-102A")
writeadc("F-104A+")
writeadc("F-104A")
writeadc("F-104B")
writeadc("F-104C")
writeadc("F-104D")
writeadc("F-105B")
writeadc("F-105D")
writeadc("F-16A-1")
writeadc("F-16A-10")
writeadc("F-16A-15")
writeadc("F-16A-5")
writeadc("F-4B")
writeadc("F-4C")
writeadc("F-4E")
writeadc("F-4J")
writeadc("F-51D")
writeadc("F-5A")
writeadc("F-5C")
writeadc("F-80C")
writeadc("F-84E")
writeadc("F-84G")
writeadc("F-86A")
writeadc("F-86D")
writeadc("F-86E")
writeadc("F-86F-25")
writeadc("F-86F-35")
writeadc("F-86F-40")
writeadc("F-86F")
writeadc("F-86H Early")
writeadc("F-86H Late")
writeadc("F-86K Early")
writeadc("F-86K Late")
writeadc("F-86L")
writeadc("F-89D")
writeadc("F-89H")
writeadc("F-89J Long-Range")
writeadc("F-89J")
writeadc("F-8E")
writeadc("F-8J")
writeadc("F-94A")
writeadc("F-94B")
writeadc("F2H-2")
writeadc("F2H-2B")
writeadc("F2H-2P")
writeadc("F2H-3")
writeadc("F2H-4")
writeadc("F4U-5")
writeadc("F7U-3")
writeadc("F7U-3M")
writeadc("F9F-2")
writeadc("F9F-2P")
writeadc("F9F-5")
writeadc("F9F-5P")
# writeadc("HH-53C")
writeadc("Il-28")
writeadc("Meteor F.8")
writeadc("Meteor FR.9")
writeadc("MiG-15ISh")
writeadc("MiG-15P")
writeadc("MiG-15bis")
writeadc("MiG-17F")
writeadc("MiG-17PF")
writeadc("MiG-17PFU")
writeadc("MiG-19PF")
writeadc("MiG-19PM")
writeadc("MiG-19SF-CS")
writeadc("MiG-19SF")
writeadc("MiG-21F-13")
writeadc("MiG-21F")
writeadc("MiG-21M")
writeadc("MiG-21MF")
writeadc("MiG-21PFMA")
# writeadc("O-1E")
# writeadc("O-2A")
writeadc("OA-37B")
writeadc("RB-29A")
writeadc("RB-66C")
writeadc("RF-4B")
writeadc("RF-4C")
writeadc("RF-51D")
writeadc("RF-5A")
writeadc("RF-80C")
writeadc("Sabre 5")
writeadc("Sabre 6")
writeadc("Sea Fury FB.11")
writeadc("Sea Harrier FA.2")
writeadc("Sea Harrier FRS.1")
writeadc("Sea Harrier FRS.2")
writeadc("Su-11")
writeadc("Su-9")
writeadc("T-37C")
writeadc("Tu-16A")
writeadc("Tu-16K")
writeadc("Tu-16KS")
writeadc("Tu-4")
writeadc("Yak-9D")

latexfile.close()
