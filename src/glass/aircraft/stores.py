################################################################################

import glass.log

################################################################################

_storedict = {

    ############################################################################

    # FTs

    # In the value, [0] is the class, [1] is the weight, and [2] is the
    # load. For FTs, [3] is the empty load and [4] is the fuel capacity.
    # FTs

    "FT/250L"   : [ "FT",   550,  1.5,  1.0,  25 ],
    "FT/310L"   : [ "FT",   670,  1.0,  1.0,  27 ],
    "FT/400L"   : [ "FT",   700,  2.0,  1.0,  30 ],
    "FT/450L"   : [ "FT",   800,  2.5,  1.5,  40 ],
    "FT/600L"   : [ "FT",  1100,  3.0,  2.0,  50 ],
    "FT/700L"   : [ "FT",  1300,  3.0,  2.0,  60 ],
    "FT/850L"   : [ "FT",  1500,  3.5,  2.5,  75 ],
    "FT/1000L"  : [ "FT",  1800,  3.5,  2.5,  85 ],
    "FT/1200L"  : [ "FT",  2200,  4.0,  2.5, 100 ],
    "FT/1250L"  : [ "FT",  2300,  4.0,  2.5, 105 ],
    "FT/1400L"  : [ "FT",  2700,  4.0,  3.0, 120 ],
    "FT/1700L"  : [ "FT",  3000,  5.0,  3.5, 140 ],
    "FT/1800L"  : [ "FT",  3200,  5.0,  3.5, 150 ],
    "FT/1900L"  : [ "FT",  3500,  6.0,  4.0, 175 ],
    "FT/2200L"  : [ "FT",  4500,  8.0,  5.0, 200 ],
    "FT/750gal" : [ "FT",  6000, 10.0,  7.0, 240 ],  # B-52 only
    "FT/3000gal": [ "FT", 20000, 20.0, 14.0, 975 ],  # B-52 only

    # French
    "FT/MRT/500L"  : [ "FT",  1100,  3.0,  2.0,  44 ], # TK-500 + 4 x 500 lb bombs
    "FT/RPT/270L"  : [ "FT",   900,  4.0,  2.5,  20 ], # JL-100 + 18 x 68 mm rockets
    "FT/RPT/1300L" : [ "FT",  3000,  6.0,  4.0, 114 ], # JL 350 gal. in Air Strike

    ################################################################################

    # BBs

    # Generic
    "BB/HE/100"                 : [ "BB",  100, 0.5 ],
    "BB/HE/110"                 : [ "BB",  110, 0.5 ],
    "BB/HE/225"                 : [ "BB",  225, 1.0 ],
    "BB/HE/250"                 : [ "BB",  250, 1.0 ],
    "BB/HE/500"                 : [ "BB",  500, 1.5 ],
    "BB/HE/550"                 : [ "BB",  550, 1.5 ],
    "BB/HE/750"                 : [ "BB",  750, 2.0 ],
    "BB/HE/800"                 : [ "BB",  800, 2.0 ],
    "BB/HE/1000"                : [ "BB", 1000, 2.5 ],
    "BB/HE/1100"                : [ "BB", 1100, 2.5 ],
    "BB/HE/1500"                : [ "BB", 1500, 3.0 ],
    "BB/HE/1650"                : [ "BB", 1650, 3.0 ],
    "BB/HE/2000"                : [ "BB", 2000, 3.0 ],
    "BB/HE/2200"                : [ "BB", 2200, 3.0 ],
    "BB/Incendiary/100"         : [ "BB",  100, 0.5 ],
    "BB/Incendiary/225"         : [ "BB",  225, 1.0 ],
    "BB/Incendiary/500"         : [ "BB",  500, 1.5 ],
    "BB/Incendiary/550"         : [ "BB",  550, 1.5 ],
    "BB/Incendiary/1100"        : [ "BB", 1100, 2.5 ],
    "BB/Incendiary/1650"        : [ "BB", 1650, 3.0 ],
    "BB/Incendiary/Cluster/500" : [ "BB",  500, 1.5 ],
    "BB/Incendiary/Cluster/800" : [ "BB",  800, 2.0 ],
    "BB/Fire/250"               : [ "BB",  250, 1.0 ],
    "BB/Fire/440"               : [ "BB",  440, 1.5 ],
    "BB/Fire/500"               : [ "BB",  500, 1.5 ],
    "BB/Fire/750"               : [ "BB",  750, 2.0 ],
    "BB/Fire/1000"              : [ "BB", 1000, 2.5 ],
    "BB/Fire/Cluster/1000"      : [ "BB", 1000, 2.5 ],
    "BB/Napalm/500"             : [ "BB",  500, 1.5 ],
    "BB/Napalm/550"             : [ "BB",  550, 1.5 ],
    "BB/Napalm/750"             : [ "BB",  750, 2.0 ],
    "BB/Napalm/1100"            : [ "BB", 1100, 2.5 ],
    "BB/FAE/2400"               : [ "BB", 2400, 3.0 ],
    "BB/FAE/2500"               : [ "BB", 2500, 3.0 ],
    "BB/FAE/Cluster/900"        : [ "BB",  900, 2.5 ],
    "BB/AP/Cluster/100"         : [ "BB",  100, 0.5 ],
    "BB/AP/Cluster/285"         : [ "BB",  285, 1.0 ],
    "BB/AP/Cluster/500"         : [ "BB",  500, 1.5 ],
    "BB/AP/Cluster/550"         : [ "BB",  550, 1.5 ],
    "BB/AP/Cluster/650"         : [ "BB",  650, 1.5 ],
    "BB/AP/Cluster/800"         : [ "BB",  800, 2.0 ],
    "BB/AT/Cluster/220"         : [ "BB",  220, 1.5 ],
    "BB/AT/Cluster/500"         : [ "BB",  500, 1.5 ],
    "BB/AT/Cluster/550"         : [ "BB",  550, 1.5 ],
    "BB/AT/Cluster/650"         : [ "BB",  650, 1.5 ],
    "BB/Mixed/Cluster/600"      : [ "BB",  650, 1.5 ],
    "BB/Mixed/Cluster/750"      : [ "BB",  750, 2.0 ],
    "BB/Cratering/450"          : [ "BB",  450, 1.5 ],
    "BB/Cratering/550"          : [ "BB",  550, 1.5 ],
    "BB/Cratering/650"          : [ "BB",  650, 1.5 ],
    "BB/Cratering/1100"         : [ "BB", 1000, 2.5 ],
    "BB/Cratering/Cluster/500"  : [ "BB",  500, 2.0 ],
    "BB/Cratering/Cluster/750"  : [ "BB",  750, 3.0 ],
    "BB/Cratering/Cluster/1000" : [ "BB", 1000, 3.5 ],

    # Soviet
    "BB/FAB-50": [ "BB", 110, 1.0 ],
    "BB/FAB-100": [ "BB", 225, 1.5 ],
    "BB/FAB-250": [ "BB", 550, 2.0 ],
    "BB/FAB-500": [ "BB", 1100, 3.0 ],
    "BB/FAB-750": [ "BB", 1650, 3.5 ],
    "BB/FAB-1000": [ "BB", 2200, 4.0 ],
    "BB/ZAB-100": [ "BB", 225, 1.5 ],
    "BB/ZAB-250": [ "BB", 550, 2.0 ],
    "BB/ZAB-1000": [ "BB", 2200, 4.0 ],
    "BB/HD/PLAB-250": [ "BB", 550, 2.0 ],
        
    # US
    "BB/M30": [ "BB", 100, 0.5 ],
    "BB/M57": [ "BB", 250, 1.5 ],
    "BB/M64": [ "BB", 500, 2.0 ],
    "BB/M65": [ "BB", 1000, 3.0 ],
    "BB/M66": [ "BB", 2000, 4.0 ],
    "BB/M74": [ "BB", 100, 0.5 ],
    "BB/M76": [ "BB", 500, 1.5 ],
    "BB/HD/BLU-1": [ "BB", 750, 2.5 ],  # HD only from errata.
    "BB/M117": [ "BB", 750, 2.0 ],
    "BB/HD/M117": [ "BB", 750, 2.0 ],
    "BB/M118": [ "BB", 3000, 5.0 ],
    "BB/Mk81": [ "BB", 250, 1.0 ],
    "BB/HD/Mk81": [ "BB", 250, 1.0 ],
    "BB/Mk82": [ "BB", 500, 1.5 ],
    "BB/HD/Mk82": [ "BB", 500, 1.5 ],
    "BB/Mk83": [ "BB", 1000, 2.5 ],
    "BB/HD/Mk83": [ "BB", 1000, 2.5 ],
    "BB/Mk84": [ "BB", 2000, 3.0 ],
    "BB/HD/BLU-10": [ "BB", 250, 1.0 ],
    "BB/HD/BLU-11": [ "BB", 500, 1.5 ],
    "BB/HD/BLU-27": [ "BB", 750, 2.5 ],  # Same properties as BLU-1.
    "BB/HD/Mk77": [ "BB", 750, 2.0 ],
    "BB/HD/Mk79": [ "BB", 1000, 2.5 ],
    "BB/CBU-20": [ "BB", 500, 1.5 ],
    "BB/HD/CBU-20": [ "BB", 500, 1.5 ],
    "BB/CBU-41": [ "BB", 850, 2.0 ],
    "BB/HD/CBU-41": [ "BB", 850, 2.0 ],
    "BB/CBU-58": [ "BB", 800, 2.0 ],
    "BB/CBU-59": [ "BB", 750, 2.0 ],
    "BB/HD/CBU-59": [ "BB", 750, 2.0 ],
    "BB/CBU-71": [ "BB", 800, 2.0 ],
    "BB/HD/CBU-71": [ "BB", 800, 2.0 ],

    ################################################################################

    # BGs

    # Generic
    "BG/HE/Laser/500"      : [ "BG",  500, 2.0 ],
    "BG/HE/Laser/550"      : [ "BG",  550, 2.0 ],
    "BG/HE/Laser/750"      : [ "BG",  750, 2.5 ],
    "BG/HE/Laser/800"      : [ "BG",  800, 2.5 ],
    "BG/HE/Laser/1000"     : [ "BG", 1000, 3.0 ],
    "BG/HE/Laser/1100"     : [ "BG", 1100, 3.0 ],
    "BG/HE/Laser/2000"     : [ "BG", 2000, 3.5 ],
    "BG/HE/Laser/2200"     : [ "BG", 2200, 3.5 ],
    "BG/AP/Laser/500"      : [ "BG",  500, 2.0 ],
    "BG/AP/Laser/550"      : [ "BG",  550, 2.0 ],
    "BG/AP/Laser/650"      : [ "BG",  650, 2.0 ],
    "BG/AP/Laser/800"      : [ "BG",  800, 2.5 ],
    "BG/AT/Laser/500"      : [ "BG",  500, 2.0 ],
    "BG/AT/Laser/550"      : [ "BG",  550, 2.0 ],
    "BG/AT/Laser/650"      : [ "BG",  650, 2.0 ],
    "BG/Mixed/Laser/600"   : [ "BG",  600, 2.0 ],
    "BG/Mixed/Laser/750"   : [ "BG",  750, 2.5 ],

    # US
    "BG/GBU-15D"           : [ "BG", 2200, 4.0 ],

    ################################################################################

    # BSs

    # US
    "BS/AGM-62A"           : [ "BS", 1200, 3.0 ],
    "BS/AGM-62B"           : [ "BS", 2500, 4.0 ],
    "BS/GBU-15A"           : [ "BS", 2200, 4.0 ],
    "BS/GBU-15B"           : [ "BS", 2200, 4.0 ],
    "BS/GBU-15C"           : [ "BS", 2200, 4.0 ],

    ################################################################################

    # GPs

    # Generic
    "GP/12.7 mm"                 : [ "GP",  500, 1.0 ],

    # France
    "GP/30 mm DEFA"              : [ "GP", 1500, 3.5 ],

    # Germany
    "GP/27 mm Mauser"            : [ "GP",  800, 2.5 ],

    # Soviet
    "GP/23 mm GSh-23 GP-9"       : [ "GP",  600, 1.0 ],
    "GP/23 mm GSh-23 UPK-23-250" : [ "GP",  500, 2.5 ],

    # Sweden
    "GP/30 mm KCA"               : [ "GP", 1000, 3.0 ],

    # US
    "GP/20 mm SUU-16"            : [ "GP", 1700, 4.0 ],
    "GP/20 mm SUU-23"            : [ "GP", 1700, 4.0 ],
    "GP/20 mm GPU-2/A"           : [ "GP",  600, 2.0 ],
    "GP/20 mm Mk.4"              : [ "GP", 1400, 3.5 ],
    "GP/30 mm GAU-13"            : [ "GP",  600, 2.0 ],
    "GP/7.62 mm SUU-118/A"       : [ "GP",  350, 1.0 ],

    # UK
    "GP/30 mm ADEN"              : [ "GP",  800, 2.5 ],    

    ################################################################################

    # RKs

    # Generic
    "RK/35"                : [ "RK",   35, 0.5 ],
    "RK/75"                : [ "RK",   75, 0.5 ],
    "RK/100"               : [ "RK",  100, 1.0 ],
    "RK/250"               : [ "RK",  250, 1.0 ],

    # Soviet
    "RK/S-8": [ "RK", 25, 0.5 ],
    "RK/TRS-190": [ "RK", 100, 1.0 ],
    "RK/ARS-212": [ "RK", 260, 1.0 ],
    "RK/S-24": [ "RK", 350, 1.5 ],

    # US
    "RK/HVAR": [ "RK", 140, 1.0 ],
    "RK/Tiny Tim": [ "RK", 1200, 2.0 ],

    ################################################################################

    # RGs

    # French
    "RG/AS-20"             : [ "RG",  350, 1.0 ],
    "RG/AS-30A"            : [ "RG", 1200, 3.0 ],
    "RG/AS-30B"            : [ "RG", 1200, 3.0 ],
    "RG/AS-30L"            : [ "RG", 1200, 3.0 ],

    # Soviet
    "RG/AS-7"              : [ "RG", 1100, 3.0 ],
    "RG/AS-11"             : [ "RG",  750, 2.0 ],

    # Swedish
    "RG/RB05A"             : [ "RG",  700, 2.0 ],

    # US
    "RG/AGM-12B"           : [ "RG",  600, 1.5 ],
    "RG/AGM-12C"           : [ "RG", 1800, 3.0 ],
    "RG/AGM-123"           : [ "RG", 1200, 3.0 ],
    "RG/AGM-65E"           : [ "RG",  650, 2.0 ],
    "RG/AGM-65G"           : [ "RG",  650, 2.0 ],
    "RG/AGM-130L"          : [ "RG", 2200, 4.0 ],

    ################################################################################

    # RSs

    # European
    "RS/AJ168"             : [ "RS", 1200, 3.0 ],

    # US
    "RS/AGM-65B"           : [ "RS",  500, 1.5 ],
    "RS/AGM-65D"           : [ "RS",  500, 1.5 ],
    "RS/AGM-65F"           : [ "RS",  650, 2.0 ],
    "RS/AGM-130L"          : [ "RS", 2200, 4.0 ],
    
    ################################################################################

    # RPs

    # Generic (pod/rocket)
    "RP/Small/Small"       : [ "RP",  100, 2.0 ],
    "RP/Small/Medium"      : [ "RP",  250, 2.0 ],
    "RP/Small/Large"       : [ "RP",  550, 3.0 ],
    "RP/Small/Heavy"       : [ "RP",  750, 3.0 ],
    "RP/Medium/Small"      : [ "RP",  150, 2.0 ],
    "RP/Medium/Medium"     : [ "RP",  300, 3.0 ],
    "RP/Medium/Large"      : [ "RP",  500, 3.0 ],
    "RP/Big/Medium"        : [ "RP",  400, 3.0 ],
    "RP/Large/Small"       : [ "RP",  250, 3.0 ],
    "RP/Large/Medium"      : [ "RP",  500, 3.5 ],

    # Soviet
    "RP/ORO-8K": [ "RP", 175, 2.0 ],
    "RP/UV-8-57": [ "RP", 175, 2.0 ],
    "RP/UV-16-57": [ "RP", 300, 3.0 ],
    "RP/UV-32-57": [ "RP", 500, 3.5 ],

    # US
    "RP/LAU-68": [ "RP", 250, 2.0 ],
    "RP/LAU-3A": [ "RP", 450, 3.0 ],
    "RP/LAU-10": [ "RP", 550, 3.0 ],
    "RP/LAU-33": [ "RP", 200, 2.9 ],  # From errata.
    "RP/LAU-37": [ "RP", 850, 3.5 ],

    ################################################################################

    # ARMs

    # European
    "ARM/AS-37"            : [ "ARM", 1200, 3.0 ],

    # Soviet
    "ARM/AS-9"             : [ "ARM", 1100, 3.0 ],

    # UK
    "ARM/ALARM"            : [ "ARM",  600, 2.0 ],
        
    # US
    "ARM/AGM-45"           : [ "ARM",  500, 2.0 ],
    "ARM/AGM-78"           : [ "ARM", 1500, 3.0 ],
    "ARM/AGM-88"           : [ "ARM",  800, 2.5 ],
    "ARM/AGM-122"          : [ "ARM",  200, 1.0 ],

    ################################################################################

    # WRs

    "WR/DR"    : [ "WR",  100, 1.0 ],
    "WR/TR"    : [ "WR",  100, 1.0 ],
    "WR/MR"    : [ "WR",  200, 2.0 ],
    "WR/MDR"   : [ "WR",  100, 1.0 ],
    "WR/ARM-DR": [ "WR",  200, 2.0 ],
        
    ################################################################################

    # Air-to-air missiles

    # France
    "IRM/R.550 Magic I" : [ "IRM", 200, 1.0 ],
    "IRM/R.550 Magic II": [ "IRM", 200, 1.0 ],
    "RHM/R.530 A"       : [ "RHM", 450, 1.5 ],
    "IRM/R.530 B"       : [ "IRM", 450, 1.5 ],
    "RHM/R.530 D"       : [ "RHM", 550, 1.5 ],

    # Germany
    "IRM/FGW.2": [ "IRM", 170, 1.0 ],

    # Italy
    "RHM/Aspide"        : [ "RHM", 500, 1.0 ],

    # Soviet
    "IRM/AA-2"          : [ "IRM", 160, 1.0 ],
    "IRM/AA-2A"         : [ "IRM", 160, 1.0 ],
    "IRM/AA-2B"         : [ "IRM", 180, 1.0 ],
    "RHM/AA-2C"         : [ "RHM", 200, 1.0 ],
    "IRM/AA-2D"         : [ "IRM", 200, 1.0 ],
    "IRM/AA-3A"         : [ "IRM", 600, 1.5 ],
    "RHM/AA-3B"         : [ "RHM", 600, 1.5 ],
    "RHM/AA-7A"         : [ "RHM", 700, 1.5 ],
    "IRM/AA-7B"         : [ "IRM", 700, 1.5 ],
    "IRM/AA-8"          : [ "IRM", 140, 1.0 ],
    "IRM/AA-8B"         : [ "IRM", 140, 1.0 ],
    "IRM/AA-8C"         : [ "IRM", 150, 1.0 ],
    "RHM/AA-10A"        : [ "RHM", 550, 1.0 ],
    "IRM/AA-10B"        : [ "IRM", 550, 1.0 ],

    # UK
    "IRM/Redtop"        : [ "IRM", 300, 1.0 ],
    "RHM/Skyflash"      : [ "RHM", 400, 1.0 ],
        
    # US
    "IRM/AIM-9B"        : [ "IRM", 160, 1.0 ],
    "RHM/AIM-9C"        : [ "RHM", 190, 1.0 ],
    "IRM/AIM-9D"        : [ "IRM", 200, 1.0 ],
    "IRM/AIM-9E"        : [ "IRM", 170, 1.0 ],
    "IRM/AIM-9E2"       : [ "IRM", 170, 1.0 ],
    "IRM/AIM-9G"        : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9H"        : [ "IRM", 185, 1.0 ],
    "IRM/AIM-9J"        : [ "IRM", 175, 1.0 ],
    "IRM/AIM-9J3"       : [ "IRM", 175, 1.0 ],
    "IRM/AIM-9N"        : [ "IRM", 175, 1.0 ],
    "IRM/AIM-9P"        : [ "IRM", 170, 1.0 ],
    "IRM/AIM-9P2"       : [ "IRM", 170, 1.0 ],
    "IRM/AIM-9P3"       : [ "IRM", 170, 1.0 ],
    "IRM/AIM-9P4"       : [ "IRM", 170, 1.0 ],
    "IRM/AIM-9L"        : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9M"        : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9M4"       : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9M5"       : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9S"        : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9X"        : [ "IRM", 190, 1.0 ],
    "IRM/AIM-9X-II"     : [ "IRM", 190, 1.0 ],
    "AHM/AIM-120A"      : [ "AHM", 350, 1.0 ],
    "AHM/AIM-54C"       : [ "AHM", 1000, 2.0 ],

}

################################################################################


def _class(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    return _storedict[storename][0]


def _weight(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    return _storedict[storename][1]


def _load(storename, storesfuel=0):

    # We make the crude assumption that if there is any stores fuel,
    # then none of the FTs are empty.

    empty = storesfuel is None or storesfuel == 0

    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)

    if _class(storename) == "FT" and empty:
        return _storedict[storename][3]
    else:
        return _storedict[storename][2]


def _fuelcapacity(storename):
    if not storename in _storedict:
        raise RuntimeError("unknown store %r." % storename)
    if _class(storename) == "FT":
        return _storedict[storename][4]
    else:
        return 0


################################################################################


def _storestotalweight(self):
    totalweight = 0
    for loadstation, storename in self._stores.items():
        totalweight += _weight(storename)
    return totalweight


def _storestotalload(self):
    totalload = 0
    for loadstation, storename in self._stores.items():
        totalload += _load(storename, storesfuel=self.storesfuel())
    # Round down. See 4.3.
    totalload = int(totalload)
    return totalload


def _storestotalfuelcapacity(self):
    totalfuelcapacity = 0
    for loadstation, storename in self._stores.items():
        totalfuelcapacity += _fuelcapacity(storename)
    return totalfuelcapacity


################################################################################


def _initstores(self, stores):

    newstores = {}
    for loadstation, name in stores.items():
        if isinstance(loadstation, int):
            loadstation = str(loadstation)
        if not isinstance(loadstation, str):
            raise RuntimeError("invalid load station %r." % loadstation)
        if name not in _storedict:
            raise RuntimeError("invalid store %r." % name)
        newstores[loadstation] = name
    self._stores = newstores

    self._showstores()
    self._updateconfiguration()


################################################################################


def _updateconfiguration(self):
    """
    Updated the configuration based on the current stores.
    """

    # If no stores are specified, do nothing.
    if self._stores == None:
        return

    assert self._aircraftdata.hasstoreslimits()

    # See rule 4.2 and 4.3.

    totalweight = self._storestotalweight()
    totalload = self._storestotalload()

    if totalweight > self._aircraftdata.storeslimit("DT"):
        raise RuntimeError("total stores weight exceeds the aircraft capacity.")

    if totalload <= self._aircraftdata.storeslimit("CL"):
        self._configuration = "CL"
    elif totalload <= self._aircraftdata.storeslimit("1/2"):
        self._configuration = "1/2"
    else:
        self._configuration = "DT"


################################################################################


def _showstores(self):

    if len(self._stores) != 0:
        self.logwhenwhat("", "stores are:")
        for loadstation, name in self._stores.items():
            self.logwhenwhat(
                "",
                "  %-2s: %-17s  %-3s / %4d / %.1f%s"
                % (
                    loadstation,
                    name,
                    _class(name),
                    _weight(name),
                    _load(name, storesfuel=self.storesfuel()),
                    " / %d" % _fuelcapacity(name) if _class(name) == "FT" else "",
                ),
            )

        self.logwhenwhat(
            "", "stores total weight        is %d." % self._storestotalweight()
        )
        self.logwhenwhat(
            "", "stores total load          is %d." % self._storestotalload()
        )
        self.logwhenwhat(
            "", "stores total fuel capacity is %d." % self._storestotalfuelcapacity()
        )
        if self.storesfuel() is not None:
            self.logwhenwhat(
                "", "stores total fuel          is %.1f." % self.storesfuel()
            )


################################################################################


def showstores(self, note=None):
    """
    Show the aircraft's stores to the log.
    """
    try:
        self._showstores()
        self.lognote(note)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################


def _airtoairlaunch(stores, launched, printer=print):

    newstores = stores.copy()

    loadstation = str(launched)

    if loadstation not in stores:
        raise RuntimeError("load station %s is not loaded." % loadstation)

    if _class(stores[loadstation]) not in [ "IRM", "BRM", "RHM", "AHM"]:
        raise RuntimeError(
            "load station %s is not loaded with an air-to-air missile." % loadstation
        )

    missiletype = stores[loadstation]

    printer("launching %s from load station %s." % (stores[loadstation], loadstation))
    del newstores[loadstation]

    return missiletype, newstores


################################################################################


def _release(self, released):

    previousconfiguration = self._configuration

    if isinstance(released, int) or isinstance(released, str):
        releasedlist = [released]
    else:
        releasedlist = released
    releasedlist = list(str(releaseditem) for releaseditem in releasedlist)

    stores = self._stores

    for releaseditem in releasedlist:

        if releaseditem[0] in "0123456789":
            loadstation = releaseditem
            if loadstation not in stores.keys():
                raise RuntimeError("load station %s is not loaded." % loadstation)
            loadstationlist = [loadstation]
        else:
            loadstationlist = list(
                filter(
                    lambda loadstation: stores[loadstation].startswith(releaseditem),
                    stores.keys(),
                )
            )
            if len(loadstationlist) == 0:
                raise RuntimeError(
                    "no load stations are loaded with %s." % releaseditem
                )

        for loadstation in loadstationlist:
            self.logwhenwhat(
                "",
                "releases %s on load station %s." % (stores[loadstation], loadstation),
            )
            del stores[loadstation]

    self._updateconfiguration()

    if self._configuration != previousconfiguration:
        self.logwhenwhat(
            "",
            "configuration changes from %s to %s."
            % (previousconfiguration, self._configuration),
        )


################################################################################


def release(self, *args):
    try:
        self._release(*args)
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################
