#!/usr/bin/env python3

# Binary Tree Inorder Traversal
#
# https://leetcode.com/problems/binary-tree-inorder-traversal/
#
# Given the root of a binary tree, return the inorder traversal of its nodes'
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

        assert algo(TreeNode(2, TreeNode(1), TreeNode(3))) == [1, 2, 3]

        assert algo(TreeNode(1, None, TreeNode(3, TreeNode(2), None))) == [1, 2, 3]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dfs_recursive, solution.dfs_iterative]:
        test_algo(algo)


class Solution:
    def dfs_recursive(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach:  Recursive DFS.
        Idea:      For every parent node, first visit the left child, then visit the parent node itself, then visit the right node, recursively.
        Time:      O(n): We visit every node in the tree exactly once.
        Space:     O(1): We don't store any additional data structure besides the output list.
        Leetcode:  31 ms runtime, 16.56 MB memory
        """

        def traverse(node: Optional[TreeNode]) -> List[int]:
            if node is None:
                return []
            else:
                return traverse(node.left) + [node.val] + traverse(node.right)

        return traverse(root)

    def dfs_iterative(self, root: Optional[TreeNode]) -> List[int]:
        """
        Approach:  Iterative DFS.
        Idea:      Same as recursive approach.
        Time:      O(n): From each node, we traverse to the deepest, left-most node, visit it, and then "recurse" into its right node.
        Space:     O(n): We keep a stack of nodes we still need to explore around, and every node is part of this stack exactly once (so gets pushed to and popped from the stack exactly once).
        Leetcode:  43 ms runtime, 16.46 MB memory
        """

        inorder = []

        # All nodes we still need to explore.
        to_explore = []

        # The current node we are exploring.
        cur = root

        while True:
            # Traverse to deepest, left-most node relative to current node.
            while cur:
                to_explore.append(cur)
                cur = cur.left

            # Break if there are no more nodes to explore.
            if not to_explore:
                break

            # Visit deepest, left-most.
            deepest_left = to_explore.pop()
            inorder.append(deepest_left.val)

            # The deepest left-most node definitely doesn't have another left child (since it's the deepest), but it might have a right child.
            if deepest_left.right:
                cur = deepest_left.right
            else:
                cur = None

        return inorder
