#!/usr/bin/env python3

# Reverse Vowels of a String
#
# https://leetcode.com/problems/reverse-vowels-of-a-string
#
# Given a string s, reverse only all the vowels in the string and return it.
# The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower
# and upper cases, more than once.


import itertools


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="hello") == "holle"
        assert algo(s="leetcode") == "leotcede"
        assert algo(s="aA") == "Aa"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.two_pointer]:
        test_algo(algo)


class Solution:
    def two_pointer(self, s: str) -> str:
        """
        Approach:  Two pointer.
        Idea:      Move two pointers from the left and right towards the middle. Everytime the left and right pointer are both pointing to a vowel, swap the vowels (essentially reversing them).
        Time:      O(n): Each char will be the left or right pointer exactly once.
        Space:     O(n): We are forced to construct an O(n) char list, since python strings are immutable.
        Leetcode:  46 ms runtime, 17.48 MB memory
        """

        def is_vowel(char: str) -> bool:
            return char.lower() in ["a", "e", "i", "o", "u"]

        n = len(s)
        # NOTE: We must are forced to convert to char list and back because python strings are immutable.
        chars = list(s)
        (l, r) = (0, n - 1)
        while l < r:
            # Move the left pointer to the next vowel.
            while l < r and not is_vowel(chars[l]):
                l += 1
            # Move the right pointer to the next vowel.
            while l < r and not is_vowel(chars[r]):
                r -= 1
            # Swap the vowels.
            (chars[l], chars[r]) = (chars[r], chars[l])
            l += 1
            r -= 1

        return "".join(chars)
