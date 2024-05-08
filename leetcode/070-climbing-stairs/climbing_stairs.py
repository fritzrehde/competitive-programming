#!/usr/bin/env python3

# Climbing Stairs
#
# https://leetcode.com/problems/climbing-stairs/
#
# You are climbing a staircase. It takes n steps to reach the top. Each time you
# can either climb 1 or 2 steps. In how many distinct ways can you climb to the
# top?


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        # 3 ways: 1+1+1 steps, 2+1 steps, 1+2 steps
        assert algo(3) == 3

        # 2 ways: 1+1 steps, 2 steps
        assert algo(2) == 2

        # 1 way: 1 step
        assert algo(1) == 1

        # 0 ways: 1 step
        assert algo(0) == 1

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dynamic_programming]:
        test_algo(algo)


class Solution:
    def dynamic_programming(self, n: int) -> int:
        """
        Approach:  Dynamic programming.
        Idea:      Define a subproblem dp[i] as the number of ways to climb i steps, and calculate dp[i] recursively.
        Time:      O(n): Calculating each subproblem is O(1), and there are n subproblems.
        Space:     O(n): The DP table is 1D with n elements.
        Leetcode:  ? ms runtime, ? MB memory
        """

        # Subproblem: dp[i] means how many ways there are to climb i steps.
        dp = [None for _ in range(0, n+1)]

        # Order of computation: increasing order of i, since dp[i] only depends on dp[i-1] and dp[i-2] in the recurrence.
        for i in range(0, n+1):
            if i == 0:
                # Base case: there is one way to climb 0 steps, namely by doing nothing.
                dp[i] = 1
            elif i == 1:
                # Base case: there is one way to climb 1 step, namely by taking 1 step once.
                dp[i] = 1
            else:
                # Recurrence: there are dp[i-1] ways to get to step i-1, and then we can climb 1 more step, and there are dp[i-2] ways to get to step i-2, and then we can climb 2 more steps.
                dp[i] = dp[i-1] + dp[i-2]

        # Overall answer: we precisely want the number of way to climb n steps.
        return dp[n]
