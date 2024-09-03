#!/usr/bin/env python3

# Next Greater Element II
#
# https://leetcode.com/problems/next-greater-element-ii
#
# Given a circular integer array nums (i.e., the next element of
# nums[nums.length - 1] is nums[0]), return the next greater number for every
# element in nums.
# The next greater number of a number x is the first greater number to its
# traversing-order next in the array, which means you could search circularly to
# find its next greater number. If it doesn't exist, return -1 for this number.


from collections import defaultdict
from itertools import chain
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 2, 1]) == [2, -1, 2]
        assert algo(nums=[1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.precalc]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      To calculate each answer[i], search [i+1,n) and [0,i) for a greater number.
        Time:      O(n^2): There are n answer[i] values to calculate, and in each we search a range of at most size O(2n) ([i+1,n) size O(n) and [0,i) size O(n)) for a greater number.
        Space:     O(1): No additional memory is used.
        Leetcode:  1499 ms runtime, 18.28 MB memory
        """

        n = len(nums)

        def next_greater(from_idx: int) -> int:
            for i in chain(range(from_idx + 1, n), range(0, from_idx)):
                if nums[i] > nums[from_idx]:
                    return nums[i]
            return -1

        return [next_greater(i) for i in range(0, n)]

    def precalc(self, nums: List[int]) -> List[int]:
        """
        Approach:  Pre-calculate next greater numbers.
        Idea:      Pre-calculate the next greater number for every number.
        Time:      O(n): Make two passes: Find the next greater numbers that occur after numbers using a montonic stack storing a decreasing subsequence. In a second pass, iterate over all numbers again, and if a number doesn't have a next greater number yet, assign it one that comes before the number itself.
        Space:     O(n): We maintain a decreasing subsequence stack of at most size n, and a hashmap mapping each index to the next greater element.
        Leetcode:  156 ms runtime, 18.46 MB memory
        """

        n = len(nums)

        next_greater = defaultdict(lambda: -1)
        decreasing_subseq: List = []

        for i in range(0, n):
            while decreasing_subseq and nums[i] > nums[decreasing_subseq[-1]]:
                j = decreasing_subseq.pop()
                next_greater[j] = nums[i]
            decreasing_subseq.append(i)

        for i in range(0, n):
            while decreasing_subseq and nums[i] > nums[decreasing_subseq[-1]]:
                j = decreasing_subseq.pop()
                if j not in next_greater:
                    next_greater[j] = nums[i]
            decreasing_subseq.append(i)

        return [next_greater[i] for i in range(0, n)]
