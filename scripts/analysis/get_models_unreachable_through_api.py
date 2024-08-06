import os, json
from bs4 import BeautifulSoup
from scripts.utils import getModelHTMLFiles

def findConsentCount():           
    files = getModelHTMLFiles()
    gated_list = []
    disabled_list = []
    missing = []
    restricted = []
    for f in files:
        soup = getSoup(f)
        gated = soup.find("div", attrs= {"data-target":"RepoGatedModal"})
        headings = soup.findAll("h2")
        if isDisabled(headings): disabled_list.append(f)
        elif gated: gated_list.append(f)
        elif is404(soup.findAll("h1")): missing.append(f)
        elif isRestricted(soup): restricted.append(f)
        else: print(f)
    print("Models requiring consent:", len(gated_list))
    print("Models that are disabled:", len(disabled_list))
    print("Models that are missing:", len(missing))
    print("Models that are restricted:", len(restricted))
    d = {"gated": gated_list, "disabled": disabled_list, "missing": missing, "restricted": restricted}
    path = os.path.join("data", "analysis", "unreachable_through_api.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(d, file, indent=4)

def getSoup(file):
        with open(file, "r", encoding="utf-8") as f:
            return BeautifulSoup(f, "html.parser")
        
def isDisabled(headings):
    for h in headings:
        if h.text.strip() == "Access to this model has been disabled":
            return True
    return False

def is404(headings):
    for h in headings:
        if h.text.strip() == "404":
            return True
    return False

def isRestricted(soup):
    for span in soup.findAll("span"):
        if span.text.strip() == "Not-For-All-Audiences":
            return True
    return False