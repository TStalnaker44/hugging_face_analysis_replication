from ..utils import loadModelData, print_stats

import collections

import matplotlib.pyplot as plt

def main():

    models = loadModelData()

    counts = []
    for model in models:
        counts.append(len(model["datasets"]))

    print_stats(counts, "Number of declared datasets")

    #plt.hist(counts, bins = 50)