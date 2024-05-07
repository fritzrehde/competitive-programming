#!/usr/bin/env python3

# Generate Parentheses
#
# https://leetcode.com/problems/generate-parentheses/
#
# Given n pairs of parentheses, write a function to generate all combinations of
# well-formed parentheses.


from typing import List


def test():
    """
    Run `pytest <this-file > `.
    """

    def test_algo(algo):
        def cmp_list(l1, l2) -> bool:
            "Check if two lists contain the same elements, where different orders are allowed."
            assert sorted(l1) == sorted(l2)

        cmp_list(algo(3), ["((()))", "(()())", "(())()", "()(())", "()()()"])

        cmp_list(algo(1), ["()"])

        # Edge case: There is exactly one way to form 0-pairs of parentheses (though 1 <= n <= 8, so n = 0 is undefined)
        cmp_list(algo(0), [""])

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.dynamic_programming]:
        test_algo(algo)


class Solution:
    def dynamic_programming(self, n: int) -> List[str]:
        """
        Approach:  Dynamic programming.
        Idea:      Form valid outer brackets, and fill the inside with results of recursive calls.
        Time:      O(n): Each subproblem takes O(1) (constant recurrence), and we have n subproblems.
        Space:     O(n): We have a DP table of length n.
        Leetcode:  Not accepted, because order of found strings is different (leetcode should disregard order for this problem, but they don't!)
        """

        # Subproblems: dp[i] contains a list of all combinations of i well-formed parentheses.
        dp = [[] for _ in range(0, n+1)]

        # Calculate dp[i] in increasing order of i, since dp[i] depends on dp[i-1] and dp[i-2] in the recurrence.
        for i in range(0, n+1):
            if i == 0:
                # Base case
                dp[i] = [""]
            elif i == 1:
                # Base case
                dp[i] = ["()"]
            else:
                # Recurrence
                lists = [
                    ["(" + inner + ")" for inner in dp[i-1]],
                    ["()" + inner + "()" for inner in dp[i-2]],
                    ["()(" + inner + ")" for inner in dp[i-2]],
                    ["(" + inner + ")()" for inner in dp[i-2]],
                ]
                # Concatenate all lists, filtering out duplicates.
                dp[i] = list(set(sum(lists, [])))

        return dp[n]
