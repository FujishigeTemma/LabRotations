import generate
import numpy as np
from edm.ccm import find_best_embedding


def test_find_best_embedding():
    sigma, rho, beta = 10, 28, 8 / 3
    X0 = np.array([0.1, 0, 0])
    dt, t_max = 0.01, 20  # 2000
    _, X = generate.lorenz(sigma, rho, beta, X0, dt, t_max)

    assert not np.isnan(X).any(), "Generated data contains NaNs"

    x = X[:, 0]
    tau_list = list(range(1, 11))
    e_list = list(range(1, 11))
    Tp = 10

    tau, E, rho = find_best_embedding(x, tau_list, e_list, Tp)

    print(f"tau: {tau}, E: {E}, rho: {rho}")
    assert tau == 1 and E == 2 and rho < 0.9
