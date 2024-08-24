#!/usr/bin/env python3

# Clone Graph
#
# https://leetcode.com/problems/clone-graph
#
# Given a reference of a node in a connected undirected graph.
# Return a deep copy (clone) of the graph.
# Each node in the graph contains a value (int) and a list (List[Node]) of its
# neighbors.
#
# class Node {
#     public int val;
#     public List<Node> neighbors;
# }


from typing import Dict, Optional, Set
from graph import Node


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        pass
        # assert algo(adjList = [[2,4],[1,3],[2,4],[1,3]]) == [[2,4],[1,3],[2,4],[1,3]]
        # assert algo(adjList = [[]]) == [[]]
        # assert algo(adjList = []) == []

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def bfs(self, node: Optional[Node]) -> Optional[Node]:
        """
        Approach:  BFS.
        Idea:      Use breadth-first-search.
        Time:      O(V + E): BFS runs in O(V + E), where V is the number of nodes and E the number of edges.
        Space:     O(V): All nodes in V will be in the queue at some point.
        Leetcode:  31 ms runtime, 16.95 MB memory
        """

        from collections import deque

        if node is None:
            return None
        else:
            val_to_clones: Dict[int, Node] = dict()

            def clone_node(node: Node) -> Node:
                return Node(node.val, neighbors=[])

            def bfs(start):
                unvisited = deque()

                val_to_clones[start.val] = clone_node(start)
                unvisited.append(start)

                while unvisited:
                    curr = unvisited.popleft()

                    for neighbor in curr.neighbors:
                        if neighbor.val not in val_to_clones:
                            val_to_clones[neighbor.val] = clone_node(neighbor)
                            unvisited.append(neighbor)

                        val_to_clones[curr.val].neighbors.append(
                            val_to_clones[neighbor.val]
                        )

            bfs(start=node)
            return val_to_clones[node.val]

    def dfs(self, node: Optional[Node]) -> Optional[Node]:
        """
        Approach:  DFS.
        Idea:      Use depth-first-search.
        Time:      O(V + E): DFS runs in O(V + E), where V is the number of nodes and E the number of edges.
        Space:     O(1): No additional memory is used (besides O(V) on recursion stack).
        Leetcode:  49 ms runtime, 16.92 MB memory
        """

        if node is None:
            return None
        else:
            val_to_clones: Dict[int, Node] = dict()

            def clone_node(node: Node) -> Node:
                return Node(node.val, neighbors=[])

            def dfs(curr):
                val_to_clones[curr.val] = clone_node(curr)

                for neighbor in curr.neighbors:
                    if neighbor.val not in val_to_clones:
                        dfs(neighbor)

                    val_to_clones[curr.val].neighbors.append(
                        val_to_clones[neighbor.val]
                    )

            dfs(node)
            return val_to_clones[node.val]
