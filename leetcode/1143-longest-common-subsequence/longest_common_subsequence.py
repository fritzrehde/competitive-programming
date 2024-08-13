#!/usr/bin/env python3

# Longest Common Subsequence
#
# https://leetcode.com/problems/longest-common-subsequence
#
# Given two strings text1 and text2, return the length of their longest common
# subsequence. If there is no common subsequence, return 0.
# A subsequence of a string is a new string generated from the original string
# with some characters (can be none) deleted without changing the relative order
# of the remaining characters.
#
# For example, "ace" is a subsequence of "abcde".
#
# A common subsequence of two strings is a subsequence that is common to both
# strings.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(text1="abcde", text2="ace") == 3
        assert algo(text1="abc", text2="abc") == 3
        assert algo(text1="abc", text2="def") == 0

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.dynamic_programming,
        solution.memoized,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, text1: str, text2: str) -> int:
        """
        Approach:  Brute force.
        Idea:      Calculate lcs(i, j), the length of the longest subsequence of text1[:i] and text2[:j], recursively.
        Time:      O(2^(n+m)): There are 2^(n+m) possible subsequences, since each character from each string can either be included or not.
        Space:     O(1): No additional memory (besides OS recursion stack) is used.
        Leetcode:  Time Limit Exceeded
        """

        n = len(text1)
        m = len(text2)

        def lcs(i: int, j: int) -> int:
            """
            lcs(i, j) is the length of the longest subsequence of text1[:i] and text2[:j].
            """
            # Base case: longest subsequence where at least one of text1[:i] and text2[:j] is empty is "".
            if i == 0 or j == 0:
                return 0
            else:
                # Recurrence:
                if text1[i - 1] == text2[j - 1]:
                    return lcs(i - 1, j - 1) + 1
                else:
                    return max(lcs(i - 1, j), lcs(i, j - 1))

        return lcs(n, m)

    def memoized(self, text1: str, text2: str) -> int:
        """
        Approach:  Memoization (aka dynamic programming).
        Idea:      Calculate lcs(i, j), the length of the longest subsequence of text1[:i] and text2[:j], recursively, but cache/memoize results.
        Time:      O(n*m): Given text1 has length n and text2 length m, there are n*m subproblems, and each subproblem takes O(1) to calculate.
        Space:     O(n*m): The DP table has n*m elements.
        Leetcode:  1094 ms runtime, 310.06 MB memory
        """

        from functools import cache

        n = len(text1)
        m = len(text2)

        @cache
        def lcs(i: int, j: int) -> int:
            """
            lcs(i, j) is the length of the longest subsequence of text1[:i] and text2[:j].
            """
            # Base case: longest subsequence where at least one of text1[:i] and text2[:j] is empty is "".
            if i == 0 or j == 0:
                return 0
            else:
                # Recurrence:
                if text1[i - 1] == text2[j - 1]:
                    return lcs(i - 1, j - 1) + 1
                else:
                    return max(lcs(i - 1, j), lcs(i, j - 1))

        return lcs(n, m)

    def dynamic_programming(self, text1: str, text2: str) -> int:
        """
        Approach:  Dynamic Programming.
        Idea:      Use the subproblem that dp[i][j] is the longest subsequence of the first i characters of text1 and the first j characters of text2.
        Time:      O(n*m): Given text1 has length n and text2 length m, there are n*m subproblems, and each subproblem takes O(1) to calculate.
        Space:     O(n*m): The DP table has n*m elements.
        Leetcode:  529 ms runtime, 41.78 MB memory
        """

        n = len(text1)
        m = len(text2)

        # Subproblem: dp[i][j] is the length of the longest subsequence of text1[:i] and text2[:j].
        dp = [[None] * (m + 1) for _ in range(n + 1)]

        # Order of computation: dp[i][j] depends on dp[i-1][j-1], dp[i-1][j] and dp[i][j-1]: increasing order if i and j (in any order).
        for i in range(0, n + 1):
            for j in range(0, m + 1):
                # Base case: longest subsequence where at least one of text1[:i] and text2[:j] is empty is "".
                if i == 0 or j == 0:
                    dp[i][j] = 0
                else:
                    # Recurrence:
                    if text1[i - 1] == text2[j - 1]:
                        dp[i][j] = dp[i - 1][j - 1] + 1
                    else:
                        dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        # Result: dp[n][m]
        return dp[n][m]
