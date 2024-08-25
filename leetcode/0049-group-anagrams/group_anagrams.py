#!/usr/bin/env python3

# Group Anagrams
#
# https://leetcode.com/problems/group-anagrams
#
# Given an array of strings strs, group the anagrams together. You can return
# the answer in any order.
# An Anagram is a word or phrase formed by rearranging the letters of a
# different word or phrase, typically using all the original letters exactly
# once.


from collections import defaultdict
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def sort(list_of_lists):
        sorted(map(sorted, list_of_lists))

    def test_algo(algo):
        assert sort(
            algo(strs=["eat", "tea", "tan", "ate", "nat", "bat"])
        ) == sort(
            [
                ["bat"],
                ["nat", "tan"],
                ["ate", "eat", "tea"],
            ]
        )
        assert sort(algo(strs=[""])) == sort([[""]])
        assert sort(algo(strs=["a"])) == sort([["a"]])

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.sorting]:
        test_algo(algo)


class Solution:
    def sorting(self, strs: List[str]) -> List[List[str]]:
        """
        Approach:  Uniqueness by sorting.
        Idea:      Insert input strings into a map of anagram chars to all anagrams.
        Time:      O(n * m log m): For each of the n input strings, sort the string (O(m log m) given max string length m) and add the string to its storage in the hashmap (O(1)).
        Space:     O(n): The hashmap will contain all n input strings at the end.
        Leetcode:  82 ms runtime, 19.62 MB memory
        """

        # Map the unique characters (sorted ascendingly) as a string to all
        # strings containing exactly those characters.
        anagrams = defaultdict(lambda: [])
        for s in strs:
            anagrams["".join(sorted(s))].append(s)

        return list(anagrams.values())
