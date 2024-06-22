#!/usr/bin/env python3

# Minimum Time To Collect All Apples In A Tree
#
# https://leetcode.com/problems/minimum-time-to-collect-all-apples-in-a-tree/
#
# Given an undirected tree consisting of n vertices numbered from 0 to n-1,
# which has some apples in their vertices. You spend 1 second to walk over one
# edge of the tree. Return the minimum time in seconds you have to spend to
# collect all apples in the tree, starting at vertex 0 and coming back to this
# vertex.
#
# The edges of the undirected tree are given in the array edges, where edges[i]
# = [ai, bi] means that exists an edge connecting the vertices ai and bi.
# Additionally, there is a boolean array hasApple, where hasApple[i] = true
# means that vertex i has an apple; otherwise, it does not have any apple.


from collections import defaultdict
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(n=7, edges=[[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], hasApple=[False, False, True, False, True, True, False]) == 8

        assert algo(n=7, edges=[[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], hasApple=[False, False, True, False, False, True, False]) == 6

        assert algo(n=7, edges=[[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], hasApple=[False, False, False, False, False, False, False]) == 0

        #   0
        #  1  2
        # 3
        assert algo(n=4, edges=[[0, 2], [0, 3], [1, 2]], hasApple=[False, True, False, False]) == 4

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dfs_hashset, solution.dfs_counter, solution.dfs_direct]:
        test_algo(algo)


class Solution:
    def dfs_hashset(self, n: int, edges: List[List[int]], hasApple: List[bool]) -> int:
        """
        Approach:  DFS, collecting results in hashset.
        Idea:      Recurse into each subtree, deciding which edges are necessary to keep based on whether an apple is somewhere deeper in the path.
        Time:      O(V + E): Every node and edge is visited once.
        Space:     O(E): If all leaves contain apples (worst-case), we'll add all edges to a hashset.
        Leetcode:  567 ms runtime, 63.74 MB memory
        """

        # Map each parent to its children.
        edge = defaultdict(lambda: [])
        for (a, b) in edges:
            # Insert both directions.
            edge[a].append(b)
            edge[b].append(a)

        required_edges = set()
        visited = set()

        def has_apple_in_path(node) -> bool:
            """Whether this node or any of its (recursive) children have apples."""
            children_have_apples = False
            visited.add(node)

            for child in edge[node]:
                if child not in visited:
                    if has_apple_in_path(child):
                        required_edges.add((node, child))
                        children_have_apples = True

            return children_have_apples or hasApple[node]

        root_node = 0
        has_apple_in_path(root_node)

        return len(required_edges) * 2

    def dfs_counter(self, n: int, edges: List[List[int]], hasApple: List[bool]) -> int:
        """
        Approach:  DFS, collecting results with a counter.
        Idea:      Recurse into each subtree, deciding which edges are necessary to keep based on whether an apple is somewhere deeper in the path.
        Time:      O(V + E): Every node and edge is visited once.
        Space:     O(1): We only maintain a counter that represents the required edges, which is correct since each edge is only visited once and can, therefore, only be added once.
        Leetcode:  526 ms runtime, 56.40 MB memory
        """

        # Map each parent to its children.
        edge = defaultdict(lambda: [])
        for (a, b) in edges:
            # Insert both directions.
            edge[a].append(b)
            edge[b].append(a)

        required_edges = 0
        visited = set()

        def find_edges_to_apples(node) -> bool:
            """Whether this node or any of its (recursive) children have apples."""
            nonlocal required_edges

            children_have_apples = False
            visited.add(node)

            for child in edge[node]:
                if child not in visited:
                    if find_edges_to_apples(child):
                        required_edges += 1
                        children_have_apples = True

            return children_have_apples or hasApple[node]

        root_node = 0
        find_edges_to_apples(root_node)

        return required_edges * 2

    def dfs_direct(self, n: int, edges: List[List[int]], hasApple: List[bool]) -> int:
        """
        Approach:  DFS, returning results directly.
        Idea:      Recurse into each subtree, deciding which edges are necessary to keep based on whether an apple is somewhere deeper in the path.
        Time:      O(V + E): Every node and edge is visited once.
        Space:     O(1): We only maintain a counter that represents the required edges, which is correct since each edge is only visited once and can, therefore, only be added once.
        Leetcode:  522 ms runtime, 56.29 MB memory
        """

        # Map each parent to its children.
        edge = defaultdict(lambda: [])
        for (a, b) in edges:
            # Insert both directions.
            edge[a].append(b)
            edge[b].append(a)

        visited = set()

        def find_edges_to_apples_from(node) -> int:
            """The number of edges used (any number of times) to reach all apples, from given node."""

            required_edges = 0
            visited.add(node)

            for child in edge[node]:
                if child not in visited:
                    match find_edges_to_apples_from(child):
                        case 0:
                            # No more apples are reached from the child, but check if the child may have an apple itself.
                            if hasApple[child]:
                                required_edges += 1
                        case required_edges_from_child:
                            if required_edges_from_child > 0:
                                # Add the number of edges to get from this node to child (1), and then from there to all the apples (required_edges_from_child).
                                required_edges += 1 + required_edges_from_child

            return required_edges

        root_node = 0
        return find_edges_to_apples_from(root_node) * 2
