
import os, json, csv
from ..utilities.querier import Querier
from collections import Counter
from ..utils import loadModelData, loadDatasetData

def findInstancesOfDroppedLicenses():
    path = os.path.join("data", "cleaned_data", "chains.json")
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    dropped = {}
    for name, chains in data.items():
        for chain in chains:
            if chain[0]["license"] == ["UNDECLARED"]: continue
            for model in chain[1:-1]:
                if model["license"] == ["UNDECLARED"]:
                    dropped[name] = chains
    path = os.path.join("data", "analysis", "undeclared_licenses.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(dropped, file, indent=4)
    print(f"Licenses dropped: {len(dropped)}")

def getUnlicensedSubset():
    q = Querier()
    models = q.getModelsByLicense([])
    print(len(models))
    models.sort(key=lambda x: int(x["downloads"]), reverse=True)
    subset = models[:100]
    path = os.path.join("data", "analysis")
    with open(os.path.join(path, "unlicensed_subset.json"), "w", encoding="utf-8") as file:
        json.dump(subset, file, indent=4)
    with open(os.path.join(path, "unlicensed_subset.csv"), "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["id", "owner", "name", "downloads", "likes", "url", "has_license", "license", "license_location"])
        for model in subset:
            id = model["id"]
            owner, name = model["name"].split("/")
            url = f"https://huggingface.co/{owner}/{name}"
            downloads = model["downloads"]
            likes = model["likes"]
            writer.writerow([id, owner, name, downloads, likes, url])

def getFrequenciesOfLicenseChanges():
    path = os.path.join("data", "cleaned_data", "license_type_mapping.csv")
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        mapping = {row[0]:row[1] for row in reader}

    path = os.path.join("data", "cleaned_data", "license_changes.json")
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    dropped = 0
    declared = 0
    changed = 0
    lost_license = 0
    add_license = 0
    rows = []
    for d in data:
        if d["end"] == "UNDECLARED" and d["start"] != "UNDECLARED":
            dropped += d["count"]
        elif d["start"] == "UNDECLARED" and d["end"] != "UNDECLARED":
            declared += d["count"]
        elif d["start"] != d["end"] and ("|" not in d["start"] and "|" not in d["end"]):
            changed += d["count"]
            rows.append((d["start"], d["end"], f"{mapping[d['start']]} to {mapping[d['end']]}", d["count"]))
        elif len(d["start"].split(" | ")) > len(d["end"].split(" | ")):
            lost_license += d["count"]
            print(d)
        elif len(d["start"].split(" | ")) < len(d["end"].split(" | ")):
            add_license += d["count"]
    print(f"{sum([d['count'] for d in data])} total license changes were recorded")
    print(f"{dropped} licenses were dropped")
    print(f"{declared} licenses were declared")
    print(f"{changed} licenses were changed")
    print(f"{lost_license} licenses were lost")
    print(f"{add_license} licenses were added")

    path = os.path.join("data", "analysis", "license_variations.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Parent License", "Child License", "Type", "Count"])
        for row in rows:
            writer.writerow(row)

def getDatasetModelLicenseCombinations():
    path = os.path.join("data", "analysis", "dataset_license_analysis.json")
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    combinations = []
    for d in data:
        mlicense = d["model_license"]
        if mlicense.endswith("(other)"): mlicense = "other"
        for dlicense in d["dataset_licenses"]:
            if dlicense.endswith("(other)"): dlicense = "other"
            combinations.append((mlicense, dlicense))
    c = Counter(combinations)
    path = os.path.join("data", "analysis", "license_combinations.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Model License", "Dataset License", "Count"])
        rows = sorted([[k[0], k[1], v] for k, v in c.items()], key=lambda x: x[2], reverse=True)
        writer.writerows(rows)
    print(f"Out of {len(data)} total combinations.")

def getPrevalenceOfLicenseClassesInModels():
    path = os.path.join("data", "cleaned_data", "license_type_mapping.csv")
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = {row[0]:row[1] for row in reader}
    models = loadModelData()
    classes = []
    for model in models:
        lics = model.get("licenses", [])
        licenses = []
        for lic in lics:
            if lic.endswith("(other)"): lic = "other"
            licenses.append(data[lic])
        classes.append("|".join(sorted(list(set(licenses)))))
    c = Counter(classes)
    path = os.path.join("data", "analysis", "license_classes_in_models.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["License Class", "Count"])
        rows = sorted([[k, v] for k, v in c.items()], key=lambda x: x[1], reverse=True)
        writer.writerows(rows)
    print(c)

def getPrevalenceOfLicenseClassesInDatasets():
    path = os.path.join("data", "cleaned_data", "license_type_mapping.csv")
    with open(path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = {row[0]:row[1] for row in reader}
    models = loadDatasetData()
    classes = []
    for model in models:
        lics = model.get("license", [])
        if type(lics) == str: lics = [lics]
        licenses = []
        for lic in lics:
            if lic.endswith("(other)"): lic = "other"
            licenses.append(data[lic])
        classes.append("|".join(sorted(list(set(licenses)))))
    c = Counter(classes)
    path = os.path.join("data", "analysis", "license_classes_in_datasets.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["License Class", "Count"])
        rows = sorted([[k, v] for k, v in c.items()], key=lambda x: x[1], reverse=True)
        writer.writerows(rows)
    print(c)

def getLicensesWithUnknownID():
    data = loadModelData()
    count = 0
    unknown = set()
    for model in data:
        datasets = model.get("datasets", [])
        for dataset in datasets:
            if dataset.get("id") == None:
                unknown.add(dataset.get("declared").strip().lower())
                count += 1
    print(f"Models with datasets that have unknown IDs: {count}")
    print(f"Distinct unknown datasets: {len(unknown)}")
    print(list(unknown)[:10])