#!/usr/bin/env python3

import re
import sys
import os
import os.path
import json

sys.path.append("../src")
from glass import aircraftdata
import glass.jsonc
import glass.variants

if "version" in os.environ:
    version = int(os.environ["version"])
else:
    version = 1

if version == 1:
    glass.variants.setvariants(["use first-edition ADCs"])
elif version == 2:
    pass
elif version == 3:
    glass.variants.setvariants(["use house rules"])


def log(s):
    print("aircraftdatacards: %s: %s" % (os.path.basename(jsonfilename), s))
    sys.stdout.flush()


def minusify(s):
    # Subsitute minus sign for hyphen where appropriate.
    s = re.sub(r"([^-/0-9a-zA-Z])-([0-9]+)", r"\1−\2", s)
    s = re.sub(r"([0-9]+)-([^-/0-9a-zA-Z])", r"\1−\2", s)
    return s


def writelatex(s):
    print(minusify(s), file=latexfile)


def blockA(data, geometry=None):

    if geometry is None:
        writelatex(r"\renewcommand{\Aaa}{%s}" % data.fullvariantname())
    else:
        writelatex(
            r"\renewcommand{\Aaa}{%s --- %s geometry}"
            % (data.fullvariantname(), geometry)
        )

    splitfullname = re.sub(
        r"\s+(([A-Z][a-z]+([-\s][A-Z][a-z]*)?(\s+II)?)|([A-Za-z]+\.[0-9]+))$",
        r"\\\\\1",
        data.fullname(),
    )
    if data.variantname() is None:
        writelatex(r"\renewcommand{\Aab}{%s}" % data.fullname())
    else:
        writelatex(
            r"\renewcommand{\Aab}{%s\\[0.2em](%s)}"
            % (data.fullname(), data.variantname())
        )

    if data.propellerengines() == 0 and data.jetengines() <= 4:
        writelatex(
            r"\renewcommand{\Ac}{\Acone{%s}}" % (data.jetengines() * r"\jetengine")
        )
    elif data.propellerengines() == 0:
        writelatex(
            r"\renewcommand{\Ac}{\Actwo{%s}{%s}}"
            % (
                ((data.jetengines() // 2) * r"\jetengine"),
                ((data.jetengines() // 2) * r"\jetengine"),
            )
        )
    elif data.jetengines() == 0:
        writelatex(
            r"\renewcommand{\Ac}{\Acone{%s}}"
            % (data.propellerengines() * r"\propellerengine")
        )
    else:
        writelatex(
            r"\renewcommand{\Ac}{\Actwo{%s}{%s}}"
            % (
                (data.jetengines() * r"\jetengine"),
                (data.propellerengines() * r"\propellerengine"),
            )
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
        r"\renewcommand{\Aga}{%s}\renewcommand{\Agb}{%s}\renewcommand{\Agc}{%s}\renewcommand{\Agd}{%s}"
        % (power("CL", "I"), power("1/2", "I"), power("DT", "I"), fuelrate("I")),
    )
    writelatex(
        r"\renewcommand{\Aha}{%s}\renewcommand{\Ahb}{%s}\renewcommand{\Ahc}{%s}"
        % (speedbrake("CL"), speedbrake("1/2"), speedbrake("DT")),
    )

    s = ""
    if data.hasproperty("SMP", geometry):
        s += "Smoker in military power (SMP). "
    if data.powerfade(100, 0) is not None:
        lastpowerfade = 0.0
        speed = 0.0
        while speed < 100:
            powerfade = data.powerfade(speed, 0)
            if powerfade != lastpowerfade:
                s += r"If speed ≥ %.1f, reduce power by %.1f.\\" % (
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
                s += r"If altitude ≥ %d, reduce power by %.1f.\\" % (
                    altitude,
                    powerfade,
                )
            lastpowerfade = powerfade
            altitude += 1
    if data.hasproperty("ABSF", geometry):
        s += "If not using AB, reduce maximum speeds by %.1f." % data.ABSFamount(
            geometry
        )

    writelatex(
        r"\renewcommand{\Ai}{%s}" % s,
    )


def blockB(data, geometry=None):

    def arcs(arcs):
        if len(arcs) == 0:
            return "---"
        elif len(arcs) == 1:
            return r"%s" % arcs[0]
        else:
            return r"\twoarcs{%s}{%s}" % (arcs[0], arcs[1])

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


def blockC(data, geometry=None):

    def crew():
        if len(data.crew()) == 1:
            return data.crew()[0]
        elif len(data.crew()) == 2:
            return data.crew()[0] + r" and " + data.crew()[1]
        else:
            return ", ".join(data.crew()[0:-1]) + r", and " + data.crew()[-1]

    writelatex(r"\renewcommand{\Ccrew}{%s}" % crew())
    if len(data.crew()) >= 10:
        writelatex(r"\renewcommand{\Ccrewfont}{\tiny}")
    elif len(data.crew()) >= 3:
        writelatex(r"\renewcommand{\Ccrewfont}{\footnotesize}")

    elif len(data.crew()) >= 2:
        writelatex(r"\renewcommand{\Ccrewfont}{\small}")
    else:
        writelatex(r"\renewcommand{\Ccrewfont}{\normalsize}")

    def rollhfp():
        value = data.rollhfp()
        if value == None:
            return "---"
        else:
            return r"%.1f" % value

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

        drag = data.turndrag(configuration, geometry, turnrate)
        if drag is None:
            return "---"
        if data.lowspeedliftdevicename() is None:
            return formatdrag(drag)
        else:
            lowspeedliftdevicedrag = data.turndrag(
                configuration, geometry, turnrate, lowspeedliftdevice=True
            )
            return "%s/%s" % (formatdrag(drag), formatdrag(lowspeedliftdevicedrag))

    if version == 3:
        writelatex(r"\renewcommand{\Caa}{}")
    else:
        writelatex(r"\renewcommand{\Caa}{%s}" % rollhfp())
    writelatex(r"\renewcommand{\Cab}{%s}" % maneuverdrag("DR"))
    writelatex(r"\renewcommand{\Cb}{%s}" % maneuverdrag("VR"))

    precision = 0
    values = [
        data.turndrag("CL", geometry, "TT"),
        data.turndrag("1/2", geometry, "TT"),
        data.turndrag("DT", geometry, "TT"),
        data.turndrag("CL", geometry, "HT"),
        data.turndrag("1/2", geometry, "HT"),
        data.turndrag("DT", geometry, "HT"),
        data.turndrag("CL", geometry, "BT"),
        data.turndrag("1/2", geometry, "BT"),
        data.turndrag("DT", geometry, "BT"),
        data.turndrag("CL", geometry, "ET"),
        data.turndrag("1/2", geometry, "ET"),
        data.turndrag("DT", geometry, "ET"),
    ]
    if data.lowspeedliftdevicename() is not None:
        values += [
            data.turndrag("CL", geometry, "TT", lowspeedliftdevice=True),
            data.turndrag("1/2", geometry, "TT", lowspeedliftdevice=True),
            data.turndrag("DT", geometry, "TT", lowspeedliftdevice=True),
            data.turndrag("CL", geometry, "HT", lowspeedliftdevice=True),
            data.turndrag("1/2", geometry, "HT", lowspeedliftdevice=True),
            data.turndrag("DT", geometry, "HT", lowspeedliftdevice=True),
            data.turndrag("CL", geometry, "BT", lowspeedliftdevice=True),
            data.turndrag("1/2", geometry, "BT", lowspeedliftdevice=True),
            data.turndrag("DT", geometry, "BT", lowspeedliftdevice=True),
            data.turndrag("CL", geometry, "ET", lowspeedliftdevice=True),
            data.turndrag("1/2", geometry, "ET", lowspeedliftdevice=True),
            data.turndrag("DT", geometry, "ET", lowspeedliftdevice=True),
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
                r"Selectable %s. If selected and speed ≤ "
                % data.lowspeedliftdevicename()
            )
        else:
            s += r"Automatic %s. If speed ≤ " % data.lowspeedliftdevicename()
        if data.lowspeedliftdevicelimittype() == "absolute":
            s += r"%.1f," % data.lowspeedliftdevicelimit()
        else:
            s += r"minimum + %.1f," % data.lowspeedliftdevicelimit()
        if data.lowspeedliftdeviceminspeedchange() is None:
            s += r" use higher drag."
        else:
            s += (
                r" use higher drag and reduce minimum speeds by %.1f."
                % data.lowspeedliftdeviceminspeedchange()
            )
    if data.hasproperty("NRM", geometry):
        s += r"No rolling maneuvers allowed."
    if data.hasproperty("OVR", geometry):
        s += r"Only one vertical roll allowed per game turn."
    if (
        data.hasproperty("NDRHS", geometry)
        and data.hasproperty("NDRHS", geometry)
        and data.NDRHSlimit(geometry) == data.NDRHSlimit(geometry)
    ):
        s += r"No lag or displacement rolls if speed ≥ %.1f. " % data.NDRHSlimit(
            geometry
        )
    else:
        if data.hasproperty("NDRHS", geometry):
            s += r"No displacement rolls if speed ≥ %.1f. " % data.NDRHSlimit(geometry)
        if data.hasproperty("NLRHS", geometry):
            s += r"No lag rolls if speed ≥ %.1f. " % data.NLRHSlimit(geometry)
    if data.hasproperty("RMCL", geometry):
        s += r"Rolling maneuvers only if CL."

    writelatex(r"\renewcommand{\Cg}{%s}" % s)


def blockD(data, geometry=None):

    def speeds(configuration, altitudeband):
        if data.minspeed(configuration, geometry, altitudeband) is None:
            return "---"
        else:
            width = {
                "CL": "\\Dba",
                "1/2": "\\Dbb",
                "DT": "\\Dbc",
            }
            return r"\blockDminmaxspeed{%.1f}{%.1f}{%s}" % (
                data.minspeed(configuration, geometry, altitudeband),
                data.maxspeed(configuration, geometry, altitudeband),
                width[configuration],
            )

    def divespeed(altitudeband):
        if data.maxdivespeed(geometry, altitudeband) is None:
            return "---"
        else:
            return r"\blockDdivespeed{%.1f}" % data.maxdivespeed(geometry, altitudeband)

    maxspeed = 0
    if data.maxspeed("CL", geometry, "EH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("CL", geometry, "EH"))
    if data.maxspeed("CL", geometry, "VH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("CL", geometry, "VH"))
    if data.maxspeed("CL", geometry, "HI") is not None:
        maxspeed = max(maxspeed, data.maxspeed("CL", geometry, "HI"))
    if data.maxspeed("CL", geometry, "MH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("CL", geometry, "MH"))
    if data.maxspeed("CL", geometry, "ML") is not None:
        maxspeed = max(maxspeed, data.maxspeed("CL", geometry, "ML"))
    if data.maxspeed("CL", geometry, "LO") is not None:
        maxspeed = max(maxspeed, data.maxspeed("CL", geometry, "LO"))
    writelatex(r"\renewcommand{\Dba}{%.1f}" % maxspeed)

    maxspeed = 0
    if data.maxspeed("1/2", geometry, "EH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("1/2", geometry, "EH"))
    if data.maxspeed("1/2", geometry, "VH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("1/2", geometry, "VH"))
    if data.maxspeed("1/2", geometry, "HI") is not None:
        maxspeed = max(maxspeed, data.maxspeed("1/2", geometry, "HI"))
    if data.maxspeed("1/2", geometry, "MH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("1/2", geometry, "MH"))
    if data.maxspeed("1/2", geometry, "ML") is not None:
        maxspeed = max(maxspeed, data.maxspeed("1/2", geometry, "ML"))
    if data.maxspeed("1/2", geometry, "LO") is not None:
        maxspeed = max(maxspeed, data.maxspeed("1/2", geometry, "LO"))
    writelatex(r"\renewcommand{\Dbb}{%.1f}" % maxspeed)

    maxspeed = 0
    if data.maxspeed("DT", geometry, "EH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("DT", geometry, "EH"))
    if data.maxspeed("DT", geometry, "VH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("DT", geometry, "VH"))
    if data.maxspeed("DT", geometry, "HI") is not None:
        maxspeed = max(maxspeed, data.maxspeed("DT", geometry, "HI"))
    if data.maxspeed("DT", geometry, "MH") is not None:
        maxspeed = max(maxspeed, data.maxspeed("DT", geometry, "MH"))
    if data.maxspeed("DT", geometry, "ML") is not None:
        maxspeed = max(maxspeed, data.maxspeed("DT", geometry, "ML"))
    if data.maxspeed("DT", geometry, "LO") is not None:
        maxspeed = max(maxspeed, data.maxspeed("DT", geometry, "LO"))
    writelatex(r"\renewcommand{\Dbc}{%.1f}" % maxspeed)

    maxspeed = 0
    if data.maxdivespeed(geometry, "EH") is not None:
        maxspeed = max(maxspeed, data.maxdivespeed(geometry, "EH"))
    if data.maxdivespeed(geometry, "VH") is not None:
        maxspeed = max(maxspeed, data.maxdivespeed(geometry, "VH"))
    if data.maxdivespeed(geometry, "HI") is not None:
        maxspeed = max(maxspeed, data.maxdivespeed(geometry, "HI"))
    if data.maxdivespeed(geometry, "MH") is not None:
        maxspeed = max(maxspeed, data.maxdivespeed(geometry, "MH"))
    if data.maxdivespeed(geometry, "ML") is not None:
        maxspeed = max(maxspeed, data.maxdivespeed(geometry, "ML"))
    if data.maxdivespeed(geometry, "LO") is not None:
        maxspeed = max(maxspeed, data.maxdivespeed(geometry, "LO"))
    writelatex(r"\renewcommand{\Dbd}{%.1f}" % maxspeed)

    writelatex(
        r"\renewcommand{\Daa}{\blockDceiling{%d}}\renewcommand{\Dab}{\blockDceiling{%d}}\renewcommand{\Dac}{\blockDceiling{%d}}"
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


def blockE(data, geometry=None):

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


def blockF(data, geometry=None):

    if data.radar() is None:
        # no radar
        writelatex(r"\renewcommand{\Fa}{---}")
        writelatex(r"\renewcommand{\Fb}{---}")
        writelatex(r"\renewcommand{\Fc}{---}")
        writelatex(r"\renewcommand{\Fd}{---}")
        writelatex(r"\renewcommand{\Fe}{---}")
        writelatex(r"\renewcommand{\Ff}{---}")
    elif data.radar("arc") is None:
        # ranging only radar
        writelatex(r"\renewcommand{\Fa}{%s}" % data.radar("name"))
        writelatex(r"\renewcommand{\Fb}{---}")
        writelatex(r"\renewcommand{\Fc}{---}")
        writelatex(r"\renewcommand{\Fd}{---}")
        writelatex(r"\renewcommand{\Fe}{---}")
        writelatex(r"\renewcommand{\Ff}{%d}" % data.radar("lockon"))
    elif (
        data.radar("searchstrength") is None and data.radar("trackingstrength") is None
    ):
        # air-to-ground radar
        writelatex(r"\renewcommand{\Fa}{%s}" % data.radar("name"))
        writelatex(r"\renewcommand{\Fb}{%d}" % data.radar("eccm"))
        writelatex(r"\renewcommand{\Fc}{%s}" % data.radar("arc"))
        writelatex(r"\renewcommand{\Fd}{Gr.~Nav.~(%d)}" % data.radar("searchrange"))
        if data.radar("trackingrange") is None:
            writelatex(r"\renewcommand{\Fe}{---}")
        else:
            writelatex(
                r"\renewcommand{\Fe}{Gr.~Attack~ (%d)}" % data.radar("trackingrange")
            )
        if data.radar("lockon") is None:
            writelatex(r"\renewcommand{\Ff}{---}")
        else:
            writelatex(r"\renewcommand{\Ff}{%d}" % data.radar("lockon"))
    else:
        # air-to-air radar without search capability
        writelatex(r"\renewcommand{\Fa}{%s}" % data.radar("name"))
        writelatex(r"\renewcommand{\Fb}{%d}" % data.radar("eccm"))
        writelatex(r"\renewcommand{\Fc}{%s}" % data.radar("arc"))
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
        if data.radar("lockon") is None:
            writelatex(r"\renewcommand{\Ff}{---}")
        else:
            writelatex(r"\renewcommand{\Ff}{%d}" % data.radar("lockon"))

    if data.gun() is None:
        writelatex(r"\renewcommand{\Fg}{---}")
        writelatex(r"\renewcommand{\Fh}{---}")
        writelatex(r"\renewcommand{\Fi}{---}")
        writelatex(r"\renewcommand{\Fl}{---}")
    else:
        s = data.gun()
        if " and " in s:
            prefix = r"\parbox{\linewidth}{\centering\scriptsize "
            suffix = r"}"
            s = re.sub(r"and one", r"\\\\One", s)
            s = re.sub(r"and two", r"\\\\Two", s)
            s = re.sub(r"and three", r"\\\\Three", s)
            s = re.sub(r"and four", r"\\\\Four", s)
        else:
            prefix = ""
            suffix = ""
        s = re.sub(r"\. ", r".~", s)
        s = re.sub(r" mm", r"~mm", s)
        writelatex(r"\renewcommand{\Fg}{%s%s%s}" % (prefix, s, suffix))
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
        if data.gunatgdamagerating()[-1] == "_":
            writelatex(
                r"\renewcommand{\Fl}{%d/\underline{%s}}"
                % (data.gunatadamagerating(), data.gunatgdamagerating()[:-1])
            )
        else:
            writelatex(
                r"\renewcommand{\Fl}{%d/%s}"
                % (data.gunatadamagerating(), data.gunatgdamagerating())
            )

    s = data.bombsystem().capitalize()
    if "/" in s:
        prefix = r"\parbox{\linewidth}{\centering\scriptsize "
        suffix = r"}"
        s = re.sub(r"/", r"\\\\", s)
    else:
        prefix = ""
        suffix = ""
    writelatex(r"\renewcommand{\Fm}{%s%s%s}" % (prefix, s, suffix))

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
        writelatex(r"\renewcommand{\Fn}{IFF}")
    else:
        writelatex(r"\renewcommand{\Fn}{}")
    if data.ecm("rwr") is not None:
        writelatex(r"\renewcommand{\Fo}{%s}" % data.ecm("rwr"))
    else:
        writelatex(r"\renewcommand{\Fo}{---}")
    if data.ecm("dds") is not None:
        writelatex(r"\renewcommand{\Fp}{%s}" % data.ecm("dds"))
    else:
        writelatex(r"\renewcommand{\Fp}{---}")
    if data.ecm("djm") is not None:
        writelatex(r"\renewcommand{\Fq}{%s}" % data.ecm("djm"))
    else:
        writelatex(r"\renewcommand{\Fq}{---}")
    if data.ecm("ajm") is not None:
        writelatex(r"\renewcommand{\Fr}{%s}" % data.ecm("ajm"))
    else:
        writelatex(r"\renewcommand{\Fr}{---}")
    if data.ecm("bjm") is not None:
        writelatex(r"\renewcommand{\Fs}{%s}" % data.ecm("bjm"))
    else:
        writelatex(r"\renewcommand{\Fs}{---}")

    technologylist = []
    if data.technology() is not None:
        technologylist += data.technology()
    if len(technologylist) == 0:
        s = "None"
    elif len(technologylist) == 1:
        s = technologylist[0]
    elif len(technologylist) == 2:
        s = " and ".join(technologylist)
    else:
        s = ", ".join(technologylist[:-1]) + ", and " + technologylist[-1]
    writelatex(r"\renewcommand{\Ft}{%s}" % s)

    s = ""

    if data.description() is not None:
        s += "\\item %s\n\n" % data.description()

    if data.hasproperty("EVG", geometry):
        s += "\\item This is a variable-geometry aircraft with allowed geometries of "
        geometries = data.geometries()
        if len(geometries) == 2:
            s += geometries[0] + " and " + geometries[1]
        else:
            s += ", ".join(geometries[:-1])
            s += ", and " + geometries[-1]
        s += "."
        if data.hasproperty("EVGA", geometry):
            s += " The geometry changes automatically at the end of each turn according to the speed."
        if data.hasproperty("EVG1", geometry):
            s += " The geometry may be changed by one step at the end of each turn."
        if data.hasproperty("EVGTT", geometry):
            s += " The geometry may be changed at the end of the aircraft’s move if the maximum turn rate used is TT or less."
        if data.hasproperty("EVGA", geometry):
            s += (
                " The data shown here are for the %s geometry and are used if the speed is "
                % geometry
            )
            if data.geometryminspeed(geometry) is None:
                s += "%.1f or less." % data.geometrymaxspeed(geometry)
            elif data.geometrymaxspeed(geometry) is None:
                s += "%.1f or more." % data.geometryminspeed(geometry)
            else:
                s += "%.1f to %.1f." % (
                    data.geometryminspeed(geometry),
                    data.geometrymaxspeed(geometry),
                )
        else:
            s += " The data shown here are for the %s geometry." % geometry

    if len(data.properties(geometry)) != 0:
        t = ""
        for property in sorted(data.properties(geometry)):
            if property == "ABSF" or property == "SMP":
                # Noted in power section.
                pass
            elif (
                property == "OVR"
                or property == "NRM"
                or property == "NDRHS"
                or property == "NLRHS"
                or property == "RMCL"
            ):
                # Noted in maneuver section.
                pass
            elif (
                property == "EVG"
                or property == "EVG1"
                or property == "EVGA"
                or property == "EVGTT"
            ):
                # Noted immediately above.
                pass
            else:
                if property == "GSSM":
                    t += r"Good supersonic maneuverability (GSSM). "
                elif property == "HAE":
                    t += r"High altitude engines (HAE). "
                elif property == "HBR":
                    t += r"High bleed rate (HBR). "
                elif property == "HPR":
                    t += r"High pitch rate (HPR). "
                elif property == "HRR":
                    t += r"High roll rate (HRR). "
                elif property == "HRRCL":
                    t += r"High roll rate (HRR) if CL. "
                elif property == "HTD":
                    t += r"High transonic drag (HTD). "
                elif property == "LBR":
                    t += r"Low bleed rate (LBR). "
                elif property == "LRR":
                    t += r"Low roll rate (LRR). "
                elif property == "LRRHS":
                    t += (
                        r"Low roll rate (LRR) if speed ≥ %.1f. "
                        % data._data["LRRHSlimit"]
                    )
                elif property == "LTD":
                    t += r"Low transonic drag (LTD). "
                elif property == "LTDCL":
                    t += r"Low transonic drag (LTD) if CL. "
                elif property == "PSSM":
                    t += r"Poor supersonic maneuverability (PSSM). "
                elif property == "RA":
                    t += r"Rapid acceleration (RA). "
                elif property == "RACL":
                    t += r"Rapid acceleration (RA) if CL. "
                elif property == "RALS":
                    t += (
                        r"Rapid acceleration (RA) if speed ≤ %.1f. "
                        % data._data["RALSlimit"]
                    )
                elif property == "RPR":
                    t += r"Rapid power response (RPR). "
                elif property == "FBW":
                    t += r"Fly-by-wire (FBW). "
                else:
                    log("unknown property: %s" % property)
                    t += "%s. " % property

        if t != "":
            s += r"\item %s" % t

    for note in data.notes():
        s += "\\item %s\n\n" % note

    for note in data.typenotes():
        s += "\\item %s\n\n" % note

    for note in data.versionnotes():
        s += "\\item %s\n\n" % note

    for note in data.variantnotes():
        s += "\\item %s\n\n" % note

    if s == "":
        writelatex(r"\renewcommand{\Fu}{}")
    else:
        writelatex(r"\renewcommand{\Fu}{\Fua{%s}}" % s)


def blockG(data, geometry=None):

    if not data.hasstoreslimits():
        writelatex(r"\renewcommand{\Gba}{}")
        writelatex(r"\renewcommand{\Gbb}{}")
        writelatex(r"\renewcommand{\Gbc}{}")
        writelatex(r"\renewcommand{\Gbd}{}")
    elif version != 3:
        writelatex(r"\renewcommand{\Gba}{\wbox[r]{00}{0}--%d}" % data.storeslimit("CL"))
        writelatex(
            r"\renewcommand{\Gbb}{\wbox[r]{00}{%d}--%d}"
            % (data.storeslimit("CL") + 1, data.storeslimit("1/2"))
        )
        writelatex(
            r"\renewcommand{\Gbc}{\wbox[r]{00}{%d}+}" % (data.storeslimit("1/2") + 1)
        )
        writelatex(r"\renewcommand{\Gbd}{%s}" % ("{:,}".format(data.storeslimit("DT"))))
    else:
        writelatex(
            r"\renewcommand{\Gba}{<\wbox[r]{00}{%d}}" % (data.storeslimit("CL") + 1)
        )
        writelatex(
            r"\renewcommand{\Gbb}{<\wbox[r]{00}{%d}}" % (data.storeslimit("1/2") + 1)
        )
        writelatex(
            r"\renewcommand{\Gbc}{≥\wbox[r]{00}{%d}}" % (data.storeslimit("1/2") + 1)
        )
        writelatex(r"\renewcommand{\Gbd}{%s}" % ("{:,}".format(data.storeslimit("DT"))))

    s = ""
    for station in data.stations():
        stationtype = station[0]
        stationidentifiers = station[1]
        stationlimit = station[2]
        stationloads = station[3]
        if stationtype == "single":
            s += "%s" % stationidentifiers[0]
        elif stationtype == "pair":
            s += "%s and %s" % tuple(stationidentifiers)
        elif stationtype == "group":
            s += "%s--%s" % tuple(stationidentifiers)
        elif stationtype == "grouppair":
            s += "%s--%s and %s--%s" % tuple(stationidentifiers)
        s += "&%s&%s\\\\\n" % (
            "{:,}".format(stationlimit),
            r"\mbox{" + r"} \mbox{".join(stationloads) + r"}",
        )
    writelatex(r"\renewcommand{\Gca}{%s}" % s)

    s = ""
    for note in data.loadnotes():
        s += "\\item %s\n\n" % note
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

    writelatex(r"\renewcommand{\Gea}{%s}" % data.commitabbreviatedhash())
    writelatex(r"\renewcommand{\Geb}{%s}" % data.commitdatetime())


def writechapter(name):
    log("writing chapter %s." % name)
    writelatex(r"\twocolumn\chapter{%s}" % name)


def writetype(name):
    if name is not None:
        log("writing type %s." % name)
        file = "../src/glass/aircraftdata/" + name.replace("/", ":") + ".tex"
        if os.path.exists(file):
            writelatex(r"\input{%s}" % file)
        else:
            raise RuntimeError("%s does not exist." % file)


def writeadc(name):

    writelatex(r"\clearpage")
    log("writing variant %s." % name)
    writelatex("%% %s" % name)

    data = aircraftdata.aircraftdata(name)

    labelled = False
    for geometry in data.geometries():
        blockA(data, geometry=geometry)
        blockB(data, geometry=geometry)
        blockC(data, geometry=geometry)
        blockD(data, geometry=geometry)
        blockE(data, geometry=geometry)
        blockF(data, geometry=geometry)
        blockG(data, geometry=geometry)
        writelatex(r"\adc")
        if not labelled:
            writelatex(r"\adclabel{%s}" % name)
            labelled = True


def writelatexprolog(withtableofcontents):
    writelatex(
        r"""
%%!LW recipe=latexmk (xelatex)
%%!TEX program = xelatex

\documentclass[twocolumn]{report}
\input aircraftdatacards.tex
\newif\ifversionone\versiononefalse
\newif\ifversiontwo\versiontwofalse
\newif\ifversionthree\versionthreefalse
\version%strue
\begin{document}
"""
        % ["one", "two", "three"][version - 1]
    )
    if withtableofcontents:
        writelatex(
            r"""
\tableofcontents
"""
        )
    writelatex(
        r"""
\onecolumn
\newpage
"""
    )


def writelatexepilog():
    writelatex(
        r"""
\end{document}
"""
    )


def readjsonfile(jsonfilename):
    log("reading %s." % os.path.basename(jsonfilename))
    with open(jsonfilename, "r", encoding="utf-8") as f:
        s = f.read(-1)
        # Strip initial #! line.
        if s[:2] == "#!":
            r = re.compile("^#.*$", re.MULTILINE)
            s = re.sub(r, "", s)
        directives = glass.jsonc.loads(s)
    log("finished reading %s." % os.path.basename(jsonfilename))

    return directives


def writelatexfile(latexfilename, directives):
    log("writing %s." % os.path.basename(latexfilename))
    global latexfile
    latexfile = open(latexfilename, "w")
    for directive in directives:
        if directive[0] == "prolog":
            writelatexprolog(directive[1])
        elif directive[0] == "type":
            writetype(directive[1])
            for variant in directive[2:]:
                writeadc(variant)
        elif directive[0] == "example":
            writeadc(directive[1])
        elif directive[0] == "chapter":
            writechapter(directive[1])
        elif directive[0] == "comment":
            pass
        else:
            raise RuntimeError("invalid directive %r." % directive)
    writelatexepilog()
    latexfile.close()
    log("finished writing %s." % os.path.basename(latexfilename))


def makepdffile(latexfilename, pdffilename):
    log("making %s." % pdffilename)
    os.system(
        "xelatex -interaction=nonstopmode "
        + latexfilename
        + " >aircraftdatacards.log 2>&1 || cat aircraftdatacards.log"
    )
    log("finished making %s." % pdffilename)


for jsonfilename in sys.argv[1:]:

    r = re.compile(r"\.json$")
    latexfilename = re.sub(r, ".tex", jsonfilename)
    pdffilename = re.sub(r, ".pdf", jsonfilename)

    directives = readjsonfile(jsonfilename)
    writelatexfile(latexfilename, directives)
    makepdffile(latexfilename, pdffilename)

    log("finished.")


sys.exit(0)
