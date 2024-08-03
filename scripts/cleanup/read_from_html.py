
import os, glob
from bs4 import BeautifulSoup
from scripts.utilities.index import INDEX
from ..utils import saveJsonToFile

def main():
    files = glob.glob(os.path.join("data", "raw_data", "model_page_data", "*.html"))
    models = []
    for file in files:
        soup = getSoup(file)
        models.append(getMetaData(soup))
    path = os.path.join("data", "raw_data", "html_to_json.json")
    saveJsonToFile(path, models)
        
def getMetaData(soup):
    d = {}
    name = getModelName(soup)
    d["id"] = getModelID(name)
    d["name"] = name
    d["downloads"] = getDownloads(soup)
    d["likes"] = getLikes(soup)
    d["licenses"] = getLicenses(soup)
    d["datasets"] = getDatasetDetails(getDatasets(soup))
    d["bases"] = getBaseDetails(getBases(soup))
    d["architectures"] = [] # I don't think I can get this from the HTML
    return d

def getTextFromTag(txt):
    tags = txt.split("\n")[1:]
    return " ".join([t for t in tags if t not in ("", " ", "\t")])

def getSoup(file):
    with open(file, "r", encoding="utf-8") as f:
        return BeautifulSoup(f, "html.parser")

def getModelName(soup):
    return soup.find_all('meta', property='og:title')[0]['content'].split()[0]

def getModelID(name):
    return INDEX.getModelID(name)

def getLikes(soup):
    likes = soup.find_all('button', title='See users who liked this repository')[0].text
    if likes.endswith("k"): likes = int(float(likes[:-1]) * 1000)
    return int(likes)

def getDownloads(soup):
    definitions = soup.find_all('dl')
    for d in definitions:
        if d.find('dt').text.startswith("Downloads"):
            downloads = d.find('dd').text.replace(",", "")
            if downloads == "-": downloads = 0
            return downloads
    return 0

def getLicenses(soup):
    tag_class = "tag tag-white rounded-full relative rounded-br-none pr-2.5"
    hits = soup.find_all('div', class_=tag_class)
    licenses = []
    if hits: 
        for hit in hits:
            txt = hit.text.strip()
            if txt.startswith("License:"):
                licenses.append(getTextFromTag(txt))
    return licenses

DATABASE = """<ellipse cx="12.5" cy="5" fill="currentColor" fill-opacity="0.25" rx="7.5" ry="2"></ellipse><path d="M12.5 15C16.6421 15 20 14.1046 20 13V20C20 21.1046 16.6421 22 12.5 22C8.35786 22 5 21.1046 5 20V13C5 14.1046 8.35786 15 12.5 15Z" fill="currentColor" opacity="0.5"></path><path d="M12.5 7C16.6421 7 20 6.10457 20 5V11.5C20 12.6046 16.6421 13.5 12.5 13.5C8.35786 13.5 5 12.6046 5 11.5V5C5 6.10457 8.35786 7 12.5 7Z" fill="currentColor" opacity="0.5"></path><path d="M5.23628 12C5.08204 12.1598 5 12.8273 5 13C5 14.1046 8.35786 15 12.5 15C16.6421 15 20 14.1046 20 13C20 12.8273 19.918 12.1598 19.7637 12C18.9311 12.8626 15.9947 13.5 12.5 13.5C9.0053 13.5 6.06886 12.8626 5.23628 12Z" fill="currentColor"></path>"""

def getDatasets(soup):
    tag_class = "tag tag-white relative rounded-br-none pr-2.5"
    hits = soup.find_all('div', class_=tag_class)
    datasets = []
    if hits: 
        for hit in hits:
            if DATABASE in str(hit):
                datasets.append(hit.text.strip())
    # If only dataset counts are available, grab them
    tag_class = "tag tag-white"
    hits = soup.find_all('div', class_=tag_class)
    if hits: 
        for hit in hits:
            if "datasets" in hit.text:
                datasets.append(hit.text.strip())
    return datasets

def getBases(soup):
    hits = soup.find_all('div', attrs= {"data-target":"BaseModelDetails"})
    bases = []
    if hits: 
        for hit in hits:
            for txt in hit.text.strip().split():
                if "/" in txt: bases.append(txt)
    return bases

def getBaseDetails(bases):
    data = []
    for base in bases:
        d = {}
        d["declared"] = base
        d["ambiguous"] = not "/" in base
        d["id"] = INDEX.getModelID(base)
        data.append(d)
    return data

def getDatasetDetails(datasets):
    data = []
    for dataset in datasets:
        d = {}
        d["declared"] = dataset
        d["ambiguous"] = not "/" in dataset
        d["id"] = INDEX.getDatasetID(dataset)
        data.append(d)
    return data
