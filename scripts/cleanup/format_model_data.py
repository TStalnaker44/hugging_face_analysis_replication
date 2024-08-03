
import os, glob, json
from ..utils import makeFolder, loadJSON
from ..utilities.thread_manager import ThreadManager
from ..utilities.index import INDEX

def main(thread_count=5):
    cleaner = ModelDataCleaner()
    cleaner.clean(thread_count)

def segment_list(lyst, x):
    return [lyst[i:i + x] for i in range(0, len(lyst), x)]

def parseDataFromTags(tags, target):
    hits = []
    for tag in tags:
        if tag.startswith(target + ":"):
            hits.append(tag.split(":")[-1])
    return hits

def combineDataSources(*lists):
    combined = []
    for l in lists: combined.extend(l)
    return sorted(list(set(combined)))

def loadModels():
    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    files = glob.glob(path)
    return files

def loadJSON(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def saveDataToFile(data):
    segmented = segment_list(data, 10000)
    for i, seg in enumerate(segmented):
        path = os.path.join("data", "cleaned_data", "model_data", f"data_{i:02d}.json")
        with open(path, "w", encoding="utf-8") as file:
            json.dump(seg, file)
        
class ModelDataCleaner:

    def __init__(self):
        makeFolder(os.path.join("data", "cleaned_data", "model_data"))

    def clean(self, thread_count=5):
        files = loadModels()
        data = self.parseModelFiles_withThreads(files, thread_count)
        path = os.path.join("data", "raw_data", "html_to_json.json")
        html_data = loadJSON(path) if path else []
        data = self.removeDuplicates(data + html_data)
        saveDataToFile(data)

    def removeDuplicates(self, data):
        seen, unique = set(), list()
        for d in data:
            if d["id"] in seen or d["id"]==None: continue
            seen.add(d["id"])
            unique.append(d)
        return unique

    def parseModelFiles_withThreads(self, files, thread_count=5):
        threads = ThreadManager(self.parseModelFiles, files, thread_count)
        threads.run()
        threads.join()
        models = []
        for result in threads.get_results():
            models.extend(result)
        return models

    def parseModelFiles(self, files):
        models = []
        for f in files:
            with open(f, "r", encoding="utf-8") as file:
                data = json.load(file)
                model_data = self.extractModelData(data)
                models.append(model_data)
        return models

    def extractBaseData(self, bases):
        base_data = []
        for base in bases:
            data = {}
            declared = base.strip()
            if declared == "None": continue
            data["declared"] = declared
            data["ambiguous"] = not "/" in base
            data["id"] = INDEX.getModelID(declared)
            base_data.append(data)
        return base_data

    def extractDatasetData(self, datasets):
        dataset_data = []
        for d in datasets:
            data = {}
            declared = d.strip()
            data["declared"] = declared
            data["ambiguous"] = not "/" in declared
            data_id = INDEX.getDatasetID(declared)
            if data_id and INDEX.getModelName(data_id):
                data["note"] = "Declared dataset is actually a model."
            if data_id is None:
                data_id = INDEX.getModelID(declared)
                if not data_id is None: 
                    data["note"] = "Declared dataset is actually a model."
            data["id"] = data_id
            dataset_data.append(data)
        return dataset_data

    def extractModelData(self, data):

        model = {}
        model["id"] = data["_id"]
        model["name"] = data["id"]
        model["downloads"] = data["downloads"]
        model["likes"] = data["likes"]

        tag_licenses = parseDataFromTags(data["tags"], "license")
        meta_licenses = data.get("cardData", {}).get("license", [])
        if type(meta_licenses) == str: meta_licenses = [meta_licenses]
        model["licenses"] = combineDataSources(tag_licenses, meta_licenses)

        tag_datasets = parseDataFromTags(data["tags"], "dataset")
        meta_datasets = data.get("cardData", {}).get("datasets", [])
        model["datasets"] = self.extractDatasetData(combineDataSources(tag_datasets, meta_datasets))

        tag_bases = parseDataFromTags(data["tags"], "base_model")
        meta_bases = data.get("cardData", {}).get("base_model", [])
        if type(meta_bases) == str: meta_bases = [meta_bases]
        model["bases"] = self.extractBaseData(combineDataSources(tag_bases, meta_bases))

        model["architectures"] = data.get("config", {}).get("architectures", [])
        
        return model
            