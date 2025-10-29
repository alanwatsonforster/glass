import math


def turnrequirement(altitudeband, speed, rate, divisor=1):
    """
    Determine the turn requirement accoring to the Air Power Integrated Turn
    Charts.
    """

    speed = int(speed)
    if speed < 8:
        ispeed = speed - 1
    elif speed < 10:
        ispeed = 7
    elif speed < 12:
        ispeed = 8
    elif speed < 14:
        ispeed = 9
    else:
        ispeed = 10

    irate = ["EZ", "TT", "HT", "BT", "ET"].index(rate)

    if altitudeband == "LO" or altitudeband == "ML":
        raw = [
            [
                60,
                1,
                2,
                3,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                20,
            ],
            [
                90,
                60,
                1,
                2,
                3,
                4,
                5,
                6,
                8,
                19,
                12,
                14,
            ],
            [
                0,
                90,
                60,
                1,
                2,
                2,
                3,
                4,
                6,
                8,
                10,
                12,
            ],
            [
                0,
                0,
                90,
                60,
                1,
                1,
                2,
                3,
                4,
                6,
                8,
                10,
            ],
            [
                0,
                0,
                0,
                60,
                60,
                1,
                1,
                2,
                3,
                4,
                6,
                8,
            ],
        ][irate][ispeed]
    elif altitudeband == "MH":
        raw = [
            [
                1,
                2,
                3,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                22,
            ],
            [
                60,
                1,
                2,
                3,
                4,
                6,
                7,
                8,
                10,
                12,
                14,
                18,
            ],
            [
                0,
                60,
                1,
                2,
                3,
                4,
                5,
                6,
                8,
                10,
                12,
                14,
            ],
            [
                0,
                0,
                60,
                1,
                2,
                2,
                3,
                4,
                6,
                7,
                10,
                11,
            ],
            [
                0,
                0,
                0,
                60,
                1,
                1,
                2,
                2,
                4,
                5,
                7,
                9,
            ],
        ][irate][ispeed]
    elif altitudeband == "HI":
        raw = [
            [
                2,
                3,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
                24,
            ],
            [
                1,
                2,
                3,
                4,
                5,
                6,
                8,
                10,
                12,
                14,
                16,
                20,
            ],
            [
                0,
                1,
                2,
                3,
                4,
                5,
                6,
                8,
                9,
                10,
                13,
                16,
            ],
            [
                0,
                0,
                1,
                2,
                3,
                3,
                4,
                6,
                7,
                8,
                10,
                12,
            ],
            [
                0,
                0,
                0,
                1,
                2,
                2,
                3,
                4,
                5,
                6,
                8,
                10,
            ],
        ][irate][ispeed]
    elif altitudeband == "VH":
        raw = [
            [
                2,
                4,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
                22,
                24,
            ],
            [
                1,
                2,
                4,
                6,
                8,
                9,
                10,
                13,
                15,
                17,
                20,
                22,
            ],
            [
                0,
                0,
                3,
                4,
                6,
                7,
                8,
                10,
                12,
                14,
                17,
                20,
            ],
            [
                0,
                0,
                0,
                3,
                4,
                5,
                6,
                7,
                9,
                11,
                14,
                16,
            ],
            [
                0,
                0,
                0,
                0,
                3,
                4,
                5,
                6,
                7,
                8,
                10,
                12,
            ],
        ][irate][ispeed]
    else:
        raw = [
            [
                3,
                6,
                8,
                10,
                12,
                14,
                16,
                18,
                20,
                22,
                24,
                28,
            ],
            [
                0,
                4,
                6,
                8,
                10,
                12,
                13,
                14,
                16,
                18,
                21,
                24,
            ],
            [
                0,
                0,
                4,
                6,
                7,
                8,
                10,
                11,
                13,
                15,
                18,
                21,
            ],
            [
                0,
                0,
                0,
                4,
                5,
                6,
                7,
                8,
                10,
                12,
                14,
                18,
            ],
            [
                0,
                0,
                0,
                0,
                4,
                5,
                6,
                7,
                9,
                10,
                12,
                14,
            ],
        ][irate][ispeed]
        if altitudeband == "UH" and raw != 0:
            raw += 2

    if raw == 0:
        return None
    elif raw == 60 or raw == 90:
        return raw
    else:
        return int(math.ceil(raw / divisor))


if __name__ == "__main__":

    """
    Produce a table for the g-force for all turn rates.
    """

    def gforce(speed, turnrequirement):
        meterspermile = 1604
        if turnrequirement is None:
            return None
        if turnrequirement == 60:
            turnrequirement = 1 / 2
        if turnrequirement == 90:
            turnrequirement = 1 / 3
        # speed of 1 = 100 mph
        v = speed * (100 / 3600) * meterspermile
        # circumference of turning circle is 12 turn requirements
        r = 12 * turnrequirement * (meterspermile / 3) / (2 * math.pi)
        a = v**2 / r
        g = 9.8
        return a / g

    maxspeed = 7.5

    print()
    for altitudeband in ["LO", "ML", "MH", "HI", "VH", "EH", "UH"]:
        print("%-4s" % altitudeband, end="")
        speeds = [1 + i / 2 for i in range(0,int(maxspeed / 0.5 - 1))]
        for speed in speeds:
            print(" %4.1f" % speed, end="")
        print()
        for turnrate in ["EZ", "TT", "HT", "BT", "ET"]:
            print("%-4s" % turnrate, end="")
            mingforce = math.inf
            maxgforce = 0
            for speed in speeds:
                _gforce = gforce(
                    speed, turnrequirement(altitudeband, speed, turnrate)
                )
                if _gforce is None:
                    print("     ", end="")
                else:
                    print(" %4.1f" % _gforce, end="")
                    mingforce = min(mingforce, _gforce)
                    maxgforce = max(maxgforce, _gforce)
            print("   %.1f to %.1f" % (mingforce, maxgforce), end="")
            print()
        print()
    print()
