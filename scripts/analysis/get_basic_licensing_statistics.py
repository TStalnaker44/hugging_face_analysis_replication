
import pprint, csv, os
from collections import Counter
from ..utilities.querier import Querier
from ..utils import loadDatasetData, loadModelData

def getCountOfLicensedDatasets():
    data = loadDatasetData()
    count = 0
    for dataset in data:
        if len(dataset.get("license", [])) > 0:
            count += 1
    print("Datasets with licenses:", count)
    print("Datasets without licenses:", len(data) - count)
    print("Total datasets:", len(data))

def getModelLicenseFrequencies():
    q = Querier()
    pprint.pprint(q.getLicenseFrequencies(True).most_common(11))

def getDatasetLicenseFrequencies():
    data = loadDatasetData()
    licenses = []
    for ds in data:
        lics = ds.get("license", [])
        lics.sort()
        licenses.append("|".join(lics))
    c = Counter(licenses)
    pprint.pprint(c.most_common(11))

def getUniqueModelLicenses():
    data = loadModelData()
    licenses = set()
    for model in data:
        lics = model.get("licenses", [])
        for lic in lics:
            if lic.endswith("(other)"): lic = "other"
            licenses.add(lic)
    print(f"There are {len(licenses)} unique licenses")

def getUniqueDatasetLicenses():
    data = loadDatasetData()
    licenses = set()
    for model in data:
        lics = model.get("license", [])
        for lic in lics:
            if lic.endswith("(other)"): lic = "other"
            licenses.add(lic)
    print(f"There are {len(licenses)} unique licenses")

def getUniqueLicensesForModels():
    q = Querier()
    c = q.getLicenseFrequencies(True)
    licenses = set()
    for lic in c.keys():
        for l in lic.split("|"):
            licenses.add(l)
    licenses = sorted(list(licenses))
    path = os.path.join("data", "analysis", "model_license_frequencies.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["License", "Count"])
        writer.writerows([[l] for l in licenses])

def getUniqueLicensesForDatasets():
    data = loadDatasetData()
    licenses = set()
    for ds in data:
        lics = ds.get("license", [])
        for l in lics:
            licenses.add(l)
    licenses = sorted(list(licenses))
    path = os.path.join("data", "analysis", "dataset_license_frequencies.csv")
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["License", "Type"])
        writer.writerows([[l] for l in licenses])