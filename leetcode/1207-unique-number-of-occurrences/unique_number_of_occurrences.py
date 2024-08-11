#!/usr/bin/env python3

# Unique Number of Occurrences
#
# https://leetcode.com/problems/unique-number-of-occurrences
#
# Given an array of integers arr, return true if the number of occurrences of
# each value in the array is unique or false otherwise.


from collections import defaultdict
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(arr=[1, 2, 2, 1, 1, 3]) == True
        assert algo(arr=[1, 2]) == False
        assert algo(arr=[-3, 0, 1, -3, 1, 1, 1, -3, 10, 0]) == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.seen_hashset, solution.sorting]:
        test_algo(algo)


class Solution:
    def seen_hashset(self, arr: List[int]) -> bool:
        """
        Approach:  Maintain hashset of seen values to find duplicates.
        Idea:      Build a frequency table, and then check if any frequencies are duplicated by collecting seen frequencies in set.
        Time:      O(n): Iterate over all n numbers to build the frequency table, and then iterate over all frequency table items (at most n) to check for duplicates.
        Space:     O(n): The frequency table has at most size n and the seen frequencies set has at most size n.
        Leetcode:  33 ms runtime, 16.48 MB memory
        """

        frequencies = defaultdict(lambda: 0)
        for num in arr:
            frequencies[num] += 1

        def contains_duplicates(iterable):
            seen = set()
            for item in iterable:
                if item in seen:
                    return False
                else:
                    seen.add(item)
            return True

        return contains_duplicates(frequencies.values())

    def seen_hashset_simple(self, arr: List[int]) -> bool:
        """
        Approach:  Maintain hashset of seen values to find duplicates.
        Idea:      Build a frequency table, and then check if any frequencies are duplicated by collecting seen frequencies in set and comparing length.
        Time:      O(n): Iterate over all n numbers to build the frequency table, then collect frequency values (at most n) to set and compare length (O(1)).
        Space:     O(n): The frequency table has at most size n and the seen frequencies set has at most size n.
        Leetcode:  42 ms runtime, 16.65 MB memory
        """

        frequencies = defaultdict(lambda: 0)
        for num in arr:
            frequencies[num] += 1

        def contains_duplicates(arr):
            return len(arr) == len(set(arr))

        return contains_duplicates(frequencies.values())

    def sorting(self, arr: List[int]) -> bool:
        """
        Approach:  Sort and iterate to find seen values.
        Idea:      Build a frequency table, and then check if any frequencies are duplicated by sorting and comparing all adjacent elements for equality.
        Time:      O(n log n): Iterate over all n numbers to build the frequency table, and then sort frequencies in O(n log n) and iterate over all adjacent items (at most n) to check for duplicates.
        Space:     O(n): The frequency table has at most size n.
        Leetcode:  47 ms runtime, 16.73 MB memory
        """

        frequencies = defaultdict(lambda: 0)
        for num in arr:
            frequencies[num] += 1

        def contains_duplicates(iterable):
            sorted_items = sorted(iterable)
            for i in range(0, len(sorted_items) - 1):
                if sorted_items[i] == sorted_items[i + 1]:
                    return False
            return True

        return contains_duplicates(frequencies.values())
