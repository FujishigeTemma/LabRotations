import numpy as np
import pytest
from edmkit.graph import chu_liu_edmonds


def test_chu_liu_edmonds_simple():
    """
    Test the chu_liu_edmonds function with a simple graph.
    """
    # Simple graph with 3 nodes
    # 0 -> 1 with weight 2
    # 0 -> 2 with weight 3
    # 1 -> 2 with weight 1
    A = np.array([[0, 2, 3], [0, 0, 1], [0, 0, 0]])

    # Root is node 0
    root = 0

    # Expected result: 0 -> 1 -> 2
    expected = np.array([[0, 2, 0], [0, 0, 1], [0, 0, 0]])

    result = chu_liu_edmonds(A, root)
    np.testing.assert_array_equal(result, expected)


def test_chu_liu_edmonds_with_cycle():
    """
    Test the chu_liu_edmonds function with a graph containing a cycle.
    """
    # Graph with 4 nodes and a cycle
    # 0 -> 1 with weight 2
    # 0 -> 2 with weight 3
    # 1 -> 2 with weight 1
    # 2 -> 1 with weight 1
    # 1 -> 3 with weight 4
    # 2 -> 3 with weight 2
    A = np.array([[0, 2, 3, 0], [0, 0, 1, 4], [0, 1, 0, 2], [0, 0, 0, 0]])

    # Root is node 0
    root = 0

    # Expected result: 0 -> 1, 1 -> 2, 2 -> 3
    # The cycle between 1 and 2 is broken by choosing the minimum incoming edge
    expected = np.array([[0, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 2], [0, 0, 0, 0]])

    result = chu_liu_edmonds(A, root)
    np.testing.assert_array_equal(result, expected)


def test_chu_liu_edmonds_complete_graph():
    """
    Test the chu_liu_edmonds function with a complete graph.
    """
    # Complete graph with 4 nodes
    A = np.array([[0, 4, 3, 5], [2, 0, 5, 1], [3, 2, 0, 4], [1, 3, 2, 0]])

    # Root is node 0
    root = 0

    # Expected result: 0 -> 2, 2 -> 1, 1 -> 3
    expected = np.array([[0, 0, 3, 0], [0, 0, 0, 1], [0, 2, 0, 0], [0, 0, 0, 0]])

    result = chu_liu_edmonds(A, root)
    np.testing.assert_array_equal(result, expected)


def test_chu_liu_edmonds_disconnected():
    """
    Test the chu_liu_edmonds function with a disconnected graph.
    This should raise an error since all vertices must be reachable from the root.
    """
    # Disconnected graph
    A = np.array([[0, 1, 0], [0, 0, 0], [0, 1, 0]])

    # Root is node 0
    root = 0

    # Node 2 is not reachable from the root
    with pytest.raises(ValueError, match="Not all vertices are reachable from the root"):
        chu_liu_edmonds(A, root)


def test_chu_liu_edmonds_invalid_input():
    """
    Test the chu_liu_edmonds function with invalid inputs.
    """
    # Non-square matrix
    A = np.array([[0, 1, 2], [3, 4, 5]])

    with pytest.raises(AssertionError, match="A must be square"):
        chu_liu_edmonds(A, 0)

    # 3D matrix
    A = np.ones((3, 3, 3))

    with pytest.raises(AssertionError, match="A must be 2-dimensional"):
        chu_liu_edmonds(A, 0)

    # Invalid root
    A = np.array([[0, 1, 2], [3, 0, 5], [6, 7, 0]])

    with pytest.raises(AssertionError, match="root must be in the range of the number of nodes"):
        chu_liu_edmonds(A, 3)


def calculate_msa_weight_sum(msa: np.ndarray) -> int:
    """
    Calculate the sum of weights in a minimum spanning arborescence.

    Parameters
    ----------
    msa : np.ndarray
        The adjacency matrix of the minimum spanning arborescence.

    Returns
    -------
    int
        The sum of weights in the minimum spanning arborescence.
    """
    return int(np.sum(msa))


def test_chu_liu_edmonds_weight_sum_example1():
    """
    Test the chu_liu_edmonds function with the first example from the problem.

    Input:
    4 6 0
    0 1 3
    0 2 2
    2 0 1
    2 3 1
    3 0 1
    3 1 5

    Expected output: 6
    """
    # Create the adjacency matrix from the input
    V, E, root = 4, 6, 0
    A = np.zeros((V, V))

    # Add edges
    edges = [(0, 1, 3), (0, 2, 2), (2, 0, 1), (2, 3, 1), (3, 0, 1), (3, 1, 5)]

    for s, t, w in edges:
        A[s, t] = w

    # Find the minimum spanning arborescence
    msa = chu_liu_edmonds(A, root)

    # Calculate the sum of weights
    weight_sum = calculate_msa_weight_sum(msa)

    # Expected weight sum is 6
    assert weight_sum == 6, f"Expected weight sum 6, got {weight_sum}"


def test_chu_liu_edmonds_weight_sum_example2():
    """
    Test the chu_liu_edmonds function with the second example from the problem.

    Input:
    6 10 0
    0 2 7
    0 1 1
    0 3 5
    1 4 9
    2 1 6
    1 3 2
    3 4 3
    4 2 2
    2 5 8
    3 5 3

    Expected output: 11
    """
    # Create the adjacency matrix from the input
    V, E, root = 6, 10, 0
    A = np.zeros((V, V))

    # Add edges
    edges = [(0, 2, 7), (0, 1, 1), (0, 3, 5), (1, 4, 9), (2, 1, 6), (1, 3, 2), (3, 4, 3), (4, 2, 2), (2, 5, 8), (3, 5, 3)]

    for s, t, w in edges:
        A[s, t] = w

    # Find the minimum spanning arborescence
    msa = chu_liu_edmonds(A, root)

    # Calculate the sum of weights
    weight_sum = calculate_msa_weight_sum(msa)

    # Expected weight sum is 11
    assert weight_sum == 11, f"Expected weight sum 11, got {weight_sum}"


def test_chu_liu_edmonds_maximum():
    """
    Test the chu_liu_edmonds function with maximize=True to find the maximum spanning arborescence.
    """
    # Simple graph with 3 nodes
    # 0 -> 1 with weight 2
    # 0 -> 2 with weight 3
    # 1 -> 2 with weight 1
    A = np.array([[0, 2, 3], [0, 0, 1], [0, 0, 0]])

    # Root is node 0
    root = 0

    # Expected result for maximum: 0 -> 2, 0 -> 1
    # (Choose the maximum weight edges from the root)
    expected_max = np.array([[0, 2, 3], [0, 0, 0], [0, 0, 0]])

    result_max = chu_liu_edmonds(A, root, maximize=True)
    np.testing.assert_array_equal(result_max, expected_max)

    # Verify that the default (minimize=False) still works
    expected_min = np.array([[0, 2, 0], [0, 0, 1], [0, 0, 0]])
    result_min = chu_liu_edmonds(A, root, maximize=False)
    np.testing.assert_array_equal(result_min, expected_min)


def test_chu_liu_edmonds_maximum_with_cycle():
    """
    Test the chu_liu_edmonds function with maximize=True on a graph with a cycle.
    """
    # Graph with 4 nodes and a cycle
    # 0 -> 1 with weight 2
    # 0 -> 2 with weight 3
    # 1 -> 2 with weight 1
    # 2 -> 1 with weight 1
    # 1 -> 3 with weight 4
    # 2 -> 3 with weight 2
    A = np.array([[0, 2, 3, 0], [0, 0, 1, 4], [0, 1, 0, 2], [0, 0, 0, 0]])

    # Root is node 0
    root = 0

    # Get the actual result
    result_max = chu_liu_edmonds(A, root, maximize=True)

    # The expected result should be the maximum spanning arborescence
    # The algorithm chooses: 0 -> 1, 0 -> 2, 1 -> 3
    expected_max = np.array([[0, 2, 3, 0], [0, 0, 0, 4], [0, 0, 0, 0], [0, 0, 0, 0]])

    np.testing.assert_array_equal(result_max, expected_max)

    # Verify the weight sum is 9 (2 + 3 + 4)
    weight_sum = calculate_msa_weight_sum(result_max)
    assert weight_sum == 9, f"Expected weight sum 9, got {weight_sum}"


def test_chu_liu_edmonds_maximum_weight_sum():
    """
    Test the weight sum of the maximum spanning arborescence.
    """
    # Create a graph where the maximum and minimum spanning arborescences are different
    V, root = 5, 0
    A = np.zeros((V, V))

    # Add edges with varying weights
    edges = [(0, 1, 10), (0, 2, 5), (1, 3, 8), (2, 3, 3), (2, 4, 7), (3, 4, 2)]

    for s, t, w in edges:
        A[s, t] = w

    # Find the maximum spanning arborescence
    max_msa = chu_liu_edmonds(A, root, maximize=True)
    max_weight_sum = calculate_msa_weight_sum(max_msa)

    # Find the minimum spanning arborescence
    min_msa = chu_liu_edmonds(A, root, maximize=False)
    min_weight_sum = calculate_msa_weight_sum(min_msa)

    # The maximum weight sum should be greater than the minimum weight sum
    assert max_weight_sum > min_weight_sum, f"Expected max_weight_sum > min_weight_sum, got {max_weight_sum} <= {min_weight_sum}"

    # Verify the expected weight sums
    # For this graph, the maximum spanning arborescence has a weight sum of 30
    # The minimum spanning arborescence has a weight sum of 20
    assert max_weight_sum == 30, f"Expected maximum weight sum 30, got {max_weight_sum}"
    assert min_weight_sum == 20, f"Expected minimum weight sum 20, got {min_weight_sum}"

    # Print the arborescences for debugging
    print("Maximum spanning arborescence:")
    print(max_msa)
    print("Minimum spanning arborescence:")
    print(min_msa)
