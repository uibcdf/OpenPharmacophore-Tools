from itertools import combinations
import random
from typing import List
import networkx as nx

nodelabels = ["A", "D", "E", "H", "I", "N", "P", "R"]
edgelabels = list(range(1, 10))

def random_graph(min_num_nodes: int,
                max_number_nodes: int) -> nx.Graph:

    if min_num_nodes < 0 or max_number_nodes < 0:
        raise ValueError("Number of nodes must be greater than zero")

    if max_number_nodes < min_num_nodes:
        raise ValueError("Max number of nodes must be greater than min number of npdes")
    
    graph = nx.Graph()
    n_nodes = random.choice(range(min_num_nodes, max_number_nodes + 1))
    nodes = list(range(1, n_nodes + 1))

    for node in nodes:
        graph.add_node(node, feat_type=random.choice(nodelabels))
    
    for node1, node2 in combinations(nodes, 2):
        graph.add_edge(node1, node2, distance=random.choice(edgelabels))

    assert graph.number_of_edges() == (graph.number_of_nodes() * (graph.number_of_nodes() - 1)) / 2
    return graph

def print_graph(graph: nx.Graph) -> None:
    print("Nodes")
    for node, label in graph.nodes(data="feat_type"):
        print(node, label)
    print("\nEdges")
    for u, v in graph.edges:
        distance = graph[u][v]["distance"]
        print(f"({u}, {v}) {distance}")
