
import glob, os, json

def loadModelData():
    path = os.path.join("data", "cleaned_data", "model_data", "*.json")
    files = glob.glob(path)
    data = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
    return data

def loadDatasetData():
    path = os.path.join("data", "cleaned_data", "datasets.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def getAllModelFiles():
    path = os.path.join("data", "raw_data", "api_data", "model_data_from_list", "*.json")
    list_files = glob.glob(path)
    path = os.path.join("data", "raw_data", "api_data", "additional_model_data", "*.json")
    additional_files = glob.glob(path)
    return list_files + additional_files
    
def loadJSON(file):
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def makeFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def makeFile(file):
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            pass
def saveJsonToFile(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)

def saveHTMLToFile(path, data):
    with open(path, "w", encoding="utf-8") as file:
        file.write(data)