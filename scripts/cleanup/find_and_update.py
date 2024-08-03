
import os, json, requests, time
from ..utils import makeFile, loadModelData, saveJsonToFile

def find_and_update_ambiguous_models():
    target_file = os.path.join("data", "cleaned_data", "indices", "model_ambig_to_standard.json")
    f = lambda base, mapping: base["ambiguous"] and base["declared"].lower() not in mapping
    main(target_file, f)

def find_and_update_renamed_models():
    target_file = os.path.join("data", "cleaned_data", "indices", "model_renamed.json")
    f = lambda base, mapping: base["id"] is None and "/" in base["declared"] and not base["declared"].lower() in mapping
    main(target_file, f)

def find_404_models():
    target_file = os.path.join("data", "cleaned_data", "indices", "404_list.json")
    main(target_file, lambda base, mapping: base["id"] is None, 404)

def find_and_update_ambiguous_datasets():
    target_file = os.path.join("data", "cleaned_data", "indices", "dataset_ambig_to_standard.json")
    f = lambda base, mapping: base["ambiguous"] and base["declared"].lower() not in mapping
    main(target_file, f, search="datasets")

def find_and_update_renamed_datasets():
    target_file = os.path.join("data", "cleaned_data", "indices", "dataset_renamed.json")
    f = lambda base, mapping: base["id"] is None and "/" in base["declared"] \
        and not base["declared"].lower() in mapping and base["declared"] != "/"
    main(target_file, f, search="datasets")

def find_and_update_renamed_datasets():
    target_file = os.path.join("data", "cleaned_data", "indices", "renamed_datasets.json")
    f = lambda base, mapping: base["ambiguous"] and base["declared"].lower() not in mapping
    main(target_file, f, search="datasets")

def replaceDOIs():
    path = os.path.join("data", "cleaned_data", "indices", "doi_to_datasets.json")
    makeFile(path)
    data = loadModelData()
    mapping = loadTargetData(path)
    func = lambda base, mapping: base["declared"].startswith("doi:") and base["declared"].lower() not in mapping
    hits = findTargetModelData(data, mapping, func, "datasets")
    base_url = "https://doi.org/"
    for hit in hits:
        response = requests.get(base_url + hit.replace("doi:", ""))
        if response.status_code == 200:
            url = response.url.replace("https://huggingface.co/datasets/", "")
            url = response.url.replace("https://huggingface.co/", "")
            if "/" in url: mapping[hit] = url
        time.sleep(.15)
    saveJsonToFile(path, mapping)

def main(path, func, code=200, search="bases"):  
    makeFile(path)
    data = loadModelData()
    mapping = loadTargetData(path)
    hits = findTargetModelData(data, mapping, func, search)
    updateMapping(hits, mapping, code, search)
    saveJsonToFile(path, mapping)

def loadTargetData(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}
    
def findTargetModelData(data, mapping, func, search="bases"):
    targets = set()
    for model in data:
        for base in model[search]:
            if func(base, mapping):
                targets.add(base["declared"].lower())
    return sorted(list(targets))

def updateMapping(hits, mapping, code=200, search="bases"):
    base_url = "https://huggingface.co/"
    if search == "datasets": base_url += "datasets/"
    for hit in hits:
        response = requests.get(base_url + hit)
        if response.status_code == code:
            url = response.url.replace(base_url, "")
            if "/" in url: mapping[hit] = url
        time.sleep(.15)