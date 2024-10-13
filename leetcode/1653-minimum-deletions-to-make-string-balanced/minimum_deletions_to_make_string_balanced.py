#!/usr/bin/env python3

# Minimum Deletions to Make String Balanced
#
# https://leetcode.com/problems/minimum-deletions-to-make-string-balanced
#
# You are given a string s consisting only of characters 'a' and 'b'​​​​.
# You can delete any number of characters in s to make s balanced. s is balanced
# if there is no pair of indices (i,j) such that i < j and s[i] = 'b' and s[j]=
# 'a'.
# Return the minimum number of deletions needed to make s balanced.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="aababbab") == 2
        assert algo(s="bbaaaaabb") == 2

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.dynamic_programming,
        solution.dynamic_programming_preprocessing,
        solution.dynamic_programming_constant,
    ]:
        test_algo(algo)


class Solution:
    def dynamic_programming(self, s: str) -> int:
        """
        Approach:  Dynamic programming.
        Idea:      ?
        Time:      O(n^2): ?
        Space:     O(n): ?
        Leetcode:  Time Limit Exceeded.
        """

        from more_itertools import ilen

        n = len(s)

        # dp[i] is the minimum number of deletions to make s[:i] balanced.
        dp = [-1 for _ in range(n)]

        # O(n^2)
        # Order of computation: dp[i] only relies on dp[i-1].
        for i in range(0, n):
            if i == 0:
                # Base case:
                # If s[i] is a "b", then every s[j] j > i would have to be a "b".
                dp[i] = 0
            else:
                # Recurrence:
                match s[i]:
                    case "a":
                        # O(n)
                        # We can either:
                        # 1. Delete all "b"s that come before, or
                        # 2. Delete this "a", and ensure the rest of the left is balanced.
                        bs_before = ilen(j for j in range(0, i) if s[j] == "b")
                        dp[i] = min(bs_before, 1 + dp[i - 1])
                    case "b":
                        # No need to delete anything.
                        dp[i] = dp[i - 1]

        # Result:
        return dp[n - 1]

    def dynamic_programming_preprocessing(self, s: str) -> int:
        """
        Approach:  Dynamic programming, with pre-processing.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(n): ?
        Leetcode:  686 ms runtime, 22.41 MB memory
        """

        n = len(s)

        # O(n)
        # bs_before[i] is the number of "b"s that come before s[i].
        bs_before = [-1 for _ in range(n)]
        bs_seen = 0
        for i in range(0, n):
            bs_before[i] = bs_seen
            if s[i] == "b":
                bs_seen += 1

        # dp[i] is the minimum number of deletions to make s[:i] balanced.
        dp = [-1 for _ in range(n)]

        # O(n)
        # Order of computation: dp[i] only relies on dp[i-1].
        for i in range(0, n):
            if i == 0:
                # Base case:
                # If s[i] is a "b", then every s[j] j > i would have to be a "b".
                dp[i] = 0
            else:
                # Recurrence:
                match s[i]:
                    case "a":
                        # We can either:
                        # 1. Delete all "b"s that come before, or
                        # 2. Delete this "a", and ensure the rest of the left is balanced.
                        dp[i] = min(bs_before[i], 1 + dp[i - 1])
                    case "b":
                        # No need to delete anything.
                        dp[i] = dp[i - 1]

        # Result:
        return dp[n - 1]

    def dynamic_programming_constant(self, s: str) -> int:
        """
        Approach:  Dynamic programming, with constant space.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  399 ms runtime, 17.64 MB memory
        """

        n = len(s)

        # bs_before[i] is the number of "b"s that come before s[i].
        bs_before_i = 0

        # dp[i] is the minimum number of deletions to make s[:i] balanced.
        dp_i = -1

        # O(n)
        # Order of computation: dp[i] only relies on dp[i-1].
        for i in range(0, n):
            if i == 0:
                # Base case:
                # If s[i] is a "b", then every s[j] j > i would have to be a "b".
                dp_i = 0
            else:
                # Recurrence:
                match s[i]:
                    case "a":
                        # We can either:
                        # 1. Delete all "b"s that come before, or
                        # 2. Delete this "a", and ensure the rest of the left is balanced.
                        dp_i = min(bs_before_i, 1 + dp_i)
                    case "b":
                        # No need to delete anything.
                        dp_i = dp_i

            if s[i] == "b":
                bs_before_i += 1

        # Result:
        return dp_i
