from functools import reduce

import numpy as np
from scipy.cluster.hierarchy import (
    ClusterNode,
    leaves_list,
    linkage,
    to_tree,
)
from tqdm import tqdm


def cluster(M: np.ndarray, method="ward"):
    Z_row, Z_col = (
        linkage(M, method=method),
        linkage(M.T, method=method),
    )
    col_indecies, row_indecies = leaves_list(Z_row), leaves_list(Z_col)
    return M[row_indecies, :][:, col_indecies], (Z_row, Z_col)


def collect_leaves(node):
    if node.is_leaf():
        return [node.id]
    else:
        return collect_leaves(node.left) + collect_leaves(node.right)


def find_lowest_common_ancestor(Z: np.ndarray, target_leaves: np.ndarray):
    tree: ClusterNode
    nodelist: list[ClusterNode]
    tree, nodelist = to_tree(Z, rd=True)  # type: ignore

    paths = {}

    def traverse(node, path):
        if node.is_leaf():
            paths[node.id] = path
        else:
            traverse(node.left, path + [node.id])
            traverse(node.right, path + [node.id])

    traverse(tree, [])

    leaf_paths = [paths[leaf] for leaf in target_leaves]

    shortest_common_path = reduce(lambda x, y: [a for a, b in zip(x, y) if a == b], leaf_paths)

    lca_id = shortest_common_path[-1]
    lca = next((node for node in nodelist if node.id == lca_id), None)

    if lca is None:
        raise ValueError("No lowest common ancestor found")

    return lca, paths, np.array(collect_leaves(lca), dtype=np.int32)


def filter_redundant_factors(corr_matrix: np.ndarray, threshold: float) -> tuple[np.ndarray, np.ndarray]:
    n = corr_matrix.shape[0]
    mask = np.ones(n, dtype=bool)
    np.fill_diagonal(corr_matrix, 0)

    for i in tqdm(range(n), desc="Filtering redundant factors"):
        if mask[i]:
            mask = (corr_matrix[i] < threshold) & mask

    return corr_matrix[mask][:, mask], mask
