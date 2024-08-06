
import os, glob, json

def getAttrByTag(tags, target):
    hits = []
    for tag in tags:
        if tag.startswith(target+":"):
            hits.append(tag.split(":")[-1])
    return hits

def main():
    path = os.path.join("data", "raw_data", "dataset_lists", "*.json")
    files = glob.glob(path)

    datasets = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                t = {}
                t["id"] = d.get("id")
                t["internal_id"] = d.get("_id")
                t["likes"] = d.get("likes", 0)
                t["downloads"] = d.get("downloads", 0)
                t["license"] = getAttrByTag(d.get("tags", []), "license")
                t["tasks"] = getAttrByTag(d.get("tags", []), "task_categories")
                doi = getAttrByTag(d.get("tags", []), "doi")
                t["doi"] = doi[0] if len(doi)>0 else None
                datasets.append(t)

    path = os.path.join("data", "cleaned_data", "datasets.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datasets, f, indent=4)