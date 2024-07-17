#!/usr/bin/env python3

# Binary Tree Postorder Traversal
#
# https://leetcode.com/problems/binary-tree-postorder-traversal/
#
# Given the root of a binary tree, return the postorder traversal of its nodes'
# values.

from typing import List, Optional
from binary_tree import TreeNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(None) == []

        # 2
        assert algo(TreeNode(2)) == [2]

        #   2
        # 1   3
        assert algo(TreeNode(2, TreeNode(1), TreeNode(3))) == [1, 3, 2]

        #     1
        #   X   3
        #     2   X
        assert algo(TreeNode(1, None, TreeNode(3, TreeNode(2), None))) == [2, 3, 1]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.recursive, solution.iterative_state_machine, solution.iterative]:
        test_algo(algo)


class Solution:
    def recursive(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach:  Traverse tree recursively.
        Idea:      Recursively traverse tree, visiting a node only after its children have been visited.
        Time:      O(V): We visit every node once.
        Space:     O(1): We only use the OS recursion stack as additional memory.
        Leetcode:  31 ms runtime, 16.48 MB memory
        """

        order = []

        def visit(node):
            order.append(node.val)

        def traverse(node):
            if node:
                traverse(node.left)
                traverse(node.right)
                visit(node)

        traverse(root)

        return order

    def iterative_state_machine(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach:  Traverse tree iteratively using a state machine.
        Idea:      Each node has a state, which represents the node it will next be visited from (either parent, left child or right child). Only when a node will be visited from the right child may it actually be visited (post-order).
        Time:      O(3V) = O(V): We will "visit" (single iteration in while loop) every node exactly 3 times, namely when visited from parent, left child and right child.
        Space:     O(V): We allocate a stack of nodes to visit next.
        Leetcode:  35 ms runtime, 16.36 MB memory
        """

        order = []

        def visit(node):
            order.append(node.val)

        # A node can be visited next from: "parent", "left_child", "right_child"
        next_visited_from = dict()

        if root:
            next_visited_from[root] = "parent"
            stack = [root]
            while stack:
                node = stack[-1]
                match next_visited_from[node]:
                    case "parent":
                        # No child visited yet, so visit left child.
                        next_visited_from[node] = "left_child"
                        if node.left:
                            next_visited_from[node.left] = "parent"
                            stack.append(node.left)
                    case "left_child":
                        # Left child visited, so visit right child.
                        next_visited_from[node] = "right_child"
                        if node.right:
                            next_visited_from[node.right] = "parent"
                            stack.append(node.right)
                    case "right_child":
                        # Left and right children have been visited, so this is the last time we visit this node.
                        stack.pop()
                        # Post-order traversal.
                        visit(node)

        return order

    def iterative(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach:  Traverse tree iteratively.
        Idea:      Recursively traverse tree, visiting a node only after its children have been visited.
        Time:      O(2V) = O(V): We add every node to the stack twice, once when it may not be visited yet (since its children must be visited first) and once when it may be visited (after its children have been visited).
        Space:     O(V): While we add every node to the stack twice overall, every node will only be in the stack once at any time, since the second addition happens right after the first addition is popped.
        Leetcode:  41 ms runtime, 16.55 MB memory
        """

        order = []

        def visit(node):
            order.append(node.val)

        if root:
            stack = [(root, False)]
            while stack:
                (node, may_be_visited) = stack.pop()
                if node:
                    if may_be_visited:
                        visit(node)
                    else:
                        # Post-order: a node may only be visited after its children.
                        stack.append((node, True))
                        stack.append((node.right, False))
                        stack.append((node.left, False))

        return order
