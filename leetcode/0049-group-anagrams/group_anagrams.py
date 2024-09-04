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


from collections import Counter, defaultdict
import string
from typing import Dict, List


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
    for algo in [
        solution.sorting,
        solution.serialize_counter,
        solution.freeze_counter,
    ]:
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

    def serialize_counter(self, strs: List[str]) -> List[List[str]]:
        """
        Approach:  Uniqueness by counting letters and serializing.
        Idea:      Insert input strings into a map of anagram chars to all anagrams.
        Time:      O(n * m): For each of the n input strings, serialize it to a value all of its anagrams will also be serialized to (Counter in alphabetical order, O(m + 26) = O(m)) and add the string to its storage in the hashmap (O(1)).
        Space:     O(n): The hashmap will contain all n input strings at the end.
        Leetcode:  149 ms runtime, 19.76 MB memory
        """

        def serialize_letter_counter(letter_counter: Dict) -> str:
            def generator():
                for c in string.ascii_lowercase:
                    if (count := letter_counter.get(c, None)) is not None:
                        yield f"{c}:{count}"

            return ",".join(generator())

        def serialize_anagram(s: str) -> str:
            return serialize_letter_counter(Counter(s))

        # Map the unique characters (serialized) as a string to all
        # strings containing exactly those characters.
        anagrams = defaultdict(lambda: [])
        for s in strs:
            # NOTE: Ideally, we would just use the Counter(s) itself as a
            # string, but a hashmap is mutable and, therefore, not hashable.
            anagrams[serialize_anagram(s)].append(s)

        return list(anagrams.values())

    def freeze_counter(self, strs: List[str]) -> List[List[str]]:
        """
        Approach:  Uniqueness by counting letters and freezing.
        Idea:      Insert input strings into a map of anagram chars to all anagrams.
        Time:      O(n * m): For each of the n input strings, map word to frozen (immutable) letter Counter and add the string to its storage in the hashmap (O(1)).
        Space:     O(n): The hashmap will contain all n input strings at the end.
        Leetcode:  123 ms runtime, 29.83 MB memory
        """

        # Map the unique characters (serialized) as a string to all
        # strings containing exactly those characters.
        anagrams = defaultdict(lambda: [])
        for s in strs:
            # NOTE: Ideally, we would just use the Counter(s) itself as a
            # string, but a hashmap is mutable and, therefore, not hashable.
            anagrams[frozenset(Counter(s).items())].append(s)

        return list(anagrams.values())
