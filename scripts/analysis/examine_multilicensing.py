
import pprint
from collections import Counter
from ..utils import loadModelData, loadDatasetData

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
    c = Counter(datasets)
    pprint.pprint(c)