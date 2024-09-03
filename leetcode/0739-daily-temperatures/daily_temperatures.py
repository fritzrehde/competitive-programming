#!/usr/bin/env python3

# Daily Temperatures
#
# https://leetcode.com/problems/daily-temperatures
#
# Given an array of integers temperatures represents the daily temperatures,
# return an array answer such that answer[i] is the number of days you have to
# wait after the ith day to get a warmer temperature. If there is no future day
# for which this is possible, keep answer[i] == 0 instead.


from collections import defaultdict
from typing import List, Optional


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(temperatures=[73, 74, 75, 71, 69, 72, 76, 73]) == [
            1,
            1,
            4,
            2,
            1,
            1,
            0,
            0,
        ]
        assert algo(temperatures=[30, 40, 50, 60]) == [1, 1, 1, 0]
        assert algo(temperatures=[30, 60, 90]) == [1, 1, 0]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.monotonic_stack,
        solution.monotonic_stack_direct,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, temperatures: List[int]) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      Calculate answer[i] as (i-j), where j is the idx of the next warmer (larger) temperature.
        Time:      O(n^2): For each of the n i's, calculate j in O(n).
        Space:     O(1): No additional memory is used.
        Leetcode:  Time Limit Exceeded.
        """

        n = len(temperatures)

        def next_warmer_idx(from_idx: int) -> Optional[int]:
            for j in range(from_idx + 1, n):
                if temperatures[j] > temperatures[from_idx]:
                    return j
            return None

        def answers():
            for i in range(0, n):
                if (j := next_warmer_idx(i)) is not None:
                    yield j - i
                else:
                    yield 0

        return list(answers())

    def monotonic_stack(self, temperatures: List[int]) -> List[int]:
        """
        Approach:  Pre-calculate next warmer indices using monotonic stack.
        Idea:      Calculate answer[i] as (i-j), where j is the idx of the next warmer (larger) temperature.
        Time:      O(n): Pre-calculate next warmer indices by maintaining a monotonic decreasing subsequence, and once we find a larger element i, all elements smaller than i have i as their next warmer/larger element. Every temperature is pushed and popped from the stack exactly once.
        Space:     O(n): The stack contains at most n elements. Furthermore, we store the next warmer index in a hashmap comprising at most n elements.
        Leetcode:  957 ms runtime, 39.78 MB memory
        """

        n = len(temperatures)

        next_warmer_idx = dict()
        decreasing_subseq: List = []
        for i, temp_i in enumerate(temperatures):
            # If temp_i breaks the decreasing subsequence, then the next warmer
            # temp for all temp_j in the decreasing subsequence that are smaller
            # than temp_i is temp_i.
            while len(decreasing_subseq) > 0:
                temp_j, j = decreasing_subseq[-1]
                if temp_i > temp_j:
                    decreasing_subseq.pop()
                    next_warmer_idx[j] = i
                else:
                    break

            # Continue decreasing subsequence.
            decreasing_subseq.append((temp_i, i))

        def answers():
            for i in range(0, n):
                if (j := next_warmer_idx.get(i, None)) is not None:
                    yield j - i
                else:
                    yield 0

        return list(answers())

    def monotonic_stack_direct(self, temperatures: List[int]) -> List[int]:
        """
        Approach:  Pre-calculate next warmer indices using monotonic stack.
        Idea:      Calculate answer[i] as (i-j), where j is the idx of the next warmer (larger) temperature.
        Time:      O(n): Pre-calculate next warmer indices by maintaining a monotonic decreasing subsequence, and once we find a larger element i, all elements smaller than i have i as their next warmer/larger element. Every temperature is pushed and popped from the stack exactly once.
        Space:     O(n): The stack contains at most n elements.
        Leetcode:  904 ms runtime, 29.66 MB memory
        """

        n = len(temperatures)

        answers = [0] * n
        decreasing_subseq: List = []
        for i, temp_i in enumerate(temperatures):
            # If temp_i breaks the decreasing subsequence, then the next warmer
            # temp for all temp_j in the decreasing subsequence that are smaller
            # than temp_i is temp_i.
            while (
                len(decreasing_subseq) > 0
                and temp_i > temperatures[decreasing_subseq[-1]]
            ):
                next_warmer_idx = i
                from_idx = decreasing_subseq.pop()
                answers[from_idx] = next_warmer_idx - from_idx

            # Continue decreasing subsequence.
            decreasing_subseq.append(i)

        return answers
