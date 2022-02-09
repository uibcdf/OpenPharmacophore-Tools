import canonical_code
from collections import Counter, defaultdict
import itertools
from typing import List
import networkx as nx
import pprint

def find_freq_2_cliques(graphs : List[nx.Graph], min_frequency=1) -> List[str]:
    """ Find all frequent 2-cliques in a set of graphs.

        Parameters
        ----------
        graphs : list of networkx.Graph
            A list with graphs

        min_frequency : int
            The minimum frequency of the clique. Number between 0 and 1

        Returns
        -------
        cliques : list of str
            A list with the frequent clieques represented by their canonical label.
    """
    cliques_count = {}
    min_frequency = int(min_frequency * len(graphs))

    for graph in graphs:
        labels = []
        for clique in itertools.combinations(graph.nodes, 2):
            node1 = graph.nodes[clique[0]]["feat_type"]
            node2 = graph.nodes[clique[1]]["feat_type"]
            edge = str(graph[clique[0]][clique[1]]["distance"])
            if node1 < node2:
                can_label = node1 + node2 + edge
            else:
                can_label = node2 + node1 + edge
            
            # In case a canonical label was already found in a graph it shoouldn't be counted more than one 
            if can_label not in labels:            
                try:
                    cliques_count[can_label] += 1
                except KeyError:
                    cliques_count[can_label] = 1
            
            labels.append(can_label)    

    return [clique for clique in cliques_count.keys() if cliques_count[clique] >= min_frequency] 


def grow_clique(graphs : list, cliques : list, clique_size : int, min_frequency=1) -> list:
    """ Grows a set of n-cliques to (n+1)-cliques.
    
        Parameters
        ----------
        graphs : list of networx.Graph
            A list with graphs
        
        cliques : list of str
            List of cliques of the same size represented by their canonical code.

        clique_size: int
            The size of the original cliques

        min_frequency : int
            The minimum frequency of the clique. Number between 0 and 1

        Returns
        -------
        cliques : list of str
            List of cliques of with one more node than the cliques passed to the function.
        
    """
    # TODO: Finds all frequent cliques by enumerating all posible combinations. This should be improved to 
    # just use the cliques that have the original cliques as a prefix

    new_cliques = []
    min_frequency = int(min_frequency * len(graphs))

    for graph_ in graphs:
        # Try all combinations of (n+1)-cliques.
        for node_combination in itertools.combinations(graph_.nodes, clique_size + 1):
            can_label = canonical_code.minimum_canonical_code(graph_, node_combination)
            new_cliques.append(can_label)

    # Find all (n+1)-cliques that have one of the frequent cliques as a prefix
    pruned_cliques = []
    for clique_ in cliques:
        for new_clique_ in new_cliques:
            if new_clique_.startswith(clique_):
                pruned_cliques.append(new_clique_)

    cliques_count = Counter(pruned_cliques)

    return [clique for clique in cliques_count.keys() if cliques_count[clique] >= min_frequency] 


def clique_detection_naive(graphs: List[nx.Graph]) -> List[str]:
    """ Found the largest cliques that are present in all graphs of a set of graphs.
        This algorithm enumerates all the cliques in each graph.
    """
    cliques = {}
    min_number_nodes = min(graphs, key=lambda g: g.number_of_nodes()).number_of_nodes()

    # Find all cliques of size <= min_number_nodes
    for ii, graph in enumerate(graphs):
        for jj in range(2, min_number_nodes + 1):
            for node_comb in itertools.combinations(graph.nodes, jj):
                try:
                    cliques[canonical_code.minimum_canonical_code(graph, node_comb)] += 1
                except KeyError:
                    cliques[canonical_code.minimum_canonical_code(graph, node_comb)] = 1

    # pprint.pprint(cliques)

    # Find the cliques with count == len(graphs)
    frequent_cliques = []
    max_clique_size = 0
    for clique, count in cliques.items():
        if count == len(graphs):
            frequent_cliques.append(clique)
            if len(clique) > max_clique_size:
                max_clique_size = len(clique)
    
    # Prune cliques of smaller sizw
    return [c for c in frequent_cliques if len(c) == max_clique_size]


