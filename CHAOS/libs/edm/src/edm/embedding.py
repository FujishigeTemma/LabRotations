import numpy as np


def lagged_embed(x: np.ndarray, tau: int, e: int):
    assert len(x.shape) == 1, "X must be an array of scalars"
    assert tau > 0 and e > 0, "tau and e must be positive"
    assert e * tau <= x.shape[0], "e and tau must satisfy `e * tau < len(X)`"

    return np.array(
        [x[tau * i : -tau * ((e - 1) - i)] for i in range(e - 1)] + [x[tau * (e - 1) :]]
    ).transpose()
