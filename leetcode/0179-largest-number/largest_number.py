#!/usr/bin/env python3

# Largest Number
#
# https://leetcode.com/problems/largest-number/
#
# Given a list of non-negative integers nums, arrange them such that they form
# the largest number and return it.
#
# Since the result may be very large, so you need to return a string instead of
# an integer.


from functools import cmp_to_key
from typing import List
import re


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[10, 2]) == "210"

        assert algo(nums=[3, 30, 34, 5, 9]) == "9534330"

        assert algo(nums=[432, 43243]) == "43243432"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.custom_sort, solution.custom_sort_simplified, solution.custom_sort_optimized]:
        test_algo(algo)


class Solution:
    def custom_sort(self, nums: List[int]) -> str:
        """
        Approach:  Sort with custom comparator.
        Idea:      Sort the numbers descendingly, but comparisons need to include the greedy observation that in numbers AB and C, for AB to be larger than C if A=B, B also needs to be larger than C.
        Time:      O(m n log n): Given a list of size n, sorting takes O(n log n) comparisons. However, each comparison takes O(m), where m is the number of digits in the larger string, 
        Space:     O(1): No additional memory is used.
        Leetcode:  44 ms runtime, 16.74 MB memory
        """

        def comparator(number_a: str, number_b: str) -> int:
            def numbers_equal(): return 0
            def number_a_smaller(): return -1
            def number_a_larger(): return 1

            (number_a_len, number_b_len) = (len(number_a), len(number_b))
            min_len = min(number_a_len, number_b_len)

            # Compare shared indices.
            (number_a_shared, number_b_shared) = (int(number_a[0:min_len]), int(number_b[0:min_len]))
            if number_a_shared < number_b_shared:
                return number_a_smaller()
            elif number_a_shared > number_b_shared:
                return number_a_larger()

            # If there is a longer number: its leftover digits must be larger than shorter number.
            if number_a_len > number_b_len:
                return comparator(number_a[min_len:], number_b)
            elif number_a_len < number_b_len:
                return comparator(number_a, number_b[min_len:])

            return numbers_equal()

        def trim_leading_zeros(number: str) -> str:
            if (m := re.search(r'0*([0-9]+)', number)):
                return m.group(1)
            else:
                raise Exception("unreachable: the regex will match any valid number")

        largest_number = "".join(sorted(map(str, nums), key=cmp_to_key(comparator), reverse=True))
        return trim_leading_zeros(largest_number)

    def custom_sort_simplified(self, nums: List[int]) -> str:
        """
        Approach:  Sort with custom comparator.
        Idea:      Sort the numbers descendingly, but comparisons need to include the greedy observation that in numbers AB and C, for AB to be larger than C if A=B, B also needs to be larger than C. This can be enforced by checking if ABC is larger than CAB.
        Time:      O(n log n): Given a list of size n, sorting takes O(n log n) comparisons. Each comparison takes O(1).
        Space:     O(1): No additional memory is used.
        Leetcode:  45 ms runtime, 16.37 MB memory
        """

        def comparator(number_a: str, number_b: str) -> int:
            return int(number_a + number_b) - int(number_b + number_a)

        def trim_leading_zeros(number: str) -> str:
            if (m := re.search(r'0*([0-9]+)', number)):
                return m.group(1)
            else:
                raise Exception("unreachable: the regex will match any valid number")

        largest_number = "".join(sorted(map(str, nums), key=cmp_to_key(comparator), reverse=True))
        return trim_leading_zeros(largest_number)

    def custom_sort_optimized(self, nums: List[int]) -> str:
        """
        Approach:  Sort with custom comparator.
        Idea:      Sort the numbers descendingly, but comparisons need to include the greedy observation that in numbers AB and C, for AB to be larger than C if A=B, B also needs to be larger than C. This can be enforced by checking if ABC is larger than CAB.
        Time:      O(n log n): Given a list of size n, sorting takes O(n log n) comparisons. Each comparison takes O(1).
        Space:     O(1): No additional memory is used.
        Leetcode:  44 ms runtime, 16.50 MB memory
        """

        def comparator(number_a: str, number_b: str) -> int:
            return int(number_a + number_b) - int(number_b + number_a)

        def trim_leading_zeros(number: str) -> str:
            # The only way there is a leading zero is if the number only consists of zeros (since we sort descendingly).
            if number[0] == "0":
                return "0"
            else:
                return number

        largest_number = "".join(sorted(map(str, nums), key=cmp_to_key(comparator), reverse=True))
        return trim_leading_zeros(largest_number)
