#!/usr/bin/env python3

# Valid Anagram
#
# https://leetcode.com/problems/valid-anagram
#
# Given two strings s and t, return true if t is an anagram of s, and false
# otherwise.
# An Anagram is a word or phrase formed by rearranging the letters of a
# different word or phrase, typically using all the original letters exactly
# once.


from collections import defaultdict
from typing import Dict


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(s="anagram", t="nagaram") == True
        assert algo(s="rat", t="car") == False
        assert algo(s="aa", t="a") == False

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [
        solution.char_counting,
        solution.sorted,
        solution.char_counting_improved,
    ]:
        test_algo(algo)


class Solution:
    def char_counting(self, s: str, t: str) -> bool:
        """
        Approach:  Count char occurences.
        Idea:      For each string, count the character occurences, and compare.
        Time:      O(n): Given n characters in total (in both strings), iterate over each string once to count its chars.
        Space:     O(n): Store the char counts for each string in a hashmap.
        Leetcode:  41 ms runtime, 16.83 MB memory
        """

        def counter(s: str):
            char_counts = defaultdict(lambda: 0)
            for c in s:
                char_counts[c] += 1
            return char_counts

        return counter(s) == counter(t)

    def sorted(self, s: str, t: str) -> bool:
        """
        Approach:  Sort strings.
        Idea:      Sort the characters in each string and compare.
        Time:      O(n log n): Given n characters in total (in both strings), sort each string with merge sort.
        Space:     O(1): No additional memory is used (assuming sorting takes no memory).
        Leetcode:  47 ms runtime, 17.43 MB memory
        """

        return sorted(s) == sorted(t)

    def char_counting_improved(self, s: str, t: str) -> bool:
        """
        Approach:  Count char occurences, with early exit.
        Idea:      Count the chars for one string, and then subtract counts of other string from original count.
        Time:      O(n): Given n characters in total (in both strings), iterate over each string once to count its chars.
        Space:     O(n): Store the char counts for each string in a hashmap.
        Leetcode:  51 ms runtime, 16.96 MB memory
        """

        char_counts = defaultdict(lambda: 0)

        for c in s:
            char_counts[c] += 1

        for c in t:
            char_counts[c] -= 1

            # Early exit.
            if char_counts[c] < 0:
                return False

        return all(count == 0 for count in char_counts.values())
