#!/usr/bin/env python3

# Single Number
#
# https://leetcode.com/problems/single-number
#
# Given a non-empty array of integers nums, every element appears twice except
# for one. Find that single one.
# You must implement a solution with a linear runtime complexity and use only
# constant extra space.


from collections import defaultdict
from functools import reduce
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[2, 2, 1]) == 1
        assert algo(nums=[4, 1, 2, 1, 2]) == 4
        assert algo(nums=[1]) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.xor]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Build a hashmap mapping each number to its number of occurences, and return number with count 1.
        Time:      O(n): Creating the number count hashmap takes O(n), and finding the number with count 1 takes O(1).
        Space:     O(n): We store at most n elements in the number count hashmap.
        Leetcode:  114 ms runtime, 19.28 MB memory
        """

        num_count = defaultdict(lambda: 0)
        for num in nums:
            num_count[num] += 1

        return next(num for (num, count) in num_count.items() if count != 2)

    def xor(self, nums: List[int]) -> int:
        """
        Approach:  XOR operator.
        Idea:      If we aggregate all number with the XOR operator, we are left with the number that occurs an odd number of times.
        Time:      O(n): We apply the XOR operator n times, taking O(1) each time.
        Space:     O(1): No additional memory is used.
        Leetcode:  109 ms runtime, 19.17 MB memory
        """

        # XOR properties:
        # A ^ 0 = A
        # A ^ A = 0

        # Given that X is the number that occurs an odd number of times, if we
        # apply the XOR operator to all numbers, we get:
        # A ^ B ^ C ^ ... ^ X ^ A ^ B ^ C ^ ...
        # = (A ^ A) ^ (B ^ B) ^ (C ^ C) ^ ... ^ X
        # = 0 ^ 0 ^ 0 ^ ... ^ X
        # = 0 ^ X
        # = X
        return reduce(lambda a, b: a ^ b, nums)
