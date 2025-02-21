import pytest
from edmkit.heap import FibonacciHeap


@pytest.fixture
def empty_heap():
    """
    Returns an empty FibonacciHeap.
    """
    return FibonacciHeap()


@pytest.fixture
def small_heap():
    """
    Returns a FibonacciHeap with a few inserted elements.
    """
    heap = FibonacciHeap()
    heap.insert(10, "ten")
    heap.insert(3, "three")
    heap.insert(5, "five")
    return heap


@pytest.fixture
def large_heap():
    """
    Returns a FibonacciHeap with more elements inserted.
    """
    heap = FibonacciHeap()
    heap.insert(8, "eight")
    heap.insert(2, "two")
    heap.insert(15, "fifteen")
    heap.insert(1, "one")
    heap.insert(9, "nine")
    heap.insert(20, "twenty")
    heap.insert(7, "seven")
    heap.insert(4, "four")
    heap.insert(11, "eleven")
    heap.insert(3, "three")
    heap.insert(6, "six")
    heap.insert(13, "thirteen")
    heap.insert(16, "sixteen")
    heap.insert(14, "fourteen")
    heap.insert(5, "five")
    return heap


def test_min_on_empty_heap(empty_heap: FibonacciHeap):
    """
    For an empty heap, min() should return None.
    """
    assert empty_heap.min() is None


def test_min_on_non_empty_heap(small_heap: FibonacciHeap):
    """
    Test min() on a non-empty heap.
    The minimum key should be 3 for the given small_heap fixture.
    """
    min_node = small_heap.min()
    assert min_node is not None
    assert min_node.key == 3


def test_insert_and_min(empty_heap: FibonacciHeap):
    """
    Test insert() and min() by inserting multiple elements in sequence.
    """
    node_100 = empty_heap.insert(100, "hundred")
    assert empty_heap.min() == node_100
    assert empty_heap.min().key == 100

    node_200 = empty_heap.insert(200, "two-hundred")
    # The min node should still be 100
    assert empty_heap.min() == node_100
    assert empty_heap.min().key == 100

    node_50 = empty_heap.insert(50, "fifty")
    # Now the min node should be 50
    assert empty_heap.min() == node_50
    assert empty_heap.min().key == 50


def test_pop_on_empty_heap(empty_heap: FibonacciHeap):
    """
    For an empty heap, pop() should return None.
    """
    popped = empty_heap.pop()
    assert popped is None
    # The heap remains empty.
    assert empty_heap.min() is None


def test_pop_on_non_empty_heap(small_heap: FibonacciHeap):
    """
    Test pop() on a small heap:
    - The smallest key is 3, so it should pop first.
    - Then 5, then 10, until the heap is empty.
    """
    # small_heap has keys: 10, 3, 5
    popped_first = small_heap.pop()
    assert popped_first.key == 3
    # Next min should be 5
    assert small_heap.min().key == 5

    popped_second = small_heap.pop()
    assert popped_second.key == 5
    # Next min should be 10
    assert small_heap.min().key == 10

    popped_third = small_heap.pop()
    assert popped_third.key == 10
    # Now the heap should be empty
    assert small_heap.min() is None

    # Popping again should return None
    popped_empty = small_heap.pop()
    assert popped_empty is None


def test_decrease_key_valid(small_heap: FibonacciHeap):
    """
    Test decrease_key() under valid conditions.
    - Decrease the key of a node from 10 to 2.
    - Verify that min() is updated accordingly.
    - Also test an invalid decrease_key call (new key > old key) if applicable.
    """
    # Find the node that has key == 10 in the small_heap
    node_to_decrease = None
    for node in small_heap.iterate(small_heap.min()):
        if node.key == 10:
            node_to_decrease = node
            break

    # Decrease its key to 2
    small_heap.decrease_key(node_to_decrease, 2)
    # Now the min should be 2
    assert small_heap.min().key == 2

    # Try decreasing the key to a value greater than the current key (10) - should be a no-op
    small_heap.decrease_key(node_to_decrease, 11)
    # The key should remain 2
    assert node_to_decrease.key == 2


def test_decrease_key_on_min(small_heap: FibonacciHeap):
    """
    Decrease the key of the current min node to an even smaller key.
    """
    # The min node in small_heap has key == 3
    min_node = small_heap.min()
    original_min_key = min_node.key
    assert original_min_key == 3

    # Decrease key from 3 to 1
    small_heap.decrease_key(min_node, 1)
    assert small_heap.min().key == 1
    assert small_heap.min() == min_node


def test_merge_empty_with_small_heap(empty_heap: FibonacciHeap, small_heap: FibonacciHeap):
    """
    Test merging an empty heap with a small heap.
    """
    merged = empty_heap.merge(small_heap)
    # Expect merged to be equivalent to small_heap
    assert merged.min().key == 3

    # Pop all elements to confirm they match the small_heap contents
    assert merged.pop().key == 3
    assert merged.pop().key == 5
    assert merged.pop().key == 10
    # Now it should be empty
    assert merged.pop() is None


def test_merge_small_with_large_heap(small_heap: FibonacciHeap, large_heap: FibonacciHeap):
    """
    Test merging a small heap with a large heap.
    """
    merged = small_heap.merge(large_heap)
    # The combined keys should include:
    #   [1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 20]
    #   (two '3's, two '5's, etc.)
    # The minimum of all those keys is 1
    assert merged.min().key == 1

    # Optional check: pop everything and confirm sorted order
    expected_sorted_keys = [1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 20]
    for expected_key in expected_sorted_keys:
        popped = merged.pop()
        assert popped.key == expected_key, f"Expected {expected_key}, got {popped.key}"

    # Now it should be empty
    assert merged.pop() is None


def test_iterate(small_heap: FibonacciHeap):
    """
    Test the iterate() function to ensure it properly traverses
    the circular doubly linked list of the root nodes.
    """
    # For small_heap, the keys are 3, 5, 10.
    head = small_heap.min()
    assert head is not None

    # Count how many nodes we see in the root list.
    count = 0
    for node in small_heap.iterate(head):
        count += 1
        # Check if node has at least the 'key' attribute
        assert hasattr(node, "key"), "Node should have a 'key' attribute."

    # If no linking or cutting has happened yet, we expect at least
    # these 3 nodes in the root list.
    # (Implementation details may differ if nodes have been rearranged internally.)
    assert count >= 3, "The root list should contain at least the 3 inserted nodes."
