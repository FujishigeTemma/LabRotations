import numpy as np
from edmkit.tensor import Tensor, dtypes
from edmkit.util import pad, pairwise_distance, topk


def test_topk():
    x = np.array([6, 4, 2, 1, 5, 3])
    k = 3

    largest = True
    indices, values = topk(x, k, largest)
    assert (indices == np.array([1, 4, 0])).all()
    assert (values == np.array([4, 5, 6])).all()

    largest = False
    indices, values = topk(x, k, largest)
    assert (indices == np.array([3, 2, 5])).all()
    assert (values == np.array([1, 2, 3])).all()


def test_pad():
    # (L, D) = (2, 4), (2, 3), (2, 2) -> (L, D) = (2, 4), (2, 4), (2, 4)
    X1 = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    X2 = np.array([[9, 10, 11], [13, 14, 15]])
    X3 = np.array([[17, 18], [21, 22]])
    X = pad([X1, X2, X3])

    assert (
        X
        == np.array(
            [
                [[1, 2, 3, 4], [5, 6, 7, 8]],
                [[9, 10, 11, 0], [13, 14, 15, 0]],
                [[17, 18, 0, 0], [21, 22, 0, 0]],
            ]
        )
    ).all()


def test_pairwise_distance():
    # Test when A is of shape (L, D) = (3, 4) -> (L, L) = (3, 3)
    X = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])
    X = Tensor(X, dtype=dtypes.float32)
    D = pairwise_distance(X).numpy()
    assert (D == np.array([[0, 64, 256], [64, 0, 64], [256, 64, 0]])).all()

    # Test when A is of shape (B, L, D) = (3, 2, 4) -> (B, L, L) = (3, 2, 2)
    X = np.array(
        [
            [[1, 2, 3, 4], [5, 6, 7, 8]],
            [[9, 10, 11, 0], [13, 14, 15, 0]],
            [[17, 18, 0, 0], [21, 22, 0, 0]],
        ]
    )
    X = Tensor(X, dtype=dtypes.float32)
    D = pairwise_distance(X).numpy()
    assert (D == np.array([[[0, 64], [64, 0]], [[0, 48], [48, 0]], [[0, 32], [32, 0]]])).all()


def test_pairwise_distance_without_batch_A_only():
    # A is of shape (L, D)
    A = Tensor([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    expected = Tensor([[0.0, 1.0, 1.0], [1.0, 0.0, 2.0], [1.0, 2.0, 0.0]])
    actual = pairwise_distance(A)
    assert (actual == expected).all().numpy()


def test_pairwise_distance_without_batch_A_and_B():
    # A is of shape (L, D)
    A = Tensor([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    # B is of shape (L', D) with L' != L
    B = Tensor([[1.0, 1.0], [2.0, 2.0], [0.0, 2.0], [2.0, 0.0]])
    expected = Tensor([[2.0, 8.0, 4.0, 4.0], [1.0, 5.0, 5.0, 1.0], [1.0, 5.0, 1.0, 5.0]])
    actual = pairwise_distance(A, B)
    assert (actual == expected).all().numpy()


def test_pairwise_distance_with_batch_A_only():
    # A is of shape (B, L, D)
    A = Tensor([[[0.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [1.0, 1.0]]])
    expected = Tensor([[[0.0, 1.0], [1.0, 0.0]], [[0.0, 1.0], [1.0, 0.0]]])
    actual = pairwise_distance(A)
    assert (actual == expected).all().numpy()


def test_pairwise_distance_with_batch_A_and_B():
    # A is of shape (B, L, D)
    A = Tensor([[[0.0, 0.0], [1.0, 0.0]], [[0.0, 1.0], [1.0, 1.0]]])  # Shape: (2, 2, 2)
    # B is of shape (B, L', D) with L' != L
    B = Tensor([[[1.0, 1.0], [2.0, 2.0], [3.0, 3.0]], [[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]]])  # Shape: (2, 3, 2)
    expected = Tensor([[[2.0, 8.0, 18.0], [1.0, 5.0, 13.0]], [[1.0, 2.0, 5.0], [2.0, 1.0, 2.0]]])
    actual = pairwise_distance(A, B)
    assert (actual == expected).all().numpy()
