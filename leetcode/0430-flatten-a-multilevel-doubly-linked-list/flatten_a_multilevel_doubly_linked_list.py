#!/usr/bin/env python3

# Flatten a Multilevel Doubly Linked List
#
# https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list
#
# You are given a doubly linked list, which contains nodes that have a next
# pointer, a previous pointer, and an additional child pointer. This child
# pointer may or may not point to a separate doubly linked list, also containing
# these special nodes. These child lists may have one or more children of their
# own, and so on, to produce a multilevel data structure as shown in the example
# below.
# Given the head of the first level of the list, flatten the list so that all
# the nodes appear in a single-level, doubly linked list. Let curr be a node
# with a child list. The nodes in the child list should appear after curr and
# before curr.next in the flattened list.
# Return the head of the flattened list. The nodes in the list must have all of
# their child pointers set to null.


from collections import deque
from typing import Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # assert algo(head = [1,2,3,4,5,6,null,null,null,7,8,9,10,null,null,11,12]) == [1,2,3,7,8,11,12,9,10,4,5,6]
        # assert algo(head = [1,2,null,3]) == [1,3,2]
        # assert algo(head = []) == []
        assert algo(head=Node(1, next=Node(3, next=Node(2)))) == Node(
            1, next=Node(3, next=Node(2))
        )
        algo()
        pass
        assert False

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        # solution.copy_all_recursive,
        # solution.copy_all_iterative,
        # solution.recursive,
        solution.iterative,
    ]:
        test_algo(algo)


class Node:
    def __init__(self, val, prev=None, next=None, child=None):
        self.val = val
        self.prev = prev
        self.next = next
        self.child = child


def print_linked_list(node):
    if node is not None:
        print(node.val, end=" -> ")
        print_linked_list(node.next)
    else:
        print("None")


class Solution:
    def copy_all_recursive(self, head: Optional[Node]) -> Optional[Node]:
        """
        Approach:  Copy all, recursively.
        Idea:      Iterate over all nodes (child first, then next node), and copy them into a new linked list.
        Time:      O(n): We iterate over each of the n nodes once.
        Space:     O(n): We don't just change the node pointers, but copy each node into output list.
        Leetcode:  41 ms runtime, 17.41 MB memory
        """

        flat_dummy_head = Node(val=-1, prev=None, next=None, child=None)
        flat_prev = flat_dummy_head

        def visit(node: Node):
            nonlocal flat_prev
            new_curr = Node(node.val, prev=None, next=None, child=None)
            new_curr.prev = flat_prev
            flat_prev.next = new_curr
            flat_prev = new_curr

        def iter(node: Optional[Node]):
            if node is not None:
                visit(node)
                iter(node.child)
                iter(node.next)

        iter(head)

        flat_head = flat_dummy_head.next

        if flat_head is not None:
            # Remove dummy head.
            flat_head.prev = None

        return flat_head

    def copy_all_iterative(self, head: Optional[Node]) -> Optional[Node]:
        """
        Approach:  Copy all, iteratively.
        Idea:      Iterate over all nodes (child first, then next node), and copy them into a new linked list.
        Time:      O(n): We iterate over each of the n nodes once.
        Space:     O(n): We don't just change the node pointers, but copy each node into output list. Also, the stack can grow to at most n elements.
        Leetcode:  30 ms runtime, 17.36 MB memory
        """

        flat_dummy_head = Node(val=-1, prev=None, next=None, child=None)
        flat_prev = flat_dummy_head

        def visit(node: Node):
            nonlocal flat_prev
            new_curr = Node(node.val, prev=None, next=None, child=None)
            new_curr.prev = flat_prev
            flat_prev.next = new_curr
            flat_prev = new_curr

        stack = []
        stack.append(head)
        while stack:
            if (curr := stack.pop()) is not None:
                visit(curr)
                stack.extend((curr.next, curr.child))

        flat_head = flat_dummy_head.next

        if flat_head is not None:
            # Remove dummy head.
            flat_head.prev = None

        return flat_head

    def recursive(self, head: Optional[Node]) -> Optional[Node]:
        """
        Approach:  Recursion.
        Idea:      Iterate over all nodes (child first, then next node), updating next and prev pointers along the way.
        Time:      O(n): We iterate over each of the n nodes once.
        Space:     O(1): No additional memory is used (besides OS recursion stack).
        Leetcode:  46 ms runtime, 17.16 MB memory
        """

        def flatten(
            head: Optional[Node], rest: Optional[Node]
        ) -> Optional[Node]:
            if head is None:
                return rest
            else:
                # Append flattened child first, then append flattened next.
                head.next = flatten(head.child, flatten(head.next, rest))
                if head.next is not None:
                    head.next.prev = head
                head.child = None
                return head

        return flatten(head, None)

    def iterative(self, head: Optional[Node]) -> Optional[Node]:
        """
        Approach:  Iterative.
        Idea:      Iterate over all nodes (child first, then next node), updating next and prev pointers along the way.
        Time:      O(n): We iterate over each of the n nodes once.
        Space:     O(n): The stack will contain at most n elements.
        Leetcode:  44 ms runtime, 17.12 MB memory
        """

        flat_dummy_head = Node(val=-1, prev=None, next=None, child=None)

        stack = [head]
        prev = flat_dummy_head
        while stack:
            if (curr := stack.pop()) is not None:
                # Plan on visiting next after child has been visited completely.
                stack.extend((curr.next, curr.child))

                prev.next = curr
                curr.prev = prev

                curr.child = None

                prev = curr

        flat_head = flat_dummy_head.next

        if flat_head is not None:
            # Remove dummy head.
            flat_head.prev = None

        return flat_head
