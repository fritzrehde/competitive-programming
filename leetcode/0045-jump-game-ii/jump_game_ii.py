#!/usr/bin/env python3

# Jump Game Ii
#
# https://leetcode.com/problems/jump-game-ii/
#
# You are given a 0-indexed array of integers nums of length n. You are
# initially positioned at nums[0].
#
# Each element nums[i] represents the maximum length of a forward jump from
# index i. In other words, if you are at nums[i], you can jump to any nums[i +
# j] where:
#
# 0 <= j <= nums[i] and
# i + j < n
#
# Return the minimum number of jumps to reach nums[n - 1]. The test cases are
# generated such that you can reach nums[n - 1].


from collections import deque
from typing import Callable, Dict, List, TypeVar


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # Jump from index 0 to 1 (max 2), 1 to 4 (max 3).
        assert algo([2, 3, 1, 1, 4]) == 2

        # Jump from index 0 to 1 (max 2), 1 to 4 (max 3).
        assert algo([2, 3, 0, 1, 4]) == 2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dynamic_programming, solution.dynamic_programming_optimized, solution.graph_bfs, solution.dynamic_programming_more_optimized, solution.greedy_sliding_window]:
        test_algo(algo)


class Solution:
    def dynamic_programming(self, nums: List[int]) -> int:
        """
        Approach:  Dynamic programming.
        Idea:      Define the subproblem dp[i] as the minimum number of jumps to get to index i, which is calculated recursively.
        Time:      O(n^2): There are n subproblems, and to calculate each dp[i] we need to to check all indices j before i, of which there are at most n.
        Space:     O(n): The DP table is 1D and stores n elements.
        Leetcode:  10086 ms runtime, 17.1 MB memory
        """

        n = len(nums)

        # Subproblem: dp[i]: the minimum number of jumps to get to index i.
        dp = [None for _ in range(0, n)]

        # Order of computation: Increasing order of i, since dp[i] only depends on dp[j] with j < i in the recurrence.
        for i in range(0, n):
            if i == 0:
                # Base case: We start at index 0.
                dp[i] = 0
            else:
                # Recurrence: For all previous indices j from which we could jump to index i (if nums[j] >= (i-j)), get the one that can be reached in the least number of jumps (minimum dp[j]). Then, we do one from jump from j to i.
                dp[i] = 1 + min(dp[j] for j in range(0, i) if nums[j] >= (i - j))

        # Overall answer: We are precisely looking for the minimum number of jumps to get to index n-1.
        return dp[n - 1]

    def dynamic_programming_optimized(self, nums: List[int]) -> int:
        """
        Approach:  Dynamic programming optimized by precomputing values.
        Idea:      The subproblem is defined the same way as in the regular DP. However, we avoid recalculating all indices j from which we can jump to i for every i by doing this calculation once upfront.
        Time:      O(n^2): There are n subproblems, and to calculate each dp[i] we need to to check all indices j from which we can jump to i, of which there are at most n.
        Space:     O(n^2): The DP table is 1D and stores n elements (O(n)), and the jumpable list of lists stores at most n^2 elements if it is possible to jump from every index to every other index.
        Leetcode:  1857 ms runtime, 59.12 MB memory
        """

        n = len(nums)

        # jumpable[i] contains all indices from which we can jump to index i.
        jumpable = [[] for _ in range(0, n)]
        for jump_start in range(0, n):
            for jump_end in range(jump_start + 1, min(jump_start + nums[jump_start] + 1, n)):
                jumpable[jump_end].append(jump_start)

        # Subproblem: dp[i]: the minimum number of jumps to get to index i.
        dp = [None for _ in range(0, n)]

        # Order of computation: Increasing order of i, since dp[i] only depends on dp[j] with j < i in the recurrence.
        for i in range(0, n):
            if i == 0:
                # Base case: We start at index 0.
                dp[i] = 0
            else:
                # Recurrence: For all previous indices j from which we could jump to index i (if nums[j] >= (i-j)), get the one that can be reached in the least number of jumps (minimum dp[j]). Then, we do one from jump from j to i.
                dp[i] = 1 + min(dp[j] for j in jumpable[i])

        # Overall answer: We are precisely looking for the minimum number of jumps to get to index n-1.
        return dp[n - 1]

    def graph_bfs(self, nums: List[int]) -> int:
        """
        Approach:  BFS in a graph.
        Idea:      We can model being able to jump from one index i to another index j in the game as an unweighted edge from node i to node j in a graph. Then, the minimum number of jumps from index i to index n-1 corresponds to the shortest path from node i to node n-1, which we can find with a Breadth-First-Search (BFS).
        Time:      O(n^2): The graph will have exactly V = n nodes, and at most V = O(n^2) edges if it is possible to jump from every index to every other index (greater than the starting jump point). BFS has a time complexity of O(V + E) = O(n + n^2) = O(n^2).
        Space:     O(n^2): The graph stores every one of the O(n^2) edges once in an adjacency list.
        Leetcode:  1742 ms runtime, 209.58 MB memory
        """

        n = len(nums)

        # graph[i] contains all indices which we can jump to from index i, i.e. all neighbours of i.
        graph = [[] for _ in range(0, n)]
        for jump_start in range(0, n):
            for jump_end in range(jump_start + 1, min(jump_start + nums[jump_start] + 1, n)):
                graph[jump_start].append(jump_end)

        def bfs(start_node: int) -> list[int]:
            """
            Return the length of the shortest path to each node from the starting node.
            The graph is undirected and unweighted.
            """
            # The length of the shortest path from the starting node to every other node.
            distance = [None for _ in range(0, n)]

            # The nodes we have already visited and don't want to explore again.
            visited = set()
            # The nodes of which we still need to explore the neighbours.
            to_explore = deque()

            # The starting node has been visited and the length of shortest path from a node to itself is 0.
            visited.add(start_node)
            distance[start_node] = 0

            # We start off by exploring the neighbours of the starting node.
            to_explore.append(start_node)

            # Continue exploring while there are still nodes to explore.
            while to_explore:
                explored_node = to_explore.popleft()
                # Explore the neighbours of the node.
                for neighbour in graph[explored_node]:
                    # We only set the distance to a node the first time we reach that node (i.e. never again once we've visited it):
                    # When we first reach a node via BFS, we are reaching it by the shortest path possible due to the layer-by-layer nature of BFS.
                    if neighbour not in visited:
                        visited.add(neighbour)
                        distance[neighbour] = distance[explored_node] + 1
                        to_explore.append(neighbour)

            return distance

        # Find the shortest path from 0 to n-1 in the graph.
        starting_node = 0
        distances = bfs(starting_node)
        return distances[n - 1]

    def dynamic_programming_more_optimized(self, nums: List[int]) -> int:
        """
        Approach:  Dynamic programming optimized by precomputing less values.
        Idea:      The subproblem is defined the same way as in the regular DP. However, we avoid recalculating all indices j from which we can jump to i for every i by calculating the index farthest back from which we can still jump to index i.
        Time:      O(n^2): There are n subproblems, and to calculate each dp[i] we need to to check all indices j from which we can jump to i, of which there are at most n.
        Space:     O(n): The DP table is 1D and stores n elements (O(n)), and for each index i we also store the farthest previous index from which we can still jump to i (O(n)).
        Leetcode:  5347 ms runtime, 17.71 MB memory
        """

        def min_opt(a: int | None, b: int | None) -> int:
            """
            Return the minimum value of two integers where one of the two could be None.
            """
            if a is None:
                return b
            if b is None:
                return a
            return min(a, b)

        n = len(nums)

        # jumpable[i] contains the index farthest away from index i from which we can still jump to index i.
        farthest_jumpable = [None for _ in range(0, n)]
        for jump_start in range(0, n):
            farthest_jump_end = min(jump_start + nums[jump_start], n - 1)
            for i in range(jump_start, farthest_jump_end + 1):
                farthest_jumpable[i] = min_opt(farthest_jumpable[i], jump_start)

        # Subproblem: dp[i]: the minimum number of jumps to get to index i.
        dp = [None for _ in range(0, n)]

        # Order of computation: Increasing order of i, since dp[i] only depends on dp[j] with j < i in the recurrence.
        for i in range(0, n):
            if i == 0:
                # Base case: We start at index 0.
                dp[i] = 0
            else:
                # Recurrence: For all previous indices j from which we could jump to index i (if nums[j] >= (i-j)), get the one that can be reached in the least number of jumps (minimum dp[j]). Then, we do one from jump from j to i.
                dp[i] = 1 + min(dp[j] for j in range(farthest_jumpable[i], i))

        # Overall answer: We are precisely looking for the minimum number of jumps to get to index n-1.
        return dp[n - 1]

    def greedy_sliding_window(self, nums: List[int]) -> int:
        """
        Approach:  Greedy with sliding window.
        Idea:      We can maintain a sliding window that we must slide to the right i times. In each configuration, the ith sliding window contains all indices reachable only in at least i jumps. Then, we can pick the index inside our current sliding window from which jumping would get us the farthest (this farthest index being i), and use i as the upper bound of the next sliding window. Note that the sliding window changes in size, so one might argue the term "sliding window" is inappropriate.
        Time:      O(n): Given the ith sliding window from l to r, the (i+1)th sliding window is defined going from r+1 to some index j>i. Since the sliding window starts at the beginning of the array, and is moved right until it contains the last index, every index will have been in the sliding window exactly once. In other words, the sliding windows have sizes s_1, s_2, etc., where the sum of all s_i equals n. For each sliding window, we iterate over all elements in it, which is O(s_i). Therefore, the time complexity is the sum of all O(s_i), which is O(n).
        Space:     O(1): We store no additional data structures besides some indices/pointers.
        Leetcode:  97 ms runtime, 17.58 MB memory
        """

        n = len(nums)

        # The problem is undefined for n = 0.
        if n == 0:
            return 0

        # When the list contains only one element, the first and last indices are the same, so we need 0 jumps to get from the first to last index.
        if n == 1:
            return 0

        jumps = 0

        # The bounds (left and right inclusive) of the ith sliding window, where we could have reached any of the indices inside the current bounds of the sliding window in i jumps. Initially, by doing the first jump, we can reach any indices between the starting position and the farthest index we can jump to from the starting position.
        start_idx = 0
        l = start_idx
        r = nums[start_idx]
        jumps += 1

        # We haven't reached (i.e. haven't jumped to) the last index until our sliding window contains the last index.
        while r < (n - 1):
            # Consider all possible indices that we could jump to from indices within our sliding window, and take the largest possible index. This will now be the new upper (right) bound of the next sliding window position.
            next_r = max(i + nums[i] for i in range(l, r + 1))
            # The next sliding window should be disjoint with the previous sliding window, so start the next one at r+1.
            l, r = r + 1, next_r
            jumps += 1

        return jumps
