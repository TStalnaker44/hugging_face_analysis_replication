
import os, json
import networkx as nx
from collections import Counter

def main():
    graph = loadGraph()
    simple_cycles = list(nx.simple_cycles(graph))
    print(f"Count of simple cycles: {len(simple_cycles)}")
    print(simple_cycles[0])
    all_cycles = list(find_all_cycles(graph))
    all_cycles = filter_cycles(all_cycles)
    print(f"Count of all cycles: {len(all_cycles)}")

    trivial_cycles = count_trivial_cycles(all_cycles)
    print(f"Count of trivial cycles: {trivial_cycles}")

    owner_counts = owners_in_cycle(all_cycles)
    print(owner_counts)

    cycle_sizes = get_cycle_sizes(all_cycles)
    print(cycle_sizes)

    responsible_owners = get_responsible_owners(all_cycles)
    print(f"Count of owners responsible for cycles: {len(responsible_owners)}")

    owner_counts = get_owner_counts(all_cycles)
    print(owner_counts)

    with open("cycles.json", "w", encoding="utf-8") as file:
        json.dump(all_cycles, file, indent=4)


def get_owner_counts(cycles):
    return Counter([cycle[0].split("/")[0] for cycle in cycles])

def get_responsible_owners(cycles):
    return {cycle[0].split("/")[0] for cycle in cycles}

def get_cycle_sizes(cycles):
    return Counter([len(cycle) for cycle in cycles])

def count_trivial_cycles(cycles):
    return len([cycle for cycle in cycles if len(cycle) == 1])

def owners_in_cycle(cycles):
    owner_counts = []
    for cycle in cycles:
        owners = set()
        for node in cycle:
            owners.add(node.split("/")[0])
        owner_counts.append(len(owners))
    return Counter(owner_counts)
        

def filter_cycles(cycles):
    """Remove cycles with different starting points but the same nodes."""
    filtered_sets = []
    filtered_cycles = []
    for cycle in cycles:
        if not set(cycle) in filtered_sets:
            filtered_sets.append(set(cycle))
            filtered_cycles.append(cycle)
    return filtered_cycles

def find_all_cycles(G):
    cycles = []

    def dfs(node, visited, stack):
        if node in stack:
            cycle_start_index = stack.index(node)
            cycles.append(stack[cycle_start_index:])
            return

        visited.add(node)
        stack.append(node)
        
        for neighbor in G[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, stack)
            elif neighbor in stack:
                cycle_start_index = stack.index(neighbor)
                cycles.append(stack[cycle_start_index:])

        stack.pop()

    for node in G:
        dfs(node, set(), [])
    
    return cycles


def loadGraph():
    path = os.path.join("data", "graphs", "model_relationship_graph.graphml")
    return nx.read_graphml(path)

