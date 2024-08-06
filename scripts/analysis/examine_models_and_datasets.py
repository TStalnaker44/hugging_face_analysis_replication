
from ..utils import loadDatasetData, loadModelData, loadRawModelData
from collections import Counter
from ..utilities.index import INDEX

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

def getArxivInTags():

    def containsPaperLink(tags):
        for tag in tags:
            if tag.startswith("arxiv:"):
                return True
        return False
    
    models = loadRawModelData()
    count = 0
    ids = set()
    for model in models:
        if model["_id"] in ids: continue
        tags = model.get("tags", [])
        if containsPaperLink(tags):
                count += 1
        ids.add(model["_id"])
    print("Models with arXiv links:", count)
    print("Total models:", len(ids))

def getInstancesOf404():
    data = loadModelData()
    count = 0
    for model in data:
        for base in model["bases"]:
            if base["id"] is not None and base["id"].startswith("404"):
                count += 1
    print(f"Models with 404 references: {count}")