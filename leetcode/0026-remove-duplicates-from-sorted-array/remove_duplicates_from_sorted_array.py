#!/usr/bin/env python3

# Remove Duplicates from Sorted Array
#
# https://leetcode.com/problems/remove-duplicates-from-sorted-array
#
# Given an integer array nums sorted in non-decreasing order, remove the
# duplicates in-place such that each unique element appears only once. The
# relative order of the elements should be kept the same. Then return the number
# of unique elements in nums.
# Consider the number of unique elements of nums to be k, to get accepted, you
# need to do the following things:
#
# Change the array nums such that the first k elements of nums contain the
# unique elements in the order they were present in nums initially. The
# remaining elements of nums are not important as well as the size of nums.
# Return k.
#
# Custom Judge:
# The judge will test your solution with the following code:
#
# int[] nums = [...]; // Input array
# int[] expectedNums = [...]; // The expected answer with correct length
#
# int k = removeDuplicates(nums); // Calls your implementation
#
# assert k == expectedNums.length;
# for (int i = 0; i < k; i++) {
#     assert nums[i] == expectedNums[i];
# }
#
# If all assertions pass, then your solution will be accepted.


from typing import List

from more_itertools import sliding_window


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        def do_test(nums: List[int], output: List[int]):
            k = algo(nums)
            assert k == len(output)
            assert nums[:k] == output[:k]

        do_test(nums=[1, 1, 2], output=[1, 2])
        do_test(nums=[1, 1, 2], output=[1, 2])
        do_test(
            nums=[0, 0, 1, 1, 1, 2, 2, 3, 3, 4],
            output=[0, 1, 2, 3, 4],
        )

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.group_by, solution.two_pointer]:
        test_algo(algo)


class Solution:
    def group_by(self, nums: List[int]) -> int:
        """
        Approach:  Group by.
        Idea:      Since the numbers are already sorted, we can group them into groups with same elements, and keep only one element from each group.
        Time:      O(n): Visit each element and place it into a group (O(n)). Then, copy the first k (at most n) unique elements into the input array.
        Space:     O(n): Group by stores all elements in their respective groups.
        Leetcode:  66 ms runtime, 17.95 MB memory
        """

        from itertools import groupby

        nums[:] = (elem for (elem, _group) in groupby(nums))
        return len(nums)

    def two_pointer(self, nums: List[int]) -> int:
        """
        Approach:  Two pointer.
        Idea:      Maintain two pointers: One for iterating over the array and checking whether we have seen a new item (fast), and one that tracks where can insert an unique number we want to keep next (slow).
        Time:      O(n): The fast pointer iterates over all n elements, and the slow pointer iterates over at most all n elements (less if there are duplicated numbers).
        Space:     O(1): No additional memory is used, since we store the output in-place.
        Leetcode:  68 ms runtime, 17.92 MB memory
        """

        n = len(nums)

        k = 0

        def add_to_output(keep_idx: int):
            nonlocal k
            nums[k] = nums[keep_idx]
            k += 1

        # The first element is always part of output.
        add_to_output(0)

        for i in range(1, n):
            # Once we switch from old elem to new elem, store new elem.
            if nums[i - 1] != nums[i]:
                add_to_output(i)

        return k
