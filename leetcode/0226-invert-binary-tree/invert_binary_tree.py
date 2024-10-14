#!/usr/bin/env python3

# Invert Binary Tree
#
# https://leetcode.com/problems/invert-binary-tree
#
# Given the root of a binary tree, invert the tree, and return its root.


from collections import deque
from typing import Optional
from binary_tree import TreeNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # assert algo(root=[4, 2, 7, 1, 3, 6, 9]) == [4, 7, 2, 9, 6, 3, 1]
        # assert algo(root=[2, 1, 3]) == [2, 3, 1]
        # assert algo(root=[]) == []
        pass

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.recursive, solution.iterative]:
        test_algo(algo)


class Solution:
    def recursive(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  30 ms runtime, 16.49 MB memory
        """

        # DFS
        def invert(node: Optional[TreeNode]):
            if node is None:
                return

            invert(node.left)
            invert(node.right)
            # Swap.
            node.left, node.right = node.right, node.left

        invert(root)
        return root

    def iterative(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  37 ms runtime, 16.51 MB memory
        """

        def bfs(start):
            visited = set()
            unvisited = deque()
            unvisited.append(start)

            while unvisited:
                node = unvisited.pop()
                if node is None:
                    continue

                # Swap.
                node.left, node.right = node.right, node.left

                for child in [node.left, node.right]:
                    if child not in visited:
                        visited.add(child)
                        unvisited.append(child)

        bfs(root)
        return root
