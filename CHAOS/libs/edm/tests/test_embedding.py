import numpy as np
from edm.embedding import lagged_embed


def test_lagged_embed():
    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    tau = 2
    e = 3

    X = lagged_embed(x, tau, e)
    assert (
        X == np.array([[1, 3, 5], [2, 4, 6], [3, 5, 7], [4, 6, 8], [5, 7, 9]])
    ).all()
