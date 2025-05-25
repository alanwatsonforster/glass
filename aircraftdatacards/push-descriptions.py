import glob
import os.path
import json

print("pushing descriptions to aircraft data files.")
paths = os.path.join(os.path.dirname(__file__), "..", "src", "glass", "aircraftdata", "*.json")

descriptionpath = os.path.join(os.path.dirname(__file__), "description.json")

with open(descriptionpath, "r") as f:
    description = json.loads(f.read())

for path in sorted(glob.glob(paths)):
    basename = os.path.basename(path)
    name = basename[:-5]
    if name[0] == "_":
        continue
    print("pushing description to \"%s\"" % basename)
    try:
        with open(path, "r") as f:
            text = f.read()
        object = json.loads(text)
        if not name in description:
            raise RuntimeError("no description for %s" % basename)
        object["description"] = description[name]
        newtext = json.dumps(object, indent=4, sort_keys=False, ensure_ascii=False)
        with open(path, "w") as f:
            f.write(newtext)
    except json.JSONDecodeError as e:
        print("error in file \"%s\": %s" % (path, e))
