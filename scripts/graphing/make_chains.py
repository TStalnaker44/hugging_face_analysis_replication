"""
This script takes the lineage (family tree) files created by create_lineages.py and creates linear
descent chains for each leaf model.  Each chain represents a path from a root model to a leaf model.
"""

import os, json, glob, ast

def main():

    files = glob.glob(os.path.join("data", "graphs", "lineages", "text", "*.txt"))

    chains = {}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            contents = f.read().strip().split("\n")
        i = 0
        model_chains = []
        while i < len(contents):
            new_chain = [convertLine2Dict(contents[i])]
            i += 1
            while i < len(contents) and contents[i].startswith(" "):
                new_chain.append(convertLine2Dict(contents[i].strip()))
                i += 1
            model_chains.append(new_chain)
        
        model_name = file.split(os.sep)[-1][:-4]
        chains[model_name] = model_chains

    ## Filter chains
    filtered = {}
    for model, chain in chains.items():
        if len(chain) > 1 or any(len(path) > 2 for path in chain):
            filtered[model] = chain

    path = os.path.join("data", "cleaned_data", "chains.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=4)

def isAList(s):
    try:
        result = ast.literal_eval(s)
        return isinstance(result, list)
    except (ValueError, SyntaxError):
        return False

def convertLine2Dict(content):
    try:
        model, license = content.split(" ", 1)
    except:
        print(content.split(" "))
    license = license[1:-1].split(", ") # Remove parenteheses
    return {"model": model, "license": license}

