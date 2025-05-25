import glob
import os.path
import json

print("pulling descriptions from aircraft data files.")
paths = os.path.join(os.path.dirname(__file__), "..", "src", "glass", "aircraftdata", "*.json")

descriptionpath = os.path.join(os.path.dirname(__file__), "description.json")

description = {}

for path in sorted(glob.glob(paths)):
    basename = os.path.basename(path)
    name = basename[:-5]
    if name[0] == "_":
        continue
    print("pulling description from \"%s\"" % basename)
    try:
        with open(path, "r") as f:
            text = f.read()
        object = json.loads(text)
        if "description" in object:
            description[name] = object["description"]
        else:
            description[name] = ""
        newtext = json.dumps(object, indent=4, sort_keys=False, ensure_ascii=False)
        with open(path, "w") as f:
            f.write(newtext)
    except json.JSONDecodeError as e:
        print("error in file \"%s\": %s" % (path, e))

with open(descriptionpath, "w") as f:
    f.write(json.dumps(description, indent=4, sort_keys=True, ensure_ascii=False))