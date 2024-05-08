#!/usr/bin/env python3

# Maximum Subarray
#
# https://leetcode.com/problems/maximum-subarray/
#
# Given an integer array nums, find the subarray with the largest sum, and
# return its sum.


from typing import List


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # sum([4, -1, 2, 1]) == 6
        assert algo([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

        # sum([5, 4, -1, 7, 8]) == 23
        assert algo([5, 4, -1, 7, 8]) == 23

        # sum([1]) == 1
        assert algo([1]) == 1

        # Edge case: Leetcode defines it this way (though I would argue the maximum subarray is [] with sum 0).
        assert algo([-1]) == -1

        # Edge case: The maximum sum of an empty array is zero.
        assert algo([]) == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.two_parameter_dynamic_programming, solution.one_parameter_dynamic_programming]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> int:
        """
        Approach:  Brute-force.
        Idea:      Consider every possible subarray, and check if its sum is the maximum.
        Time:      O(n^3): There are n^2 possible subarrays, and calculating the sum for each is O(n).
        Space:     O(1): Only the current maximum sum is stored.
        Leetcode:  Time Limit Exceeded
        """

        max_sum = None

        n = len(nums)
        for l in range(0, n):
            for r in range(l, n):
                subarray = nums[l:r+1]

                # Update the current maximum if necessary.
                new_sum = sum(subarray)
                if max_sum is None or new_sum > max_sum:
                    max_sum = new_sum

        return max_sum if max_sum is not None else 0

    def two_parameter_dynamic_programming(self, nums: List[int]) -> int:
        """
        Approach:  Dynamic programming with two parameters.
        Idea:      Consider every possible subarray, and calculate its sum using recursive calls.
        Time:      O(n^2): We calculate dp[l][r] for all possible values of the l and r, of which there are n for both. The recurrence is O(1).
        Space:     O(n^2): The DP table is 2D where each dimension stores n elements.
        Leetcode:  Memory Limit Exceeded
        """

        max_sum = None

        n = len(nums)

        # Subproblem: dp[l][r] is the sum of a subarray starting at index l and ending at, and including, index r.
        dp = [[None] * n for _ in range(0, n)]

        # Calculate dp[l][r] in increasing order of r-l, i.e. subarray length, since dp[l][r] only depends on dp[l+1][r-1].
        for diff_l_r in range(0, n):
            # The order of calculating subproblems of the same subarray length is irrelevant.
            for l in range(n - diff_l_r):
                r = l + diff_l_r
                subarr_len = diff_l_r + 1

                if subarr_len == 1:
                    # Base case
                    dp[l][r] = nums[l]
                elif subarr_len == 2:
                    # Base case
                    dp[l][r] = nums[l] + nums[r]
                else:
                    # Recurrence:
                    dp[l][r] = nums[l] + dp[l+1][r-1] + nums[r]

                # Update the current maximum if necessary.
                new_sum = dp[l][r]
                if max_sum is None or new_sum > max_sum:
                    max_sum = new_sum

        return max_sum if max_sum is not None else 0

    def one_parameter_dynamic_programming(self, nums: List[int]) -> int:
        """
        Approach:  Dynamic programming with one parameter.
        Idea:      Calculate the maximum sum subarray ending at each possible index i in the array using the result from i-1, and take the overall maximum sum subarray.
        Time:      O(n): Each subproblem takes O(1), and there are n subproblems. Furthermore, the final answer calculation is O(n).
        Space:     O(n): The DP table is 1D with length n.
        Leetcode:  545 ms runtime, 31.12 MB memory
        """

        n = len(nums)

        # Subproblem: dp[i] is the maximum sum of a subarray ending at, and including, index i. The subarray can start anywhere from 0 to i-1.
        dp = [None for _ in range(0, n)]

        # Order of computation: Calculate dp[i] in increasing order of i, since dp[i] depends only on dp[i-1] in the recurrence.
        for i in range(0, n):
            if i == 0:
                # Base case
                dp[i] = nums[i]
            else:
                # Recurrence: We must include nums[i] (according to subproblem definition), but we only extend the subarray with the largest subarray ending at index i-1 (since the concatenation of the two subarrays still forms a valid subarray) if it has a positive sum.
                dp[i] = nums[i] + max(dp[i-1], 0)

        # Overall answer: The maximum sum subarray could end at any possible index.
        return max([dp[i] for i in range(0, n)], default=0)
