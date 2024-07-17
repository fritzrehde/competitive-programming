#!/usr/bin/env python3

# Top K Frequent Words
#
# https://leetcode.com/problems/top-k-frequent-words/
#
# Given an array of strings words and an integer k, return the k most frequent
# strings.
#
# Return the answer sorted by the frequency from highest to lowest. Sort the
# words with the same frequency by their lexicographical order.


from collections import defaultdict
from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(words=["i", "love", "leetcode", "i", "love", "coding"], k=2) == ["i", "love"]

        assert algo(words=["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], k=4) == ["the", "is", "sunny", "day"]

        # Check that same frequency (a and b) are sorted lexicographically.
        assert algo(words=["b", "a", "a", "a", "a", "b", "b", "b", "c"], k=3) == ["a", "b", "c"]

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.brute_force]:
        test_algo(algo)


class Solution:
    def brute_force(self, words: List[str], k: int) -> List[str]:
        """
        Approach:  Brute-force.
        Idea:      Collect a frequency hashmap, and sort it by occurences, descendingly, and word, ascendingly, and get first k elements.
        Time:      O(n log n): We only sort the aggregated hashmap, the size of which should be smaller that n (size of words) on average if words occur multiple times.
        Space:     O(n): Store a hashmap mapping every word to its number of occurences.
        Leetcode:  54 ms runtime, 16.52 MB memory
        """

        freq = defaultdict(lambda: 0)
        for word in words:
            freq[word] += 1

        def sort_key(item):
            word, occurences = item
            # Sort by occurences, descendingly, and then by word (alphabetically), ascendingly.
            return (-occurences, word)

        return [word for (word, _occurences) in sorted(freq.items(), key=sort_key)][:k]
