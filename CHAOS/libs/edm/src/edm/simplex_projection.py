import platform

# workaround
if platform.system() == "Darwin":
    import os

    os.environ["METAL_XCODE"] = "1"
    os.environ["DISABLE_COMPILER_CACHE"] = "1"

    print("Running on macOS, setting METAL_XCODE=1 and DISABLE_COMPILER_CACHE=1")

import numpy as np
from tinygrad import Tensor
from tinygrad.dtype import dtypes


def pad(Xs: list[np.ndarray]):
    """
    Parameters:
        `Xs`: list of np.ndarray of shape (L, D_i)

    Returns:
        single np.ndarray of shape (B, L, max(D)) where B is the number of tensors in `Xs`.
    """
    B = len(Xs)
    L = Xs[0].shape[0]
    max_D = max(t.shape[-1] for t in Xs)  # type: ignore

    X = np.zeros((B, L, max_D), dtype=Xs[0].dtype)
    for i, t in enumerate(Xs):
        X[i, :, : t.shape[-1]] = t

    return np.ascontiguousarray(X)


def pairwise_distance(A: Tensor):
    """
    Parameters:
        `A`: Tensor of shape (L, D) or (B, L, D)
            B: batch size
            L: number of points
            D: dimension of each point

    Returns:
        When `A` is of shape (L, D):
            Tensor of shape (L, L) where the element at position (i, j) is the squared Euclidean distance between A[i] and A[j].
        When `A` is of shape (B, L, D):
            Tensor of shape (B, L, L) where the element at position (b, i, j) is the squared Euclidean distance between A[b, i] and A[b, j].
    """

    return (A.unsqueeze(A.ndim - 1) - A.unsqueeze(A.ndim - 2)).pow(2).sum(-1)


def topk(x: np.ndarray, k: int, largest=True):
    """
    Parameters:
        `x`: np.ndarray of shape (N,)
        `k`: int
        `largest`: bool

    Returns:
        `indices`: np.ndarray of shape (`k`,)
        `values`: np.ndarray of shape (`k`,)

    Note:
        `values` are sorted in ascending order. (i.e. `values[0]` is the smallest value in `values`)
    """
    assert x.ndim == 1, "x must be a 1D array"
    assert k > 0 and k <= len(x), "k must satisfy 0 < k <= len(x)"

    if largest:
        indices = np.argpartition(-x, k)[:k]
    else:
        indices = np.argpartition(x, k)[:k]

    argsort = np.argsort(x[indices])

    indices = indices[argsort]
    values = x[indices]

    return indices, values


def simplex_projection(
    X: np.ndarray,
    Y: np.ndarray,
    t: np.ndarray,
    Tp: int,
    partition: int | None = None,
    exclusion_radius: int | None = None,
):
    assert X.shape[0] == Y.shape[0], "X and Y must have the same length"
    assert (t < X.shape[0] - Tp).all(), "t+Tp must be less than the length of X,Y"

    D = pairwise_distance(Tensor(X, dtype=dtypes.float32)).numpy()

    N = D.shape[0]
    seq = np.arange(N)

    k: int = X.shape[1] + 1
    neighbors = []
    # TODO: parallelize
    for i in t:
        mask = np.ones(N, dtype=bool)
        # exclude self
        mask[i] = False
        # exclude last Tp points to prevent out-of-bound indexing
        mask[max(0, len(D[i]) - Tp) :] = False
        # split into lib and test
        if partition is not None:
            assert partition < N, "partition must be less than the number of points"
            assert (
                t >= partition
            ).all(), "t must be greater than or equal to partition when partition is specified"
            mask[partition:] = False
        # exclude neighbors within exclusion_radius
        if exclusion_radius is not None:
            mask[max(0, i - exclusion_radius) : min(N, i + exclusion_radius + 1)] = (
                False
            )

        # find k nearest neighbors
        indices_masked, _ = topk(D[i][mask], k, largest=False)
        indices = seq[mask][indices_masked]
        neighbors.append(indices)

    observations = Y[t + Tp]
    # TODO: parallelize
    predictions = np.array([Y[indices + Tp].mean() for indices in neighbors])

    return observations, predictions
