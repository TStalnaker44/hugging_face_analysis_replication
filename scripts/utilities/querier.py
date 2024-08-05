
from ..utils import loadModelData
from collections import Counter

class Querier():

    def __init__(self):
        self.data = loadModelData()

    def getModelCount(self):
        return len(self.data)

    def setData(self, data):
        self.data = data

    def getModelWithMostDownloads(self):
        return max(self.data, key=lambda x: x["downloads"])
    
    def getModelWithMostLikes(self):
        return max(self.data, key=lambda x: x["likes"])

    def getModelsByLikes(self, min_likes, max_likes=None):
        if not max_likes:
            return [model for model in self.data if model["likes"] >= min_likes]
        else:
            return [model for model in self.data if model["likes"] >= min_likes and model["likes"] <= max_likes]

    def getModelsByDownloads(self, min_downloads, max_downloads=None):
        if not max_downloads:
            return [model for model in self.data if model["likes"] >= min_downloads]
        else:
            return [model for model in self.data if model["likes"] >= min_downloads and model["likes"] <= max_downloads]

    def getLicenseList(self):
        licenses = set()
        for model in self.data:
            for license in model["licenses"]:
                licenses.add(license)
        return sorted(list(licenses))
    
    def getLicenseFrequencies(self, combineOther=False):
        licenses = []
        for model in self.data:
            if combineOther:
                lics = []
                for lic in model["licenses"]:
                    if lic.endswith("(other)"): lics.append("other")
                    else: lics.append(lic)
            else: lics = model["licenses"]
            lics.sort()
            licenses.append("|".join(lics))
        return Counter(licenses)
    
    def getModelsByLicense(self, license):
        if type(license) == str: license = [license]
        if license == [""]: license = []
        models = []
        for model in self.data:
            if sorted(license) == sorted(model["licenses"]):
                models.append(model)
        return models
    
    def getBaseModelList(self):
        base_models = set()
        for model in self.data:
            for base in model["bases"]:
                if base["id"] is not None:
                    base_models.add(base["id"])
        return sorted(list(base_models))

    def getBaseModelFrequencies(self):
        bases = []
        for model in self.data:
            for base in model["bases"]:
                bases.append(base["id"])
        return Counter(bases)

    def getModelsByBase(self, base_id):
        models = []
        for model in self.data:
            for base in model["bases"]:
                if base["id"].lower() == base_id.lower():
                    models.append(model)
        return models
    
    def getDatasetList(self):
        datasets = set()
        for model in self.data:
            for data in model["datasets"]:
                if data["id"] is not None:
                    datasets.add(data["id"])
        return sorted(list(datasets))

    def getModelsByDataset(self, dataset_id):
        models = []
        for model in self.data:
            for data in model["datasets"]:
                if data["id"].lower() == dataset_id.lower():
                    models.append(model)
        return models
    
    def getDatasetFrequencies(self):
        datasets = []
        for model in self.data:
            for data in model["datasets"]:
                datasets.append(data["id"])
        return Counter(datasets)
    
    def getDatasetPerModelCounts(self):
        counts = []
        for model in self.data:
            counts.append(len(model["datasets"]))
        return Counter(counts)
    
    def getModelsByOwner(self, owner):
        models = []
        for model in self.data:
            if model["name"].split("/")[0].lower() == owner.lower():
                models.append(model)
        return models
    
    def getArchitectureList(self):
        architectures = set()
        for model in self.data:
            for architecture in model["architectures"]:
                architectures.add(architecture)
        return sorted(list(architectures))
    
    def getModelById(self, modelId):
        hits = []
        for model in self.data:
            if model['id'] == modelId:
                hits.append(model)
        if len(hits) == 1:
            return hits[0]
        if len(hits) > 1:
            print("Warning: muliple models found for id " + str(modelId))
            return hits
        else:
            print('No models found for id ' + str(modelId))
            return None