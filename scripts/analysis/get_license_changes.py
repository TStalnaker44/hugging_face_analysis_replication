
import json, os, pprint
from collections import Counter

def loadChainData():
    path = os.path.join("data", "cleaned_data", "chains.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    changes = getChanges()
    c = Counter(changes)
    changes = [{"start":k[0], "end":k[1], "count":v} for k, v in c.items()]
    changes.sort(key=lambda x: x["count"], reverse=True)
    saveChanges(changes)

def getChanges():
    data = loadChainData()
    deltas = []
    for model_name, chains in data.items():
        for chain in chains:
            deltas.extend(getLicenseDeltas(chain))
    return deltas

def collapseOther(lic_list):
    licenses = set()
    for lic in lic_list:
        if lic.endswith("(other)"):
            licenses.add("other")
        else:
            licenses.add(lic)
    return list(licenses)

def getLicenseDeltas(chain):
    deltas = []
    prev_link = chain[0]
    for link in chain[1:]:
        prev_lic = " | ".join(sorted(collapseOther(prev_link["license"])))
        curr_lic = " | ".join(sorted(collapseOther(link["license"])))
        if prev_lic != curr_lic:
            deltas.append((prev_lic, curr_lic))
        prev_link = link
    return deltas

def saveChanges(changes):
    path = os.path.join("data", "cleaned_data", "license_changes.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(changes, f, indent=4)
