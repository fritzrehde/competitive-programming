#!/usr/bin/env python3

# String Compression III
#
# https://leetcode.com/problems/string-compression-iii
#
# Given a string word, compress it using the following algorithm:
#
# Begin with an empty string comp. While word is not empty, use the following
# operation:
#
#
# Remove a maximum length prefix of word made of a single character c repeating
# at most 9 times.
# Append the length of the prefix followed by c to comp.
#
#
#
# Return the string comp.


from typing import List


def test():
    """
    Run `pytest <this-file>`.
    """

    def test_algo(algo):
        assert algo(word="abcde") == "1a1b1c1d1e"
        assert algo(word="aaaaaaaaaaaaaabb") == "9a5a2b"

    # Test all different algorithms/implementations
    solution = Solution()
    for algo in [solution.string_collection, solution.list_collection]:
        test_algo(algo)


class Solution:
    def string_collection(self, word: str) -> str:
        """
        Approach:  Collect result as string.
        Idea:      Collect the compressed data into a string, and return it.
        Time:      O(n): Iterate of each of the input chars, and add to compressed array (O(1)).
        Space:     O(1): The result is collected in an out-of-place compressed array of length at most 2n.
        Leetcode:  860 ms runtime, 19.12 MB memory
        """

        def digits(num: int) -> str:
            return str(num)

        compressed = ""

        def append_to_compressed(s: str):
            nonlocal compressed
            compressed += s

        n = len(word)
        i = 0
        while i < n:
            curr_char = word[i]
            curr_char_count = 0
            while i < n and word[i] == curr_char and curr_char_count < 9:
                curr_char_count += 1
                i += 1

            append_to_compressed(digits(curr_char_count) + curr_char)

        return compressed

    def list_collection(self, word: str) -> str:
        """
        Approach:  Collect result as list.
        Idea:      Collect the compressed data into an array, and return it.
        Time:      O(n): Iterate of each of the input chars, and add to compressed array (O(1)).
        Space:     O(1): The result is collected in an out-of-place compressed array of length at most 2n.
        Leetcode:  320 ms runtime, 20.03 MB memory
        """

        def digits(num: int) -> str:
            return str(num)

        compressed: List[str] = []

        def append_to_compressed(s: str):
            nonlocal compressed
            compressed.extend(s)

        n = len(word)
        i = 0
        while i < n:
            curr_char = word[i]
            curr_char_count = 0
            while i < n and word[i] == curr_char and curr_char_count < 9:
                curr_char_count += 1
                i += 1

            append_to_compressed(digits(curr_char_count) + curr_char)

        return "".join(compressed)
