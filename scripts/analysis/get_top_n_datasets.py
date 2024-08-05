from ..utils import loadDatasetData

import pandas as pd

def main():
    datasets = loadDatasetData()

    df = pd.DataFrame(datasets)
    
    #Set n for the Top-n
    n = 10

    #df.head(n)

    print("Top-" + str(n) + " datasets by likes:")
    print(get_top_n_by_likes(df, n))

    print("Top-" + str(n) + " datasets by downloads:")
    print(get_top_n_by_downloads(df, n))

def get_top_n_by_likes(df, n):
    by_likes = df.sort_values(by = "likes", ascending = False)
    return by_likes.head(n)

def get_top_n_by_downloads(df, n):
    by_downloads = df.sort_values(by = "downloads", ascending = False)
    return by_downloads.head(n)