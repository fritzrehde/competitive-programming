#!/usr/bin/env python3

# Delete Node In A Bst
#
# https://leetcode.com/problems/delete-node-in-a-bst/
#
# Given a root node reference of a BST and a key, delete the node with the given
# key in the BST. Return the root node reference (possibly updated) of the BST.
#
# Basically, the deletion can be divided into two stages:
#
# Search for a node to remove.
# If the node is found, delete the node.


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
        #      5
        #   3     6
        # 2   4     7
        # into:
        #     5
        #   4   6
        # 2       7
        assert post_order_traversal(algo(root=TreeNode(5, TreeNode(3, TreeNode(2), TreeNode(4)), TreeNode(6, None, TreeNode(7))), key=3)) == [2, 4, 7, 6, 5]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.recursive]:
        test_algo(algo)


class Solution:
    def recursive(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Approach:  Recursive.
        Idea:      Find the node with key, and delete in by replacing it with the leftmost node in the right subtree if it has two children.
        Time:      O(log n): Assuming the tree is balanced, finding the node takes O(log n) with binary search, finding the leftmost in the right subtree takes O(log n), and deleting the replacement node in the right subtree, which was moved into deleted node's spot, takes O(log n).
        Space:     O(1): No additional memory is used.
        Leetcode:  58 ms runtime, 19.95 MB memory
        """

        def get_leftmost_node(root: TreeNode) -> TreeNode:
            curr = root
            while curr.left:
                curr = curr.left
            return curr

        # Find node to delete.
        def delete(node: Optional[TreeNode], key: int) -> Optional[TreeNode]:
            if not node:
                # The to-be-deleted node was never found.
                return node
            else:
                if key == node.val:
                    # Found node to delete.
                    node_to_delete = node
                    if not node_to_delete.left and not node_to_delete.right:
                        # No children: no node needs to take its place.
                        return None

                    if node_to_delete.left and not node_to_delete.right:
                        # Only left child: left child takes its place.
                        return node_to_delete.left

                    if not node_to_delete.left and node_to_delete.right:
                        # Only right child: right child takes its place.
                        return node_to_delete.right

                    elif node_to_delete.left and node_to_delete.right:
                        # Two children:
                        # - in-order successor: left-most node in right subtree OR
                        # - in-order predecessor: right-most node in left subtree
                        replacement = get_leftmost_node(node_to_delete.right)
                        # Replace deleted node('s value) with replacement node.
                        node_to_delete.val = replacement.val
                        # Since replacement node is now in the place of deleted node, the original replacement node needs to be deleted.
                        node_to_delete.right = delete(node_to_delete.right, replacement.val)
                        return node_to_delete

                elif key < node.val:
                    node.left = delete(node.left, key)
                else:
                    node.right = delete(node.right, key)

                return node

        return delete(root, key)
