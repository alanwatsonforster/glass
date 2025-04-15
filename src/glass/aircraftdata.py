import glass.variants

import os.path
import json
import re


def _checkconfiguration(configuration):
    assert configuration in ["CL", "1/2", "DT"]


def _checkpowersetting(powersetting):
    assert powersetting in ["AB", "M", "N", "I", "FT", "HT"]


def _checkturnrate(turnrate):
    assert turnrate in ["EZ", "TT", "HT", "BT", "ET"]


def _checkaltitudeband(altitudeband):
    assert altitudeband in ["LO", "ML", "MH", "HI", "VH", "EH", "UH"]


def _configurationindex(configuration):
    return ["CL", "1/2", "DT"].index(configuration)


class aircraftdata:

    def __init__(self, name):

        def filename(name):
            return os.path.join(
                os.path.dirname(__file__), "aircraftdata", name + ".json"
            )

        def loadfile(name):
            try:
                with open(filename(name), "r", encoding="utf-8") as f:
                    s = f.read(-1)
                    # Strip whole-line // comments.
                    r = re.compile("^[ \t]*//.*$", re.MULTILINE)
                    s = re.sub(r, "", s)
                    return json.loads(s)
            except FileNotFoundError:
                raise RuntimeError(
                    'unable to find aircraft data file for aircraft type "%s".' % name
                )
            except json.JSONDecodeError as e:
                raise RuntimeError(
                    'unable to read aircraft data file for aircraft type "%s": line %d: %s.'
                    % (name, e.lineno, e.msg.lower())
                )

        self._name = name

        data = loadfile(name)
        while "base" in data:
            base = data["base"]
            del data["base"]
            basedata = loadfile(base)
            basedata.update(data)
            data = basedata
        self._data = data

        if False:
            process = os.popen(
                'env TZ=UTC git log -n 1 --date=local --date=format-local:"%%Y-%%m-%%d %%H:%%M.%%SZ" --pretty=format:"%%cd %%h %%H" "%s"'
                % filename(name)
            )
            gitlogoutput = process.read()
            process.close()
        else:
            gitlogoutput = ""
        if gitlogoutput == "":
            gitlogoutput = "0000-00-00 00:00:00 %s %s" % (7 * "0", 40 * "0")
        self._gitlogoutput = gitlogoutput

    def commitdate(self):
        return self._gitlogoutput.split()[0]

    def committime(self):
        return self._gitlogoutput.split()[1]

    def commitdatetime(self):
        return "%sT%s" % (self.commitdate(), self.committime())

    def commitabbreviatedhash(self):
        return self._gitlogoutput.split()[2]

    def commithash(self):
        return self._gitlogoutput.split()[3]

    def manufacturername(self):
        if "manufacturername" in self._data:
            return self._data["manufacturername"]
        else:
            return None

    def versionname(self):
        return self._data["versionname"]

    def popularname(self):
        if "popularname" in self._data:
            return self._data["popularname"]
        else:
            return None

    def variantname(self):
        if "variantname" in self._data:
            return self._data["variantname"]
        else:
            return None

    def fullname(self):
        if self.popularname() is None:
            return "%s" % self.versionname()
        else:
            return "%s %s" % (self.versionname(), self.popularname())

    def fullvariantname(self):
        if self.variantname() is None:
            return "%s" % self.versionname()
        else:
            return "%s (%s)" % (self.versionname(), self.variantname())

    def description(self):
        if "description" in self._data:
            return self._data["description"]
        else:
            return None

    def versiondescription(self):
        if "versiondescription" in self._data:
            return self._data["versiondescription"]
        else:
            return None

    def variantdescription(self):
        if "variantdescription" in self._data:
            return self._data["variantdescription"]
        else:
            return None

    def originallydesignated(self):
        if "originallydesignated" in self._data:
            return self._data["originallydesignated"]
        else:
            return None

    def previouslydesignated(self):
        if "previouslydesignated" in self._data:
            return self._data["previouslydesignated"]
        else:
            return None

    def subsequentlydesignated(self):
        if "subsequentlydesignated" in self._data:
            return self._data["subsequentlydesignated"]
        else:
            return None

    def natoreportingnames(self):
        if "natoreportingnames" in self._data:
            return self._data["natoreportingnames"]
        else:
            return None

    def crew(self):
        return self._data["crew"]

    def power(self, configuration, powersetting):
        _checkconfiguration(configuration)
        _checkpowersetting(powersetting)
        if not powersetting in self._data["powertable"]:
            return None
        elif powersetting == "I":
            if glass.variants.withvariant("use first-edition ADCs"):
                return self._data["powertable"][powersetting][
                    _configurationindex(configuration)
                ]
            else:
                return (
                    self._data["powertable"][powersetting][
                        _configurationindex(configuration)
                    ]
                    * 2
                )
        else:
            return self._data["powertable"][powersetting][
                _configurationindex(configuration)
            ]

    def powerfade(self, speed, altitude):
        if (
            not "powerfadespeedtable" in self._data
            and not "poweraltitudefadetable" in self._data
        ):
            return None
        fadespeed = 0
        fadealtitude = 0
        if "powerfadespeedtable" in self._data:
            for p in self._data["powerfadespeedtable"]:
                if speed > p[0]:
                    fadespeed = p[1]
        if "poweraltitudefadetable" in self._data:
            for p in self._data["poweraltitudefadetable"]:
                if altitude > p[0]:
                    fadealtitude = p[1]
        return fadespeed + fadealtitude

    def speedbrake(self, configuration):
        _checkconfiguration(configuration)
        raw = self._data["powertable"]["SPBR"][_configurationindex(configuration)]
        if raw == "-":
            return None
        elif glass.variants.withvariant("use first-edition ADCs"):
            return raw
        else:
            return raw * 2.0

    def fuelrate(self, powersetting):
        _checkpowersetting(powersetting)
        if not powersetting in self._data["powertable"]:
            return None
        else:
            return self._data["powertable"][powersetting][3]

    def internalfuelcapacity(self):
        if not "internalfuel" in self._data:
            raise RuntimeError(
                "the internal fuel capacity is not specified for this aircraft type."
            )
        return self._data["internalfuel"]

    def engines(self):
        return self.jetengines() + self.propellerengines()

    def jetengines(self):
        if "jetengines" in self._data:
            return self._data["jetengines"]
        else:
            return 0

    def propellerengines(self):
        if "propellerengines" in self._data:
            return self._data["propellerengines"]
        else:
            return 0

    def lowspeedliftdeviceselectable(self):
        if "lowspeedliftdeviceselectable" in self._data:
            return self._data["lowspeedliftdeviceselectable"]
        else:
            return False

    def lowspeedliftdevicelimittype(self):
        if "lowspeedliftdevicelimittype" in self._data:
            return self._data["lowspeedliftdevicelimittype"]
        else:
            return None

    def lowspeedliftdevicelimit(self):
        if "lowspeedliftdevicelimit" in self._data:
            return self._data["lowspeedliftdevicelimit"]
        else:
            return None

    def lowspeedliftdevicename(self):
        if "lowspeedliftdevicename" in self._data:
            return self._data["lowspeedliftdevicename"]
        else:
            return None

    def lowspeedliftdeviceminspeedchange(self):
        if "lowspeedliftdeviceminspeedchange" in self._data:
            return self._data["lowspeedliftdeviceminspeedchange"]
        else:
            return None

    def geometries(self):
        if "geometries" in self._data:
            return list(self._data["geometries"].keys())
        else:
            return [None]

    def turndrag(self, configuration, geometry, turnrate, lowspeedliftdevice=False):
        _checkconfiguration(configuration)
        _checkturnrate(turnrate)
        if lowspeedliftdevice:
            table = "lowspeedliftdeviceturndragtable"
        else:
            table = "turndragtable"
        if not turnrate in self._data[table]:
            return None
        if geometry is None:
            turndragtable = self._data[table]
        else:
            turndragtable = self._data["geometries"][geometry][table]
        raw = turndragtable[turnrate][_configurationindex(configuration)]
        if raw == "-":
            return None
        elif glass.variants.withvariant("use house rules"):
            if self.hasproperty("LBR", geometry):
                return raw / 2.0 + 0.25
            elif self.hasproperty("HBR", geometry):
                return raw / 2.0 + 0.75
            else:
                return raw / 2.0 + 0.5
        else:
            return raw

    def minspeed(self, configuration, geometry, altitudeband):
        _checkconfiguration(configuration)
        _checkaltitudeband(altitudeband)
        if altitudeband == "UH":
            altitudeband = "EH"
        if geometry is None:
            speedtable = self._data["speedtable"]
        else:
            speedtable = self._data["geometries"][geometry]["speedtable"]
        raw = speedtable[altitudeband][_configurationindex(configuration)][0]
        if raw == "-":
            return None
        else:
            return raw

    def maxspeed(self, configuration, geometry, altitudeband):
        _checkconfiguration(configuration)
        _checkaltitudeband(altitudeband)
        if altitudeband == "UH":
            altitudeband = "EH"
        if geometry is None:
            speedtable = self._data["speedtable"]
        else:
            speedtable = self._data["geometries"][geometry]["speedtable"]
        raw = speedtable[altitudeband][_configurationindex(configuration)][1]
        if raw == "-":
            return None
        else:
            return raw

    def maxdivespeed(self, altitudeband):
        _checkaltitudeband(altitudeband)
        if altitudeband == "UH":
            altitudeband = "EH"
        raw = self._data["speedtable"][altitudeband][3]
        if raw == "-":
            return None
        else:
            return raw

    def ceiling(self, configuration):
        _checkconfiguration(configuration)
        return self._data["ceilingtable"][_configurationindex(configuration)]

    def cruisespeed(self, configuration):
        basecruisespeed = self._data["cruisespeed"]
        if configuration == "CL":
            return basecruisespeed
        elif configuration == "1/2":
            return basecruisespeed - 0.5
        else:
            return basecruisespeed - 1.0

    def climbspeed(self):
        return self._data["climbspeed"]

    def sizemodifier(self):
        return self._data["sizemodifier"]

    def vulnerability(self):
        return self._data["vulnerability"]

    def visibility(self):
        return self._data["visibility"]

    def blindarcs(self):
        if self._data["blindarcs"] == "":
            return []
        else:
            return self._data["blindarcs"].split("/")

    def restrictedarcs(self):
        if self._data["restrictedarcs"] == "":
            return []
        else:
            return self._data["restrictedarcs"].split("/")

    def visibility(self):
        return self._data["visibility"]

    def atarefuel(self):
        return self._data["atarefuel"]

    def ejectionseat(self):
        return self._data["ejectionseat"]

    def rollhfp(self):
        raw = self._data["maneuvertable"]["LR/DR"][0]
        if raw == "-":
            return None
        else:
            return raw

    def rolldrag(self, rolltype):
        assert rolltype in ["VR", "LR", "DR"]
        if rolltype != "VR":
            rolltype = "LR/DR"
        raw = self._data["maneuvertable"][rolltype][1]
        if raw == "-":
            return None
        else:
            return raw

    def properties(self, geometry):
        if geometry is None:
            return set(self._data["properties"])
        else:
            return set(
                self._data["geometries"][geometry]["properties"]
                + self._data["properties"]
            )

    def hasproperty(self, p, geometry):
        return p in self.properties(geometry)

    def climbcapability(self, configuration, altitudeband, powersetting):
        _checkaltitudeband(altitudeband)
        _checkpowersetting(powersetting)
        if altitudeband == "UH":
            altitudeband = "EH"
        if powersetting == "AB":
            powersettingindex = 0
        else:
            powersettingindex = 1
        raw = self._data["climbcapabilitytable"][altitudeband][
            _configurationindex(configuration)
        ][powersettingindex]
        if raw == "-":
            return None
        else:
            return raw

    def specialclimbcapability(self):
        if "specialclimbcapability" in self._data:
            return self._data["specialclimbcapability"]
        else:
            return 1

    def radar(self, what=None):
        if "radar" not in self._data or self._data["radar"] is None:
            return None
        elif what is None:
            return True
        elif what in self._data["radar"]:
            return self._data["radar"][what]
        else:
            return None

    def gun(self):
        if "gun" in self._data and self._data["gun"] != "":
            return self._data["gun"]
        else:
            return None

    def gunarc(self):
        if "gunarc" in self._data:
            return self._data["gunarc"]
        else:
            return None

    def gunammunition(self):
        if "gunammunition" in self._data:
            return self._data["gunammunition"]
        else:
            return 0

    def gunsightmodifier(self, turnrate):
        if "gunsightmodifiers" not in self._data:
            return None
        elif turnrate not in self._data["gunsightmodifiers"]:
            return None
        else:
            return self._data["gunsightmodifiers"][turnrate]

    def gunatatohitroll(self, range):
        if "gunatatohitrolls" in self._data:
            tohitroll = self._data["gunatatohitrolls"].split("/")[range]
            if tohitroll == "-":
                tohitroll = None
            else:
                tohitroll = int(tohitroll)
            return tohitroll
        else:
            return None

    def ataradarrangingtype(self):
        if "ataradarranging" not in self._data:
            return None
        elif self._data["ataradarranging"] is None:
            return None
        else:
            assert self._data["ataradarranging"] in ["RE", "CA", "IG"]
            return self._data["ataradarranging"]

    def gunatadamagerating(self):
        if "gundamagerating" in self._data:
            return int(self._data["gundamagerating"].split("/")[0])
        else:
            return None

    def gunatgdamagerating(self):
        if "gundamagerating" in self._data:
            return self._data["gundamagerating"].split("/")[1]
        else:
            return None

    def lockon(self):
        return self.radar("lockon")

    def bombsystem(self):
        if "bombsystem" in self._data:
            return self._data["bombsystem"].lower()
        else:
            return "manual"

    def ecm(self, what):
        if "ecm" not in self._data or self._data["ecm"] is False:
            return None
        elif what not in self._data["ecm"]:
            return None
        else:
            return self._data["ecm"][what]

    def technology(self):
        if (
            "technology" not in self._data
            or self._data["technology"] is False
            or len(self._data["technology"]) == 0
        ):
            return None
        else:
            return self._data["technology"]

    def ABSFamount(self, geometry):
        if "ABSF" in self.properties(geometry):
            return self._data["ABSFamount"]
        else:
            return None

    def NDRHSlimit(self, geometry):
        if "NDRHS" in self.properties(geometry):
            return self._data["NDRHSlimit"]
        else:
            return None

    def NLRHSlimit(self, geometry):
        if "NLRHS" in self.properties(geometry):
            return self._data["NLRHSlimit"]
        else:
            return None

    def rocketfactors(self):
        if "rocketfactors" in self._data:
            return self._data["rocketfactors"]
        else:
            return 0

    def hasstoreslimits(self):
        """
        Return True if the aircraft data has a stores limit specified.
        """
        return "storeslimits" in self._data

    def storeslimit(self, configuration):
        """
        Return the stores limit for the given configuration. If
        configuration is "CL" or "1/2", return the load point limit. If
        configuration is "DT", return the weight limit.
        """

        assert configuration in ["CL", "1/2", "DT"]
        assert self.hasstoreslimits()

        if configuration == "CL":
            return self._data["storeslimits"][0]
        elif configuration == "1/2":
            return self._data["storeslimits"][1]
        elif configuration == "DT":
            return self._data["storeslimits"][2]

    def stations(self):
        """
        Return the stations list.
        """
        if "stations" in self._data:
            return self._data["stations"]
        else:
            return []

    def loadnotes(self):
        """
        Return the load notes list.
        """
        if "loadnotes" in self._data:
            return self._data["loadnotes"]
        else:
            return []

    def hasVPs(self):
        """
        Return True if the aircraft data has VPs specified.
        """
        return "VPs" in self._data

    def VPs(self, damage):
        """
        Return the VPs.
        """

        assert damage in ["K", "C", "H", "L"]
        assert self.hasVPs()

        if damage == "K":
            return self._data["VPs"][0]
        elif damage == "C":
            return self._data["VPs"][1]
        elif damage == "H":
            return self._data["VPs"][2]
        elif damage == "L":
            return self._data["VPs"][3]

    def wikiurl(self):
        if "wikiurl" in self._data:
            return self._data["wikiurl"]
        else:
            return None

    def notes(self):
        if "notes" in self._data:
            return self._data["notes"]
        else:
            return []

    def typenotes(self):
        if "typenotes" in self._data:
            return self._data["typenotes"]
        else:
            return []

    def versionnotes(self):
        if "versiontnotes" in self._data:
            return self._data["versiontnotes"]
        else:
            return []

    def variantnotes(self):
        if "variantnotes" in self._data:
            return self._data["variantnotes"]
        else:
            return []

    ##############################################################################
