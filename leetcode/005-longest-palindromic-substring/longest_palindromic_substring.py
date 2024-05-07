#!/usr/bin/env python3

# Longest Palindromic Substring
#
# https://leetcode.com/problems/longest-palindromic-substring/
#
# Given a string s, return the longest palindromic substring in s.


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        assert algo("babad") == "bab"

        assert algo("cbbd") == "bb"

        # Edge case: every char is unique
        assert algo("abc") == "a"

        # Edge case: every char is identical
        assert algo("aaa") == "aaa"

        # Edge case: single char is palindromic
        assert algo("a") == "a"

        # Edge case: empty string is palindromic
        assert algo("") == ""

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force, solution.dynamic_programming, solution.dynamic_programming_optimised_allocations]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str) -> str:
        """
        Approach:  Brute-force.
        Idea:      For every possible substring, check if it is palindromic, and take the longest one.
        Time:      O(n^3): Getting all possible substrings takes O(n^2), but checking whether a substring is palindromic also takes O(n).
        Space:     O(n^2): We store all possible substrings as new strings temporarily (but this is simply an unnecessary string copy by Python).
        Leetcode:  Time Limit Exceeded
        """

        def is_palindromic(s: str) -> bool:
            "Check if a string is palindromic."
            n = len(s)
            # Iterate from left and right and check if all seen elements are equal.
            for i in range(0, n//2):
                if s[i] != s[n-i-1]:
                    return False
            return True

        longest_palindrome = ""
        # Check all possible substrings.
        for l in range(0, len(s)):
            for r in range(l, len(s)):
                substring = s[l:r+1]
                if is_palindromic(substring):
                    # Update longest palindrome if necessary.
                    if len(substring) > len(longest_palindrome):
                        longest_palindrome = substring

        return longest_palindrome

    def dynamic_programming(self, s: str) -> str:
        """
        Approach:  Dynamic Programming.
        Idea:      Use a DP table to store whether the substring starting at index l and ending at index r (dp[l][r]) is a palindrome or not.
        Time:      O(n^2): By building the table from the bottom-up (in increasing order of r-l, i.e. substring length), we can use previous subproblems to determine if the substring from l to r is palindromic in O(1).
        Space:     O(n^2): The DP table has an entry for every possible substring starting at index l and ending at index r (dp[l][r]). There are n possible values for both l and r.
        Leetcode:  2851 ms runtime, 24.30 MB memory
        """

        longest_palindrome = ""

        n = len(s)

        # dp[l][r] is True if the substring from index l to r is a palindrome, and False otherwise.
        dp = [[False] * n for _ in range(0, n)]

        # Calculate dp[l][r] for in increasing order of r-l, i.e. substring length.
        for diff_l_r in range(0, n):
            # The order of calculating subproblems of the same substring length is irrelevant.
            for l in range(n - diff_l_r):
                r = l + diff_l_r
                substr_len = diff_l_r + 1

                if substr_len == 1:
                    # Base case: Any substring with only one element is a palindrome.
                    dp[l][r] = True
                elif substr_len == 2:
                    # Base case: Any substring with two elements is a palindrome if the elements are equal.
                    dp[l][r] = (s[l] == s[r])
                else:
                    # Recurrence: A substring is a palindrome if the outer-most elements are equal and the remaining inner elements are also a palindrome.
                    dp[l][r] = (s[l] == s[r] and dp[l+1][r-1])

                # Update the longest palindrome if necessary.
                if dp[l][r] and substr_len > len(longest_palindrome):
                    longest_palindrome = s[l:r+1]

        return longest_palindrome

    def dynamic_programming_optimised_allocations(self, s: str) -> str:
        """
        Approach:  Dynamic Programming, but store indices rather than substrings.
        Idea:      Same as the regular dynamic programming solution, but only store indices of the current longest palindrome instead of the substring itself (to save on allocations).
        Time:      O(n^2): Same as regular dynamic programming solution.
        Space:     O(n^2): Same as regular dynamic programming solution.
        Leetcode:  3082 ms runtime, 24.36 MB memory
        """

        # The left (inclusive) and right (exclusive) indices of the current longest palindrome.
        longest_palindrome = 0, 0

        n = len(s)

        # dp[l][r] is True if the substring from index l to r is a palindrome, and False otherwise.
        dp = [[False] * n for _ in range(0, n)]

        # Calculate dp[l][r] for in increasing order of r-l, i.e. substring length.
        for diff_l_r in range(0, n):
            # The order of calculating subproblems of the same substring length is irrelevant.
            for l in range(n - diff_l_r):
                r = l + diff_l_r
                substr_len = diff_l_r + 1

                if substr_len == 1:
                    # Base case: Any substring with only one element is a palindrome.
                    dp[l][r] = True
                elif substr_len == 2:
                    # Base case: Any substring with two elements is a palindrome if the elements are equal.
                    dp[l][r] = (s[l] == s[r])
                else:
                    # Recurrence: A substring is a palindrome if the outer-most elements are equal and the remaining inner elements are also a palindrome.
                    dp[l][r] = (s[l] == s[r] and dp[l+1][r-1])

                # Update the longest palindrome if necessary.
                max_l, max_r = longest_palindrome
                if dp[l][r] and substr_len > (max_r - max_l):
                    longest_palindrome = l, r+1

        l, r = longest_palindrome
        return s[l:r]
