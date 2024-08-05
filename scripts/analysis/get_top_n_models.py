from ..utils import loadModelData

import pandas as pd

def main():
    models = loadModelData()

    df = pd.DataFrame(models)

    #Set n for the Top-n
    n = 10

    #The raw data has a mix of ints and string labels in the downloads column: cast all to integers.
    df['downloads'] = df['downloads'].apply(lambda x: int(x))

    #df.head(n)

    print("Top-" + str(n) + " models by likes:")
    print(get_top_n_by_likes(df, n))

    print("Top-" + str(n) + " models by downloads:")
    print(get_top_n_by_downloads(df, n))

def get_top_n_by_likes(df, n):
    by_likes = df.sort_values(by = "likes", ascending = False)
    return by_likes.head(n)

def get_top_n_by_downloads(df, n):
    by_downloads = df.sort_values(by = "downloads", ascending = False)
    return by_downloads.head(n)