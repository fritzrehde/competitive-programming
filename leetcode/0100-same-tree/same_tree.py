#!/usr/bin/env python3

# Same Tree
#
# https://leetcode.com/problems/same-tree
#
# Given the roots of two binary trees p and q, write a function to check if they
# are the same or not.
# Two binary trees are considered the same if they are structurally identical,
# and the nodes have the same value.


from collections import deque
from typing import Optional
from binary_tree import TreeNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                p=TreeNode(1, left=TreeNode(2), right=TreeNode(3)),
                q=TreeNode(1, left=TreeNode(2), right=TreeNode(3)),
            )
            == True
        )
        assert (
            algo(
                p=TreeNode(1, left=TreeNode(2)),
                q=TreeNode(1, right=TreeNode(2)),
            )
            == False
        )
        assert (
            algo(
                p=TreeNode(1, left=TreeNode(2), right=TreeNode(1)),
                q=TreeNode(1, left=TreeNode(1), right=TreeNode(2)),
            )
            == False
        )
        assert (
            algo(
                p=TreeNode(10, left=TreeNode(5), right=TreeNode(15)),
                q=TreeNode(10, left=TreeNode(5, right=TreeNode(15))),
            )
            == False
        )
        assert (
            algo(
                p=TreeNode(1),
                q=TreeNode(1, right=TreeNode(2)),
            )
            == False
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.preorder_traversal_iterative,
        solution.preorder_traversal_recursive,
    ]:
        test_algo(algo)


class Solution:
    def preorder_traversal_iterative(
        self, p: Optional[TreeNode], q: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Pre-order traversal, implemented iteratively.
        Idea:      Maintain a queue of nodes still left to visit for each tree, and visit in the same (pre-)order. We also need to uniquely label each node as being either the left or right child, and being the child of its parent, which we do by storing a string "{parent}{left|right}" alongside each child node.
        Time:      O(n): Given n nodes in each tree, every node is visited exactly once.
        Space:     O(n): The queues that store the next children nodes to visit can grow up to size n.
        Leetcode:  38 ms runtime, 16.67 MB memory
        """

        if p is None or q is None:
            return p is None and q is None
        else:
            p_queue = deque()
            q_queue = deque()
            p_queue.append((p, "root"))
            q_queue.append((q, "root"))

            while True:
                if (not p_queue) and (not q_queue):
                    return True
                else:
                    if p_queue and q_queue:
                        # Preorder traversal.
                        (p_next, p_which_child) = p_queue.popleft()
                        (q_next, q_which_child) = q_queue.popleft()
                        if p_next.val != q_next.val:
                            return False
                        if p_which_child != q_which_child:
                            return False

                        def non_none(item) -> bool:
                            (node, _child_status) = item
                            return node is not None

                        p_queue.extend(
                            filter(
                                non_none,
                                [
                                    (p_next.left, f"{p_next.val}left"),
                                    (p_next.right, f"{p_next.val}right"),
                                ],
                            )
                        )
                        q_queue.extend(
                            filter(
                                non_none,
                                [
                                    (q_next.left, f"{q_next.val}left"),
                                    (q_next.right, f"{q_next.val}right"),
                                ],
                            )
                        )
                    else:
                        return False

    def preorder_traversal_recursive(
        self, p: Optional[TreeNode], q: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Pre-order traversal, implemented recursively.
        Idea:      For two trees to be equal, either their roots could both be None, or their root's value is the same, and the left and right subtrees of both are equal, recursively.
        Time:      O(n): Given n nodes in each tree, every node is visited exactly once.
        Space:     O(1): No additional memory is used (besides the OS recursion stack).
        Leetcode:  26 ms runtime, 16.49 MB memory
        """

        def same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
            match (p, q):
                case (None, None):
                    return True
                case (None, _) | (_, None):
                    return False
                case (some_p, some_q):
                    return (
                        some_p.val == some_q.val
                        and same_tree(some_p.left, some_q.left)
                        and same_tree(some_p.right, some_q.right)
                    )
                case _:
                    raise Exception("unreachable")

        return same_tree(p, q)
