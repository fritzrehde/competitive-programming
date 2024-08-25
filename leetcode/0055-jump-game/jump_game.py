#!/usr/bin/env python3

# Jump Game
#
# https://leetcode.com/problems/jump-game
#
# You are given an integer array nums. You are initially positioned at the
# array's first index, and each element in the array represents your maximum
# jump length at that position.
# Return true if you can reach the last index, or false otherwise.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(nums=[2, 3, 1, 1, 4]) == True
        assert algo(nums=[3, 2, 1, 0, 4]) == False
        assert algo(nums=[2, 0]) == True
        assert algo(nums=[5, 9, 3, 2, 1, 0, 2, 3, 3, 1, 0, 0]) == True
        assert algo(nums=[0, 2, 3]) == False

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_optimized,
        solution.dynamic_programming,
        solution.greedy,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, nums: List[int]) -> bool:
        """
        Approach:  Brute-force.
        Idea:      From each field, consider jumping from all fields leading up to and including that field, and jump as far as possible.
        Time:      O(n^2): We may have to jump from all n fields, and each time we must consider all previous fields.
        Space:     O(1): No additional memory is used.
        Leetcode:  Time Limit Exceeded.
        """

        n = len(nums)

        i = 0
        last_idx = n - 1

        while i < last_idx:
            # In each step, jump as far as possible, but you can look behind as
            # well for your next jump.
            furthest_jumpable = max(j + nums[j] for j in range(0, i + 1))

            # If we can't jump further than our current position, we will never
            # reach the last index.
            if furthest_jumpable == i:
                return False

            i = furthest_jumpable

        return True

    def brute_force_optimized(self, nums: List[int]) -> bool:
        """
        Approach:  Brute-force, optimized.
        Idea:      From each field, consider jumping from all fields leading up to and including that field, and jump as far as possible.
        Time:      O(n * max(nums)): We may have to jump from all n fields, and each time we must consider the previous max(nums) fields to jump from.
        Space:     O(1): No additional memory is used.
        Leetcode:  406 ms runtime, 17.89 MB memory
        """

        n = len(nums)

        i = 0
        last_idx = n - 1

        # The furthest we can jump, from any field.
        max_jump = max(nums)

        while i < last_idx:
            # In each step, jump as far as possible, but you can look behind as
            # well for your next jump. Only consider those fields from which we
            # have a chance of jumping further than i.
            furthest_jumpable = max(
                j + nums[j] for j in range(max(i - max_jump, 0), i + 1)
            )

            # If we can't jump further than our current position, we will never
            # reach the last index.
            if furthest_jumpable == i:
                return False

            i = furthest_jumpable

        return True

    def dynamic_programming(self, nums: List[int]) -> bool:
        """
        Approach:  Dynamic Programming.
        Idea:      Define a subproblem dp[i] as being able to reach the last index from index i.
        Time:      O(n * max(nums)): There are n subproblems, and for each we must consider at most the next max(nums) fields to jump to.
        Space:     O(n): The DP table stores n subproblem solutions.
        Leetcode:  3223 ms runtime, 18.00 MB memory
        """

        n = len(nums)

        last_idx = n - 1

        # Subproblem: dp[i] represents being able to reach the last index from
        # index i.
        dp = [False] * n

        for i in reversed(range(0, n)):
            if i == last_idx:
                # Base case: The last index is reachable from the last index.
                dp[i] = True
            else:
                furthest_jumpable = i + nums[i]
                jumpable_range = range(i + 1, min(furthest_jumpable + 1, n))
                # Recurrence: Check if we can reach any index from here from which
                # we can reach the last index.
                dp[i] = any(dp[j] for j in jumpable_range)

        return dp[0]

    def greedy(self, nums: List[int]) -> bool:
        """
        Approach:  Greedy.
        Idea:      Keep updating the furthest reachable index until we cannot jump any further.
        Time:      O(n): Visit every i at most once while iterating, and each iteration is O(1).
        Space:     O(1): No additional memory is used.
        Leetcode:  364 ms runtime, 17.96 MB memory
        """

        n = len(nums)
        last_idx = n - 1

        i = 0
        max_reachable = 0

        # Continue while we are still able to jump.
        while i < n and i <= max_reachable:
            # Check if jumping from index i gets us further than we've gotten
            # so far.
            max_reachable = max(i + nums[i], max_reachable)
            i += 1

        return max_reachable >= last_idx
