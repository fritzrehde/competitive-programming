#!/usr/bin/env python3

# Binary Tree Preorder Traversal
#
# https://leetcode.com/problems/binary-tree-preorder-traversal/
#
# Given the root of a binary tree, return the preorder traversal of its nodes'
# values.

from typing import List, Optional
from binary_tree import TreeNode


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo(None) == []

        assert algo(TreeNode(2)) == [2]

        assert algo(TreeNode(2, TreeNode(1), TreeNode(3))) == [2, 1, 3]

        assert algo(TreeNode(1, None, TreeNode(3, TreeNode(2), None))) == [1, 3, 2]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dfs_recursive]:
        test_algo(algo)


class Solution:
    def dfs_recursive(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach:  Recursive DFS.
        Idea:      For every parent node, first visit the parent node itself, then the left child, and then the right child.
        Time:      O(n): We visit every node in the tree exactly once.
        Space:     O(1): We don't store any additional data structure besides the output list.
        Leetcode:  43 ms runtime, 16.46 MB memory
        """

        def traverse(node: Optional[TreeNode]) -> List[int]:
            if node is None:
                return []
            else:
                return [node.val] + traverse(node.left) + traverse(node.right)

        return traverse(root)
