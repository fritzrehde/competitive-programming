#!/usr/bin/env python3

# Missing Number
#
# https://leetcode.com/problems/missing-number
#
# Given an array nums containing n distinct numbers in the range [0, n], return
# the only number in the range that is missing from the array.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[3, 0, 1]) == 2
        assert algo(nums=[0, 1]) == 2
        assert algo(nums=[9, 6, 4, 2, 3, 5, 7, 0, 1]) == 8
        assert algo(nums=[1, 2]) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.maths,
        solution.maths_optimal,
        solution.difference_of_sets,
        solution.binary_search,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Save numbers as hashset.
        Idea:      Get the element range (min to max elements), and check if one is missing.
        Time:      O(n): Getting the max element takes O(n), and then we search for a missing element from 0 to the max element, n, taking O(n).
        Space:     O(n): We store the numbers input lists as a set.
        Leetcode:  106 ms runtime, 18.50 MB memory
        """
        n = len(nums)

        nums_set = set(nums)
        for i in range(0, n + 1):
            if i not in nums_set:
                return i

        raise Exception("unreachable")

    def difference_of_sets(self, nums: List[int]) -> int:
        """
        Approach:  Difference of sets.
        Idea:      Turn both [0, n] and the input numbers into sets, and their difference will be the missing element.
        Time:      O(n): Turning both into sets takes O(n) each, and taking the difference is assumed to take O(n) as well.
        Space:     O(n): Two sets with length O(n) are created.
        Leetcode:  113 ms runtime, 18.94 MB memory
        """

        n = len(nums)
        return (set(range(0, n + 1)) - set(nums)).pop()

    def maths(self, nums: List[int]) -> int:
        """
        Approach:  Sum range and numbers.
        Idea:      We can find the missing number by subtracting the sum of the numbers from the sum of [0, n].
        Time:      O(n): Summing [0, n] takes O(n), and summing the input numbers takes O(n).
        Space:     O(1): No additional memory is used.
        Leetcode:  104 ms runtime, 17.74 MB memory
        """

        # missing number = sum([0, n]) - sum(nums)
        n = len(nums)
        return sum(range(0, n + 1)) - sum(nums)

    def maths_optimal(self, nums: List[int]) -> int:
        """
        Approach:  Sum range and numbers.
        Idea:      We can find the missing number by subtracting the sum of the numbers from the sum of [0, n].
        Time:      O(n): Summing [0, n] takes O(1) using the formula for the arithmetic series, and summing the input numbers takes O(n).
        Space:     O(1): No additional memory is used.
        Leetcode:  108 ms runtime, 17.76 MB memory
        """

        def sum_first_n_even(n: int) -> int:
            """
            Return the sum of the first 1 to n (both inclusive).
            Assume n is even.
            """
            # Arithmetic series:
            # sum(1 to n)
            # = 1 + 2 + ... + (n-1) + n
            # = (1 + n) + (2 + (n-1)) + ...
            # = (1 + n) + (1 + n) + ...
            # = (n/2)(1 + n)
            return (n // 2) * (1 + n)

        def sum_first_n(n: int) -> int:
            if (n % 2) == 0:
                return sum_first_n_even(n)
            else:
                return sum_first_n_even(n - 1) + n

        # missing number = sum([0, n]) - sum(nums)
        n = len(nums)
        return sum_first_n(n) - sum(nums)

    def binary_search(self, nums: List[int]) -> int:
        """
        Approach:  Sort and binary search
        Idea:      Sort the numbers, so we can binary search for the missing number.
        Time:      O(n log n): Sorting takes O(n log n), and then we do a binary search taking O(log n).
        Space:     O(1): No additional memory is used.
        Leetcode:  121 ms runtime, 17.68 MB memory
        """

        n = len(nums)
        nums_sorted = sorted(nums)

        (l, r) = (0, n - 1)

        while l < r:
            m = (l + r) // 2
            if nums_sorted[m] == m:
                # For all k < m, nums_sorted[k] == nums_sorted[m] => search right.
                l = m + 1
            elif nums_sorted[m] < m:
                # There must be some nums_sorted[k], k < m, missing => search left.
                r = m
            elif nums_sorted[m] > m:
                # There must be some nums_sorted[k], k < m, missing => search left.
                r = m

        if l == nums_sorted[l]:
            return l + 1
        else:
            return l
