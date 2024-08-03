
import os
import networkx as nx
from ..utils import loadModelData, makeFolder, saveJsonToFile
from ..utilities.index import INDEX

def main():
    G = createModelRelationshipGraph()
    saveGraph(G)

def createModelRelationshipGraph():
    G = nx.DiGraph()
    data = loadModelData()
    for model in data:
        base_models = model.get("bases", None)
        model_name = model["name"].lower()
        addNode(G, model_name)

        for base in base_models:
            base_id = base.get("id", None)
            base_name = INDEX.getModelName(base_id, base.get("declared", None))
            if base_name:
                base_name = base_name.lower()
                addNode(G, base_name)
                G.add_edge(base_name, model_name)
    return G

def addNode(G, node):
    if not G.has_node(node):
        G.add_node(node)
    
def saveGraph(G):
    path = os.path.join("data", "graphs", "model_relationship_graph.graphml")
    makeFolder(os.path.join("data", "graphs"))
    nx.write_graphml(G, path)
    data = nx.node_link_data(G)
    path = os.path.join("data", "graphs", "model_relationship_graph.json")
    saveJsonToFile(path, data)