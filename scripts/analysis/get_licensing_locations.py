
import os, json
from ..utils import loadRawModelData
from scripts.utilities.querier import Querier

def getLicenseDeclarationStatistics():
    q = Querier()
    print("Models:", q.getModelCount())
    print("Without License:", len(q.getModelsByLicense([])))
    print(q.getLicenseFrequencies())

def getLicenseLocationStatistics():

    def licenseInTags(tags):
        for tag in tags:
            if tag.startswith("license:"):
                return True
        return False

    def licenseInMeta(data):
        return len(data.get("cardData", {}).get("license", [])) > 0

    in_tags, in_meta, both = 0, 0, 0
    models = loadRawModelData()
    ids = set()
    for i, model in enumerate(models):
        if i % 10000 == 0: print(f"Processing {i}/{len(models)}...")
        if model["_id"] in ids: continue
        intag = licenseInTags(model.get("tags", []))
        inmeta = licenseInMeta(model)
        if intag and inmeta:
            both += 1
        elif intag:
            in_tags += 1
        elif inmeta:
            in_meta += 1
        ids.add(model["_id"])

    print("Models with licenses only in tags:", in_tags)
    print("Models with licensese only in meta:", in_meta)
    print("Models with licensese in both:", both)

def getDeclarationDifferences():
    
    def getLicenseFromTags(tags):
        return [tag.replace("license:", "") for tag in tags if tag.startswith("license:")]

    def getLicenseFromMeta(data):
        license = data.get("cardData", {}).get("license", [])
        if type(license) == str: license = [license]
        return license

    diffs = []
    models = loadRawModelData()
    for i, model in enumerate(models):
        if i % 10000 == 0: print(f"Processing {i}/{len(models)}...")
        tags = sorted(list(set(getLicenseFromTags(model.get("tags", [])))))
        meta = sorted(list(set(getLicenseFromMeta(model))))
        if tags != meta and (len(meta) > 0):
            diffs.append((model["id"], tags, meta))

    print("Number of differences:", len(diffs))
    path = os.path.join("data", "analysis", "discrepancies_in_tags_and_meta.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(diffs, file, indent=4)
        
def analyzeDiscrepancies():
    extra_in_tags = 0
    path = os.path.join("data", "analysis", "discrepancies_in_tags_and_meta.json")
    with open(path, "r", encoding="utf-8") as file:
        diffs = json.load(file)
        for diff in diffs:
            tags = diff[2]
            for license in tags:
                if license not in diff[1]:
                    extra_in_tags += 1
                    break
    print("Extra licenses in tags:", extra_in_tags)