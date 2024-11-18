#!/usr/bin/env python3

import re
import sys

sys.path.append("..")
from apxo import aircraftdata
import apxo.variants

version = 1

if version == 1:
    apxo.variants.setvariants(["use first-edition ADCs"])
elif version == 2:
    pass
elif version == 3:
    apxo.variants.setvariants(["use house rules"])


def log(s):
    print("adc: %s" % s)


def writelatex(s):
    print(s, file=latexfile)


def latexify(s):
    s = re.sub(r"([ (])([-+][0-9]+)([. )])", r"\1$\2$\3", s)
    s = re.sub(r"([ (])([0-9]+[-+])([. )])", r"\1$\2$\3", s)
    return s


def blockA(data):

    def crew():
        if len(data.crew()) == 1:
            return data.crew()[0]
        elif len(data.crew()) == 2:
            return data.crew()[0] + r" \& " + data.crew()[1]
        else:
            return ", ".join(data.crew()[0:-1]) + r", \& " + data.crew()[-1]

    writelatex(r"\renewcommand{\Aaa}{%s}" % data.fullvariantname())

    splitfullname = re.sub(
        r"\s+(([A-Z][a-z]+([-\s][A-Z][a-z]*)?(\s+II)?)|([A-Za-z]+\.[0-9]+))$",
        r"\\\\\1",
        data.fullname(),
    )
    writelatex(r"\renewcommand{\Aab}{%s}" % splitfullname)

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
        value = data.rolldrag(maneuvertype)
        if value == None:
            return "---"
        elif value % 0.5 == 0:
            return r"%.1f" % value
        else:
            return r"%.2f" % value

    def turndrag(configuration, turnrate):

        def formatdrag(value):
            if precision == 1:
                return "%.1f" % value
            else:
                return "%.2f" % value

        drag = data.turndrag(configuration, turnrate)
        if drag is None:
            return "---"
        if data.lowspeedliftdevicename() is None:
            return formatdrag(drag)
        else:
            lowspeedliftdevicedrag = data.turndrag(
                configuration, turnrate, lowspeedliftdevice=True
            )
            return "%s/%s" % (formatdrag(drag), formatdrag(lowspeedliftdevicedrag))

    writelatex(r"\renewcommand{\Ca}{%s}" % maneuverdrag("DR"))
    writelatex(r"\renewcommand{\Cb}{%s}" % maneuverdrag("VR"))

    precision = 0
    values = [
        data.turndrag("CL", "TT"),
        data.turndrag("1/2", "TT"),
        data.turndrag("DT", "TT"),
        data.turndrag("CL", "HT"),
        data.turndrag("1/2", "HT"),
        data.turndrag("DT", "HT"),
        data.turndrag("CL", "BT"),
        data.turndrag("1/2", "BT"),
        data.turndrag("DT", "BT"),
        data.turndrag("CL", "ET"),
        data.turndrag("1/2", "ET"),
        data.turndrag("DT", "ET"),
    ]
    if data.lowspeedliftdevicename() is not None:
        values += [
            data.turndrag("CL", "TT", lowspeedliftdevice=True),
            data.turndrag("1/2", "TT", lowspeedliftdevice=True),
            data.turndrag("DT", "TT", lowspeedliftdevice=True),
            data.turndrag("CL", "HT", lowspeedliftdevice=True),
            data.turndrag("1/2", "HT", lowspeedliftdevice=True),
            data.turndrag("DT", "HT", lowspeedliftdevice=True),
            data.turndrag("CL", "BT", lowspeedliftdevice=True),
            data.turndrag("1/2", "BT", lowspeedliftdevice=True),
            data.turndrag("DT", "BT", lowspeedliftdevice=True),
            data.turndrag("CL", "ET", lowspeedliftdevice=True),
            data.turndrag("1/2", "ET", lowspeedliftdevice=True),
            data.turndrag("DT", "ET", lowspeedliftdevice=True),
        ]
    for value in values:
        if value is None:
            pass
        elif value % 0.5 == 0:
            precision = max(precision, 1)
        else:
            precision = max(precision, 2)

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
        elif precision == 1:
            return r"%.1f" % value
        else:
            return r"%.2f" % value

    precision = 0
    values = [
        data.climbcapability("CL", "EH", "AB"),
        data.climbcapability("CL", "EH", "M"),
        data.climbcapability("1/2", "EH", "AB"),
        data.climbcapability("1/2", "EH", "M"),
        data.climbcapability("DT", "EH", "AB"),
        data.climbcapability("DT", "EH", "M"),
        data.climbcapability("CL", "VH", "AB"),
        data.climbcapability("CL", "VH", "M"),
        data.climbcapability("1/2", "VH", "AB"),
        data.climbcapability("1/2", "VH", "M"),
        data.climbcapability("DT", "VH", "AB"),
        data.climbcapability("DT", "VH", "M"),
        data.climbcapability("CL", "HI", "AB"),
        data.climbcapability("CL", "HI", "M"),
        data.climbcapability("1/2", "HI", "AB"),
        data.climbcapability("1/2", "HI", "M"),
        data.climbcapability("DT", "HI", "AB"),
        data.climbcapability("DT", "HI", "M"),
        data.climbcapability("CL", "MH", "AB"),
        data.climbcapability("CL", "MH", "M"),
        data.climbcapability("1/2", "MH", "AB"),
        data.climbcapability("1/2", "MH", "M"),
        data.climbcapability("DT", "MH", "AB"),
        data.climbcapability("DT", "MH", "M"),
        data.climbcapability("CL", "ML", "AB"),
        data.climbcapability("CL", "ML", "M"),
        data.climbcapability("1/2", "ML", "AB"),
        data.climbcapability("1/2", "ML", "M"),
        data.climbcapability("DT", "ML", "AB"),
        data.climbcapability("DT", "ML", "M"),
        data.climbcapability("CL", "LO", "AB"),
        data.climbcapability("CL", "LO", "M"),
        data.climbcapability("1/2", "LO", "AB"),
        data.climbcapability("1/2", "LO", "M"),
        data.climbcapability("DT", "LO", "AB"),
        data.climbcapability("DT", "LO", "M"),
    ]
    for value in values:
        if value is None:
            pass
        elif value % 0.5 == 0:
            precision = max(precision, 1)
        else:
            precision = max(precision, 2)

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

    if data.radar() is None:
        writelatex(r"\renewcommand{\Fa}{---}")
        writelatex(r"\renewcommand{\Fb}{---}")
        writelatex(r"\renewcommand{\Fc}{---}")
        writelatex(r"\renewcommand{\Fd}{---}")
        writelatex(r"\renewcommand{\Fe}{---}")
    elif data.radar("name") == "gunsight":
        writelatex(r"\renewcommand{\Fa}{Gunsight}")
        writelatex(r"\renewcommand{\Fb}{---}")
        writelatex(r"\renewcommand{\Fc}{---}")
        writelatex(r"\renewcommand{\Fd}{---}")
        writelatex(r"\renewcommand{\Fe}{---}")
    else:
        writelatex(r"\renewcommand{\Fa}{%s}" % data.radar("name"))
        if data.radar("eccm") is None:
            writelatex(r"\renewcommand{\Fb}{---}")
        else:
            writelatex(r"\renewcommand{\Fb}{%d}" % data.radar("eccm"))
        if data.radar("arc") is None:
            writelatex(r"\renewcommand{\Fc}{---}")
        else:
            writelatex(r"\renewcommand{\Fc}{$\mathrm{%s}$}" % data.radar("arc"))
        if data.radar("searchrange") is None:
            writelatex(r"\renewcommand{\Fd}{---}")
        else:
            writelatex(
                r"\renewcommand{\Fd}{%d--%d}"
                % (data.radar("searchrange"), data.radar("searchstrength"))
            )
        if data.radar("trackingrange") is None:
            writelatex(r"\renewcommand{\Fe}{---}")
        else:
            writelatex(
                r"\renewcommand{\Fe}{%d--%d}"
                % (data.radar("trackingrange"), data.radar("trackingstrength"))
            )

    if data.lockon() is None:
        writelatex(r"\renewcommand{\Ff}{---}")
    else:
        writelatex(r"\renewcommand{\Ff}{%d}" % data.lockon())

    if data.gun() is None:
        writelatex(r"\renewcommand{\Fg}{---}")
        writelatex(r"\renewcommand{\Fh}{---}")
        writelatex(r"\renewcommand{\Fi}{---}")
        writelatex(r"\renewcommand{\Fl}{---}")
    else:
        s = data.gun()
        if " and " in s:
            font = r"\scriptsize"
            s = re.sub(r"and one", r"\\\\One", s)
            s = re.sub(r"and two", r"\\\\Two", s)
            s = re.sub(r"and three", r"\\\\Three", s)
            s = re.sub(r"and four", r"\\\\Four", s)
        else:
            font = ""
        s = re.sub(r"\. ", r".~", s)
        s = re.sub(r" mm", r"~mm", s)
        writelatex(r"\renewcommand{\Fg}{%s %s}" % (font, s))
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
        writelatex(
            r"\renewcommand{\Fl}{%d/%s}"
            % (data.gunatadamagerating(), data.gunatgdamagerating())
        )

    writelatex(r"\renewcommand{\Fm}{%s}" % data.bombsystem())

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

    if data.ecm("iff") is True:
        writelatex(r"\renewcommand{\Fn}{Yes}")
    else:
        writelatex(r"\renewcommand{\Fn}{No}")
    if data.ecm("rwr") is not None:
        writelatex(r"\renewcommand{\Fo}{%s}" % data.ecm("rwr"))
    else:
        writelatex(r"\renewcommand{\Fo}{---}")
    if data.ecm("dds") is not None:
        writelatex(r"\renewcommand{\Fp}{%s}" % data.ecm("rwr"))
    else:
        writelatex(r"\renewcommand{\Fp}{---}")
    if data.ecm("djm") is not None:
        writelatex(r"\renewcommand{\Fq}{%s}" % data.ecm("rwr"))
    else:
        writelatex(r"\renewcommand{\Fq}{---}")
    if data.ecm("ajm") is not None:
        writelatex(r"\renewcommand{\Fr}{%s}" % data.ecm("rwr"))
    else:
        writelatex(r"\renewcommand{\Fr}{---}")

    if data.technology() is None:
        writelatex(r"\renewcommand{\Fs}{None}")
    else:
        s = " ".join(data.technology())
        writelatex(r"\renewcommand{\Fs}{%s}" % s)

    writelatex(r"\renewcommand{\Fta}{%s}" % data.manufacturername())
    writelatex(r"\renewcommand{\Ftb}{%s}" % data.fullvariantname())
    if data.variantdescription() is None:
        writelatex(r"\renewcommand{\Ftc}{}")
    else:
        writelatex(r"\renewcommand{\Ftc}{%s}" % data.variantdescription())

    #if data.service() is None:
    #    writelatex(r"\renewcommand{\Fu}{}")
    #else:
    #    writelatex(r"\renewcommand{\Fu}{\Fua{%s}}" % data.service())

    s = ""
    
    if data.variantname() is not None:
        s += "\item %s variant %s" % (
            data.fullvariantname(),
            latexify(data.variantdescription())
        )

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
                s += "\\item "
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
        s += "\\item %s\n\n" % (latexify(note))

    for note in data.variantnotes():
        s += "\\item %s\n\n" % (latexify(note))
        
    if data.originallydesignated() is not None:
        s += "\\item Originally designated %s.\n\n" % (latexify(data.originallydesignated()))
    if data.previouslydesignated() is not None:
        s += "\\item Previously designated %s.\n\n" % (latexify(data.previouslydesignated()))
    if data.subsequentlydesignated() is not None:
        s += "\\item Subsequently designated %s.\n\n" % (latexify(data.subsequentlydesignated()))
    if data.natoreportingname() is not None:
        s += "\\item NATO reporting name is %s.\n\n" % (latexify(data.natoreportingname()))
    

    if data.wikiurl() is not None:
        s += "\\item \\href{\\detokenize{%s}}{ADC page on GitHub}.\n\n" % (
            data.wikiurl(),
        )
        
    if s == "":
        writelatex(r"\renewcommand{\Fv}{}")
    else:
        writelatex(r"\renewcommand{\Fv}{\Fva{%s}}" % s)


def blockG(data):

    if data.hasstoreslimits():
        writelatex(r"\renewcommand{\Gba}{\le %.1f}" % data.storeslimit("CL"))
        writelatex(r"\renewcommand{\Gbb}{\le %.1f}" % data.storeslimit("1/2"))
        writelatex(r"\renewcommand{\Gbc}{> %.1f}" % data.storeslimit("1/2"))
        writelatex(r"\renewcommand{\Gbd}{%s}" % ("{:,}".format(data.storeslimit("DT"))))
    else:
        writelatex(r"\renewcommand{\Gba}{}")
        writelatex(r"\renewcommand{\Gbb}{}")
        writelatex(r"\renewcommand{\Gbc}{}")
        writelatex(r"\renewcommand{\Gbd}{}")
        
    s = ""
    for station in data.stations():
        stationtype = station[0]
        stationidentifiers = station[1]
        stationlimit = station[2]
        stationloads = station[3]
        if stationtype == "single":
          s += "%d" % stationidentifiers[0]
        elif stationtype == "pair":
          s += "%d and %d" % tuple(stationidentifiers)
        elif stationtype == "group":
          s += "%d--%d" % tuple(stationidentifiers)
        elif stationtype == "grouppair":
          s += "%d--%d and %d--%d" % tuple(stationidentifiers)
        s += "&%s&%s\\\\\n" % (
          "{:,}".format(stationlimit), 
          "/".join(stationloads)
        )
    writelatex(r"\renewcommand{\Gca}{%s}" % s)
    
    s = ""
    for note in data.loadnotes():
        s += "\\item %s\n\n" % (latexify(note))
    if s == "":
        writelatex(r"\renewcommand{\Gcb}{%s}" % s)
    else:
        writelatex(r"\renewcommand{\Gcb}{\Gcc{%s}}" % s)
        
    if data.hasVPs():
        writelatex(
            r"\renewcommand{\Gda}{%d/%d/%d/%d}"
            % (data.VPs("K"), data.VPs("C"), data.VPs("H"), data.VPs("L"))
        )
    else:
        writelatex(r"\renewcommand{\Gda}{}")


def writeversion():
    writelatex(r"\renewcommand{\V}{%d}" % version)


def writecountry(name):
    writelatex(r"\addtoccountry{%s}" % name)


def writetype(name):
    writelatex(r"\addtoctype{%s}" % name)


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
    blockG(data)

    writelatex(r"\adc")


# We assign aircraft to counties according to the country of their
# original manufacture. Hence, CAC and Avon Sabres are considered to be
# Australian and Canadian aircraft.

# We order aircraft types within country by date of delivery.

latexfilename = "generated.tex"
latexfile = open(latexfilename, "w")
writeversion()

writecountry("Australian Aircraft")

writeadc("Avon Sabre Mk.31 (Early)")
writeadc("Avon Sabre Mk.31 (Late)")
writeadc("Avon Sabre Mk.32")

writecountry("British Aircraft")

writetype("Meteor")  # 1944
writeadc("Meteor F.8")
writeadc("Meteor FR.9")

writetype("Sea Fury")  # 1948
writeadc("Sea Fury FB.11")

writecountry("Canadian Aircraft")

writeadc("Sabre Mk.5")
writeadc("Sabre Mk.6")

writecountry("Soviet Union Aircraft")

writetype("Yak-9")  # 1942
writeadc("Yak-9D")

writetype("Il-10 Beast")  # 1944
writeadc("Il-10")

writetype("Tu-4 Bull")  # 1947
writeadc("Tu-4")

writetype("MiG-15 Fagot")  # 1949
writeadc("MiG-15bis")
writeadc("MiG-15P")
writeadc("MiG-15ISh")

writecountry("US Aircraft")

writetype("P-51/F-51 Mustang")  # Jan 1942 with RAF
writeadc("F-51D")
writeadc("RF-51D")

writetype("F4U/AU Corsair")  # December 1942 with USCMC
writeadc("F4U-5")
writeadc("AU-1")

writetype("B-26/A-26 Invader")  # 1943
writeadc("B-26B (Two Turrets)")
writeadc("B-26B (One Turret)")
writeadc("B-26B (No Turrets)")
writeadc("B-26C (Two Turrets)")
writeadc("B-26C (One Turret)")
writeadc("B-26C (No Turrets)")
writeadc("B-26K")
writeadc("A-26A")

writetype("B-29 Superfortress")  # 1944
writeadc("B-29A")
writeadc("RB-29A")

writetype("P-80/F-80/AT-33 Shooting Star")  # 1945
writeadc("F-80C")
writeadc("RF-80C")
writeadc("AT-33A")

writetype("AD/A-1 Skyraider")  # 1946
writeadc("AD-4")
writeadc("AD-5")
writeadc("A-1E")
writeadc("AD-6")
writeadc("A-1H")
writeadc("AD-7")
writeadc("A-1J")

writetype("F-84 Thunderjet")  # 1947
writeadc("F-84E")
writeadc("F-84G")

writetype("F2H Banshee")  # 1948
writeadc("F2H-2")
writeadc("F2H-2P")
writeadc("F2H-2B")
writeadc("F2H-2B (ATA Refueling)")
writeadc("F2H-3")
writeadc("F2H-3 (ATA Refueling)")
writeadc("F2H-3 (RCN)")
writeadc("F2H-4")
writeadc("F2H-4 (ATA Refueling)")

writetype("F9F Panther")  # 1947
writeadc("F9F-2 (Early)")
writeadc("F9F-2 (Late)")
writeadc("F9F-2P")
writeadc("F9F-5")
writeadc("F9F-5P")

writetype("F-86 Sabre")  # 1949
writeadc("F-86A")
writeadc("F-86D")
writeadc("F-86E")
writeadc("F-86F-10")
writeadc("F-86F-25")
writeadc("F-86F-35")
writeadc("F-86F-40")
writeadc("F-86H (Early)")
writeadc("F-86H (Late)")
writeadc("F-86K (Early)")
writeadc("F-86K (Late)")
writeadc("F-86L")

if False:


    writetype("B-52 Stratofortress")  # 1954
    writeadc("B-52D")
    writeadc("B-52G")

    writetype("A3D/A-3 Skywarrior")  # 1956
    writeadc("A3D-2")
    writeadc("A-3B")
    writeadc("A3D-2Q")
    writeadc("EA-3B")

    writetype("F4H/F-4A Phantom II")  # 1959
    writeadc("F-4B")
    writeadc("RF-4B")
    writeadc("F-4C")
    writeadc("RF-4C")
    writeadc("F-4E")
    writeadc("F-4J")

    writetype("F-5 Freedom Fighter \\& Tiger II")  # 1964
    writeadc("F-5A")
    writeadc("RF-5A")
    writeadc("F-5C")

    writetype("Harrier \\& Sea Harrier")  # 1969
    writeadc("Sea Harrier FRS.1")
    writeadc("Sea Harrier FRS.2")
    writeadc("Sea Harrier FA.2")

    writetype("Canberra")  # 1954
    writeadc("B-57B-early")
    writeadc("B-57B")
    writeadc("B-57G")

    writetype("MiG-21")  # 1959
    writeadc("MiG-21F-13")
    writeadc("MiG-21F")
    writeadc("MiG-21M")
    writeadc("MiG-21MF")
    writeadc("MiG-21PFMA")

    writecountry("Unsorted Aircraft")

    writetype("A-27 Dragonfly")
    writeadc("A-37B")
    writeadc("OA-37B")
    writeadc("T-37C")

    writetype("B-66 Destroyer")
    writeadc("B-66B")
    writeadc("EB-66C")
    writeadc("RB-66C")

    writetype("F-100 Super Sabre")
    writeadc("F-100A")
    writeadc("F-100C")
    writeadc("F-100D")
    writeadc("F-100F")

    writetype("F-102 Delta Dart")
    writeadc("F-102A")

    writetype("F-104 Star Fighter")
    writeadc("F-104A+")
    writeadc("F-104A")
    writeadc("F-104B")
    writeadc("F-104C")
    writeadc("F-104D")

    writetype("F-105 Thunderchief")
    writeadc("F-105B")
    writeadc("F-105D")

    writetype("F-16 Fighting Falcon \\& Viper")
    writeadc("F-16A-1")
    writeadc("F-16A-10")
    writeadc("F-16A-15")
    writeadc("F-16A-5")

    writetype("F-89 Scorpion")
    writeadc("F-89D")
    writeadc("F-89H")
    writeadc("F-89J Long-Range")
    writeadc("F-89J")

    writetype("F8U/F-8 Crusader")
    writeadc("F-8E")
    writeadc("F-8J")

    writetype("F-94 Starfire")
    writeadc("F-94A")
    writeadc("F-94B")

    writetye("F7U Cutlass")
    writeadc("F7U-3")
    writeadc("F7U-3M")

    writetype("Il-28 Beagle")
    writeadc("Il-28")

    writetype("MiG-15 Fagot")
    writeadc("MiG-15ISh")
    writeadc("MiG-15P")
    writeadc("MiG-15bis")

    writetype("MiG-17 Fresco")
    writeadc("MiG-17F")
    writeadc("MiG-17PF")
    writeadc("MiG-17PFU")

    writetype("MiG-19 Farmer")
    writeadc("MiG-19PF")
    writeadc("MiG-19PM")
    writeadc("MiG-19SF-CS")
    writeadc("MiG-19SF")

    # writeadc("HH-53C")
    # writeadc("O-1E")
    # writeadc("O-2A")

    writetype("Sea Fury")
    writeadc("Sea Fury FB.11")

    writetype("Su-9/11 Fishpot")
    writeadc("Su-9")
    writeadc("Su-11")

    writetype("TU-16 Badger")
    writeadc("Tu-16A")
    writeadc("Tu-16K")
    writeadc("Tu-16KS")

    writetype("Yak-9 Frank")
    writeadc("Yak-9D")

latexfile.close()
