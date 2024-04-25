import os

import h5py as h5
import matplotlib.pyplot as plt
import numpy as np


def plot(A):
    N = len(A)
    theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
    x = np.cos(theta)
    y = np.sin(theta)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(x, y, s=50, color="blue", zorder=2)

    for i in range(N):
        for j in range(N):
            if A[i, j] != 0:
                ax.annotate("", xy=(x[j], y[j]), xytext=(x[i], y[i]), arrowprops=dict(arrowstyle="->", color="grey", lw=1, alpha=0.6))

    ax.axis("off")

    return fig


output = "outputs"
job_id = "job_01hwb3r8vqfzqb0ks9dzmzft9a"

with h5.File(os.path.join(output, str(job_id), "ring.h5"), "r") as f:
    A = f["A"][:]
    print(A)
    fig = plot(A)
    fig.savefig(os.path.join(output, str(job_id), "ring.png"))
