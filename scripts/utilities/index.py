
import os
from ..utils import loadJSON

def lookup(d, key, default=None):
    return d.get(key.lower(), default)

class Index():

    _INDEX = None

    @classmethod
    def getInstance(cls):
        if cls._INDEX is None:
            cls._INDEX = cls._INTERNAL_INDEX()
        return cls._INDEX
    
    class _INTERNAL_INDEX():

        def __init__(self):
            self.loadIndices()

        def loadIndices(self):
            base_path = os.path.join("data", "cleaned_data", "indices")
            self.model_to_id = loadJSON(os.path.join(base_path, "model_to_id.json"))
            self.dataset_to_id = loadJSON(os.path.join(base_path, "dataset_to_id.json"))
            self.id_to_model = loadJSON(os.path.join(base_path, "id_to_model.json"))
            self.id_to_dataset = loadJSON(os.path.join(base_path, "id_to_dataset.json"))
            self.ambig_models = loadJSON(os.path.join(base_path, "model_ambig_to_standard.json"))
            self.ambig_datasets = loadJSON(os.path.join(base_path, "dataset_ambig_to_standard.json"))
            self.renamed_models = loadJSON(os.path.join(base_path, "model_renamed.json"))
            self.renamed_datasets = loadJSON(os.path.join(base_path, "dataset_renamed.json"))
            model_manual = loadJSON(os.path.join(base_path, "manual.json"))
            self.model_manual_to_id = model_manual
            self.id_to_model.update({v: k for k, v in model_manual.items()})
            missing = loadJSON(os.path.join(base_path, "404_list.json"))
            self.giveIDsToMissing(missing)
            datasets = loadJSON(os.path.join("data", "cleaned_data", "datasets.json"))
            self.doi_mapping = {d["doi"]:d["internal_id"] for d in datasets if d["doi"] is not None}
            self.doi_to_source = loadJSON(os.path.join(base_path, "doi_to_datasets.json"))
            self.id_to_doi = {d["id"]:d["doi"] for d in datasets if d["doi"] is not None}

        def giveIDsToMissing(self, missing):
            self.missing_to_ids = {}
            self.ids_to_missing = {}
            for i, m in enumerate(missing):
                self.missing_to_ids[m] = f"404_{str(i).zfill(4)}"
                self.ids_to_missing[f"404_{str(i).zfill(4)}"] = m

        def getDatasetID(self, dataset_name, default=None):
            if dataset_name == ".": return None
            dataset_id = lookup(self.dataset_to_id, dataset_name, default)
            if dataset_id is None:
                dataset_id = lookup(self.dataset_to_id, lookup(self.ambig_datasets, dataset_name, ""), None)
            if dataset_id is None:
                dataset_id = lookup(self.dataset_to_id, lookup(self.renamed_datasets, dataset_name, ""), None)
            if dataset_id is None:
                dataset_id = lookup(self.doi_mapping, dataset_name.replace("doi:", ""), None)
            if dataset_id is None:
                dataset_id = lookup(self.dataset_to_id, lookup(self.doi_to_source, dataset_name, ""), None)
            if dataset_id is None:
                dataset_id = lookup(self.model_to_id, lookup(self.doi_to_source, dataset_name, ""), None)
            if dataset_id is None:
                dataset_id = default
            return dataset_id
        
        def getModelID(self, model_name, default=None):
            model_id = lookup(self.model_to_id, model_name, None)
            if model_id is None:
                model_id = lookup(self.model_to_id, lookup(self.ambig_models, model_name, ""), None)
            if model_id is None:
                model_id = lookup(self.model_to_id, lookup(self.renamed_models, model_name, ""), None)
            if model_id is None:
                model_id = lookup(self.missing_to_ids, model_name, None)
            if model_id is None:
                model_id = lookup(self.model_manual_to_id, model_name, None)
            if model_id is None: 
                model_id = default
            return model_id
        
        def getModelName(self, model_id, default=None):
            if model_id is None: return default
            if model_id.startswith("404_"):
                return self.ids_to_missing.get(model_id, default)
            return self.id_to_model.get(model_id, default)
        
        def getDatasetName(self, dataset_id, default=None):         
            return self.id_to_dataset.get(dataset_id, default)



INDEX = Index.getInstance()