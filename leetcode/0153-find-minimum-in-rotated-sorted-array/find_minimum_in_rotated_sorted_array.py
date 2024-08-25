#!/usr/bin/env python3

# Find Minimum in Rotated Sorted Array
#
# https://leetcode.com/problems/find-minimum-in-rotated-sorted-array
#
# Suppose an array of length n sorted in ascending order is rotated between 1
# and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:
#
# [4,5,6,7,0,1,2] if it was rotated 4 times.
# [0,1,2,4,5,6,7] if it was rotated 7 times.
#
# Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results
# in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].
# Given the sorted rotated array nums of unique elements, return the minimum
# element of this array.
# You must write an algorithm that runs in O(log n) time.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[3, 4, 5, 1, 2]) == 1
        assert algo(nums=[4, 5, 6, 7, 0, 1, 2]) == 0
        assert algo(nums=[11, 13, 15, 17]) == 11
        assert algo(nums=[2, 1]) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.binary_search]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Use the built-in min function.
        Time:      O(n): Iterate over every element to check which is smallest.
        Space:     O(1): No additional memory was used.
        Leetcode:  36 ms runtime, 16.65 MB memory
        """

        return min(nums)

    def binary_search(self, nums: List[int]) -> int:
        """
        Approach:  Binary Search.
        Idea:      Find the inflection point (e.g. 1 would be inflection point in 3,4,5,1,2) with binary search, and min will then be the first element right of inflection point.
        Time:      O(log n): Binary searching n elements takes O(log n).
        Space:     O(1): No additional memory was used.
        Leetcode:  43 ms runtime, 16.69 MB memory
        """

        n = len(nums)

        def find_inflection_point() -> int:
            first = nums[0]
            l, r = 0, n - 1

            if nums[l] < nums[r]:
                # There is no rotation.
                return 0

            while l < r:
                m = (l + r) // 2
                if nums[m] > first:
                    # m is left of inflection point => search right.
                    l = m + 1
                elif nums[m] < first:
                    # m is right of inflection point => search left.
                    r = m
                elif nums[m] == first:
                    # m is left of inflection point => search right.
                    l = m + 1

            return l

        inflection_point = find_inflection_point()

        # First element in right half is minimum.
        return nums[inflection_point]
