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


def pairwise_distance(X: Tensor):
    return (X.unsqueeze(1) - X.unsqueeze(0)).pow(2).sum(-1)


def topk(x: np.ndarray, k: int, largest=True):
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
    t: list[int],
    Tp: int,
    exclusion_radius: int | None = None,
):
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
        # exclude neighbors within exclusion_radius
        if exclusion_radius is not None:
            mask[max(0, i - exclusion_radius) : min(N, i + exclusion_radius + 1)] = (
                False
            )

        # find k nearest neighbors
        indices_masked, _ = topk(D[i][mask], k, largest=False)
        indices = seq[mask][indices_masked]
        neighbors.append(indices)

    observations = Y[t]
    # TODO: parallelize
    predictions = np.array([Y[indices + Tp].mean() for indices in neighbors])

    return observations, predictions
