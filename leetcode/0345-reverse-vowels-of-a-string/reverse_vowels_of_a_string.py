#!/usr/bin/env python3

# Reverse Vowels of a String
#
# https://leetcode.com/problems/reverse-vowels-of-a-string
#
# Given a string s, reverse only all the vowels in the string and return it.
# The vowels are 'a', 'e', 'i', 'o', and 'u', and they can appear in both lower
# and upper cases, more than once.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        # assert algo(s="hello") == "holle"
        assert algo(s="leetcode") == "leotcede"
        assert algo(s="aA") == "Aa"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.two_pointer, solution.collect_vowels_regex, solution.collect_vowels_manual]:
        test_algo(algo)


class Solution:
    def collect_vowels_manual(self, s: str) -> str:
        """
        Approach:  Collect and substitute vowels, manually.
        Idea:      Collect all vowels in a list, and then iterate from the front, substituting each found vowel with the last vowel from our collected vowels.
        Time:      O(n): Finding all vowels takes O(n), and the replacement iteration takes O(n).
        Space:     O(n): The vowel list contains at most n elements.
        Leetcode:  54 ms runtime, 17.42 MB memory
        """

        vowels = set(["a", "e", "i", "o", "u"])

        def is_vowel(char: str) -> bool:
            return char.lower() in vowels

        seen_vowels = filter(is_vowel, s)

        # Iterate over s from the back, replacing each seen vowel with the previously collected vowels.
        chars = list(s)
        for i in reversed(range(0, len(s))):
            if is_vowel(chars[i]):
                chars[i] = next(seen_vowels)

        return "".join(chars)

    def collect_vowels_regex(self, s: str) -> str:
        """
        Approach:  Collect and substitute vowels, with regex.
        Idea:      Collect all vowels in a list, and then iterate from the front, substituting each found vowel with the last vowel from our collected vowels.
        Time:      O(n): Finding all vowels takes O(n), and the replacement iteration takes O(n).
        Space:     O(n): The vowel list contains at most n elements.
        Leetcode:  48 ms runtime, 18.46 MB memory
        """

        import re

        vowels = re.findall(r'[aeiou]', s, flags=re.IGNORECASE)
        return re.sub(r'[aeiou]', lambda m: vowels.pop(), s, flags=re.IGNORECASE)

    def two_pointer(self, s: str) -> str:
        """
        Approach:  Two pointer.
        Idea:      Move two pointers from the left and right towards the middle. Everytime the left and right pointer are both pointing to a vowel, swap the vowels (essentially reversing them).
        Time:      O(n): Each char will be the left or right pointer exactly once.
        Space:     O(n): We are forced to construct an O(n) char list, since python strings are immutable.
        Leetcode:  58 ms runtime, 17.47 MB memory
        """

        vowels = set(["a", "e", "i", "o", "u"])

        def is_vowel(char: str) -> bool:
            return char.lower() in vowels

        n = len(s)
        # NOTE: We must are forced to convert to char list and back because python strings are immutable.
        chars = list(s)
        (l, r) = (0, n - 1)
        while l < r:
            match (is_vowel(chars[l]), is_vowel(chars[r])):
                case (True, True):
                    # Swap the vowels.
                    (chars[l], chars[r]) = (chars[r], chars[l])
                    l += 1
                    r -= 1
                case (True, False):
                    # Try finding a right vowel as well.
                    r -= 1
                case (False, True):
                    # Try finding a left vowel as well.
                    l += 1
                case (False, False):
                    l += 1
                    r -= 1

        return "".join(chars)
