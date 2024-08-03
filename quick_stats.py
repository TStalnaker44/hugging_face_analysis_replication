
from scripts.utilities.querier import Querier
from scripts.utilities.index import INDEX

q = Querier()

print()

print(f"Models in dataset: {q.getModelCount()}")
most_downloads = q.getModelWithMostDownloads()
print(f"Model with most downloads: {most_downloads['name']} -- {most_downloads['downloads']} downloads")
most_likes = q.getModelWithMostLikes()
print(f"Model with most likes: {most_likes['name']} -- {most_likes['likes']} likes")

print()

print(f"Unique licensing combinations: {len(q.getLicenseList())}")
print("Top 10 most common licensing combinations:")
for license, count in q.getLicenseFrequencies().most_common(10):
    print(f"\t{license}: {count}")

print()

print(f"Unique identifiable base models: {len(q.getBaseModelList())}")
print("Top 10 most common base models:")
for base, count in q.getBaseModelFrequencies().most_common(10):
    print(f"\t{INDEX.getModelName(base)}: {count}")

print()

print(f"Unique identifiable datasets: {len(q.getDatasetList())}")
print("Top 10 most common datasets:")
for dataset, count in q.getDatasetFrequencies().most_common(10):
    print(f"\t{INDEX.getDatasetName(dataset)}: {count}")