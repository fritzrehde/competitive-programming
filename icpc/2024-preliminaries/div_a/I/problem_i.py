#!/usr/bin/env python3

# Iguana Gift


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(
                input="""iloveyou
"""
            )
            == "7"
        )
        assert (
            algo(
                input="""xoxoxoxoxoxoxoxoxoxo
"""
            )
            == "1"
        )
        assert (
            algo(
                input="""icpc
"""
            )
            == "1"
        )
        assert (
            algo(
                input="""tacocat
"""
            )
            == "0"
        )
        assert (
            algo(
                input="""x
"""
            )
            == "0"
        )

    # Test all different algorithms/implementations.
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, input=str) -> str:
        """
        Approach:  Brute force.
        Idea:      Find the longest substring that includes the last character that is a palindrome with length m. Then, we would need to add n-m characters to the back.
        Time:      O(n^2): For each position of the n positions (i) in word, check if word[i:] is a palindrome (O(n) each).
        Space:     O(n^2): Each time we check if a subarray is a palindrome (at most n times), we allocate the reversed string slice.
        """

        def is_palindrome(s: str) -> bool:
            return s == s[::-1]

        word = input.rstrip("\n")
        n = len(word)

        for i in range(0, n):
            if is_palindrome(word[i:]):
                return str(i)

        raise Exception("unreachable")
