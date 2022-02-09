from canonical_code import minimum_canonical_code, minimum_canonical_code_naive
from random_graph import random_graph, print_graph

def stress_test_canonical_code() -> None:

    while True:
        try:
            graph = random_graph(2, 10)
            if minimum_canonical_code_naive(graph) != minimum_canonical_code(graph):
                print(f"Found an error with the following graph:")
                print_graph(graph)
                print(f"\nCanonical code from naive algorithm {minimum_canonical_code_naive(graph)}")
                print(f"Canonical code faster algorithm {minimum_canonical_code(graph)}")
                break
        except KeyboardInterrupt:
            print("\nExiting....")
            break


def stress_test_clique_detection() -> None:
    pass

def main():

    stress_test_canonical_code()
    stress_test_clique_detection()

if __name__=="__main__":
    main()