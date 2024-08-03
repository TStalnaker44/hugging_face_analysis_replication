
import os, csv, json
from ..utils import loadDatasetData, loadModelData


def createDatasetToLicenseDictionary():
    datasets = {}
    for d in loadDatasetData():
        datasets[d["internal_id"]] = d["license"]
    return datasets

def main():
    data = []
    dataset2license = createDatasetToLicenseDictionary()
    for model in loadModelData():
        license = "|".join(model["licenses"])
        if license != "":
            model_datasets = model["datasets"]
            if len(model_datasets) > 0:
                dlicenses = []
                for dataset in model_datasets:
                    dlicenses.extend(dataset2license.get(dataset["id"], []))
                dlicenses = sorted(list(set(dlicenses)))
                if len(dlicenses) > 0:
                    data.append({"model_id":model["id"], "model_name":model["name"], "model_license":license, 
                                 "dataset_licenses":dlicenses})
    with open(os.path.join("data", "analysis", "dataset_license_analysis.json"), "w") as f:
        json.dump(data, f, indent=4)

# models = loadModelData()
