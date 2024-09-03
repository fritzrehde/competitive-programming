#!/usr/bin/env python3

# Next Greater Element I
#
# https://leetcode.com/problems/next-greater-element-i
#
# The next greater element of some element x in an array is the first greater
# element that is to the right of x in the same array.
# You are given two distinct 0-indexed integer arrays nums1 and nums2, where
# nums1 is a subset of nums2.
# For each 0 <= i < nums1.length, find the index j such that nums1[i] ==
# nums2[j] and determine the next greater element of nums2[j] in nums2. If there
# is no next greater element, then the answer for this query is -1.
# Return an array ans of length nums1.length such that ans[i] is the next
# greater element as described above.


from collections import defaultdict
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums1=[4, 1, 2], nums2=[1, 3, 4, 2]) == [-1, 3, -1]
        assert algo(nums1=[2, 4], nums2=[1, 2, 3, 4]) == [3, -1]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.precalc]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Approach:  Brute-force.
        Idea:      Find matching elements and next greater element brute force.
        Time:      O(n * m^2): Given nums1 has length n and nums2 has length m, for each i in nums1 (O(n)), we iterate over all elements j in nums2 (O(m)), and then have to find the next greater element in O(m).
        Space:     O(1): No additional memory is used.
        Leetcode:  198 ms runtime, 16.86 MB memory
        """

        def next_greater(num: int, next_nums: List[int]) -> int:
            for next_num in next_nums:
                if next_num > num:
                    return next_num
            return -1

        def generator():
            for i in range(0, len(nums1)):
                # Find the index j such that nums1[i] == nums2[j].
                for j in range(0, len(nums2)):
                    if nums1[i] == nums2[j]:
                        # Find next greater element of nums2[j].
                        yield next_greater(nums2[j], nums2[j + 1 :])

        return list(generator())

    def precalc(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Approach:  Pre-calculate next greater.
        Idea:      Find matching elements and next greater element brute force.
        Time:      O(m + n): Given nums1 has length n and nums2 has length m, we precalculate the next greater element for each element in nums2 by maintaining a stack containing any decreasing subsequence, and setting the next greater element of some items in the stack once we see a larger number (O(n), since each number is added and removed from the stack exactly once). Then, we can iterate over each number in nums1 and find its next greater element in O(1).
        Space:     O(m): We store the next greater element for all numbers in nums2.
        Leetcode:  34 ms runtime, 16.74 MB memory
        """

        # All numbers in nums2 are unique.
        next_greater = defaultdict(lambda: -1)
        decreasing_subseq: List = []
        for num in nums2:
            if len(decreasing_subseq) == 0 or num < decreasing_subseq[-1]:
                # num starts or continues decreasing subsequence.
                decreasing_subseq.append(num)
            else:
                # num breaks decreasing subsequence: it will be the next greater
                # element for all items in stack smaller than it.
                while decreasing_subseq and num > decreasing_subseq[-1]:
                    next_greater[decreasing_subseq.pop()] = num
                decreasing_subseq.append(num)

        def generator():
            for num in nums1:
                yield next_greater[num]

        return list(generator())
