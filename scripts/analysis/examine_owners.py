from ..utils import loadModelData, print_stats

import collections

import pandas as pd

import matplotlib.pyplot as plt


def main():
    models = loadModelData()
    df = pd.DataFrame(models)

    #Set n for the Top-n
    n = 10

    #The raw data has a mix of ints and string labels in the downloads column: cast all to integers.
    df['downloads'] = df['downloads'].apply(lambda x: int(x))

    #df.head(n)

    models_by_owner = map_ownership(df)
    print("Number of model owners:", len(models_by_owner.keys()))
    owned_models = [len(k) for k in models_by_owner.values()] #Convert dictionary into a list containing the numbers of models owned by each owenr
    print_stats(owned_models, "Number of owned models")

    #Print the n most prolific model owners
    print("Top-" + str(n) + " model owners: ")
    sorted_owners = sorted(models_by_owner.items(), key = lambda i: len(i[1]), reverse = True)
    ordered_owners = collections.OrderedDict(sorted_owners)
    for i in list(ordered_owners.keys())[:n]:
        print(" " + str(i) + " " + str(len(ordered_owners[i])))

    #plt.plot(owned_counts)


#Get all model owners in the dataset, create a dictionary mapping them to the models they own
def map_ownership(df):
    names = df['name']
    owners = set()
    models_by_owner = dict()
    for name in names:
        owner = name.split('/')[0].lower()
        owners.add(owner)
        if owner in models_by_owner.keys():
            models_by_owner[owner].append(name)
        else:
            models_by_owner[owner] = [name]
    return models_by_owner