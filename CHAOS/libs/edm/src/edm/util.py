import numpy as np

from edm.tensor import Tensor


def pad(Xs: list[np.ndarray]):
    """Pad the `np.ndarray` in `Xs` to merge them into a single `np.ndarray`.

    Parameters
    ----------
        `Xs` : `list` of `np.ndarray` of shape `(L, D_i)`

    Returns
    -------
        single `np.ndarray` of shape `(B, L, max(D))` where `B` is the number of tensors in `Xs`.
    """
    B = len(Xs)
    L = Xs[0].shape[0]
    max_D = max(t.shape[-1] for t in Xs)  # type: ignore

    X = np.zeros((B, L, max_D), dtype=Xs[0].dtype)
    for i, t in enumerate(Xs):
        X[i, :, : t.shape[-1]] = t

    return np.ascontiguousarray(X)


def pairwise_distance(A: Tensor, B: Tensor | None = None):
    """Compute the pairwise squared Euclidean distance between points in `A` (or between points in `A` and `B`).

    Parameters
    ----------
    `A` : `Tensor` of shape `(L, D)` or `(B, L, D)`
        `B`: batch size
        `L`: number of points
        `D`: dimension of each point
    `B` : `Tensor` of shape `(L', D)` or `(B, L', D)`
        `B`: batch size
        `L'`: number of points
        `D`: dimension of each point

    Returns
    -------
    When `A` is of shape `(L, D)`:
        `Tensor` of shape `(L, L)` [or `(L, L')`] where the element at position `(i, j)` is the squared Euclidean distance between `A[i]` and `A[j]` [or between `A[i]` and `B[j]`].
    When `A` is of shape `(B, L, D)`:
        `Tensor` of shape `(B, L, L)` [or `(B, L, L')`] where the element at position `(b, i, j)` is the squared Euclidean distance between `A[b, i]` and `A[b, j]`.
    """
    if B is None:
        B = A

    return (A.unsqueeze(A.ndim - 1) - B.unsqueeze(B.ndim - 2)).pow(2).sum(-1)


def topk(x: np.ndarray, k: int, largest=True):
    """Find the `k` largest or smallest elements in `x`.

    Parameters
    ----------
    `x` : `np.ndarray` of shape (N,)
    `k` : `int`
    `largest` : `bool`

    Returns
    -------
    `indices` : `np.ndarray` of shape `(k,)`
    `values` : `np.ndarray` of shape `(k,)`

    Notes
    -----
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
