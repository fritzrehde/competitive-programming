#!/usr/bin/env python3

# Minimum Increment To Make Array Unique
#
# https://leetcode.com/problems/minimum-increment-to-make-array-unique/
#
# You are given an integer array nums. In one move, you can pick an index i
# where 0 <= i < nums.length and increment nums[i] by 1.
#
# Return the minimum number of moves to make every value in nums unique.
#
# The test cases are generated so that the answer fits in a 32-bit integer.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # After 1 move, the array could be [1, 2, 3]
        assert algo([1, 2, 2]) == 1

        # After 6 moves, the array could be [3, 4, 1, 2, 5, 7]
        assert algo([3, 2, 1, 2, 1, 7]) == 6

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Sort the array, after which we can greedily say that every inversion needs to be corrected by incrementing the right element until it is larger than the left.
        Time:      O(n log n): Sorting the array takes O(n log n), and iterating over it to fix the inversions takes O(n).
        Space:     O(n): Sorting an array of length n (with mergesort) uses O(n).
        Leetcode:  665 ms runtime, 30.14 MB memory
        """

        nums.sort()
        moves = 0

        def make_moves(i: int, n: int):
            """Make n moves at index i."""
            nonlocal moves
            nums[i] += n
            moves += n

        for i in range(0, len(nums) - 1):
            # Found an inversion.
            if nums[i] >= nums[i + 1]:
                # Make moves until nums[i+1] is exactly 1 larger than nums[i].
                n = nums[i] - nums[i + 1] + 1
                make_moves(i + 1, n)

        return moves
