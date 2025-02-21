import numpy as np

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


def chu_liu_edmonds(A: np.ndarray, root: int) -> np.ndarray:
    """
    Find the minimum spanning arborescence of a directed graph using the Chu-Liu/Edmonds algorithm.
    Assumes all vertices are reachable from the root vertex.

    Parameters
    ----------
    `A` : `np.ndarray`
        The adjacency matrix of the directed graph.
    `root` : `int`
        The root vertex of the arborescence.

    Returns
    -------
    `np.ndarray`
        The adjacency matrix of the minimum spanning arborescence.

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

    n = A.shape[0]
