from canonical_code import minimum_canonical_code, minimum_canonical_code_naive
import test_graphs

def test_no_repeated_labels():
    graphs = test_graphs.complete_graphs()
    G = graphs[0]
    H = graphs[1]
    J = graphs[2]

    canonical_code = minimum_canonical_code(G)
    canonical_code_naive = minimum_canonical_code_naive(G)
    assert canonical_code_naive == "AD4N38R524", f"G wrong canonical label: {canonical_code_naive}. Expected AD4N38R524"
    assert canonical_code == canonical_code_naive
  
    canonical_code = minimum_canonical_code(J)
    canonical_code_naive = minimum_canonical_code_naive(J)
    assert canonical_code_naive == "AD4P38R524", f"J wrong canonical label: {canonical_code_naive}. Expected AD4P38R524"
    assert canonical_code == canonical_code_naive

    canonical_code = minimum_canonical_code(H)
    canonical_code_naive = minimum_canonical_code_naive(H)
    assert canonical_code_naive == "AD4H45N385P3246R52847", f"H wrong canonical label: {canonical_code_naive}. Expected AD4H45N385P3246R52847"
    assert canonical_code == canonical_code_naive

def test_repeated_labels():

    k4 = test_graphs.k4_repeated_labels()
    k5 = test_graphs.k5_repeated_labels()
    k6 = test_graphs.k6_repeated_labels()

    canonical_code_naive = minimum_canonical_code_naive(k4)
    canonical_code = minimum_canonical_code(k4)
    assert canonical_code_naive == "AA3D48R542", f"Graph 1 wrong canonical label: {canonical_code_naive}. Expected AA3D48R524"
    assert canonical_code == canonical_code_naive

    canonical_code_naive = minimum_canonical_code_naive(k5)
    canonical_code = minimum_canonical_code(k5)
    assert canonical_code_naive == "AD6H28H545R7345", f"Graph 2 wrong canonical label: {canonical_code_naive}. Expected AD6H28H565R7345"
    assert canonical_code == canonical_code_naive

    canonical_code_naive = minimum_canonical_code_naive(k6)
    canonical_code = minimum_canonical_code(k6)
    assert canonical_code_naive == "AD2D55R273R6843R74983", f"Graph 3 wrong canonical label: {canonical_code_naive}. Expected AD2D55R273R6843R74983"
    assert canonical_code == canonical_code_naive

def test_single_label_graph():
    
    k3 = test_graphs.k3_single_label()
    
    canonical_code_naive = minimum_canonical_code_naive(k3)
    canonical_code = minimum_canonical_code(k3)
    assert canonical_code_naive == "AA2A34"
    assert canonical_code == canonical_code_naive

    k4 = test_graphs.k4_single_label()

    canonical_code_naive = minimum_canonical_code_naive(k4)
    canonical_code = minimum_canonical_code(k4)
    assert canonical_code_naive == "AA3A44A563"
    assert canonical_code == canonical_code_naive

test_no_repeated_labels()
test_single_label_graph()
test_repeated_labels()
print("All tests passed!!")
