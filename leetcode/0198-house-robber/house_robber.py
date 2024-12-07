#!/usr/bin/env python3

# House Robber
#
# https://leetcode.com/problems/house-robber
#
# You are a professional robber planning to rob houses along a street. Each
# house has a certain amount of money stashed, the only constraint stopping you
# from robbing each of them is that adjacent houses have security systems
# connected and it will automatically contact the police if two adjacent houses
# were broken into on the same night.
# Given an integer array nums representing the amount of money of each house,
# return the maximum amount of money you can rob tonight without alerting the
# police.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[1, 2, 3, 1]) == 4
        assert algo(nums=[2, 7, 9, 3, 1]) == 12
        assert algo(nums=[1, 2]) == 2
        assert algo(nums=[4]) == 4

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dp, solution.dp_mem_optized]:
        test_algo(algo)


class Solution:
    def dp(self, nums: List[int]) -> int:
        """
        Approach:  DP.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(n): ?
        Leetcode:  0 ms runtime, 17.37 MB memory
        """

        n = len(nums)

        # dp[i] is the max amount of money we can rob, given that no two
        # consecutive houses are robbed, considering houses 0 to i (0-indexed,
        # exclusive). dp[i] doesn't necessarily mean that we rob house i, just
        # that we have the option to (whether that is optimal is a different
        # question).
        dp = [-1 for _ in range(n)]

        for i in range(0, n):
            match i:
                # Base cases:
                case 0:
                    # We can either rob or not rob house i, and since all house values are
                    # positive, it's never worse to rob the house.
                    dp[0] = nums[0]
                case 1:
                    # We cannot rob both houses 0 and 1, so rob the one that maximises
                    # profits.
                    dp[1] = max(nums[0], nums[1])
                case _:
                    # Recurrence:
                    # We can:
                    # - Rob house i, but then we can't rob house i-1.
                    # - Don't rob house i, so we can (decide to) rob house i-1.
                    dp[i] = max(nums[i] + dp[i - 2], dp[i - 1])

        return dp[n - 1]

    def dp_mem_optized(self, nums: List[int]) -> int:
        """
        Approach:  DP, with optimal memory usage.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  0 ms runtime, 17.27 MB memory
        """

        n = len(nums)

        # dp[i] is the max amount of money we can rob, given that no two
        # consecutive houses are robbed, considering houses 0 to i (0-indexed,
        # exclusive). dp[i] doesn't necessarily mean that we rob house i, just
        # that we have the option to (whether that is optimal is a different
        # question).
        # Since our recurrence only involves the dp[i-2] and dp[i-1], that's all
        # we have to store.
        dp_i_2, dp_i_1 = -1, -1

        for i in range(0, n):
            match i:
                # Base cases:
                case 0:
                    # We can either rob or not rob house i, and since all house values are
                    # positive, it's never worse to rob the house.
                    dp_i = nums[0]
                case 1:
                    # We cannot rob both houses 0 and 1, so rob the one that maximises
                    # profits.
                    dp_i = max(nums[0], nums[1])
                case _:
                    # Recurrence:
                    # We can:
                    # - Rob house i, but then we can't rob house i-1.
                    # - Don't rob house i, so we can (decide to) rob house i-1.
                    dp_i = max(nums[i] + dp_i_2, dp_i_1)

            dp_i_2, dp_i_1 = dp_i_1, dp_i

        return dp_i
