
import os, json
from ..utils import loadModelData
from ..utilities.querier import Querier


def main():
    q = Querier()
    models = q.getModelsByLicense("llama3")
    print(len(models))
    starts_count = 0
    contains_count = 0
    contains_llama_count = 0
    contains_l3_count = 0
    for model in models:
        name = model["name"].split("/")[-1].lower()
        if name.startswith("llama3"):
            starts_count += 1
        if "llama3" in name:
            contains_count += 1
        if "llama" in name:
            contains_llama_count += 1
        if "l3" in name: ##or "llama" in name:
            contains_l3_count += 1
    print(f"Starts with llama3: {starts_count}")
    print(f"Contains llama3: {contains_count}")
    print(f"Contains llama: {contains_llama_count}")
    print(f"Contains l3: {contains_l3_count}")
    # data = loadModelData() 