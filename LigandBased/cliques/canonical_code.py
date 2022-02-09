from collections import defaultdict
from itertools import permutations, product
from typing import Sequence, Optional
from networkx import Graph

def canonical_code(graph : Graph, nodes : Sequence) -> str:
    """Get the canonical code of a labeled graph.
       
        Parameters
        ----------
        graph : networkx.graph
            A graph
        
        nodes: sequence
            An iterable with the nodes of the graphs as integer values.

        Returns
        -------
        can_label : str
            The minimum canonical label of the graph.

    """
    visited = []
    can_label = ""
    
    for node in nodes:
        can_label += str(graph.nodes[node]["feat_type"])
        for v in visited:
            can_label += str(graph[node][v]["distance"])
        visited.append(node)    

    return can_label

def minimum_canonical_code_naive(graph: Graph) -> str:
    """ Get the minimum canonical code of a graph by comparing all possible permutations
        of the graph nodes. This algorithm will always be correct, however the runtime is
        O(n!). It shouldn't be used for large graphs. 

        In practice pharmacophore graphs will rarely have more than 20 nodes and normally 
        will have between 5 and 10 nodes aproximately.
    """
    min_can_code = "z" # z is greater than all possible labels of the graph
    for nodes_perm in permutations(graph.nodes, graph.number_of_nodes()):
        can_code = canonical_code(graph, nodes_perm)
        if can_code < min_can_code:
            min_can_code = can_code
    
    return min_can_code

def minimum_canonical_code(graph : Graph, node_subset: Optional[Sequence] = None) -> str:
    """ Get the minimum canonical code of a graph.

        In case all nodes have different labels the minimum canonical code is just the code
        when the nodes are sorted in ascending order. If there are nodes with the same label
        we have to consider different permutations with these nodes; nevertheless, it's still
        less than the naive method.  
    
        Parameters
        ----------
        graph : networkx.graph
            A graph
        
        node_subset : Sequence, optional, default=None
            A subset of nodes of the graph, in case a canonical code of a subgraph is required.
            An iterable with the nodes of the graphs as integer values.

        Returns
        -------
        can_label : str
            The minimum canonical label of the graph.
    """
    # Sort the nodes by their labels
    nodes = [n[0] for n in sorted(dict(graph.nodes.data("feat_type")).items(), key=lambda item: item[1])]
    if node_subset:
       nodes = [n for n in nodes if n in node_subset] 
    
    # Find if there are repeated node labels and where are they
    repeated_nodes = defaultdict(set)
    for ii in range(len(nodes) - 1):
        if graph.nodes[nodes[ii]]["feat_type"] == graph.nodes[nodes[ii + 1]]["feat_type"]:
            node_label = graph.nodes[nodes[ii]]["feat_type"]
            repeated_nodes[node_label].add(nodes[ii])
            repeated_nodes[node_label].add(nodes[ii + 1])

    min_can_label = "z"
    can_label = ""
    if len(repeated_nodes) == 0:    
        min_can_label = canonical_code(graph, nodes)
    else:
        # If there are repeated labels we need to consider different permutations of the nodes
        # TODO: Can we find a more efficient way to eliminate more unecessary permutations?
        permuts = []
        for repeated in repeated_nodes.values():
            permuts.append(permutations(repeated, len(repeated)))

        for permut in product(*permuts):
            subpermut_index = 0
            full_permutation = []
            for node in nodes:
                if subpermut_index < len(permut):
                    if node in permut[subpermut_index]:
                        for n in permut[subpermut_index]:
                            full_permutation.append(n)
                        subpermut_index += 1
                
                if node not in full_permutation:
                    full_permutation.append(node)

            can_label = canonical_code(graph, full_permutation)
            if can_label < min_can_label:
                min_can_label = can_label

    return min_can_label







    
    

