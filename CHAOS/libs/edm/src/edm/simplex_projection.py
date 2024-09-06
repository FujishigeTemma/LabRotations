import numpy as np

from edm.tensor import Tensor, dtypes
from edm.util import pairwise_distance, topk


def simplex_projection(
    X: np.ndarray,
    Y: np.ndarray,
    t: np.ndarray,
    partition: int | None = None,
    exclusion_radius: int | None = None,
):
    assert X.shape[0] == Y.shape[0], "X and Y must have the same length"

    D = pairwise_distance(Tensor(X, dtype=dtypes.float32)).numpy()

    N = D.shape[0]
    seq = np.arange(N)

    k: int = X.shape[1] + 1
    neighbors = []

    for i in t:
        mask = np.ones(N, dtype=bool)

        # exclude self
        mask[i] = False

        # split into lib and test
        if partition is not None:
            assert partition < N, "partition must be less than the number of points"
            assert (t >= partition).all(), "t must be greater than or equal to partition when partition is specified"
            mask[partition:] = False

        # exclude neighbors within exclusion_radius
        if exclusion_radius is not None:
            mask[max(0, i - exclusion_radius) : min(N, i + exclusion_radius + 1)] = False

        # find k nearest neighbors
        indices_masked, _ = topk(D[i][mask], k, largest=False)
        indices = seq[mask][indices_masked]
        neighbors.append(indices)

    observations = X[t]
    predictions = np.array([Y[indices].mean() for indices in neighbors])

    return observations, predictions
