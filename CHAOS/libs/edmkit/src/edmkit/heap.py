from __future__ import annotations

import math
from typing import Any, Generator


class FibonacciHeap:
    """
    A Fibonacci heap is a collection of trees satisfying the min-heap property.

    Methods
    -------
    iterate(head: Node) -> Generator[Node, None, None]
        Iterate through a circular doubly linked list starting from 'head'.
    min() -> Node | None
        Return the node with the minimum key (or None if empty).
    pop() -> Node | None
        Extract (remove) the node with the minimum key from the heap.
    insert(key: float, value: Any = None) -> Node
        Insert a new node into the root list.
    decrease_key(x: Node, k: float) -> None
        Decrease the key of node x to k.
    merge(h2: FibonacciHeap) -> FibonacciHeap
        Merge the current heap with another Fibonacci heap h2.
    """

    class Node:
        def __init__(self, key: int | float, value: Any) -> None:
            self.key: int | float = key
            """The key of the node."""
            self.value: Any = value
            """The value of the node."""
            self.parent: FibonacciHeap.Node | None = None
            """Pointer to the parent node."""
            self.child: FibonacciHeap.Node | None = None
            """Pointer to the child node."""
            self.left: FibonacciHeap.Node | None = None
            """Pointer to the left sibling node."""
            self.right: FibonacciHeap.Node | None = None
            """Pointer to the right sibling node."""
            self.degree: int = 0
            """The degree of the node."""
            self.mark: bool = False
            """Whether the node has lost a child since the last time it was made the child of another node."""

    def __init__(self) -> None:
        self.root_list: FibonacciHeap.Node | None = None
        """Pointer to the head of the root list"""
        self.min_node: FibonacciHeap.Node | None = None
        """Pointer to the minimum node in the heap"""
        self.total_nodes: int = 0
        """Total number of nodes in the heap"""

    def iterate(self, head: Node) -> Generator[Node, None, None]:
        """Iterate through a circular doubly linked list starting from 'head'."""
        node = stop = head
        started = False
        while True:
            if node == stop and started:
                break
            yield node
            node = node.right
            started = True

    def min(self) -> Node | None:
        """Return the minimum node (or None if empty)."""
        return self.min_node

    def pop(self) -> Node | None:
        """Extract (remove) the minimum node from the heap."""
        minimum = self.min_node
        if minimum is not None:
            # Move min_node's children (if any) to the root list
            if minimum.child is not None:
                children = list(self.iterate(minimum.child))
                for child in children:
                    self._add_to_root_list(child)
                    child.parent = None

            self._remove_from_root_list(minimum)

            # If minimum was the only node in the root list
            if minimum == minimum.right:
                self.root_list = None
                self.min_node = None
            else:
                self.min_node = minimum.right
                self._consolidate_roots()

            self.total_nodes -= 1

        return minimum

    def insert(self, key: int | float, value: Any = None) -> Node:
        """Insert a new node into the root list."""
        node = self.Node(key, value)
        node.left = node.right = node
        self._add_to_root_list(node)

        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node

        self.total_nodes += 1
        return node

    def decrease_key(self, target: Node, new_key: int | float) -> None:
        """Decrease the key of target node to new_key."""
        if new_key > target.key:
            return  # No-op if new key is greater than current key
        target.key = new_key

        parent = target.parent
        if parent is not None and target.key < parent.key:
            self._detach_child(child=target, parent=parent)
            self._cascade(parent)

        if self.min_node and target.key < self.min_node.key:
            self.min_node = target

    def merge(self, h2: FibonacciHeap) -> FibonacciHeap:
        """Merge the current heap with another Fibonacci heap h2."""
        if self.min_node is None:
            return h2
        if h2.min_node is None:
            return self

        # Create a new heap
        merged = FibonacciHeap()
        merged.root_list = self.root_list
        merged.min_node = self.min_node

        # Concatenate root lists of self and h2
        if h2.root_list is not None:
            last_h2_node = h2.root_list.left
            # Link h2's root list into merged_heap's
            h2.root_list.left = merged.root_list.left
            merged.root_list.left.right = h2.root_list

            # Complete the circle
            merged.root_list.left = last_h2_node
            last_h2_node.right = merged.root_list

            # Update min node if needed
            if h2.min_node and h2.min_node.key < merged.min_node.key:
                merged.min_node = h2.min_node

        # Update total node count
        merged.total_nodes = self.total_nodes + h2.total_nodes
        return merged

    # -----------------------------
    #      Private Helper Methods
    # -----------------------------

    def _detach_child(self, child: Node, parent: Node) -> None:
        """Detach 'child' from 'parent' and add it to the root list."""
        self._remove_child_from(parent=parent, child=child)
        parent.degree -= 1
        self._add_to_root_list(child)
        child.parent = None
        child.mark = False

    def _cascade(self, node: Node) -> None:
        """Perform cascading cuts up the tree."""
        parent = node.parent
        if parent is not None:
            if not node.mark:
                node.mark = True
            else:
                self._detach_child(child=node, parent=parent)
                self._cascade(parent)

    def _consolidate_roots(self) -> None:
        """Consolidate the root list by linking trees of the same degree."""
        if self.total_nodes == 0:
            return

        array_size = int(math.log(self.total_nodes, 2)) + 2
        auxiliary_array: list[FibonacciHeap.Node | None] = [None] * array_size

        # Collect all current root nodes
        root_nodes = list(self.iterate(self.root_list)) if self.root_list else []
        for root_node in root_nodes:
            current = root_node
            degree = current.degree
            while auxiliary_array[degree] is not None:
                other = auxiliary_array[degree]
                if current.key > other.key:
                    current, other = other, current
                self._make_child_of(child=other, parent=current)
                auxiliary_array[degree] = None
                degree += 1
            auxiliary_array[degree] = current

        self.min_node = None

        # Reconstruct the root list from the auxiliary array
        for entry in auxiliary_array:
            if entry is not None:
                if self.min_node is None:
                    self.root_list = entry
                    self.min_node = entry
                    entry.left = entry
                    entry.right = entry
                else:
                    self._add_to_root_list(entry)
                    if entry.key < self.min_node.key:
                        self.min_node = entry

    def _make_child_of(self, child: Node, parent: Node) -> None:
        """Make 'child' a child of 'parent'."""
        self._remove_from_root_list(child)
        child.left = child.right = child
        self._add_child_to(parent, child)
        parent.degree += 1
        child.parent = parent
        child.mark = False

    def _add_to_root_list(self, node: Node) -> None:
        """Add 'node' to the root list."""
        if self.root_list is None:
            self.root_list = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def _remove_from_root_list(self, node: Node) -> None:
        """Remove 'node' from the root list."""
        if node == self.root_list:
            # If there's only one node, root_list becomes None
            if node.right == node:
                self.root_list = None
            else:
                self.root_list = node.right

        node.left.right = node.right
        node.right.left = node.left

    def _add_child_to(self, parent: Node, child: Node) -> None:
        """Add 'child' to the doubly linked child list of 'parent'."""
        if parent.child is None:
            parent.child = child
        else:
            child.right = parent.child.right
            child.left = parent.child
            parent.child.right.left = child
            parent.child.right = child

    def _remove_child_from(self, parent: Node, child: Node) -> None:
        """Remove 'child' from the child list of 'parent'."""
        if parent.child == child:
            if child.right == child:
                parent.child = None
            else:
                parent.child = child.right

        child.left.right = child.right
        child.right.left = child.left
