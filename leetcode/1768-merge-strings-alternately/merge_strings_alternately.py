#!/usr/bin/env python3

# Merge Strings Alternately
#
# https://leetcode.com/problems/merge-strings-alternately
#
# You are given two strings word1 and word2. Merge the strings by adding letters
# in alternating order, starting with word1. If a string is longer than the
# other, append the additional letters onto the end of the merged string.
# Return the merged string.


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(word1 = "abc", word2 = "pqr") == "apbqcr"
        assert algo(word1 = "ab", word2 = "pqrs") == "apbqrs"
        assert algo(word1 = "abcd", word2 = "pq") == "apbqcd"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.two_pointer, solution.one_pointer, solution.functional]:
        test_algo(algo)


class Solution:
    def two_pointer(self, word1: str, word2: str) -> str:
        """
        Approach:  Two pointer.
        Idea:      First take a char from each word until either is empty, then take rest from non-empty word.
        Time:      O(n): We iterate over every element of each of the elements.
        Space:     O(1): We store no additional memory.
        Leetcode:  34 ms runtime, 16.54 MB memory
        """

        output = ""

        word1_idx = 0
        word2_idx = 0

        while word1_idx < len(word1) and word2_idx < len(word2):
            output += word1[word1_idx]
            output += word2[word2_idx]
            word1_idx += 1
            word2_idx += 1
        
            
        # Consume remaining.
        if word1_idx < len(word1):
            output += word1[word1_idx:]
        elif word2_idx < len(word2):
            output += word2[word2_idx:]

        return output

    def one_pointer(self, word1: str, word2: str) -> str:
        """
        Approach:  One pointer.
        Idea:      First take a char from each word until either is empty, then take rest from non-empty word.
        Time:      O(n): We iterate over every element of each of the elements.
        Space:     O(1): We store no additional memory.
        Leetcode:  24 ms runtime, 16.56 MB memory
        """

        output = ""

        i = 0

        while i < len(word1) and i < len(word2):
            output += word1[i]
            output += word2[i]
            i += 1
        
            
        # Consume remaining.
        if i < len(word1):
            output += word1[i:]
        elif i < len(word2):
            output += word2[i:]

        return output

    def functional(self, word1: str, word2: str) -> str:
        """
        Approach:  Functional programming approach.
        Idea:      Zip words together, and fill in missing chars of shorter word with empty string.
        Time:      O(n): We iterate over every element of each of the elements.
        Space:     O(1): We store no additional memory.
        Leetcode:  27 ms runtime, 16.54 MB memory
        """

        import itertools

        return "".join(f"{char1}{char2}" for (char1, char2) in itertools.zip_longest(word1, word2, fillvalue=""))

