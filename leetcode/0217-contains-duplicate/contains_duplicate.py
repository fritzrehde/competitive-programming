#!/usr/bin/env python3

# Contains Duplicate
#
# https://leetcode.com/problems/contains-duplicate
#
# Given an integer array nums, return true if any value appears at least twice
# in the array, and return false if every element is distinct.


from collections import Counter
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 2, 3, 1]) == True
        assert algo(nums=[1, 2, 3, 4]) == False
        assert algo(nums=[1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.counter, solution.set, solution.sort]:
        test_algo(algo)


class Solution:
    def counter(self, nums: List[int]) -> bool:
        """
        Approach:  Count hashmap.
        Idea:      Store the count of each element in a hashmap, and then check if any counts are >= 2.
        Time:      O(n): For each of the n elements, update the hashmap (O(1)).
        Space:     O(n): The hashmap has size at most n.
        Leetcode:  452 ms runtime, 34.66 MB memory
        """

        return any(count >= 2 for (_elem, count) in Counter(nums).items())

    def set(self, nums: List[int]) -> bool:
        """
        Approach:  Collect to set.
        Idea:      The numbers contain duplicates if the length of its set is smaller than the numbers.
        Time:      O(n): For each of the n elements, insert into set (O(1)).
        Space:     O(n): The set has size at most n.
        Leetcode:  425 ms runtime, 31.94 MB memory
        """

        return len(set(nums)) < len(nums)

    def sort(self, nums: List[int]) -> bool:
        """
        Approach:  Check adjacent sorted elements.
        Idea:      Sort the array, and then check if any adjacent elements are equal.
        Time:      O(n log n): Sort the array (O(n log n)) and check if any adjacent elements are equal (O(n)).
        Space:     O(1): No additional memory is used (assuming sorting uses O(1)).
        Leetcode:  482 ms runtime, 28.34 MB memory
        """

        nums.sort()
        return any(nums[i - 1] == nums[i] for i in range(1, len(nums)))
