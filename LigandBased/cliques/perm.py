from itertools import permutations, product

nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

repeated_nodes = {
    "repeated_1": [2, 3],
    "repeated_2": [4, 5, 6],
    "repeated_3": [9, 10]
}

permuts = []
for repeated in repeated_nodes.values():
    permuts.append(permutations(repeated, len(repeated)))

node_permutations = []
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

    print(full_permutation)


