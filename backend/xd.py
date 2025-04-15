import json

with open("no_users_fixture.json", "r", encoding="utf-8") as f:
    data = json.load(f)

filtered = [obj for obj in data if obj["model"] != "contenttypes.contenttype"]

with open("no_contenttypes_fixture.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)