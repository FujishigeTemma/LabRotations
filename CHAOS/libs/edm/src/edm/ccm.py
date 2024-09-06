import numpy as np
import polars as pl

from edm.embedding import lagged_embed
from edm.tensor import Tensor, dtypes
from edm.util import pad, pairwise_distance, topk


def calculate_rho(observations: np.ndarray, predictions: np.ndarray):
    assert len(observations) == len(predictions), "observations and predictions must have the same length"
    rho = np.corrcoef(observations, predictions)[0, 1]
    return rho


def find_best_embedding(x: np.ndarray, tau_list: list[int], e_list: list[int], Tp: int):
    assert all(tau > 0 for tau in tau_list), "tau must be positive"
    assert all(e > 0 for e in e_list), "e must be positive"

    # embeding.shape[0] == N - (e - 1) * tau
    min_L = len(x) - (max(e_list) - 1) * max(tau_list)
    assert min_L > 0, "Not enough data points to embed"

    embeddings: list[np.ndarray] = []
    for tau in tau_list:
        for e in e_list:
            # align the time indices of the embeddings. note that the time index of the first embedding is `1 + (e - 1) * tau`
            # embeding.shape = (min_L, e)
            embeddings.append(lagged_embed(x, tau, e)[-min_L:])

    X = pad(embeddings)
    D = pairwise_distance(Tensor(X, dtype=dtypes.float32)).numpy()

    L = min_L
    seq = np.arange(L)
    lib_size = L // 2

    best_tau = None
    best_e = None
    best_rho = -np.inf

    for i, tau in enumerate(tau_list):
        for j, e in enumerate(e_list):
            samples_indecies = np.arange(lib_size, L)

            observations = X[i * len(e_list) + j, samples_indecies, :e]
            predictions = np.zeros((len(samples_indecies), e), dtype=x.dtype)

            for k, t in enumerate(samples_indecies):
                # [0, 1, 2, 3, 4 | 5, 6, 7, 8, 9, 10]; initialize mask, `|` separates lib and test
                mask = np.ones(L, dtype=bool)

                # [0, 1, 2, 3, 4 | 5, F, 7, 8, 9, 10], t = 6; exclude self
                mask[t] = False

                # [0, 1, 2, 3, 4 | 5, F, 7, 8, F, F ], Tp = 2; exclude last Tp points to prevent out-of-bound indexing on predictions
                mask[-Tp:] = False

                # [0, 1, 2, 3, 4 | F, F, F, F, F, F ], lib_size = 5; exclude test points
                mask[lib_size:] = False

                # find k(=e+1) nearest neighbors in phase space for simplex projection
                indices_masked, _ = topk(D[i * len(e_list) + j, t, mask], e + 1, largest=False)
                indices = seq[mask][indices_masked]
                predictions[k] = X[i * len(e_list) + j, indices + Tp].mean()

            rho = calculate_rho(observations, predictions)
            if rho > best_rho:
                best_tau = tau
                best_e = e
                best_rho = rho

    return best_tau, best_e, best_rho


def scan_best_embedding(x: np.ndarray, tau_list: list[int], e_list: list[int], Tp: int):
    assert all(tau > 0 for tau in tau_list), "tau must be positive"
    assert all(e > 0 for e in e_list), "e must be positive"

    # embeding.shape[0] == N - (e - 1) * tau
    min_L = len(x) - (max(e_list) - 1) * max(tau_list)
    assert min_L > 0, "Not enough data points to embed"

    embeddings: list[np.ndarray] = []
    for tau in tau_list:
        for e in e_list:
            # embeding.shape = (min_L, e)
            embeddings.append(lagged_embed(x, tau, e)[-min_L:])

    X = pad(embeddings)
    D = pairwise_distance(Tensor(X, dtype=dtypes.float32))
    D = D.numpy()

    L = min_L
    seq = np.arange(L)
    lib_size = L // 2

    rho = np.zeros((len(tau_list), len(e_list)))

    for i, tau in enumerate(tau_list):
        for j, e in enumerate(e_list):
            samples_indecies = np.arange(lib_size, L - Tp)

            observations = X[i + j, samples_indecies + Tp, :e]
            predictions = np.zeros((len(samples_indecies), e), dtype=x.dtype)

            for k, t in enumerate(samples_indecies):
                mask = np.ones(L, dtype=bool)
                # exclude self
                mask[t] = False
                # exclude last Tp points to prevent out-of-bound indexing
                mask[max(0, L - Tp) :] = False
                # exclude test points
                mask[lib_size:] = False
                # find k nearest neighbors
                indices_masked, _ = topk(D[i + j, t, mask], e + 1, largest=False)
                indices = seq[mask][indices_masked]
                predictions[k] = X[i + j, indices + Tp].mean()

            rho[i, j] = calculate_rho(observations, predictions)

    df = pl.DataFrame(
        {
            "tau": np.repeat(tau_list, len(e_list)),
            "e": np.tile(e_list, len(tau_list)),
            "rho": rho.flatten(),
        }
    )

    return df
