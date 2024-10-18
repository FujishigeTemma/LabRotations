import numpy as np

from edmkit.tensor import Tensor


def pad(As: list[np.ndarray]):
    """Pad the `np.ndarray` in `Xs` to merge them into a single `np.ndarray`.

    Parameters
    ----------
        `As` : `list` of `np.ndarray` of shape `(L, D_i)`

    Returns
    -------
        Single `np.ndarray` of shape `(B, L, max(D))` where `B` is `len(As)`

    Raises
    ------
    AssertionError
        - If any array in `As` is not 2D.
        - If the first dimension of all arrays in `As` are not equal.
    """
    assert all(A.ndim == 2 for A in As), "All arrays must be 2D"
    assert all(A.shape[0] == As[0].shape[0] for A in As), "All arrays must have the same length"

    B = len(As)
    L = As[0].shape[0]
    max_D = max(t.shape[-1] for t in As)  # type: ignore

    A = np.zeros((B, L, max_D), dtype=As[0].dtype)
    for i, x in enumerate(As):
        A[i, :, : x.shape[-1]] = x

    return np.ascontiguousarray(A)


def _pairwise_distance(A: Tensor, B: Tensor):
    A_sq = A.pow(2).sum(-1, keepdim=True)
    B_sq = B.pow(2).sum(-1, keepdim=True).transpose(-1, -2)

    D = A_sq + B_sq - 2 * A.matmul(B.transpose(-1, -2))

    return D.clamp(min_=0)


def pairwise_distance(A: Tensor, B: Tensor | None = None):
    """Compute the pairwise squared Euclidean distance between points in `A` (or between points in `A` and `B`).

    Parameters
    ----------
    `A` : `Tensor` of shape `(L, D)` or `(B, L, D)`
        - `B`: batch size
        - `L`: number of points
        - `D`: dimension of each point
    `B` : `Tensor` of shape `(L', D)` or `(B, L', D)`
        - `B`: batch size
        - `L'`: number of points
        - `D`: dimension of each point

    Returns
    -------
    When `A` is of shape `(L, D)`:
        `Tensor` of shape `(L, L)` [or `(L, L')`] where the element at position `(i, j)` is the squared Euclidean distance between `A[i]` and `A[j]` [or between `A[i]` and `B[j]`].
    When `A` is of shape `(B, L, D)`:
        `Tensor` of shape `(B, L, L)` [or `(B, L, L')`] where the element at position `(b, i, j)` is the squared Euclidean distance between `A[b, i]` and `A[b, j]`.

    Raises
    ------
    AssertionError
        - If `A` is not a 2D or 3D tensor.
        - If `B` is not `None` and `A` and `B` have different number of dimensions.
    """
    assert A.ndim == 2 or A.ndim == 3, "A must be a 2D or 3D tensor"
    assert B is None or (A.ndim == B.ndim), "A and B must have the same number of dimensions"

    if B is None:
        B = A

    A_sq = A.pow(2).sum(-1, keepdim=True)
    B_sq = B.pow(2).sum(-1, keepdim=True).transpose(-1, -2)

    D = A_sq + B_sq - 2 * A.matmul(B.transpose(-1, -2))

    return D.clamp(min_=0)


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

    Raises
    ------
    AssertionError
        - If `x` is not a 1D array.
        - If `k` is not in the range `(0, len(x)]`.

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


def autocorrelation(x: np.ndarray, max_lag: int, step: int = 1):
    """
    Computes the autocorrelation of a given 1D numpy array up to a specified maximum lag.

    Parameters
    ----------
        `x` : `np.ndarray` The input array for which to compute the autocorrelation.
        `max_lag` : `int` The maximum lag up to which the autocorrelation is computed.
        `step` : `int`, `optional` The step size for the lag. Default is 1.

    Returns
    -------
        `np.ndarray` of shape `(max_lag // step + 1,)` containing the autocorrelation values.
    """
    lags = np.arange(1, max_lag, step)
    autocorr = [1] + [np.corrcoef(x[:-lag], x[lag:])[0, 1] for lag in lags]
    return np.array(autocorr)
