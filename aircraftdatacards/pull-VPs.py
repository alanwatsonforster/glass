import glob
import os.path
import json

import glass.aircraftdata

print("pulling VPs from aircraft data files.")
paths = os.path.join(
    os.path.dirname(__file__), "..", "src", "glass", "aircraftdata", "*.json"
)

outputpath = os.path.join(os.path.dirname(__file__), "VPs.tsv")

try:
    os.remove(outputpath)
except:
    pass

for path in sorted(glob.glob(paths)):

    basename = os.path.basename(path)

    name = basename[:-5]
    if name[0] == "_":
        continue
    print('pulling VPs for "%s"' % name)
    data = glass.aircraftdata.aircraftdata(name)
    with open(outputpath, "a") as f:
        f.write(
            "%d\t%s\n"
            % (
                data.VPs()[0],
                data.fullvariantname(),
            )
        )
