from random_graph import random_graph
from canonical_code import minimum_canonical_code, minimum_canonical_code_naive
from timer import time_function

def time_canonical_code(graph_size: int) -> None:

    graph = random_graph(graph_size, graph_size)
    # Minimum canonical code naive function
    time = time_function(minimum_canonical_code_naive, args=(graph,), verbose=True)
    print(f"Avg time for naive canonical code algorithm is {time}"
          f" for a graph with {graph_size} nodes\n")
    # Minimum canonical code
    time = time_function(minimum_canonical_code, args=(graph,), verbose=True)
    print(f"Avg time for faster canonical code algorithm is {time}"
          f" for a graph with {graph_size} nodes")

def time_clique_detection() -> None:
    pass

def main():
    
    time_canonical_code(10)


if __name__=="__main__":
    main()