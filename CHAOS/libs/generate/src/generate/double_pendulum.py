import numpy as np


def double_pendulum(
    m1: float,
    m2: float,
    L1: float,
    L2: float,
    g: float,
    X0: np.ndarray,
    dt: float,
    t_max: int,
):
    def f(x: np.ndarray):
        # TODO
        return x

    t = np.arange(0, t_max, dt)
    X = np.zeros((len(t), 4))
    X[0] = X0

    for i in range(1, len(t)):
        X[i] = X[i - 1] + dt * f(X[i - 1])

    return t, X
