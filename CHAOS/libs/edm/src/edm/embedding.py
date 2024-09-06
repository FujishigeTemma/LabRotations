import numpy as np


def lagged_embed(x: np.ndarray, tau: int, e: int):
    """Lagged embedding of a time series `x`.

    Parameters
    ----------
        `x` : `np.ndarray` of shape `(N,)`
        `tau` : `int`
        `e` : `int`

    Returns
    -------
        `np.ndarray` of shape `(N - (e - 1) * tau, e)`

    Examples
    --------
    ```
    import numpy as np
    from edm.embedding import lagged_embed

    x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    tau = 2
    e = 3

    E = lagged_embed(x, tau, e)
    print(E)
    print(E.shape)
    # [[1 3 5]
    #  [2 4 6]
    #  [3 5 7]
    #  [4 6 8]
    #  [5 7 9]]
    # (5, 3)
    ```
    """
    assert len(x.shape) == 1, "X must be an array of scalars"
    assert tau > 0 and e > 0, "tau and e must be positive"
    assert e * tau <= x.shape[0], "e and tau must satisfy `e * tau < len(X)`"

    return np.array(
        [x[tau * (e - 1) :]] + [x[tau * i : -tau * ((e - 1) - i)] for i in reversed(range(e - 1))]
    ).transpose()
