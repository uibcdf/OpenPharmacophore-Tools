from collections import defaultdict
from itertools import permutations, product

def minimum_canonical_code(graph : object) -> str:
    """ Get the minimum canonical code of a graph.
    
        Parameters
        ----------
        graph : networkx.graph
            A graph
        
        Returns
        -------
        can_label : str
            The minimum canonical label of the graph.
    """
    # Sort the nodes by their labels
    nodes = [n[0] for n in sorted(dict(graph.nodes.data("feat_type")).items(), key=lambda item: item[1])]
    # Find if there are repeated node labels and where are they
    repeated_nodes = defaultdict(set)
    for ii in range(len(nodes) - 1):
        if graph.nodes[nodes[ii]]["feat_type"] == graph.nodes[nodes[ii + 1]]["feat_type"]:
            node_label = graph.nodes[nodes[ii]]["feat_type"]
            repeated_nodes[node_label].add(nodes[ii])
            repeated_nodes[node_label].add(nodes[ii + 1])

    min_can_label = "ZZZ"
    can_label = ""
    if len(repeated_nodes) == 0:    
        min_can_label = canonical_code(graph, nodes)
    else:
        # If there are repeated labels we need to consider different permutations of the nodes
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


def canonical_code(graph : object, nodes : tuple) -> str:
    """Get the canonical code of a labeled graph.
       
        Parameters
        ----------
        graph : networkx.graph
            A graph
        
        nodes: iterable
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

    assert len(can_label) == graph.number_of_nodes() + graph.number_of_edges()
    return can_label


def canonical_code_single_label(graph : object) -> str:
    """Get the minimum canonical code for a graph whose labels are all equal.
    """
    if graph.number_of_edges() == 0:
        raise ValueError("Graph has no edges")

    n_nodes = graph.number_of_nodes()
    
    # Create a dictionary with edges grouped by their distance
    # Also a sorted list with the distances in ascending order
    edges_dict = defaultdict(list)
    min_distance = 1000
    for edge in graph.edges.data("distance"):
        if edge[2] < min_distance:
            min_distance = edge[2]
        edges_dict[edge[2]].append((edge[0], edge[1]))
    
    # This is the case with a graph whose all node labels are equal and its edge labels are
    # also equal. In this case the canonical label should be unique.
    if len(edges_dict) == 1:
        return canonical_code(graph.nodes)

    start_nodes = []
    for edge in edges_dict[min_distance]:
        start_nodes.append(edge)
        start_nodes.append((edge[-1], edge[0])) # Put the edge in reverse order 
    
    min_can_code = "ZZZZZ"
    for nodes_perm in permutations(graph.nodes, n_nodes):
        first_nodes = nodes_perm[0], nodes_perm[1]
        if first_nodes in start_nodes:
            can_code = canonical_code(graph, nodes_perm)
            if can_code < min_can_code:
                min_can_code = can_code
        else:
            continue
    
    return min_can_code







    
    

