#!/usr/bin/env python3

# Subtree of Another Tree
#
# https://leetcode.com/problems/subtree-of-another-tree
#
# Given the roots of two binary trees root and subRoot, return true if there is
# a subtree of root with the same structure and node values of subRoot and false
# otherwise.
# A subtree of a binary tree tree is a tree that consists of a node in tree and
# all of this node's descendants. The tree tree could also be considered as a
# subtree of itself.


from typing import List, Optional
from binary_tree import TreeNode


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                root=TreeNode(
                    3,
                    left=TreeNode(4, left=TreeNode(1), right=TreeNode(2)),
                    right=TreeNode(5),
                ),
                subRoot=TreeNode(4, left=TreeNode(1), right=TreeNode(2)),
            )
            == True
        )
        assert (
            algo(
                root=TreeNode(
                    3,
                    left=TreeNode(
                        4, left=TreeNode(1), right=TreeNode(2, left=TreeNode(0))
                    ),
                    right=TreeNode(5),
                ),
                subRoot=TreeNode(4, left=TreeNode(1), right=TreeNode(2)),
            )
            == False
        )
        assert (
            algo(
                root=TreeNode(
                    1,
                    left=TreeNode(2),
                    right=TreeNode(3),
                ),
                subRoot=TreeNode(
                    1,
                    left=TreeNode(2),
                ),
            )
            == False
        )
        assert (
            algo(
                root=TreeNode(
                    12,
                ),
                subRoot=TreeNode(
                    2,
                ),
            )
            == False
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.hash_tree,
        solution.preorder_traversal,
        solution.preorder_traversal_regex,
        solution.preorder_traversal_substring_search,
    ]:
        test_algo(algo)


class Solution:

    def brute_force(
        self, root: Optional[TreeNode], subRoot: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Brute-force.
        Idea:      For every node in root, check if the subtree rooted at that node is equal to the given subtree.
        Time:      O(n * m): Given a root with n nodes and a subtree with m nodes, for each node in the root, checking equality with the given subtree is O(m).
        Space:     O(1): No additional memory is used.
        Leetcode:  103 ms runtime, 16.74 MB memory
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

        def same_subtree(
            root: Optional[TreeNode], sub_root: Optional[TreeNode]
        ) -> bool:
            match (root, sub_root):
                case (None, _):
                    return same_tree(root, sub_root)
                case (some_root, _):
                    return (
                        same_tree(some_root, sub_root)
                        or same_subtree(some_root.left, sub_root)
                        or same_subtree(some_root.right, sub_root)
                    )
                case _:
                    raise Exception("unreachable")

        return same_subtree(root, subRoot)

    def hash_tree(
        self, root: Optional[TreeNode], subRoot: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Hash tree, or Merkle tree.
        Idea:      For every node in root, check if the subtree rooted at that node is equal to the given subtree. However, make checking equality of trees efficient by assigning every node in each tree a hash value, which is generated from a node's value plus the hashes of its children.
        Time:      O(n + m): Given a root with n nodes and a subtree with m nodes, first we traverse all nodes in each tree to set the hash values (O(n + m)), and then checking equality of trees is O(1), so we need to check if subtrees rooted at any node in root are equal to the given subtree (O(1) each).
        Space:     O(n + m): Each node in each tree gets an additional hash value/attribute.
        Leetcode:  70 ms runtime, 20.64 MB memory
        """

        from hashlib import sha256

        def hash(x: str):
            return sha256(x.encode()).hexdigest()

        def add_hash_to_nodes(node: Optional[TreeNode]) -> str:
            if node is None:
                return "#"
            else:
                node.hash = hash(
                    add_hash_to_nodes(node.left)
                    + str(node.val)
                    + add_hash_to_nodes(node.right)
                )
                return node.hash

        add_hash_to_nodes(root)
        add_hash_to_nodes(subRoot)

        def same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
            match (p, q):
                case (None, None):
                    return True
                case (None, _) | (_, None):
                    return False
                case (some_p, some_q):
                    return some_p.hash == some_q.hash
                case _:
                    raise Exception("unreachable")

        def same_subtree(
            root: Optional[TreeNode], sub_root: Optional[TreeNode]
        ) -> bool:
            match (root, sub_root):
                case (None, _):
                    return same_tree(root, sub_root)
                case (some_root, _):
                    return (
                        same_tree(some_root, sub_root)
                        or same_subtree(some_root.left, sub_root)
                        or same_subtree(some_root.right, sub_root)
                    )
                case _:
                    raise Exception("unreachable")

        return same_subtree(root, subRoot)

    def preorder_traversal(
        self, root: Optional[TreeNode], subRoot: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Serialize tree using pre-order traversal.
        Idea:      Serialize both tree using pre-order traversal, and then check if the subroot list is a sublist of the root list.
        Time:      O(n*m): Given the root has n nodes and the subroot has m nodes, the preorder traversals take (O(n+m)), and a naive sublist matching (with a sliding window) takes O(n*m).
        Space:     O(n+m): The serialized trees have sizes n and m.
        Leetcode:  74 ms runtime, 17.26 MB memory
        """

        from collections import deque
        import itertools

        def preorder_traversal(start: Optional[TreeNode], visit):
            def rec(node: Optional[TreeNode]):
                if node is not None:
                    visit(node)
                    rec(node.left)
                    rec(node.right)
                else:
                    visit(None)

            rec(start)

        root_order = []
        sub_root_order = []

        def visit_root(node: Optional[TreeNode]):
            root_order.append(node.val if node is not None else "#")

        def visit_sub_root(node: Optional[TreeNode]):
            sub_root_order.append(node.val if node is not None else "#")

        preorder_traversal(root, visit_root)
        preorder_traversal(subRoot, visit_sub_root)

        def sliding_window(iterable, n):
            it = iter(iterable)
            window = deque(itertools.islice(it, n - 1), maxlen=n)
            for x in it:
                window.append(x)
                yield tuple(window)

        def list_contains_sublist(list: List[int], sublist: List[int]) -> bool:
            return any(
                window == tuple(sublist)
                for window in sliding_window(list, len(sublist))
            )

        # Subroot is a subtree of root if its pre-order traversal list is
        # contained in root's pre-order traversal list.
        return list_contains_sublist(root_order, sub_root_order)

    def preorder_traversal_regex(
        self, root: Optional[TreeNode], subRoot: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Serialize tree using pre-order traversal, regex search.
        Idea:      Serialize both tree using pre-order traversal, and then check if the subroot list is a sublist of the root list.
        Time:      O(n*m): Given the root has n nodes and the subroot has m nodes, the preorder traversals take (O(n+m)), converting each to strings (O(n+m)), and check if subroot is sublist with regex (assumed O(n*m)).
        Space:     O(n+m): The serialized trees have sizes n and m.
        Leetcode:  87 ms runtime, 17.76 MB memory
        """

        import re

        def preorder_traversal(start: Optional[TreeNode], visit):
            def rec(node: Optional[TreeNode]):
                if node is not None:
                    visit(node)
                    rec(node.left)
                    rec(node.right)
                else:
                    visit(None)

            rec(start)

        root_order = []
        sub_root_order = []

        def visit_root(node: Optional[TreeNode]):
            root_order.append(node.val if node is not None else "#")

        def visit_sub_root(node: Optional[TreeNode]):
            sub_root_order.append(node.val if node is not None else "#")

        preorder_traversal(root, visit_root)
        preorder_traversal(subRoot, visit_sub_root)

        root_order_str = ",".join(map(str, root_order))
        sub_root_order_str = ",".join(map(str, sub_root_order))

        # Subroot is a subtree of root if its pre-order traversal list is
        # contained in root's pre-order traversal list.
        return (
            re.search(rf"(^|,){sub_root_order_str}($|,)", root_order_str)
            is not None
        )
        # return sub_root_order_str in root_order_str

    def preorder_traversal_substring_search(
        self, root: Optional[TreeNode], subRoot: Optional[TreeNode]
    ) -> bool:
        """
        Approach:  Serialize tree using pre-order traversal, substring search.
        Idea:      Serialize both tree using pre-order traversal, and then check if the subroot list is a sublist of the root list.
        Time:      O(n+m): Given the root has n nodes and the subroot has m nodes, the preorder traversals take (O(n+m)), converting each to strings (O(n+m)), and check if subroot is substring with "in" (assumed O(n+m), similar to KMP).
        Space:     O(n+m): The serialized trees have sizes n and m.
        Leetcode:  62 ms runtime, 17.36 MB memory
        """

        def preorder_traversal(start: Optional[TreeNode], visit):
            def rec(node: Optional[TreeNode]):
                if node is not None:
                    visit(node)
                    rec(node.left)
                    rec(node.right)
                else:
                    visit(None)

            rec(start)

        root_order = []
        sub_root_order = []

        def visit_root(node: Optional[TreeNode]):
            root_order.extend(["^", node.val] if node is not None else ["#"])

        def visit_sub_root(node: Optional[TreeNode]):
            sub_root_order.extend(
                ["^", node.val] if node is not None else ["#"]
            )

        preorder_traversal(root, visit_root)
        preorder_traversal(subRoot, visit_sub_root)

        root_order_str = ",".join(map(str, root_order))
        sub_root_order_str = ",".join(map(str, sub_root_order))

        # Subroot is a subtree of root if its pre-order traversal list is
        # contained in root's pre-order traversal list.
        return sub_root_order_str in root_order_str
