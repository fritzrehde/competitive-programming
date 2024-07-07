#!/usr/bin/env python3

# Two Sum
#
# https://leetcode.com/problems/two-sum/
#
# Given an array of integers `nums` and an integer `target`, return indices of
# the two numbers such that they add up to `target`.

# Run `pytest two_sum.py`.
def test():
    def test_algo(algo):
        # A[0] + A[1] = 2 + 7 = 9
        assert algo([2, 7, 11, 15], 9) == [0, 1]

        # A[1] + A[2] = 2 + 4 = 6
        assert algo([3, 2, 4], 6) == [1, 2]

        # A[0] + A[1] = 3 + 3 = 6
        assert algo([3, 3], 6) == [0, 1]

        # Edge case: can't sum up multiple numbers in a one-element array
        assert algo([42], 42) == None

        # Edge case: can't sum up multiple numbers in a empty array
        assert algo([], 42) == None

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.one_pass, solution.two_pass]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: list[int], target: int) -> list[int]:
        """
        Approach:  Brute-force
        Idea:      For each number, check if addition with any other number equals `target`
        Time:      O(n^2), compare each element to each other element
        Space:     O(1), no allocations
        Leetcode:  3653 ms runtime, 14.9 MB memory
        """

        len_ = len(nums)
        for i in range(len_):
            for j in range(i + 1, len_):
                if (nums[i] + nums[j] == target):
                    return [i, j]

        return None

    def one_pass(self, nums: list[int], target: int) -> list[int]:
        """
        Approach:  One-pass with dictionary
        Idea:      Only check if complement for a value has already been seen
        Time:      O(n), list is traversed once (second traversal is avoided through faster index lookup given number)
        Space:     O(n), space for hashmap
        Leetcode:  51 ms runtime, 15.1 MB memory
        """
        # Map each number to index in array
        nums_indices = dict()

        for i, num in enumerate(nums):
            complement = target - num

            # Get the complement's index if it has already been seen
            if (complement_idx := nums_indices.get(complement)) is not None:
                # Since the complement was seen before this ith element num, it must appear in the array earlier than num.
                return [complement_idx, i]
            else:
                nums_indices[num] = i

        return None

    def two_pass(self, nums: list[int], target: int) -> list[int]:
        """
        Approach:  Two-pass with dictionary.
        Idea:      Only check if complement for a value has already been seen.
        Time:      O(n), list is traversed once to build up nums_indices and once for complement search.
        Space:     O(n), space for hashmap
        Leetcode:  70 ms runtime, 17.75 MB memory
        """
        # Map each number to index in array
        nums_indices = dict()
        for i, num in enumerate(nums):
            nums_indices[num] = i

        for i, num in enumerate(nums):
            complement = target - num
            # Check if the complement exists in the array.
            if complement in nums_indices:
                complement_idx = nums_indices[complement]
                # We can't use the same index twice.
                if complement_idx != i:
                    return sorted([complement_idx, i])

        return None
