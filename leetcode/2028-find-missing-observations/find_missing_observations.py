#!/usr/bin/env python3

# Find Missing Observations
#
# https://leetcode.com/problems/find-missing-observations
#
# You have observations of n + m 6-sided dice rolls with each face numbered from
# 1 to 6. n of the observations went missing, and you only have the observations
# of m rolls. Fortunately, you have also calculated the average value of the n +
# m rolls.
# You are given an integer array rolls of length m where rolls[i] is the value
# of the ith observation. You are also given the two integers mean and n.
# Return an array of length n containing the missing observations such that the
# average value of the n + m rolls is exactly mean. If there are multiple valid
# answers, return any of them. If no such array exists, return an empty array.
# The average value of a set of k numbers is the sum of the numbers divided by
# k.
# Note that mean is an integer, so the sum of the n + m rolls should be
# divisible by n + m.


from math import floor
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        def fmt(arr):
            return sorted(arr)

        assert fmt(algo(rolls=[3, 2, 4, 3], mean=4, n=2)) == fmt([6, 6])
        assert fmt(algo(rolls=[1, 5, 6], mean=3, n=4)) == fmt([2, 3, 2, 2])
        assert fmt(algo(rolls=[1, 2, 3, 4], mean=6, n=4)) == fmt([])

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, rolls: List[int], mean: int, n: int) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      Calculate the required sum of the n values, divide by n to find initial required value of each roll, and then split the remainder between at most n values.
        Time:      O(m + n): We calculate the sum of rolls (size m), and the remainder is at most n, and we iterate remainder-many values (O(n)).
        Space:     O(1): No additional memory is used.
        Leetcode:  1009 ms runtime, 26.83 MB memory
        """

        m = len(rolls)
        m_sum = sum(rolls)

        # (m_sum + n_sum) / m_n_count = mean
        # n_sum = (mean * m_n_count) - m_sum
        n_sum = (mean * (m + n)) - m_sum

        # Not even n-rolls of 1 would suffice to reach required sum.
        if n_sum < n:
            return []

        # n_mean = n_sum / n_count
        n_mean = n_sum / n
        remaining = n_sum % n

        # A mean of more than 6 is impossible, since the highest roll value
        # is 6.
        if n_mean > 6.0:
            return []

        rolls_n = [floor(n_mean)] * n
        for i in range(0, remaining):
            rolls_n[i] += 1

        return rolls_n
