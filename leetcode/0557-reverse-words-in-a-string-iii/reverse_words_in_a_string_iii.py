#!/usr/bin/env python3

# Reverse Words in a String III
#
# https://leetcode.com/problems/reverse-words-in-a-string-iii
#
# Given a string s, reverse the order of characters in each word within a
# sentence while still preserving whitespace and initial word order.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert (
            algo(s="Let's take LeetCode contest")
            == "s'teL ekat edoCteeL tsetnoc"
        )
        assert algo(s="Mr Ding") == "rM gniD"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.manual]:
        test_algo(algo)


class Solution:
    def manual(self, s: str) -> str:
        """
        Approach:  Brute-force.
        Idea:      ?
        Time:      O(n): ?
        Space:     O(1): ?
        Leetcode:  70 ms runtime, 17.20 MB memory
        """

        n = len(s)
        chars = list(s)

        def reverse_word(start_idx: int) -> int:
            """
            Reverse the word starting at a given index, and return the index of
            the first character after the word.
            """
            i = start_idx
            while i < n and chars[i] != " ":
                i += 1
            after_word_idx = i

            # Two pointer.
            l, r = start_idx, after_word_idx - 1
            while l < r:
                # Swap.
                chars[l], chars[r] = chars[r], chars[l]
                l += 1
                r -= 1

            return after_word_idx

        i = 0
        while i < n:
            # Skip whitespace, but leave unchanged.
            while i < n and chars[i] == " ":
                i += 1

            i = reverse_word(i)

        return "".join(chars)
