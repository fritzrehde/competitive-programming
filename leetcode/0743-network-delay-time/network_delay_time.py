#!/usr/bin/env python3

# Network Delay Time
#
# https://leetcode.com/problems/network-delay-time/
#
# You are given a network of n nodes, labeled from 1 to n. You are also given
# times, a list of travel times as directed edges times[i] = (ui, vi, wi), where
# ui is the source node, vi is the target node, and wi is the time it takes for
# a signal to travel from source to target.
#
# We will send a signal from a given node k. Return the minimum time it takes
# for all the n nodes to receive the signal. If it is impossible for all the n
# nodes to receive the signal, return -1.


from collections import defaultdict
import heapq
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(times=[[2, 1, 1], [2, 3, 1], [3, 4, 1]], n=4, k=2) == 2

        assert algo(times=[[1, 2, 1]], n=2, k=1) == 1

        assert algo(times=[[1, 2, 1]], n=2, k=2) == -1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dijkstra, solution.dijkstra2]:
        test_algo(algo)


class Solution:
    def dijkstra(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach:  Dijkstra.
        Idea:      Find the shortest path from the source node k to each other node with dijkstra, and return the distance to the furthest node (they will receive the signal last). If some node couldn't be reached, return -1.
        Time:      O(V log V): We pop every node (of which there are V) from the priority queue once (each taking O(log V) due to heap).
        Space:     O(E): We store a hashmap mapping each node to all of its outgoing edges.
        Leetcode:  425 ms runtime, 18.46 MB memory
        """

        class MinHeap:
            def __init__(self, initial):
                self.min_heap = initial
                heapq.heapify(initial)
                # All values that have been popped. The same node can only be popped exactly once.
                self.popped = set()

            def pop_min(self):
                while self.min_heap:
                    (_priority, element) = heapq.heappop(self.min_heap)
                    if element in self.popped:
                        # We ignore nodes that were already popped before.
                        continue
                    else:
                        self.popped.add(element)
                        return element

            def push(self, priority, element):
                heapq.heappush(self.min_heap, (priority, element))

            def improve_priority(self, new_priority, element):
                """Update the priority of an element already in the heap to a **better** value."""
                # We add the element again with the higher priority, meaning it will definitely get popped first.
                self.push(new_priority, element)

            def is_empty(self):
                # If all the remaining elements have already been popped once, we consider the heap empty.
                return all(node in self.popped for (_priority, node) in self.min_heap)

        from dataclasses import dataclass

        @dataclass(frozen=True, order=True)
        class Edge:
            from_node: int
            to_node: int
            edge_weight: int

        nodes = [node for node in range(1, n + 1)]

        # Map each node to all of its outgoing edges.
        neighbours = defaultdict(lambda: [])
        for (from_node, to_node, edge_weight) in times:
            neighbours[from_node].append(Edge(from_node, to_node, edge_weight))

        def shortest_distance_to_all_nodes(source: int) -> dict[int, int]:
            """Dijkstra."""
            # The shortest distances from the source to all nodes.
            distance = {node: float("inf") for node in nodes}
            distance[source] = 0

            # Min heap priority queue, initially filled with all nodes.
            queue = MinHeap([(distance[node], node) for node in nodes])
            # Initially, all nodes are in the queue.
            in_queue = set(node for node in nodes)

            while not queue.is_empty():
                # Node with minimum distance to source.
                cur = queue.pop_min()
                in_queue.remove(cur)

                for edge_to_neighbour in neighbours[cur]:
                    if edge_to_neighbour.to_node in in_queue:
                        distance_through_cur = distance[cur] + edge_to_neighbour.edge_weight
                        if distance_through_cur < distance[edge_to_neighbour.to_node]:
                            distance[edge_to_neighbour.to_node] = distance_through_cur
                            queue.improve_priority(distance_through_cur, edge_to_neighbour.to_node)

            return distance

        furthest_distance = max(shortest_path_to_node for (_node, shortest_path_to_node) in shortest_distance_to_all_nodes(k).items())
        if furthest_distance == float('inf'):
            # Some node was not reachable from k and, therefore, has distance infinity.
            return -1
        else:
            return furthest_distance

    def dijkstra2(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Approach:  Dijkstra.
        Idea:      Find the shortest path from the source node k to each other node with dijkstra, and return the distance to the furthest node (they will receive the signal last). If some node couldn't be reached, return -1.
        Time:      O(V log V): We pop every node (of which there are V) from the priority queue once (each taking O(log V) due to heap).
        Space:     O(E): We store a hashmap mapping each node to all of its outgoing edges.
        Leetcode:  415 ms runtime, 18.74 MB memory
        """

        class MinHeap:
            def __init__(self, initial):
                self.min_heap = initial
                heapq.heapify(initial)
                # All values that have been popped. The same node can only be popped exactly once.
                self.popped = set()

            def pop_min(self):
                while self.min_heap:
                    (_priority, element) = heapq.heappop(self.min_heap)
                    if element in self.popped:
                        # We ignore nodes that were already popped before.
                        continue
                    else:
                        self.popped.add(element)
                        return element

            def push(self, priority, element):
                heapq.heappush(self.min_heap, (priority, element))

            def improve_priority(self, new_priority, element):
                """Update the priority of an element already in the heap to a **better** value."""
                # We add the element again with the higher priority, meaning it will definitely get popped first.
                self.push(new_priority, element)

            def is_empty(self):
                # If all the remaining elements have already been popped once, we consider the heap empty.
                return all(node in self.popped for (_priority, node) in self.min_heap)

        from dataclasses import dataclass

        @dataclass(frozen=True, order=True)
        class Edge:
            from_node: int
            to_node: int
            edge_weight: int

        nodes = [node for node in range(1, n + 1)]

        # Map each node to all of its outgoing edges.
        neighbours = defaultdict(lambda: [])
        for (from_node, to_node, edge_weight) in times:
            neighbours[from_node].append(Edge(from_node, to_node, edge_weight))

        def shortest_distance_to_all_nodes(source: int) -> dict[int, int]:
            """Dijkstra."""
            # The shortest distances from the source to all nodes.
            distance = {node: float("inf") for node in nodes}
            distance[source] = 0

            # Min heap priority queue, initially filled with just the starting node.
            queue = MinHeap([(distance[source], source)])

            while not queue.is_empty():
                # Node with minimum distance to source.
                cur = queue.pop_min()

                for edge_to_neighbour in neighbours[cur]:
                    distance_through_cur = distance[cur] + edge_to_neighbour.edge_weight
                    if distance_through_cur < distance[edge_to_neighbour.to_node]:
                        distance[edge_to_neighbour.to_node] = distance_through_cur
                        queue.push(distance_through_cur, edge_to_neighbour.to_node)

            return distance

        furthest_distance = max(shortest_path_to_node for (_node, shortest_path_to_node) in shortest_distance_to_all_nodes(k).items())
        if furthest_distance == float('inf'):
            # Some node was not reachable from k and, therefore, has distance infinity.
            return -1
        else:
            return furthest_distance
