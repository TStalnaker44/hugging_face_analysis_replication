
import json, os
from collections import Counter
from ..utils import loadModelData, loadRawModelData

def checkForGrandfatherParadox():
    own_parent = []
    models = loadModelData()
    for m in models:
        mid = m["id"]
        for b in m["bases"]:
            if b["id"] == mid and m not in own_parent:
                own_parent.append(m)
    print(f"{len(own_parent)} models are their own parent...")

    path = os.path.join("data", "analysis", "grandfather_paradox.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(own_parent, file, indent=4)

def getExamplesOfDuplications():
    models = loadRawModelData()
    data_duplicates = []
    base_duplicates = []
    for i, model in enumerate(models):
        if i % 10000 == 0: print(f"Processing {i}/{len(models)}...")  
        meta_datasets = model.get("cardData", {}).get("datasets", [])
        if type(meta_datasets) == str: meta_datasets = [meta_datasets]
        meta_bases = model.get("cardData", {}).get("base_model", [])
        if type(meta_bases) == str: meta_bases = [meta_bases]
        if len(meta_datasets) != len(set(meta_datasets)):
            data_duplicates.append(model["id"])
        if len(meta_bases) != len(set(meta_bases)):
            base_duplicates.append(model["id"])
    print("Data Duplicates:", len(data_duplicates))
    print("Base Duplicates:", len(base_duplicates))
    path = os.path.join("data", "analysis", "duplicate_declarations.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump({"data": data_duplicates, "base": base_duplicates}, file, indent=4)

def getAmbiguities():
    count = 0
    data = loadModelData()
    for model in data:
        for base in model["bases"]:
            if base["ambiguous"]:
                count += 1
    print("Ambiguous instances:", count)

def getDeadReferences():
    count = 0
    data = loadModelData()
    unique = set()
    for model in data:
        for base in model["bases"]:
            if base["id"] is not None and base["id"].startswith("404"):
                count += 1
                unique.add(base["id"])
    print("Dead references:", count)
    print("Unique dead references:", len(unique))

def getPopularModelNames():
    data = loadModelData()
    names = []
    for model in data:
        name = model["name"].split("/")[-1]
        names.append(name)
    c = Counter(names)
    print(c.most_common(10))

def getModelsDeclaredAsDatasets():
    data = loadModelData()
    count = 0
    for model in data:
        for dataset in model["datasets"]:
            if dataset.get("note"):
                count += 1
    print("Models declared as datasets:", count)