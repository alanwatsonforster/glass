import glob
import os.path
import json

print("formatting aircraft data files.")
paths = os.path.join(os.path.dirname(__file__), "..", "apxo", "aircraftdata", "*.json")

descriptionpath = os.path.join(os.path.dirname(__file__), "description.json")

extractdescriptions = False

if extractdescriptions:
    description = {}
else:
    with open(descriptionpath, "r") as f:
        description = json.loads(f.read())

for path in sorted(glob.glob(paths)):
    basename = os.path.basename(path)
    if basename[0] == "_":
        continue
    print("formatting \"%s\"" % basename)
    try:
        with open(path, "r") as f:
            text = f.read()
        object = json.loads(text)
        if extractdescriptions:
            if "description" in object:
                description[basename] = object["description"]
            else:
                description[basename] = ""
        else:
            if not basename in description:
                raise RuntimeError("no description for %s" % basename)
            else:
                object["description"] = description[basename]
        newtext = json.dumps(object, indent=4, sort_keys=False, ensure_ascii=False)
        with open(path, "w") as f:
            f.write(newtext)
    except json.JSONDecodeError as e:
        print("error in file \"%s\": %s" % (path, e))

if extractdescriptions:
    with open(descriptionpath, "w") as f:
        f.write(json.dumps(description, indent=4, sort_keys=True, ensure_ascii=False))