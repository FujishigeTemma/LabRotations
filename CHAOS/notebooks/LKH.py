import numpy as np


def save_NODE_COORD_SECTION(arr: np.ndarray, filename: str):
    with open(filename, "w") as f:
        for i, (x, y) in enumerate(arr):
            f.write(f"{i + 1} {x} {y}\n")


def save_EDGE_WEIGHT_SECTION(arr: np.ndarray, filename: str):
    arr = 1 - arr
    arr = arr * 10000
    arr = arr.astype(np.int32)
    with open(filename, "w") as f:
        for row in arr:
            f.write(" ".join(map(str, row)) + "\n")
