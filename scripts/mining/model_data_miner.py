
import requests, json, os, time, glob, re, threading
from datetime import datetime
from ..config import MODEL_SEPERATOR
from ..utils import makeFolder, makeFile, saveJsonToFile, saveHTMLToFile

API_URL = "https://huggingface.co/api/models"

def loadModelList():
    path = os.path.join("data", "raw_data", "model_lists", "models_page*.json")
    files = glob.glob(path)
    models = []
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            models.extend(json.load(f))
    return models

def filterModels(models):
    basepath = os.path.join("data", "raw_data", "api_data", "model_data_from_list")
    path = os.path.join(basepath, "*json")
    mined = glob.glob(path)
    mined = [model.replace(basepath, "").replace(MODEL_SEPERATOR, "/")[1:-16] for model in mined]
    path = os.path.join("data", "raw_data", "log_files", "failed.txt")
    with open(path, "r", encoding="utf-8") as file:
        failed = [m.replace(API_URL, "")[1:] for m in file.read().split()]
    path = os.path.join("data", "raw_data", "log_files", "unauthorized.txt")
    with open(path, "r", encoding="utf-8") as file:
        unauthorized = [m.replace(API_URL, "")[1:] for m in file.read().split()]
    mined = set(mined + unauthorized + failed)
    print(f"{len(mined)} models have already been mined")
    return [model for model in models if not model["modelId"] in mined]

def getAPIJson(url, lock):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 429:
        time.sleep(60)
    elif response.status_code == 401:
        print(f"Error: Unauthorized to access {url}")
        path = os.path.join("data", "raw_data", "log_files", "unauthorized.txt")
        with lock:
            with open(path, "a", encoding="utf-8") as file:
                file.write(f"{url}\n")   
    else:
        print(f"Error: {response.status_code} for {url}")
        path = os.path.join("data", "raw_data", "log_files", "failed.txt")
        with lock:
            with open(path, "a", encoding="utf-8") as file:
                file.write(f"{url}\n")

def prepareWorkspace():
    base_path = os.path.join("data", "raw_data")
    makeFolder(os.path.join("data", "raw_data", "api_data"))
    makeFolder(os.path.join(base_path, "api_data", "model_data_from_list"))
    makeFolder(os.path.join(base_path, "model_page_data"))
    makeFolder(os.path.join(base_path, "log_files"))
    makeFile(os.path.join(base_path, "log_files", "unauthorized.txt"))
    makeFile(os.path.join(base_path, "log_files", "failed.txt"))
    makeFile(os.path.join(base_path, "log_files", "no_page.txt"))

def mineData(max_models=500, thread_count=2):
    prepareWorkspace()
    models = loadModelList() # read models from file
    print(len(models))
    models = filterModels(models) # filter out models that have already been mined
    models = models[:max_models]  # limit the number of models to mine during this run
    date = datetime.now().strftime('%m-%d-%Y')
    print(f"Mining {max_models} models using HuggingFace API and {thread_count} threads...")

    lock = threading.Lock()

    model_split = len(models) // thread_count
    if model_split != len(models) / thread_count:
        extra = len(models) % thread_count
    else: extra = 0

    # Create threads
    threads = []
    for i in range(thread_count):
        start = i * model_split
        end = start + model_split
        if end + model_split >= max_models:
            end += extra
        print(start, end)
        th = threading.Thread(target=mine, args=(models[start:end], date, lock, 0.1, i))
        threads.append(th)

    # Start threads
    for th in threads:
        th.start()

    # Wait for both threads to complete
    for th in threads:
        th.join()

def mine(models, date, lock=None, sleep_time=0.1, thread_num=0):
    print(f"Starting thread {thread_num}...")
    progress = len(models) // 50
    interval = 5
    for i, model in enumerate(models):
        mid = model['modelId']
        api_url = f"{API_URL}/{mid}"
        file_name = mid.replace("/",MODEL_SEPERATOR) + f"_{date}"
        jsonpath = os.path.join("data", "raw_data", "api_data", "model_data_from_list", f"{file_name}.json")
        api_json = getAPIJson(api_url, lock)
        if api_json: saveJsonToFile(jsonpath, api_json)
        if i % interval == 0: time.sleep(.25)
        if i % progress == 0: print(f"Thread {thread_num}: {i}/{len(models)} models mined")
