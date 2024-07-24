#!/usr/bin/env python3

# Insert Into A Binary Search Tree
#
# https://leetcode.com/problems/insert-into-a-binary-search-tree/
#
# You are given the root node of a binary search tree (BST) and a value to
# insert into the tree. Return the root node of the BST after the insertion. It
# is guaranteed that the new value does not exist in the original BST.
#
# Notice that there may exist multiple valid ways for the insertion, as long as
# the tree remains a BST after insertion. You can return any of them.

from typing import List, Optional
from binary_tree import TreeNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def post_order_traversal(root: Optional[TreeNode]) -> List[int]:
        order = []
        def visit(node): order.append(node.val)

        def traverse(node):
            if node:
                traverse(node.left)
                traverse(node.right)
                visit(node)

        traverse(root)
        return order

    def test_algo(algo):
        #     4
        #   2   7
        # 1   3
        # into:
        #       4
        #   2      7
        # 1   3  5
        assert post_order_traversal(algo(root=TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7)), val=5)) == [1, 3, 2, 5, 7, 4]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.recursive, solution.iterative]:
        test_algo(algo)


class Solution:
    def recursive(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Approach:  Recursive.
        Idea:      If the new value is smaller than current node's value, insert in left subtree, if larger insert in right subtree.
        Time:      O(log n): If the BST is balanced, we visit every level once, and height is log n.
        Space:     O(1): No additional memory is allocated.
        Leetcode:  87 ms runtime, 18.69 MB memory
        """

        def insert(node: Optional[TreeNode], val: int) -> Optional[TreeNode]:
            if node is None:
                new_node = TreeNode(val)
                return new_node
            else:
                if val == node.val:
                    raise Exception(f"node with value {val} already exists in BST")
                elif val < node.val:
                    # Insert new node in left subtree.
                    node.left = insert(node.left, val)
                else:
                    # Insert new node in right subtree.
                    node.right = insert(node.right, val)

                return node

        return insert(root, val)

    def iterative(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """
        Approach:  Iterative.
        Idea:      If the new value is smaller than current node's value, insert in left subtree, if larger insert in right subtree.
        Time:      O(log n): If the BST is balanced, we visit every level once, and height is log n.
        Space:     O(1): No additional memory is allocated.
        Leetcode:  86 ms runtime, 18.87 MB memory
        """

        # TreeNode **cur = &root;
        # while( *cur )
        # 	cur = (val > (*cur)->val) ? &(*cur)->right : &(*cur)->left;
        # *cur = new TreeNode(val);
        # return root;

        # Trying to mimic the power of C/C++ pointer magic, demonstrated above, in python:

        if not root:
            return TreeNode(val)
        else:
            curr = root

            while curr:
                if val == curr.val:
                    raise Exception(f"node with value {val} already exists in BST")
                if val < curr.val:
                    # Traverse into left subtree.
                    if not curr.left:
                        curr.left = TreeNode(val)
                        break
                    curr = curr.left
                else:
                    # Traverse into right subtree.
                    if not curr.right:
                        curr.right = TreeNode(val)
                        break
                    curr = curr.right

            return root
