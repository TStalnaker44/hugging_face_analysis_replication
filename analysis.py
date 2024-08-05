
import os, glob, json, pprint, csv
from scripts.utils import loadModelData, loadDatasetData
from bs4 import BeautifulSoup
from scripts.utilities.index import Index, INDEX
from scripts.utilities.querier import Querier
from scripts.config import MODEL_SEPERATOR
from collections import Counter

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
    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    files = glob.glob(path)
    ids = set()
    for i, f in enumerate(files):
        if i % 10000 == 0: print(f"Processing {i}/{len(files)}...")
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            if data["_id"] in ids: continue
            intag = licenseInTags(data.get("tags", []))
            inmeta = licenseInMeta(data)
            if intag and inmeta:
                both += 1
            elif intag:
                in_tags += 1
            elif inmeta:
                in_meta += 1
            ids.add(data["_id"])

    print("Models with licenses in tags:", in_tags)
    print("Models with licensese in meta:", in_meta)
    print("Models with licensese in both:", both)

def getDeclarationDifferences():
    
    def getLicenseFromTags(tags):
        return [tag.replace("license:", "") for tag in tags if tag.startswith("license:")]

    def getLicenseFromMeta(data):
        license = data.get("cardData", {}).get("license", [])
        if type(license) == str: license = [license]
        return license

    diffs = []
    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    files = glob.glob(path)
    for i, f in enumerate(files):
        if i % 10000 == 0: print(f"Processing {i}/{len(files)}...")
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            tags = sorted(list(set(getLicenseFromTags(data.get("tags", [])))))
            meta = sorted(list(set(getLicenseFromMeta(data))))
            if tags != meta and (len(meta) > 0):
                diffs.append((f, tags, meta))

    print("Number of differences:", len(diffs))
    with open("temp.json", "w", encoding="utf-8") as file:
        json.dump(diffs, file, indent=4)
        
def analyzeDiscrepancies():
    extra_in_tags = 0
    with open("temp.json", "r", encoding="utf-8") as file:
        diffs = json.load(file)
        for diff in diffs:
            tags = diff[2]
            for license in tags:
                if license not in diff[1]:
                    extra_in_tags += 1
                    break
    print("Extra licenses in tags:", extra_in_tags)

def findConsentCount():

    def getSoup(file):
        with open(file, "r", encoding="utf-8") as f:
            return BeautifulSoup(f, "html.parser")
        
    def isDisabled(headings):
        for h in headings:
            if h.text.strip() == "Access to this model has been disabled":
                return True
        return False
    
    def is404(headings):
        for h in headings:
            if h.text.strip() == "404":
                return True
        return False
    
    def isRestricted(soup):
        for span in soup.findAll("span"):
            if span.text.strip() == "Not-For-All-Audiences":
                return True
        return False
                
    path = os.path.join("data", "raw_data", "model_page_data", "*.html")
    files = glob.glob(path)
    gated_list = []
    disabled_list = []
    missing = []
    restricted = []
    for f in files:
        soup = getSoup(f)
        gated = soup.find("div", attrs= {"data-target":"RepoGatedModal"})
        headings = soup.findAll("h2")
        if isDisabled(headings): disabled_list.append(f)
        elif gated: gated_list.append(f)
        elif is404(soup.findAll("h1")): missing.append(f)
        elif isRestricted(soup): restricted.append(f)
        else:
            print(f)
    print("Models requiring consent:", len(gated_list))
    print("Models that are disabled:", len(disabled_list))
    print("Models that are missing:", len(missing))
    print("Models that are restricted:", len(restricted))
    d = {"gated": gated_list, "disabled": disabled_list, "missing": missing, "restricted": restricted}
    with open("temp2.json", "w", encoding="utf-8") as file:
        json.dump(d, file, indent=4)

def checkForGrandfatherParadox():
    own_parent = []
    models = loadModelData()
    for m in models:
        mid = m["id"]
        for b in m["bases"]:
            if b["id"] == mid and m not in own_parent:
                own_parent.append(m)
    print(f"{len(own_parent)} models are their own parent...")

    with open("grandfather_paradox.json", "w", encoding="utf-8") as file:
        json.dump(own_parent, file, indent=4)

def getExamplesOfDuplications():
    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    files = glob.glob(path)
    data_duplicates = []
    base_duplicates = []
    for i, f in enumerate(files):
        if i % 10000 == 0: print(f"Processing {i}/{len(files)}...")
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            meta_datasets = data.get("cardData", {}).get("datasets", [])
            if type(meta_datasets) == str: meta_datasets = [meta_datasets]
            meta_bases = data.get("cardData", {}).get("base_model", [])
            if type(meta_bases) == str: meta_bases = [meta_bases]
            if len(meta_datasets) != len(set(meta_datasets)):
                data_duplicates.append(f)
            if len(meta_bases) != len(set(meta_bases)):
                base_duplicates.append(f)
    print("Data Duplicates:", len(data_duplicates))
    print("Base Duplicates:", len(base_duplicates))
    with open("temp3.json", "w", encoding="utf-8") as file:
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

def getCountOfMultiLicensing():
    data = loadModelData()
    count = 0
    for model in data:
        if len(model.get("licenses", [])) > 1:
            count += 1
    print(f"Models with multiple licenses: {count}")
    
    data = loadDatasetData()
    count = 0
    for model in data:
        if len(model.get("license", [])) > 1:
            count += 1
    print(f"Datasets with multiple licenses: {count}")

def getFrequenciesOfMultilicensing():
    data = loadModelData()
    models = []
    for model in data:
        lics = model.get("licenses", [])
        if len(lics) > 1:
            models.append("|".join(sorted(lics)))
    c = Counter(models)
    pprint.pprint(c)
    
    data = loadDatasetData()
    datasets = []
    for model in data:
        lics = model.get("license", [])
        if len(lics) > 1:
            datasets.append("|".join(sorted(lics)))
            if "license-plate-detection" in lics:
                print(model)
    c = Counter(datasets)
    pprint.pprint(c)

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
    with open("unknown_licenses.json", "w", encoding="utf-8") as file:
        json.dump(dropped, file, indent=4)
    print(f"Licenses dropped: {len(dropped)}")

def getUnlicensedSubset():
    q = Querier()
    models = q.getModelsByLicense([])
    print(len(models))
    models.sort(key=lambda x: int(x["downloads"]), reverse=True)
    subset = models[:100]
    with open("unlicensed_subset.json", "w", encoding="utf-8") as file:
        json.dump(subset, file, indent=4)
    with open("unlicensed_subset.csv", "w", encoding="utf-8", newline="") as file:
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

    with open("temp4.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Parent License", "Child License", "Type", "Count"])
        for row in rows:
            writer.writerow(row)

def getArxivInTags():

    def containsPaperLink(tags):
        for tag in tags:
            if tag.startswith("arxiv:"):
                return True
        return False

    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    files = glob.glob(path)
    count = 0
    ids = set()
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            if data["_id"] in ids: continue
            tags = data.get("tags", [])
            if containsPaperLink(tags):
                    count += 1
            ids.add(data["_id"])
    print("Models with arXiv links:", count)
    print("Total models:", len(ids))

def getUniqueLicensesForModels():
    q = Querier()
    c = q.getLicenseFrequencies(True)
    licenses = set()
    for lic in c.keys():
        for l in lic.split("|"):
            licenses.add(l)
    licenses = sorted(list(licenses))
    with open("temp5.csv", "w", encoding="utf-8", newline="") as file:
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
    with open("temp6.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["License", "Type"])
        writer.writerows([[l] for l in licenses])

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
    with open("temp7.csv", "w", encoding="utf-8", newline="") as file:
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
    with open("temp8.csv", "w", encoding="utf-8", newline="") as file:
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
    with open("temp9.csv", "w", encoding="utf-8", newline="") as file:
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

def getInstancesOf404():
    data = loadModelData()
    count = 0
    for model in data:
        for base in model["bases"]:
            if base["id"] is not None and base["id"].startswith("404"):
                count += 1
    print(f"Models with 404 references: {count}")

def getDuplicates():
    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    files = glob.glob(path)
    uniques = {}
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            if data["id"] in uniques:
                uniques[data["id"]].append(f)
            else:
                uniques[data["id"]] = [f]
    duplicates = {k:v for k, v in uniques.items() if len(v) > 1}
    print(len(duplicates))
    with open("temp10.json", "w", encoding="utf-8") as file:
        json.dump(duplicates, file, indent=4)

def getPulledList():
    path = os.path.join("data", "raw_data", "model_lists", "*.json")
    files = glob.glob(path)
    models = []
    for f in files:
        with open(f, "r", encoding="utf-8") as file:
            data = json.load(file)
            models.extend(data)
    return models

def analyzeDuplicates():
    lyst = getPulledList()
    ids = {model["id"] for model in lyst}
    print(len(lyst), len(ids))

    def cleanValue(v):
        v = v.split(os.sep)[-1]
        index = v.rfind("_")
        v = v[:index]
        return v.replace(MODEL_SEPERATOR, "/")

    with open("temp10.json", "r", encoding="utf-8") as file:
        duplicates = json.load(file)
        for k, v in duplicates.items():
            if len([value in ids for value in v if cleanValue(value) in ids]) > 1:
                print(k, v)
    print("Done")

def getModelsWithDatasets():
    data = loadModelData()
    count = 0
    for model in data:
        if len(model["datasets"]) > 0:
            count += 1
    print(f"Models with datasets: {count}")

def getModelsWithBases():
    data = loadModelData()
    count = 0
    for model in data:
        if len(model["bases"]) > 0:
            count += 1
    print(f"Models with bases: {count}")

def getFrequenciesForModelsWithDatasets():
    data = loadModelData()
    frequencies = []
    for model in data:
        frequencies.append(len(model["datasets"]))
        if len(model["datasets"]) == 287:
            print(model)
    print(Counter(frequencies))

def getDeclaredDatasetFrequencies():
    data = loadModelData()
    frequencies = []
    for model in data:
        for dataset in model["datasets"]:
            if dataset.get("id") != None:
                id = INDEX.getDatasetName(dataset["id"])
                if id != None:
                    frequencies.append(id)        
    c = Counter(frequencies)
    datasets = [d[0] for d in c.most_common(10)]
    for d in loadDatasetData():
        if d["internal_id"] == "627007d3becab9e2dcf15a40":
            print(d)
        # if d["id"] in datasets:
        #     print(d["id"], d["likes"], d["downloads"], d["license"])

# print(INDEX.getModelID("FacebookAI/xlm-roberta-base"))
# print(INDEX.getDatasetID("ilsvrc/imagenet-1k"))

# with open("temp10.json", "r", encoding="utf-8") as file:
#     duplicates = json.load(file)
#     print(len(duplicates))
#     s = 0
#     for v in duplicates.values():
#         s += len(v) - 1
#     print(s)



# data = [d["id"] for d in loadModelData()]
# unique = {d for d in data}
# print(len(data), len(unique))
# getDuplicates()

# i = Index().getInstance()
# print(i.getDatasetID("doi:10.57967/hf/2192"))
# print(i.getModelName(i.getDatasetID("doi:10.57967/hf/2192")))
# # print(i.getModelID("fine-tuned/fiqa2018-256-24-gpt-4o-2024-05-13-992459"))
# # model_id = i.getDatasetID("doi:10.57967/hf/0171")
# # print(model_id)
# # model_name = i.getDatasetName(model_id)
# # print(model_name)
# # print(i.getModelName(model_id))


# files = glob.glob(os.path.join("data", "cleaned_data" ,"model_data", "*.json"))
# models = []
# for file in files:
#     with open(file, "r", encoding="utf-8") as f:
#         models.extend(json.load(f))

# broken = set()
# for m in models:
#     for d in m["datasets"]:
#         if d["id"] == None:
#             broken.add(d["declared"])
#             # print(m)

# with open("interesting_datasets.json", "w", encoding="utf-8") as file:
#     json.dump(sorted(list(broken)), file, indent=4)
        