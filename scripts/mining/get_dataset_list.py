
import re, requests, os
from datetime import datetime
from ..utils import makeFolder, saveJsonToFile


BASE_URL = "https://huggingface.co/api/datasets"

def main():
    getDatasets(500)
    print("Done!")

def prepareFolders():
    path = os.path.join("data", "raw_data")
    makeFolder(path)
    path = os.path.join("data", "raw_data", "dataset_lists")
    makeFolder(path)

def getDatasets(max_pages=1, start_page=1):
    prepareFolders()
    date = datetime.now().strftime('%m-%d-%Y')
    url = f"{BASE_URL}?sort=downloads"
    page = start_page
    stop = (max_pages + start_page)
    while url and page < stop:
        print(f"Mining page {page}")
        response = requests.get(url)
        if response.status_code == 200:
            models = response.json()
            link = response.headers.get("Link")
            if link:
                match = re.search("<.+>", link)
                if match:
                    url = match.group(0)[1:-1]
                else:
                    url = None
                if start_page <= page < stop:
                    path = os.path.join("data", "raw_data", "dataset_lists", 
                                        f"datasets_page{page}_{date}.json")
                    saveJsonToFile(path, models)
                page += 1
            else:
                break

if __name__ == "__main__":
    main()