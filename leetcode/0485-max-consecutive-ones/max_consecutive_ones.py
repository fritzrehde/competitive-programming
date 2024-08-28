#!/usr/bin/env python3

# Max Consecutive Ones
#
# https://leetcode.com/problems/max-consecutive-ones
#
# Given a binary array nums, return the maximum number of consecutive 1's in the
# array.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 1, 0, 1, 1, 1]) == 3
        assert algo(nums=[1, 0, 1, 1, 0, 1]) == 2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.group_by, solution.regex]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Find all subarrays containing only 1s, and return the length of the largest one.
        Time:      O(n): Iterate over every number in the input numbers once to find 1s groups (O(n)), and then find max length group (O(n)).
        Space:     O(1): No additional memory is used.
        Leetcode:  329 ms runtime, 18.44 MB memory
        """

        def all_consecutive_1s_subarray_lengths():
            ones_subarray_len = 0
            for num in nums:
                match num:
                    case 1:
                        ones_subarray_len += 1
                    case 0:
                        yield ones_subarray_len
                        ones_subarray_len = 0
            yield ones_subarray_len

        return max(all_consecutive_1s_subarray_lengths(), default=0)

    def group_by(self, nums: List[int]) -> int:
        """
        Approach:  Iterator group by.
        Idea:      Find all subarrays containing only 1s using groupby, and return the length of the largest one.
        Time:      O(n): Iterate over every number in the input numbers once to find 1s groups (O(n)), and then find max length group (O(n)).
        Space:     O(1): No additional memory is used (the groups aren't allocated, but lazy iterators).
        Leetcode:  374 ms runtime, 22.26 MB memory
        """

        from itertools import groupby
        from more_itertools import ilen

        def all_consecutive_1s_subarray_lengths():
            for num, group in groupby(nums):
                if num == 1:
                    yield ilen(group)

        return max(all_consecutive_1s_subarray_lengths(), default=0)

    def regex(self, nums: List[int]) -> int:
        """
        Approach:  Regex.
        Idea:      Find all subarrays containing only 1s using regex.findall(1s), and return the length of the largest one.
        Time:      O(n): Iterate over every number in the input numbers once to find 1s groups (O(n)), and then find max length group (O(n)).
        Space:     O(1): No additional memory is used (the groups aren't allocated, but lazy iterators).
        Leetcode:  328 ms runtime, 24.54 MB memory
        """

        import re

        def all_consecutive_1s_subarray_lengths():
            return map(len, re.findall(r"1+", "".join(map(str, nums))))

        return max(all_consecutive_1s_subarray_lengths(), default=0)
