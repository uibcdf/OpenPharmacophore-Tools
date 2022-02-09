import clique_detection
import test_graphs
import networkx as nx

graphs = test_graphs.complete_graphs()

def k5_repeated_labels() -> nx.Graph:
    """ Returns a complete graph with five nodes and repeated node labels"""
    k5 = nx.Graph()
    k5.name = "Graph 2"
    nodes = [(1, "A"),(2, "A"),(3, "D"),(4, "R"), (5, "H")]
    edges = [(1, 2, 3),(1, 3, 4),(1, 4, 5),(1, 5, 6),
             (2, 3, 8),(2, 4, 4),(2, 5, 7),(3, 4, 2),
             (3, 5, 9),(4, 5, 7)]
    for node in nodes:
        k5.add_node(node[0], feat_type=node[1])
    for edge in edges:
        k5.add_edge(edge[0], edge[1], distance=edge[2])     
    assert k5.number_of_edges() == (k5.number_of_nodes() * (k5.number_of_nodes() - 1)) / 2 # Condition for complete graphs
    return k5

def k6_repeated_labels() -> nx.Graph:
    """ Returns a complete graph with six nodes and repeated node labels"""
    k6 = nx.Graph()
    k6.name = "Graph 3"
    nodes = [(1, "A"),(2, "A"),(3, "D"),(4, "R"), (5, "H"),(6, "R")]
    edges = [(1, 2, 3),(1, 3, 4),(1, 4, 5),(1, 5, 6),(1, 6, 9),
             (2, 3, 8),(2, 4, 4),(2, 5, 7),(2, 6, 6),(3, 4, 2),
             (3, 5, 9),(3, 6, 8),(4, 5, 7),(4, 6, 4),(5, 6, 7)]
    for node in nodes:
        k6.add_node(node[0], feat_type=node[1])
    for edge in edges:
        k6.add_edge(edge[0], edge[1], distance=edge[2])     
    assert k6.number_of_edges() == (k6.number_of_nodes() * (k6.number_of_nodes() - 1)) / 2 # Condition for complete graphs
    return k6


def test_find_freq_2_cliques():
    
    expected_result = ["AD4", "AR5", "DR2"]
    cliques = clique_detection.find_freq_2_cliques(graphs)
    assert len(cliques) == 3
    for c in cliques:
        assert c in expected_result
    
    k4 = test_graphs.k4_repeated_labels()
    k5 = k5_repeated_labels()
    k6 = k6_repeated_labels()

    expected_result = ["AA3", "AD4", "AD8", "AR5", "DR2", "AR4"]
    cliques = clique_detection.find_freq_2_cliques([k4, k5, k6])
    assert len(cliques) == 6
    for c in cliques:
        assert c in expected_result
    
    k3 = test_graphs.k3_single_label()
    k4 = test_graphs.k4_single_label()

    expected_result = ["AA3", "AA4"]
    cliques = clique_detection.find_freq_2_cliques([k3, k4])
    assert len(cliques) == 2
    for c in cliques:
        assert c in expected_result

def test_grow_clique():
    
    cliques_2 = ["AD4", "AR5", "DR2"]
    cliques_3 = clique_detection.grow_clique(graphs, cliques_2, 2, min_frequency=1)
    expected_result = ["AD4R25"]
    assert len(cliques_3) == 1
    assert cliques_3 == expected_result

    cliques_2 = ["AD4", "AR5", "DR2"]
    cliques_3 = clique_detection.grow_clique(graphs, cliques_2, 2, min_frequency=0.75)
    expected_result = ["AD4R25", "AD4N38"]
    assert len(cliques_3) == 2
    for c in cliques_3:
        assert c in expected_result

    k4 = test_graphs.k4_repeated_labels()
    k5 = k5_repeated_labels()
    k6 = k6_repeated_labels()

def test_clique_detection_naive():
    
    cliques = clique_detection.clique_detection_naive(graphs)
    print(cliques)

# test_find_freq_2_cliques()
test_clique_detection_naive()