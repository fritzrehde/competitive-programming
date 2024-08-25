#!/usr/bin/env python3

# Longest Increasing Subsequence
#
# https://leetcode.com/problems/longest-increasing-subsequence
#
# Given an integer array nums, return the length of the longest strictly
# increasing subsequence.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[10, 9, 2, 5, 3, 7, 101, 18]) == 4
        assert algo(nums=[0, 1, 0, 3, 2, 3]) == 4
        assert algo(nums=[7, 7, 7, 7, 7, 7, 7]) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.dynamic_programming,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Generate all possible subsequences, keep only the increasing ones, and return the length of the longest subsequence.
        Time:      O(n 2^n): There are 2^n possible subsequences (for each element in the subsequence, we can either include or exclude it), and for each we check if it is increasing (O(n) each).
        Space:     O(2^n): We store the 2^n possible subsequences as lists.
        Leetcode:  Memory Limit Exceeded.
        """

        from collections import deque
        import itertools

        def sliding_window(iterable, n):
            it = iter(iterable)
            window = deque(itertools.islice(it, n - 1), maxlen=n)
            for x in it:
                window.append(x)
                yield tuple(window)

        n = len(nums)

        def all_subsequences(sequence: List[int]) -> List[List[int]]:
            subsequences = []

            def recurse(i: int, subsequence: List[int]):
                if i == n:
                    subsequences.append(subsequence.copy())
                else:
                    # Include ith element.
                    recurse(i + 1, subsequence + [sequence[i]])
                    # Exclude ith element.
                    recurse(i + 1, subsequence.copy())

            recurse(0, subsequence=[])
            return subsequences

        def is_increasing_sequence(sequence) -> bool:
            return all(
                map(lambda pair: pair[0] < pair[1], sliding_window(sequence, 2))
            )

        return max(
            map(len, filter(is_increasing_sequence, all_subsequences(nums))),
            default=0,
        )

    def dynamic_programming(self, nums: List[int]) -> int:
        """
        Approach:  Dynamic Programming.
        Idea:      Define the subproblem dp[i] as the LIS ending at and including index i, so the recurrence is defined as any dp[j] with j < i where nums[i] forms a next element of the sequence.
        Time:      O(n^2): There are n subproblems, each of which take O(n) to solve.
        Space:     O(n): The DP table stores the results of n subproblems.
        Leetcode:  1141 ms runtime, 16.92 MB memory
        """

        n = len(nums)

        # Subproblem: dp[i] represents the length of the longest strictly
        # increasing subsequence ending at and including index i (0-based).
        dp = [-1] * (n)

        # Order of computation: dp[i] only depends on dp[j] with j < i, so
        # increasing order of i.
        for i in range(0, n):
            if i == 0:
                # Base case: The longest strictly increasing subsequence is
                # [nums[0]].
                dp[i] = 1
            else:
                # Recurrence:
                dp[i] = 1 + max(
                    (dp[j] for j in range(0, i) if nums[j] < nums[i]), default=0
                )

        # Final result:
        return max(dp[i] for i in range(0, n))
