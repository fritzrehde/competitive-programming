#!/usr/bin/env python3

# Range Addition
#
# https://leetcode.com/problems/range-addition
#
# Assume you have an array of length n initialized with all 0's and are given k
# update operations.
#
# Each operation is represented as a triplet: [startIndex, endIndex, inc] which
# increments each element of subarray A[startIndex ... endIndex] (startIndex and
# endIndex inclusive) with inc.
#
# Return the modified array after all k operations were executed.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(length=5, updates=[[1, 3, 2], [2, 4, 3], [0, 2, -2]]) == [
            -2,
            0,
            3,
            5,
            3,
        ]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.optimized]:
        test_algo(algo)


class Solution:
    def brute_force(self, length: int, updates: List[List[int]]):
        """
        Approach:  Brute-force.
        Idea:      Apply each update all affected indices in the output array directly.
        Time:      O(m*n): Given an output array length of n and m updates, in the worst case each update requires incrementing all n elements in the array.
        Space:     O(1): No additional memory is used.
        Leetcode:  ? ms runtime, ? MB memory
        """

        arr = [0] * length

        for start_idx, end_idx, inc in updates:
            for i in range(start_idx, end_idx + 1):
                arr[i] += inc

        return arr

    def optimized(self, length: int, updates: List[List[int]]):
        """
        Approach:  Store increment diff.
        Idea:      Only save the idx at which an increment was introduced and when it was undone again.
        Time:      O(m+n): Given an output array length of n and m updates, exctracting increment introduction and removal indices takes O(m) overall, and then we can simply do one pass over output array and apply increment introductions and removals as we go (O(n)).
        Space:     O(m): For each update, we store the diff to be applied when that idx is reached.
        Leetcode:  ? ms runtime, ? MB memory
        """

        diff = [0] * length

        for start_idx, end_idx, inc in updates:
            diff[start_idx] += inc
            if end_idx + 1 < length:
                diff[end_idx + 1] -= inc

        arr = [0] * length
        diff_sum = 0

        for i in range(0, length):
            diff_sum += diff[i]
            arr[i] = diff_sum

        return arr
