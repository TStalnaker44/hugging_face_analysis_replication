
import json, os
from ..utils import makeFolder

def licenseInList(license, lic_list):
    for lic in lic_list:
        if license.lower() in lic.lower():
            return True
    return False

def loadChains():
    path = os.path.join("data", "cleaned_data", "chains.json")
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def findExamples():
    chains = loadChains()
    hits = []
    for model, chain in list(chains.items()):
        for path in chain:
            if len(path) > 2:
                hit = {}
                hit["tags"] = set()
                lic = sorted(path[0]["license"])
                mid = path[0]["model"]
                owners = set()
                owners.add(mid.split("/")[0])
                parent = mid
                if not "/" in mid: hit["tags"].add("ambiguous_base")
                for i, link in enumerate(path[1:]):
                    owners.add(link["model"].split("/")[0])
                    if "UNKNOWN" in lic: hit["tags"].add("unknown_license") 
                    new_lic = sorted(link["license"])
                    if new_lic != lic: hit["tags"].add("license_change")
                    if i == len(path[1:]) - 1 and "UNKNOWN" in new_lic: 
                        hit["tags"].add("ends_with_unknown_license")
                        hit["tags"].add("unknown_license")
                    if licenseInList("llama", new_lic) and "llama" not in link["model"].lower():
                        hit["tags"].add("llama_naming_issue")
                    if (not licenseInList("llama", new_lic)) and "llama" in link["model"].lower():
                        hit["tags"].add("missing_llama_license")
                    if "llama" in parent.lower() and ("llama" not in link["model"].lower() or not licenseInList("llama", new_lic)):
                        hit["tags"].add("undeclared_llama_dependency")
                    lic = new_lic
                    parent = link["model"]
                if hit["tags"]:
                    if len(owners) == 1: hit["tags"].add("single_owner")
                    hit["tags"] = sorted(list(hit["tags"]))
                    hit["chain"] = path
                    hits.append(hit)

    saveExamples(hits)

def saveExamples(hits):
    makeFolder(os.path.join("data", "analysis"))
    path = os.path.join("data", "analysis", "licensing_changes.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(hits, file, indent=4)

