
"""
This file mines and saves individual family trees for each leaf node in the model relationship graph.
The resultant files are saved in both JSON and GraphML formats.
"""

import os, json 
import networkx as nx
from ..utils import makeFolder, loadModelData
from ..config import MODEL_SEPERATOR
from ..utilities.index import INDEX

def main():
    G = loadGraph()
    license_data = createLicenseDict()
    getLineages(G, license_data)

def loadGraph():
    path = os.path.join("data", "graphs", "model_relationship_graph.json")
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return nx.readwrite.json_graph.node_link_graph(data)

def getRootNodes(G):
    return [node for node in G.nodes if G.in_degree(node) == 0]

def getLineageFor(node, G):
    return nx.dfs_tree(G, node)

def getLineages(G, license_data):
    G_rev = G.reverse()
    source_nodes = getRootNodes(G_rev)
    for i, node in enumerate(source_nodes):
        if i % 10000 == 0: print(f"Finding lineage for {i}/{len(source_nodes)}")
        subtree = getLineageFor(node, G_rev)
        subtree = subtree.reverse()
        saveData(subtree, node, license_data)

def saveData(graph, root, license_data):
    path = os.path.join("data", "graphs", "lineages")
    makeFolder(path)
    root_name = root.replace("/", MODEL_SEPERATOR)

    # Save as GraphML
    makeFolder(os.path.join(path, "graphml"))
    graph_path = os.path.join(path, "graphml", f"{root_name}.graphml")
    nx.write_graphml(graph, graph_path)
    
    # Save as JSON
    makeFolder(os.path.join(path, "json"))
    data = nx.node_link_data(graph)
    json_path = os.path.join(path, "json", f"{root_name}.json")
    with open(json_path, "w") as f:
        json.dump(data, f)

    # Save as txt (this option also adds licensing information)
    makeFolder(os.path.join(path, "text"))
    root_nodes = {node:{} for node in graph.nodes if graph.in_degree(node) == 0}
    addChildren(root_nodes, graph)
    output = printChildren(root_nodes, license_data)
    path = os.path.join(path, "text", f"{root_name}.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(output)

def addChildren(root_nodes, G):
    for root, children in root_nodes.items():
        for neighbor in G.neighbors(root):
            children[neighbor] = {}
        addChildren(children, G)

def printChildren(root_nodes, license_data, indent=0, output=""):
    for root, children in root_nodes.items():
        license = license_data.get(INDEX.getModelID(root), "UNDECLARED")
        if license == []: license = "UNDECLARED"
        if type(license) == list: license = ", ".join(license)
        output += ("  "*indent + root + f" ({license})") + "\n"
        output = printChildren(children, license_data, indent+1, output)
    return output

def createLicenseDict():
    licenses = {}
    for model in loadModelData():
        licenses[model["id"]] = model["licenses"]
    return licenses