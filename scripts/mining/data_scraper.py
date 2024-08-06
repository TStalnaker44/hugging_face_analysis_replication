
import requests, os, time, glob
from datetime import datetime
from ..config import MODEL_SEPERATOR
from ..utils import saveHTMLToFile, getModelHTMLFiles, makeFolder

MODEL_URL = "https://huggingface.co"

def loadDone():
    files = getModelHTMLFiles()
    done = []
    for file in files:
        file = file.split(os.sep)[-1]
        file = file.replace(MODEL_SEPERATOR, "/")
        done.append(file[:-16])
    return done

def load404s():
    path = os.path.join("data", "raw_data", "log_files", "no_page.txt")
    with open(path, "r", encoding="utf-8") as file:
        return file.read().strip().split("\n")

def loadFails(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        fails = f.read().strip().split("\n")
    done = ["https://huggingface.co/api/models/" + f for f in loadDone()]
    no_page = [f.replace("https://huggingface.co/",
                         "https://huggingface.co/api/models/") for f in load404s()]
    return [fail for fail in fails if (not fail in done) and (not fail in no_page)]

def mineWebPages(file_path):
    date = datetime.now().strftime('%m-%d-%Y')
    fails = loadFails(file_path)
    for fail in fails:
        owner, model = fail.split("/")[-2:]
        page_url = f"{MODEL_URL}/{owner}/{model}"
        file_name = f"{owner}{MODEL_SEPERATOR}{model}_{date}"
        html_path = os.path.join("data", "raw_data", "model_page_data", file_name[0])
        makeFolder(html_path)
        html_path = os.path.join(html_path, f"{file_name}.html")
        html_page = getPage(page_url)
        if html_page: saveHTMLToFile(html_path, html_page)
        time.sleep(2.5)
    
def getPage(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: {response.status_code} for {url}")
        path = os.path.join("data", "raw_data", "log_files", "no_page.txt")
        with open(path, "a", encoding="utf-8") as file:
            file.write(f"{url}\n")

