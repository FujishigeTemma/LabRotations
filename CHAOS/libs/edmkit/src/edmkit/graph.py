from collections import deque

import numpy as np

from edmkit.heap import FibonacciHeap

# @article{
#    year={1986},
#    issn={0209-9683},
#    journal={Combinatorica},
#    volume={6},
#    number={2},
#    doi={10.1007/BF02579168},
#    title={Efficient algorithms for finding minimum spanning trees in
#        undirected and directed graphs},
#    url={https://doi.org/10.1007/BF02579168},
#    publisher={Springer-Verlag},
#    keywords={68 B 15; 68 C 05},
#    author={Gabow, Harold N. and Galil, Zvi and Spencer, Thomas and Tarjan,
#        Robert E.},
#    pages={109-122},
#    language={English}
# }


def chu_liu_edmonds(A: np.ndarray, root: int, maximize: bool = False) -> np.ndarray:
    """
    Find the optimal spanning arborescence of a directed graph using the Chu-Liu/Edmonds algorithm.
    By default, finds the minimum spanning arborescence. If maximize=True, finds the maximum spanning arborescence.
    Assumes all vertices are reachable from the root vertex.

    Parameters
    ----------
    `A` : `np.ndarray`
        The adjacency matrix of the directed graph.
    `root` : `int`
        The root vertex of the arborescence.
    `maximize` : `bool`, optional
        If True, find the maximum spanning arborescence. If False (default), find the minimum spanning arborescence.

    Returns
    -------
    `np.ndarray`
        The adjacency matrix of the optimal spanning arborescence.

    Raises
    ------
    AssertionError
        - If the input matrix `A` is not square.
        - If the input matrix `A` is not 2-dimensional.
        - If the root vertex is not in the range of the number of nodes.
    """
    assert A.shape[0] == A.shape[1], "A must be square"
    assert len(A.shape) == 2, "A must be 2-dimensional"
    assert 0 <= root < A.shape[0], "root must be in the range of the number of nodes"

    return _chu_liu_edmonds_recursive(A, root, maximize, is_contracted_graph=False)


def _chu_liu_edmonds_recursive(A: np.ndarray, root: int, maximize: bool, is_contracted_graph: bool) -> np.ndarray:
    """
    Internal recursive function for the Chu-Liu/Edmonds algorithm.

    Parameters
    ----------
    A : np.ndarray
        The adjacency matrix of the directed graph.
    root : int
        The root vertex of the arborescence.
    maximize : bool
        If True, find the maximum spanning arborescence. If False, find the minimum spanning arborescence.
    is_contracted_graph : bool
        Whether the graph is a contracted graph.

    Returns
    -------
    np.ndarray
        The adjacency matrix of the optimal spanning arborescence.
    """
    n = A.shape[0]

    # If there's only one node, return an empty adjacency matrix
    if n == 1:
        return np.zeros((1, 1))

    # Check if all vertices are reachable from the root
    # Only check for the original graph, not for contracted graphs
    if not is_contracted_graph and not _is_reachable_from_root(A, root, n):
        raise ValueError("Not all vertices are reachable from the root")

    # Find the optimal incoming edge for each vertex (except the root)
    optimal_edges = _find_optimal_incoming_edges(A, root, maximize)

    # Create a graph with the optimal incoming edges
    B = np.zeros_like(A)
    for v, (u, weight) in optimal_edges.items():
        B[u, v] = weight

    # Check if the resulting graph has cycles
    cycles = _find_cycles(B, root)

    if not cycles:
        # No cycles, we're done
        return B

    # Contract each cycle into a single vertex
    contracted_graph, cycle_nodes, cycle_repr = _contract_cycles(A, cycles, root, maximize)

    # Recursively find the optimal spanning arborescence of the contracted graph
    contracted_msa = _chu_liu_edmonds_recursive(contracted_graph, root, maximize, is_contracted_graph=True)

    # Expand the contracted vertices back to the original graph
    return _expand_cycles(contracted_msa, A, cycle_nodes, cycle_repr, optimal_edges, maximize)


def _is_reachable_from_root(A: np.ndarray, root: int, n: int = None) -> bool:
    """
    Check if all vertices are reachable from the root using BFS.

    Parameters
    ----------
    A : np.ndarray
        The adjacency matrix of the directed graph.
    root : int
        The root vertex.
    n : int, optional
        The number of vertices to check. If None, all vertices are checked.

    Returns
    -------
    bool
        True if all vertices are reachable from the root, False otherwise.
    """
    n = n if n is not None else A.shape[0]
    visited = [False] * n
    queue = deque([root])
    visited[root] = True

    while queue:
        u = queue.popleft()
        for v in range(n):
            if A[u, v] > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)

    return all(visited)


def _find_optimal_incoming_edges(A: np.ndarray, root: int, maximize: bool):
    """
    Find the optimal incoming edge for each vertex (except the root).
    If maximize is True, find the maximum incoming edge. Otherwise, find the minimum incoming edge.

    Parameters
    ----------
    A : np.ndarray
        The adjacency matrix of the directed graph.
    root : int
        The root vertex.
    maximize : bool
        If True, find the maximum incoming edge. If False, find the minimum incoming edge.

    Returns
    -------
    dict
        A dictionary mapping each vertex to its optimal incoming edge (u, weight).
    """
    n = A.shape[0]
    optimal_edges: dict[int, tuple[int, float]] = {}

    for v in range(n):
        if v == root:
            continue

        # Use a Fibonacci heap to find the optimal incoming edge
        heap = FibonacciHeap()

        for u in range(n):
            if A[u, v] > 0:  # There's an edge from u to v
                # If maximizing, negate the weight to find the maximum
                key = -A[u, v] if maximize else A[u, v]
                heap.insert(key, u)

        min_node = heap.pop()
        if min_node is not None:
            # If maximizing, negate the key back to get the original weight
            weight = -min_node.key if maximize else min_node.key
            optimal_edges[v] = (min_node.value, weight)  # (u, weight)

    return optimal_edges


def _find_cycles(B: np.ndarray, root: int) -> list:
    """
    Find cycles in the graph using DFS.

    Parameters
    ----------
    B : np.ndarray
        The adjacency matrix of the directed graph.
    root : int
        The root vertex.

    Returns
    -------
    list
        A list of cycles, where each cycle is a list of vertices.
    """
    n = B.shape[0]
    visited = [False] * n
    rec_stack = [False] * n
    cycles = []

    def dfs(u, path):
        visited[u] = True
        rec_stack[u] = True
        path.append(u)

        for v in range(n):
            if B[u, v] > 0:
                if not visited[v]:
                    if dfs(v, path):
                        return True
                elif rec_stack[v]:
                    # Found a cycle
                    cycle_start = path.index(v)
                    cycles.append(path[cycle_start:])
                    return True

        path.pop()
        rec_stack[u] = False
        return False

    for i in range(n):
        if i != root and not visited[i]:
            dfs(i, [])

    return cycles


def _contract_cycles(A: np.ndarray, cycles: list, root: int, maximize: bool) -> tuple:
    """
    Contract each cycle into a single vertex.

    Parameters
    ----------
    A : np.ndarray
        The adjacency matrix of the directed graph.
    cycles : list
        A list of cycles, where each cycle is a list of vertices.
    root : int
        The root vertex.
    maximize : bool
        If True, find the maximum spanning arborescence. If False, find the minimum spanning arborescence.

    Returns
    -------
    tuple
        A tuple containing the contracted graph, a dictionary mapping each contracted vertex
        to its original vertices, and a dictionary mapping each original vertex to its
        contracted vertex.
    """
    n = A.shape[0]

    # Map each vertex to its cycle representative
    cycle_repr = {}  # original vertex -> contracted vertex
    cycle_nodes = {}  # contracted vertex -> list of original vertices

    # Assign a new index to each cycle
    next_index = n
    for cycle in cycles:
        cycle_id = next_index
        next_index += 1
        cycle_nodes[cycle_id] = cycle

        for v in cycle:
            cycle_repr[v] = cycle_id

    # Create the contracted graph
    contracted_size = n + len(cycles)
    contracted_graph = np.zeros((contracted_size, contracted_size))

    # Copy edges that are not part of cycles
    for u in range(n):
        if u in cycle_repr:
            continue  # Skip vertices that are part of cycles

        for v in range(n):
            if v in cycle_repr:
                # Edge to a vertex in a cycle
                cycle_id = cycle_repr[v]
                if A[u, v] > 0:
                    if contracted_graph[u, cycle_id] == 0:
                        contracted_graph[u, cycle_id] = A[u, v]
                    elif (maximize and A[u, v] > contracted_graph[u, cycle_id]) or (not maximize and A[u, v] < contracted_graph[u, cycle_id]):
                        contracted_graph[u, cycle_id] = A[u, v]
            elif A[u, v] > 0:
                # Regular edge
                contracted_graph[u, v] = A[u, v]

    # Handle edges from cycles to other vertices
    for cycle_id, cycle in cycle_nodes.items():
        for u in cycle:
            for v in range(n):
                if v in cycle:
                    continue  # Skip edges within the same cycle

                if v in cycle_repr:
                    # Edge to a vertex in another cycle
                    other_cycle_id = cycle_repr[v]
                    if cycle_id != other_cycle_id and A[u, v] > 0:
                        if contracted_graph[cycle_id, other_cycle_id] == 0:
                            contracted_graph[cycle_id, other_cycle_id] = A[u, v]
                        elif (maximize and A[u, v] > contracted_graph[cycle_id, other_cycle_id]) or (
                            not maximize and A[u, v] < contracted_graph[cycle_id, other_cycle_id]
                        ):
                            contracted_graph[cycle_id, other_cycle_id] = A[u, v]
                elif A[u, v] > 0:
                    # Edge to a regular vertex
                    if contracted_graph[cycle_id, v] == 0:
                        contracted_graph[cycle_id, v] = A[u, v]
                    elif (maximize and A[u, v] > contracted_graph[cycle_id, v]) or (not maximize and A[u, v] < contracted_graph[cycle_id, v]):
                        contracted_graph[cycle_id, v] = A[u, v]

    # Ensure all contracted vertices are reachable from the root
    # Add a direct edge from the root to each contracted vertex if needed
    for cycle_id in cycle_nodes:
        # Add a direct edge from the root to the cycle
        # Use a very high/low weight so it won't be chosen unless necessary
        if not any(contracted_graph[u, cycle_id] > 0 for u in range(n) if u != cycle_id and u < n):
            contracted_graph[root, cycle_id] = float("-inf") if maximize else float("inf")

    return contracted_graph, cycle_nodes, cycle_repr


def _expand_cycles(contracted_msa: np.ndarray, A: np.ndarray, cycle_nodes: dict, cycle_repr: dict, optimal_edges: dict, maximize: bool) -> np.ndarray:
    """
    Expand the contracted vertices back to the original graph.

    Parameters
    ----------
    contracted_msa : np.ndarray
        The adjacency matrix of the optimal spanning arborescence of the contracted graph.
    A : np.ndarray
        The original adjacency matrix.
    cycle_nodes : dict
        A dictionary mapping each contracted vertex to its original vertices.
    cycle_repr : dict
        A dictionary mapping each original vertex to its contracted vertex.
    optimal_edges : dict
        A dictionary mapping each vertex to its optimal incoming edge.
    maximize : bool
        If True, find the maximum spanning arborescence. If False, find the minimum spanning arborescence.

    Returns
    -------
    np.ndarray
        The adjacency matrix of the optimal spanning arborescence of the original graph.
    """
    n = A.shape[0]
    msa = np.zeros((n, n))

    # Copy edges that are not part of cycles
    for u in range(n):
        if u in cycle_repr:
            continue  # Skip vertices that are part of cycles

        for v in range(n):
            if v in cycle_repr:
                continue  # Skip edges to vertices in cycles

            if contracted_msa[u, v] > 0:
                msa[u, v] = contracted_msa[u, v]

    # Handle edges to and within cycles
    for cycle_id, cycle in cycle_nodes.items():
        # Find the incoming edge to the cycle
        incoming_edge = None
        incoming_weight = float("-inf") if maximize else float("inf")
        incoming_target = None

        for v in cycle:
            for u in range(n):
                if u not in cycle and u < n and contracted_msa[u, cycle_id] > 0 and A[u, v] > 0:
                    if (maximize and A[u, v] > incoming_weight) or (not maximize and A[u, v] < incoming_weight):
                        incoming_edge = (u, v)
                        incoming_weight = A[u, v]
                        incoming_target = v

        if incoming_edge:
            u, v = incoming_edge
            msa[u, v] = A[u, v]

            # Add all edges in the cycle except the one entering the incoming_target
            for i in range(len(cycle)):
                u = cycle[i]
                v = cycle[(i + 1) % len(cycle)]
                if v != incoming_target:
                    msa[u, v] = A[u, v]

        # Handle outgoing edges from the cycle
        for u in cycle:
            for v in range(n):
                if v not in cycle and v < n and contracted_msa[cycle_id, v] > 0 and A[u, v] > 0:
                    # Find the optimal weight edge from the cycle to v
                    if all(msa[w, v] == 0 for w in cycle):
                        optimal_weight = float("-inf") if maximize else float("inf")
                        optimal_edge = None
                        for w in cycle:
                            if A[w, v] > 0:
                                if (maximize and A[w, v] > optimal_weight) or (not maximize and A[w, v] < optimal_weight):
                                    optimal_weight = A[w, v]
                                    optimal_edge = (w, v)
                        if optimal_edge:
                            w, v = optimal_edge
                            msa[w, v] = A[w, v]

    return msa
