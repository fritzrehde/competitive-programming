#!/usr/bin/env python3

# Regular Expression Matching
#
# https://leetcode.com/problems/regular-expression-matching
#
# Given an input string s and a pattern p, implement regular expression matching
# with support for '.' and '*' where:
#
# '.' Matches any single character.​​​​
# '*' Matches zero or more of the preceding element.
#
# The matching should cover the entire input string (not partial).


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="aa", p="a") == False
        assert algo(s="aa", p="a.") == True
        assert algo(s="ab", p="a.") == True
        assert algo(s="ab", p="b.") == False
        assert algo(s="aa", p="a*") == True
        assert algo(s="ab", p=".*") == True
        assert algo(s="a", p="ab*") == True
        assert algo(s="ab", p=".*c") == False

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.brute_force,
        solution.brute_force_optimized,
        solution.dynamic_programming,
    ]:
        test_algo(algo)


class Solution:
    def brute_force(self, s: str, p: str) -> bool:
        """
        Approach:  Brute-force.
        Idea:      Match the first char of string and pattern, and then recurse into rest of each. Handle kleene star by trying all possible repetitions.
        Time:      O(?): ?
        Space:     O(1): No additional space (besides OS recursion stack) is used.
        Leetcode:  Time Limit Exceeded.
        """

        def chars_match(s_char: str, p_char: str) -> bool:
            if p_char == ".":
                return True
            else:
                return s_char == p_char

        def is_match(s: str, p: str) -> bool:
            match (s, p):
                case ("", ""):
                    return True
                case (s, ""):
                    return False
                case (s, p):
                    if len(p) >= 2 and p[1] == "*":
                        # Try any number of "a"s to replace "a*".
                        return any(
                            is_match(s, p[0] * i + p[2:])
                            for i in range(0, len(s) + 1)
                        )
                    elif len(s) == 0:
                        return False
                    else:
                        return chars_match(s[0], p[0]) and is_match(
                            s[1:], p[1:]
                        )
                case _:
                    raise Exception("unreachable")

        return is_match(s, p)

    def brute_force_optimized(self, s: str, p: str) -> bool:
        """
        Approach:  Brute-force, optimized.
        Idea:      Match the first char of string and pattern, and then recurse into rest of each. Handle kleene star by trying zero occurences or one occurence plus recursive matching of the rest.
        Time:      O(?): ?
        Space:     O(1): No additional space (besides OS recursion stack) is used.
        Leetcode:  Time Limit Exceeded.
        """

        def chars_match(s_char: str, p_char: str) -> bool:
            if p_char == ".":
                return True
            else:
                return s_char == p_char

        def is_match(s: str, p: str) -> bool:
            match (s, p):
                case ("", ""):
                    return True
                case (s, ""):
                    return False
                case (s, p):
                    if len(p) >= 2 and p[1] == "*":
                        # Try any number of "a"s to replace "a*".
                        return (
                            # - Zero occurences of "a".
                            is_match(s, p[2:])
                            # - One or more occurences of "a"a.
                            or (
                                len(s) > 0
                                and chars_match(s[0], p[0])
                                and is_match(s[1:], p)
                            )
                        )
                    elif len(s) == 0 or len(p) == 0:
                        return False
                    else:
                        return chars_match(s[0], p[0]) and is_match(
                            s[1:], p[1:]
                        )
                case _:
                    raise Exception("unreachable")

        return is_match(s, p)

    def dynamic_programming(self, s: str, p: str) -> bool:
        """
        Approach:  Dynamic Programming.
        Idea:      Match the first char of string and pattern, and then recurse into rest of each. Handle kleene star by trying zero occurences or one occurence plus recursive matching of the rest. Cache results in the DP table.
        Time:      O(n*m): There are n*m subproblems, each of which takes O(1) to solve.
        Space:     O(n*m): n*m subproblem results are stored in the DP table.
        Leetcode:  56 ms runtime, 16.77 MB memory
        """

        def chars_match(s_char: str, p_char: str) -> bool:
            if p_char == ".":
                return True
            else:
                return s_char == p_char

        n = len(s)
        m = len(p)

        # TODO: try alternate subproblem definition:
        # Subproblem: dp[i][j] means whether s[0:i] matches p[0:j].

        # Subproblem: dp[i][j] means whether s[i:] matches p[j:].
        dp = [[False] * (m + 1) for _ in range(0, n + 1)]

        # Order of computation: Decreasing order of i, decreasing order of j,
        # since dp[i][j] depends on dp[i+1][j+1].
        for i in reversed(range(0, n + 1)):
            for j in reversed(range(0, m + 1)):
                # Recurrence: dp[i][j]
                match (s[i:], p[j:]):
                    case ("", ""):
                        # Base case.
                        dp[i][j] = True
                    case (s_slice, ""):
                        # Base case.
                        dp[i][j] = False
                    case (s_slice, p_slice):
                        # Recurrence.
                        if len(p_slice) >= 2 and p_slice[1] == "*":
                            # Try any number of "a"s for to replace "a*".
                            dp[i][j] = (
                                # - Zero occurences of "a".
                                dp[i][j + 2]
                                # - One or more occurences of "a"a.
                                or (
                                    len(s_slice) > 0
                                    and chars_match(s_slice[0], p_slice[0])
                                    and dp[i + 1][j]
                                )
                            )
                        elif len(s_slice) == 0 or len(p_slice) == 0:
                            dp[i][j] = False
                        else:
                            dp[i][j] = (
                                chars_match(s_slice[0], p_slice[0])
                                and dp[i + 1][j + 1]
                            )
                    case _:
                        raise Exception("unreachable")

        # Result: dp[0][0] means whether s[0:] (i.e. s) matches p[0:] (i.e. p).
        return dp[0][0]
