import glob
import os.path
import json

print("formatting aircraft data files.")
paths = os.path.join(os.path.dirname(__file__), "..", "glass", "aircraftdata", "*.json")

for path in sorted(glob.glob(paths)):
    basename = os.path.basename(path)
    if basename[0] == "_":
        continue
    print("formatting \"%s\"" % basename)
    try:
        with open(path, "r") as f:
            text = f.read()
        object = json.loads(text)
        newtext = json.dumps(object, indent=4, sort_keys=False, ensure_ascii=False)
        with open(path, "w") as f:
            f.write(newtext)
    except json.JSONDecodeError as e:
        print("error in file \"%s\": %s" % (path, e))
