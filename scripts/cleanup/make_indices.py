
import os, glob, json
from ..utils import saveJsonToFile

def getFiles(folder):
    path = os.path.join("data", "raw_data", folder, "*.json")
    return glob.glob(path)

def loadModels():
    return getFiles("model_lists")

def loadDatasets():
    return getFiles("dataset_lists")

def parseFiles(files):
    id_to_name, name_to_id = {}, {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for d in data:
                id_to_name[d["_id"]] = d["id"].lower()
                name_to_id[d["id"].lower()] = d["_id"]
    return id_to_name, name_to_id

def makeIndices():

    files = loadModels()
    id_to_model, model_to_id = parseFiles(files)
    saveJsonToFile(os.path.join("data", "cleaned_data", "indices", "id_to_model.json"), id_to_model)
    saveJsonToFile(os.path.join("data", "cleaned_data", "indices", "model_to_id.json"), model_to_id)

    files = loadDatasets()
    id_to_dataset, dataset_to_id = parseFiles(files)
    saveJsonToFile(os.path.join("data", "cleaned_data", "indices", "id_to_dataset.json"), id_to_dataset)
    saveJsonToFile(os.path.join("data", "cleaned_data", "indices", "dataset_to_id.json"), dataset_to_id)