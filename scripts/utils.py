
import glob, os, json
import collections
import numpy as np

def loadModelData():
    path = os.path.join("data", "cleaned_data", "model_data", "*.json")
    files = glob.glob(path)
    data = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data.extend(json.load(f))
    return data

def loadRawModelData():
    path = os.path.join("data", "raw_data", "model_data")
    subfolders = [item for item in os.listdir(path) 
                  if os.path.isdir(os.path.join(path, item))]
    data = []
    for folder in subfolders:
        files = glob.glob(os.path.join(path, folder, "*.json"))
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                data.append(json.load(f))
    return data

def getModelHTMLFiles():
    path = os.path.join("data", "raw_data", "model_page_data")
    subfolders = [item for item in os.listdir(path) 
                  if os.path.isdir(os.path.join(path, item))]
    files = []
    for folder in subfolders:
        fs = glob.glob(os.path.join(path, folder, "*.html"))
        files.extend(fs)
    return files

def loadDatasetData():
    path = os.path.join("data", "cleaned_data", "datasets.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def loadChainsData():
    path = os.path.join("data", "cleaned_data", "chains.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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

#Takes a list of numbers, computes the average value, the count of each value in the list, Q1, Q2, and Q3
def print_stats(my_list, name = ""):
    if name:
        print(name + ":")
    avg = sum(my_list) / len(my_list)
    print(" Avg", avg)
    my_counter = collections.Counter(my_list)
    print(" " + str(my_counter))
    print(" Q1", np.percentile(my_list, 25))
    print(" Q2", np.percentile(my_list, 50))
    print(" Q3", np.percentile(my_list, 75))