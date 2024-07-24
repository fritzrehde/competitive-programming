#!/usr/bin/env python3

# Sort Array By Increasing Frequency
#
# https://leetcode.com/problems/sort-array-by-increasing-frequency/
#
# Given an array of integers nums, sort the array in increasing order based on
# the frequency of the values. If multiple values have the same frequency, sort
# them in decreasing order.
#
# Return the sorted array.


import itertools
from collections import Counter, defaultdict
from typing import Dict, List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 1, 2, 2, 2, 3]) == [3, 1, 1, 2, 2, 2]

        assert algo(nums=[2, 3, 1, 3, 2]) == [1, 3, 3, 2, 2]

        assert algo(nums=[-1, 1, -6, 4, 5, -6, 1, 4, 1]) == [5, -1, 4, 4, -6, -6, 1, 1, 1]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.brute_force_lazy, solution.brute_force_simple]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      Create a frequency map, and then sort according to spec.
        Time:      O(n log n): Building the frequency map takes O(n), sorting takes O(n log n).
        Space:     O(n): The frequency map uses O(n) space.
        Leetcode:  51 ms runtime, 16.63 MB memory
        """

        frequency: Dict[int, int] = defaultdict(lambda: 0)
        for num in nums:
            frequency[num] += 1

        def sort_key(item):
            (num, occurences) = item
            # Sort by occurences, ascendingly, then by number value, descendingly.
            return (occurences, -num)

        return list(itertools.chain.from_iterable(([num] * occurences) for (num, occurences) in sorted(frequency.items(), key=sort_key)))

    def brute_force_lazy(self, nums: List[int]) -> List[int]:
        """
        Approach:  Brute-force, with some lazy optimisations.
        Idea:      Create a frequency map, and then sort according to spec.
        Time:      O(n log n): Building the frequency map takes O(n), sorting takes O(n log n).
        Space:     O(n): The frequency map uses O(n) space.
        Leetcode:  52 ms runtime, 16.72 MB memory
        """

        frequency: Dict[int, int] = defaultdict(lambda: 0)
        for num in nums:
            frequency[num] += 1

        def sort_key(item):
            (num, occurences) = item
            # Sort by occurences, ascendingly, then by number value, descendingly.
            return (occurences, -num)

        return list(itertools.chain.from_iterable((itertools.repeat(num, occurences)) for (num, occurences) in sorted(frequency.items(), key=sort_key)))

    def brute_force_simple(self, nums: List[int]) -> List[int]:
        """
        Approach:  Brute-force, simple.
        Idea:      Create a frequency map, and then sort according to spec.
        Time:      O(n log n): Building the frequency map takes O(n), sorting takes O(n log n).
        Space:     O(n): The frequency map uses O(n) space.
        Leetcode:  52 ms runtime, 16.54 MB memory
        """

        frequency = Counter(nums)

        def sort_key(item):
            num = item
            occurences = frequency[num]
            # Sort by occurences, ascendingly, then by number value, descendingly.
            return (occurences, -num)

        return sorted(nums, key=sort_key)
